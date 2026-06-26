---
title: Non-Relational Databases (NoSQL) — Roadmap
date: 2026-06-25
tags: [databases, nosql, mongodb, redis, cassandra, roadmap]
source: self-study
status: seedling
---

# 🟩 Non-Relational Databases (NoSQL) — Roadmap

## TL;DR
> "NoSQL" = databases that drop the fixed-table relational model for **flexible schemas** and
> **horizontal scale**. Comes in four main flavours — document, key-value, wide-column, graph —
> each tuned for different access patterns. Often trades strict consistency (ACID) for
> availability and speed (**BASE**).

**When to use:** massive scale, rapidly evolving or unstructured data, very high write
throughput, or a specific access pattern that maps cleanly to one model.

---

## Stage 1 — Foundations 🌱
- [ ] Why NoSQL exists (scale, schema flexibility, developer speed) — and its trade-offs
- [ ] The four families and a flagship for each:
  - [ ] **Document** — MongoDB (JSON-like documents)
  - [ ] **Key-value** — Redis, DynamoDB
  - [ ] **Wide-column** — Cassandra, HBase
  - [ ] **Graph** — Neo4j (nodes + edges)
- [ ] Flexible / schema-on-read vs schema-on-write
- [ ] **ACID vs BASE**; the **CAP theorem** (Consistency, Availability, Partition tolerance)
- [ ] Basic CRUD in one document store (start with **MongoDB**)

## Stage 2 — Core / Intermediate 🌿
- [ ] Data modeling for NoSQL: **embedding vs referencing**; model around *queries*, not entities
- [ ] Denormalization and duplication as a deliberate strategy
- [ ] **Partitioning / sharding** and choosing a good partition key
- [ ] **Replication** and replica sets
- [ ] Consistency models: strong, eventual, **tunable/quorum**
- [ ] Indexing in NoSQL; secondary indexes; TTL (auto-expiry)
- [ ] MongoDB **aggregation pipeline**; Redis data structures (lists, sets, sorted sets, streams)

## Stage 3 — Advanced 🌳
- [ ] Distributed-systems core: **consistent hashing**, quorum reads/writes (**N / R / W**)
- [ ] Conflict resolution: last-write-wins, **vector clocks**, **CRDTs**
- [ ] Multi-region / geo-distribution and latency trade-offs
- [ ] **Polyglot persistence** — using several databases for different jobs in one system
- [ ] Specialized stores: **time-series** (InfluxDB, TimescaleDB), **search** (Elasticsearch / OpenSearch)
- [ ] Capacity planning, hot-partition problems, and performance tuning
- [ ] Knowing when NOT to use NoSQL (and reaching back for relational)

## Hands-on
- [ ] Model the same app (e.g. a blog) in MongoDB and compare with a relational design
- [ ] Use Redis as a cache + a leaderboard (sorted set) in front of another DB
- [ ] Design a Cassandra table starting from the query you need to serve

## Resources
- **MongoDB University** (free courses) — document modeling done right
- **Redis docs / Try Redis** — key-value + data structures
- **DynamoDB single-table design** talks (Rick Houlihan) — advanced modeling
- 📘 *Designing Data-Intensive Applications* — the consistency/replication chapters are essential

## Related
- [[relational-databases]]
- [[vector-databases]]
