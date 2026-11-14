class SNode:
    _slots_ = ("value", "next")

    def _init_(self, value, nxt=None):
        self.value = value
        self.next = nxt


class SinglyLinkedList:

    def _init_(self):
        self.head = None
        self.size = 0

    def _len_(self):
        return self.size

    def prepend(self, v):  # O(1)
        self.head = SNode(v, self.head)
        self.size += 1

    def append(self, v):  # O(n)
        node = SNode(v)
        if self.head is None:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node
        self.size += 1

    def delete_first(self):  # O(1)
        if self.head is None:
            raise IndexError("list is empty")
        v = self.head.value
        self.head = self.head.next
        self.size -= 1
        return v

    def delete_last(self):  # O(n)
        if self.head is None:
            raise IndexError("list is empty")
        if self.head.next is None:
            v = self.head.value
            self.head = None
            self.size = 0
            return v
        cur = self.head
        while cur.next.next:
            cur = cur.next
        v = cur.next.value
        cur.next = None
        self.size -= 1
        return v

    def delete_value(self, v):  # O(n)
        prev, cur = None, self.head
        while cur:
            if cur.value == v:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                self.size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def search(self, v):  # O(n)
        cur, i = self.head, 0
        while cur:
            if cur.value == v:
                return i
            cur, i = cur.next, i + 1
        return -1

    def to_list(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out


class DNode:
    _slots_ = ("value", "prev", "next")

    def _init_(self, value):
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:

    def _init_(self):
        self.head = None
        self.tail = None
        self.size = 0

    def _len_(self):
        return self.size

    def prepend(self, v):  # O(1)
        node = DNode(v)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1

    def append(self, v):  # O(1)
        node = DNode(v)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1

    def delete_first(self):  # O(1)
        if self.head is None:
            raise IndexError("list is empty")
        node = self.head
        self.head = node.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
        return node.value

    def delete_last(self):  # O(1)
        if self.tail is None:
            raise IndexError("list is empty")
        node = self.tail
        self.tail = node.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self.size -= 1
        return node.value

    def delete_value(self, v):  # O(n)
        cur = self.head
        while cur:
            if cur.value == v:
                if cur.prev:
                    cur.prev.next = cur.next
                else:
                    self.head = cur.next
                if cur.next:
                    cur.next.prev = cur.prev
                else:
                    self.tail = cur.prev
                self.size -= 1
                return True
            cur = cur.next
        return False

    def search(self, v):  # O(n)
        cur, i = self.head, 0
        while cur:
            if cur.value == v:
                return i
            cur, i = cur.next, i + 1
        return -1

    def to_list(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out

    def to_list_reverse(self):
        out, cur = [], self.tail
        while cur:
            out.append(cur.value)
            cur = cur.prev
        return out