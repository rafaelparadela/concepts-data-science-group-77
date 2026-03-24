# concepts-data-science-group-77
Concepts of Data Science - Group 77

## Optimization

This Bloom Filter implementation utilizes an optimization developped by Kirsh and Mitzenmacher[1]. By utilizing a Poisson approximation, the authors successfully prove that the asymptotic false positive probability of their Double Hashing scheme converges to exactly the same formula as the standard Bloom filter: $(1−e^{−kn/m})^k$.

In Double Hashing $k$ hash functions are generated using the formula:

$$g_i(x) = h_1(x)+ i\cdot h_2(x) \% m$$

$g_i(x)$ is the ith hash function computed from the original 2 hash functions $h_1(x)$ and $h_2(x)$. i ranges from 0 (only $h_1(x)$ position is flipped) to $k-1$ ($k$ total functions are returned). $m$ is the total number of bits in the filter. Hence, only two hash functions $h_1(x)$ and $h_2(x)$ need to be computed in order to encode a single word. 

## Environment

To recreate the environment and create a dedicated Jupyter kernel, run:

```bash
conda env create -f bloomenv.yaml
conda activate bloomenv
python -m ipykernel install --user --name=bloomenv --display-name="Bloom Filter Env"
```

## References

[1] Kirsch, A., & Mitzenmacher, M. (2008). Less hashing, same performance: Building a better Bloom filter. Random Structures & Algorithms, 33(2), 187-218. https://doi.org/10.1002/rsa.20208