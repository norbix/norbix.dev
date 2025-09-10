+++
date = '2025-07-24T18:10:25+02:00'
draft = false
title = 'DSA - Data Structures and Algorithms'
tags = ["go", "golang", "python", "algorithms", "data-structures"]
categories = ["backend", "golang", "python"]
summary = "A deep dive into Data Structures and Algorithms (DSA) using Go and its Python counterpart, covering essential concepts, implementations, and best practices."
comments = true
ShowToc = true
TocOpen = true
image = "banner.jpg"
weight = 6
+++

![banner](banner.jpg)

---

## 🧠 Mastering Data Structures and Algorithms (DSA) with `Go` and  its `Python` Counterpart 

Whether you're preparing for technical interviews, optimizing backend systems, or simply sharpening your problem-solving chops, Data Structures and Algorithms (DSA) are foundational to your success as a developer.

In this article, I’ll walk you through core DSA concepts using `Golang` and `Python`, a language praised for its simplicity, performance, and concurrency model. You'll see how Go makes understanding DSA both intuitive and powerful.

---

## 🚀 What is DSA?

Data Structures organize and store data efficiently, while Algorithms define step-by-step instructions to solve problems or manipulate data.

Together, DSA provides the backbone for high-performance applications.

---

## 📦 Essential Data Structures in `Go` and its `Python` Counterpart

1. Arrays & Slices

    Go implementation:

    ```go
    arr := [5]int{1, 2, 3, 4, 5} // Fixed-size array
    slice := []int{1, 2, 3}      // Dynamic size
    
    slice = append(slice, 4)
    fmt.Println(slice) // [1 2 3 4]
    ```

   Python implementation:

   ```python
    arr = [1, 2, 3, 4, 5]  # Dynamic array (list in Python)
    arr.append(6)
    print(arr)  # [1, 2, 3, 4, 5, 6]
   ```

    Slices are the idiomatic way to work with collections in Go. They offer flexibility while leveraging arrays under the hood.

1. Linked List

   Go doesn’t have a built-in linked list, but the container/list package provides one.

   Go implementation:

    ```go
    package main
    
    import (
    "container/list"
    "fmt"
    )
    
    func main() {
    l := list.New()
    l.PushBack("Go")
    l.PushBack("DSA")
    
        for e := l.Front(); e != nil; e = e.Next() {
            fmt.Println(e.Value)
        }
    }
    ```

   Python implementation:

   ```python
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
    
    class LinkedList:
        def __init__(self):
            self.head = None
    
        def append(self, data):
            new_node = Node(data)
            if not self.head:
                self.head = new_node
                return
            last = self.head
            while last.next:
                last = last.next
            last.next = new_node
    
        def print_list(self):
            current = self.head
            while current:
                print(current.data)
                current = current.next
    
    ll = LinkedList()
    ll.append("Python")
    ll.append("DSA")
    ll.print_list()
   ```

1. Stack (`LIFO`)

    A stack can be easily implemented using slices.

    Go implementation:

    ```go
    type Stack []int
    
    func (s *Stack) Push(v int) {
        *s = append(*s, v)
    }
    
    func (s *Stack) Pop() int {
        n := len(*s)
        val := (*s)[n-1]
        *s = (*s)[:n-1]
        return val
    }
    ```

   Python implementation:

   ```python
    class Stack:
          def __init__(self):
                self.stack = []
    
          def push(self, item):
                self.stack.append(item)  # append to the end (like Go's append)
    
          def pop(self):
                if not self.stack:
                 raise IndexError("pop from empty stack")
                return self.stack.pop()  # pop from the end (like Go's slice)
    ```

1. Queue (`FIFO`)

    Queues can also be implemented using slices.

    Go implementation:

    ```go
    type Queue []int
    
    func (q *Queue) Enqueue(v int) {
        *q = append(*q, v)
    }
    
    func (q *Queue) Dequeue() int {
        val := (*q)[0]
        *q = (*q)[1:]
        return val
    }
    ```

   Python implementation:

   ```python
   class Queue:
        def __init__(self):
            self.queue = []
   
        def enqueue(self, item):
            # append to the end (like Go's append)
            self.queue.append(item)
   
        def dequeue(self):
            if not self.queue:
                raise IndexError("dequeue from empty queue")
            # take from the front (like q[0] in Go)
            val = self.queue[0]
            self.queue = self.queue[1:]  # shrink list (like Go slice)
            return val
   ```

