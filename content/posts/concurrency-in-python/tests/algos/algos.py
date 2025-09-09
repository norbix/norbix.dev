# algos.py
from __future__ import annotations
from collections import Counter, deque, defaultdict
from typing import List, Tuple, Optional
import bisect
import heapq
import math


# 1) Two Sum (hash map)
def two_sum(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        y = target - x
        if y in seen:
            return (seen[y], i)
        seen[x] = i
    return None


# 2) Longest substring without repeating chars (sliding window)
def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best


# 3) Merge intervals (sorting)
def merge_intervals(ivals: List[List[int]]) -> List[List[int]]:
    if not ivals:
        return []
    ivals.sort()
    out: List[List[int]] = [ivals[0][:]]
    for s, e in ivals[1:]:
        if s > out[-1][1]:
            out.append([s, e])
        else:
            out[-1][1] = max(out[-1][1], e)
    return out


# 4) Minimum meeting rooms (heap of end times)
def min_meeting_rooms(ivals: List[List[int]]) -> int:
    if not ivals:
        return 0
    ivals.sort()
    heap: List[int] = []  # stores end times
    for s, e in ivals:
        if heap and heap[0] <= s:
            heapq.heappop(heap)
        heapq.heappush(heap, e)
    return len(heap)


# 5) Valid parentheses (stack)
def is_valid(s: str) -> bool:
    pairs = {')': '(', ']': '[', '}': '{'}
    st: List[str] = []
    for ch in s:
        if ch in "([{":
            st.append(ch)
        elif ch in ")]}":
            if not st or st.pop() != pairs[ch]:
                return False
    return not st


# 6) Next greater element to the right (monotonic stack)
def next_greater(nums: List[int]) -> List[int]:
    res = [-1] * len(nums)
    st: List[int] = []  # indices with decreasing values
    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            res[st.pop()] = x
        st.append(i)
    return res


# 7) Binary search (exact + bounds)
def search(xs: List[int], target: int) -> int:
    i = bisect.bisect_left(xs, target)
    return i if i < len(xs) and xs[i] == target else -1


def bounds(xs: List[int], x: int) -> Tuple[int, int]:
    return bisect.bisect_left(xs, x), bisect.bisect_right(xs, x)


# 8) Binary search on answer (smallest divisor under threshold)
def smallest_divisor(nums: List[int], threshold: int) -> int:
    lo, hi = 1, max(nums)

    def ok(d: int) -> bool:
        # ceil(x/d) = (x + d - 1)//d
        return sum((x + d - 1) // d for x in nums) <= threshold

    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


# 9) Shortest path in grid (BFS 4-dir), walls=1
def shortest_path(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> int:
    R, C = len(grid), len(grid[0])
    (sr, sc), (gr, gc) = start, goal
    q = deque([((sr, sc), 0)])
    seen = {(sr, sc)}
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while q:
        (r, c), d = q.popleft()
        if (r, c) == (gr, gc):
            return d
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append(((nr, nc), d + 1))
    return -1


# 10) Course schedule (topological sort / cycle check)
def can_finish(num: int, prereq: List[Tuple[int, int]]) -> bool:
    adj: dict[int, List[int]] = defaultdict(list)
    indeg = [0] * num
    for a, b in prereq:  # b -> a
        adj[b].append(a)
        indeg[a] += 1
    q = deque([i for i in range(num) if indeg[i] == 0])
    seen = 0
    while q:
        u = q.popleft()
        seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return seen == num
