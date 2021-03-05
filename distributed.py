from datetime import datetime
from fastapi import FastAPI
from typing import Generic, TypeVar
from cache import MyCache
import json
import requests

T = TypeVar('T')
class MyDistributed(Generic[T]):
    last_sync = datetime.utcnow()
    remotes = []
    cache: MyCache

    def __init__(self, cache: MyCache[T]):
        self.cache = cache

    def sync(self):
        since_dt = self.last_sync
        self.last_sync = datetime.utcnow()
        for remote in self.remotes:
            recent_items = json.loads(requests.get(remote, since_dt=since_dt).content)
            recent_keys = [item.key for item in recent_items]
            print(f'Sync with {remote} found {recent_keys}')
            self.cache.sync_add(recent_items)

    def expose_recent(self, since_dt: datetime):
        items = self.cache.since(since_dt)
        return json.dumps(items)

    def add_remote(self, remote: str):
        self.remotes.append(remote)

    def expose_to_fastapi(self, prefix: str, app: FastAPI):
        app.get(f'{prefix}/sync/expose')(lambda since_dt: self.expose_recent(since_dt))
        app.post(f'{prefix}/sync/execute')(lambda : self.sync())
        app.post(f'{prefix}/sync/add_remote')(lambda remote: self.add_remote(remote))

