from typing import Any, Dict


class DarkWebDorks:
    """Dark web and dork search helper."""

    DORKS = {
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
            'inurl:{target} "AWS_ACCESS_KEY_ID"',
            'inurl:{target} "secret"',
        ],
        "phone": [
            '"{target}" "telegram"',
            '"{target}" "leak"',
        ],
    }

    @staticmethod
    async def search(target: str, target_type: str = "email") -> Dict[str, Any]:
        dorks = DarkWebDorks.DORKS.get(target_type, DarkWebDorks.DORKS["email"])
        return {
            "target": target,
            "paste_sites": [
                {"name": "Pastebin", "url": f"https://pastebin.com/search?q={target}"},
                {"name": "Ghostbin", "url": "https://ghostbin.com/"},
                {"name": "JustPaste", "url": "https://justpaste.it/"},
            ],
            "dorks": [d.format(target=target) for d in dorks],
            "search_engines": [
                {"name": "IntelX", "url": "https://intelx.io/"},
                {"name": "DarkDump", "url": "https://www.darkdump.io/"},
                {"name": "Ahmia", "url": "https://ahmia.fi/"},
            ],
            "breach_db": [
                {"name": "Dehashed", "url": "https://dehashed.com/"},
                {"name": "Snusbase", "url": "https://snusbase.com/"},
                {"name": "LeakCheck", "url": "https://leakcheck.io/"},
            ],
        }


class VPNProxyCheck:
    """Check whether an IP appears to be VPN/proxy/Tor."""

    @staticmethod
    async def check(ip_address: str) -> Dict[str, Any]:
        return {
            "ip": ip_address,
            "services": [
                {"name": "IP-API", "url": f"http://ip-api.com/json/{ip_address}"},
                {"name": "AbuseIPDB", "url": f"https://www.abuseipdb.com/check/{ip_address}"},
                {"name": "GreyNoise", "url": f"https://viz.greynoise.io/ip/{ip_address}"},
                {"name": "Shodan", "url": f"https://www.shodan.io/host/{ip_address}"},
            ],
            "can_detect": [
                "VPN",
                "Proxy",
                "Tor exit node",
                "Datacenter ASN",
                "Organization",
                "Geolocation",
            ],
        }


class WiFiGeolocation:
    """WiFi geolocation helper."""

    @staticmethod
    async def lookup(ssid_or_bssid: str) -> Dict[str, Any]:
        return {
            "target": ssid_or_bssid,
            "wigle": f"https://wigle.net/search?search={ssid_or_bssid}",
            "method": "WiGLE maps SSID/BSSID observations to coordinates.",
            "can_find": "Approximate to precise geolocation where recorded.",
            "privacy_note": "Broadcast identifiers can reveal sensitive location history.",
            "tools": [
                {"name": "WiGLE", "url": "https://wigle.net/"},
                {"name": "WiGLE WiFi Map", "description": "Mobile mapping companion app."},
            ],
        }
