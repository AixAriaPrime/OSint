from typing import Any, Dict


class TelegramOSINT:
    """Telegram intelligence helper."""

    @staticmethod
    async def lookup(target: str, target_type: str = "username") -> Dict[str, Any]:
        username = target.replace("@", "") if target_type == "username" else target
        return {
            "target": target,
            "type": target_type,
            "username_lookup": {
                "profile": f"https://t.me/{username}" if username else None,
                "can_find": [
                    "Username",
                    "Display name",
                    "Bio/About",
                    "Profile photo",
                    "Bot flag",
                ],
                "tools": ["Telegram Web", "Telegram API clients"],
            },
            "phone_lookup": {
                "can_check": "Whether a number appears linked to a Telegram account.",
                "cannot_do": "Recover private number from username without access.",
                "search": "Cross-reference breach datasets for matching number.",
            },
            "tools": [
                {"name": "TGStat", "url": "https://tgstat.com/"},
                {"name": "TgramSearch", "url": "https://tgstat.com/en/search"},
            ],
        }


class SocialOmni:
    """Cross-platform username lookup helper."""

    PLATFORMS = {
        "twitter": {"url": "https://twitter.com/", "data": "Profile, posts, followers"},
        "instagram": {"url": "https://instagram.com/", "data": "Profile, posts, stories"},
        "facebook": {"url": "https://facebook.com/", "data": "Profile, friends, photos"},
        "tiktok": {"url": "https://tiktok.com/@", "data": "Profile, videos"},
        "linkedin": {"url": "https://linkedin.com/in/", "data": "Experience, connections"},
        "youtube": {"url": "https://youtube.com/@", "data": "Channels, uploads"},
        "reddit": {"url": "https://reddit.com/user/", "data": "Posts, comments, karma"},
        "github": {"url": "https://github.com/", "data": "Repos, commits, followers"},
    }

    @staticmethod
    async def search(target: str, platform: str = "all") -> Dict[str, Any]:
        if platform == "all":
            return {
                "target": target,
                "platforms": [
                    {"platform": p, "url": f"{v['url']}{target}", "data": v["data"]}
                    for p, v in SocialOmni.PLATFORMS.items()
                ],
                "cross_platform_tools": [
                    {"name": "Sherlock", "url": "https://github.com/sherlock-project/sherlock"},
                    {"name": "Namechk", "url": "https://namechk.com/"},
                    {"name": "WhatsMyName", "url": "https://whatsmyname.app/"},
                ],
            }

        selected = SocialOmni.PLATFORMS.get(platform.lower())
        if not selected:
            return {"target": target, "error": f"Unsupported platform: {platform}"}

        return {
            "target": target,
            "platform": platform.lower(),
            "url": f"{selected['url']}{target}",
            "data": selected["data"],
        }
