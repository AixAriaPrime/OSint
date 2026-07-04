from __future__ import annotations

import ipaddress
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


# Use possessive-style bounded quantifiers to avoid catastrophic backtracking.
# Each character class is atomic; no nested repetition.
_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]{1,64}@[A-Za-z0-9.\-]{1,253}\.[A-Za-z]{2,}$")
_DOMAIN_RE = re.compile(r"^(?:[A-Za-z0-9][A-Za-z0-9\-]{0,61}[A-Za-z0-9]?\.)+[A-Za-z]{2,}$")
_PHONE_RE = re.compile(r"^\+?[\d\s\-().]{7,20}$")
_HASH_RE = re.compile(r"^[0-9a-fA-F]{32,64}$")

_MAX_QUERY_LEN = 512


def detect_query_type(query: str) -> QueryType:
    q = query.strip()
    # Reject excessively long input before running regexes
    if len(q) > _MAX_QUERY_LEN:
        return QueryType.UNKNOWN

    # Use stdlib for IP validation — immune to ReDoS
    try:
        ipaddress.ip_address(q)
        return QueryType.IP
    except ValueError:
        pass

    if _EMAIL_RE.match(q):
        return QueryType.EMAIL
    if _DOMAIN_RE.match(q):
        return QueryType.DOMAIN
    if _HASH_RE.match(q):
        return QueryType.HASH
    if _PHONE_RE.match(q):
        return QueryType.PHONE
    return QueryType.USERNAME
