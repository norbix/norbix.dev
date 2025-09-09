# test_algos.py
import pytest
from algos import (
    two_sum, length_of_longest_substring, merge_intervals, min_meeting_rooms,
    is_valid, next_greater, search, bounds, smallest_divisor,
    shortest_path, can_finish
)

# 1) Two Sum
@pytest.mark.parametrize("nums,target,expect", [
    ([2,7,11,15], 9, (0,1)),
    ([3,2,4], 6, (1,2)),
    ([3,3], 6, (0,1)),
    ([1,2,3], 7, None),
])
def test_two_sum(nums, target, expect):
    assert two_sum(nums, target) == expect

# 2) Longest substring without repeat
@pytest.mark.parametrize("s,expect", [
    ("", 0),
    ("aaaa", 1),
    ("abcabcbb", 3),
    ("pwwkew", 3),
    ("abcaabcd", 4),
])
def test_length_of_longest_substring(s, expect):
    assert length_of_longest_substring(s) == expect

# 3) Merge intervals
@pytest.mark.parametrize("ivals,expect", [
    ([], []),
    ([[1,3],[2,6],[8,10],[15,18]], [[1,6],[8,10],[15,18]]),
    ([[1,4],[4,5]], [[1,5]]),
])
def test_merge_intervals(ivals, expect):
    assert merge_intervals(ivals) == expect

# 4) Meeting rooms
@pytest.mark.parametrize("ivals,expect", [
    ([], 0),
    ([[0,30],[5,10],[15,20]], 2),
    ([[7,10],[2,4]], 1),
])
def test_min_meeting_rooms(ivals, expect):
    assert min_meeting_rooms(ivals) == expect

# 5) Valid parentheses
@pytest.mark.parametrize("s,expect", [
    ("", True),
    ("([]){}", True),
    ("(]", False),
    ("([)]", False),
])
def test_is_valid(s, expect):
    assert is_valid(s) is expect

# 6) Next greater
@pytest.mark.parametrize("nums,expect", [
    ([2,1,2,4,3], [4,2,4,-1,-1]),
    ([1,1,1], [-1,-1,-1]),
    ([5,4,3,2,1], [-1,-1,-1,-1,-1]),
])
def test_next_greater(nums, expect):
    assert next_greater(nums) == expect

# 7) Binary search + bounds
def test_search_and_bounds():
    xs = [1,2,2,2,5,9]
    assert search(xs, 5) == 4
    assert search(xs, 7) == -1
    assert bounds(xs, 2) == (1,4)

# 8) Binary search on answer
@pytest.mark.parametrize("nums,threshold,expect", [
    ([1,2,5,9], 6, 5),
    ([2,3,5,7,11], 11, 3),
])
def test_smallest_divisor(nums, threshold, expect):
    assert smallest_divisor(nums, threshold) == expect

# 9) Shortest path in grid
def test_shortest_path():
    g = [
        [0,0,1],
        [0,0,0],
        [1,0,0],
    ]
    assert shortest_path(g, (0,0), (2,2)) == 4
    assert shortest_path(g, (0,0), (0,2)) == -1

# 10) Course schedule
@pytest.mark.parametrize("num,prereq,expect", [
    (2, [(1,0)], True),
    (2, [(1,0),(0,1)], False),
    (4, [(1,0),(2,0),(3,1),(3,2)], True),
])
def test_can_finish(num, prereq, expect):
    assert can_finish(num, prereq) is expect
