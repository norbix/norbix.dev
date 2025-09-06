+++
date = '2025-09-06T12:00:00+02:00'
draft = false
title = 'Architectural Patterns in Go: MVC, Hexagonal, CQRS, and Microservices'
tags = ['go', 'golang', 'architecture', 'mvc', 'hexagonal', 'cqrs', 'microservices']
categories = ['Programming', 'Architecture']
summary = 'Understand the difference between design patterns and architectural patterns. Explore how MVC, Hexagonal, CQRS, and Microservices can be applied in Go projects with practical insights and examples.'
comments = true
ShowToc = true
TocOpen = true
image = 'architecture-banner.jpg'
weight = 21
+++

**Design patterns** (like Singleton, Factory, Strategy) are reusable solutions to small-scale design problems.

**Architectural patterns**, on the other hand, define the **big picture** of how systems are structured, how components interact, and how responsibilities are separated.

In this article, we’ll explore four influential architectural patterns — **MVC**, **Hexagonal**, **CQRS**, and **Microservices** — and see how they apply to Go development.

<div style="display: flex; justify-content: center;">
  <img src="banner.jpg" alt="Architectural Patterns in Go" style="max-width: 100%; height: auto;" />
</div>

---

## 🖼 MVC (Model–View–Controller)

The **MVC pattern** splits an application into three roles:

- **Model** → data and business logic
- **View** → presentation layer (UI, HTML templates, JSON responses)
- **Controller** → handles input and orchestrates between Model and View

### Goal: keep responsibilities crisp.

- Model (Domain): business entities + rules (no framework details).

- View: JSON/HTML returned to the client.

- Controller: HTTP entrypoint; validates input, calls services, shapes output.

- DTO (Data Transfer Object): API-facing structs (request/response). Shields the domain from external shape changes.

- DAO/Repository: persistence port; hides database from the domain. (DAO is essentially a repository here.)

### Why DTO + DAO with MVC?

- DTOs prevent leaking internal domain fields (e.g., hashed passwords, internal IDs) and stabilize your public API.

- DAO/Repository makes business logic testable (swap Postgres for in-memory in tests) and keeps SQL out of controllers.

### Suggested backend layout (Go)

- Domain has zero dependency on infra (DB/HTTP).

- Services orchestrate use cases.

- Controllers adapt HTTP ↔️ services and map DTO ↔️ Model.

```text
.
├─ cmd/
│  └─ server/
│     └─ main.go                  # wire HTTP router, DI, config
├─ internal/
│  ├─ app/
│  │  ├─ http/
│  │  │  └─ controllers/          # controllers (handlers) — “C”
│  │  └─ services/                # application/services layer (use cases)
│  ├─ domain/
│  │  └─ user/                    # domain models & interfaces — “M”
│  │     ├─ model.go
│  │     ├─ repository.go         # DAO (port)
│  │     └─ errors.go
│  ├─ infra/
│  │  ├─ db/                      # db bootstrapping (sqlx/gorm/pgx)
│  │  └─ repository/              # DAO impls (adapters) — Postgres/MySQL
│  │     └─ user_pg.go
│  └─ transport/
│     └─ http/
│        ├─ router.go             # gin/chi mux + routes
│        └─ dto/                  # DTOs — request/response
│           └─ user.go
├─ pkg/
│  ├─ logger/
│  └─ validator/
└─ go.mod
```

### MVC Diagram.

```mermaid
flowchart LR
    subgraph Client["Client (Frontend/UI)"]
        A["HTTP Request\nJSON Payload"]
    end

    subgraph Transport["Transport Layer"]
        B["Controller\nGin/Chi Handler"]
        C["DTO\nRequest/Response"]
    end

    subgraph App["Application Layer"]
        D["Service\nBusiness Use Case"]
    end

    subgraph Domain["Domain Layer"]
        E["Domain Model\nEntities & Rules"]
        F["Repository Interface\n(DAO Port)"]
    end

    subgraph Infra["Infrastructure Layer"]
        G["Repository Impl\nPostgres Adapter"]
        H[("Database\nPostgres")]
    end

    A -->|HTTP JSON| B
    B -->|Map to DTO| C
    C -->|Pass Valid Data| D
    D -->|Use Entities| E
    D -->|Call Port| F
    F -->|Implemented by| G
    G -->|SQL Queries| H
    H -->|Result Rows| G
    G -->|Return Entities| F
    F -->|Back to| D
    D -->|Domain → DTO| C
    C -->|JSON Response| B
    B -->|HTTP Response| A
```

