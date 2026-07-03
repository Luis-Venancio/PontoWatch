from functools import lru_cache

from loguru import logger
from supabase import Client, create_client

from app.core.config import get_settings


class _DummyResponse:
    def __init__(self, data=None):
        self.data = data or []


class _DummyQuery:
    def __init__(self, data=None):
        self._data = data or []

    def select(self, *args, **kwargs):
        return self

    def eq(self, *args, **kwargs):
        return self

    def gte(self, *args, **kwargs):
        return self

    def order(self, *args, **kwargs):
        return self

    def update(self, *args, **kwargs):
        return self

    def delete(self, *args, **kwargs):
        return self

    def insert(self, *args, **kwargs):
        return self

    def execute(self):
        return _DummyResponse(self._data)


class _DummySupabaseClient:
    def table(self, _name: str):
        return _DummyQuery()


@lru_cache
def get_supabase() -> Client:
    s = get_settings()
    if not s.supabase_url or not s.supabase_service_key:
        logger.warning("Supabase credentials not configured; using empty fallback client")
        return _DummySupabaseClient()

    try:
        return create_client(s.supabase_url, s.supabase_service_key)
    except Exception as exc:
        logger.warning(f"Supabase client initialization failed: {exc}")
        return _DummySupabaseClient()
