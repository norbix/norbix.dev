+++
title = "Understanding Databases: B-Trees, SQL, NoSQL, ACID, and Normalization"
date = "2025-04-28T18:00:00+02:00"
draft = false
tags = ["databases", "sql", "nosql", "btrees", "acid", "normalization"]
categories = ["software-engineering", "databases"]
summary = "Learn the key database concepts every software engineer should know: B-Trees, SQL, NoSQL, ACID properties, and database normalization principles."
comments = true
ShowToc = true
TocOpen = true
image = "banner.jpg"
weight = 17
+++

![banner](banner.jpg)

**"Bad data ruins good applications. Good databases build great systems."**

Databases are the silent powerhouse behind most modern applications. Whether you’re building a simple blog, an enterprise CRM, or a distributed IoT system, understanding database fundamentals can dramatically improve the quality and scalability of your software.

In this article, I’ll walk through essential database concepts every engineer should master: B-Trees, SQL, NoSQL, ACID properties, and normalization.

---

## 📚 B-Trees: The Backbone of Indexing

Efficient data retrieval is crucial, and that's where B-Trees come in. B-Trees are balanced tree structures that allow fast search, insert, and delete operations in logarithmic time.

In databases like MySQL (InnoDB) and PostgreSQL, indexes are often implemented as B-Trees, making queries much faster by avoiding full table scans.

🔹 **Tip:** Always index columns used in WHERE, JOIN, and ORDER BY clauses to leverage B-Tree advantages.

---

## 📂 SQL: Structured Query Language

SQL is the standard language for querying and manipulating relational databases.

Key operations:

- `SELECT`: Retrieve data
- `INSERT`: Add new records
- `UPDATE`: Modify existing records
- `DELETE`: Remove records

SQL enforces a strict schema and supports relationships, making it ideal for structured data.

Popular SQL databases: PostgreSQL, MySQL, MariaDB, Microsoft SQL Server.

🔹 **Tip:** Master `JOIN` operations and subqueries to unlock SQL's full power.


### 🔰 PostgreSQL quick start (copy–paste)

```sql
-- One-time sandbox
CREATE SCHEMA learnsql;
SET search_path TO learnsql;

CREATE TABLE authors (
  author_id BIGSERIAL PRIMARY KEY,
  name      TEXT NOT NULL,
  country   TEXT NOT NULL
);

CREATE TABLE books (
  book_id    BIGSERIAL PRIMARY KEY,
  author_id  BIGINT NOT NULL REFERENCES authors(author_id),
  title      TEXT NOT NULL,
  year       INT,
  price_usd  NUMERIC(6,2) CHECK (price_usd >= 0)
);

INSERT INTO authors (name, country) VALUES
 ('Alicja Kowalska','PL'), ('Bartosz Nowak','PL'),
 ('Chloe Schneider','DE'), ('Diego García','ES');

INSERT INTO books (author_id,title,year,price_usd) VALUES
 (1,'SQL for Starters',2023,29.99),
 (1,'Advanced SQL Patterns',2025,39.50),
 (2,'Data Modeling 101',2022,24.00),
 (2,'PostgreSQL Cookbook',2024,35.00),
 (3,'Window Functions in Practice',2024,32.00),
 (4,'Indexing and Performance',2021,27.50),
 (4,'JSON in Postgres',2025,31.00);
```

#### Select & filter

Select specific columns, filter with `WHERE`, sort with `ORDER BY`, and limit results with `LIMIT`.

```sql
SELECT title, price_usd
FROM books
WHERE price_usd > 30
ORDER BY price_usd DESC
LIMIT 3;
```

#### Joins

Joins combine rows from two or more tables based on related columns.

A SQL JOIN doesn’t permanently merge tables; it builds a wider result set at query time by pairing rows whose keys match your condition. 
Think of it as a lookup that produces a new, temporary table.

##### Inner join (most common)

Keep matching rows from both tables.

```sql
-- All books with author info
SELECT b.title, a.name AS author, a.country, b.year, b.price_usd
FROM books b
JOIN authors a ON a.author_id = b.author_id
ORDER BY a.name, b.year;
```

##### Left join

Keep all rows from the left table, even if there’s no match on the right.

