from __future__ import annotations

import re
from enum import Enum


class QueryType(str, Enum):
    IP = "ip"
    DOMAIN = "domain"
    EMAIL = "email"
    PHONE = "phone"
    HASH = "hash"
    USERNAME = "username"
    UNKNOWN = "unknown"


_IP_RE = re.compile(
    r"^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)
_DOMAIN_RE = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_RE = re.compile(r"^\+?[\d\s\-().]{7,20}$")
_HASH_RE = re.compile(r"^[0-9a-fA-F]{32,64}$")


def detect_query_type(query: str) -> QueryType:
    q = query.strip()
    if _IP_RE.match(q):
        return QueryType.IP
    if _EMAIL_RE.match(q):
        return QueryType.EMAIL
    if _DOMAIN_RE.match(q):
        return QueryType.DOMAIN
    if _HASH_RE.match(q):
        return QueryType.HASH
    if _PHONE_RE.match(q):
        return QueryType.PHONE
    return QueryType.USERNAME