### 🧩 Domain Model (M)

File: `internal/domain/user/model.go`

```go
package user

import "time"

type ID string

type User struct {
	ID        ID
	Name      string
	Email     string
	Active    bool
	CreatedAt time.Time
}

// Domain invariants/constructors keep the model valid.
func New(name, email string) (User, error) {
	if name == "" {
		return User{}, ErrInvalidName
	}
	if !isValidEmail(email) {
		return User{}, ErrInvalidEmail
	}
	return User{
		ID:     ID(NewID()),
		Name:   name,
		Email:  email,
		Active: true,
		// CreatedAt set in service or repo
	}, nil
}
```

File: `internal/domain/user/repository.go (DAO Port)`

```go
package user

import "context"

type Repository interface {
	Create(ctx context.Context, u User) error
	ByID(ctx context.Context, id ID) (User, error)
	ByEmail(ctx context.Context, email string) (User, error)
	List(ctx context.Context, limit, offset int) ([]User, error)
	Update(ctx context.Context, u User) error
	Delete(ctx context.Context, id ID) error
}
```

### 🧰 DAO Implementation (Adapter)

File: `internal/infra/repository/user_pg.go`

```go
package repository

import (
	"context"
	"database/sql"
	"errors"
	"time"

	domain "yourapp/internal/domain/user"
)

type UserPG struct {
	db *sql.DB
}

func NewUserPG(db *sql.DB) *UserPG { return &UserPG{db: db} }

func (r *UserPG) Create(ctx context.Context, u domain.User) error {
	_, err := r.db.ExecContext(ctx,
		`INSERT INTO users (id, name, email, active, created_at)
         VALUES ($1,$2,$3,$4,$5)`,
		u.ID, u.Name, u.Email, u.Active, time.Now().UTC(),
	)
	return err
}

func (r *UserPG) ByID(ctx context.Context, id domain.ID) (domain.User, error) {
	row := r.db.QueryRowContext(ctx,
		`SELECT id, name, email, active, created_at FROM users WHERE id=$1`, id)
	var u domain.User
	if err := row.Scan(&u.ID, &u.Name, &u.Email, &u.Active, &u.CreatedAt); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return domain.User{}, domain.ErrNotFound
		}
		return domain.User{}, err
	}
	return u, nil
}

// ... ByEmail, List, Update, Delete similarly
```

### 🧠 Application Service (Use Case Layer)

- Services speak domain and depend on ports (interfaces).

- They’re trivial to unit-test with a fake repository.

File: `internal/app/services/user_service.go`

```go
package services

import (
	"context"
	"time"

	domain "yourapp/internal/domain/user"
)

type UserService struct {
	repo domain.Repository
}

func NewUserService(repo domain.Repository) *UserService {
	return &UserService{repo: repo}
}

func (s *UserService) Register(ctx context.Context, name, email string) (domain.User, error) {
	u, err := domain.New(name, email)
	if err != nil {
		return domain.User{}, err
	}
	// set creation time here if not in repo
	u.CreatedAt = time.Now().UTC()
	if err := s.repo.Create(ctx, u); err != nil {
		return domain.User{}, err
	}
	return u, nil
}

func (s *UserService) Get(ctx context.Context, id domain.ID) (domain.User, error) {
	return s.repo.ByID(ctx, id)
}
```

###  📦 DTOs (Requests/Responses)

- Keep validation on DTOs (with validator).

- Mapping functions isolate domain ↔️ transport conversion.

File: `internal/transport/http/dto/user.go`

```go
package dto

import (
	domain "yourapp/internal/domain/user"
)

type CreateUserRequest struct {
	Name  string `json:"name" validate:"required,min=2"`
	Email string `json:"email" validate:"required,email"`
}

type UserResponse struct {
	ID     string `json:"id"`
	Name   string `json:"name"`
	Email  string `json:"email"`
	Active bool   `json:"active"`
}

func ToUserResponse(u domain.User) UserResponse {
	return UserResponse{
		ID:     string(u.ID),
		Name:   u.Name,
		Email:  u.Email,
		Active: u.Active,
	}
}
```

