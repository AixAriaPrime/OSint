from typing import Any, Dict


class UsernameSearch:
    """Cross-platform username search helper."""

    PLATFORMS = [
        "twitter",
        "instagram",
        "facebook",
        "tiktok",
        "github",
        "reddit",
        "youtube",
        "steam",
        "twitch",
        "pinterest",
        "medium",
        "quora",
        "soundcloud",
        "vimeo",
        "flickr",
        "keybase",
        "mastodon",
        "pastebin",
        "snapchat",
        "discord",
    ]

    @staticmethod
    async def search(username: str) -> Dict[str, Any]:
        normalized = username.strip().replace("@", "")
        return {
            "username": normalized,
            "platforms": [
                {"platform": platform, "url": f"https://{platform}.com/{normalized}"}
                for platform in UsernameSearch.PLATFORMS
            ],
            "tools": [
                {"name": "Sherlock", "url": "https://github.com/sherlock-project/sherlock"},
                {"name": "Namechk", "url": "https://namechk.com/"},
                {"name": "WhatsMyName", "url": "https://whatsmyname.app/"},
                {"name": "UserSearch", "url": "https://usersearch.org/"},
            ],
            "search_commands": {
                "sherlock": f"python3 sherlock.py {normalized}",
                "whatsmyname": f"Search {normalized} on https://whatsmyname.app/",
            },
        }