1. Hash Map (`Go's map`)

   Go implementation:

    ```go
    m := map[string]int{
        "apple":  5,
        "banana": 3,
    }
    fmt.Println(m["apple"]) // 5
    ```

   Python implementation:

   ```python
    m = {
        "apple": 5,
        "banana": 3,
    }
    print(m["apple"])  # 5
   ```

    **Hint:**
   Go’s built-in map is a powerful hash table implementation for key-value pairs.

---

## 🧩 Must-Know Algorithms in `Go`

1. Binary Search

    Efficient O(log n) search on sorted arrays.

    Go implementation:

    ```go
    func binarySearch(arr []int, target int) int {
        low, high := 0, len(arr)-1
    
        for low <= high {
            mid := (low + high) / 2
            if arr[mid] == target {
                return mid
            } else if arr[mid] < target {
                low = mid + 1
            } else {
                high = mid - 1
            }
        }
        return -1
    }
    ```

   Python implementation:

   ```python
    def binary_search(arr, target):
         low, high = 0, len(arr) - 1
         while low <= high:
              mid = (low + high) // 2
              if arr[mid] == target:
                   return mid
              elif arr[mid] < target:
                   low = mid + 1
              else:
                   high = mid - 1
         return -1
   ```

1. Sorting (`Bubble Sort` Example)

   Video explanation: [Bubble Sort Algorithm](https://www.youtube.com/watch?v=yIQuKSwPlro)

   Go implementation:

    ```go
    func bubbleSort(arr []int) {
        n := len(arr)
        for i := 0; i < n-1; i++ {
            for j := 0; j < n-i-1; j++ {
                if arr[j] > arr[j+1] {
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                }
            }
        }
    }
    ```

    Python implementation:
    
   ```python
    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
    ```

    For real projects, use Go’s built-in sorting:

    ```go
    sort.Ints(arr)
    ```

1. Recursion: Factorial

   Factorial of `n` (n!) is the product of all positive integers up to `n`.

    Go implementation:

    ```go
    func factorial(n int) int {
        if n == 0 {
        return 1
        }
    
        return n * factorial(n-1)
    }
    ```

   Python implementation:

   ```python
    def factorial(n):
         if n == 0:
              return 1
         return n * factorial(n-1)
   ```

   Example: The factorial of 4 is `4 * 3 * 2 * 1 = 24`.

    ```matlab
    factorial(4)
    = 4 * factorial(3)
    = 4 * (3 * factorial(2))
    = 4 * (3 * (2 * factorial(1)))
    = 4 * (3 * (2 * (1 * factorial(0))))
    = 4 * (3 * (2 * (1 * 1)))
    = 24
    ```

1. Fibonacci Sequence

   Fibonacci numbers are the sum of the two preceding ones, starting from 0 and 1.

   Go implementation:

    ```go
    func fibonacci(n int) int {
        if n <= 1 {
            return n
        }
        return fibonacci(n-1) + fibonacci(n-2)
    }
    ```

   Python implementation:

   ```python
    def fibonacci(n):
         if n <= 1:
              return n
         return fibonacci(n-1) + fibonacci(n-2)
    ```

   Example: The sequence starts as: 0, 1, 1, 2, 3, 5, 8, 13, ...

    ```matlab
    fibonacci(5)
    = fibonacci(4) + fibonacci(3)
    = (fibonacci(3) + fibonacci(2)) + (fibonacci(2) + fibonacci(1))
    = ((fibonacci(2) + fibonacci(1)) + (fibonacci(1) + fibonacci(0))) + (fibonacci(1) + 1)
    = (((fibonacci(1) + fibonacci(0)) + 1) + (1 + 0)) + (1 + 1)
    = (((1 + 0) + 1) + 1) + 2
    = 5
    ```

1. Prime Check

   Prime numbers are greater than 1 and only divisible by 1 and themselves.

    `Go` implementation:

    ```go
    func isPrime(n int) bool {
        if n <= 1 {
            return false
        }
        for i := 2; i*i <= n; i++ {
            if n%i == 0 {
                return false
            }
        }
        return true
    }
    ```

    `Python` implementation:

   ```python
    from math import sqrt
   
    def is_prime(n):
         if n <= 1:
              return False
         for i in range(2, int(sqrt(n)) + 1):
              if n % i == 0:
                return False
         return True
   ```

   Example: The number 11 is prime, while 12 is not.

    ```matlab
    isPrime(11)
    = true (11 is only divisible by 1 and 11)
    
    isPrime(12)
    = false (12 is divisible by 1, 2, 3, 4, 6, and 12)
    ```

1. FizzBuzz :)

   A classic programming challenge.

   `Go` implementation:

    ```go
    func fizzBuzz(n int) {
        for i := 1; i <= n; i++ {
            if i%3 == 0 && i%5 == 0 {
                fmt.Println("FizzBuzz")
            } else if i%3 == 0 {
                fmt.Println("Fizz")
            } else if i%5 == 0 {
                fmt.Println("Buzz")
            } else {
                fmt.Println(i)
            }
        }
    }
    ```
   
    `Python` implementation:

   ```python
   def fizz_buzz(n):
       for i in range(1, n + 1):
           if i % 3 == 0 and i % 5 == 0:
               print("FizzBuzz")
           elif i % 3 == 0:
               print("Fizz")
           elif i % 5 == 0:
               print("Buzz")
           else:
               print(i)
   ```

   Example: For `n = 15` print the numbers from 1 to 15. For multiples of 3, print "Fizz" instead of the number. For multiples of 5, print "Buzz". For numbers which are multiples of both 3 and 5, print "FizzBuzz".
    
   ```matlab
    1
    2
    Fizz
    4
    Buzz
    Fizz
    7
    8
    Fizz
    Buzz
    11
    Fizz
    13
    14
    FizzBuzz
    ```

