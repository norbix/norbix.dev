+++
title = "Profiling Go Applications: CPU, Memory, and Concurrency Insights"
date = "2025-04-22T19:00:00+02:00"
draft = false
tags = ["go", "profiling", "performance", "pprof", "concurrency"]
categories = ["golang", "performance-engineering"]
summary = "Learn how to profile Go applications using pprof, trace, and runtime tools to uncover bottlenecks, memory leaks, and concurrency issues in production and development."
comments = true
ShowToc = true
TocOpen = true
image = "profiling-banner.jpg"
weight = 11
+++

![banner](banner.jpg)

**"Fast is fine, but profiling tells you why you're slow."**

Performance issues are often hard to debug — your app feels sluggish, CPU spikes randomly, or memory usage keeps growing. Fortunately, Go provides powerful built-in tools to profile applications and uncover these bottlenecks.

In this article, I'll walk through profiling techniques in `Go`, focusing on `CPU`, `memory`, `goroutine`, and `concurrency` analysis using tools like `pprof` and `trace`.

---

## 🔍 What Is Profiling?

Profiling is the act of measuring the performance characteristics of your application:

- Where is the CPU time being spent?

- How much memory is being allocated?

- Are goroutines being leaked?

- Is concurrency causing contention?

**Go’s standard library includes everything you need to answer these questions.**

---

## ⚙️ net/http/pprof: Built-in Profiler

The simplest way to expose profiling data is to import:

```go
import _ "net/http/pprof"
```

Add this to your HTTP server:

```go
http.ListenAndServe("localhost:6060", nil)
```

Then, access these endpoints:

- `/debug/pprof/profile` — CPU profile

- `/debug/pprof/heap` — memory profile

- `/debug/pprof/goroutine` — goroutine dump

---

## 🧠 CPU Profiling

Generate a CPU profile:

```text
curl http://localhost:6060/debug/pprof/profile?seconds=30 > cpu.prof
```

Analyze it with:

```text
go tool pprof cpu.prof
(pprof) top
(pprof) web
```

**`web` opens a flame graph (requires `Graphviz`) **

---

## 🧠 Memory Profiling

Generate a heap profile:

```text
curl http://localhost:6060/debug/pprof/heap > heap.prof
```

Look for high allocation counts and large retained objects.

**Use pprof -alloc_objects, -inuse_space to slice the data differently.**

---

## 🧵 Goroutines and Blocking

Dump goroutines:

```text
curl http://localhost:6060/debug/pprof/goroutine?debug=2
```

Find out if:

- Goroutines are leaking

- Something is blocking channels or mutexes

---

## ⚡ Execution Tracing

Go also supports full execution traces:

```go
import "runtime/trace"
```

Wrap your code:

```go
f, _ := os.Create("trace.out")
runtime/trace.Start(f)
defer trace.Stop()
```

Then run:

```text
go tool trace trace.out
```

**Use this to spot scheduling delays, GC pauses, network latency, etc.**

---

## 🧪 Benchmarking + Profiling

You can combine unit tests and profiling:

```go
func BenchmarkXxx(b *testing.B) {
    for i := 0; i < b.N; i++ {
        MyFunction()
    }
}
```

Run with profiling:

```text
go test -bench=. -cpuprofile=cpu.prof -memprofile=mem.prof
```

---

## 🛠️ Real-World Tips

- Profile in production with real workloads when possible

- Use flame graphs to spot hot loops and recursive calls

- Compare snapshots before and after changes

- Combine `pprof` with metrics (`Prometheus`, `Grafana`)

---

## 🧭 Summary

Profiling Go applications is straightforward but incredibly powerful:

- Use pprof for CPU, memory, and goroutines

- Use trace for low-level runtime behavior

- Benchmark with go test to validate changes

**Profile before you optimize — measure twice, cut once.**

---

🚀 Follow me on [norbix.dev](https://norbix.dev) for more insights on Go, system design, and engineering wisdom.
