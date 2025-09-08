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

```sql
-- All books with author info
SELECT b.title, a.name AS author, a.country, b.year, b.price_usd
FROM books b
JOIN authors a ON a.author_id = b.author_id
ORDER BY a.name, b.year;
```

#### Aggregation

Aggregate functions summarize data: `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`.

```sql
-- Avg price by country; only countries with ≥2 books
SELECT a.country,
       ROUND(AVG(b.price_usd), 2) AS avg_price,
       COUNT(*) AS books
FROM books b
JOIN authors a ON a.author_id = b.author_id
GROUP BY a.country
HAVING COUNT(*) >= 2
ORDER BY avg_price DESC;
```

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

### Common pitfalls (Postgres)

- Strings use single quotes ('PL'). Double quotes are identifiers.

- NULL logic: use IS NULL / IS NOT NULL; = NULL is never true.

- Integer division: 1/2 = 0. Cast for rates: sum(x)::numeric / nullif(count(*),0).

- All non-aggregated SELECT columns must appear in GROUP BY.

- Prefer window functions for “top-k per group” and “rolling” metrics.

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

---

## 💪 ACID Properties: Reliability You Can Trust

ACID is a set of properties that guarantee reliable database transactions:

- Atomicity: All operations succeed or none do.
- Consistency: Data remains valid after transactions.
- Isolation: Concurrent transactions don't interfere.
- Durability: Committed data persists even after crashes.

Relational databases excel at enforcing ACID properties, which are critical for financial systems, order processing, and anywhere data integrity matters.

🔹 **Tip:** In distributed systems, understand when relaxing ACID is acceptable for performance gains (e.g., eventual consistency).

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
