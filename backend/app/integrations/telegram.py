from typing import Dict, Any

class TelegramOSINT:
    """Telegram intelligence"""
    
    @staticmethod
    async def lookup(target: str, target_type: str = "username") -> Dict[str, Any]:
        
        username = target.replace("@", "") if target_type == "username" else target
        
        return 
            "target": target,
            "type": target_type,
            "username_lookup": {
                "profile": f"https://t.me/{username",
                "can_find": [
                    "Username",
                    "Display name", 
                    "Bio/About",
                    "Profile photo",
                    "Premium status",
                    "Last seen",
                    "Bot status"
                ],
                "tools": ["Apify Telegram Scraper", "Telegram API"]
            },
            "phone_lookup": 
                "can_check": "Is phone registered on Telegram?",
                "cannot_do": "Get phone from username (blocked by privacy)",
                "search": "Search breach data for phone number"
            ,
            "tools": [
                "name": "TGStat", "url": "https://tgstat.com/",
                "name": "Tgram", "url": "https://tgram.io/",
                "name": "TelegramDB", "description": "Search engines"
            ]
        }# backend/app/integrations/social.py
from typing import Dict, Any

class SocialOmni:
    """All social media platforms"""
    
    PLATFORMS = 
        "twitter": {"url": "https://twitter.com/", "data": "Profile, tweets, followers",
        "instagram": "url": "https://instagram.com/", "data": "Profile, posts, stories",
        "facebook": "url": "https://facebook.com/", "data": "Profile, friends, photos",
        "tiktok": "url": "https://tiktok.com/@", "data": "Profile, videos",
        "linkedin": "url": "https://linkedin.com/in/", "data": "Profile, experience, connections",
        "youtube": "url": "https://youtube.com/@", "data": "Channel, videos, subscribers",
        "reddit": "url": "https://reddit.com/u/", "data": "Posts, karma, subreddits",
        "discord": "url": "Check via Discord API", "data": "Profile, servers",
        "whatsapp": "url": "https://wa.me/", "data": "Profile photo, status",
        "snapchat": "url": "https://snapchat.com/add/", "data": "Snap score, stories",
        "steam": "url": "https://steamcommunity.com/id/", "data": "Games, playtime, profile",
        "twitch": "url": "https://twitch.tv/", "data": "Streams, followers, videos",
        "github": "url": "https://github.com/", "data": "Repos, commits, followers",
        "pinterest": "url": "https://pinterest.com/", "data": "Boards, pins",
        "medium": "url": "https://medium.com/@", "data": "Articles, followers",
        "quora": "url": "https://quora.com/profile/", "data": "Questions, answers",
        "onlyfans": "url": "https://onlyfans.com/", "data": "Profile, pricing",
        "patreon": "url": "https://patreon.com/", "data": "Tiers, earnings"
    }
    
    @staticmethod
    async def search(target: str, platform: str = "all") -> Dict[str, Any]:
        
        if platform == "all":
            return 
                "target": target,
                "platforms": [
                    {"platform": p, "url": f"{v['url']target", "data": v['data"]}
                    for p, v in SocialOmni.PLATFORMS.items()
                ],
                "cross_platform_tools": [
                    "name": "Sherlock", "url": "https://github.com/sherlock-project/sherlock",
                    "name": "Namechk", "url": "https://namechk.com",
                    "name": "WhatsMyName", "url": "https://whatsmyname.app"
                ]
            }
        else:
            p = SocialOmni.PLATFORMS.get(platform.lower())
            if p:
                return 
                    "target": target,
                    "platform": platform,
                    "url": f"{p['url']target",
                    "data": p['data']
      }