```sql
--- Only authors with their books (if any)
SELECT a.name, b.title
FROM authors a
LEFT JOIN books b ON b.author_id = a.author_id
ORDER BY a.name, b.title;
```

##### Right join

Keep all rows from the right table, even if there’s no match on the left.

```sql
SELECT a.name, b.title
FROM books b
RIGHT JOIN authors a ON a.author_id = b.author_id;
```

##### Full outer join

Keep all rows from both tables, matching where possible.

```sql
SELECT COALESCE(a.name, '[no author]') AS author, b.title
FROM authors a
FULL JOIN books b ON b.author_id = a.author_id;
```

##### Cross join

Produces the Cartesian product of two tables (every row from A with every row from B).

```sql
SELECT a.name, y.year
FROM authors a
CROSS JOIN (VALUES (2024), (2025)) AS y(year);
```

##### Semi/anti joins (idiomatic filters)

EXISTS (semi-join): return authors who have at least one book.

```sql
SELECT a.*
FROM authors a
WHERE EXISTS (SELECT 1 FROM books b WHERE b.author_id = a.author_id);
```

LEFT + IS NULL (anti-join): return authors without books.

```sql
SELECT a.*
FROM authors a
LEFT JOIN books b ON b.author_id = a.author_id
WHERE b.author_id IS NULL;
```

**(You can also write WHERE NOT EXISTS (...).)**

##### USING vs ON (syntax sugar)

If join columns share the same name, USING(column) saves typing and removes duplicate columns in the result:

```sql
-- If both tables have column author_id
SELECT *
FROM books
JOIN authors USING (author_id);
```

##### Nulls & duplicates gotchas

- `INNER JOIN` drops non-matching rows; LEFT JOIN keeps them with NULLs on the right.

- Aggregates on left joins: count only matched rows with `COUNT(b.book_id)` (not COUNT(*)), since `COUNT(*)` counts the left row even when unmatched.

- If the right side can have multiple matches, rows duplicate (one per match). Use `DISTINCT` or aggregate if you need one row per left.

##### Choosing the right join (rule of thumb)

- Need only matched pairs? → INNER.

- Keep everything from A, optional B? → LEFT.

- Symmetric “show all, mark gaps”? → FULL OUTER.

- Filtering presence/absence? → EXISTS / LEFT … IS NULL (semi/anti).

#### Aggregation

Aggregate functions summarize data: `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`.

```sql
-- Avg price by country; only countries with ≥2 books
SELECT a.country,                              -- 1) grouping key (country)
       ROUND(AVG(b.price_usd), 2) AS avg_price -- 2) average book price, 2 decimals
FROM books b
JOIN authors a ON a.author_id = b.author_id    -- 3) attach each book to its author's country
GROUP BY a.country                             -- 4) aggregate per country
HAVING COUNT(*) >= 2                           -- 5) keep only countries with 2+ books
ORDER BY avg_price DESC;                       -- 6) sort by avg price, highest first
```

**Hint: `GROUP BY` vs `ORDER BY`**

- `GROUP BY` partitions rows into groups and reduces them (with aggregates like COUNT, AVG, SUM).

- `ORDER BY` sorts the final rows (whatever they are—raw or aggregated).

They do different jobs and often appear together.

#### Useful operators 

```sql
-- Case-insensitive search
SELECT title FROM books WHERE title ILIKE '%sql%';

-- Categorize with CASE
SELECT title,
       CASE WHEN price_usd >= 35 THEN 'premium'
            WHEN price_usd >= 30 THEN 'mid'
            ELSE 'budget' END AS price_tier
FROM books;

-- Distinct values
SELECT DISTINCT country FROM authors ORDER BY country;
```

#### CTEs (WITH) & subqueries

CTE (Common Table Expression) example:

```sql
-- Authors whose average book price > $30
WITH avg_price AS (
  SELECT author_id, AVG(price_usd) AS avg_price
  FROM books
  GROUP BY author_id
)
SELECT a.name, ap.avg_price
FROM avg_price ap
JOIN authors a ON a.author_id = ap.author_id
WHERE ap.avg_price > 30;
```

#### Window functions (analytics without collapsing rows)

Functions like `ROW_NUMBER()`, `RANK()`, `SUM() OVER()`, etc., operate over a set of rows related to the current row.

