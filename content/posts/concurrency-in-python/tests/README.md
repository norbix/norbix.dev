# Notes you can mention in interviews

- Model boundary: the “model” is just a function today; swap with a real model (e.g., load a .pt/.pkl) in startup.

- Batch endpoint: improves throughput, reduces overhead.

- Validation: FastAPI’s Pydantic schemas give type validation & OpenAPI docs for free (/docs).

- Scaling: run with multiple workers (e.g., uvicorn --workers 4) behind a reverse proxy; add request timeouts & logging.

- Concurrency: I/O-bound models (remote vector DB, files) benefit from async (FastAPI); CPU-bound models may need process workers.


## Arrays & Strings

## Reverse a string (list-based, in place)

```python
def reverse_string(s: str) -> str:
    chars = list(s)          # convert string → list of chars
    left, right = 0, len(chars) - 1
    
    while left < right:      # two-pointer swap
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    
    return ''.join(chars)    # back to string
```

Example: 

```python
print(reverse_string("hello"))  # "olleh"
print(reverse_string("norbix")) # "xibron"
```

## Find first non-repeating character

```python
def first_non_repeating_char(s: str):
    freq = {}

    # Count frequency of each character
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1

    # Find first character with frequency = 1
    for ch in s:
        if freq[ch] == 1:
            return ch
    return None
```

Example: 
    
```matlab
Input: "swiss"
Output: "w"     # because 's' repeats, 'w' is first non-repeating
```

```python
print(first_non_repeating_char("swiss"))     # w
print(first_non_repeating_char("aabbcc"))    # None
print(first_non_repeating_char("alphabet"))  # l
```

## Merge two sorted arrays

```python
def merge_sorted(arr1, arr2):
    i, j = 0, 0
    merged = []

    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            merged.append(arr1[i])
            i += 1
        else:
            merged.append(arr2[j])
            j += 1

    # add leftovers
    merged += arr1[i:]
    merged += arr2[j:]
    return merged
```

Example:

```matlab
Input:  
    arr1 = [1, 3, 5] 
    arr2 = [2, 4, 6]

Output: 
    [1, 2, 3, 4, 5, 6]

Compare 1 and 2, take 1 -> merged = [1]
Compare 3 and 2, take 2 -> merged = [1, 2]
Compare 3 and 4, take 3 -> merged = [1, 2, 3]
Compare 5 and 4, take 4 -> merged = [1, 2, 3, 4]
Compare 5 and 6, take 5 -> merged = [1, 2, 3, 4, 5]
Leftover: add 6 -> merged = [1, 2, 3, 4, 5, 6]
```

```python
print(merge_sorted([1, 3, 5], [2, 4, 6]))
# [1, 2, 3, 4, 5, 6]

print(merge_sorted([1, 2, 7], [3, 4, 5, 6]))
# [1, 2, 3, 4, 5, 6, 7]
```

## Rotate an array by k steps

```python
def rotate_array(arr, k):
    n = len(arr)
    k = k % n  # handle k > n, normalize k to within array length
    
    return arr[-k:] + arr[:-k] # [last k elements] + [first n-k elements]
```

Example:
```matlab
Input:
    arr = [1, 2, 3, 4, 5]
    k = 2
Output:
    [4, 5, 1, 2, 3]
Rotate right by 2:
Take last 2 elements: [4, 5]
Take first 3 elements: [1, 2, 3]
Concatenate: [4, 5] + [1, 2, 3]
```











