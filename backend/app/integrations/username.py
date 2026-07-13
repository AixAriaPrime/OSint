from typing import Any


class UsernameSearch:
    """Cross-platform username search."""

    PLATFORMS = [
        "twitter.com",
        "instagram.com",
        "facebook.com",
        "tiktok.com/@",
        "github.com",
        "reddit.com/u",
        "youtube.com/@",
        "steamcommunity.com/id",
    ]

    @staticmethod
    async def search(username: str) -> dict[str, Any]:
        normalized = username.strip().replace("@", "")
        return {
            "username": normalized,
            "platforms": [
                {
                    "platform": platform,
                    "url": (
                        f"https://{platform[:-2]}/@{normalized}"
                        if platform.endswith("/@")
                        else f"https://{platform}/{normalized}"
                    ),
                }
                for platform in UsernameSearch.PLATFORMS
            ],
            "tools": [
                {"name": "Sherlock", "url": "https://github.com/sherlock-project/sherlock"},
                {"name": "Namechk", "url": "https://namechk.com"},
                {"name": "WhatsMyName", "url": "https://whatsmyname.app"},
            ],
        }
