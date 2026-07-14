from __future__ import annotations

import hashlib
import hmac
from hmac import compare_digest

from fastapi import Depends, HTTPException, Request

from .config import settings


async def verify_webhook(request: Request, secret: str) -> bool:
    """Verify the HMAC-SHA256 signature on an incoming request.

    The caller must send the hex-encoded HMAC of the raw request body,
    signed with the shared *secret*, in the ``X-OmniTrace-Signature`` header.

    Raises:
        HTTPException(401): if the header is absent or the signature does not
            match the computed HMAC (comparison always uses ``compare_digest``
            to prevent timing attacks).

    Returns:
        ``True`` when the signature is valid.
    """
    signature = request.headers.get("X-OmniTrace-Signature")
    if not signature:
        raise HTTPException(401, "Missing signature")

    body = await request.body()
    computed = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

    if not compare_digest(computed, signature):
        raise HTTPException(401, "Invalid signature")

    return True


async def require_hmac(request: Request) -> None:
    """FastAPI dependency that enforces HMAC verification when ``HMAC_SECRET``
    is configured.  When the setting is absent the check is skipped so that
    deployments without request signing continue to work unchanged.
    """
    if settings.hmac_secret:
        await verify_webhook(request, settings.hmac_secret)
