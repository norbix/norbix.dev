+++
title = "Vanilla vs Frameworks in Software Engineering: Control, Speed, and Trade-offs"
date = "2026-03-26T20:00:00+02:00"
draft = false
tags = ["software-engineering", "frameworks", "architecture", "backend", "design"]
categories = ["software-engineering"]
summary = "Should you build software using frameworks or go vanilla? Explore trade-offs, real-world scenarios, and how experienced engineers make the right choice."
comments = true
ShowToc = true
TocOpen = true
image = "vanilla-vs-frameworks.jpg"
weight = 33
+++

![banner](banner.png)

**"Frameworks are tools — not architecture."**

That distinction is where most engineering decisions go wrong.

In modern software development, teams often default to frameworks without questioning whether they actually solve their problem — or introduce new ones.

This article breaks down the real trade-offs between **vanilla development** and **framework-driven development** — from the perspective of building real systems.

---

## 🧭 What Does "Vanilla" Mean?

In software engineering, **vanilla** means building with:

- Standard language features
- Minimal dependencies
- No heavy abstraction layers

Examples:

- Go HTTP server using `net/http`
- Python API using standard library + minimal routing
- Frontend using plain JavaScript (no React/Vue)

Vanilla doesn’t mean primitive.

➡️ It means **intentional simplicity and control**.

---

## ⚙️ What Are Frameworks?

Frameworks provide:

- Predefined structure
- Built-in patterns
- Convention over configuration

Examples:

- Backend: Django (Python), Spring Boot (Java), NestJS (Node.js), Gin/Echo/Fiber/Chi (Go, lightweight HTTP frameworks)
- Frontend: React, Angular, Vue
- Infrastructure: Serverless frameworks, ORMs

They accelerate development — but also constrain it.

---

## 💎 The Core Trade-off

At its core, this is a trade-off between:

| Aspect        | Vanilla                          | Frameworks                        |
|---------------|----------------------------------|----------------------------------|
| Control       | Full                             | Limited by framework             |
| Speed (start) | Slower                           | Faster                           |
| Flexibility   | High                             | Medium                           |
| Complexity    | Low (initially)                  | Hidden / abstracted              |
| Scaling       | Predictable                      | Can become restrictive           |

➡️ Vanilla optimizes for **control and clarity**  
➡️ Frameworks optimize for **speed and standardization**

---

## 🧠 Reality Check (From Real Systems)

In real-world backend and platform engineering:

- Frameworks help you **start fast**
- Vanilla helps you **stay in control**

From experience building APIs, async systems, and cloud services:

- Frameworks often introduce **implicit behavior**
- Debugging becomes harder at scale
- Performance tuning becomes constrained

➡️ The cost of abstraction shows up **later — not on day one**

---

## When Vanilla Wins

Vanilla shines when:

### You need full control

Example:
- Custom protocol
- Performance-critical system
- Low-level networking

### You’re building platform components

- Internal SDKs
- Infrastructure services
- Core APIs

These systems benefit from:

- Predictability
- Minimal magic
- Explicit design

### You want long-term maintainability

Less abstraction = easier reasoning

---

## When Frameworks Win

Frameworks are the right choice when:

### You need to move fast

- MVPs
- Startups validating ideas

### The problem is standard

- CRUD applications
- Admin panels
- Forms and dashboards

### Team onboarding matters

Frameworks provide:

- Familiar structure
- Shared conventions
- Faster ramp-up

---

## Vanilla in Action (Backend Example)

Let’s say you’re building a job processing API:

- POST /jobs → returns 202
- DynamoDB stores state
- S3 stores results
- Workers process async tasks

Vanilla approach:

1. Use Go `net/http` or minimal Python handler
2. Define explicit request/response contracts
3. Implement only what you need
4. Control every layer (serialization, retries, logging)
5. Integrate with AWS SDK directly

No hidden layers.

No magic.

➡️ Just clear, testable behavior.

---

## ⚙️ Framework Approach (Same System)

Using a framework:

1. Define models and controllers
2. Use ORM / abstraction layer
3. Plug into framework lifecycle
4. Use built-in validation and routing

Faster to start.

But:

- More layers
- Less visibility
- Harder to customize edge cases

---

## ⚠️ Where Frameworks Hurt

Frameworks become problematic when:

- ❌ You fight the framework instead of using it
- ❌ You need behavior it wasn’t designed for
- ❌ Performance becomes critical
- ❌ Debugging crosses multiple abstraction layers

At that point:

➡️ The framework stops being an accelerator  
➡️ And becomes a constraint

---

## ⚠️ Where Vanilla Hurts

Vanilla is not free from trade-offs:

- ❌ Slower initial development
- ❌ Requires stronger engineering discipline
- ❌ No built-in structure
- ❌ Reinventing common patterns

Without experience, vanilla can turn into:

➡️ inconsistent architecture  
➡️ fragmented codebases

---

## 🔄 Hybrid Approach (What Actually Works)

In practice, the best systems are hybrid:

- Use frameworks at the edges (UI, APIs)
- Use vanilla in the core (business logic, infra)

Example:

- FastAPI for HTTP layer
- Pure Python for domain logic
- AWS SDK directly (no heavy abstractions)

➡️ Frameworks handle **delivery**
➡️ Vanilla handles **core logic**

---

## 🛠️ Decision Framework

Ask these questions:

1. Is the problem standard or custom?
2. Do I need full control over behavior?
3. Will this system evolve significantly?
4. Is performance critical?
5. What is the team’s experience level?

If most answers point to control → go vanilla  
If speed and convention matter → use a framework

---

## 📌 Final Thoughts

This is not a religious debate.

It’s an engineering decision.

Frameworks are excellent tools — when used intentionally.

Vanilla is powerful — when used by experienced engineers.

The real skill is knowing:

➡️ when to abstract  
➡️ and when to stay close to the metal

Because in the end:

**Good engineers don’t follow tools. They choose them deliberately.**

---

🚀 Follow me on [norbix.dev](https://norbix.dev) for more insights on Go, Python, system design, and building real-world software.
