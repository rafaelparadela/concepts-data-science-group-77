from bitarray import bitarray
from bloomfilter.hash_functions import h1, h2


class BloomFilter:
    def __init__(self, size: int, hash_count: int):
        self.size = size              # m
        self.hash_count = hash_count  # k
        self.bits = bitarray(size)
        self.bits.setall(0)

    def _hashes(self, item: str):
        x = item.encode('utf-8')

        h1_val = h1(x)
        h2_val = h2(x)

        for i in range(self.hash_count):
            yield (h1_val + i * h2_val) % self.size

    def add(self, item: str):
        for idx in self._hashes(item):
            self.bits[idx] = 1

    def contains(self, item: str) -> bool:
        return all(self.bits[idx] for idx in self._hashes(item))
