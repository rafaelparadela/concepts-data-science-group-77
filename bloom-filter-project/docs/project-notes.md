# Requirements

- Add README: content of the repository + a summary of your conclusions
- Commit often since the number of commits are an evaluation criteria
- Object-oriented approach of functional approach
- Easy-to-read code with clear documentation
- Implement Bloom filter as
	1. Python module for testing and demonstration in Jupyter notebook
	2. Python script for benchmarking on the HPC
- Test thoroughly for correctness
	- Define a family of hash functions
	- Test with at least two data types
- Discuss the expected time and space complexity of your implementation
- Test the performance with a large data sample
	- Time the insert and search functions for an increasing number of words
	- Create plots (number of words X run time)
	- Use HPC
	- Include the job script + Python test scripts + output of the benchmark runs
- Check `Number of words` X `False positive rate` (including the number of words that exceed the designed limit)
- Check the compression rate of a Bloom filter as a function of the expected number of and  the rate of false positives.

Deadline June 14, 2026

# Bloom filter notes

## Resources
[Medium](https://medium.com/@sylvain.tiset/bloom-filters-101-the-power-of-probabilistic-data-structures-ef1b4a422b0b)
[Wikipedia](https://en.wikipedia.org/wiki/Bloom_filter)
[Brilliant](https://brilliant.org/wiki/bloom-filter/)
[GeeksforGeeks](https://www.geeksforgeeks.org/python/bloom-filters-introduction-and-python-implementation/)

## Formulas

The probability that a bit is still zero after one insertion: $$(1-\frac{1}{m})^k$$
The probability of a bit being zero after $n$ insertions: $$(1-\frac{1}{m})^{nk}$$
Probability of False Positive: $$(1-(1-\frac{1}{m})^{nk})^k$$
FP rate approximation: $$(1-e^{-kn/m})^k$$
Optimized number of hash functions: $$k=\ln(2)\frac{m}{n}$$
Bit array size: $$m=-\frac{n\ln P}{(\ln2)^2}$$

## Time Complexity of a Bloom Filter 
### Insert operation

1. Compute **k hash functions**
2. Set **k bits** in the array

So the work is proportional to (k).

Time complexity: $O(k)$  
If $k$ is a **small constant** (like 5–10). $O(1)$ (constant time)

### Query operation

1. Compute **k hash functions**
2. Check **k bits**

Time complexity: $O(k)$
If $k$ is a **small constant** (like 5–10). $O(1)$ (constant time)
So lookups are **constant time**.

## Space Complexity

- A Bloom filter stores only the **bit array** of size (m)
- Memory used: $O(m)$
- Memory **does not grow with the number of elements stored directly**. Instead, we choose (m) in advance based on how many elements we expect.

# Slurm notes

A Slurm job script to run the `script.py` on HPC
```bash
#!/bin/bash -l

#SBATCH -- account=lp_h_ds students
#SBATCH -- cluster=wice
#SBATCH -- time=00:02:00
#SBATCH -- mem=1G

conda activate hpc_intro
python script.py
```

Useful commands
```bash
# List available accounts
sam-balance

# Run a Slurm job script
sbatch python_script.slurm

# Check the status of your job on the cluster
squeue --cluster=wice

# Cancel the job
scancel --cludter=wice <JOBID>
```


# Q&A 20/03/26

1. How to choose hash functions?
> Least correlated + most uniform options. Hash functions from libraries are acceptable.
2. How to generate test datasets of 2 datatypes?
> No need to generate, find online. The test dataset for binary trees on Blackboard can be used 
3. How many entries a large dataset contains?
> ~20-50K, unrestricted

Additional objective could be to benchmark bit arrays performance compared to lists

# Potential datasets

A word dataset for many languages, including Ukrainian [ml_spoken_languages](https://huggingface.co/datasets/MLCommons/ml_spoken_words)
A dataset containing full sentences of varying lengths: [random_Sentence](https://huggingface.co/datasets/HuggingFace-DataSet/random_Sentence)
A dataset with rsIDs of genetic variations: [ensembl_variations](https://huggingface.co/datasets/just-dna-seq/ensembl_variations/viewer/default/train?row=0)
Zebra fish DNA sequences: [Zebrafish_DNA_v0](https://huggingface.co/datasets/davidcechak/Zebrafish_DNA_v0)