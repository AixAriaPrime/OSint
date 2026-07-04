from __future__ import annotations

import logging

import httpx

from ..config import settings
from ..models import IntegrationResult
from .base import BaseIntegration

logger = logging.getLogger(__name__)


class HIBPIntegration(BaseIntegration):
    """Have I Been Pwned breach lookup for email addresses."""

    name = "hibp"

    async def run(self, query: str) -> IntegrationResult:
        if not settings.hibp_api_key:
            return self._err("HIBP_API_KEY not configured")
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(
                    f"https://haveibeenpwned.com/api/v3/breachedaccount/{query}",
                    headers={
                        "hibp-api-key": settings.hibp_api_key,
                        "user-agent": "OmniTrace-OSINT",
                    },
                    params={"truncateResponse": "false"},
                )

                if resp.status_code == 404:
                    return self._ok({"breaches": [], "count": 0})

                resp.raise_for_status()
                breaches = resp.json()

            return self._ok(
                {
                    "count": len(breaches),
                    "breaches": [
                        {
                            "name": b.get("Name"),
                            "title": b.get("Title"),
                            "domain": b.get("Domain"),
                            "breach_date": b.get("BreachDate"),
                            "pwn_count": b.get("PwnCount"),
                            "data_classes": b.get("DataClasses", []),
                        }
                        for b in breaches
                    ],
                }
            )
        except httpx.HTTPStatusError as exc:
            return self._err(f"HTTP {exc.response.status_code}")
        except Exception as exc:
            return self._err(str(exc))
