+++
date = '2025-04-08T19:10:10+02:00'
draft = false
title = "Best Practices for Software Development in Go"
tags = ["go", "golang", "best-practices", "software-engineering"]
categories = ["backend", "golang"]
summary = "A collection of real-world Go best practices from years of building backend systems, APIs, and cloud-native services."
comments = true
ShowToc = true
TocOpen = true
image = "banner.jpg"
weight = 1
+++

> Writing Go code that works is easy. Writing Go code that lasts? That takes practice.

After working on production systems in Go for several years — across SaaS platforms, cloud-native backends, and developer tooling — I’ve collected a set of battle-tested best practices that have helped me write maintainable, clean, and scalable Go code.

![banner](banner.jpg)

---

## 🧭 0. Agree on Code Style Before You Write a Line

Before starting any development, align on a shared code style with your team.

This prevents unnecessary friction during code reviews, ensures consistency, and reduces the mental overhead of switching between files written by different developers.

A great starting point is the **[Google Go Style Guide](https://google.github.io/styleguide/go/)** — it's clear, opinionated, and battle-tested at scale. You can automate style enforcement with:

- `gofmt` / `goimports` for formatting
- `golangci-lint` to enforce idiomatic Go practices

Establishing your code style early also makes onboarding faster and simplifies collaboration — especially in cross-functional teams or open source projects.

---

## ✅ 1. Keep it Simple

Go is intentionally minimal — embrace it.

- Avoid over-engineering.
- Prefer composition over inheritance.
- Use plain interfaces and simple data structures.
- Don’t abstract too early — write the concrete code first.

### 🔑 1.1 Keys in a Map

Go maps are incredibly powerful, but not all types can be used as keys.

Allowed as keys ✅:

- `string`, `int`, `bool`, `float64` (comparable primitives)

- Structs and arrays (if all their fields/elements are comparable)

Not allowed ❌:

- `slices`, `maps`, `functions` (they’re not comparable)

Example:

```go
m := map[string]int{
    "alice": 1,
    "bob":   2,
}

fmt.Println(m["alice"]) // 1
```

If you try to use a slice as a key:

```go
bad := map[[]int]string{} // ❌ compile error
```

Another important property: map iteration order is random.

Never rely on a fixed order when looping:

```go
for k, v := range m {
    fmt.Println(k, v) // order is not guaranteed
}
```

#### ✅ Best practices:

- Use maps for lookups, not ordered data.

- If you need order, collect keys into a slice and sort

    ```go
    keys := make([]string, 0, len(m))
    for k := range m {
        keys = append(keys, k)
    }
    sort.Strings(keys)
    
    for _, k := range keys {
        fmt.Println(k, m[k])
    }
    ```

---

## 🧱 2. Project Structure Matters

Use a predictable layout:

```text
/cmd - entry points 
/internal - private packages 
/pkg - public, reusable packages 
/api - OpenAPI/proto definitions 
/config - config loading 
/scripts - helper scripts
```


Stick to convention. Tools like [`golang-standards/project-layout`](https://github.com/golang-standards/project-layout) are a great starting point — but adapt it to your team’s needs.

---

## 🧪 3. Tests Are Not Optional

- Use table-driven tests
- Use [`testing`](https://pkg.go.dev/testing), and only bring in libraries like `testify` if you really need them
- Keep unit tests fast and independent
- Use `go test -cover` to check coverage

---

## ✨ 4. Errors Are First-Class Citizens

- Always check errors — no exceptions.
- Wrap errors with context using `fmt.Errorf("failed to read config: %w", err)`
- For complex systems, consider using `errors.Join` or `errors.Is/As` for proper error handling.

---

## 📦 5. Use Interfaces at the Boundaries

Keep interfaces small, and only expose them where needed:

```go
type Storer interface {
    Save(ctx context.Context, data Item) error
}
```

Don’t write interfaces for everything — only where mocking or substitution matters (e.g. storage, HTTP clients, etc.).

### 🔗 5.1 Interface Embedding (Composing Behaviors)

In Go, it’s common to see interfaces inside other interfaces — this is called interface embedding.

Example from the standard library:

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type ReadWriter interface {
    Reader
    Writer
}
```

Instead of repeating method signatures, Go lets you compose small interfaces into bigger ones.

Why it matters:

- Encourages small, focused interfaces (e.g. io.Reader, io.Writer)

- Avoids “fat interfaces” that are harder to mock/test

- Makes code more reusable and flexible

Example in practice (net.Conn):

```go
type Conn interface {
    Reader
    Writer
    Closer
}
```

Any type that implements Read, Write, and Close automatically satisfies Conn.

**✅ This pattern keeps Go code clean, DRY, and testable.**

### 🔍 5.2 Type Assertions

When working with interfaces, you often need to access the concrete type stored inside.

Type assertion syntax:

```go
value, ok := i.(T)
```

- `i` → the interface value

- `T` → the type you expect

- `ok` → boolean (true if successful, false if not)

Example:

```go
var x interface{} = "hello"

s, ok := x.(string)
if ok {
    fmt.Println("string value:", s)
}
```

**⚠️ Without ok, a failed assertion will panic:**

```go
i := interface{}(42)
s := i.(string) // panic: interface {} is int, not string
```

✅ Common Use Case: Generic Maps

```go
data := map[string]interface{}{
    "id":   123,
    "name": "Alice",
}

id := data["id"].(int)
name := data["name"].(string)
```

🔄 Type Switch

```go
switch v := i.(type) {
case string:
    fmt.Println("string:", v)
case int:
    fmt.Println("int:", v)
default:
    fmt.Println("unknown type")
}
```

#### Best Practices:

- Prefer narrow interfaces (avoid interface{} unless really needed).

- Always use the ok idiom unless you are 100% sure of the type.

- Use type switches for clean multi-branch logic.

---

## 🧰 6. Tooling Makes You Better

- Use go vet, staticcheck, and golangci-lint
- Automate formatting: gofmt, goimports
- Use go mod tidy to keep your dependencies clean
- Pin tool versions with a `tools.go` file
- 📊 Use **SonarQube** for static code analysis at scale

SonarQube helps enforce code quality and security standards across large codebases. It can detect bugs, vulnerabilities, code smells, and even provide actionable remediation guidance. Integrate it into your CI pipeline to ensure every PR gets automatically analyzed.

You can use [`sonar-scanner`](https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/) or a Docker-based runner like:

```text
```bash
docker run --rm \
  -e SONAR_HOST_URL="https://your-sonarqube-url" \
  -e SONAR_LOGIN="your_token" \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli
```

SonarQube works great alongside golangci-lint, giving you both quick feedback locally and deep insights via the web dashboard.

---

## 🔐 7. Secure By Default

- Always set timeouts on HTTP clients and servers
- Avoid leaking secrets in logs
- Validate all inputs — especially on the API boundary
- Use context.Context consistently and propagate it properly

---

## 🌐 8. Embrace the Go Ecosystem

- Use standard library wherever possible — it's well-tested and fast
- Prefer established, well-maintained packages
- Read source code — Go makes it easy to learn from the best

---

## 🚀 9. Performance Matters (but correctness first)

- Profile with `pprof`
- Avoid allocations in tight loops
- Use channels, but don’t abuse goroutines
- Benchmark with go test -bench

### 9.1 Cache vs Memoization

These two terms are often confused, but they solve slightly different problems:

| Concept       | Definition                                                                 | Example in Go                                         | Best For                                |
|---------------|-----------------------------------------------------------------------------|-------------------------------------------------------|-----------------------------------------|
| **Cache**     | General-purpose store that saves results for reuse, often across requests   | `map[string][]byte` holding responses from an API     | Web servers, database queries, heavy I/O |
| **Memoization** | Caching applied to a function call — same inputs, same output            | Store Fibonacci results in a local map inside a func  | Pure functions, recursive computations   |

Example: Memoizing Fibonacci

```go
var memo = map[int]int{}

func fib(n int) int {
    if n <= 1 {
        return n
    }
    if v, ok := memo[n]; ok {
        return v
    }
    res := fib(n-1) + fib(n-2)
    memo[n] = res
    return res
}
```

#### Key differences:

- Cache can be global, cross-service, even distributed (e.g., Redis).

- Memoization is function-scoped, purely about optimization of repeated calls with identical input.

#### ⚖️ Comparison

| Feature   | Cache                                   | Memoization                          |
|-----------|-----------------------------------------|---------------------------------------|
| **Scope** | System-wide (data, responses, etc)      | Function-local (results of calls)     |
| **Key**   | Anything (URLs, queries, objects)       | Function arguments                    |
| **Policy**| TTL, eviction (LRU, LFU, etc.)          | None (grows with unique inputs)       |
| **Use Cases** | DB queries, API responses, assets   | Fibonacci, factorial, DP problems     |


#### 👉 Rule of thumb:

- Use memoization when optimizing pure functions.

- Use a cache when optimizing data retrieval/storage across systems or layers.


#### ✅ Best Practice: 

- Use memoization for pure CPU-bound functions,

- Use cache for I/O-heavy or cross-request data.

---

## 🧠 10. Readability > Cleverness

Your code will be read 10x more than it’s written.

    "Write code for humans, not machines."

Stick to idiomatic Go — use golangci-lint to enforce consistency, and always code with your teammates in mind.

---

## 🙌 Conclusion

Go is an incredible tool for building fast, reliable software — but like any tool, it shines brightest in the hands of developers who respect its philosophy: clarity, simplicity, and composability.

What are your favorite Go best practices? Let me know on [Twitter](https://x.com/norbixjakubczak) or GitHub [@norbix](https://github.com/norbix)!

---

🚀 Follow me on [norbix.dev](https://norbix.dev) for more insights on Go, Python, AI, system design, and engineering wisdom.
