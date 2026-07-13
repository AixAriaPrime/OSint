from typing import Any


class DarkWebDorks:
    """Dark web search + Google dorks."""

    DORKS: dict[str, list[str]] = {
        "email": [
            'site:pastebin.com "{target}" password',
            '"{target}" filetype:xls',
            '"{target}" "combo list"',
            '"{target}" "database"',
            '"{target}" "leak"',
        ],
        "domain": [
            'site:github.com "{target}" "password"',
            'site:github.com "{target}" "api_key"',
            'inurl:{target} "AWS_ACCESS"',
            'inurl:{target} "secret"',
        ],
        "phone": ['"{target}" "telegram"', '"{target}" leak'],
    }

    @staticmethod
    async def search(target: str, target_type: str = "email") -> dict[str, Any]:
        templates = DarkWebDorks.DORKS.get(target_type, DarkWebDorks.DORKS["email"])
        dorks = [template.format(target=target) for template in templates]

        return {
            "target": target,
            "paste_sites": [
                {"name": "Pastebin", "url": f"https://pastebin.com/search?q={target}"},
                {"name": "GhostPaste", "url": "https://ghostpaste.me/"},
                {"name": "JustPaste", "url": "https://justpaste.it/"},
            ],
            "dorks": dorks,
            "search_engines": [
                {"name": "IntelX", "url": "https://intelx.io/"},
                {"name": "Darkdump", "url": "https://www.darkdump.io/"},
                {"name": "Hive", "url": "https://www.hive.cool/"},
            ],
        }
