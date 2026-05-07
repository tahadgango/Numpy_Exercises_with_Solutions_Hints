import pandas as pd
import numpy as np
from collections import defaultdict

n = 10

nums = np.array([1,2,3,4,5,6], dtype='int8')
sums = defaultdict(int)
rng = np.random.default_rng()

couples = defaultdict(list)
for n1 in nums:
    for n2 in nums:
        couples[n1+n2].append((int(n1),int(n2)))

for k,v in couples.items():
    print(f"{k}: {v}")
    
nums1 = rng.choice(nums, size=n)
nums2 = rng.choice(nums, size=n)

sums = nums1 + nums2

keys, counts = np.unique(sums, return_counts=True)
for k,v in zip(keys, counts):
    print(f"{k}: {v}")


