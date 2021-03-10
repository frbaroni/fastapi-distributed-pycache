from datetime import datetime
from fastapi import FastAPI
from typing import Generic, TypeVar, Callable, List
from cache import MyCache
import pickle
import requests
import base64

def serialize(data):
    return base64.b64encode(pickle.dumps(data))

def unserialize(b64):
    return pickle.loads(base64.b64decode(b64))

T = TypeVar('T')
class MyDistributed(Generic[T]):
    last_sync = datetime.utcnow()
    remotes: set[str] = set()
    cache: MyCache
    my_name: str

    def __init__(self, cache: MyCache[T], my_name: str):
        self.cache = cache
        self.my_name = my_name

    def sync(self):
        since_dt = self.last_sync
        self.last_sync = datetime.utcnow()
        # Get all remotes from all remotes
        for remote in self.remotes:
            self.fetch_remotes(remote)
        # Fetch remote items
        for remote in self.remotes:
            self.sync_with_remote(remote, since_dt)


    def recent(self, since_dt: datetime, ):
        recent_items = self.cache.since(since_dt)
        return serialize(recent_items)

    def get_remotes(self, name: str):
        self.add_remote(name)
        return serialize(list(self.remotes))

    def add_remote(self, remote: str):
        self.remotes.add(remote)
        return self.remotes

    def fetch_remotes(self, remote: str):
        try:
            print(f'Retrieving new /remotes from {remote}')
            response = requests.get(f'{remote}/sync/remotes', {'name': self.my_name})
            print(response.content)
            remotes = unserialize(response.content)
            for remote in remotes:
                if self.my_name != remote:
                    self.add_remote(remote)
        except Exception as e:
            raise Exception(f"Failed to fetch remotes {remote} -> {e}")

    def sync_with_remote(self, remote: str, since_dt: datetime):
        try:
            print(f'Retrieving new /recent from {remote} since {since_dt}')
            response = requests.get(f'{remote}/sync/recent', { "since_dt": str(since_dt)})
            recent_items = unserialize(response.content)
            print(recent_items)
            self.cache.sync_add(recent_items)
        except Exception as e:
            raise Exception(f"Failed to fetch recent {remote} -> {e}")

    def expose_to_fastapi(self, prefix: str, app: FastAPI):
        app.get(f'{prefix}/sync/recent')(self.recent)
        app.get(f'{prefix}/sync/remotes')(self.get_remotes)
        app.post(f'{prefix}/sync/execute')(self.sync)
        app.post(f'{prefix}/sync/add_remote')(self.add_remote)

