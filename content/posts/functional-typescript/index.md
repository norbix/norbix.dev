+++
date = '2026-09-07T10:20:00+02:00'
draft = false
title = "Functional TypeScript in the Real World — From package.json to Runtime Contracts"
tags = ["typescript", "functional-programming", "nodejs", "json-schema", "runtime-validation", "software-architecture", "best-practices"]
categories = ["software-engineering", "best-practices"]
summary = "A practical guide to applying functional programming in production TypeScript backends, covering project setup, explicit dependencies, runtime contract validation, error handling, generated types, and clean architectural boundaries."
comments = true
ShowToc = true
TocOpen = true
image = "banner.png"
weight = 38
+++

> Functional programming becomes much more interesting when it moves beyond textbook examples and into production-grade TypeScript backends.

The important questions are no longer just how to use map(), filter(), or immutable data. Functional principles can influence the architecture of an entire application.

How should dependencies enter a function?

Where should side effects happen?

What should a function return when something fails?

Where does TypeScript's compile-time protection end?

How can API contracts become the source of truth for both types and runtime validation?

Some of these architectural decisions begin surprisingly early—even with the structure of package.json.

This post explores practical patterns for applying functional programming principles to modern TypeScript backends, from project setup and dependency management to contract-driven development, runtime validation, explicit error handling, and clean application boundaries.

All examples are intentionally generic and simplified to focus on the underlying engineering principles.

## 📦 Start with a Deliberate `package.json`

Functional programming doesn't start with `package.json`, but a predictable project does.

A backend should make its development workflow explicit:

```json
{
  "scripts": {
    "dev": "tsx src/server.ts",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "lint": "eslint src",
    "format": "prettier --write .",
    "contracts:generate": "node scripts/generate-contracts.mjs",
    "contracts:check": "node scripts/check-contracts.mjs"
  }
}
```

The exact tools are less important than the idea.

The project should clearly define how to:

* run the application,
* type-check it,
* test it,
* lint and format it,
* generate contract-derived types,
* verify that generated artifacts are synchronized with their contracts.

This makes the repository reproducible.

Instead of relying on a developer remembering a sequence of commands, the repository describes how it should be operated.

That becomes especially important once code generation enters the picture.

## 🧠 TypeScript Is Not Runtime Validation

This was one of the most important distinctions.

Consider:

```ts
type CreateDeviceRequest = {
  serialNumber: string;
};
```

TypeScript can verify this:

```ts
const request: CreateDeviceRequest = {
  serialNumber: "ABC123"
};
```

But TypeScript cannot guarantee that an HTTP client actually sends that structure.

External data arrives at runtime.

Conceptually:

```text
HTTP
 │
 ▼
JSON
 │
 ▼
unknown
 │
 ▼
runtime validation
 │
 ▼
trusted TypeScript value
```

The important word here is:

```ts
unknown
```

Data crossing an external boundary should not magically become a trusted application type because of a cast.

This:

```ts
const request = body as CreateDeviceRequest;
```

doesn't validate anything.

It only tells the compiler:

> Trust me.

Production systems should require more than trust.

## 📜 Contracts as the Source of Truth

A pattern I increasingly like is making the API contract authoritative.

For example:

```text
JSON Schema
     │
     ├────► runtime validator
     │
     └────► generated TypeScript type
```

The same contract now participates in two different worlds.

At compile time:

```text
JSON Schema → TypeScript
```

At runtime:

```text
incoming data → JSON Schema validation
```

That dramatically reduces the possibility of having:

```text
documentation says A
TypeScript says B
runtime accepts C
```

Instead, the architecture pushes toward:

```text
Contract
   │
   ├── TypeScript model
   └── Runtime validation
```

The contract becomes something executable rather than merely documentation.

## 🛡️ Validate at the Boundary

Using a JSON Schema validator such as AJV, an incoming request can remain `unknown` until it proves that it satisfies the contract.

A simplified validator might conceptually look like this:

```ts
const validateRequest = (value: unknown): Result<Request, ValidationError> => {
  if (!validator(value)) {
    return err(toValidationError(validator.errors));
  }

  return ok(value);
};
```

Notice what happens.

The validator accepts:

```ts
unknown
```

and only produces:

```ts
Request
```

after successful validation.

That creates a very useful architectural boundary.

Before validation:

```text
untrusted
```

After validation:

```text
trusted according to our contract
```

## ↔️ Validate Responses Too

Request validation receives most of the attention.

But responses are contracts as well.

Imagine:

```text
Database
   │
   ▼
Service
   │
   ▼
Mapper
   │
   ▼
HTTP Response
```

