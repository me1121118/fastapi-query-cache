import functools, hashlib, time
from typing import Callable, Optional
from fastapi import Request

class MemoryCache:
    def __init__(self):
        self.store = {}
    def get(self, key):
        if key in self.store:
            val, exp = self.store[key]
            if time.time() < exp: return val
            del self.store[key]
        return None
    def set(self, key, val, ttl):
        self.store[key] = (val, time.time() + ttl)

_cache = MemoryCache()

def cache_query(ttl: int = 60):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            req = kwargs.get("request")
            if not req:
                for arg in args:
                    if isinstance(arg, Request):
                        req = arg; break
            
            key = f"{func.__name__}:{req.url.path}:{sorted(req.query_params.items())}" if req else f"{func.__name__}:{sorted(kwargs.items())}"
            cache_key = hashlib.sha256(key.encode()).hexdigest()
            
            cached = _cache.get(cache_key)
            if cached is not None:
                return cached
            
            import inspect
            res = await func(*args, **kwargs) if inspect.iscoroutinefunction(func) else func(*args, **kwargs)
            _cache.set(cache_key, res, ttl)
            return res
        return wrapper
    return decorator
