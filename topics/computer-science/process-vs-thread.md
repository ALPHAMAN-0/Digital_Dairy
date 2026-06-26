---
title: "Process vs Thread"
date: 2026-06-25
tags: ["operating-systems", "concurrency"]
source: "AIUB - Operating Systems"
status: growing
---

# Process vs Thread

## TL;DR
> A process is an independent program with its own memory; threads are lightweight units that share their process's memory.

## Key differences

| | Process | Thread |
|---|---|---|
| Memory | Own address space | Shared within the process |
| Creation cost | High | Low |
| Crash impact | Isolated | Can take down the whole process |

## Why it matters
Threads make concurrency cheap because they share memory, but that sharing is exactly why you need synchronization (locks, mutexes) to avoid race conditions.
