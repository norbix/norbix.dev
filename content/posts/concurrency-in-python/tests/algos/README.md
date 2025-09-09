# Core SWE Patterns (Python) — Quick Cues & Complexity

**Two Sum (hash map)**
- Cue: pair sums to target.
- Idea: store seen[value] = index; check target - x.
- Time: O(n) | Space: O(n)

**Longest Substring w/o Repeat (sliding window)**
- Cue: “longest/shortest subarray/substring with constraint”.
- Idea: window + last index map; move left when repeat.
- O(n) | O(k) alphabet

**Merge Intervals (sort + sweep)**
- Cue: merge/insert intervals, meeting rooms, timelines.
- Idea: sort by start; extend current end.
- O(n log n)

**Meeting Rooms (min rooms)**
- Cue: min concurrent intervals.
- Idea: heap of end times; pop if end <= next start.
- O(n log n)

**Valid Parentheses (stack)**
- Cue: matching pairs, nesting.
- Idea: push opens; on close, check top.
- O(n)

**Next Greater Element (monotonic stack)**
- Cue: “next greater/warmer”, stock span.
- Idea: maintain decreasing stack of indices.
- O(n)

**Binary Search (exact/bounds)**
- Cue: sorted array, first ≥ x / first > x.
- Idea: `bisect_left/right`.
- O(log n)

**Binary Search on Answer**
- Cue: minimize/feasible monotonic predicate.
- Idea: search range [lo, hi], test `ok(mid)`.
- O(log range × cost(ok))

**Shortest Path (BFS unweighted)**
- Cue: grid/graph, unit weights.
- Idea: BFS; track seen.
- O(V+E)

**Topological Sort / Cycle (Kahn)**
- Cue: prerequisites, DAG order; detect cycle.
- Idea: indegree queue; count visited.
- O(V+E)

General tips:
- Prefer stdlib: `bisect`, `heapq`, `collections.deque`, `Counter`, `defaultdict`.
- State time/space; sketch approach; handle edge cases early.

---

# Run it

```shell
#pip install -r requirements.txt
pytest -q
```
