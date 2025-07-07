import pytest
import httpx
from httpx import Response, Request
from httpx._transports.base import AsyncBaseTransport
from typing import Any

from pytest import MonkeyPatch
from bot.services import openrouter_client

class MockTransport(AsyncBaseTransport):
    async def handle_async_request(self, request: Request) -> Response:
        return Response(200, json={"choices": [{"message": {"content": "Hello"}}]})

@pytest.mark.asyncio
async def test_openrouter_response(monkeypatch: MonkeyPatch) -> None:
    async def mock_client(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=MockTransport())

    monkeypatch.setattr("bot.services.openrouter_client.httpx.AsyncClient", mock_client)
    result = await openrouter_client.get_openrouter_response([{"role": "user", "content": "Hi"}])
    assert "Hello" in result
