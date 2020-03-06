class Entry:
    def __init__(self, k, v):
        self.key = k
        self.value = v
    def __repr__(self):
        return str(self.key, self.value)
    def __lt__(self, other):
        return self.key < other.key

class HashTable:

    def __init__(self, table_size):         # can add additional attributes
        self.table_size = table_size        # initial table size
        self.hash_table = [None]*table_size # hash table
        self.num_items = 0                  # empty hash table

    def insert(self, key, value):
        """ Inserts an entry into the hash table (using Horner hash function to determine index, 
        and quadratic probing to resolve collisions).
        The key is a string (a word) to be entered, and value is any object (e.g. Python List).
        If the key is not already in the table, the key is inserted along with the associated value
        If the key is is in the table, the new value replaces the existing value.
        When used with the concordance, value is a Python List of line numbers.
        If load factor is greater than 0.5 after an insertion, hash table size should be increased (doubled + 1)."""
        entry = Entry(key, value)
        # self.check_load()
        index = self.horner_hash(entry.key)
        j = 0
        for i in range(0, self.table_size):
            j = (index + i**2) % self.table_size  #quad probing in case of collision

            if not self.hash_table[j]:   #insert if there is nothing there
                self.hash_table[j] = entry
                self.num_items += 1
                self.check_load()
                return

            elif self.hash_table[j].key == entry.key:    #insert if it's the same word
                self.hash_table[j] = entry
                return

    def grow_hash(self):
        x = HashTable(self.table_size * 2 + 1)  #create new empty hash table
        for i in self.hash_table:
            if i:
                x.insert(i.key, i.value)      #copy over values / previously x.insert(i)
        self.hash_table = x.hash_table        #copy back to new hash table
        self.table_size = x.table_size
        self.num_items = x.num_items


    def check_load(self):
        load = self.num_items / self.table_size
        if load > 0.5:
            self.grow_hash()

    def horner_hash(self, key):
        """ Compute and return an integer from 0 to the (size of the hash table) - 1
        Compute the hash value by using Horner’s rule, as described in project specification."""
        h = 0
        for i in range(min(len(key), 8)):
            h = h*31 + ord(key[i])
        return h % self.table_size

    def in_table(self, key):
        """ Returns True if key is in an entry of the hash table, False otherwise. Must be O(1)."""
        index = self.horner_hash(key)
        j = 0
        for i in range(0, self.table_size):
            j = (index + i ** 2) % self.table_size
            if self.hash_table[j] and self.hash_table[j].key == key:
                return True
        return False

    def get_index(self, key):
        """ Returns the index of the hash table entry containing the provided key. 
        If there is not an entry with the provided key, returns None. Must be O(1)."""
        index = self.horner_hash(key)
        j = 0
        for i in range(0, self.table_size):
            j = (index + i ** 2) % self.table_size
            if self.hash_table[j] and self.hash_table[j].key == key:
                return j
        return None

    def get_all_keys(self):
        """ Returns a Python list of all keys in the hash table."""
        listA = []
        for entry in self.hash_table:
            if entry != None:
                listA.append(entry.key)
        return listA

    def get_value(self, key):
        """ Returns the value (for concordance, list of line numbers) associated with the key.
        If key is not in hash table, returns None. Must be O(1)."""
        index = self.horner_hash(key)
        j = 0
        for i in range(0, self.table_size):
            j = (index + i ** 2) % self.table_size
            if self.hash_table[j] and self.hash_table[j].key == key:
                return self.hash_table[j].value
        return None

    def get_num_items(self):
        """ Returns the number of entries (words) in the table. Must be O(1)."""
        return self.num_items

    def get_table_size(self):
        """ Returns the size of the hash table."""
        return self.table_size

    def get_load_factor(self):
        """ Returns the load factor of the hash table (entries / table_size)."""
        load = self.num_items / self.table_size
        return load

