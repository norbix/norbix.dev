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
    func worker(id int, jobs <-chan int, results chan<- int) {
    
        for j := range jobs {
            fmt.Printf("Worker %d processing job %d\n", id, j)
            time.Sleep(time.Second)
            results <- j * 2
        }
    }
    ```

    ```go
    func main() {
    jobs := make(chan int, 5)
    results := make(chan int, 5)
    
        for w := 1; w <= 3; w++ {
            go worker(w, jobs, results)
        }
    
        for j := 1; j <= 5; j++ {
            jobs <- j
        }
        close(jobs)
    
        for a := 1; a <= 5; a++ {
            fmt.Println("Result:", <-results)
        }
    }
    ```

2. Worker Pool

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
	const numJobs = 5
	const numWorkers = 3

	jobs := make(chan int, numJobs)
	results := make(chan int, numJobs)
	var wg sync.WaitGroup

	// start workers
	for w := 1; w <= numWorkers; w++ {
		wg.Add(1)
		go worker(w, jobs, results, &wg)
	}

	// send jobs
	for j := 1; j <= numJobs; j++ {
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

🧠 Key Observations

- `numWorkers` controls parallelism (not number of jobs).

- Jobs are pushed into a channel → workers pull them at their own pace.

- `sync.WaitGroup` ensures all workers finish before closing results.

⚡ Variations in Production

- Dynamic Pools → adjust number of workers depending on load.

- Error Handling → use an errChan to collect errors from workers.

- Context-Aware Pools → cancel all workers if one fails or timeout occurs.

```go
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
```

📊 When to Use Worker Pools

✅ Best for:

- CPU-bound tasks (e.g., image processing).

- I/O-bound tasks (e.g., HTTP requests, DB queries).

- Batch jobs and pipelines.

❌ Not needed for:

- Small scripts.

- Lightweight goroutine fan-out without backpressure.

👉 Rule of Thumb:

Start with goroutines + channels. If you notice too many goroutines or unbounded resource use, switch to a worker pool.

3. Timeout with select

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

Use it to wait for all goroutines to finish.

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
