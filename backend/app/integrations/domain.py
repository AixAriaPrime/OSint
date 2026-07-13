from typing import Any


class DomainRecon:
    """Complete domain reconnaissance."""

    @staticmethod
    async def recon(domain: str) -> dict[str, Any]:
        return {
            "domain": domain,
            "whois": [
                {"name": "Whois", "url": f"https://www.whois.com/whois/{domain}"},
                {
                    "name": "DomainTools",
                    "url": f"https://www.domaintools.com/research/whois/{domain}",
                },
                {"name": "WhoisXMLAPI", "url": "https://whoisxmlapi.com/"},
            ],
            "dns": [
                {"name": "DNSdumpster", "url": "https://dnsdumpster.com/"},
                {"name": "ViewDNS", "url": "https://viewdns.info/"},
                {"name": "MXToolbox", "url": "https://mxtoolbox.com/"},
            ],
            "subdomains": [
                {"name": "Amass", "url": "https://github.com/OWASP/Amass"},
                {"name": "Sublist3r", "url": "https://github.com/aboul3la/Sublist3r"},
                {"name": "Findomain", "url": "https://github.com/Findomain/Findomain"},
            ],
        }
