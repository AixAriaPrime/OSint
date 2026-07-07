from typing import Dict, Any

class DomainRecon:
    """Complete domain reconnaissance"""
    
    @staticmethod
    async def recon(domain: str) -> Dict[str, Any]:
        
        return 
            "domain": domain,
            "whois": [
                {"name": "Whois", "url": f"https://www.whois.com/whois/{domain"},
                "name": "DomainTools", "url": f"https://www.domaintools.com/research/whois/",
                "name": "WhoisXMLAPI", "url": "https://whoisxmlapi.com/"
            ],
            "dns": [
                "name": "DNSdumpster", "url": "https://dnsdumpster.com/",
                "name": "ViewDNS", "url": "https://viewdns.info/",
                "name": "MXToolbox", "url": "https://mxtoolbox.com/",
                "name": "Cloudflare", "url": "https://cloudflare.com/dns"
            ],
            "subdomains": [
                "name": "Amass", "url": "https://github.com/OWASP/Amass",
                "name": "Sublist3r", "url": "https://github.com/aboul3la/Sublist3r",
                "name": "Findomain", "url": "https://github.com/Findomain/Findomain",
                "name": "Subdomainizer", "url": "https://github.com/nsonaniya2010/Subdomainizer"
            ],
            "technologies": [
                "name": "Wappalyzer", "url": "https://www.wappalyzer.com/",
                "name": "BuiltWith", "url": "https://builtwith.com/",
                "name": "WhatWeb", "url": "https://www.whatweb.net/"
            ],
            "screenshots": [
                "name": "Wayback Machine", "url": f"https://web.archive.org/web/*/{domain"},
                "name": "Chrome-Lamb", "url": "https://chromelamb.com/",
                "name": "Microsult", "url": "https://microsult.com/"
            ],
            "ssl": [
                "name": "SSL Labs", "url": "https://www.ssllabs.com/ssltest/",
                "name": "CertSpotter", "url": "https://crt.sh/"
            ]
        }# backend/app/integrations/reverse_image.py
from typing import Dict, Any

class ReverseImage:
    """Reverse image search tools"""
    
    @staticmethod
    async def search(image_url: str) -> Dict[str, Any]:
        
        return 
            "image": image_url,
            "search_engines": [
                {"name": "Google Lens", "url": "https://lens.google.com/",
                "name": "Yandex", "url": "https://yandex.com/images/",
                "name": "Bing Visual Search", "url": "https://www.bing.com/visualsearch",
                "name": "TinEye", "url": "https://tineye.com/"
            ],
            "osint_tools": [
                "name": "EXIF metadata", "description": "Check GPS in original",
                "name": "Forensically", "url": "https://29a.ch/photo-forensics/",
                "name": "ImgOps", "url": "https://imgops.com/",
                "name": "FotoForensics", "url": "https://fotoforensics.com/"
            ],
            "facial_recognition": [
                "name": "PimEyes", "url": "https://pimeyes.com/",
                "name": "Betaface", "url": "https://www.betaface.com/",
                "name": "Face++", "url": "https://www.faceplusplus.com/"
            ]
}
