import random
import math
import json
from bloomfilter.bloom_filter import BloomFilter


# === Config ===
FPR_TARGETS = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2]   # target false positive rates
RANDOM_SEED = 42

random.seed(RANDOM_SEED)


# === Utils ===
def load_data(path):
    """Loads the dataset"""
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def optimal_m(n, fpr):
    """Optimal Bloom filter bit size m for n elements and target FPR."""
    return math.ceil(-n * math.log(fpr) / (math.log(2) ** 2))


def optimal_k(m, n):
    """Optimal number of hash functions k given m bits and n elements."""
    return max(1, round((m / n) * math.log(2)))


def theoretical_fpr(m, k, n):
    """Theoretical FPR for given m, k, n."""
    return (1 - math.exp(-k * n / m)) ** k


def measure_fpr(bf, negatives, sample_size=1_000):
    """Measures empirical FPR on true negatives."""
    if not negatives:
        return 0.0
    sample = random.sample(negatives, min(sample_size, len(negatives)))
    false_positives = sum(1 for x in sample if bf.contains(x))
    return false_positives / len(sample)


def naive_set_size_bits(n, avg_bytes_per_element):
    """
    Baseline: storing n elements as a plain set.
    Approximates memory as n * avg_bytes_per_element * 8 bits.
    """
    return n * avg_bytes_per_element * 8


# === The Main Experiment ===
def run_compression_experiment(data, dataset_name):
    """
    For each combination of (n_inserted, fpr_target):
      - Compute optimal m and k for the target FPR
      - Build a Bloom filter and insert n elements
      - Compute:
          * compression_ratio = naive_set_bits / bloom_bits
          * bits_per_element  = m / n
          * measured FPR      (empirical check)
          * theoretical FPR   (sanity check)
    """

    results = []

    # Representative element sizes per dataset type
    avg_bytes = sum(len(x.encode("utf-8")) for x in data[:1000]) / min(1000, len(data))

    # Test a range of n values
    sizes = sorted(set([
        100,
        500,
        1_000,
        5_000,
        10_000,
        50_000,
        min(100_000, len(data)),
    ]))
    sizes = [s for s in sizes if s <= len(data)]

    full_set = set(data)

    print(f"\n=== Dataset: {dataset_name} | avg element size: {avg_bytes:.1f} bytes ===")

    for n in sizes:
        inserted = data[:n]
        inserted_set = set(inserted)
        negatives = list(full_set - inserted_set)

        for fpr_target in FPR_TARGETS:
            # Optimal filter parameters for this (n, fpr_target)
            m = optimal_m(n, fpr_target)
            k = optimal_k(m, n)

            # Build and populate the Bloom filter
            bf = BloomFilter(m, k)
            for item in inserted:
                bf.add(item)

            # Empirical and theoretical FPR
            fpr_measured = measure_fpr(bf, negatives)
            fpr_theory = theoretical_fpr(m, k, n)

            # Compression metrics
            naive_bits = naive_set_size_bits(n, avg_bytes)
            compression_ratio = naive_bits / m        # >1 means BF is smaller
            bits_per_element = m / n

            record = {
                "dataset": dataset_name,
                "n_inserted": n,
                "fpr_target": fpr_target,
                "m_bits": m,
                "k_hashes": k,
                "bits_per_element": round(bits_per_element, 4),
                "naive_set_bits": int(naive_bits),
                "compression_ratio": round(compression_ratio, 4),
                "fpr_measured": round(fpr_measured, 6),
                "fpr_theoretical": round(fpr_theory, 6),
            }

            results.append(record)
            print(record)

    return results


# === Run ===
if __name__ == "__main__":

    english_words = load_data("data/english_words.txt")
    sentences     = load_data("data/sentences.txt")
    dna           = load_data("data/dna.txt")

    all_results = []
    all_results += run_compression_experiment(english_words, "english_words")
    all_results += run_compression_experiment(sentences,     "sentences")
    all_results += run_compression_experiment(dna,           "dna")

    # Save results
    with open("benchmarks/compression_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nSaved {len(all_results)} records to benchmarks/compression_results.json")