It is easy for a mapper, service, or refactoring to accidentally produce something that no longer matches the published API.

So the boundary should work in both directions.

```text
REQUEST

HTTP
 ↓
parse
 ↓
unknown
 ↓
contract validation
 ↓
receiving type
 ↓
application


RESPONSE

application
 ↓
sending type / mapper
 ↓
contract validation
 ↓
HTTP
```

This symmetry is powerful.

The API boundary becomes responsible for enforcing the API contract.

Not the database.

Not the domain service.

Not some mapper hidden several layers below.

The boundary.

## 🧩 Pure Core, Impure Shell

This is where functional programming starts shaping architecture.

Every backend needs side effects:

* HTTP calls,
* databases,
* filesystem access,
* secrets,
* logging,
* queues,
* timestamps,
* random values.

Trying to eliminate them is pointless.

The useful goal is to **push them toward the edges**.

Consider:

```ts
const calculateRegion = (country: string): Region =>
  country === "JP" ? "asia" : "europe";
```

For the same input, this function always produces the same output.

It doesn't know about HTTP.

It doesn't know about a database.

It doesn't know about AWS.

It doesn't even know that it is running inside a backend.

That makes it extremely easy to reason about and test.

Compare that with:

```ts
const processRequest = async () => {
  const record = await database.get(...);
  const secret = await secrets.get(...);
  const response = await httpClient.send(...);

  // ...
};
```

Side effects are unavoidable here.

But we can organize the system so that most decision-making happens in small functions while orchestration coordinates effects around them.

This leads naturally toward:

```text
        IMPURE BOUNDARY
              │
              ▼
       parse / validate
              │
              ▼
         PURE LOGIC
              │
              ▼
          services
              │
              ▼
     databases / APIs
              │
              ▼
         map result
              │
              ▼
       validate response
              │
              ▼
        IMPURE BOUNDARY
```

## 💉 Dependency Injection Without a Framework

Functional TypeScript also changed how I think about dependency injection.

You don't necessarily need a DI container.

Functions already provide dependency injection.

Instead of:

```ts
const getUser = async (id: string) => {
  return database.findUser(id);
};
```

we can make the dependency explicit:

```ts
const getUser = async (
  database: UserRepository,
  id: string
) => {
  return database.findUser(id);
};
```

Or create a function that captures the dependency:

```ts
const createGetUser =
  (database: UserRepository) =>
  async (id: string) =>
    database.findUser(id);
```

Now the dependency graph is visible.

Testing becomes simpler:

```ts
const fakeRepository = {
  findUser: async () => ({ id: "123", name: "John" })
};

const getUser = createGetUser(fakeRepository);
```

No framework magic.

No global state.

No complicated mocking machinery.

Just functions.

## 📦 Errors Are Values Too

Another useful functional idea is treating expected failures as values.

A simplified result type:

```ts
type Result<T, E> =
  | { ok: true; value: T }
  | { ok: false; error: E };
```

A function can now communicate failure explicitly:

```ts
const findConfiguration = async (
  id: string
): Promise<Result<Configuration, ConfigurationError>> => {
  // ...
};
```

The caller cannot pretend failure doesn't exist.

It must inspect the result.

```ts
const result = await findConfiguration(id);

if (!result.ok) {
  return handleError(result.error);
}

return useConfiguration(result.value);
```

Compare that with a function returning:

```ts
Promise<Configuration>
```

while secretly being capable of throwing several unrelated exceptions.

`Result` makes the failure path part of the function's contract.

This becomes particularly useful in backend systems where infrastructure errors eventually need to become meaningful HTTP responses.

## 🔄 Transformation Should Be Explicit

Another recurring pattern is separating transport contracts from internal models.

Suppose the API accepts:

```ts
type ApiRequest = {
  countryCode: string;
};
```

while internally we want:

```ts
type Location = {
  country: string;
};
```

The transformation can simply be:

```ts
const toLocation = (request: ApiRequest): Location => ({
  country: request.countryCode
});
```

This is a tiny function.

And that is exactly why it is useful.

It has:

* no side effects,
* no infrastructure dependency,
* deterministic output,
* trivial tests,
* a single responsibility.

A mapper should transform data.

A validator should validate data.

A service should perform application operations.

An HTTP handler should coordinate the boundary.

Keeping those responsibilities separate prevents surprisingly large amounts of complexity.

## ⚙️ Generate Types, But Verify Them

Code generation introduces another problem.

Suppose we have:

