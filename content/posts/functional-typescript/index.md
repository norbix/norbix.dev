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

![banner](banner.png)

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

## 🛠️ Utility Types: Derive Models Without Duplicating Them

Small transformations are useful at the type level too.

A backend often needs several views of the same data: a stored record, a creation command, an update command, and a public response.

Writing each shape by hand makes changes harder to keep consistent.

TypeScript's built-in utility types let us express how those shapes relate. They are available without imports.

Start with a simple internal model:

```ts
type Device = {
  id: string;
  serialNumber: string;
  country: string;
  firmwareVersion?: string;
  internalToken: string;
  metadata: {
    model: string;
    labels: string[];
  };
};
```

### `Record<K, T>`: Model a Lookup Table

Sometimes the relationship is between a set of keys and one value type.

```ts
type Market = "PL" | "DE" | "JP";
type Region = "europe" | "asia";

const regionByMarket: Record<Market, Region> = {
  PL: "europe",
  DE: "europe",
  JP: "asia"
};

const resolveRegion = (market: Market): Region =>
  regionByMarket[market];
```

`K` describes the keys. `T` describes the value stored under each key.

Here, every market in the finite union needs an entry. Adding another market makes the compiler point out the missing mapping.

This works well for routing rules, status labels, and configuration tables.

An open dictionary needs more care:

```ts
const devicesById: Partial<Record<string, Device>> = {};

const device = devicesById["missing-id"];
// Device | undefined
```

A type annotation cannot guarantee that an arbitrary identifier exists at runtime. Use an optional lookup shape, or enable `noUncheckedIndexedAccess` to make unchecked indexed reads account for missing values.

### `Omit<T, K>`: Leave Selected Properties Out

A client creating a device should not need to provide fields owned by the server.

```ts
type CreateDeviceCommand = Omit<Device, "id" | "internalToken">;

const command: CreateDeviceCommand = {
  serialNumber: "ABC123",
  country: "PL",
  metadata: {
    model: "sensor",
    labels: []
  }
};
```

The remaining properties keep their existing types and modifiers. `firmwareVersion` is still optional.

This is useful when a derived model should follow most of the original model.

There is a tradeoff: adding a property to `Device` also adds it to this command unless we exclude it. For a public contract that must evolve independently, an explicit contract can be a better choice.

### `Pick<T, K>`: Select a Focused View

A response often needs only a few properties.

```ts
type DeviceSummary = Pick<Device, "id" | "serialNumber" | "country">;

const toDeviceSummary = (device: Device): DeviceSummary => ({
  id: device.id,
  serialNumber: device.serialNumber,
  country: device.country
});
```

The selected keys must exist in `Device`.

This gives the mapper a focused output type and makes the intended response easy to inspect.

Neither `Pick` nor `Omit` changes an object at runtime:

```ts
const unsafeSummary = (device: Device): DeviceSummary => device;
```

This can compile because TypeScript uses structural compatibility. The returned object still contains `internalToken` and every other original field. Serializing it can expose those fields.

The explicit mapper above constructs the actual response. A return type alone does not filter data.

### `Readonly<T>`: Prevent Reassignment Through a Typed Reference

Functional transformations are easier to follow when input data stays unchanged.

The built-in spelling is `Readonly<T>`.

```ts
const moveDevice = (
  device: Readonly<Device>,
  country: string
): Device => ({
  ...device,
  country
});
```

Reassigning `device.country` inside this function would be a type error. Returning a new object makes the change explicit.

However, `Readonly` on this object is shallow:

```ts
const inspectDevice = (device: Readonly<Device>): void => {
  device.metadata.labels.push("inspected");
  // Allowed: the nested array is still mutable.
};
```

It also does not freeze the object at runtime or prevent another mutable reference from changing it.

For nested immutability, model nested properties as readonly too. For runtime enforcement, consider freezing where appropriate; `Object.freeze` itself is also shallow.

