from datetime import datetime
from typing import Generic, TypeVar
from cache import MyCache
import requests

T = TypeVar('T')
class MyDistributed(Generic[T]):
    last_sync = datetime.utcnow()
    remotes = []
    cache: MyCache

    def __init__(self, cache: MyCache[T]):
        self.cache = cache

    def sync(self):
        for remote in self.remotes:
            recent_items = requests.get(remote, since=self.last_sync)
            self.cache.sync_add(recent_items)

    def add_remote(self, remote: str):
        self.remotes.append(remote)