```sql
-- Rank the most expensive book per author
SELECT a.name, b.title, b.price_usd,
       RANK() OVER (PARTITION BY a.author_id ORDER BY b.price_usd DESC) AS rnk
FROM books b
JOIN authors a ON a.author_id = b.author_id
ORDER BY a.name, rnk;
```

#### Indexes & EXPLAIN (performance mindset)

Indexes speed up lookups but slow down writes and take space. Use them wisely.

```sql
CREATE INDEX idx_books_author_year ON books(author_id, year);
EXPLAIN ANALYZE
SELECT * FROM books WHERE author_id = 2 AND year >= 2024 ORDER BY year;
```

If you see a sequential scan on a large table, consider whether your index matches the filter and order columns (and their order).

#### Common pitfalls (Postgres)

- Strings use single quotes ('PL'). Double quotes are identifiers.

- NULL logic: use IS NULL / IS NOT NULL; = NULL is never true.

- Integer division: 1/2 = 0. Cast for rates: sum(x)::numeric / nullif(count(*),0).

- All non-aggregated SELECT columns must appear in GROUP BY.

- Prefer window functions for “top-k per group” and “rolling” metrics.

### 🔒 Transactions (PostgreSQL): writing safely

A transaction groups multiple statements so they succeed all together or not at all.

#### Quick start

```sql
BEGIN;                                   -- start a transaction
  INSERT INTO orders(customer_id) VALUES (42) RETURNING id;
  INSERT INTO order_items(order_id, product_id, qty) VALUES (currval('orders_id_seq'), 7, 2);
COMMIT;                                   -- make changes durable
-- ROLLBACK;                              -- undo everything (if something went wrong)
```

- Postgres is autocommit by default (each statement = its own transaction).

- Inside a transaction, an error aborts the txn until you ROLLBACK (or use a SAVEPOINT).

#### Savepoints (recover from a partial failure)

```sql
BEGIN;
  SAVEPOINT s1;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  -- if a check fails you can roll back just this part:
  -- ROLLBACK TO SAVEPOINT s1;

  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

#### Idempotent upsert (avoid duplicates, safe retries)

Use a unique constraint and `ON CONFLICT`:

```sql
-- setup once:
-- CREATE UNIQUE INDEX ux_inventory_sku ON inventory(sku);

INSERT INTO inventory(sku, stock)
VALUES ('A-001', 10)
ON CONFLICT (sku) DO UPDATE
SET stock = inventory.stock + EXCLUDED.stock
RETURNING *;
```

This is retry-safe if your app repeats the insert after a crash.

#### Claim-a-job queue (locking without blocking the world)

```sql
-- One worker atomically claims the highest-priority unclaimed job.
UPDATE jobs
SET claimed_by = 'worker-1', claimed_at = now()
WHERE id = (
  SELECT id FROM jobs
  WHERE claimed_by IS NULL
  ORDER BY priority DESC, created_at
  FOR UPDATE SKIP LOCKED
  LIMIT 1
)
RETURNING *;
```

- `FOR UPDATE` locks the chosen row;

- `SKIP LOCKED` makes other workers skip locked rows (great for parallel consumers);

- Add `NOWAIT` if you prefer to error instead of waiting.

#### Consistent reads (isolation level quick use)

Default is READ COMMITTED. For a stable snapshot during an analytical read:

```sql
BEGIN;
  SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
  -- all SELECTs below see the same snapshot
  SELECT COUNT(*) FROM orders WHERE status = 'paid';
  SELECT SUM(total_cents) FROM orders WHERE status = 'paid';
COMMIT;
```

For cross-row invariants, use SERIALIZABLE and be ready to retry on 40001.

#### Keep invariants in the database (constraints)

```sql
CREATE TABLE orders (
  id BIGSERIAL PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customers(id),
  status TEXT NOT NULL CHECK (status IN ('new','paid','shipped','cancelled'))
);
```

Constraints + transactions = fewer data bugs than app-only checks.

#### DDL is transactional in Postgres

```sql
BEGIN;
  ALTER TABLE orders ADD COLUMN shipped_at timestamptz;
