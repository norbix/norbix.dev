+++
date = '2025-04-08T19:10:10+02:00'
draft = false
title = "Best Practices for Software Development in Go"
tags = ["go", "golang", "best-practices", "software-engineering"]
categories = ["backend", "golang"]
summary = "A collection of real-world Go best practices from years of building backend systems, APIs, and cloud-native services."
comments = true
+++

> Writing Go code that works is easy. Writing Go code that lasts? That takes practice.

After working on production systems in Go for several years — across SaaS platforms, cloud-native backends, and developer tooling — I’ve collected a set of battle-tested best practices that have helped me write maintainable, clean, and scalable Go code.

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

## 🧰 6. Tooling Makes You Better

- Use go vet, staticcheck, and golangci-lint
- Automate formatting: gofmt, goimports
- Use go mod tidy to keep your dependencies clean
- Pin tool versions with a tools.go file

## 🔐 7. Secure By Default

- Always set timeouts on HTTP clients and servers
- Avoid leaking secrets in logs
- Validate all inputs — especially on the API boundary
- Use context.Context consistently and propagate it properly

## 🌐 8. Embrace the Go Ecosystem

- Use standard library wherever possible — it's well-tested and fast
- Prefer established, well-maintained packages
- Read source code — Go makes it easy to learn from the best

## 🚀 9. Performance Matters (but correctness first)

- Profile with `pprof`
- Avoid allocations in tight loops
- Use channels, but don’t abuse goroutines
- Benchmark with go test -bench


## 🧠 10. Readability > Cleverness

Your code will be read 10x more than it’s written.

    "Write code for humans, not machines."

Stick to idiomatic Go — use golangci-lint to enforce consistency, and always code with your teammates in mind.


## 🙌 Conclusion

Go is an incredible tool for building fast, reliable software — but like any tool, it shines brightest in the hands of developers who respect its philosophy: clarity, simplicity, and composability.

What are your favorite Go best practices? Let me know on [Twitter](https://x.com/norbixjakubczak) or GitHub [@norbix](https://github.com/norbix)!
