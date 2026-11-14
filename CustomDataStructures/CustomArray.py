class Array:
    #Fixed capacity array
    def __init__(self, capacity):
        self.capacity = capacity
        self._data = [None] * capacity
        self.size = 0

    def __len__(self):
        return self.size

    def get(self,i): #O(1)
        if not 0<=i<self.capacity:
            raise IndexError("index out of range")
        return self._data[i]

    def append(self,x): #O(1)
        if self.size == self.capacity:
            raise OverflowError("array is full")
        self._data[self.size] = x
        self.size += 1

    def insert(self,i,x): #O(n)
        if self.size == self.capacity:
            raise OverflowError("array is full")
        if not 0<=i<=self.size:
            raise IndexError("index out of range")
        for j in range(self.size,i,-1):
            self._data[j] = self._data[j-1]
        self._data[i] = x
        self.size += 1

    def delete_at(self,i): # O(n)
        if not 0<= i<self.size:
            raise IndexError("index out of range")
        v = self._data[i]
        for j in range(i,self.size-1):
            self._data[j] = self._data[j+1]
        self._data[self.size-1] = None
        self.size -= 1
        return v

    def search(self,x): # O(n)
        for i in range(self.size):
            if self._data[i] == x:
                return i
        return -1

    def to_list(self): #converting to standard python list
        return self._data[:self.size]

class DynamicArray(Array):
    #Array that doubles its capacity when full and halves it when 3/4 empty
    def __init__(self, capacity=4):
        super().__init__(max(1,capacity))
        self.resizes = 0

    def _resize(self,new_capacity):
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self._data[i]
        self._data = new_data
        self.capacity = new_capacity
        self.resizes += 1

    def append(self, x):
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        super().append(x)

    def insert(self, i, x):
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        super().insert(i, x)

    def delete_at(self, i):
        v = super().delete_at(i)
        if self.capacity > 4 and self.size <= self.capacity // 4:
            self._resize(self.capacity // 2)
        return v