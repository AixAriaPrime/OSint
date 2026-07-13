import re
from typing import Any


class PhoneLookup:
    """Phone number intelligence."""

    @staticmethod
    async def lookup(phone_number: str) -> dict[str, Any]:
        clean = re.sub(r"\D", "", phone_number)
        is_valid = len(clean) in {10, 11}

        return {
            "input": phone_number,
            "cleaned": clean,
            "country_code": clean[0] if len(clean) == 11 else None,
            "area_code": clean[-10:-7] if is_valid else None,
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