```text
contracts/
   request.schema.json
   response.schema.json

src/types/
   request.ts
   response.ts
```

The TypeScript files are generated from the schemas.

Someone changes:

```text
request.schema.json
```

but forgets to regenerate:

```text
request.ts
```

Now the repository contains two versions of reality.

A useful CI invariant is therefore:

```text
committed generated types
          ==
types generated from current contracts
```

Conceptually, CI can:

```text
1. preserve current generated models
2. regenerate models from contracts
3. compare them
4. fail if they differ
```

The important distinction is that this does **not** prove the API contract is correct.

It proves something narrower and extremely valuable:

> The generated TypeScript models accurately represent the currently committed contracts.

Contract correctness and generated-code synchronization are different problems.

Keeping that distinction explicit makes the tooling easier to understand.

## 🧱 The Architecture That Emerges

Put these ideas together and a backend starts looking something like this:

```text
                    ┌───────────────┐
                    │  API Contract │
                    │  JSON Schema  │
                    └───────┬───────┘
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
        Generated TS Types      Runtime Validators
                 │                     │
                 └──────────┬──────────┘
                            │
                            ▼
HTTP ──► Parse ──► Validate ──► Map ──► Service
                                            │
                                   ┌────────┴────────┐
                                   ▼                 ▼
                              Database          External API
                                   │                 │
                                   └────────┬────────┘
                                            ▼
                                         Result
                                            │
                                            ▼
HTTP ◄── Validate ◄── Map ◄────────────────┘
```

There are still side effects.

There are still asynchronous operations.

There are still databases, network failures, infrastructure errors, and ugly real-world data.

Functional programming doesn't make those disappear.

It gives us tools for **containing the complexity**.

## 🧪 Testing Becomes a Consequence of the Design

One of the best signs of a good architecture is that testing becomes boring.

Pure transformation:

```ts
expect(toLocation(input)).toEqual(expected);
```

Dependency passed as a parameter:

```ts
const service = createService(fakeRepository);
```

Explicit result:

```ts
expect(result).toEqual(ok(expected));
```

Invalid external data:

```ts
expect(validateRequest(invalid)).toEqual(
  expect.objectContaining({ ok: false })
);
```

There is less need to reconstruct an entire application environment just to test one decision.

Testability isn't something added afterward.

It emerges from the design.

## 🚫 Functional Programming Is Not "No Classes"

I used to think discussions around functional TypeScript too easily became:

```text
functions good
classes bad
```

That misses the useful part.

Functional programming is much more about properties such as:

* explicit inputs,
* explicit outputs,
* controlled side effects,
* immutability,
* deterministic transformations,
* composition,
* dependencies visible in function signatures,
* failures represented explicitly.

A TypeScript application doesn't need to become academically functional to benefit from these ideas.

The practical question is:

> Can I understand what this function can do by looking at its inputs and output?

The closer the answer is to **yes**, the easier the system usually becomes to maintain.

## 🚀 What Changed My View of TypeScript

TypeScript is often introduced as:

> JavaScript with types.

Technically, that's reasonable.

Architecturally, it undersells it.

Combined with runtime schemas, generated contracts, functional boundaries and explicit error models, TypeScript can support remarkably disciplined backend architectures.

The key is understanding where TypeScript ends.

Types disappear at runtime.

The network doesn't care about your interfaces.

A database doesn't promise to return what your TypeScript type says.

An external API doesn't know that you wrote:

```ts
as MyType
```

That is why the combination matters:

```text
TypeScript
    +
runtime validation
    +
explicit contracts
    +
functional design
    +
automated verification
```

Compile-time safety handles one part of the problem.

Runtime contracts handle another.

Functional architecture keeps the pieces understandable.

## 🏁 Final Thoughts

The most useful functional programming lessons I've learned from production TypeScript weren't about clever abstractions.

They were surprisingly simple:

**Keep pure logic pure.**

Push side effects toward boundaries.

Treat external data as `unknown`.

Validate requests **and responses**.

Let contracts generate types where possible.

Verify generated artifacts in CI.

Pass dependencies explicitly.

Represent expected failures explicitly.

Keep transformations small and deterministic.

And make the repository itself—from `package.json` scripts onward—describe how the system is supposed to work.

None of these techniques is particularly impressive in isolation.

Together, however, they create something much more valuable:

**a backend whose behavior is easier to reason about.**

And for me, that is where functional programming becomes genuinely useful—not as a programming style, but as an engineering tool.

---

🚀 Follow me on [norbix.dev](https://norbix.dev) for more insights on Go, TypeScript, Python, AI, system design, and software engineering.
