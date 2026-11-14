class HNode:
    __slots__ = ("key", "value", "next")

    def __init__(self, key, value, nxt=None):
        self.key = key
        self.value = value
        self.next = nxt


class HashTable:
    def __init__(self,capacity=8, max_load=0.75):
        self.capacity = capacity
        self.max_load = max_load
        self.buckets = [None] * capacity
        self.size = 0
        self.resizes = 0

    def __len__(self):
        return self.size

    def _hash(self, key): # polynomial string hash, base 31
        if isinstance(key, int):
            h = key
        else:
            h = 0
            for ch in str(key):
                h = (h * 31 + ord(ch)) & 0xFFFFFFFF
        return h % self.capacity

    def put(self, key, value):
        idx = self._hash(key)
        cur = self.buckets[idx]
        while cur:
            if cur.key == key:
                cur.value = value
                return
            cur = cur.next
        self.buckets[idx] = HNode(key, value, self.buckets[idx])
        self.size += 1
        if self.size / self.capacity > self.max_load:
            self._resize()

    def get(self, key, default=None):
        cur = self.buckets[self._hash(key)]
        while cur:
            if cur.key == key:
                return cur.value
            cur = cur.next
        return default

    def contains(self, key):
        marker = object()
        test = self.get(key, marker)
        return test is not marker

    def __contains__(self, key):
        return self.contains(key)

    def delete(self, key):
        idx = self._hash(key)
        prev, cur = None, self.buckets[idx]
        while cur:
            if cur.key == key:
                if prev:
                    prev.next = cur.next
                else:
                    self.buckets[idx] = cur.next
                self.size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def _resize(self):
        old = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity

        for head in old:
            cur = head
            while cur:
                nxt = cur.next
                idx = self._hash(cur.key)
                cur.next = self.buckets[idx]
                self.buckets[idx] = cur
                cur = nxt
        self.resizes += 1

    def stats(self):
        used = 0
        longest = 0
        for head in self.buckets:
            if head:
                used += 1
                length, cur = 0, head
                while cur:
                    length += 1
                    cur = cur.next
                longest = max(longest, length)
        return {
            "entries": self.size,
            "buckets": self.capacity,
            "load factor": round(self.size / self.capacity, 3),
            "used buckets": used,
            "colliding entries": self.size - used,
            "longest chain": longest,
            "resizes": self.resizes,
        }

    def show(self):
        for i, head in enumerate(self.buckets):
            parts, cur = [], head
            while cur:
                parts.append(f"({cur.key}: {cur.value})")
                cur = cur.next
            print(f"  [{i:>3}] " + (" -> ".join(parts) if parts else "empty"))

