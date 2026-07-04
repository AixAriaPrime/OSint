from __future__ import annotations

import asyncio
import logging
from typing import Any

from ..models import IntegrationResult
from .base import BaseIntegration

logger = logging.getLogger(__name__)


class WhoisIntegration(BaseIntegration):
    name = "whois"

    async def run(self, query: str) -> IntegrationResult:
        try:
            import whois  # type: ignore

            loop = asyncio.get_event_loop()
            w = await loop.run_in_executor(None, whois.whois, query)
            if w is None:
                return self._err("No WHOIS data returned")

            def _safe(val: Any) -> Any:
                if isinstance(val, list):
                    return [str(v) for v in val]
                return str(val) if val is not None else None

            return self._ok(
                {
                    "domain_name": _safe(w.domain_name),
                    "registrar": _safe(w.registrar),
                    "creation_date": _safe(w.creation_date),
                    "expiration_date": _safe(w.expiration_date),
                    "updated_date": _safe(w.updated_date),
                    "name_servers": _safe(w.name_servers),
                    "status": _safe(w.status),
                    "emails": _safe(w.emails),
                    "org": _safe(w.org),
                    "country": _safe(w.country),
                }
            )
        except Exception as exc:
            return self._err(str(exc))