### 🎮 Controller (C) — HTTP Handlers

File: `internal/app/http/controllers/user_controller.go`

```go
package controllers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"yourapp/internal/app/services"
	"yourapp/internal/transport/http/dto"
	domain "yourapp/internal/domain/user"
)

type UserController struct {
	svc *services.UserService
}

func NewUserController(svc *services.UserService) *UserController {
	return &UserController{svc: svc}
}

func (uc *UserController) Register(c *gin.Context) {
	var req dto.CreateUserRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid_payload"})
		return
	}
	// optional: validate req with pkg/validator

	user, err := uc.svc.Register(c.Request.Context(), req.Name, req.Email)
	if err != nil {
		switch err {
		case domain.ErrInvalidEmail, domain.ErrInvalidName:
			c.JSON(http.StatusUnprocessableEntity, gin.H{"error": err.Error()})
		default:
			c.JSON(http.StatusInternalServerError, gin.H{"error": "internal_error"})
		}
		return
	}
	c.JSON(http.StatusCreated, dto.ToUserResponse(user))
}

func (uc *UserController) Get(c *gin.Context) {
	id := domain.ID(c.Param("id"))
	user, err := uc.svc.Get(c.Request.Context(), id)
	if err != nil {
		if err == domain.ErrNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "not_found"})
			return
		}
		c.JSON(http.StatusInternalServerError, gin.H{"error": "internal_error"})
		return
	}
	c.JSON(http.StatusOK, dto.ToUserResponse(user))
}
```

File: `internal/transport/http/router.go`

```go
package http

import (
	"github.com/gin-gonic/gin"
	"yourapp/internal/app/http/controllers"
)

func NewRouter(userCtrl *controllers.UserController) *gin.Engine {
	r := gin.New()
	r.Use(gin.Recovery())

	v1 := r.Group("/v1")
	{
		v1.POST("/users", userCtrl.Register)
		v1.GET("/users/:id", userCtrl.Get)
	}
	return r
}
```

### 🚀 Wiring (main)

File: `cmd/server/main.go`

```go
package main

import (
	"database/sql"
	"log"
	"net/http"

	_ "github.com/lib/pq"

	"yourapp/internal/app/http/controllers"
	"yourapp/internal/app/services"
	"yourapp/internal/infra/repository"
	transport "yourapp/internal/transport/http"
)

func main() {
	db, err := sql.Open("postgres", "postgres://user:pass@localhost:5432/app?sslmode=disable")
	if err != nil { log.Fatal(err) }

	userRepo := repository.NewUserPG(db)          // DAO impl
	userSvc  := services.NewUserService(userRepo) // Service
	userCtrl := controllers.NewUserController(userSvc)

	router := transport.NewRouter(userCtrl)
	log.Println("listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", router))
}
```

### ✅ Checklist & Tips

- Controller: tiny; only HTTP + mapping + error codes.

- DTO: versioned (e.g., /v1), validated, stable to external changes.

- Service: business orchestration; no HTTP/SQL.

- Domain: invariants, pure logic; no frameworks.

- DAO/Repository: concrete DB code; easily mocked.

- Testing: unit test services with in-memory repo; integration test DAO with a test DB.

- Errors: map domain errors to HTTP status codes in controllers.

- Versioning: keep DTOs under transport/http/dto/v1 if you plan multiple API versions.

### ✅ When to use:

- Web applications with clear input/output flows

- Great for monolithic Go services

- ⚠️ Pitfall: Controllers can easily become “fat” if not managed well.

---

## 🛡 Hexagonal Architecture (Ports & Adapters)

Idea: keep your domain core pure and push frameworks, DBs, and transports to the edges.

- Domain (core): entities, value objects, domain services, errors.

- Ports: interfaces the core depends on (e.g., UserRepository, Mailer).

- Adapters: implementations for ports (Postgres, Redis, SMTP, HTTP clients).

- Drivers: incoming adapters (HTTP/gRPC/CLI/Jobs) that call the core.

Suggested layout (Go)