1. Graph and Trees

    For binary trees, you define custom structures.

    Go implementation:

    ```go
   type Node struct {
	Value int
	Left  *Node
	Right *Node
    }
    ```

   Python implementation:
    
   ```python
    class Node:
          def __init__(self, value):
                self.value = value
                self.left = None
                self.right = None
     ```

    Depth-first traversal:

    Go implementation:

    ```go
    func dfs(n *Node) {
        if n == nil {
            return
        }
    
        fmt.Println(n.Value)
        dfs(n.Left)
        dfs(n.Right)
    }
    ```

   Python implementation:

   ```python
   class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

   def dfs(node):
        if node is None:
            return
   
       print(node.value)      # Preorder: visit root
       dfs(node.left)         # Traverse left subtree
       dfs(node.right)        # Traverse right subtree
   ```

---

## 🔃 Sort Algorithms

Sorting is a fundamental concept in computer science used in everything from searching to data normalization and ranking systems. Below are essential sorting algorithms every developer should know, implemented in Go.

1. Merge Sort (🧬 Divide and Conquer – O(n log n))

   Merge Sort recursively splits arrays into halves and merges them in a sorted manner.
   
   ```go
   func mergeSort(arr []int) []int {
       if len(arr) <= 1 {
           return arr
       }
   
       mid := len(arr) / 2
       left := mergeSort(arr[:mid])
       right := mergeSort(arr[mid:])
       return merge(left, right)
   }
   
   func merge(left, right []int) []int {
       result := []int{}
       i, j := 0, 0
   
       for i < len(left) && j < len(right) {
           if left[i] < right[j] {
               result = append(result, left[i])
               i++
           } else {
               result = append(result, right[j])
               j++
           }
       }
       return append(result, append(left[i:], right[j:]...)...)
   }
   ```

1. Quick Sort (⚡ Partition-based – Average: O(n log n), Worst: O(n²))

   Quick Sort selects a pivot and partitions the array into smaller and larger elements.
   
   ```go
   func quickSort(arr []int) {
       if len(arr) < 2 {
           return
       }
   
       left, right := 0, len(arr)-1
       pivot := rand.Int() % len(arr)
       arr[pivot], arr[right] = arr[right], arr[pivot]
   
       for i := range arr {
           if arr[i] < arr[right] {
               arr[i], arr[left] = arr[left], arr[i]
               left++
           }
       }
   
       arr[left], arr[right] = arr[right], arr[left]
       quickSort(arr[:left])
       quickSort(arr[left+1:])
   }
   ```