ROLLBACK;   -- schema change undone too
```

#### Handy patterns

- Return data you just wrote: `INSERT ... RETURNING *`

- Short transactions win: keep them brief to reduce contention & bloat.

- Deterministic ordering: add unique tiebreakers in `ORDER BY` inside write paths.

---

## 🔄 NoSQL: Flexibility at Scale

NoSQL databases emerged to handle massive, unstructured, and rapidly changing data.

Types of NoSQL databases:

- Document stores: MongoDB, Couchbase
- Key-value stores: Redis, DynamoDB
- Wide-column stores: Cassandra, HBase
- Graph databases: Neo4j, Amazon Neptune

NoSQL systems often prioritize availability and partition tolerance (CAP theorem) over strict consistency.

🔹 **Tip:** Choose NoSQL when your application requires high write throughput, horizontal scaling, or flexible schemas.

NoSQL systems were built to handle massive scale, high write throughput, global availability, and flexible schemas. Instead of one relational model, NoSQL offers several data models optimized for different access patterns.

### Why teams pick NoSQL

- Scale-out horizontally (add nodes instead of bigger nodes).

- Flexible schema (evolve fields without migrations).

- Low-latency reads/writes at high volume.

- Built-in sharding & replication (varies by engine).

**⚖️ Trade-off: You often give up rich joins, multi-table transactions, or strict relational constraints in exchange for scale and simplicity of operations.**

### The landscape at a glance

- Document stores (MongoDB, Couchbase) — JSON-like docs, rich secondary indexes.

- Key–value / single-table (DynamoDB, Redis) — ultra-fast point access, simple patterns.

- Wide-column (Cassandra, HBase) — time-series & large-scale event data with tunable consistency.

- Graph (Neo4j, Neptune) — first-class relationships and traversals.

### CAP & BASE in one minute

- `CAP`: Under partitions you can choose at most two of {Consistency, Availability, Partition tolerance}. Distributed systems must tolerate partitions, so engines lean C or A.

- `BASE`: Basically Available, Soft state, Eventually consistent — a pragmatic stance for internet-scale systems. Some engines offer tunable consistency per request.

### Consistency menu (common options):

- Strong (read sees latest committed write) — e.g., DynamoDB strongly consistent read, MongoDB readConcern: "majority" with writeConcern: {w: "majority"}.

- Eventual (reads may lag) — highest availability/throughput.

- Causal / session (reads respect causality) — MongoDB readConcern: "local" + sessions; Cosmos DB offers session consistency.

- Tunable (Cassandra): choose QUORUM, ONE, ALL per operation.

### Modeling by data model (practical patterns)

1. Document store (MongoDB)

    Use embedding when you read parent+child together and the child set is bounded; referencing when children grow large or are shared.
    
    Order with embedded items (embedding):

    ```mongodb-json
    {
        "_id": "o#1001",
        "customerId": "c#12",
        "status": "paid",
        "items": [
            {"sku": "SKU-1", "qty": 1, "price": 19.99},
            {"sku": "SKU-2", "qty": 2, "price": 9.90}
        ],
        "createdAt": ISODate("2025-09-05T10:00:00Z")
    }
    ```

    Query + index:

    ```mongodb
    // index: { status: 1, createdAt: -1 }
    db.orders.find({ status: "paid", createdAt: { $gte: ISODate("2025-09-01") } })
            .sort({ createdAt: -1 })
            .limit(50)
    ```

    When to reference: items reused, or unbounded growth. Store orderItems in a separate collection keyed by orderId.

1. Key–value / single-table (DynamoDB)

    Design from queries back. Choose PK (partition key) for distribution, SK (sort key) for slicing. Use GSIs for alternate access.
    
    Single-table design example:

    ```mongodb-json
    { "PK": "C#12", "SK": "META", "name": "Alice", "tier": "gold" }
    { "PK": "C#12", "SK": "ORDER#2025-09-05#1001", "total": 39.79 }
    { "PK": "C#12", "SK": "ORDER#2025-09-07#1002", "total": 89.00 }
    // GSI1PK = SK prefix enables order-by-date queries per customer
    ```

    Queries:

    ```mongodb
    Get customer: GetItem(PK="C#12", SK="META")
    List recent orders: Query(PK="C#12", SK begins_with "ORDER#2025-") LIMIT 25
    ```

    Pitfalls: hot partitions (low-cardinality PK), large items (>400KB), and Scan (avoid in prod paths).

1. Wide-column (Cassandra)

    Tables are pre-optimized for queries; denormalize per access pattern. Pick partition key for distribution; clustering columns for on-disk order.

    ```sql
    -- Events per device per day (time-series buckets)
    CREATE TABLE events_by_device (
    device_id text,
    day date,
    ts timestamp,
    event text,
    payload text,
    PRIMARY KEY ((device_id, day), ts)
    ) WITH CLUSTERING ORDER BY (ts DESC);
    
    
    -- Query: latest 100 events for a device today
    SELECT * FROM events_by_device
    WHERE device_id='d-42' AND day='2025-09-08' LIMIT 100;
    ```

    Consistency: CONSISTENCY QUORUM (balance C/A). Prefer idempotent writes; consider TTL for roll-off.

1. Graph (Neo4j/Cypher)

    Great for recommendations, fraud rings, network analysis.

    ```sql
    // People who worked with Alice on the same project (2 hops)
    MATCH (a:Person {name: 'Alice'})-[:WORKED_ON]->(p:Project)<-[:WORKED_ON]-(colleague)
    RETURN DISTINCT colleague.name
    ORDER BY colleague.name;
    ```

    Strengths: variable-length traversals and path queries that are awkward in SQL or KV stores.

### Sharding & replication (nutshell)

- Sharding distributes data across nodes by a key (hash/range). Choose keys with high cardinality to avoid hotspots.

- Replication provides HA and read scale. Define replication factor (e.g., 3). Some engines offer multi-region replicas with per-request consistency.

- Resharding (moving partitions) can be online but still needs capacity planning.


### Secondary indexes & queries

- `MongoDB`: compound indexes; text/geo indexes; partial/TTL indexes.

- `DynamoDB`: GSI (global), LSI (local) — plan them up front; each has throughput cost.

- `Cassandra`: prefer query tables over global secondary indexes; use materialized views cautiously.


### Transactions & constraints in NoSQL

- `MongoDB`: multi-document transactions (replica set / sharded clusters) exist but reduce throughput; prefer single-document atomicity when possible.

- `DynamoDB`: TransactWriteItems (25 items) for all-or-nothing across keys.

- `Cassandra`: lightweight transactions (LWT) for compare-and-set; higher latency.

**Rule of thumb: keep invariants within a partition/document; cross-entity invariants need application-level workflows (sagas, outbox).**

### When to choose NoSQL vs SQL

#### Pick NoSQL when:

- You know your access patterns and they map cleanly to a single partition/document.

- You need millions of writes/sec, global distribution, or sub-10 ms reads at scale.

- Your data is naturally hierarchical (documents), time-series (wide-column), or graph-shaped.

#### Pick SQL when:

- You need rich ad-hoc queries, joins, and OLTP transactions across multiple tables.

- Strong consistency and constraints are central to correctness.

Often the answer is both: OLTP in Postgres + analytics/time-series in a NoSQL engine.

### Common pitfalls (and fixes)

- Hot partitions / uneven keys → choose higher-cardinality partition keys; add salt or time-bucketing.

- Modeling like SQL → in NoSQL, start from queries, not entities; denormalize intentionally.

- Unbounded arrays/documents → cap list sizes; split to child collections/partitions.

- Full scans → add indexes/GSIs or precompute views; avoid Scan/collection sweeps in hot paths.

- Write amplification from transactions → keep operations idempotent; prefer upserts.


### Quick chooser (cheat sheet)

Create a markdown table with two columns: Use case and Good fit. Fill in the rows with the following data:

| Use case                          | Good fit                                   |
|-----------------------------------|--------------------------------------------|
| Session cache, counters, queues   | Redis, DynamoDB                            |
| Product catalog with search facets| MongoDB (documents + compound indexes)     |
| High-ingest time-series / events  | Cassandra / ClickHouse (analytics)         |
| Global low-latency reads/writes   | DynamoDB (multi-region) / Cassandra        |
| Relationship-heavy queries        | Neo4j / Neptune                            |

---

## 💪 ACID Properties: Reliability You Can Trust

ACID is a set of properties that guarantee reliable database transactions:

- Atomicity: All operations succeed or none do.
- Consistency: Data remains valid after transactions.
- Isolation: Concurrent transactions don't interfere.
- Durability: Committed data persists even after crashes.

Relational databases excel at enforcing ACID properties, which are critical for financial systems, order processing, and anywhere data integrity matters.

🔹 **Tip:** In distributed systems, understand when relaxing ACID is acceptable for performance gains (e.g., eventual consistency).

`ACID` describes how a database should execute transactions so your data stays correct even under failures and concurrency.

### A — Atomicity (all-or-nothing)

A transaction’s changes are applied entirely or not at all.

- In Postgres: BEGIN … COMMIT applies; ROLLBACK undoes all.

- Errors inside a txn put it into an aborted state; either ROLLBACK or use savepoints to recover part-way.

- DDL is transactional in Postgres (rare in other DBs): schema changes roll back too.

```sql
-- Example: money transfer with a savepoint
BEGIN;
SAVEPOINT before_debit;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- if a check fails, we can rollback to the savepoint instead of the whole txn
-- ROLLBACK TO SAVEPOINT before_debit;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

