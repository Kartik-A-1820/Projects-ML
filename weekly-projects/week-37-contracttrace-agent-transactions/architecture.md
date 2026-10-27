# ContractTrace — Architecture and Production Scaling

## 1. Problem, boundary and correctness contract
Agent tool outputs are not proof that a requested state change occurred. ContractTrace makes the final state and durable receipt authoritative. A model proposes an action; the runtime validates identity, authorization, schema, preconditions and postconditions. The core correctness property is **each (tenant, request_id, payload) produces at most one durable state transition**. A reused idempotency key with a different payload is rejected. A retry after a lost acknowledgement returns the original receipt.

## 2. Local design
```text
User intent -> deterministic parser / optional local GGUF SLM
            -> typed proposal -> trusted actor/tenant binding
            -> authorization + approval gate
            -> SQLite BEGIN IMMEDIATE
            -> state-machine preconditions -> inventory mutation
            -> invariants -> receipt + audit event in SAME transaction
            -> COMMIT -> response
            -> independent state oracle / replay verification
```
Data tables: inventory(tenant,sku,available,reserved); orders(tenant,order_id,sku,quantity,status); receipts(tenant,request_id,command_hash,response); audit(seq,tenant,event,prev_hash,event_hash). Synthetic data only. The model never receives database credentials. Optional llama.cpp HTTP proposal endpoint is restricted to loopback. All test scenarios run without a model.

## 3. ADRs (architectural decisions)
- **ADR-001 SQLite for laptop:** zero infrastructure, ACID semantics, cheap tests; **not** distributed write scaling. Migrate to PostgreSQL for production.
- **ADR-002 strict schema:** a typed command is less flexible than arbitrary tool execution but blocks unknown operations and hidden parameters.
- **ADR-003 state oracle:** verify inventory/order state rather than trusting a model's text or tool ACK; costs extra reads but detects silent errors.
- **ADR-004 request-key+payload digest:** supports safe retries and conflict detection; requires retention policy aligned to retry window.
- **ADR-005 model outside transaction:** no LLM inference under DB lock; reduces lock contention and avoids nondeterministic transactions.
- **ADR-006 audit hash chain:** tamper-evident against accidental modifications, not malicious DBA with full control. Production uses external signed checkpoints.
- **ADR-007 no GPU by default:** rule planner proves transaction correctness independently of model quality. Optional local SLM evaluated separately.
- **ADR-008 fail-closed approvals:** local boolean is only a fixture; production approval must be independently authenticated and signed.

## 4. Evaluation protocol and acceptance gates
The benchmark runs nine scripted action attempts: normal reserve, replay, ship, insufficient stock, unauthorized actor, pre-commit failure, retry, post-commit lost ACK, retry. Success is asserted using state, receipt, audit and invariants. Concurrency test submits 30 one-item reservations for 10 available units, expecting 10 commits, 20 rejections and zero overselling. The benchmark does not claim general LLM task success. Optional model experiment measures schema validity, action correctness, state success, P50/P95 latency and cost per successful action over independently labeled paraphrases. Regression gate: 100% invariant preservation and no unauthorized mutations; utility metrics compared to a pinned baseline.

## 5. Production Scaling Architecture

### 5.1 State separation
Separate stateless inference/planning, policy decision, transactional execution, orchestration and immutable audit. Store workflow state and idempotency in PostgreSQL, event streams in Kafka/Redpanda, and artifacts in S3-compatible object storage. Do not store authorization in model prompts. Version commands, contracts and policies independently.

### 5.2 Horizontal and vertical scaling
Scale API/planner replicas horizontally behind ingress. Partition executor workers by tenant and aggregate key; maintain serializable row locks for SKU/order conflicts. Scale DB vertically for hot write workloads and read replicas for observability, never for authoritative writes. Use consistent hashing or work queues for hot partitions.

### 5.3 GPU serving and inference optimization
Optional small SLM via llama.cpp on CPU or 4-bit 4 GB VRAM; production may use vLLM/Triton for larger models. Dynamic batching, prefix/KV caching, quantization and request length limits reduce serving costs. Batch **inference**, not unrelated database commits. Track parse validity and end-state utility after model quantization. Provide deterministic parser fallback on model outage.

### 5.4 Batching, caching, context design
Cache read-only catalog/schema and policy versions with TTL; never cache stale inventory as authoritative. Context packets include tool schema, permitted action names and only required entity fields. Never let retrieved text modify authorization. Invalidate cache on stock changes and policy version updates. Use bounded prompt/context budgets and reject oversized requests.

### 5.5 Queues, transactional outbox, databases
PostgreSQL serializable or `SELECT FOR UPDATE` inventory mutations, unique (tenant,request_id) receipt constraints, transactional outbox event insert with state mutation. Kafka/RabbitMQ workers consume with at-least-once delivery and idempotent handlers; exactly-once *effects* are achieved through DB constraints, not messaging claims. DLQ and reconciliation job handle poison messages. Redis can cache read-only state but not be the source of truth.

### 5.6 Vector and object storage
Vector DB (pgvector/Qdrant) optional for product catalog or policy retrieval, never for transaction authority. Object storage holds signed evaluation traces, datasets, model packages, snapshots and external audit checkpoints. Version artifacts and enforce per-tenant encryption and retention.

