from __future__ import annotations

import logging

import httpx

from ..config import settings
from ..models import IntegrationResult
from .base import BaseIntegration

logger = logging.getLogger(__name__)

_HA_BASE = "https://www.hybrid-analysis.com/api/v2"

# Windows 10 64-bit environment (most common for URL/file analysis)
_DEFAULT_ENV_ID = 160


async def submit_to_hybrid(target: str, api_key: str) -> dict:
    """Submit a URL to Hybrid Analysis (Falcon Sandbox) for detonation.

    Args:
        target: URL string to submit for sandbox analysis.
        api_key: Hybrid Analysis API key.

    Returns:
        A dict with submission metadata (``job_id``, ``submission_type``,
        ``environment_id``) on success, or an ``error`` key on failure.
    """
    headers = {
        "api-key": api_key,
        "user-agent": "Falcon Sandbox",
        "accept": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{_HA_BASE}/submit/url",
                headers=headers,
                data={
                    "scan_type": "all",
                    "url": target,
                    "environment_id": str(_DEFAULT_ENV_ID),
                },
            )
            resp.raise_for_status()
            raw = resp.json()
            return {
                "job_id": raw.get("job_id"),
                "submission_type": raw.get("submission_type"),
                "environment_id": raw.get("environment_id", _DEFAULT_ENV_ID),
                "sha256": raw.get("sha256"),
            }
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP {exc.response.status_code}: {exc.response.text[:200]}"}
    except Exception as exc:
        return {"error": str(exc)}


class HybridAnalysisIntegration(BaseIntegration):
    """Submit a URL to Hybrid Analysis sandbox and return the job metadata."""

    name = "hybrid_analysis"

    async def run(self, query: str) -> IntegrationResult:
        if not settings.hybrid_analysis_api_key:
            return self._err("HYBRID_ANALYSIS_API_KEY not configured")
        result = await submit_to_hybrid(query, settings.hybrid_analysis_api_key)
        if "error" in result:
            return self._err(result["error"])
        return self._ok(result)
