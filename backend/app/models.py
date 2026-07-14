from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel

from .detector import QueryType


class SearchRequest(BaseModel):
    query: str
    force_type: Optional[QueryType] = None


class IntegrationResult(BaseModel):
    source: str
    success: bool
    data: Any = None
    error: Optional[str] = None


class SearchResponse(BaseModel):
    query: str
    query_type: QueryType
    cached: bool = False
    results: list[IntegrationResult] = []
    ai_summary: Optional[str] = None
    done: bool = False
