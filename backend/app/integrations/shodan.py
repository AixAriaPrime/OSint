from __future__ import annotations

import asyncio
import logging

from ..config import settings
from ..models import IntegrationResult
from .base import BaseIntegration

logger = logging.getLogger(__name__)


class ShodanIntegration(BaseIntegration):
    name = "shodan"

    async def run(self, query: str) -> IntegrationResult:
        if not settings.shodan_api_key:
            return self._err("SHODAN_API_KEY not configured")
        try:
            import shodan  # type: ignore

            api = shodan.Shodan(settings.shodan_api_key)
            loop = asyncio.get_event_loop()
            # Run blocking SDK call in thread pool
            host = await loop.run_in_executor(None, api.host, query)
            data = {
                "ip": host.get("ip_str"),
                "org": host.get("org"),
                "isp": host.get("isp"),
                "country": host.get("country_name"),
                "city": host.get("city"),
                "os": host.get("os"),
                "ports": host.get("ports", []),
                "vulns": list(host.get("vulns", {}).keys()),
                "hostnames": host.get("hostnames", []),
                "tags": host.get("tags", []),
            }
            return self._ok(data)
        except Exception as exc:
            return self._err(str(exc))
