---
title: Relational Databases (SQL) — Roadmap
date: 2026-06-25
tags: [databases, sql, relational, rdbms, roadmap]
source: self-study
status: seedling
---

# 🟦 Relational Databases (SQL) — Roadmap

## TL;DR
> Data lives in **tables** (rows + columns) with a fixed **schema** and explicit
> **relationships** between them. You query it with **SQL**, and it guarantees **ACID**
> transactions. The default choice when data is structured and correctness matters.

**When to use:** structured data, clear relationships, transactions (banking, orders, users),
strong consistency, complex reporting queries.

---

## Stage 1 — Foundations 🌱
- [ ] What an RDBMS is, and why tables/relations
- [ ] Tables, rows (records), columns (fields), data types
- [ ] **Primary key**, **foreign key**, unique & not-null constraints
- [ ] Relationships: one-to-one, one-to-many, many-to-many (junction tables)
- [ ] Entity–Relationship Diagrams (ERD)
- [ ] Core SQL: `SELECT`, `INSERT`, `UPDATE`, `DELETE`
- [ ] Filtering & sorting: `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`
- [ ] Pick a database to practice in: **PostgreSQL** or **SQLite**

## Stage 2 — Core / Intermediate 🌿
- [ ] **Joins**: inner, left/right/full outer, cross, self-join
- [ ] Aggregation: `GROUP BY`, `HAVING`, `COUNT/SUM/AVG/MIN/MAX`
- [ ] Subqueries and correlated subqueries
- [ ] **Normalization**: 1NF, 2NF, 3NF, BCNF (and why denormalize sometimes)
- [ ] **Indexes**: what a B-tree index is, when it helps, the cost on writes
- [ ] **Transactions & ACID** (Atomicity, Consistency, Isolation, Durability)
- [ ] Views, and the basics of stored procedures & triggers
- [ ] Constraints in depth: `CHECK`, `DEFAULT`, cascading deletes

## Stage 3 — Advanced 🌳
- [ ] **Query optimization**: read `EXPLAIN` / execution plans
- [ ] Indexing strategy: composite, covering, partial indexes; index selectivity
- [ ] **Isolation levels** & anomalies (dirty/non-repeatable reads, phantoms)
- [ ] Concurrency control: locking vs **MVCC**
- [ ] **Window functions** and **CTEs** (`WITH`, recursive CTEs)
- [ ] Partitioning, **sharding**, and read **replication**
- [ ] Backups, point-in-time recovery, connection pooling
- [ ] CAP theorem & **NewSQL** (CockroachDB, Google Spanner) for distributed SQL

## Hands-on
- [ ] Design + build a small schema (e.g. a library or e-commerce DB) with proper keys
- [ ] Write 10 increasingly hard queries (joins → aggregates → window functions)
- [ ] Add indexes and measure a query's plan before vs after

## Resources
- **SQLBolt** / **Mode SQL Tutorial** — interactive SQL basics
- **CMU 15-445 Intro to Database Systems** (Andy Pavlo, free on YouTube) — the internals
- **Use The Index, Luke!** — indexing & performance
- **PostgreSQL official docs** — the gold-standard reference
- 📘 *Designing Data-Intensive Applications*

## Related
- [[non-relational-databases]]
- [[vector-databases]]
