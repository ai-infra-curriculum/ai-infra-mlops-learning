# LLMOps Production System - Architecture

## Table of Contents
1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [LLM Serving Layer](#llm-serving-layer)
4. [RAG Pipeline](#rag-pipeline)
5. [Monitoring and Observability](#monitoring-and-observability)
6. [Security Architecture](#security-architecture)
7. [Cost Optimization](#cost-optimization)
8. [Data Flow](#data-flow)
9. [Deployment Architecture](#deployment-architecture)
10. [Scalability and Performance](#scalability-and-performance)

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              External Clients                            │
│                    (Web Apps, Mobile Apps, Internal Services)            │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Load Balancer (NGINX)                            │
│                     (SSL Termination, Request Routing)                   │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          API Gateway Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │ Rate Limiter │  │     Auth     │  │   Metrics    │                  │
│  │   (Redis)    │  │  Middleware  │  │  Collection  │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
┌───────────────────────────┐  ┌──────────────────────────┐
│   Security Layer          │  │   Optimization Layer     │
│  ┌──────────────────┐     │  │  ┌─────────────────┐    │
│  │ Input Validator  │     │  │  │  Cache Manager  │    │
│  ├──────────────────┤     │  │  ├─────────────────┤    │
│  │  PII Detector    │     │  │  │  Token Optimizer│    │
│  ├──────────────────┤     │  │  ├─────────────────┤    │
│  │ Content Filter   │     │  │  │  Cost Tracker   │    │
│  └──────────────────┘     │  │  └─────────────────┘    │
└───────────┬───────────────┘  └────────────┬─────────────┘
            │                               │
            └───────────┬───────────────────┘
                        │
        ┌───────────────┴────────────────┐
        ▼                                ▼
┌──────────────────┐          ┌─────────────────────────┐
│  RAG Pipeline    │          │   LLM Service           │
│  ┌────────────┐  │          │   ┌───────────────┐    │
│  │  Document  │  │          │   │  vLLM Server  │    │
│  │  Processor │  │          │   │               │    │
│  ├────────────┤  │          │   │ ┌───────────┐ │    │
│  │  Chunker   │  │          │   │ │PagedAttn  │ │    │
│  ├────────────┤  │          │   │ ├───────────┤ │    │
│  │ Embeddings │  │◄─────────┤   │ │Continuous │ │    │
│  ├────────────┤  │          │   │ │ Batching  │ │    │
│  │  Vector DB │  │          │   │ ├───────────┤ │    │
│  │ (ChromaDB) │  │          │   │ │  Tensor   │ │    │
│  ├────────────┤  │          │   │ │Parallelism│ │    │
│  │ Retriever  │  │          │   │ └───────────┘ │    │
│  ├────────────┤  │          │   │               │    │
│  │ Re-ranker  │  │          │   │  GPU Cluster  │    │
│  └────────────┘  │          │   └───────────────┘    │
└──────────────────┘          └─────────────────────────┘
        │                                │
        └────────────┬───────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Observability & Analytics Platform             │
│  ┌───────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐ │
│  │Prometheus │  │  Jaeger  │  │    ELK    │  │ Grafana  │ │
│  │ (Metrics) │  │ (Traces) │  │   (Logs)  │  │(Dashbrd) │ │
│  └───────────┘  └──────────┘  └───────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Modularity**: Each component is independently deployable and scalable
2. **Observability-First**: Built-in metrics, logging, and tracing from day one
3. **Security-in-Depth**: Multiple layers of security controls
4. **Cost-Awareness**: Every component tracks and optimizes for cost
5. **Performance**: Optimized for low latency and high throughput
6. **Resilience**: Graceful degradation and fault tolerance

## Component Architecture

### Service Breakdown

```
┌─────────────────────────────────────────────────────────────┐
│                    LLMOps System Components                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  API Layer                                                   │
│  ├── FastAPI Application                                    │
│  ├── Request/Response Models (Pydantic)                     │
│  ├── Route Handlers                                         │
│  └── Middleware Stack                                       │
│                                                              │
│  Core Services                                              │
│  ├── LLM Service (vLLM wrapper)                            │
│  ├── RAG Service (orchestration)                           │
│  ├── Prompt Manager                                         │
│  ├── Cost Tracker                                           │
│  └── Security Service                                       │
│                                                              │
│  Data Layer                                                  │
│  ├── Vector Database (ChromaDB)                            │
│  ├── Cache (Redis)                                          │
│  ├── Metadata Store (PostgreSQL)                           │
│  └── Object Storage (S3/MinIO)                             │
│                                                              │
│  Infrastructure Services                                    │
│  ├── Monitoring (Prometheus + Grafana)                     │
│  ├── Tracing (Jaeger)                                       │
│  ├── Logging (ELK Stack)                                    │
│  └── Message Queue (RabbitMQ/Kafka)                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## LLM Serving Layer

### vLLM Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                      vLLM Server                              │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  Request Queue                                                 │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Request 1 │ Request 2 │ Request 3 │ ... │ Request N  │    │
│  └──────────────────────────────────────────────────────┘    │
│                           │                                    │
│                           ▼                                    │
│  ┌──────────────────────────────────────────────────────┐    │
│  │         Continuous Batching Scheduler                 │    │
│  │  - Dynamic batch formation                            │    │
│  │  - Priority-based scheduling                          │    │
│  │  - Preemption for latency-sensitive requests          │    │
│  └────────────────────┬─────────────────────────────────┘    │
│                       │                                        │
│                       ▼                                        │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              PagedAttention Engine                    │    │
│  │  ┌────────────────────────────────────────────┐      │    │
│  │  │  KV Cache (Paged Memory)                   │      │    │
│  │  │  ┌─────┬─────┬─────┬─────┬─────┬─────┐    │      │    │
│  │  │  │Page │Page │Page │Page │Page │Page │    │      │    │
│  │  │  │  1  │  2  │  3  │  4  │  5  │  6  │    │      │    │
│  │  │  └─────┴─────┴─────┴─────┴─────┴─────┘    │      │    │
│  │  │  - Non-contiguous memory allocation        │      │    │
│  │  │  - Sharing across sequences (prefix)       │      │    │
│  │  │  - Efficient memory utilization (>90%)     │      │    │
│  │  └────────────────────────────────────────────┘      │    │
│  └────────────────────┬─────────────────────────────────┘    │
│                       │                                        │
│                       ▼                                        │
│  ┌──────────────────────────────────────────────────────┐    │
│  │           Model Execution (Multi-GPU)                 │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │    │
│  │  │  GPU 0   │  │  GPU 1   │  │  GPU 2   │            │    │
│  │  │          │  │          │  │          │            │    │
│  │  │  Layers  │  │  Layers  │  │  Layers  │            │    │
│  │  │   0-11   │  │  12-23   │  │  24-35   │            │    │
│  │  └──────────┘  └──────────┘  └──────────┘            │    │
│  │  Tensor Parallelism (sharded across GPUs)            │    │
│  └────────────────────┬─────────────────────────────────┘    │
│                       │                                        │
│                       ▼                                        │
│  ┌──────────────────────────────────────────────────────┐    │
│  │            Response Generation                        │    │
│  │  - Streaming output (SSE)                            │    │
│  │  - Token-by-token generation                         │    │
│  │  - Stopping criteria evaluation                      │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

### Key Optimizations

1. **PagedAttention**
   - Non-contiguous memory allocation for KV cache
   - Reduces memory fragmentation by ~60%
   - Enables higher batch sizes and throughput

2. **Continuous Batching**
   - New requests join batch immediately (not waiting for batch completion)
   - Reduces average latency by ~30%
   - Improves GPU utilization to >80%

3. **Tensor Parallelism**
   - Shards model layers across multiple GPUs
   - Enables serving models larger than single GPU memory
   - Linear scaling for throughput with GPU count

4. **Prefix Caching**
   - Shares KV cache for common prompt prefixes
   - Reduces computation for repeated system prompts
   - Saves ~40% of compute for RAG applications

## RAG Pipeline

### Document Processing Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│                  Document Ingestion Pipeline                  │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────┐
         │     Document Loader              │
         │  - PDF, DOCX, TXT, MD, HTML     │
         │  - Table extraction              │
         │  - Image OCR                     │
         │  - Metadata extraction           │
         └──────────────┬───────────────────┘
                        │
                        ▼
         ┌──────────────────────────────────┐
         │     Text Preprocessing           │
         │  - Cleaning and normalization    │
         │  - Language detection            │
         │  - Section identification        │
         │  - Deduplication                 │
         └──────────────┬───────────────────┘
                        │
                        ▼
         ┌──────────────────────────────────┐
         │     Chunking Strategy            │
         │  ┌────────────────────────────┐  │
         │  │ Recursive Char Splitter    │  │
         │  │  - Respects boundaries     │  │
         │  │  - Configurable overlap    │  │
         │  └────────────────────────────┘  │
         │  ┌────────────────────────────┐  │
         │  │ Semantic Chunker           │  │
         │  │  - Embedding-based split   │  │
         │  │  - Coherent segments       │  │
         │  └────────────────────────────┘  │
         └──────────────┬───────────────────┘
                        │
                        ▼
         ┌──────────────────────────────────┐
         │     Embedding Generation         │
         │  - Batch processing              │
         │  - Multiple models support       │
         │  - Normalization                 │
         │  - Caching                       │
         └──────────────┬───────────────────┘
                        │
                        ▼
         ┌──────────────────────────────────┐
         │     Vector Database Storage      │
         │  (ChromaDB)                      │
         │  - Collection management         │
         │  - Metadata indexing             │
         │  - Persistence                   │
         └──────────────────────────────────┘
```

### Retrieval Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│                    Query Processing                           │
│  User Query → Query Enhancement → Query Embedding            │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                  Hybrid Retrieval                             │
│  ┌─────────────────────┐        ┌─────────────────────┐     │
│  │  Dense Retrieval    │        │  Sparse Retrieval   │     │
│  │  (Vector Similarity)│        │  (BM25 / Keywords)  │     │
│  │                     │        │                     │     │
│  │  Top-K results      │        │  Top-K results      │     │
│  └──────────┬──────────┘        └──────────┬──────────┘     │
│             └────────────┬──────────────────┘                │
└──────────────────────────┼───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                    Fusion & Ranking                           │
│  - Reciprocal Rank Fusion (RRF)                              │
│  - Score normalization                                        │
│  - Deduplication                                              │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                     Re-ranking                                │
│  ┌────────────────────────────────────────────┐              │
│  │  Cross-Encoder Re-ranker                   │              │
│  │  - Deep semantic matching                  │              │
│  │  - Query-document relevance scoring        │              │
│  └────────────────────────────────────────────┘              │
│  ┌────────────────────────────────────────────┐              │
│  │  LLM-based Re-ranker (optional)            │              │
│  │  - Natural language relevance judgment     │              │
│  │  - Contextual understanding                │              │
│  └────────────────────────────────────────────┘              │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                Context Assembly                               │
│  - Token budget allocation                                    │
│  - Context compression                                        │
│  - Citation formatting                                        │
│  - Source attribution                                         │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                Prompt Construction                            │
│  System Prompt + Retrieved Context + User Query              │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
                   To LLM Service
```

## Monitoring and Observability

### Three Pillars of Observability

```
┌─────────────────────────────────────────────────────────────────┐
│                         Metrics (Prometheus)                     │
├─────────────────────────────────────────────────────────────────┤
│  Request Metrics                                                 │
│  - request_duration_seconds (histogram)                         │
│  - requests_total (counter)                                      │
│  - requests_in_flight (gauge)                                    │
│                                                                  │
│  LLM Metrics                                                     │
│  - tokens_processed_total (counter)                             │
│  - llm_latency_seconds (histogram)                              │
│  - batch_size (histogram)                                        │
│  - gpu_memory_usage_bytes (gauge)                               │
│  - gpu_utilization_percent (gauge)                              │
│                                                                  │
│  RAG Metrics                                                     │
│  - retrieval_latency_seconds (histogram)                        │
│  - documents_retrieved (histogram)                              │
│  - embedding_cache_hits (counter)                               │
│  - relevance_score (histogram)                                  │
│                                                                  │
│  Cost Metrics                                                    │
│  - request_cost_usd (histogram)                                 │
│  - daily_cost_usd (gauge)                                        │
│  - cost_by_user (gauge with labels)                             │
│                                                                  │
│  Security Metrics                                                │
│  - rate_limit_exceeded (counter)                                │
│  - pii_detected (counter)                                        │
│  - content_filtered (counter)                                    │
│  - auth_failures (counter)                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      Logs (ELK Stack)                            │
├─────────────────────────────────────────────────────────────────┤
│  Structured JSON Logs                                            │
│  {                                                               │
│    "timestamp": "2025-10-26T10:15:30.123Z",                     │
│    "level": "INFO",                                              │
│    "service": "llm-api",                                         │
│    "trace_id": "abc123...",                                      │
│    "span_id": "def456...",                                       │
│    "user_id": "user_789",                                        │
│    "request_id": "req_xyz",                                      │
│    "endpoint": "/v1/chat/completions",                          │
│    "method": "POST",                                             │
│    "duration_ms": 234,                                           │
│    "tokens_input": 50,                                           │
│    "tokens_output": 150,                                         │
│    "cost_usd": 0.0042,                                           │
│    "message": "Request completed successfully"                   │
│  }                                                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Traces (Jaeger/OpenTelemetry)                 │
├─────────────────────────────────────────────────────────────────┤
│  End-to-End Request Trace                                        │
│                                                                  │
│  ┌─ api.request [200ms] ──────────────────────────────┐        │
│  │  ┌─ security.validate [5ms] ────┐                  │        │
│  │  │  ├─ input_validator [2ms]    │                  │        │
│  │  │  └─ pii_detector [3ms]       │                  │        │
│  │  └──────────────────────────────┘                  │        │
│  │  ┌─ rag.retrieve [80ms] ────────────────┐          │        │
│  │  │  ├─ embedding.generate [20ms]        │          │        │
│  │  │  ├─ vector_search [40ms]             │          │        │
│  │  │  └─ rerank [20ms]                    │          │        │
│  │  └──────────────────────────────────────┘          │        │
│  │  ┌─ llm.inference [110ms] ──────────────────────┐  │        │
│  │  │  ├─ prompt_assembly [5ms]                    │  │        │
│  │  │  ├─ vllm_generation [100ms]                  │  │        │
│  │  │  └─ response_formatting [5ms]                │  │        │
│  │  └──────────────────────────────────────────────┘  │        │
│  │  ┌─ cost.track [5ms] ────┐                        │        │
│  │  └───────────────────────┘                        │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                  │
│  Span Attributes:                                                │
│  - user_id, request_id, model_name                              │
│  - tokens_input, tokens_output, cost_usd                        │
│  - cache_hit, error_code, retry_count                           │
└─────────────────────────────────────────────────────────────────┘
```

### Dashboards

**1. Operational Dashboard**
- Request rate and error rate
- Latency percentiles (P50, P95, P99)
- GPU utilization and memory
- Active requests and queue depth

**2. Cost Dashboard**
- Hourly/daily/monthly spending
- Cost per user/tenant
- Cost per model
- Budget alerts and projections

**3. RAG Performance Dashboard**
- Retrieval latency
- Number of documents retrieved
- Relevance scores distribution
- Cache hit rates

**4. Security Dashboard**
- Rate limit violations
- PII detection events
- Content filter triggers
- Authentication failures

## Security Architecture

### Defense in Depth

```
┌───────────────────────────────────────────────────────────┐
│  Layer 1: Network Security                                │
│  - TLS 1.3 encryption                                     │
│  - WAF (Web Application Firewall)                         │
│  - DDoS protection                                        │
│  - IP whitelisting (optional)                             │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────────────────────┐
│  Layer 2: API Gateway Security                            │
│  - Rate limiting (per user, per IP, global)              │
│  - Request size limits                                    │
│  - Timeout enforcement                                    │
│  - CORS policy                                            │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────────────────────┐
│  Layer 3: Authentication & Authorization                  │
│  - API key validation                                     │
│  - JWT token verification                                 │
│  - OAuth2 flow support                                    │
│  - Role-based access control (RBAC)                       │
│  - Multi-tenancy isolation                                │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────────────────────┐
│  Layer 4: Input Validation & Sanitization                │
│  - Schema validation (Pydantic)                           │
│  - Input length limits                                    │
│  - Character encoding validation                          │
│  - SQL injection prevention                               │
│  - XSS prevention                                         │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────────────────────┐
│  Layer 5: PII Detection & Protection                      │
│  - Email, phone, SSN, credit card detection              │
│  - Regex-based patterns                                   │
│  - ML-based entity recognition (Presidio)                │
│  - Redaction or anonymization                             │
│  - Logging with PII removed                               │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────────────────────┐
│  Layer 6: Content Filtering                               │
│  - Harmful content detection (input)                      │
│  - Jailbreak attempt detection                            │
│  - Prompt injection detection                             │
│  - Output filtering for harmful content                   │
│  - Configurable content policies                          │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────────────────────┐
│  Layer 7: Audit & Compliance                              │
│  - Comprehensive audit logging                            │
│  - Immutable audit trail                                  │
│  - Compliance reporting (GDPR, SOC 2)                     │
│  - Data retention policies                                │
└───────────────────────────────────────────────────────────┘
```

## Cost Optimization

### Cost Tracking Flow

```
Request → Token Counting → Cost Calculation → Budget Check → Execution
              │                    │                │
              ▼                    ▼                ▼
         Metrics DB          Cost Analytics    Alert System
```

### Optimization Strategies

**1. Semantic Caching**
```
User Query → Embedding → Vector Search in Cache
                              │
                              ├─ Hit (>95% similarity) → Return cached response
                              └─ Miss → Process request → Store in cache
```

**2. Prompt Compression**
```
Long Context → Identify Key Information → Compress → Shorter Prompt
(1000 tokens)                                         (400 tokens)
                                                      60% cost savings
```

**3. Dynamic Model Selection**
```
Request Analysis → Complexity Score → Model Selection
                                          │
                      ┌───────────────────┼───────────────────┐
                      ▼                   ▼                   ▼
                  Simple Query       Medium Query       Complex Query
                  (Small Model)      (Medium Model)     (Large Model)
                  Low Cost           Medium Cost        High Cost
                  Fast               Balanced           High Quality
```

**4. Token Budget Management**
```
User Request → Check User Budget → Allocate Tokens → Track Usage
                     │                                      │
                     ├─ Over Budget → Reject or Throttle   │
                     └─ Within Budget → Allow              ▼
                                                     Update Balance
```

## Data Flow

### Complete Request Flow

```
1. Client Request
   │
   ├─→ [Load Balancer] → [API Gateway]
   │
2. Security & Validation
   │
   ├─→ [Rate Limiter] → Check limits
   ├─→ [Auth] → Validate credentials
   ├─→ [Input Validator] → Validate schema
   ├─→ [PII Detector] → Detect/redact PII
   └─→ [Content Filter] → Check for harmful content
   │
3. Cost & Budget Check
   │
   ├─→ [Token Counter] → Estimate tokens
   ├─→ [Budget Checker] → Verify user budget
   └─→ [Cost Tracker] → Initialize cost tracking
   │
4. Cache Check (Optional)
   │
   ├─→ [Semantic Cache] → Check for similar queries
   │   ├─ Hit → Return cached response (skip to step 8)
   │   └─ Miss → Continue to step 5
   │
5. RAG Processing (If Enabled)
   │
   ├─→ [Query Processor] → Enhance query
   ├─→ [Embedding Service] → Generate query embedding
   ├─→ [Vector Database] → Retrieve relevant documents
   ├─→ [Re-ranker] → Rank documents by relevance
   └─→ [Context Assembler] → Build context for LLM
   │
6. Prompt Assembly
   │
   ├─→ [Prompt Manager] → Get template
   ├─→ [Variable Substitution] → Fill template
   └─→ [Prompt Validator] → Validate final prompt
   │
7. LLM Inference
   │
   ├─→ [vLLM Server] → Queue request
   │   ├─→ [Batching Scheduler] → Form batch
   │   ├─→ [PagedAttention] → Manage KV cache
   │   └─→ [Model Execution] → Generate tokens
   │
   └─→ [Streaming Handler] → Stream response (if enabled)
   │
8. Post-Processing
   │
   ├─→ [Output Filter] → Check for harmful content
   ├─→ [Citation Formatter] → Add source citations (RAG)
   └─→ [Response Validator] → Validate response structure
   │
9. Metrics & Logging
   │
   ├─→ [Metrics Collector] → Record performance metrics
   ├─→ [Tracer] → Close trace spans
   ├─→ [Logger] → Log structured event
   └─→ [Cost Tracker] → Calculate final cost
   │
10. Response
    │
    └─→ Client receives response
```

## Deployment Architecture

### Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────┐        │
│  │  Ingress Controller (NGINX)                        │        │
│  │  - SSL Termination                                 │        │
│  │  - Path-based routing                              │        │
│  └────────────────┬───────────────────────────────────┘        │
│                   │                                              │
│  ┌────────────────┴───────────────────────────────────┐        │
│  │  API Service (3 replicas)                          │        │
│  │  - FastAPI pods                                    │        │
│  │  - CPU-based autoscaling                           │        │
│  │  - Health checks                                   │        │
│  └────────────┬──────────────┬────────────────────────┘        │
│               │              │                                   │
│  ┌────────────▼─────┐  ┌────▼──────────────────────┐          │
│  │  vLLM Service    │  │  RAG Service              │          │
│  │  (GPU Pods)      │  │  (CPU Pods)               │          │
│  │                  │  │                            │          │
│  │  - GPU node      │  │  - Document processor     │          │
│  │    affinity      │  │  - Embedding service      │          │
│  │  - Shared GPU    │  │  - Retriever              │          │
│  │    (MIG/MPS)     │  │  - Re-ranker              │          │
│  │  - Model         │  │  - 3 replicas             │          │
│  │    persistent    │  │  - CPU autoscaling        │          │
│  │    volume        │  │                            │          │
│  └──────────────────┘  └───────────┬────────────────┘          │
│                                     │                            │
│  ┌─────────────────────────────────▼────────────────┐          │
│  │  Data Layer                                       │          │
│  │  ┌──────────────┐  ┌──────────────┐             │          │
│  │  │  ChromaDB    │  │   Redis      │             │          │
│  │  │  StatefulSet │  │  (Cache)     │             │          │
│  │  │  - 3 replicas│  │  - 3 replicas│             │          │
│  │  │  - Persistent│  │  - Sentinel  │             │          │
│  │  │    volumes   │  │  - HA mode   │             │          │
│  │  └──────────────┘  └──────────────┘             │          │
│  │  ┌──────────────┐  ┌──────────────┐             │          │
│  │  │  PostgreSQL  │  │  MinIO/S3    │             │          │
│  │  │  (Metadata)  │  │  (Objects)   │             │          │
│  │  │  - Primary   │  │  - Documents │             │          │
│  │  │  - Replica   │  │  - Models    │             │          │
│  │  └──────────────┘  └──────────────┘             │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                  │
│  ┌──────────────────────────────────────────────────┐          │
│  │  Observability Stack                              │          │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │          │
│  │  │ Prometheus │  │  Grafana   │  │   Jaeger   │ │          │
│  │  └────────────┘  └────────────┘  └────────────┘ │          │
│  │  ┌────────────────────────────────────────────┐  │          │
│  │  │  ELK Stack (Elasticsearch, Logstash, Kibana) │          │
│  │  └────────────────────────────────────────────┘  │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Resource Requirements

**API Pods**
- CPU: 2 cores (request), 4 cores (limit)
- Memory: 4Gi (request), 8Gi (limit)
- Replicas: 3-10 (autoscaling)

**vLLM GPU Pods**
- GPU: 1x A100 (40GB) per pod
- CPU: 8 cores
- Memory: 32Gi
- Replicas: 2-4 (static or slow autoscaling)

**RAG Service Pods**
- CPU: 4 cores (request), 8 cores (limit)
- Memory: 8Gi (request), 16Gi (limit)
- Replicas: 3-6 (autoscaling)

**Data Layer**
- ChromaDB: 100Gi persistent volume per replica
- Redis: 8Gi memory
- PostgreSQL: 50Gi persistent volume

## Scalability and Performance

### Horizontal Scaling

```
Load Increase Detection
  │
  ├─→ API Pods: Scale based on CPU/memory
  ├─→ RAG Pods: Scale based on queue depth
  └─→ vLLM Pods: Manual or slow autoscale (GPU warmup)
```

### Performance Optimizations

**1. Request Level**
- Connection pooling
- HTTP/2 multiplexing
- Response compression

**2. Computation Level**
- Batch inference
- Mixed precision (FP16/BF16)
- Flash Attention
- Quantization (INT8/INT4)

**3. Memory Level**
- KV cache sharing (prefix)
- PagedAttention memory management
- Model weight offloading (CPU/NVMe)

**4. Network Level**
- CDN for static assets
- Geographic load balancing
- Request coalescing

### Expected Performance

**Throughput**
- API endpoints: 100-500 RPS
- LLM inference: 1000-5000 tokens/second
- Vector search: 10ms for 1M vectors

**Latency**
- P50: 200ms (total)
- P95: 500ms (total)
- P99: 1000ms (total)

**Availability**
- Target: 99.9% uptime
- Max downtime: ~8.7 hours/year

---

**Document Version**: 1.0
**Last Updated**: 2025-10-26
**Maintained By**: AI Infrastructure Team
