"""
Logging configuration with Loguru.

Retention policies
------------------
- Application logs  : rotate daily, keep 30 days
- Audit logs        : rotate daily, keep 90 days  (immutable for compliance)
- Security events   : rotate daily, keep 1 year
- Deployment logs   : rotate daily, keep 14 days
"""
from __future__ import annotations

import logging
import sys

from loguru import logger

_CONFIGURED = False

LOG_DIR = "logs"


def configure_logging() -> None:
    """Set up all Loguru sinks.  Safe to call multiple times."""
    global _CONFIGURED
    if _CONFIGURED:
        return
    _CONFIGURED = True

    # Remove the default Loguru sink so we can replace it.
    logger.remove()

    # ── Console ────────────────────────────────────────────────────────────────
    logger.add(
        sys.stderr,
        level="INFO",
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        colorize=True,
        enqueue=True,
    )

    # ── Application logs (30 days) ─────────────────────────────────────────────
    logger.add(
        f"{LOG_DIR}/app.log",
        level="DEBUG",
        rotation="00:00",       # rotate at midnight
        retention="30 days",
        compression="gz",
        enqueue=True,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )

    # ── Audit logs (90 days, compliance) ──────────────────────────────────────
    logger.add(
        f"{LOG_DIR}/audit.log",
        level="INFO",
        rotation="00:00",
        retention="90 days",
        compression="gz",
        enqueue=True,
        filter=lambda record: record["extra"].get("log_type") == "audit",
        format="{time:YYYY-MM-DD HH:mm:ss} | AUDIT | {message}",
    )

    # ── Security events (1 year) ───────────────────────────────────────────────
    logger.add(
        f"{LOG_DIR}/security.log",
        level="WARNING",
        rotation="00:00",
        retention="365 days",
        compression="gz",
        enqueue=True,
        filter=lambda record: record["extra"].get("log_type") == "security",
        format="{time:YYYY-MM-DD HH:mm:ss} | SECURITY | {level: <8} | {message}",
    )

    # ── Deployment logs (14 days) ──────────────────────────────────────────────
    logger.add(
        f"{LOG_DIR}/deploy.log",
        level="INFO",
        rotation="00:00",
        retention="14 days",
        compression="gz",
        enqueue=True,
        filter=lambda record: record["extra"].get("log_type") == "deploy",
        format="{time:YYYY-MM-DD HH:mm:ss} | DEPLOY | {message}",
    )

    # Redirect stdlib logging → Loguru so third-party libraries are captured.
    _InterceptHandler.install()


class _InterceptHandler(logging.Handler):
    """Forward stdlib log records to Loguru."""

    @staticmethod
    def install() -> None:
        handler = _InterceptHandler()
        logging.basicConfig(handlers=[handler], level=0, force=True)
        for name in logging.root.manager.loggerDict:
            logging.getLogger(name).handlers = []
            logging.getLogger(name).propagate = True

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno  # type: ignore[assignment]

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore[assignment]
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# Convenience loggers for each category
audit_logger = logger.bind(log_type="audit")
security_logger = logger.bind(log_type="security")
deploy_logger = logger.bind(log_type="deploy")
