from __future__ import annotations

import logging

import httpx

from ..config import settings
from ..models import IntegrationResult
from .base import BaseIntegration

logger = logging.getLogger(__name__)

_ANYRUN_BASE = "https://api.any.run/v1"


async def submit_to_anyrun(target: str, api_key: str) -> dict:
    """Create an interactive sandbox task on ANY.RUN for a URL.

    Args:
        target: URL string to submit for interactive analysis.
        api_key: ANY.RUN API key.

    Returns:
        A dict with ``task_id`` on success, or an ``error`` key on failure.
    """
    headers = {
        "Authorization": f"API-Key {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "obj_type": "url",
        "obj_url": target,
        "env_os": "windows",
        "env_version": "10",
        "env_bitness": "64",
        "env_type": "complete",
        "opt_network_connect": True,
        "opt_timeout": 60,
    }
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{_ANYRUN_BASE}/analysis",
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            raw = resp.json()
            data = raw.get("data", {})
            return {
                "task_id": data.get("taskid"),
                "report_url": (
                    f"https://app.any.run/tasks/{data['taskid']}"
                    if data.get("taskid")
                    else None
                ),
            }
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP {exc.response.status_code}: {exc.response.text[:200]}"}
    except Exception as exc:
        return {"error": str(exc)}


class AnyRunIntegration(BaseIntegration):
    """Submit a URL to ANY.RUN interactive sandbox and return the task metadata."""

    name = "anyrun"

    async def run(self, query: str) -> IntegrationResult:
        if not settings.anyrun_api_key:
            return self._err("ANYRUN_API_KEY not configured")
        result = await submit_to_anyrun(query, settings.anyrun_api_key)
        if "error" in result:
            return self._err(result["error"])
        return self._ok(result)
