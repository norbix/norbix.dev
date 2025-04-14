+++
title = "Breaking the Chain: Dependency Inversion, Interfaces, and Testable Go Code"
date = "2025-04-14T18:00:00+02:00"
draft = false
tags = ["go", "solid", "dependency-injection", "unit-testing", "interfaces"]
categories = ["software-engineering", "golang"]
summary = "A deep dive into the Dependency Inversion Principle, its implementation with interfaces and dependency injection, and how it unlocks clean, testable Go code."
comments = true
+++

"High-level modules should not depend on low-level modules. Both should depend on abstractions."

Welcome to a core principle of software architecture: Dependency Inversion, the "D" in `SOLID`. In this article, we’ll explore what it means in practice, how to implement it in Go using interfaces and dependency injection, and why it’s essential for writing unit-testable code.

![banner](banner.png)

# Table of Contents
- [What Is the Dependency Inversion Principle?](#what-is-the-dependency-inversion-principle)
- [Refactor with Dependency Inversion](#refactor-with-dependency-inversion)
- [Enter Dependency Injection](#enter-dependency-injection)
- [Why This Rocks for Testing](#why-this-rocks-for-testing)
- [Summary](#summary)
- [When to Use DIP in Go](#when-to-use-dip-in-go)

---

## 🧠 What Is the Dependency Inversion Principle?

The Dependency Inversion Principle (DIP) flips the traditional dependency model:

- ❌ Traditional: High-level business logic depends directly on low-level implementation (e.g., a database).

- ✅ DIP: Both layers depend on abstractions — usually in the form of interfaces.

It’s about reversing the direction of dependency to reduce coupling and improve flexibility.

---

## 💡 A Quick Example: Tightly Coupled Code

```go
type OrderService struct {
    db *sql.DB
}

func (o *OrderService) Save(order Order) error {
    _, err := o.db.Exec("INSERT INTO orders ...")
    return err
}
```

This code:

- Tightly couples OrderService to a concrete *sql.DB

- Is hard to test in isolation

---

## ✅ Refactor with Dependency Inversion

Let’s invert the dependency:

```go
type OrderRepository interface {
    Save(order Order) error
}

type OrderService struct {
    repo OrderRepository
}

func (o *OrderService) Save(order Order) error {
    return o.repo.Save(order)
}
```

Now:

- OrderService depends on an interface

- OrderRepository can be backed by a real DB in prod or a mock in tests

---

## 🛠️ Enter Dependency Injection

We’ve inverted dependencies — now we need a way to supply them.
Manual constructor injection in Go:

```go
func NewOrderService(repo OrderRepository) *OrderService {
    return &OrderService{repo: repo}
}
```

At runtime, inject the actual implementation:

```go
service := NewOrderService(NewPostgresOrderRepository(db))
```

---

## 🧪 Why This Rocks for Testing

DIP + interfaces = test-friendly code.

```go
type MockOrderRepository struct {
    SavedOrder Order
}

func (m *MockOrderRepository) Save(order Order) error {
    m.SavedOrder = order
    return nil
}

func TestOrderService_Save(t *testing.T) {
    mock := &MockOrderRepository{}
    service := NewOrderService(mock)

    order := Order{ID: 42}
    err := service.Save(order)

    require.NoError(t, err)
    require.Equal(t, 42, mock.SavedOrder.ID)
}
```

**You’ve isolated business logic from infrastructure — the holy grail of testability.**

---

## 🔄 Summary

- DIP inverts traditional dependency direction: high-level modules depend on interfaces, not implementations.

- Interfaces define contracts at the boundaries.

- Dependency Injection supplies those interfaces at runtime.

- Unit Testing becomes effortless when your logic isn’t tangled up in database, network, or file system concerns.

---

## 🧭 When to Use DIP in Go

- ✅ When abstracting IO, storage, APIs, or 3rd party integrations

- ✅ When writing business logic you want to test independently

- ❌ Not needed for everything — Go prefers concrete, simple code unless you need indirection
