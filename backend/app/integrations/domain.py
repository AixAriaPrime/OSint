from typing import Any, Dict


class DomainRecon:
    """Domain reconnaissance helper."""

    @staticmethod
    async def recon(domain: str) -> Dict[str, Any]:
        return {
            "domain": domain,
            "whois": [
                {"name": "Whois", "url": f"https://www.whois.com/whois/{domain}"},
                {"name": "DomainTools", "url": "https://www.domaintools.com/"},
                {"name": "WhoisXMLAPI", "url": "https://whoisxmlapi.com/"},
            ],
            "dns": [
                {"name": "DNSdumpster", "url": "https://dnsdumpster.com/"},
                {"name": "ViewDNS", "url": "https://viewdns.info/"},
                {"name": "MXToolbox", "url": "https://mxtoolbox.com/"},
                {"name": "Cloudflare Radar", "url": "https://radar.cloudflare.com/"},
            ],
            "subdomains": [
                {"name": "Amass", "url": "https://github.com/owasp-amass/amass"},
                {"name": "Sublist3r", "url": "https://github.com/aboul3la/Sublist3r"},
                {"name": "Findomain", "url": "https://github.com/Findomain/Findomain"},
                {"name": "Subdomainizer", "url": "https://github.com/nsonaniya2010/SubDomainizer"},
            ],
            "technologies": [
                {"name": "Wappalyzer", "url": "https://www.wappalyzer.com/"},
                {"name": "BuiltWith", "url": "https://builtwith.com/"},
                {"name": "WhatWeb", "url": "https://github.com/urbanadventurer/WhatWeb"},
            ],
            "screenshots": [
                {"name": "Wayback Machine", "url": f"https://web.archive.org/web/*/{domain}"},
                {"name": "urlscan.io", "url": f"https://urlscan.io/search/#domain:{domain}"},
            ],
            "ssl": [
                {"name": "SSL Labs", "url": "https://www.ssllabs.com/ssltest/"},
                {"name": "crt.sh", "url": "https://crt.sh/"},
            ],
        }


class ReverseImage:
    """Reverse image search helper."""

    @staticmethod
    async def search(image_url: str) -> Dict[str, Any]:
        return {
            "image": image_url,
            "search_engines": [
                {"name": "Google Lens", "url": "https://lens.google.com/"},
                {"name": "Yandex Images", "url": "https://yandex.com/images/"},
                {"name": "Bing Visual Search", "url": "https://www.bing.com/visualsearch"},
                {"name": "TinEye", "url": "https://tineye.com/"},
            ],
            "osint_tools": [
                {"name": "EXIF metadata", "description": "Inspect original image metadata."},
                {"name": "Forensically", "url": "https://29a.ch/photo-forensics/"},
                {"name": "ImgOps", "url": "https://imgops.com/"},
                {"name": "FotoForensics", "url": "https://fotoforensics.com/"},
            ],
            "facial_recognition": [
                {"name": "PimEyes", "url": "https://pimeyes.com/"},
                {"name": "Betaface", "url": "https://www.betaface.com/"},
                {"name": "Face++", "url": "https://www.faceplusplus.com/"},
            ],
        }
