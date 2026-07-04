from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..models import IntegrationResult


class BaseIntegration(ABC):
    name: str = "base"

    @abstractmethod
    async def run(self, query: str) -> IntegrationResult:
        ...

    def _ok(self, data: Any) -> IntegrationResult:
        return IntegrationResult(source=self.name, success=True, data=data)

    def _err(self, error: str) -> IntegrationResult:
        return IntegrationResult(source=self.name, success=False, error=error)
