#Hash Table Class
class HashTable:

    #To mark the state of a slot without relying on None type.
    EMPTY = object()
    DELETED = object()

    def __init__(self, capacity: int = 101):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")

        self.capacity = capacity # size of hash table
        self.size = 0 # number of non-deleted entries
        self._keys = [self.EMPTY] * capacity # an entry's key
        self._values = [None] * capacity # an entry's value

    def hash_function(self, key):
        #Polynomial Rolling Hash with Horner's method
        h = 0
        g = 31 # some small prime
        for ch in str(key):
            h = (h * g + ord(ch)) % self.capacity
        return h

    def linear_probing(self, key):
        #Return the Linear probing sequence for the key
        slot = self.hash_function(key)
        for i in range(self.capacity):
            yield (slot + i) % self.capacity

    def insert(self, key, value):
        if self.size >= self.capacity *0.7:
            self.resize(self.capacity * 2)

        first_deleted = None

        for i in self.linear_probing(key):
            slot_key = self._keys[i]

            if slot_key is self.EMPTY:

                if first_deleted is not None:
                    target = first_deleted
                else:
                    target = i

                self._keys[target] = key
                self._values[target] = value
                self.size += 1

                return True

            if slot_key is self.DELETED:
                if first_deleted is None:
                    first_deleted = i
                continue

            # Inserting existing key overwrites its value instead of creating duplicates.
            if slot_key == key:
                self._values[i] = value
                return True

        raise RuntimeError("Hash table is full.")

    def search(self, key):
        for i in self.linear_probing(key):
            slot_key = self._keys[i]

            if slot_key is self.EMPTY:
                return None
            if slot_key is self.DELETED:
                continue

            if slot_key == key:
                return self._values[i]

        return None

    def delete(self, key):
        for i in self.linear_probing(key):
            slot_key = self._keys[i]

            if slot_key is self.EMPTY:
                return False

            if slot_key is self.DELETED:
                continue

            if slot_key == key:
                self._keys[i] = self.DELETED
                self._values[i] = None
                self.size -= 1
                return True

        return False

    def resize(self, new_capacity: int) -> None:
        old_keys, old_values = self._keys, self._values
        self.capacity = new_capacity
        self._keys = [self.EMPTY] * new_capacity
        self._values = [None] * new_capacity
        self.size = 0
        for k, v in zip(old_keys, old_values):
            if k is not self.EMPTY and k is not self.DELETED:
                self.insert(k, v)

    def print_items(self):
        return [(k,v) for k, v in zip(self._keys, self._values)
            if k is not self.EMPTY and k is not self.DELETED]



