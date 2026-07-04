from __future__ import annotations

import logging

import httpx

from ..models import IntegrationResult
from .base import BaseIntegration

logger = logging.getLogger(__name__)


class IPAPIIntegration(BaseIntegration):
    """Free IP geolocation via ip-api.com (no key required, rate-limited)."""

    name = "ip-api"

    async def run(self, query: str) -> IntegrationResult:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"http://ip-api.com/json/{query}",
                    params={"fields": "status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,query"},
                )
                resp.raise_for_status()
                data = resp.json()

            if data.get("status") == "fail":
                return self._err(data.get("message", "ip-api lookup failed"))

            return self._ok(
                {
                    "ip": data.get("query"),
                    "country": data.get("country"),
                    "region": data.get("regionName"),
                    "city": data.get("city"),
                    "zip": data.get("zip"),
                    "lat": data.get("lat"),
                    "lon": data.get("lon"),
                    "timezone": data.get("timezone"),
                    "isp": data.get("isp"),
                    "org": data.get("org"),
                    "as": data.get("as"),
                }
            )
        except Exception as exc:
            return self._err(str(exc))
