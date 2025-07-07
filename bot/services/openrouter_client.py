import httpx
from typing import Any

from bot import config

async def get_openrouter_response(messages: list[dict[str, str]]) -> str:
    """
    Calls the OpenRouter API with the given conversation history.
    """
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/YOUR_GITHUB_REPO",
        "X-Title": "TelegramBot"
    }
    payload = {
        "model": config.OPENROUTER_MODEL,
        "messages": messages
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(config.OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()
        resp_json: dict[str, Any] = response.json()
        return str(resp_json["choices"][0]["message"]["content"])
