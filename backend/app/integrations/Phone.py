from typing import Any
import re


class PhoneLookup:
    """Phone number intelligence."""

    @staticmethod
    async def lookup(phone_number: str) -> dict[str, Any]:
        clean = re.sub(r"\D", "", phone_number)
        is_valid = len(clean) in {10, 11}
        has_us_country_code = len(clean) == 11 and clean.startswith("1")

        country_code = None
        area_code = None
        if has_us_country_code:
            country_code = clean[:1]
            area_code = clean[1:4]
        elif len(clean) == 10:
            area_code = clean[:3]

        return {
            "input": phone_number,
            "cleaned": clean,
            "country_code": country_code,
            "area_code": area_code,
            "phone_format": f"+{clean}" if is_valid else None,
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