1. Bubble Sort (🫧 Simple but Inefficient – O(n²))

   Repeatedly swaps adjacent elements if they are in the wrong order.
   
   ```go
   func bubbleSort(arr []int) {
       n := len(arr)
       for i := 0; i < n-1; i++ {
           for j := 0; j < n-i-1; j++ {
               if arr[j] > arr[j+1] {
                   arr[j], arr[j+1] = arr[j+1], arr[j]
               }
           }
       }
   }
   ```

1. Insertion Sort (🧩 Efficient for Small Datasets – O(n²))

   Builds the sorted array one item at a time.
   
   ```go
   func insertionSort(arr []int) {
       for i := 1; i < len(arr); i++ {
           key := arr[i]
           j := i - 1
           for j >= 0 && arr[j] > key {
               arr[j+1] = arr[j]
               j--
           }
           arr[j+1] = key
       }
   }
   ```

1. Selection Sort (📌 Selects Minimum – O(n²))

   Repeatedly finds the minimum element and places it at the beginning.
   
   ```go
   func selectionSort(arr []int) {
       n := len(arr)
       for i := 0; i < n-1; i++ {
           minIdx := i
           for j := i + 1; j < n; j++ {
               if arr[j] < arr[minIdx] {
                   minIdx = j
               }
           }
           arr[i], arr[minIdx] = arr[minIdx], arr[i]
       }
   }
   ```

1. Heap Sort (🏗️ Priority Queue-based – O(n log n))

   Uses a binary heap structure to repeatedly extract the max element.
   
   ```go
   func heapSort(arr []int) {
       n := len(arr)
   
       // Build max heap
       for i := n/2 - 1; i >= 0; i-- {
           heapify(arr, n, i)
       }
   
       for i := n - 1; i > 0; i-- {
           arr[0], arr[i] = arr[i], arr[0]
           heapify(arr, i, 0)
       }
   }
   
   func heapify(arr []int, n, i int) {
       largest := i
       left := 2*i + 1
       right := 2*i + 2
   
       if left < n && arr[left] > arr[largest] {
           largest = left
       }
       if right < n && arr[right] > arr[largest] {
           largest = right
       }
   
       if largest != i {
           arr[i], arr[largest] = arr[largest], arr[i]
           heapify(arr, n, largest)
       }
   }
   ```

Each of these sorting algorithms serves different use cases. While Go’s sort package provides optimized versions, understanding how these work internally is critical for building performance-conscious software.

---

## 📑 Sorting Algorithms - Cheat Sheet

| Algorithm       | Best Time    | Avg Time     | Worst Time   | Space     | Stable | In-Place | Notes                               |
|----------------|--------------|--------------|--------------|-----------|--------|----------|-------------------------------------|
| **Merge Sort**  | O(n log n)   | O(n log n)   | O(n log n)   | O(n)      | ✅ Yes | ❌ No     | Divide and conquer, great for linked lists |
| **Quick Sort**  | O(n log n)   | O(n log n)   | O(n²)        | O(log n)  | ❌ No  | ✅ Yes    | Very fast in practice, not stable   |
| **Bubble Sort** | O(n)         | O(n²)        | O(n²)        | O(1)      | ✅ Yes | ✅ Yes    | Educational use only, very slow     |
| **Insertion Sort** | O(n)     | O(n²)        | O(n²)        | O(1)      | ✅ Yes | ✅ Yes    | Efficient for small or nearly sorted data |
| **Selection Sort** | O(n²)    | O(n²)        | O(n²)        | O(1)      | ❌ No  | ✅ Yes    | Always O(n²), rarely used           |
| **Heap Sort**   | O(n log n)   | O(n log n)   | O(n log n)   | O(1)      | ❌ No  | ✅ Yes    | Good for priority queues            |

> ✅ **Stable**: Maintains the relative order of equal elements  
> ✅ **In-Place**: Uses constant extra space (excluding recursion stack)

---

## 🔍 Search Algorithms

Search algorithms are foundational tools in computer science used to retrieve information stored in data structures like arrays, trees, or graphs. Whether you're working with sorted arrays, exploring hierarchical structures, or traversing complex graphs, the right search algorithm can dramatically improve efficiency and performance.

