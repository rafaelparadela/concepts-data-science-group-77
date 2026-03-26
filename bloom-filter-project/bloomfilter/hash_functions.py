# Hash functions used for the Bloom filter
import hashlib

def h1(x: bytes) -> int:
    # First hash function (blake2b)
    return int(hashlib.blake2b(x, digest_size=8).hexdigest(), 16)

def h2(x: bytes) -> int:
    # Second hash function (sha256)
    return int(hashlib.sha256(x).hexdigest(), 16)

def get_hashes(item, k, m):
    # Convert item to bytes (needed for hashlib)
    x = str(item).encode("utf-8")

    # Compute two base hashes
    hash1 = h1(x)
    hash2 = h2(x)

    # Generate k indices using double hashing
    hashes = []
    for i in range(k):
        index = (hash1 + i * hash2) % m
        hashes.append(index)

    return hashes
