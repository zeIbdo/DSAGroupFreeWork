from . import CustomArray as Ca
from . import CustomLinkedList as Cl
class Stack:

    def __init__(self):
        self._a =  Ca.DynamicArray()

    def __len__(self):
        return self._a.size

    def is_empty(self):
        return self._a.size == 0

    def push(self, v):
        self._a.append(v)

    def pop(self):
        if self.is_empty():
            raise IndexError("stack is empty")
        return self._a.delete_at(self._a.size - 1)

    def peek(self):
        if self.is_empty():
            raise IndexError("stack is empty")
        return self._a.get(self._a.size - 1)


class Queue:

    def __init__(self):
        self._l = Cl.DoublyLinkedList()

    def __len__(self):
        return self._l.size

    def is_empty(self):
        return self._l.size == 0

    def enqueue(self, v):
        self._l.append(v)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        return self._l.delete_first()

    def peek(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        return self._l.head.value

    def to_list(self):
        return self._l.to_list()


class Deque:

    def __init__(self):
        self._l = Cl.DoublyLinkedList()

    def __len__(self):
        return self._l.size

    def is_empty(self):
        return self._l.size == 0

    def add_front(self, v):
        self._l.prepend(v)

    def add_back(self, v):
        self._l.append(v)

    def remove_front(self):
        if self.is_empty():
            raise IndexError("deque is empty")
        return self._l.delete_first()

    def remove_back(self):
        if self.is_empty():
            raise IndexError("deque is empty")
        return self._l.delete_last()

    def peek_front(self):
        if self.is_empty():
            raise IndexError("deque is empty")
        return self._l.head.value

    def peek_back(self):
        if self.is_empty():
            raise IndexError("deque is empty")
        return self._l.tail.value

    def to_list(self):
        return self._l.to_list()