Let’s dive into three essential search algorithms and their Go implementations:

1. 🧭 Binary Search

   Use Case: Efficiently search for a value in a sorted array.
   Time Complexity: O(log n)
   Space Complexity: O(1) (iterative), O(log n) (recursive)
   
   Concept:
   Binary Search divides the array into halves, eliminating one half at each step, depending on whether the target is greater or smaller than the midpoint.
   
   ```go
   func BinarySearch(arr []int, target int) int {
       left, right := 0, len(arr)-1
       for left <= right {
           mid := left + (right-left)/2
           if arr[mid] == target {
               return mid
           } else if arr[mid] < target {
               left = mid + 1
           } else {
               right = mid - 1
           }
       }
       return -1 // not found
   }
   ```

1.  🌐 Breadth-First Search (BFS)

   Use Case: Traverse or search tree/graph level by level. Ideal for finding the shortest path in unweighted graphs.
   Time Complexity: O(V + E) (vertices + edges)
   Space Complexity: O(V)
   
   Concept:
   BFS uses a queue to explore all neighboring nodes before going deeper. It’s a level-order traversal for trees or graphs.
   
   ```go
   func BFS(graph map[int][]int, start int) []int {
       visited := make(map[int]bool)
       queue := []int{start}
       result := []int{}
   
       for len(queue) > 0 {
           node := queue[0]
           queue = queue[1:]
   
           if visited[node] {
               continue
           }
           visited[node] = true
           result = append(result, node)
   
           for _, neighbor := range graph[node] {
               if !visited[neighbor] {
                   queue = append(queue, neighbor)
               }
           }
       }
       return result
   }
   ```

1. 🧱 Depth-First Search (DFS)

   Use Case: Explore all paths or check for connectivity in graphs/trees. Great for scenarios like maze-solving, backtracking, and topological sorting.
   Time Complexity: O(V + E)
   Space Complexity: O(V) (recursive stack or visited map)
   
   Concept:
   DFS explores as far as possible along each branch before backtracking. Implemented with recursion or a stack.
   
   ```go
   func DFS(graph map[int][]int, start int, visited map[int]bool, result *[]int) {
       if visited[start] {
           return
       }
       visited[start] = true
       *result = append(*result, start)
   
       for _, neighbor := range graph[start] {
           if !visited[neighbor] {
               DFS(graph, neighbor, visited, result)
           }
       }
   }
   ```
   
   To initiate `DFS`:
   
   ```go
   graph := map[int][]int{
       1: {2, 3},
       2: {4},
       3: {},
       4: {},
   }
   visited := make(map[int]bool)
   result := []int{}
   DFS(graph, 1, visited, &result)
   fmt.Println(result) // Output: [1 2 4 3] (DFS order may vary)
   ```

---

## 🔍 Search Algorithms – Cheat Sheet

| Algorithm | Use Case | Time Complexity | Space Complexity | Notes |
|----------|----------|------------------|------------------|-------|
| **Binary Search** | Search in sorted arrays | O(log n) | O(1) (iterative)<br>O(log n) (recursive) | Requires sorted input |
| **Breadth-First Search (BFS)** | Shortest path in unweighted graphs | O(V + E) | O(V) | Level-order traversal, uses a queue |
| **Depth-First Search (DFS)** | Exploring all paths, topological sort, cycle detection | O(V + E) | O(V) | Preorder traversal, uses recursion or stack |

---

## 🌳 Tree Traversal Algorithms

Traversing a tree means visiting every node in a specific order. Whether you're parsing expressions, printing a binary tree, or converting structures, understanding traversal strategies is fundamental in computer science.

This guide covers the four most common tree traversal algorithms:

   - Pre-Order Traversal

   - In-Order Traversal

   - Post-Order Traversal

   - Level-Order Traversal

1. 📐 Tree Node Definition in Go

   Before diving into each traversal, here’s the standard binary tree structure we'll use:
   
   ```go
   type TreeNode struct {
       Val   int
       Left  *TreeNode
       Right *TreeNode
   }
   ```

