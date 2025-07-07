import httpx
from typing import Any

from bot import config
from bot.services.logger import logger  

async def get_openrouter_response(messages: list[dict[str, str]]) -> str:
    """
    Calls the OpenRouter API with the given conversation history.
    """
    logger.debug(f"OpenRouter request messages: {messages}")

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

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(config.OPENROUTER_URL, headers=headers, json=payload)
            response.raise_for_status()
            resp_json: dict[str, Any] = response.json()

            logger.debug(f"OpenRouter response: {resp_json}")

            return str(resp_json["choices"][0]["message"]["content"])

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error from OpenRouter: {e.response.status_code} - {e.response.text}")
        raise

    except Exception as e:
        logger.exception(f"Unexpected error when calling OpenRouter: {e}")
        raise