```text
.
├─ cmd/api/                         # app entrypoint(s)
│  └─ main.go
├─ internal/
│  ├─ domain/                       # PURE core (no imports of gin/sql/http)
│  │  └─ user/
│  │     ├─ entity.go               # entities/value objects
│  │     ├─ service.go              # domain services (pure)
│  │     ├─ ports.go                # ports (interfaces) e.g., UserRepo, Mailer
│  │     └─ errors.go
│  ├─ app/                          # use-cases/application services
│  │  └─ user/
│  │     └─ usecase.go              # RegisterUser, ActivateUser, etc.
│  ├─ adapters/
│  │  ├─ in/                        # driving adapters
│  │  │  └─ http/                   # HTTP handlers (gin/chi)
│  │  │     ├─ router.go
│  │  │     └─ user_controller.go
│  │  └─ out/                       # driven adapters
│  │     ├─ postgres/
│  │     │  └─ user_repo.go         # implements domain.UserRepository
│  │     └─ mail/
│  │        └─ smtp_mailer.go       # implements domain.Mailer
│  └─ platform/                     # cross-cutting infra (db, config, log)
│     ├─ db.go
│     ├─ config.go
│     └─ logger.go
└─ go.mod
```

### Minimal Go example

File: `internal/domain/user/ports.go`

```go
package user

import "context"

type Repository interface {
	Save(ctx context.Context, u User) error
	ByID(ctx context.Context, id ID) (User, error)
}

type Mailer interface {
	SendWelcome(ctx context.Context, email string) error
}
```

File: `internal/app/user/usecase.go`

```go
package userapp

import (
	"context"

	domain "yourapp/internal/domain/user"
)

type RegisterUser struct {
	Repo   domain.Repository
	Mailer domain.Mailer
}

func (uc RegisterUser) Do(ctx context.Context, name, email string) (domain.User, error) {
	u, err := domain.New(name, email)
	if err != nil {
		return domain.User{}, err
	}
	if err := uc.Repo.Save(ctx, u); err != nil {
		return domain.User{}, err
	}
	_ = uc.Mailer.SendWelcome(ctx, u.Email) // best-effort, log on failure
	return u, nil
}
```

### Hexagonal Diagram

```mermaid
flowchart LR
    subgraph Drivers["Drivers (Incoming Adapters)"]
        A["HTTP\n(gin/chi)"]
        B["CLI\nCron/Jobs"]
        C["gRPC\nGateway"]
    end

    subgraph Core["Core (Domain + Application)"]
        D["Application Services\nUse Cases"]
        E["Domain Entities\nValue Objects\nDomain Services"]
        F["Ports\n(Repo, Mailer, Cache)"]
    end

    subgraph Adapters["Driven Adapters (Infra)"]
        G["Postgres Repo\nimplements Repo"]
        H["SMTP Mailer\nimplements Mailer"]
        I["Redis Cache\nimplements Cache"]
    end

    A --> D
    B --> D
    C --> D
    D --> E
    D --> F
    F --> G
    F --> H
    F --> I
```

### ✅ Checklist & Tips

- Keep internal/domain import-clean (no framework/DB imports).

- Define ports in the domain; implement them in adapters.

- Tests: unit-test use-cases with fakes for ports; integration-test adapters.

### ✅ When to use:

- Systems with high read/write load

- Event-sourced systems (CQRS often pairs with Event Sourcing)

- ⚠️ Pitfall: Adds complexity — not always worth it for simple apps.

---

## 🔀 CQRS (Command Query Responsibility Segregation)

CQRS separates read and write responsibilities into different models:

Commands → update state (writes)

Queries → read state (reads)

This avoids having one bloated model handling both responsibilities.

📍 **Go Example**:

```go
// Command Handler
func CreateUser(repo UserRepository, user User) error {
    return repo.Save(user)
}

// Query Handler
func GetUser(repo UserRepository, id int) (User, error) {
    return repo.Find(id)
}
```

### CQRS Diagram

```mermaid
flowchart LR
    subgraph API["API Layer"]
        A["HTTP Endpoints\n/commands\n/queries"]
    end

    subgraph WriteSide["Write Side"]
        B["Command Handler\n(Validate + Execute)"]
        C["Write Model\n(Domain + Repo)"]
        D[("Write DB")]
    end

    subgraph ReadSide["Read Side"]
        E["Projector\n(Update Projections)"]
        F["Read Model\n(DTO Repository)"]
        G[("Read DB")]
        H["Query Handler\n(Reads Only)"]
    end

    subgraph Bus["Event Bus (Optional)"]
        X["Domain Events"]
    end

    %% Command path
    A -->|POST /commands| B
    B --> C
    C --> D
    C -->|Emit Events| X

    %% Projection path
    X --> E
    E --> F
    F --> G

    %% Query path
    A -->|GET /queries| H
    H --> F

    %% Notes
    classDef dim fill:#f7f7f7,stroke:#bbb,color:#333
    class API,WriteSide,ReadSide,Bus dim
```