1. 🔁 Pre-Order Traversal (Root → Left → Right)

   Use Case:
   Useful for copying a tree or prefix expression evaluation.

   Steps:

   1. Visit root

   1. Traverse left subtree

   1. Traverse right subtree

   ```go
   func PreOrder(node *TreeNode, result *[]int) {
       if node == nil {
           return
       }
       *result = append(*result, node.Val)
       PreOrder(node.Left, result)
       PreOrder(node.Right, result)
   }
   ```

1. 📏 In-Order Traversal (Left → Root → Right)

   Use Case:
   Yields nodes in ascending order for Binary Search Trees (BST).
   
   Steps:
   
    1. Traverse left subtree
   
    1. Visit root
   
    1. Traverse right subtree

   ```go
   func InOrder(node *TreeNode, result *[]int) {
       if node == nil {
           return
       }
       InOrder(node.Left, result)
       *result = append(*result, node.Val)
       InOrder(node.Right, result)
   }
   ```

1. 🧮 Post-Order Traversal (Left → Right → Root)

   Use Case:
   Ideal for deleting or freeing nodes, postfix expression evaluation.
   
   Steps:
   
    1. Traverse left subtree
   
    1. Traverse right subtree
   
    1. Visit root
   
   ```go
   func PostOrder(node *TreeNode, result *[]int) {
       if node == nil {
           return
       }
       PostOrder(node.Left, result)
       PostOrder(node.Right, result)
       *result = append(*result, node.Val)
   }
   ```


1. 🏛️ Level-Order Traversal (Breadth-First)

   Use Case:
   Used for printing trees by level or finding the shortest path in a tree.
   
   Steps:
   
    1. Traverse nodes level by level (left to right)
   
   ```go
   func LevelOrder(root *TreeNode) []int {
       if root == nil {
           return nil
       }
   
       queue := []*TreeNode{root}
       var result []int
   
       for len(queue) > 0 {
           node := queue[0]
           queue = queue[1:]
           result = append(result, node.Val)
   
           if node.Left != nil {
               queue = append(queue, node.Left)
           }
           if node.Right != nil {
               queue = append(queue, node.Right)
           }
       }
       return result
   }
   ```

1. 🔧 Test Tree Example

   ```go
   // Construct the following tree:
   //      1
   //     / \
   //    2   3
   //   / \   \
   //  4   5   6
   
   root := &TreeNode{Val: 1}
   root.Left = &TreeNode{Val: 2}
   root.Right = &TreeNode{Val: 3}
   root.Left.Left = &TreeNode{Val: 4}
   root.Left.Right = &TreeNode{Val: 5}
   root.Right.Right = &TreeNode{Val: 6}
   
   var pre, in, post []int
   PreOrder(root, &pre)
   InOrder(root, &in)
   PostOrder(root, &post)
   level := LevelOrder(root)
   
   fmt.Println("Pre-Order:", pre)    // [1 2 4 5 3 6]
   fmt.Println("In-Order:", in)      // [4 2 5 1 3 6]
   fmt.Println("Post-Order:", post)  // [4 5 2 6 3 1]
   fmt.Println("Level-Order:", level)// [1 2 3 4 5 6]
   ```

1. ⚙️ Quick Go Snippets

   ```go
   // Pre-Order Traversal
   func PreOrder(node *TreeNode, result *[]int) {
       if node == nil {
           return
       }
       *result = append(*result, node.Val)
       PreOrder(node.Left, result)
       PreOrder(node.Right, result)
   }
   
   // In-Order Traversal
   func InOrder(node *TreeNode, result *[]int) {
       if node == nil {
           return
       }
       InOrder(node.Left, result)
       *result = append(*result, node.Val)
       InOrder(node.Right, result)
   }
   
   // Post-Order Traversal
   func PostOrder(node *TreeNode, result *[]int) {
       if node == nil {
           return
       }
       PostOrder(node.Left, result)
       PostOrder(node.Right, result)
       *result = append(*result, node.Val)
   }
   
   // Level-Order Traversal (BFS)
   func LevelOrder(root *TreeNode) []int {
       if root == nil {
           return nil
       }
       queue := []*TreeNode{root}
       var result []int
   
       for len(queue) > 0 {
           node := queue[0]
           queue = queue[1:]
           result = append(result, node.Val)
   
           if node.Left != nil {
               queue = append(queue, node.Left)
           }
           if node.Right != nil {
               queue = append(queue, node.Right)
           }
       }
       return result
   }
   ```