### 5.7 Ingestion and data lineage
Ingest catalog and workflow events via CDC, schema registry, validation, deduplication, provenance, watermarking and dead-letter queues. Record source timestamps and effective policy version. Reject out-of-order events that violate entity versions. PII is minimized, tokenized and segregated from prompts.

### 5.8 Concurrency, load balancing and autoscaling
Gateway pods behind L7 load balancer; route by tenant and region. Workers autoscale on queue age, latency and outstanding action count; GPU inference scales on token throughput and VRAM utilization. Use bounded concurrency, per-tenant quotas, circuit breakers, request deadlines and jittered retries. Avoid holding locks during model inference.

### 5.9 High availability, fault tolerance and distributed processing
Multi-AZ PostgreSQL with synchronous local replication, automated failover and PITR; multi-AZ queue and object storage. At-least-once event delivery plus idempotency. Retry ambiguous ACKs using the same key. Large evaluation suites use Ray/Spark/Dask with isolated fixture DBs per trial; never share mutable fixture state across parallel evaluations. Network partitions favor safety over accepting unverified mutations.

### 5.10 Model registry and versioning
Track model weights/hash, tokenizer, quantization, inference runtime, prompts, schemas, policies and evaluation dataset versions in MLflow or equivalent registry. Include model version in traces; stage promotion requires contract and utility regression gates. Immutable release manifests and signed supply-chain provenance.

### 5.11 CI/CD and release governance
Lint/type checks, unit/property tests, concurrency tests, migration tests, fault injection, SAST, dependency scanning, SBOM, image signing and container scanning. Canary/shadow planner proposals before enabling writes; dry-run compare final-state expectations. Blue/green rollout with schema compatibility and rollback plan; never roll back ledger history. Database migrations expand/contract, never destructive in the same release.

### 5.12 Telemetry and observability
OpenTelemetry trace per request linking model proposal, schema validation, policy decision, DB transaction and state-oracle verdict. Prometheus metrics: state mismatch rate, unauthorized attempts, idempotent replay ratio, queue age, transaction retries, p95 latency, cost per verified action. Avoid PII in logs. Audit traces need independent retention and integrity anchors.

### 5.13 IAM, secrets and approval
OIDC/mTLS workload identity; policy engine (OPA/Cedar) authorizes tenant, actor, resource and action. Short-lived credentials from Vault/KMS, least-privilege DB accounts, per-tenant encryption keys. Human approvals are signed external artifacts bound to command digest and expiry; never a user-supplied boolean. Network egress allowlist; optional SLM isolated from write-capable credentials.

### 5.14 Multi-tenancy
Row-level security or tenant-isolated databases according to risk. Every unique key includes tenant; rate limits, quotas, billing and audit retention per tenant. Prevent cross-tenant retrieval and cache-key collisions. Test tenant escape and noisy-neighbor scenarios.

### 5.15 Cost/performance
Budget planner inference, DB transaction time, queueing and verification separately. Start CPU-only for low throughput; add GPU serving when utilization and latency justify it. Quantize only after task-success and calibration checks. Hot-key contention, not raw inference, may dominate inventory workflows. Benchmark P50/P95/P99 and cost per verified mutation, not just model tokens/s.

### 5.16 Backup, disaster recovery
Encrypted daily backups, WAL archiving/PITR, immutable audit checkpoints and cross-region object replication. Define RPO/RTO by business criticality; practice restore drills and verify ledger consistency after recovery. Reconcile downstream systems from outbox. Never restore old state without replaying committed receipts and authorization policy updates.

### 5.17 Rollout, rollback and failure recovery
Canary on read-only or low-risk actions, progressive traffic ramp, rollback model/policy separately from ledger state. For stuck workflows use compensating actions (sagas), not blind database undo. Ambiguous commits resolved via receipt lookup. Quarantine any state-oracle mismatch and halt high-impact actions pending investigation.

### 5.18 Cloud/on-prem/hybrid criteria
On-prem: strict data residency, low-latency factory network, CPU-first inference, limited ops team. Cloud: multi-region HA, elastic GPUs, managed Postgres/queues and high burst workloads. Hybrid: local inference with cloud control plane and encrypted event sync; requires offline authorization rules and conflict reconciliation. Evaluate regulatory scope, egress cost, operational burden and failure-domain independence.

### 5.19 Security assumptions and non-goals
A malicious DBA can rewrite local chain and receipts; hash chaining alone is not tamper-proof. API key is a local demo, not enterprise authentication. This repository does not implement a production approval provider, cross-region distributed transactions, signed audit anchoring, arbitrary tools, or real LLM evaluation. Explicitly separate implemented features from architecture proposals.

### 5.20 Scale-up migration checklist
1. Replace SQLite with PostgreSQL, add tenant RLS and optimistic entity versions.
2. Introduce durable transactional outbox and idempotent queue consumers.
3. Replace demo actors/approval with OIDC and signed authorization artifacts.
4. Export audit chain to append-only signed external checkpoints.
5. Add model registry, tracing, load testing, canary and disaster recovery drills.
6. Run adversarial/real-world evaluation with independent end-state oracles.

### 5.21 Service SLOs (proposed, not measured)
No overselling or unauthorized committed actions in acceptance tests; 99.9% availability for read-only planning; P95 under 300 ms for CPU deterministic actions at tested load; P95 deletion/reconciliation bounded by workflow-specific SLO; 100% signed audit checkpoint coverage in production. Validate under real concurrency and failure injection before adoption.
