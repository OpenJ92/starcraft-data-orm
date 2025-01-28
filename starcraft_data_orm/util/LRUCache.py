from collections import OrderedDict

class LRUCache:
    def __init__(self, maxsize=10000):
        self.cache = OrderedDict()
        self.maxsize = maxsize

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def set(self, key, value):
        self.cache[key] = value
        if len(self.cache) > self.maxsize:
            key, value = self.cache.popitem(last=False)
