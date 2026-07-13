from typing import Any, Dict


class DomainRecon:
    """Complete domain reconnaissance"""

    @staticmethod
    async def recon(domain: str) -> Dict[str, Any]:
        return {
            "domain": domain,
            "whois": [
                {"name": "Whois", "url": f"https://www.whois.com/whois/{domain}"},
                {"name": "DomainTools", "url": "https://www.domaintools.com/research/whois/"},
                {"name": "WhoisXMLAPI", "url": "https://whoisxmlapi.com/"},
            ],
            "dns": [
                {"name": "DNSdumpster", "url": "https://dnsdumpster.com/"},
                {"name": "ViewDNS", "url": "https://viewdns.info/"},
                {"name": "MXToolbox", "url": "https://mxtoolbox.com/"},
                {"name": "Cloudflare", "url": "https://cloudflare.com/dns"},
            ],
            "subdomains": [
                {"name": "Amass", "url": "https://github.com/OWASP/Amass"},
                {"name": "Sublist3r", "url": "https://github.com/aboul3la/Sublist3r"},
                {"name": "Findomain", "url": "https://github.com/Findomain/Findomain"},
                {"name": "Subdomainizer", "url": "https://github.com/nsonaniya2010/Subdomainizer"},
            ],
            "technologies": [
                {"name": "Wappalyzer", "url": "https://www.wappalyzer.com/"},
                {"name": "BuiltWith", "url": "https://builtwith.com/"},
                {"name": "WhatWeb", "url": "https://www.whatweb.net/"},
            ],
            "screenshots": [
                {"name": "Wayback Machine", "url": f"https://web.archive.org/web/*/{domain}"},
                {"name": "Chrome-Lamb", "url": "https://chromelamb.com/"},
                {"name": "Microsult", "url": "https://microsult.com/"},
            ],
            "ssl": [
                {"name": "SSL Labs", "url": "https://www.ssllabs.com/ssltest/"},
                {"name": "CertSpotter", "url": "https://crt.sh/"},
            ],
        }
