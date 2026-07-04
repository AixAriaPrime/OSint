from __future__ import annotations

import logging
from typing import Optional

from .config import settings
from .models import SearchResponse

logger = logging.getLogger(__name__)


async def generate_summary(response: SearchResponse) -> Optional[str]:
    if not settings.litellm_api_key:
        return None
    try:
        import litellm  # type: ignore

        litellm.api_key = settings.litellm_api_key

        # Build a concise prompt from available results
        parts = [f"Query: {response.query} (type: {response.query_type.value})\n"]
        for result in response.results:
            if result.success and result.data:
                parts.append(f"\n[{result.source}]\n{_format_data(result.data)}")
            elif not result.success:
                parts.append(f"\n[{result.source}] Error: {result.error}")

        prompt = (
            "You are an ethical OSINT analyst. Summarize the following intelligence findings "
            "concisely (3-5 sentences). Highlight the most important findings, any security risks, "
            "and recommend next investigation steps. Avoid speculation beyond available data.\n\n"
            + "".join(parts)
        )

        completion = await litellm.acompletion(
            model=settings.ai_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.3,
        )
        return completion.choices[0].message.content
    except Exception as exc:
        logger.warning("AI summary failed: %s", exc)
        return None


def _format_data(data: object) -> str:
    if isinstance(data, dict):
        lines = []
        for k, v in data.items():
            if v is not None and v != [] and v != {}:
                lines.append(f"  {k}: {v}")
        return "\n".join(lines)
    return str(data)
