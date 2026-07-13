from typing import Any, Dict


class EmailOSINT:
    """Email address intelligence"""

    @staticmethod
    async def lookup(email: str) -> Dict[str, Any]:
        return {
            "email": email,
            "breach_check": [
                {"name": "HaveIBeenPwned", "url": f"https://haveibeenpwned.com/account/{email}"},
                {"name": "Dehashed", "url": f"https://dehashed.com/search?query={email}"},
                {"name": "LeakCheck", "url": f"https://leakcheck.io/search?query={email}"},
                {"name": "Snusbase", "url": f"https://snusbase.com/?terms={email}"},
            ],
            "social_correlation": [
                {"action": "Search on all social platforms", "query": email},
                {"action": "Check Gravatar", "url": "https://www.gravatar.com/avatar/"},
                {"action": "Google search", "query": f"'{email}'"},
            ],
            "email_header": {
                "method": "Get full email headers",
                "tools": ["EmailHeaderAnalyzer", "MXToolbox"],
                "can_find": "Originating IP, mail server, timestamps",
            },
            "email_disposable": {
                "check": "Is this a disposable email?",
                "services": ["Disify", "TempMail", "EmailChecker"],
            },
        }