### C — Consistency (valid state → valid state)

A transaction must move the database from one valid state to another, according to constraints you define.

- Use PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, and EXCLUSION constraints to encode invariants.

- Postgres can defer some checks to the end of the transaction: `DEFERRABLE INITIALLY DEFERRED`.

```sql
CREATE TABLE orders (
id BIGSERIAL PRIMARY KEY,
customer_id BIGINT REFERENCES customers(id) DEFERRABLE INITIALLY DEFERRED,
status TEXT CHECK (status IN ('new','paid','shipped','cancelled'))
);
-- All FKs are checked at COMMIT time; useful for multi-row upserts.
```

**Consistency ≠ “business correctness” by itself. The DB enforces what you encode; model your rules as constraints/triggers to get real guarantees.**


### I — Isolation (concurrent safety)

Concurrent transactions shouldn’t step on each other. Postgres uses MVCC (multi-version concurrency control): readers don’t block writers; writers don’t block readers (most of the time).

Postgres isolation levels (default READ COMMITTED):

| Level           | Phenomena prevented                              | Notes                                                                                                                                      |
|-----------------|---------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| READ COMMITTED  | Dirty reads                                       | Each statement sees a fresh snapshot. Rows changed by concurrent transactions may appear/disappear between statements.                     |
| REPEATABLE READ | Dirty + non-repeatable reads; most phantoms       | Snapshot fixed for the whole transaction (aka snapshot isolation). Can still have write skew.                                             |
| SERIALIZABLE    | All above + write skew                            | Detects anomalies (SSI) and may abort with `40001 serialization_failure` — you must retry.                                                |

