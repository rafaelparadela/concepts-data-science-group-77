from bitarray import bitarray
from bloomfilter.hash_functions import get_hashes


class BloomFilter:
    def __init__(self, size: int, hash_count: int):
        # m: number of bits in the bit array
        self.size = size
        # k: number of hash functions to use
        self.hash_count = hash_count

        # Initialize bit array with all bits set to 0
        self.bits = bitarray(size)
        self.bits.setall(0)

    def add(self, item):
        # Add an item to the Bloom filter
        # We compute k hash indices and set those positions to 1
        for idx in get_hashes(item, self.hash_count, self.size):
            self.bits[idx] = 1

    def contains(self, item) -> bool:
        # Check if an item is in the Bloom filter
        # If any of the hashed positions is 0 then is not in the set
        # If all are 1 is likely in then set
        return all(self.bits[idx] for idx in get_hashes(item, self.hash_count, self.size))
