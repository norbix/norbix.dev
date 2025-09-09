+++
date = '2025-09-09T16:00:00+02:00'
draft = false
title = 'Concurrency in Python'
tags = ["python", "concurrency", "parallelism", "asyncio", "multiprocessing", "threads"]
categories = ["backend", "python"]
summary = "Learn how Python handles concurrency and parallelism using threads, processes, and async with asyncio."
comments = true
ShowToc = true
TocOpen = true
image = "python-concurrency-banner.jpg"
weight = 23
+++

![banner](banner.jpg)

## 🧠 Concurrency in Python: Threads, Processes, and Async

Python’s concurrency story is unique. Unlike Go, where goroutines are built into the runtime, Python offers **multiple concurrency models**—each suited for different workloads.

In this article, we’ll break down:

- What concurrency and parallelism mean in Python
- The impact of the Global Interpreter Lock (GIL)
- Threads, processes, and async
- Real-world concurrency patterns with code examples

---

## 🚦 Concurrency vs. Parallelism

- **Concurrency**: Structuring your program to handle multiple tasks at once (e.g., switching between them).
- **Parallelism**: Actually running tasks simultaneously on multiple CPU cores.

👉 In Python:
- Use **threads/asyncio** for I/O-bound work.
- Use **processes** for CPU-bound work (to bypass the GIL).

---

## 🧱 The GIL (Global Interpreter Lock)

- Python’s GIL ensures only one thread executes Python bytecode at a time.
- This means threads won’t speed up CPU-bound code.
- But I/O-bound tasks (network, file, DB) **can benefit greatly from threads or async**.

---

## 🧵 Threads

Threads give you simple concurrency for I/O-bound workloads.

```python
from concurrent.futures import ThreadPoolExecutor
import urllib.request, time

def fetch(url):
    with urllib.request.urlopen(url) as r:
        return url, len(r.read())

urls = ["https://example.com"] * 5

t0 = time.perf_counter()
with ThreadPoolExecutor(max_workers=5) as ex:
    results = list(ex.map(fetch, urls))

print("Fetched:", results)
print("Time:", time.perf_counter() - t0)
```

✅ **Best for: making many API calls, scraping, or waiting on slow I/O.**

---

## ⚡ Multiprocessing

For CPU-bound tasks, use processes to run code in parallel.

```python
from concurrent.futures import ProcessPoolExecutor

def is_prime(n: int) -> bool:
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

nums = [10_000_019 + i for i in range(10)]

with ProcessPoolExecutor() as ex:
    results = list(ex.map(is_prime, nums))

print(results)
```

✅ **Best for: CPU-heavy math, data processing, machine learning preprocessing.**

---

## Async with asyncio

Python’s asyncio provides cooperative multitasking—tasks give up control with await so others can run.

```python
import asyncio, aiohttp

async def fetch(session, url):
    async with session.get(url) as resp:
        return url, await resp.text()

async def main():
    urls = ["https://example.com"] * 5
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch(session, u)) for u in urls]
        results = await asyncio.gather(*tasks)
        print(results)

asyncio.run(main())
```

✅ **Best for: high-throughput APIs, chat servers, pipelines.**

---

## ⏱️ Timeout & Cancellation

Async tasks can be cancelled gracefully.

```python
import asyncio

async def slow_task():
    await asyncio.sleep(5)
    return "done"

async def main():
    try:
        await asyncio.wait_for(slow_task(), timeout=2)
    except asyncio.TimeoutError:
        print("Task timed out!")

asyncio.run(main())
```

---

## 🛠️ Concurrency Patterns in Python

1. Thread pool for I/O work

1. Process pool for CPU work

1. Async pipelines for structured concurrency

1. Queues and semaphores for backpressure and flow control

1. Cancellation & timeouts for robustness

---

## 🧠 Final Thoughts

Python offers multiple tools for concurrency:

- Threads: Easy, but limited by the GIL (good for I/O).

- Processes: True parallelism, bypasses the GIL (good for CPU).

- Asyncio: Structured, scalable concurrency (good for I/O-heavy apps).

### ✅ Key Takeaways:

- Pick threads or asyncio for I/O.

- Pick processes for CPU.

- Combine them for real-world systems.

---

🚀 Follow me on [norbix.dev](https://norbix.dev) for more insights on Go, Python, AI, system design, and engineering wisdom.
