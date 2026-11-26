"""
Section 8: Proposed Technology Stack & Justifications
"""

def get_markdown():
    return """## 8. Proposed Technology Stack & Justifications

### 8.1 Comprehensive Technology Matrix
The technology stack is selected to meet extreme throughput, ultra-low latency, bank-grade cryptographic security, and cloud-native portability:

| Layer / Architectural Component | Technology Selection | Primary Architectural Justification | Evaluated Alternative & Rejection Rationale |
| :--- | :--- | :--- | :--- |
| **Edge API Gateway** | **Envoy / Kong Enterprise** | C++ performance, sub-millisecond mTLS termination, native OpenTelemetry tracing, and dynamic token-bucket rate limiting. | *AWS API Gateway:* Rejected due to high per-request pricing at 1,000 TPS ($8.64M/year) and unpredictable cold-start latency. |
| **Ingestion Microservice** | **Go 1.23** | Compiles to native binary; instant startup (< 50ms); zero garbage collection pauses; goroutines handle 10,000+ concurrent connections effortlessly. | *Java Spring Boot:* Rejected due to heavier memory footprint (~500MB vs ~35MB in Go) and JVM warm-up compilation jitter. |
| **Feature Aggregation Engine** | **Apache Flink / Kafka Streams** | True event-by-event stream processing with sub-5ms sliding-window state accumulation; native RocksDB checkpointing. | *Apache Spark Streaming:* Rejected because micro-batching introduces 100-500ms latency, breaching the sub-45ms P99 SLO. |
| **Distributed L2 Cache** | **Redis Enterprise Cluster** | Ultra-low latency (< 0.8ms lookups); native atomic counters (`INCRBY`) and sorted sets for velocity windows; active-active multi-AZ replication. | *Memcached:* Rejected due to lack of native persistence, lack of data structures (sets/hashes), and lack of active multi-AZ replication. |
| **ML Inference Engine** | **Triton Inference Server (NVIDIA)** | Native support for ONNX Runtime and TensorRT; dynamic request batching (< 2ms window); multi-model concurrent execution on CPU/GPU. | *FastAPI / TorchServe:* Rejected due to Python Global Interpreter Lock (GIL) bottlenecks, poor GPU saturation, and high latency variability. |
| **Case Management DB** | **Amazon Aurora PostgreSQL (Multi-AZ)** | Full ACID compliance for legal case records; automated sub-30s failover; native JSONB support for dynamic transaction payloads; read-replicas. | *MongoDB:* Rejected due to eventual consistency trade-offs during network partitions and compliance team preference for relational ACID auditing. |
| **Compliance WORM Lakehouse** | **Apache Iceberg on Amazon S3 Object Lock** | Write-Once-Read-Many (WORM) 7-year immutable compliance lock; Parquet columnar format with ZSTD compression (6:1 ratio); partition pruning. | *Traditional Data Warehouses (Snowflake):* Rejected for raw event archiving due to prohibitive 24/7 compute warehouse costs at 86.4M events/day. |
| **Event Backbone** | **Apache Kafka (Confluent / MSK)** | 32 partitions per topic; strictly ordered append-only log; partition key routing by `account_id`; persistent 7-day buffer; KRaft consensus. | *RabbitMQ / AWS SQS:* Rejected because message broker queue semantics destroy replayability (messages disappear upon ACK). |
| **Analyst BFF Service** | **Node.js 22 (Fastify) / TypeScript** | Asynchronous non-blocking event loop handles 1,000+ persistent WebSockets with low memory; native JSON handling and TypeScript type safety. | *Ruby on Rails / Django:* Rejected due to synchronous multi-process memory consumption under heavy WebSocket concurrency. |
| **Analyst Operations UI** | **React 19 / Next.js 15 SPA** | Virtual DOM rendering; TanStack Virtual recycling; TanStack Query server caching; Web Worker background thread execution. | *Angular / Vue:* React selected due to the maturity of high-performance virtual grid ecosystems (TanStack Virtual) and enterprise banking talent pool. |
| **Observability Telemetry** | **OpenTelemetry + Tempo + Loki + Prometheus** | Vendor-neutral standard; zero lock-in; W3C TraceContext propagation across Kafka; S3-backed storage reduces telemetry cost by 85%. | *Datadog / Splunk SaaS:* Rejected due to astronomical SaaS data ingestion costs for 1,000 TPS full tracing (~$1.2M+ annually). |

---

### 8.2 In-Depth Justifications for Core Stack Decisions

#### 1. Apache Kafka as the Event Backbone vs. Traditional Message Queues (RabbitMQ / SQS)
Traditional message brokers (e.g., RabbitMQ, ActiveMQ, Amazon SQS) operate on **transient queue semantics**: once a consumer reads and acknowledges a message, the message is permanently deleted from the queue. 
In financial fraud detection, transient queues are fundamentally incompatible with regulatory requirements:
- *Regulatory Non-Compliance:* BCBS 239 mandates that historical transactions must be replayable. If an algorithm fails or an audit occurs, transient queues cannot reconstruct history.
- *Kafka Distributed Commit Log:* Kafka is an immutable, distributed append-only log. Events persist for their configured retention window (7 days in our hot tier) regardless of whether they have been consumed. This allows multiple independent consumer groups (Scoring Engine, Downstream Enforcement, Compliance Lakehouse) to read at their own pace, and enables zero-risk historical replays simply by seeking consumer offsets.

#### 2. Triton Inference Server vs. Custom Python/FastAPI Microservice
Many organizations initially deploy machine learning models inside standard Python web frameworks (such as FastAPI or Flask). In production at 1,000 TPS, this approach inevitably collapses:
- *Python GIL Bottleneck:* The Python Global Interpreter Lock prevents true multi-threaded parallel execution, requiring dozens of heavy container replicas that exhaust host memory.
- *Triton Performance Advantages:* Triton Inference Server is written in high-performance C++. It interfaces directly with NVIDIA TensorRT and ONNX Runtime, bypassing the Python runtime entirely during inference execution. Triton's **Dynamic Batching** aggregates requests arriving within a 2-millisecond window into optimized GPU matrix operations, increasing inference throughput by **4x** and slashing P99 latency from 35ms down to **< 12ms**.

#### 3. Apache Iceberg on Amazon S3 Object Lock vs. Commercial Cloud Data Warehouses
Archiving 1,000 transactions per second equals **86.4 million events per day** (over 31.5 billion records annually). 
- *Cost Comparison:* Ingesting and storing 31.5 billion records directly into an always-on cloud data warehouse (such as Snowflake or Google BigQuery) incurs immense compute clustering and per-terabyte query costs.
- *Open Lakehouse Advantage:* Storing raw, enriched, and evaluated transactions in open **Apache Iceberg** format on **Amazon S3 Glacier Instant Retrieval** with Object Lock reduces total storage costs to pennies per gigabyte. The data is immutably locked against ransomware and deletion, while remaining instantly queryable via distributed SQL engines (Trino / AWS Athena) whenever compliance audits occur.
"""