Locking primitives (pair with MVCC when needed):

```sql
-- Claim a job row without blocking others
UPDATE jobs
SET claimed_by = :worker, claimed_at = now()
WHERE id = (
SELECT id FROM jobs
WHERE claimed_at IS NULL
ORDER BY priority DESC, created_at
FOR UPDATE SKIP LOCKED
LIMIT 1
)
RETURNING *;


-- Protect a row you will update soon
SELECT * FROM accounts WHERE id = 1 FOR UPDATE NOWAIT; -- error if locked
```

### D — Durability (it sticks)

Once COMMITTED, data survives crashes.

- Postgres writes to the WAL (Write-Ahead Log) and fsyncs to disk.

- synchronous_commit = on (default) waits for WAL flush; remote_apply can wait for replicas.

- Turning off fsync or using synchronous_commit = off risks data loss on crash — OK for throwaway dev, not prod.

```sql
-- Visibility knobs (know what they do before changing)
SHOW synchronous_commit; -- on by default
SHOW wal_level; -- replica/logical for replication/CDC
```

### Putting ACID together: a safe pattern

```sql
-- Pattern: retry on serialization/conflict
DO $$
DECLARE
tries int := 0;
BEGIN
<<retry>>
BEGIN
tries := tries + 1;
-- choose isolation level suitable for invariants
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;


-- business logic here
UPDATE inventory SET stock = stock - 1 WHERE sku = 'A' AND stock > 0;
IF NOT FOUND THEN RAISE EXCEPTION 'Out of stock'; END IF;


COMMIT;
EXCEPTION WHEN serialization_failure THEN
ROLLBACK;
IF tries < 3 THEN PERFORM pg_sleep(0.01 * tries); GOTO retry; END IF;
RAISE; -- give up
WHEN OTHERS THEN
ROLLBACK; RAISE;
END;
END$$;
```

