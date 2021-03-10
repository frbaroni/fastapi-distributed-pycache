from typing import Callable, TypeVar, Generic
from datetime import datetime
from collections import OrderedDict

T = TypeVar('T')
class MyCache(Generic[T]):
    # We use OrderedDict to store the data
    data = OrderedDict()

    def set(self, key: str, value: T):
        now = datetime.utcnow()
        self.data[key] = {
            "key": key,
            "value": value,
            "updated": now,
        }
        # Everytime we change a key, we move to the most recent, and change the 'Updated' field
        self.data.move_to_end(key)
        print(f'Adding {key}')
        return self

    def get(self, key: str):
        if self.has(key):
            # Getting also makes it more recent, but no change to the Updated field
            self.data.move_to_end(key)
            row = self.data[key]
            print(row)
            return row['value']
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

    # Sync Methods: allow us to get only the recent changes since the previous sync
    def since(self, since_dt: datetime):
        recent = []
        for (_, entry_record) in reversed(self.data.items()):
            if entry_record['updated'] > since_dt:
                recent.append(entry_record)
            else:
                break
        return recent

    # And add a key without changing the timestamp, as we don't want to change the
    # Updated field from other servers
    def sync_add(self, recent):
        for entry_record in recent:
            key = entry_record['key']
            self.data[key] = entry_record
            self.data.move_to_end(key)
            print(f'Sync add item: {key}')
