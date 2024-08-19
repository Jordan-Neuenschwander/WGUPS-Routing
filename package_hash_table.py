# holds the data related to the package
# status is where the package currently is (at hub, en route, delivered)
# loaded_at and delivered_at are timestamps used to generate the report
class Package:

    def __init__(self, package_id, address, city, zip_code, deadline, mass, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.deadline = deadline
        self.mass = mass
        self.status = status
        self.loaded_at = None
        self.delivered_at = None

    # a string representation of the object
    def __str__(self):
        return self.address

# custom hash table
# takes a key and returns a value
# Insert/Delete/Lookup time complexity is O(1)
# Size complexity is O(n)
class HashTable:

    # constructs a new instance of this object
    # Creates a list of lists
    def __init__(self, capacity=10):

        self.table = []

        for i in range(capacity):
            self.table.append([])

    # inserts a key value pair into the hash table
    # if the key already is in the table, it replaces the value with the new value
    def insert(self, key, package):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                key_value[1] = package
                return True

        key_value = [key, package]
        bucket_list.append(key_value)
        return True

    # gets the list that the key could be in and then searches for that key
    # returns the value portion of the key value pair when found
    def search(self, key):

        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]

        return None

    # I found out that python doesn't do overloaded methods here
    # lets you search the hash table using a package object
    def search_for(self, package):
        key = package.package_id
        return self.search(key)

    # searches for a key and removes it from the table
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        if key in bucket_list:
            bucket_list.remove(key)
        else:
            return None
