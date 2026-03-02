+++
date = '2025-04-19T15:52:47+02:00'
draft = false
title = 'Concurrency in Go'
tags = ["go", "golang", "concurrency", "goroutines", "channels"]
categories = ["backend", "golang"]
summary = "A deep dive into concurrency in Go, covering goroutines, channels, and real-world patterns."
comments = true
ShowToc = true
TocOpen = true
image = "banner.jpg"
weight = 8
+++

![banner](banner.jpg)

## 🧠 Concurrency in Go: Goroutines, Channels, and Patterns

Go was designed with concurrency as a first-class citizen. Unlike many other languages that bolt on concurrency, Go's model—centered around goroutines and channels—is simple, elegant, and incredibly powerful.

In this article, we’ll break down:

- What concurrency is in Go
- How goroutines and channels work
- Real-world concurrency patterns
- Code examples you can plug into your own projects

---

## 🚦 Concurrency vs. Parallelism

- Concurrency is about managing multiple tasks at once.
- Parallelism is about doing multiple tasks simultaneously.

Go lets you write concurrent code easily, and if your CPU allows, it can also run in parallel.

---

## 🌀 Goroutines

A goroutine is a lightweight thread managed by the Go runtime.

```go
package main

import (
	"fmt"
	"time"
)

func sayHello() {
	fmt.Println("Hello from goroutine!")
}

func main() {
	go sayHello() // runs concurrently
	time.Sleep(time.Second)
	fmt.Println("Main finished.")
}
```

go sayHello() starts the function in the background.

⚠️ Without time.Sleep, the main function may exit before the goroutine finishes.

---

## 📡 Unbuffered Channels

Channels allow goroutines to communicate safely.

Unbuffered channel are blocking, both send and receive are blocking operations.

```go
ch := make(chan string)

go func() {
	ch <- "ping"    // send
}()

msg := <-ch         // receive
fmt.Println(msg) // prints: ping

```

- `chan T` is a channel of type T
- `<-ch` receives
- `ch <-` sends

---

## 🔄 Buffered Channels

Buffered channels don’t block until full.

```go
ch := make(chan int, 2)

ch <- 1
ch <- 2
fmt.Println(<-ch)
fmt.Println(<-ch)
```

---

## ❌ Closing Channels

You can close a channel to indicate no more values will be sent.

This example does require close(ch) because of how range works with channels. This `for range` loop keeps receiving values from the channel until it’s closed.

```go
ch := make(chan int)
go func() {
	for i := 0; i < 3; i++ {
		ch <- i
	}
	close(ch)
}()

for val := range ch {
	fmt.Println(val)
}
```

---

## 🧱 Select Statement

`select` lets you wait on multiple channel operations.

```go
ch1 := make(chan string)
ch2 := make(chan string)

go func() {
	time.Sleep(1 * time.Second)
	ch1 <- "one"
}()

go func() {
	time.Sleep(2 * time.Second)
	ch2 <- "two"
}()

select {
case msg1 := <-ch1:
	fmt.Println("Received", msg1)
case msg2 := <-ch2:
	fmt.Println("Received", msg2)
}
```

---

## 🛠️ Concurrency Patterns

1. Fan-Out / Fan-In

    Fan-Out: Multiple goroutines read from the same channel.
    
    Fan-In: Multiple goroutines send into a single channel.

    ```go
    package main
   
    import (
        "fmt"
        "time"   
    )
    
    func worker(id int, jobs <-chan int, results chan<- int) {
        for j := range jobs {
            fmt.Printf("Worker %d processing job %d\n", id, j)
            time.Sleep(time.Second) // simulate work
	    	fmt.Printf("Worker %d finished job %d\n", id, j)
            results <- j * 2
        }
    }

    func main() {
        jobs := make(chan int, 5)
        results := make(chan int, 5)
	
        // Creates 3 goroutines, each running worker(...).
        for w := 1; w <= 3; w++ {
            go worker(w, jobs, results)
        }
    
        // The main function (itself a goroutine) then sends 5 jobs.
        for j := 1; j <= 5; j++ {
            jobs <- j
        }
        close(jobs)
    
        // Main goroutine waits for results
        // It receives 5 results — one for each job processed by the pool.
        for a := 1; a <= 5; a++ {
            fmt.Println("Result:", <-results)
        }
    }
    ```

   Example output (order may vary):

   ```text
   Worker 1 processing job 1
   Worker 2 processing job 2
   Worker 3 processing job 3
   Worker 1 processing job 4
   Worker 2 processing job 5
   Result: 2
   Result: 4
   Result: 6
   Result: 8
   Result: 10
   ```
   
   Order isn’t guaranteed — it depends on goroutine scheduling   

