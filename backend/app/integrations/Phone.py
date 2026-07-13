import re
from typing import Any


class PhoneLookup:
    """Phone number intelligence."""

    @staticmethod
    async def lookup(phone_number: str) -> dict[str, Any]:
        clean = re.sub(r"\D", "", phone_number)
        is_valid = len(clean) in {10, 11}
        has_us_country_code = len(clean) == 11 and clean.startswith("1")
        country_code = clean[:1] if has_us_country_code else None
        area_code = clean[1:4] if has_us_country_code else clean[:3] if len(clean) == 10 else None

        return {
            "input": phone_number,
            "cleaned": clean,
            "country_code": country_code,
            "area_code": area_code,
            "phone_format": f"+{clean}" if clean else None,
            "valid": is_valid,
            "lookup_services": [
                {"name": "Truecaller", "url": "https://www.truecaller.com/"},
                {"name": "CallerID", "url": "https://www.calleridcheck.com/"},
                {"name": "NumVerify", "url": "https://numverify.com/"},
            ],
            "osint_links": {
                "whatsapp": f"https://wa.me/{clean}" if clean else None,
                "telegram": f"https://t.me/+{clean}" if clean else None,
                "signal": "https://signal.org/",
            },
        }
