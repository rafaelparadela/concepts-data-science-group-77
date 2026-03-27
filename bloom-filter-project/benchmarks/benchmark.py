import time
from bloomfilter.bloom_filter import BloomFilter


def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def benchmark_dataset(data, dataset_name):

    bf = BloomFilter(100000, 4)

    # Measure insertion time
    start_insert = time.perf_counter()
    for item in data:
        bf.add(item)
    end_insert = time.perf_counter()

    insert_time = end_insert - start_insert

    # Measure lookup time on inserted items
    start_lookup = time.perf_counter()
    for item in data:
        bf.contains(item)
    end_lookup = time.perf_counter()

    lookup_time = end_lookup - start_lookup

    return {
        "dataset": dataset_name,
        "items": len(data),
        "insert_time": round(insert_time,8),
        "lookup_time": round(lookup_time, 8)
    }

english_words = load_data("data/english_words.txt")
sentences = load_data("data/sentences.txt")
dna = load_data("data/dna.txt")

results = []

results.append(benchmark_dataset(english_words[:100], "english_words"))
results.append(benchmark_dataset(english_words[:1000], "english_words"))
results.append(benchmark_dataset(english_words[:10000], "english_words"))
results.append(benchmark_dataset(english_words[:50000], "english_words"))

results.append(benchmark_dataset(sentences[:100], "sentences"))
results.append(benchmark_dataset(sentences[:1000], "sentences"))
results.append(benchmark_dataset(sentences[:10000], "sentences"))
results.append(benchmark_dataset(sentences[:50000], "sentences"))

results.append(benchmark_dataset(dna[:100], "dna"))
results.append(benchmark_dataset(dna[:1000], "dna"))
results.append(benchmark_dataset(dna[:10000], "dna"))
results.append(benchmark_dataset(dna[:50000], "dna"))

with open("benchmarks/benchmark_results.text", "w", newline="", encoding="utf-8") as f:
    for row in results:
        print(row)
        f.write(str(row) + "\n")

