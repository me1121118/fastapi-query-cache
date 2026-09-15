import pytest
from fastapi import FastAPI, Request
from httpx import AsyncClient, ASGITransport
from fastapi_query_cache import cache_query

counter = 0

@pytest.fixture
def app():
    global counter
    counter = 0
    app = FastAPI()
    @app.get("/items")
    @cache_query(ttl=10)
    async def get_items(request: Request, q: str = ""):
        global counter
        counter += 1
        return {"counter": counter, "q": q}
    return app

@pytest.mark.asyncio
async def test_query_caching(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r1 = await c.get("/items?q=apple")
        assert r1.json()["counter"] == 1
        r2 = await c.get("/items?q=apple")
        assert r2.json()["counter"] == 1 # Cached
        r3 = await c.get("/items?q=banana")
        assert r3.json()["counter"] == 2 # Different query param
