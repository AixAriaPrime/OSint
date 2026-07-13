from typing import Any, Dict


class UsernameSearch:
    """Cross-platform username search"""

    PLATFORMS = [
        "Twitter",
        "Instagram",
        "Facebook",
        "TikTok",
        "GitHub",
        "Reddit",
        "YouTube",
        "Steam",
        "Twitch",
        "Pinterest",
        "Medium",
        "Quora",
        "SoundCloud",
        "Vimeo",
        "Flickr",
        "Keybase",
        "Mastodon",
        "Pastebin",
        "Snapchat",
        "Discord",
    ]

    @staticmethod
    async def search(username: str) -> Dict[str, Any]:
        username = username.strip().replace("@", "")

        return {
            "username": username,
            "platforms": [
                {"platform": p, "url": f"https://{p.lower()}.com/{username}"}
                for p in UsernameSearch.PLATFORMS
            ],
            "tools": [
                {"name": "Sherlock", "url": "https://github.com/sherlock-project/sherlock"},
                {"name": "Namechk", "url": "https://namechk.com"},
                {"name": "WhatsMyName", "url": "https://whatsmyname.app"},
                {"name": "UserSearch", "url": "https://usersearch.co"},
            ],
            "search_commands": {
                "sherlock": f"python3 sherlock.py {username}",
                "whatsmyname": "Visit https://whatsmyname.app and search for username",
            },
        }
