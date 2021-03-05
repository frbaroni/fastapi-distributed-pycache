from typing import Callable, TypeVar, Generic, List
from datetime import datetime
from collections import OrderedDict
from pydantic import BaseModel

class ExposeRequest(BaseModel):
    since_dt: datetime
    remotes: List[str]

T = TypeVar('T')
class MyCache(Generic[T]):
    data = OrderedDict()

    def set(self, key: str, value: T):
        now = datetime.utcnow()
        self.data[key] = {
            "key": key,
            "value": value,
            "updated": now,
        }
        self.data.move_to_end(key)
        return self

    def get(self, key: str):
        if self.has(key):
            self.data.move_to_end(key)
            return self.data[key].value
        else:
            raise Exception(f'key not found {key}')

    def has(self, key: str):
        return key in self.data

    def keys(self):
        return self.data.keys()

    def get_or_calc(self, key: str, calc: Callable[[str], T]):
        if not self.has(key):
            self.set(key, calc(key))
        else:
            self.get(key)

    def since(self, since_dt: datetime):
        recent = []
        for (_, entry_record) in reversed(self.data.items()):
            if entry_record.updated > since_dt:
                recent.append(entry_record)
            else:
                break
        return recent

    def sync_add(self, recent):
        for entry_record in recent:
            self.data[entry_record.key] = entry_record
