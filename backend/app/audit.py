"""
Audit and security event middleware.

- Every HTTP request/response is written to the audit log (90-day retention).
- Rate-limit violations and unhandled exceptions are written to the security
  log (1-year retention).
"""
from __future__ import annotations

import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from .logging_config import audit_logger, security_logger


class AuditMiddleware(BaseHTTPMiddleware):
    """Log every request to the audit sink and security events to the security sink."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.perf_counter()
        client_ip = request.client.host if request.client else "unknown"

        try:
            response: Response = await call_next(request)
        except Exception as exc:
            elapsed = (time.perf_counter() - start) * 1000
            security_logger.error(
                "Unhandled exception | ip={ip} method={method} path={path} "
                "elapsed_ms={elapsed:.1f} error={error}",
                ip=client_ip,
                method=request.method,
                path=request.url.path,
                elapsed=elapsed,
                error=repr(exc),
            )
            raise

        elapsed = (time.perf_counter() - start) * 1000
        status = response.status_code

        audit_logger.info(
            "ip={ip} method={method} path={path} status={status} elapsed_ms={elapsed:.1f}",
            ip=client_ip,
            method=request.method,
            path=request.url.path,
            status=status,
            elapsed=elapsed,
        )

        # 429 = rate-limit exceeded → security event
        if status == 429:
            security_logger.warning(
                "Rate limit exceeded | ip={ip} method={method} path={path}",
                ip=client_ip,
                method=request.method,
                path=request.url.path,
            )

        return response
