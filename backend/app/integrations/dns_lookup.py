from __future__ import annotations

import logging

import httpx

from ..models import IntegrationResult
from .base import BaseIntegration

logger = logging.getLogger(__name__)


class DNSIntegration(BaseIntegration):
    """DNS record lookup using a public DNS-over-HTTPS resolver."""

    name = "dns"

    async def run(self, query: str) -> IntegrationResult:
        record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]
        records: dict = {}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                for rtype in record_types:
                    try:
                        resp = await client.get(
                            "https://cloudflare-dns.com/dns-query",
                            params={"name": query, "type": rtype},
                            headers={"accept": "application/dns-json"},
                        )
                        if resp.status_code == 200:
                            data = resp.json()
                            answers = data.get("Answer", [])
                            if answers:
                                records[rtype] = [a.get("data") for a in answers]
                    except Exception:
                        pass

            return self._ok(records)
        except Exception as exc:
            return self._err(str(exc))