1. Worker Pool

   A worker pool is one of the most common and practical concurrency patterns in Go. It helps you:
   
   - Control concurrency → avoid spawning too many goroutines.
   
     - Reuse workers → instead of creating a goroutine per job.
   
     - Prevent resource exhaustion → e.g. database connections, network sockets.
   
   Think of it like a factory line: jobs come in, a fixed number of workers handle them, results are collected.
   
   Basic Worker Pool Example:

   ```go
   package main
   
   import (
       "fmt"
       "sync"
       "time"
   )
   
   func worker(id int, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) {
       defer wg.Done()
       for j := range jobs {
           fmt.Printf("Worker %d started job %d\n", id, j)
           time.Sleep(time.Second) // simulate work
           fmt.Printf("Worker %d finished job %d\n", id, j)
           results <- j * 2
       }
   }
   
   func main() {
       jobs := make(chan int, 5)
       results := make(chan int, 5)
       var wg sync.WaitGroup
   
       // start workers
       for w := 1; w <= 5; w++ {
           wg.Add(1)
           go worker(w, jobs, results, &wg)
       }
   
       // send jobs
       for j := 1; j <= 5; j++ {
           jobs <- j
       }
       close(jobs)
   
       // wait for workers to finish
       go func() {
           wg.Wait()
           close(results)
       }()
   
       // collect results
       for r := range results {
           fmt.Println("Result:", r)
       }
   }
   ```

   ### 🧠 Key Observations

   - `numWorkers` controls parallelism (not number of jobs).

   - Jobs are pushed into a channel → workers pull them at their own pace.

   - `sync.WaitGroup` ensures all workers finish before closing results.

   ### ⚡ Variations in Production

   - Dynamic Pools → adjust number of workers depending on load.

  - Error Handling → use an errChan to collect errors from workers.

  - Context-Aware Pools → cancel all workers if one fails or timeout occurs.

   ```go
   ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
   defer cancel()
   ```

   ### 📊 When to Use Worker Pools

   ✅ Best for:

   - CPU-bound tasks (e.g., image processing).
   
     - I/O-bound tasks (e.g., HTTP requests, DB queries).
   
     - Batch jobs and pipelines.

   ❌ Not needed for:

   - Small scripts.

     - Lightweight goroutine fan-out without backpressure.

   👉 Rule of Thumb:

   Start with goroutines + channels. If you notice too many goroutines or unbounded resource use, switch to a worker pool.

   ### 🔍 Key Differences Summary
   
   | Aspect | Without `WaitGroup` | With `WaitGroup` |
   |--------|---------------------|------------------|
   | **Knowing how many results to read** | Must know exact count (`for i := 1; i <= N`) | No need — `for range` until closed |
   | **Who closes `results`** | Nobody (left open) | A goroutine after all workers finish |
   | **When program ends** | Possibly before all workers finish | Guaranteed after all workers finish |
   | **Synchronization** | Implicit (via job count) | Explicit (via `wg.Wait()`) |
   | **Safety in large systems** | Not safe for unknown job counts | Safe and scalable |

