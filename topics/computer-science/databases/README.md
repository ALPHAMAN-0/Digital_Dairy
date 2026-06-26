---
title: Databases — Learning Roadmap
date: 2026-06-25
tags: [databases, sql, nosql, vector, roadmap]
source: self-study
status: growing
---

# 🗄️ Databases — Learning Roadmap (Basic → Advanced)

Three families of databases, each with its own basic→advanced path. Tick the boxes as you learn.

- 🟦 [Relational databases (SQL)](relational-databases.md)
- 🟩 [Non-relational databases (NoSQL)](non-relational-databases.md)
- 🟪 [Vector databases](vector-databases.md)

## How the three compare

| | Relational (SQL) | Non-relational (NoSQL) | Vector |
|---|---|---|---|
| **Data model** | Tables: rows + columns, fixed schema | Document / key-value / wide-column / graph | High-dimensional vectors (embeddings) + metadata |
| **Query style** | SQL with joins | API/query per type; joins rare | Similarity search (nearest neighbor) |
| **Best at** | Integrity, complex queries, transactions | Horizontal scale, flexible schema, high throughput | Semantic search, AI / RAG, recommendations |
| **Consistency** | ACID | BASE / tunable | Varies (usually eventual) |
| **Examples** | PostgreSQL, MySQL, SQLite | MongoDB, Redis, Cassandra, Neo4j | Pinecone, Milvus, Qdrant, pgvector |
| **Reach for it when** | Structured data with relationships + transactions | Huge scale, evolving schema, known access patterns | "Find things similar to this" / AI search |

## Recommended order

1. **Relational first** — it teaches the core ideas (schema, keys, transactions, querying) that
   everything else reacts to.
2. **Then NoSQL** — you'll understand *why* it relaxes relational rules (scale, flexibility).
3. **Then Vector** — newest, often layered on the others (e.g. `pgvector` is just Postgres),
   and the gateway to AI / RAG.

> 💡 These pair well with a goal — add **"Learn Databases"** to [planner/goals.md](../../../planner/goals.md)
> and let the checkboxes here drive its progress bar.

## One book to rule them all

📘 *Designing Data-Intensive Applications* — Martin Kleppmann ("DDIA"). The single best resource
that ties relational, NoSQL, and distributed-systems concepts together. Read it alongside any track.