Guidelines

- Default to READ COMMITTED; use REPEATABLE READ for consistent analytical reads; use SERIALIZABLE to protect complex invariants (and be ready to retry).

- Keep transactions short to reduce contention and bloat.

- Prefer idempotent writes (e.g., INSERT … ON CONFLICT DO NOTHING/UPDATE) to handle retries safely.

### ACID in distributed systems

A single-node ACID DB can’t make a network reliable. Across services you typically trade strict ACID for availability/latency.

Common patterns:

- Outbox/Inbox: write domain change + message to an outbox atomically; a relay publishes from the DB. Consumers write to an inbox table to get idempotency.

- Sagas: break a business txn into steps with compensations (undo actions) — eventual consistency.

- 2PC (Two-Phase Commit): strong consistency across resources but operationally fragile; avoid unless you fully control all participants.

- Idempotency keys: ensure retried requests don’t duplicate side effects.

Rule of thumb: keep ACID for your core DB boundary; use idempotent, retryable workflows between services and accept eventual consistency where user experience allows.


### Quick ACID checklist (Postgres)

- Wrap multi-statement changes in `BEGIN … COMMIT`.

- Encode invariants as constraints; use DEFERRABLE when needed.

- Use proper isolation; retry on 40001 at SERIALIZABLE.

- Use `SELECT … FOR UPDATE [SKIP LOCKED|NOWAIT]` for queues/contention hotspots.

- Monitor WAL/replication; don’t disable `fsync` in prod.

---

## 📝 Database Normalization: Design for Integrity

Normalization organizes data to reduce redundancy and improve integrity.

Key normal forms:

- **1NF**: Eliminate repeating groups.
- **2NF**: Remove partial dependencies.
- **3NF**: Remove transitive dependencies.

While normalization ensures clean data design, sometimes selective denormalization is necessary for performance reasons in read-heavy systems.

🔹 **Tip:** Normalize for clarity, denormalize for performance — based on access patterns.

### 📝 Database Normalization: Design for Integrity

Normalization is the discipline of structuring tables so each fact is stored once and in the right place. Done well, it prevents data anomalies (bugs) and keeps writes simple and safe.

Why normalize? To avoid:

- Update anomaly – you change a product’s name in one row but forget others.

- Insert anomaly – you can’t add a new product until an order exists.

- Delete anomaly – removing the last order for a product also erases the only copy of the product’s data.


#### Functional dependencies (intuitive view)

If knowing X lets you determine Y, we write X → Y.
Examples:

- customer_id → {customer_name, email}

- product_id → {product_name, unit_price}

- (order_id, product_id) → {qty}

Normalization applies these rules to table design.

#### 1NF — First Normal Form

Rows are unique, columns are atomic (no arrays/CSV-in-a-cell), and order doesn’t matter.

- Fix: move repeating groups to their own rows.

- Smelly design (repeating groups):

```scss
orders(order_id, customer_id, items_sku_csv, items_qty_csv, ... )
```

`1NF` shape (atomic rows):

```scss
orders(order_id, customer_id, ordered_at, status)
order_items(order_id, product_id, qty)
```

#### 2NF — Second Normal Form

- Applies when a table’s key is composite (e.g., (order_id, product_id)).

- Every non-key column must depend on the whole key, not just part of it.

Smelly design:

```scss
order_items(order_id, product_id, qty, product_name, unit_price_current)
-- product_* depend only on product_id (part of the key) → violates 2NF
```

`2NF` fix: split product attributes out:

```scss
products(product_id PRIMARY KEY, product_name, unit_price_current)
order_items(order_id, product_id, qty, PRIMARY KEY(order_id, product_id))
```

#### 3NF — Third Normal Form

- Non-key columns must depend only on the key (no transitive dependencies).

- If order_id → customer_id and customer_id → customer_email, then order_id → customer_email is transitive and shouldn’t live in orders.

Smelly design:

```scss
orders(order_id, customer_id, customer_email, ordered_at)
```