---

## 🌳 Tree Traversal Algorithms – Cheat Sheet

 Traversal Type  | Visit Order                | Use Case                          | Time Complexity | Space Complexity |
|-----------------|----------------------------|-----------------------------------|------------------|------------------|
| **Pre-Order**   | Root → Left → Right        | Copy tree, prefix expressions     | O(n)            | O(h)             |
| **In-Order**    | Left → Root → Right        | Sorted output in BSTs             | O(n)            | O(h)             |
| **Post-Order**  | Left → Right → Root        | Delete tree, postfix expressions  | O(n)            | O(h)             |
| **Level-Order** | Level by level (BFS)       | Print by level, shortest path     | O(n)            | O(w)             |

**Legend**:
- `n`: number of nodes
- `h`: tree height (log n for balanced, n for skewed)
- `w`: max width of the tree (can be up to n/2 in balanced trees)

---

## ➗ The Modulo Operator (%)

The modulo operator is often underestimated, but it’s a fundamental tool in both algorithm design and real-world programming.

### What Is Modulo?

`a % b` returns the remainder after dividing `a` by `b`.

   ```matlab
   a = b × q + r where 0 ≤ r < b
   ```

- Example: `5 % 2 = 1`

- Example: `12 % 5 = 2`

- Example: `20 % 5 = 0`

👉 If `a < b`, then `a % b = a`.

### When Do We Use Modulo?

1. Checking Divisibility

   It is used to check if a number is even or odd.

   Go implementation:

   ```go
   if n%2 == 0 {
       fmt.Println("Even")
   } else {
       fmt.Println("Odd")
   }
   ```

   Python implementation:

   ```python
   if n % 2 == 0:
       print("Even")
   else:
       print("Odd")
   ```

1. Cyclic Patterns (wrap-around

   Go implementation:

   ```go
   days := []string{"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"}
   dayIndex := (currentDay + offset) % 7
   fmt.Println(days[dayIndex])
   ```

   Python implementation:

   ```python
   days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
   day_index = (current_day + offset) % 7
   print(days[day_index])
   ```

1. Rotating Arrays

   It is often used in problems involving rotations or circular shifts.

    Go implementation:
    
    ```go
    func rotate(arr []int, k int) []int {
         n := len(arr)
         k = k % n // handle k > n
         return append(arr[n-k:], arr[:n-k]...)
    }
    ```
    
    Python implementation:
    
    ```python
    def rotate(arr, k):
          n = len(arr)
          k = k % n  # handle k > n
          return arr[-k:] + arr[:-k]
    ```

1. Hashing

   It is commonly used in hash functions to ensure values fit within a fixed range.

    Go implementation:
    
    ```go
    hash := (key % tableSize + tableSize) % tableSize // handle negative keys
    ```
    
    Python implementation:
    
    ```python
    hash = (key % table_size + table_size) % table_size  # handle negative keys
    ```

1. Circular Buffers

   It is used to wrap indices around when they exceed the buffer size.

    Go implementation:
    
    ```go
    nextIndex := (currentIndex + 1) % bufferSize
    ```
    
    Python implementation:
    
    ```python
    next_index = (current_index + 1) % buffer_size
    ```

### Key Insights

Modulo is the perfect operator when dealing with:

- Repetition (time, days, rotations)

- Bounded ranges (array indices, hash maps)

- Divisibility checks

Think of % as the wrap-around operator — it keeps numbers within limits.

---

## 🧠 Tips for Learning DSA with Go

- Practice problems: Use platforms like [LeetCode](https://leetcode.com/), [HackerRank](https://www.hackerrank.com/), or [Exercism](https://exercism.org/).
- Understand time complexity: Know Big-O analysis for every structure and algorithm.
- Build mini-projects: Implement your own `LRU Cache`, `Trie`, or `Priority Queue`.

---

## 🎯 Final Thoughts

Mastering DSA not only sharpens your coding skills but also prepares you for systems design, performance optimization, and real-world problem-solving.

With Go’s clean syntax and powerful standard library, you're equipped to tackle DSA challenges efficiently and idiomatically.

---

🚀 Follow me on [norbix.dev](https://norbix.dev) for more insights on Go, Python, AI, system design, and engineering wisdom.
