from __future__ import annotations

import logging

import httpx

from ..config import settings
from ..models import IntegrationResult
from .base import BaseIntegration

logger = logging.getLogger(__name__)

_VT_BASE = "https://www.virustotal.com/api/v3"


class VirusTotalIntegration(BaseIntegration):
    name = "virustotal"

    async def run(self, query: str) -> IntegrationResult:
        if not settings.virustotal_api_key:
            return self._err("VIRUSTOTAL_API_KEY not configured")

        headers = {"x-apikey": settings.virustotal_api_key}

        # Determine resource type
        if "." in query and not query.replace(".", "").isdigit():
            endpoint = f"{_VT_BASE}/domains/{query}"
        elif query.replace(".", "").isdigit():
            endpoint = f"{_VT_BASE}/ip_addresses/{query}"
        else:
            # Treat as file hash
            endpoint = f"{_VT_BASE}/files/{query}"

        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(endpoint, headers=headers)
                resp.raise_for_status()
                raw = resp.json()

            attrs = raw.get("data", {}).get("attributes", {})
            stats = attrs.get("last_analysis_stats", {})
            return self._ok(
                {
                    "malicious": stats.get("malicious", 0),
                    "suspicious": stats.get("suspicious", 0),
                    "harmless": stats.get("harmless", 0),
                    "undetected": stats.get("undetected", 0),
                    "reputation": attrs.get("reputation"),
                    "categories": attrs.get("categories", {}),
                    "tags": attrs.get("tags", []),
                    "country": attrs.get("country"),
                    "as_owner": attrs.get("as_owner"),
                }
            )
        except httpx.HTTPStatusError as exc:
            return self._err(f"HTTP {exc.response.status_code}: {exc.response.text[:200]}")
        except Exception as exc:
            return self._err(str(exc))
