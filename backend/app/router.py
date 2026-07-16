from __future__ import annotations

import asyncio
import hashlib
from collections.abc import Awaitable, Callable

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi import Depends
from fastapi.responses import JSONResponse
from loguru import logger

from .auth import require_hmac

from .ai import generate_summary
from .cache import cache_get, cache_set
from .detector import QueryType, detect_query_type
from .integrations.anyrun import AnyRunIntegration
from .integrations.base import BaseIntegration
from .integrations.breach import BreachCheck
from .integrations.darkweb import DarkWebDorks
from .integrations.dns_lookup import DNSIntegration
from .integrations.domain import DomainRecon
from .integrations.email import EmailOSINT
from .integrations.hibp import HIBPIntegration
from .integrations.hybrid_analysis import HybridAnalysisIntegration
from .integrations.ipapi import IPAPIIntegration
from .integrations.phone import PhoneLookup
from .integrations.shodan import ShodanIntegration
from .integrations.telegram import TelegramOSINT
from .integrations.username import UsernameSearch
from .integrations.virustotal import VirusTotalIntegration, VirusTotalURLIntegration
from .integrations.whois_lookup import WhoisIntegration
from .models import IntegrationResult, SearchRequest, SearchResponse


router = APIRouter()


class FunctionIntegration(BaseIntegration):
    def __init__(
        self,
        name: str,
        handler: Callable[[str], Awaitable[dict]],
    ) -> None:
        self.name = name
        self._handler = handler

    async def run(self, query: str) -> IntegrationResult:
        try:
            return self._ok(await self._handler(query))
        except Exception as exc:
            return self._err(str(exc))


async def _domain_recon(query: str) -> dict:
    return await DomainRecon.recon(query)


async def _email_osint(query: str) -> dict:
    return await EmailOSINT.lookup(query)


async def _breach_email(query: str) -> dict:
    return await BreachCheck.check(query, target_type="email")


async def _darkweb_email(query: str) -> dict:
    return await DarkWebDorks.search(query, target_type="email")


async def _darkweb_domain(query: str) -> dict:
    return await DarkWebDorks.search(query, target_type="domain")


async def _phone_lookup(query: str) -> dict:
    return await PhoneLookup.lookup(query)


async def _breach_phone(query: str) -> dict:
    return await BreachCheck.check(query, target_type="phone")


async def _darkweb_phone(query: str) -> dict:
    return await DarkWebDorks.search(query, target_type="phone")


async def _username_search(query: str) -> dict:
    return await UsernameSearch.search(query)


async def _telegram_username(query: str) -> dict:
    return await TelegramOSINT.lookup(query, target_type="username")


async def _telegram_phone(query: str) -> dict:
    return await TelegramOSINT.lookup(query, target_type="phone")

# Integrations per query type
_INTEGRATIONS_BY_TYPE: dict[QueryType, list[BaseIntegration]] = {
    QueryType.IP: [
        IPAPIIntegration(),
        ShodanIntegration(),
        VirusTotalIntegration(),
    ],
    QueryType.DOMAIN: [
        DNSIntegration(),
        WhoisIntegration(),
        VirusTotalIntegration(),
        FunctionIntegration("domain_recon", _domain_recon),
        FunctionIntegration("domain_darkweb", _darkweb_domain),
    ],
    QueryType.EMAIL: [
        HIBPIntegration(),
        FunctionIntegration("email_lookup", _email_osint),
        FunctionIntegration("email_breach", _breach_email),
        FunctionIntegration("email_darkweb", _darkweb_email),
    ],
    QueryType.HASH: [
        VirusTotalIntegration(),
    ],
    QueryType.URL: [
        VirusTotalURLIntegration(),
        HybridAnalysisIntegration(),
        AnyRunIntegration(),
    ],
    QueryType.PHONE: [
        FunctionIntegration("phone_lookup", _phone_lookup),
        FunctionIntegration("phone_breach", _breach_phone),
        FunctionIntegration("phone_darkweb", _darkweb_phone),
        FunctionIntegration("phone_telegram", _telegram_phone),
    ],
    QueryType.USERNAME: [
        FunctionIntegration("username_lookup", _username_search),
        FunctionIntegration("username_telegram", _telegram_username),
    ],
    QueryType.UNKNOWN: [],
}


@router.post("/search", response_model=SearchResponse, dependencies=[Depends(require_hmac)])
async def search(request: SearchRequest) -> SearchResponse:
    query = request.query.strip()
    query_type = request.force_type or detect_query_type(query)

    # Cache key
    cache_key = f"omnisearch:{hashlib.sha256(f'{query_type}:{query}'.encode()).hexdigest()}"
    cached = await cache_get(cache_key)
    if cached:
        resp = SearchResponse(**cached)
        resp.cached = True
        return resp

    try:
        integrations = _INTEGRATIONS_BY_TYPE.get(query_type, [])
        tasks = [integration.run(query) for integration in integrations]
        results = await asyncio.gather(*tasks)

        response = SearchResponse(
            query=query,
            query_type=query_type,
            cached=False,
            results=list(results),
        )

        # AI summary
        response.ai_summary = await generate_summary(response)

        await cache_set(cache_key, response.model_dump())
        logger.info("Search completed", query=query, sources=results)
        return response
    except Exception as e:
        logger.error("API failure", error=str(e))
        raise


@router.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@router.websocket("/ws")
async def websocket_search(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            payload = await websocket.receive_json()
            query = str(payload.get("query", "")).strip()
            if not query:
                continue

            client_type = payload.get("force_type")
            if client_type is None:
                client_type = payload.get("query_type")

            query_type = detect_query_type(query)
            if client_type and client_type != "auto":
                try:
                    query_type = QueryType(client_type)
                except ValueError:
                    pass
            integrations = _INTEGRATIONS_BY_TYPE.get(query_type, [])
            accumulated: list = []

            # Stream each integration result as it arrives
            for future in asyncio.as_completed(integ.run(query) for integ in integrations):
                result = await future
                accumulated.append(result)
                await websocket.send_json(
                    SearchResponse(
                        query=query,
                        query_type=query_type,
                        cached=False,
                        results=accumulated,
                    ).model_dump(mode="json")
                )

            # Final message with AI summary and done flag
            response = SearchResponse(
                query=query,
                query_type=query_type,
                cached=False,
                results=accumulated,
                done=True,
            )
            response.ai_summary = await generate_summary(response)
            await websocket.send_json(response.model_dump(mode="json"))

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as exc:
        logger.error("WebSocket error: %s", exc)
