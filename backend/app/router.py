from __future__ import annotations

import asyncio
import hashlib

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from loguru import logger

from .ai import generate_summary
from .cache import cache_get, cache_set
from .detector import QueryType, detect_query_type
from .integrations.anyrun import AnyRunIntegration
from .integrations.dns_lookup import DNSIntegration
from .integrations.hibp import HIBPIntegration
from .integrations.hybrid_analysis import HybridAnalysisIntegration
from .integrations.ipapi import IPAPIIntegration
from .integrations.shodan import ShodanIntegration
from .integrations.virustotal import VirusTotalIntegration, VirusTotalURLIntegration
from .integrations.whois_lookup import WhoisIntegration
from .models import SearchRequest, SearchResponse


router = APIRouter(prefix="/api")

# Integrations per query type
_INTEGRATIONS_BY_TYPE: dict[QueryType, list] = {
    QueryType.IP: [
        IPAPIIntegration(),
        ShodanIntegration(),
        VirusTotalIntegration(),
    ],
    QueryType.DOMAIN: [
        DNSIntegration(),
        WhoisIntegration(),
        VirusTotalIntegration(),
    ],
    QueryType.EMAIL: [
        HIBPIntegration(),
    ],
    QueryType.HASH: [
        VirusTotalIntegration(),
    ],
    QueryType.URL: [
        VirusTotalURLIntegration(),
        HybridAnalysisIntegration(),
        AnyRunIntegration(),
    ],
    QueryType.PHONE: [],
    QueryType.USERNAME: [],
    QueryType.UNKNOWN: [],
}


@router.post("/search", response_model=SearchResponse)
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