1. Advanced WorkerPool Implementation

    The previous examples show the concept clearly.
    Now let’s look at a more structured, reusable implementation — something you could actually use inside a backend service.
    
    This version:
    
    - Is thread-safe
    
    - Prevents starting twice
    
    - Returns only non-nil errors

    - Enforces pool size at creation
    
    - Ensures tasks cannot be added before starting
    
    - Encapsulates internal channels

    ```go
    package task
    
    import (
        "errors"
        "sync"
    )
    
    // WorkerPool errors, do not change!
    var (
        ErrBadParams  = errors.New("bad params")
        ErrBadTask    = errors.New("bad task")
        ErrNotStarted = errors.New("not started")
    )
    
    // Task to be computed by the WorkerPool.
    type Task func() error
    
    // WorkerPool represents a pool of goroutines.
    type WorkerPool struct {
        size    int
        tasks   chan Task
        results chan error
    
        started bool
        mu      sync.Mutex
    }
    
    // NewWorkerPool creates a new pool with a given size.
    func NewWorkerPool(size int) (*WorkerPool, error) {
        if size <= 0 {
            return nil, ErrBadParams
        }
    
        wp := &WorkerPool{
            size:    size,
            tasks:   make(chan Task),
            results: make(chan error, size),
        }
    
        return wp, nil
    }
    
    // Results returns channel of non-nil errors.
    func (wp *WorkerPool) Results() <-chan error {
        return wp.results
    }
    
    // Run will start workers (goroutines) for tasks computation.
    func (wp *WorkerPool) Run() {
        wp.mu.Lock()
        defer wp.mu.Unlock()
    
        if wp.started {
            return
        }
    
        wp.started = true
    
        for i := 0; i < wp.size; i++ {
            go func() {
                for task := range wp.tasks {
                    if task == nil {
                        continue
                    }
    
                    if err := task(); err != nil {
                        wp.results <- err
                    }
                }
            }()
        }
    }
    
    // AddTask will add a task to the worker pool queue.
    func (wp *WorkerPool) AddTask(task Task) error {
        if task == nil {
            return ErrBadTask
        }
    
        wp.mu.Lock()
        defer wp.mu.Unlock()
    
        if !wp.started {
            return ErrNotStarted
        }
    
        wp.tasks <- task
        return nil
    }
    ```

    # 🔬 Why This Version Is “Advanced”
    
    Compared to the basic example:
    
    |Feature	| Basic Example	| Advanced Version |
    | --- | --- | --- |
    | Encapsulation	| Inline in `main` | Reusable struct |
    | Thread-safety	| Minimal	| Mutex protected |
    | Lifecycle control	| Implicit	| Explicit `Run()` |
    | Error channel	| Optional	| Built-in |
    | Validation	| None	| Strict checks |
    | Production ready	| Demo	| Yes |

    # 🧠 Architectural Insight

    This design introduces an important production principle:

        **Control concurrency explicitly. Never let goroutines grow unbounded.**

    In real backend systems (like API servers, message consumers, or background processors):

        - You must limit DB connections

        - You must limit HTTP calls

        -- You must avoid spawning 100k goroutines

    This pool guarantees:
    
    ```text
    max concurrency = pool size
    ```

    That’s deterministic concurrency — a huge advantage in distributed systems.

    # 🧩 Where This Pattern Shines

    This implementation is ideal for:

        - Database batch processing

        - Controlled API fan-out

        - Message queue consumers

        - File processing pipelines

        - CPU-bound workers

        - Rate-limited external integrations

## ⏱️ Timeout with `select`

In Go, you can use the `select` statement with `time.After` to implement timeouts for channel operations.  
This prevents your goroutine from blocking forever if no data arrives within a given duration.

 ```go
 c := make(chan string)
 
 go func() {
     time.Sleep(2 * time.Second)
     c <- "done"
 }()
 
 select {
 case res := <-c:
     fmt.Println(res)
 case <-time.After(1 * time.Second):
     fmt.Println("timeout")
 }
 ```

---

## ⚖️ sync.WaitGroup

Use it to wait for all goroutines to finish before continuing execution.  
A `WaitGroup` provides a simple way to coordinate concurrent tasks and ensure they complete before your program exits.

```go
var wg sync.WaitGroup

for i := 0; i < 3; i++ {
	wg.Add(1)
	go func(id int) {
		defer wg.Done()
		fmt.Printf("Worker %d done\n", id)
	}(i)
}

wg.Wait()
fmt.Println("All workers finished.")
```

---

## 🧠 Final Thoughts

Go makes concurrency not only powerful—but approachable. You don't need threads or semaphores to build safe, concurrent systems.
✅ Key Takeaways:

- Use goroutines for lightweight concurrency.
- Use channels for safe communication.
- Master select, worker pools, and timeouts for production-grade patterns.

---

🚀 Follow me on [norbix.dev](https://norbix.dev) for more insights on Go, Python, AI, system design, and engineering wisdom.