✅ When to use:

- Systems with high read/write load

- Event-sourced systems (CQRS often pairs with Event Sourcing)

- ⚠️ Pitfall: Adds complexity — not always worth it for simple apps.

---

## ☁️ Microservices

A Microservices architecture structures applications as a collection of small, independent services:

- Each service owns its data and logic

- Services communicate via APIs (HTTP, gRPC, messaging)

- Each can be deployed and scaled independently

Idea: split a system into small, independently deployable services that each own their data and domain.

Services communicate via synchronous (HTTP/gRPC) or asynchronous (Kafka/NATS) channels.

Each service has its own database (no shared schema).

Requires solid platform engineering: CI/CD, observability, API governance, SLOs.

Suggested repo layout (mono-repo)

```text
.
├─ services/
│  ├─ usersvc/
│  │  ├─ cmd/usersvc/main.go
│  │  ├─ internal/...
│  │  └─ api/openapi.yaml
│  ├─ ordersvc/
│  │  ├─ cmd/ordersvc/main.go
│  │  ├─ internal/...
│  │  └─ api/openapi.yaml
│  └─ paymentsvc/
│     ├─ cmd/paymentsvc/main.go
│     ├─ internal/...
│     └─ api/openapi.yaml
├─ pkg/                         # shared libs (careful: avoid domain leakage)
│  ├─ logger/
│  ├─ tracing/
│  └─ httpx/
├─ deploy/
│  ├─ k8s/                      # Helm/Manifests
│  └─ infra/                    # Terraform (DBs, queues, buckets)
└─ Makefile / Taskfile.yaml
```

### Minimal service skeleton (Gin)

File: `services/usersvc/cmd/usersvc/main.go`

```go
package main

import (
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.New()
	r.Use(gin.Recovery())

	r.GET("/v1/users/:id", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"id": c.Param("id"), "name": "Alice"})
	})

	log.Println("usersvc listening on :8081")
	log.Fatal(http.ListenAndServe(":8081", r))
}
```

### Microservice Diagram

```mermaid
flowchart LR
    subgraph Clients["Clients"]
        A["Web\nMobile"]
    end

    subgraph Edge["API Gateway\nIngress"]
        B["Routing\nAuth\nRate Limit"]
    end

    subgraph Services["Microservices"]
        U["User Service\nDB owned by service"]
        O["Order Service\nDB owned by service"]
        P["Payment Service\nDB owned by service"]
    end

    subgraph Async["Async Messaging"]
        K["Kafka/NATS\nTopics"]
    end

    A --> B
    B --> U
    B --> O
    B --> P

    O <-->|Events| K
    P <-->|Events| K
    U <-->|Events| K
```

✅ Checklist & Tips

- Start with modular monolith → extract services when boundaries stabilize.

- Each service: own DB schema, own CI, own versioning.

- Invest early in observability (traces, logs, metrics) and API contracts.

✅ When to use:

- Large, complex systems needing scalability

- Teams working on independent modules

- ⚠️ Pitfall: Operational overhead (DevOps, CI/CD, observability, networking).

---

## 🔚 Wrap-up pointers

- Hexagonal: best baseline for testability and longevity; add adapters as you go.

- CQRS: apply where read/write divergence brings value; don’t over-split prematurely.

- Microservices: only when team size, domain boundaries, and scaling needs justify the operational cost.

---

## 🧠 Summary

- MVC → Clear separation of concerns in monolithic apps

- Hexagonal → Isolate core logic, improve testability

- CQRS → Split reads and writes for clarity and scalability

- Microservices → Independent, scalable services for large systems

### 👉 Think of it this way:

- Design patterns = small tools (Singleton, Observer, Strategy)

- Architectural patterns = the blueprint of the entire building

- Both are essential, but at different levels of abstraction.

---

🚀 Follow me on [norbix.dev](https://norbix.dev) for more insights on Go, Python, AI, system design, and engineering wisdom.
