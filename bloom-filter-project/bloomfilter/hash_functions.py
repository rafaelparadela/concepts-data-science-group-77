import hashlib


def h1(x: bytes) -> int:
    return int(hashlib.blake2b(x, digest_size=8).hexdigest(), 16)


def h2(x: bytes) -> int:
    return int(hashlib.sha256(x).hexdigest(), 16)