def get_html():
    return """
<section id="section-8" class="report-section">
  <div class="section-header">
    <span class="section-number">08</span>
    <div class="section-title-wrap">
      <h2>Proposed Technology Stack &amp; Justifications</h2>
      <p class="section-subtitle">Evaluating databases, frameworks, messaging, and cloud infrastructure with architectural trade-offs.</p>
    </div>
  </div>

  <h3>8.1 Comprehensive Technology Selection Matrix</h3>
  <div class="table-container">
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 20%;">Architectural Layer</th>
          <th style="width: 22%;">Technology Selection</th>
          <th style="width: 33%;">Primary Architectural Justification</th>
          <th style="width: 25%;">Rejected Alternative &amp; Rationale</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Edge Ingress Gateway</strong></td>
          <td><strong>Envoy / Kong Ingress</strong></td>
          <td>C++ speed; native mTLS termination; OTel span injection; token-bucket rate limiting.</td>
          <td><em>AWS API Gateway:</em> Prohibitive pricing at 1,000 TPS ($8.6M/yr) and cold starts.</td>
        </tr>
        <tr>
          <td><strong>Ingestion Microservice</strong></td>
          <td><strong>Go 1.23</strong></td>
          <td>Native binary; sub-50ms cold starts; zero GC jitter; lightweight goroutines.</td>
          <td><em>Java Spring:</em> 10x higher memory footprint and JVM warm-up latency spikes.</td>
        </tr>
        <tr>
          <td><strong>Feature Streaming</strong></td>
          <td><strong>Apache Flink / Streams</strong></td>
          <td>True event-by-event streaming; sub-5ms sliding-window calculations; RocksDB state.</td>
          <td><em>Spark Streaming:</em> Micro-batching introduces 100-500ms delay, breaching SLO.</td>
        </tr>
        <tr>
          <td><strong>Distributed L2 Cache</strong></td>
          <td><strong>Redis Enterprise Cluster</strong></td>
          <td>Sub-millisecond lookups (&lt;0.8ms); atomic counters (<code>INCRBY</code>); multi-AZ active-active.</td>
          <td><em>Memcached:</em> Lacks persistence, sorted sets, and active multi-AZ clustering.</td>
        </tr>
        <tr>
          <td><strong>ML Inference Server</strong></td>
          <td><strong>Triton Inference (NVIDIA)</strong></td>
          <td>C++ engine; ONNX/TensorRT native; dynamic request micro-batching; CPU/GPU support.</td>
          <td><em>FastAPI/Flask:</em> Python GIL bottlenecks and high latency variance.</td>
        </tr>
        <tr>
          <td><strong>Case Management DB</strong></td>
          <td><strong>Aurora PostgreSQL Multi-AZ</strong></td>
          <td>ACID compliance for legal cases; automated sub-30s failover; JSONB flexibility.</td>
          <td><em>MongoDB:</em> Eventual consistency risks and lack of relational audit constraints.</td>
        </tr>
        <tr>
          <td><strong>Compliance WORM Store</strong></td>
          <td><strong>Apache Iceberg on S3 Lock</strong></td>
          <td>WORM 7-year legal lock; Parquet columnar format (6:1 ZSTD ratio); partition pruning.</td>
          <td><em>Snowflake:</em> Prohibitive 24/7 compute clustering costs at 86.4M events/day.</td>
        </tr>
        <tr>
          <td><strong>Messaging Backbone</strong></td>
          <td><strong>Apache Kafka (MSK/Strimzi)</strong></td>
          <td>32 partitions/topic; immutable replayable commit log; key ordering by account_id.</td>
          <td><em>RabbitMQ/SQS:</em> Transient queue semantics delete messages on ACK, destroying replay.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
"""

