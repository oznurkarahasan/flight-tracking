import json
import os

class StorageManager:
    def __init__(self, file_path="data/price_history.json"):
        self.file_path = file_path
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def get_last_price(self, key):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        return data.get(key)

    def save_price(self, key, price):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        data[key] = price
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)