### `Required<T>`: Describe a Fully Populated Shape

Configuration often begins with optional overrides and ends with resolved values.

```ts
type ClientOptions = {
  timeoutMs?: number;
  retries?: number;
};

type ResolvedClientOptions = Required<ClientOptions>;

const resolveClientOptions = (
  options: ClientOptions
): ResolvedClientOptions => ({
  timeoutMs: options.timeoutMs ?? 3000,
  retries: options.retries ?? 3
});
```

`Required` removes the optional property markers. The function supplies the actual defaults.

The distinction matters: changing a type does not fill missing values. It also does not validate that `timeoutMs` is positive or `retries` is an integer.

Required properties are not automatically non-nullable. If a property's value type allows `null`, that remains a separate concern.

### `Partial<T>`: Describe an Update With Optional Fields

An update command usually changes only part of a model.

First select the properties clients may edit. Then make those properties optional.

```ts
type DeviceUpdate = Partial<
  Pick<Device, "country" | "firmwareVersion">
>;

const applyDeviceUpdate = (
  device: Readonly<Device>,
  update: Readonly<DeviceUpdate>
): Device => ({
  ...device,
  ...(update.country !== undefined
    ? { country: update.country }
    : {}),
  ...(update.firmwareVersion !== undefined
    ? { firmwareVersion: update.firmwareVersion }
    : {})
});
```

Selecting editable fields keeps server-owned properties out of the declared update shape. The function also explicitly selects fields at runtime rather than blindly spreading an input object.

Here, an absent or `undefined` value means “leave the existing value unchanged.” Clearing a field would need an explicit policy, such as a validated `null` value or a separate operation.

`Partial` is shallow. If a selected property contains a nested object, making that property optional does not make the nested object's properties optional.

It also permits an empty object:

```ts
const noChanges: DeviceUpdate = {};
```

If the endpoint requires at least one change, enforce that in the runtime contract, for example with JSON Schema's `minProperties: 1`.

The compiler option `exactOptionalPropertyTypes` helps distinguish omission from explicitly assigning `undefined`. Runtime validation still needs its own rules for accepted update values.

### Compose Types, Keep Runtime Work Explicit

These utilities can be combined:

```ts
type PublicDevice = Readonly<
  Pick<Device, "id" | "serialNumber" | "country">
>;

type DeviceDraft = Partial<
  Omit<Device, "id" | "internalToken">
>;

type RoutingTable = Readonly<Record<Market, Region>>;
```

Each composition describes a relationship. It does not perform validation, projection, defaulting, or freezing.

| Utility | Type-level effect | Typical backend use |
| --- | --- | --- |
| `Record<K, T>` | Maps keys to a value type | Routing and lookup tables |
| `Omit<T, K>` | Excludes selected properties | Commands without server-owned fields |
| `Pick<T, K>` | Selects existing properties | Focused response models |
| `Readonly<T>` | Adds readonly property modifiers | Input references that reject reassignment |
| `Required<T>` | Removes optional property markers | Resolved configuration |
| `Partial<T>` | Makes properties optional | Drafts and update commands |

Use these tools to express relationships inside the application. When a public API contract is authoritative, derive its boundary types from that contract and use utilities where they accurately describe internal models.

That keeps type reuse aligned with the architecture instead of making every API shape depend on a database record.

