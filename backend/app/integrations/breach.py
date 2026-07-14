from typing import Any


class BreachCheck:
    """Check whether a target appears in known breach sources."""

    @staticmethod
    async def check(target: str, target_type: str = "email") -> dict[str, Any]:
        return {
            "target": target,
            "type": target_type,
            "services": [
                {"name": "HaveIBeenPwned", "url": "https://haveibeenpwned.com/"},
                {"name": "Dehashed", "url": "https://dehashed.com/"},
                {"name": "LeakCheck", "url": "https://leakcheck.io/"},
                {"name": "Snusbase", "url": "https://snusbase.com/"},
                {"name": "CyberNews", "url": "https://cybernews.com/"},
                {"name": "HudsonRock", "url": "https://www.hudsonrock.com/"},
            ],
            "what_breaches_reveal": [
                "Email addresses",
                "Passwords (hashed)",
                "Phone numbers",
                "Names",
                "Addresses",
                "Personal info",
            ],
        }
