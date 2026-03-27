from bloomfilter.bloom_filter import BloomFilter

# test single word
def test_added_item_is_found():
    bf = BloomFilter(size=1000, hash_count=5)
    word = "apple"
    bf.add(word)
    assert bf.contains(word)

# test sentence
def test_sentence_input():
    bf = BloomFilter(size=1000, hash_count=5)
    sentence = "This is a test sentence"
    bf.add(sentence)
    assert bf.contains(sentence)

# test dna
def test_dna_input():
    bf = BloomFilter(size=1000, hash_count=5)
    dna = "ACGTACGTACGTACGT"
    bf.add(dna)
    assert bf.contains(dna)