For the complete built-in definitions and reference examples, see the [TypeScript Utility Types documentation](https://www.typescriptlang.org/docs/handbook/utility-types.html).

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

## How to contribute

All committed code must be tested, linted, and formatted. Check `package.json` for available scripts.

Code samples below reflect the project's `tsconfig` and linting rules.

These are guidelines, not commandments. Feel free to contest them, propose alternatives, and discuss tradeoffs with the team — including linter rules.

### 1. Keep it simple

Write code readable at 3 AM. Use explicit `type`s. Avoid `any`, complex generics, and vague types.

```ts
// GOOD
type Device = {
  id: string
  name: string
}

// BAD
interface IDevice {
  [key: string]: any
}
```

### 2. Don't mutate arguments, don't optimise prematurely

If not needed, don't optimise prematurely. Clarity beats performance until a profiler tells you otherwise.

```ts
// GOOD
function addItem(items: readonly string[], item: string): string[] {
  return [...items, item]
}

// BAD
function addItem(items: string[], item: string): void {
  items.push(item)
}
```

### 3. Avoid types that cause boilerplate — use discriminated unions

```ts
// GOOD — each case is self-describing, and narrowing is trivial
type Result =
  | { statusCode: 200; result: number }
  | { statusCode: 400; errorMessage: string }

function handle(result: Result) {
  if (result.statusCode === 200) {
    // TypeScript knows result.result exists here
    console.log(result.result)
  }
}

// BAD — vague, everything is optional
type Result = {
  statusCode: 200 | 400
  errorMessage?: string
  result?: number
}
```

### 4. Separate concerns

For example: handlers decide HTTP responses. Business logic returns data or throws — it never picks status codes.

```ts
export async function handler(event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> {
  const devices = await getDevicesByUser(event.pathParameters.userId)

  if (devices.length === 0) {
    return notFound({ message: "No devices found" })
  }

  return ok({ devices })
}
```

### 5. Use async/await

Avoid `new Promise` and callback nesting when an async alternative exists.

```ts
// GOOD
async function fetchData(id: string): Promise<Data> {
  const response = await client.get(id)
  return response.data
}

// BAD
function fetchData(id: string): Promise<Data> {
  return new Promise((resolve, reject) => {
    client.get(id, (err, res) => {
      if (err) reject(err)
      else resolve(res.data)
    })
  })
}
```

### 6. Throw simple errors

Use built-in errors first: `Error`, `TypeError`, `RangeError`, etc. If needed, extend `Error` with a single project-wide class. Don't invent error hierarchies prematurely. This is up to discussion.

```ts
throw new Error("Device not found")
throw new RangeError("Offset must be non-negative")
```

### 7. Don't try/catch everything

Only catch when the flow needs to change or you can enrich the error. Don't catch-and-rethrow without adding value.

```ts
// GOOD — catch changes the flow
try {
  await saveDevice(device)
} catch (error) {
  await notifyAdmin(device.id)
  return serviceUnavailable({ message: "Save failed, admin notified" })
}

// BAD — pointless rethrow
try {
  await saveDevice(device)
} catch (error) {
  throw error
}
```

### 8. Be explicit with null checks

Avoid `!something` for null/undefined checks — it also catches `0`, `""`, and `false`, which leads to subtle bugs.

```ts
// GOOD — explicit, only catches null and undefined
if (value == null) {
  return
}

// BAD — also catches 0, empty string, false
if (!value) {
  return
}
```

### 9. Think before adding dependencies

First check if Node.js already provides what you need (e.g. `crypto`, `fs/promises`, `URL`, `structuredClone`). If you still need a library, check how much it weighs, whether it's maintained, secure, and ideally has no transitive dependencies. As obvious — less is more.

### 10. Refer to primary sources

When in doubt, refer to W3C, TypeScript documentation, MDN Web Docs, or Node.js docs rather than blog posts or Stack Overflow.

### 11. Organize code into cohesive modules

Don't be afraid to create files that group multiple related functions. Group things that belong together.

```ts
// src/device/resource.ts
export function addDevice(payload: AddDevicePayload) { ... }
export function deleteDevice(payload: DeleteDevicePayload) { ... }
export function listDevices(payload: ListDevicesPayload) { ... }
```

### 12. Don't export internal functions for testing

Internal functions stay internal. Tests exercise the public API (black-box testing). If you can't test behavior through the public interface, reconsider your design — not your export boundaries.

### 13. Tests must not leak state

Each test runs in isolation. Don't rely on execution order or shared mutable state between tests. If a test fails when run alone, it's broken.

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
