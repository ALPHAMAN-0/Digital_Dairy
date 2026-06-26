---
title: Vector Databases — Roadmap
date: 2026-06-25
tags: [databases, vector, embeddings, ann, rag, ai, roadmap]
source: self-study
status: seedling
---

# 🟪 Vector Databases — Roadmap

## TL;DR
> A vector database stores **embeddings** — lists of numbers that capture the *meaning* of text,
> images, or audio — and finds the ones **most similar** to a query vector. It's the engine
> behind semantic search, recommendations, and **RAG** (giving LLMs external knowledge).

**When to use:** "find things similar to this", semantic/meaning-based search, recommendation,
and retrieval-augmented generation for AI apps.

---

## Stage 1 — Foundations 🌱
- [ ] What a **vector / embedding** is, and how a model turns text/images into one
- [ ] Why exact keyword search fails and **semantic** search wins
- [ ] **Dimensionality** (e.g. 384, 768, 1536-dim vectors)
- [ ] **Similarity metrics**: cosine similarity, dot product, Euclidean (L2) distance
- [ ] Generate embeddings with a model and store them (start with **Chroma** or **pgvector**)
- [ ] Do a first **k-nearest-neighbor (kNN)** search

## Stage 2 — Core / Intermediate 🌿
- [ ] **Exact vs Approximate Nearest Neighbor (ANN)** — and the recall/latency trade-off
- [ ] ANN index algorithms:
  - [ ] **HNSW** (graph-based — the common default)
  - [ ] **IVF** (inverted file / clustering)
  - [ ] **LSH**, and product-quantization variants (**IVF-PQ**)
- [ ] **Metadata filtering** (combine "similar to X" with `where category = ...`)
- [ ] **Hybrid search**: dense vectors + sparse/keyword (BM25) together
- [ ] **Chunking** strategy for documents (size, overlap) before embedding
- [ ] Compare the tools: Pinecone, Weaviate, Milvus, Qdrant, pgvector, FAISS (library)

## Stage 3 — Advanced 🌳
- [ ] **Quantization** to shrink memory: scalar & product quantization (PQ)
- [ ] Tuning **HNSW** (`M`, `ef_construction`, `ef_search`) and **IVF** (`nlist`, `nprobe`)
- [ ] Sharding & replication of vector indexes; scaling to billions of vectors
- [ ] **Reranking** (cross-encoders) after the first retrieval pass
- [ ] End-to-end **RAG pipeline**: ingest → chunk → embed → retrieve → rerank → prompt
- [ ] **Evaluation**: measuring recall, and retrieval quality (precision@k, faithfulness)
- [ ] Multi-tenancy, freshness/updates, and cost trade-offs in production

## Hands-on
- [ ] Build a "chat with your notes/PDF" RAG app over this very diary
- [ ] Compare HNSW vs IVF on the same data — measure recall and query latency
- [ ] Add metadata filtering + hybrid (keyword + vector) search

## Resources
- **Pinecone Learning Center** — clear explainers on embeddings, ANN, and RAG
- **HNSW paper** — Malkov & Yashunin (the algorithm behind most vector indexes)
- **FAISS docs / wiki** (Meta) — the foundational similarity-search library
- **pgvector** (github.com/pgvector/pgvector) — vectors inside PostgreSQL
- Embedding model docs (e.g. OpenAI / Sentence-Transformers) for generating vectors

## Related
- [[relational-databases]]
- [[non-relational-databases]]
