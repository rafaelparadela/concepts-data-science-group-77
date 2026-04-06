import random
import math
import json
from bloomfilter.bloom_filter import BloomFilter


# === Config ===
M = 100_000          # Bloom filter size (bits)
K = 4                # number of hash functions
FPR_SAMPLE_SIZE = 1_000
RANDOM_SEED = 42

random.seed(RANDOM_SEED)


# === Utils ===
def load_data(path):
    """Loads the dataset"""
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def measure_fpr(bf, negatives, sample_size=FPR_SAMPLE_SIZE):
    """Computes FPR on a BF and a set of True Negatives"""
    if not negatives:
        return 0.0

    sample = random.sample(negatives, min(sample_size, len(negatives)))
    false_positives = sum(1 for x in sample if bf.contains(x))

    return false_positives / len(sample)


def theoretical_fpr(m, k, n):
    """Calcualtes a theoretical FPR rate"""
    return (1 - math.exp(-k * n / m)) ** k


# === The Main Exeriment ===
def run_fpr_experiment(data, dataset_name):

    results = []

    # Expected capacity
    expected_n = M * math.log(2) / K   # e.g. assume 10 bits per element

    # Test sizes (including overfill)
    sizes = [
        100,
        1000,
        5000,
        10000,
        int(expected_n),
        int(expected_n * 1.5),
        int(expected_n * 2),
        int(expected_n * 2.5),
    ]

    sizes = [s for s in sizes if s <= len(data)]
    print(sizes)
    full_set = set(data)

    for n in sizes:
        inserted = data[:n]
        inserted_set = set(inserted)

        # Prepare negatives efficiently
        negatives = list(full_set - inserted_set)

        bf = BloomFilter(M, K)

        # Insert elements
        for item in inserted:
            bf.add(item)

        # Measure FPR
        fpr = measure_fpr(bf, negatives)

        # Theoretical FPR
        fpr_theory = theoretical_fpr(M, K, n)

        results.append({
            "dataset": dataset_name,
            "n_inserted": n,
            "load_factor": round(n / M, 6),
            "fpr_measured": round(fpr, 6),
            "fpr_theoretical": round(fpr_theory, 6),
            "over_capacity": n > expected_n
        })

        print(results[-1])

    return results


# === Run ===
if __name__ == "__main__":

    english_words = load_data("data/english_words.txt")
    sentences = load_data("data/sentences.txt")
    dna = load_data("data/dna.txt")

    all_results = []
    all_results += run_fpr_experiment(english_words, "english_words")
    all_results += run_fpr_experiment(sentences, "sentences")
    all_results += run_fpr_experiment(dna, "dna")

    # Save results
    with open("benchmarks/fpr_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