`3NF` fix:

```scss
customers(customer_id PRIMARY KEY, name, email)
orders(order_id PRIMARY KEY, customer_id REFERENCES customers, ordered_at)
```

#### (Bonus) BCNF, 4NF, 5NF — when things get tricky

- `BCNF`: a stronger 3NF; whenever a dependency X → Y holds, X must be a key. Use when multiple candidate keys create odd dependencies.

- `4NF`: eliminates multi-valued dependencies (e.g., artist has multiple instruments and multiple genres → use two separate link tables).

- `5NF`: decomposes tables so all joins are lossless; rarely needed outside complex M:N:N relationships.

#### Worked example (from “all-in-one” to normalized)

Start (denormalized facts mixed together):

```scss
orders_flat(
  order_id, ordered_at,
  customer_id, customer_name, customer_email,
  product_id, product_name, unit_price_current, qty
)
```

Normalize → canonical OLTP model:

```scss
CREATE TABLE customers(
  customer_id BIGINT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE
);

CREATE TABLE products(
  product_id BIGINT PRIMARY KEY,
  name TEXT NOT NULL,
  unit_price_cents INT NOT NULL CHECK (unit_price_cents >= 0)
);

CREATE TABLE orders(
  order_id BIGINT PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customers(customer_id),
  ordered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  status TEXT NOT NULL CHECK (status IN ('new','paid','shipped','cancelled'))
);

CREATE TABLE order_items(
  order_id BIGINT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
  product_id BIGINT NOT NULL REFERENCES products(product_id),
  qty INT NOT NULL CHECK (qty > 0),
  unit_price_cents INT NOT NULL,           -- snapshot at purchase time
  PRIMARY KEY(order_id, product_id)
);
```

**Why the unit_price_cents copy in order_items?**

Normalization doesn’t forbid capturing a historical snapshot. Prices change; you still need the price that applied at checkout to compute totals later. This is a legit denormalization for history, not a smell.

#### Postgres tools that help enforce normalization

- Foreign keys with actions: ON DELETE CASCADE/RESTRICT, DEFERRABLE INITIALLY DEFERRED for multi-row transactions.

- Unique constraints / composite keys to model natural identities.

- CHECK constraints for business rules (status IN (...), positive amounts).

- Partial unique indexes to scope rules (e.g., unique SKU per active catalog).

- Exclusion constraints for scheduling overlaps (via btree_gist).

#### When (and how) to denormalize safely

Normalize your write path, then denormalize your read path when profiling shows hot queries need it.

Common, safe patterns:

- Materialized views: precompute aggregates; refresh on schedule.

- Summary tables updated by jobs/triggers (e.g., daily revenue per product).

- Star schema in analytics (facts + dimensions) while OLTP remains 3NF.

- Selective duplication (e.g., orders.total_cents) maintained by trigger or app logic.

- JSONB columns for truly sparse, non-relational attributes—but index extracted fields you query (CREATE INDEX ... ( (props->>'color') )).

Trade-offs: faster reads vs. risk of drift. Always document the single source of truth and how denormalized fields are refreshed.

#### One-minute normalization checklist

- `Key`: What uniquely identifies a row? (Write it down.)

- `FDs`: List obvious dependencies (e.g., product_id → name, price).

- `1NF`: Any arrays/CSV/duplicate groups in a row? Split to rows.

- `2NF`: With composite keys, does every non-key depend on the whole key?

- `3NF`: Any non-key depending on another non-key? Move it out.

- `Integrity`: Add PKs, FKs, UNIQUE, CHECKs.

- `Performance`: Add indexes that match your most common WHERE/JOIN/ORDER BY.

Normalize for correctness; denormalize deliberately for speed with clear ownership and refresh logic.

---

## 🔄 Wrapping Up

Understanding databases isn't just about memorizing SQL queries. It’s about knowing how data structures (like B-Trees), transaction guarantees (ACID), and design principles (normalization) affect your application’s performance, reliability, and scalability.

Whether you're architecting a high-availability service or fine-tuning a reporting dashboard, strong database knowledge will elevate your solutions.

---

🚀 Follow me on [norbix.dev](https://norbix.dev) for more insights on Go, Python, AI, system design, and engineering wisdom.
