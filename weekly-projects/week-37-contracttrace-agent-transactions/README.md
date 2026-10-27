# Week 37 — ContractTrace: Verified Agent Tool Transactions

**Tuesday AI/ML engineering portfolio | 2026-10-27 | Python 3.11+ | MIT-style example code**

## Business problem
Tool-using AI agents can report successful actions when the database was not changed, retry successful operations after losing an acknowledgment, or violate authorization and inventory invariants. ContractTrace separates **proposals** from **execution authority** and evaluates actual final state rather than trusting the agent or tool's natural-language answer. Retail inventory, airline baggage services, IT ticketing, procurement and order fulfillment share these problems.

## What is implemented
- Strict structured command schema, allowlisted actions, trusted actor/tenant binding, and approval policy.
- Optional local llama.cpp-compatible JSON proposal adapter; deterministic planner is the reproducible baseline.
- Atomic SQLite inventory reservation, release and shipment state machine; idempotent receipts.
- Before-commit and after-commit fault injection; replay-safe recovery from lost acknowledgments.
- SHA-256 hash-chained audit events, receipt checks, state-hash comparison and accounting invariants.
- Concurrency stress test that proves no overselling in the local SQLite workload.
- FastAPI gateway; pytest suite; benchmark report; sample commands and synthetic fixtures.

## Local architecture
`Intent -> deterministic planner OR optional local SLM -> strict schema -> trusted identity/policy -> transactional gateway -> SQLite inventory/orders/receipts/audit -> state oracle`. No external calls or GPU are required for core verification. The SLM cannot authorize actions, set tenant/actor identity, or bypass the gateway.

## Setup (Windows PowerShell)
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH='src'
python -m contracttrace.cli seed --quantity 20
python -m contracttrace.cli act --text 'reserve 2 units of PART-A for O1' --request-id req-001
python -m contracttrace.cli verify
python -m contracttrace.cli snapshot
python -m contracttrace.cli benchmark --output reports/benchmark.json
pytest -q tests
```
Linux/macOS: `python3 -m venv .venv; source .venv/bin/activate; pip install -r requirements.txt; export PYTHONPATH=src`.

## API
Set a random `CONTRACTTRACE_API_KEY` and `CONTRACTTRACE_DB`, then run `uvicorn contracttrace.api:app --host 127.0.0.1 --port 8000`. `POST /execute` requires `X-API-Key`, body `{"request_id":"req-002","text":"reserve 1 PART-A for O2"}`. The demo gateway intentionally binds `tenant=demo, actor=alice`; production must authenticate principals with OIDC and retrieve policy roles server-side.

## Optional free local model
Run an OpenAI-compatible llama.cpp server on loopback using a legitimately licensed 0.5–1.5B GGUF instruction model with CPU inference or 4-bit quantization. Call `local_llm_proposal(text)` then `bind_proposal(proposal, tenant=..., actor=..., request_id=...)`, and finally `Gateway.execute(command, roles)`. No model download or paid API is required to reproduce tests. Never grant the model direct DB access. An LLM can hallucinate valid-looking actions: the policy gate remains mandatory.

## Experiment design
1. **Correctness:** reserve/ship/release state transitions, permissions, approval, tenant isolation.
2. **Retry safety:** inject failure before commit and lost acknowledgment after commit; compare final state.
3. **Concurrency:** 30 simultaneous requests for 10 available items; verify exactly 10 accepted and no negative inventory.
4. **Integrity:** tamper with an audit hash or live inventory and verify detection.
5. **Optional local SLM:** compare JSON validity, action accuracy, end-state success and P95 latency against deterministic planner on held-out user phrasing; do not claim this benchmark until executed.

## Benchmarks
Run `python -m contracttrace.cli benchmark --output reports/benchmark.json`. Synthetic scenarios are deterministic, but wall-clock timings vary. Scenario pass rate measures these fixtures, not a frontier-model benchmark. The report includes nine action attempts (including retries), six committed audit events, and concurrency throughput. No external LLM performance is claimed.

## Hardware
Ryzen 7 4800-series, 16 GB RAM: core reference implementation usually <100 MB process RAM, no GPU. Optional local 0.5–1.5B 4-bit model may use 1–3 GB RAM/VRAM depending on model/context; prefer CPU if GTX 1650 Ti 4 GB is busy. Database serializes writes, so benchmark latency is not a production throughput prediction.

## Threat model and limitations
Prevents accidental duplicate inventory mutations, basic unauthorized operations, and inconsistent state. Does not establish cryptographic nonrepudiation: SHA-256 hashes can be recomputed by a DB administrator. Production needs signed external audit checkpoints and IAM. Does not execute arbitrary shell/HTTP tools, validate real human approvals, protect against compromised process identity, or evaluate real LLMs. Local SQLite is not a multi-region transactional database. Approval bool is a fixture; production requires approval evidence signed by an independent service.

## Senior engineering discussion
Why do end-state assertions beat tool-message grading? Why are idempotency keys scoped per tenant and bound to payload digests? What happens when the database commits but the network response is lost? Why must inference happen outside transactions? How would you migrate from SQLite to Postgres with serializable inventory operations, durable outbox, and audit anchoring?

## Resume bullet
**Architected and benchmarked a transactionally verified AI-agent tool-execution gateway with strict action contracts, idempotent retries, role/approval policies, hash-chained audit evidence, fault injection, concurrency invariants, state-based evaluation and optional local SLM planning; designed a horizontally scalable production migration with durable queues, signed audits and multi-tenant isolation.**

## References
See `references.md`. This project is an independent engineering adaptation of the executable-contract evaluation and runtime authorization themes in 2026 research, not a reproduction of reported benchmark results.
