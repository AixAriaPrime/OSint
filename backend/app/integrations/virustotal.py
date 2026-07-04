from __future__ import annotations

import logging

import httpx

from ..config import settings
from ..models import IntegrationResult
from .base import BaseIntegration

logger = logging.getLogger(__name__)

_VT_BASE = "https://www.virustotal.com/api/v3"

import ipaddress


def _classify(query: str) -> str:
    """Return 'ip', 'domain', or 'hash'."""
    try:
        ipaddress.ip_address(query)
        return "ip"
    except ValueError:
        pass
    # If it contains a dot but isn't purely hex it's likely a domain
    if "." in query and not all(c in "0123456789abcdefABCDEF" for c in query):
        return "domain"
    return "hash"


async def submit_to_virustotal(
    target: str, target_type: str, api_key: str
) -> dict:
    """Submit a URL or file hash to VirusTotal for analysis.

    Args:
        target: URL string or file hash to submit.
        target_type: ``"url"`` to submit a URL for scanning, ``"file"`` to
            re-analyse a file by its hash.
        api_key: VirusTotal API key.

    Returns:
        A dict containing the analysis ``id`` and ``type`` on success, or an
        ``error`` key on failure.
    """
    headers = {"x-apikey": api_key}
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            if target_type == "url":
                # VT v3 encodes the URL as url-safe base64 (no padding) for
                # the endpoint; the POST body uses plain form data.
                resp = await client.post(
                    f"{_VT_BASE}/urls",
                    headers=headers,
                    data={"url": target},
                )
            else:
                # Re-analyse an already-known file by hash
                resp = await client.post(
                    f"{_VT_BASE}/files/{target}/analyse",
                    headers=headers,
                )
            resp.raise_for_status()
            data = resp.json().get("data", {})
            return {"id": data.get("id"), "type": data.get("type")}
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP {exc.response.status_code}: {exc.response.text[:200]}"}
    except Exception as exc:
        return {"error": str(exc)}


class VirusTotalIntegration(BaseIntegration):
    name = "virustotal"

    async def run(self, query: str) -> IntegrationResult:
        if not settings.virustotal_api_key:
            return self._err("VIRUSTOTAL_API_KEY not configured")

        headers = {"x-apikey": settings.virustotal_api_key}

        # Determine resource type
        resource_type = _classify(query)
        if resource_type == "ip":
            endpoint = f"{_VT_BASE}/ip_addresses/{query}"
        elif resource_type == "domain":
            endpoint = f"{_VT_BASE}/domains/{query}"
        else:
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


class VirusTotalURLIntegration(BaseIntegration):
    """Submit a URL to VirusTotal and return the resulting analysis metadata."""

    name = "virustotal_submit"

    async def run(self, query: str) -> IntegrationResult:
        if not settings.virustotal_api_key:
            return self._err("VIRUSTOTAL_API_KEY not configured")
        result = await submit_to_virustotal(query, "url", settings.virustotal_api_key)
        if "error" in result:
            return self._err(result["error"])
        return self._ok(result)
