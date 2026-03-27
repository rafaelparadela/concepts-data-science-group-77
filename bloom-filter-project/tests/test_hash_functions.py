from bloomfilter.hash_functions import h1, h2, get_hashes

# check if hash is the same for the same word
def test_h1_is_same():
    assert h1(b"apple") == h1(b"apple")

def test_h2_is_same():
    assert h2(b"apple") == h2(b"apple")


# check if hash really returns k values
def test_get_hashes_returns_k_values():
    assert len(get_hashes("apple", k=5, m=100)) == 5

# check if hash really is in m limit
def test_get_hashes_are_in_m_limit():
    assert all(0 <= h < 100 for h in get_hashes("apple", k=5, m=100))


# check if get hash is the same for the same word
def test_get_hashes_is_deterministic():
    assert get_hashes("apple", k=5, m=100) == get_hashes("apple", k=5, m=100)
