from typing import Any


class TelegramOSINT:
    """Telegram intelligence."""

    @staticmethod
    async def lookup(target: str, target_type: str = "username") -> dict[str, Any]:
        username = target.replace("@", "") if target_type == "username" else target

        return {
            "target": target,
            "type": target_type,
            "username_lookup": {
                "profile": f"https://t.me/{username}",
                "can_find": [
                    "Username",
                    "Display name",
                    "Bio/About",
                    "Profile photo",
                    "Premium status",
                    "Last seen",
                    "Bot status",
                ],
            },
            "phone_lookup": {
                "can_check": "Is phone registered on Telegram?",
                "cannot_do": "Get phone from username (blocked by privacy)",
            },
            "tools": [
                {"name": "TGStat", "url": "https://tgstat.com/"},
                {"name": "Tgram", "url": "https://tgram.io/"},
                {"name": "TelegramDB", "description": "Search engines"},
            ],
        }
