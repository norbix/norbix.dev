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

## 📡 Channels

Channels allow goroutines to communicate safely.

```go
ch := make(chan string)

go func() {
	ch <- "ping"
}()

msg := <-ch
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

You can create a pool of workers that handle jobs concurrently with limited resources.

✅ Use buffered channels and `sync.WaitGroup` for coordination.


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
