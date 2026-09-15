# ⚡ fastapi-query-cache
[![FastAPI](https://img.shields.io/badge/FastAPI-Supported-009688.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Deterministic query parameter caching decorator for FastAPI.

### ☕ Support My Studies
- ☕ **Buy Me a Coffee: [https://buymeacoffee.com/kcidi4148](https://buymeacoffee.com/kcidi4148):** [buymeacoffee.com/yourname](https://www.buymeacoffee.com)
- ⭐ **Star this repo!**

```python
from fastapi import FastAPI, Request
from fastapi_query_cache import cache_query

app = FastAPI()

@app.get("/search")
@cache_query(ttl=60)
async def search(request: Request, q: str):
    return {"results": f"Result for {q}"}
```
