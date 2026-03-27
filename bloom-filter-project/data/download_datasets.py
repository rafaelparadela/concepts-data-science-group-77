import requests
from datasets import load_dataset
import random

# size limit
size_limit = 50000

# English words
url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
response = requests.get(url, timeout=10)
words = response.text.splitlines()
words = words[:size_limit]

with open("bloom-filter-project/data/english_words.txt", "w", encoding="utf-8") as f:
    for w in words:
        f.write(w + "\n")

# English sentences
ds = load_dataset("HuggingFace-DataSet/random_Sentence", split="train")
sentences = ds["Medium"][:size_limit]

with open("bloom-filter-project/data/sentences.txt", "w", encoding="utf-8") as f:
    for s in sentences:
        f.write(s.strip() + "\n")

# DNA Codes
nucleotides = ["A", "C", "G", "T"]

dna = ["".join(random.choices(nucleotides, k=20)) for _ in range(size_limit)]

with open("bloom-filter-project/data/dna.txt", "w", encoding="utf-8") as f:
    for d in dna:
        f.write(d.strip() + "\n")
