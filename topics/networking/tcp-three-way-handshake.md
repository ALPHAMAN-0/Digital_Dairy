---
title: TCP Three-Way Handshake
date: 2026-06-25
tags: [networking, tcp, protocols, transport-layer]
source: self-study
status: growing
---

# TCP Three-Way Handshake

## TL;DR
> Before TCP sends any real data, the two sides exchange three packets (SYN → SYN-ACK → ACK)
> to agree on starting sequence numbers and confirm both can send *and* receive. It's a
> "can you hear me? — yes, can you hear me? — yes" before the real conversation.

## What it is
The handshake that **opens** a TCP connection. Both sides synchronize their initial sequence
numbers (ISN) and confirm the link is two-way before any application data flows.

## Why it matters
TCP is *reliable and ordered*. That guarantee only works if both ends agree on where the byte
numbering starts. The handshake establishes that shared state — and proves the path works in
both directions.

## How it works
1. **SYN** — Client picks a random ISN (say `x`) and sends a segment with the `SYN` flag set
   and `seq = x`. ("I want to talk; my numbering starts at x.")
2. **SYN-ACK** — Server picks its own ISN (`y`), replies with `SYN` + `ACK`, `seq = y`,
   `ack = x + 1`. ("Got it. My numbering starts at y, and I expect x+1 next.")
3. **ACK** — Client replies with `ACK`, `seq = x + 1`, `ack = y + 1`. ("Confirmed.")

After step 3 the connection is **ESTABLISHED** and data can flow.

## Example
```text
Client                         Server
   |  ---- SYN  seq=x ------->   |
   |  <-- SYN,ACK seq=y ack=x+1  |
   |  ---- ACK  ack=y+1 ----->   |
   |        [ ESTABLISHED ]      |
```

## Gotchas / things I got wrong
- It's **not** the same as the connection *teardown* — closing uses a separate FIN/ACK
  exchange (often four packets).
- The ISN is randomized on purpose (security — makes sequence prediction attacks harder),
  not always 0.
- A `SYN` flood attack abuses step 1: sending many SYNs and never completing step 3 to exhaust
  the server's half-open connection table.

## Related
- [[tcp-connection-teardown]]
- [[tcp-ip-model]]

## Sources
- RFC 9293 (TCP)
- Kurose & Ross, *Computer Networking: A Top-Down Approach*
