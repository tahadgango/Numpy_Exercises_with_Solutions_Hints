import numpy as np

# Make an Array
arr = np.array([1,2,3])

# Specify Type (for size efficiency)
arr = np.array([1,2,3], dtype='int16')

# Multi-Dimensional Array
arr = np.array([[1,2,3,4], [5,6,7,8]])

# Get Dimension
arr.ndim

# Get Shape
arr.shape

# Get Type
arr.dtype

# Get Element Size (bytes)
arr.itemsize

# Get Number of Elements
arr.size

# Get Array Size (bytes)
arr.nbytes # Or arr.size * arr.itemsize

# Multi-dimentional indexing [r,c] (2d)
arr[1,2]

# Get row or col
arr[:, 1]
arr[1, :]

# [startindex: endindex, nstep]
arr[0, 1:-1:2]

# 0s Array (can dtype)
zeros = np.zeros((2,3))

# 1s Array (can dtype)
ones = np.ones((2,3))

# Any other number's Array
narr = np.full((2,3), 9)

# number's Array same size of Another Array
otherarr = np.full_like(ones, 9) # Or np.full(ones.shape, 9)

# The Identity Matrix
np.identity(3)

# Repeat Array
rep = np.repeat(arr, 3) # -> [1,1,1,2,2,2,3,3,3] (axis=1)

arr = np.array([[1,2],
                [3,4]])

rep = np.repeat(arr, 2, axis=0) # Repeat Each Row
# -> [[1,2],    Row 0: 1st Time
#     [1,2],    Row 0: 2nd Time
#     [3,4],    Row 1: 1st Time
#     [3,4]]    Row 1: 2nd Time

rep = np.repeat(arr, 2, axis=1) # Repeat Each Col
#-> [[1,1,2,2],
#    [3,3,4,4]]
#    c0,c0,c1,c1

a = np.array([1,2,3])
# b points to the same memory address as a (b is not a copy array of a)
b = a
b[0] = 100 # a[0] also = 100

# Copy of Array
b = a.copy()
b[0] = 100 # a[0] does not change

# Operations on Array
add = arr + 2
mul = arr * 2
div = arr / 2 # Turn to float type
pow = arr ** 2
sin = np.sin(arr)

# Broadcasting (arr1.shape = (n1,n1, ...) arr2.shape = (m1,m2, ...) possible if every (ni,mi) satisfies: (ni = mi) or (ni = 1 or mi = 1))
r = a*b
# Matrix Mulitplication
m = np.matmul(a, b)
# Find the Determinant
d = np.linalg.det(a)

# Stastics
np.min(np.array([1,2,3]))
np.argmin(np.array([1,2,3])) # index of min value
np.max(np.array([1,2,3]))
np.sum(np.array([1,2,3]))
np.mean(np.array([1,2,3]))
np.std(np.array([1,2,3]))
np.var(np.array([1,2,3]))


arr = np.array([[1,2,3],
                [4,5,6]])
np.min(arr, axis=0) # Min in Each Col -> [1,2,3]
np.min(arr, axis=1) # Min in Each Row -> [1,4]
np.min(arr) # General Min

# Reshape Array
arr = np.array([[1,2,3,4],[5,6,7,8]])
rearr = arr.reshape((2,2,2)) # the new shape should fit the number of elements in the last shape

# Stacking

v1 = np.array([1,2,3])
v2 = np.array([4,5,6])
# Vertical Stack (v1 comes before v2)
vs = np.vstack([v1, v2]) # -> [[1,2,3], [4,5,6]]
# Number of Cols must be same

h1 = np.ones(2,4)
h2= np.zeros(2,2)
# Horizontal Stack (h1 comes before h2)
hs = np.hstack((h1, h2)) #-> [[1,1,1,1,0,0],
# Num of Rows must be same    [1,1,1,1,0,0]]                          [1,1,1,1,0,0]]

# Boolean Masking and Advanced Indexing
arr = np.array([4,1,100,3,50], [140, 10, 70, 53])

arr > 50 # Array of Booleans of shape arr.shape True if element > 50 else False
arr[arr > 50] # Array of the elements > 50

np.any(arr > 50, axis=0) # Array of size COLS True if any element > 50 in the cur col else False
np.all(arr > 50, axis=0) # Same size but True if all elements > 50 in the cur col else False

np.where(arr > 50, arr, 0) # keeps the elements > 50 and turn the rest to 0 (can use np.nan)

# Random

#random number generator
rng = np.random.default_rng() # with seed: np.random.default_rng(seed=1)
# can create you a seed for a specific rng if you give a function same inputs it will generate it once and keep returning same output everytime

rng.integers(1, 7) # random number between 1, 7 exclusive
rng.integers(low=1, high=101, size=(3,2)) # Array of shape (3,2) of random number 1, 101 exclusive
 
# General seed
np.random(seed=1)
np.random.uniform(low=-1, high=1, size=3) # Generate floats

arr= np.array([1,2,3,4])
rng.shuffle(arr) # shuffling arr (if seed exists same shuffling everytime)

rng.choice(arr) # choose a random element of arr (if seed same choice everytime)
rng.choice(arr, size=(3,2)) # make an array of shape(3,2) from the elements of arr (if seed same array will be generated)