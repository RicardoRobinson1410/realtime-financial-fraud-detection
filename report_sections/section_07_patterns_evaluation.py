"""
Section 7: Architectural Patterns Evaluation & Cost-Benefit Analysis
"""

def get_markdown():
    return """## 7. Architectural Patterns Evaluation & Cost-Benefit Analysis

### 7.1 Cross-Cutting Architectural Patterns Matrix
To satisfy strict banking security regulations, sub-45ms latency budgets, and continuous operability, the architecture synthesizes four foundational design patterns. The matrix below delineates how each pattern specifically reinforces system quality attributes:

| Architectural Pattern | Scalability Contribution | Resilience Contribution | Security & Governance Contribution | Observability Contribution |
| :--- | :--- | :--- | :--- | :--- |
| **Service Mesh**<br>*(Istio / Envoy)* | Decouples networking from application code; enables fine-grained client-side load balancing. | Transparent circuit breakers, retry policies with jitter, and canary traffic shifting. | **Zero-Trust mTLS 1.3** across all pods; SPIFFE cryptographic workload identity; automated cert rotation. | Automatic uniform metrics, access logging, and distributed W3C trace span injection across all services. |
| **Backend-for-Frontend**<br>*(BFF Pattern)* | Shields core microservices from chatty UI traffic; offloads connection multiplexing for 500+ analysts. | Isolates frontend crashes from transaction processing; provides graceful degradation on case store errors. | Terminates analyst sessions; enforces fine-grained OIDC RBAC; masks sensitive card data before rendering. | Centralized logging of all human triage actions; tracks analyst response time and case throughput metrics. |
| **Multi-Tier Caching**<br>*(L1 Local + L2 Redis)* | Offloads 95% of state reads from persistent databases; supports 100,000+ ops/sec for velocity counts. | Local in-memory L1 cache serves fallback defaults if the distributed L2 Redis cluster experiences failover. | Encrypted in-transit (TLS) and at-rest (AES-256); ephemeral keys expire automatically via TTL. | Exposes cache hit/miss ratio metrics, memory saturation gauges, and eviction rate telemetry. |
| **Event Sourcing & EDA**<br>*(Apache Kafka)* | Scales linearly by adding topic partitions; supports 1,000 to 10,000+ TPS with zero architectural redesign. | Absorbs extreme traffic surges; isolates service outages; enables complete state reconstruction via replay. | Immutable, tamper-evident distributed append-only log; meets BCBS 239 / Basel III compliance. | Enables lag-based monitoring; provides end-to-end event lineage across the entire transaction lifecycle. |

---

### 7.2 In-Depth Pattern Analysis & Trade-Off Evaluations

#### 1. Service Mesh (Istio / Envoy Sidecars)
* **The Architecture:** Every microservice pod is deployed alongside an Envoy proxy sidecar managed by the Istio control plane. All inter-service communication is intercepted by Envoy.
* **Benefits in Financial Context:**
  - *Automated Zero-Trust Security:* In banking, perimeter security is insufficient. Regulators (PCI-DSS v4.0 Requirement 4) mandate encryption for all traffic in-transit, even within the internal virtual private cloud (VPC). Istio enforces mutual TLS (mTLS 1.3) with ephemeral X.509 certificates rotated every 24 hours automatically, eliminating manual certificate management.
  - *Canary Model Deployments:* When releasing a new fraud scoring microservice, Istio dynamically routes 2% of live traffic to the canary pod, monitoring error rates and P99 latency before rolling out 100%.
* **Cost & Risk Trade-offs:**
  - *Latency Overhead:* Each Envoy sidecar adds approximately **0.8ms to 1.5ms** of network hop latency. In a tight sub-45ms execution budget, multiple consecutive proxy hops can consume 10-15% of the latency budget.
  - *Memory Footprint:* Running an Envoy sidecar in every pod consumes 50-120MB of RAM per replica. Across 200 pod replicas, this represents 20GB+ of dedicated infrastructure overhead.
  - *Architectural Rationale:* The security and compliance guarantees of automated mTLS, zero-trust enforcement, and uniform telemetry overwhelmingly justify the small latency and memory cost.

---

#### 2. Backend-for-Frontend (BFF Pattern)
* **The Architecture:** Rather than allowing the React single-page application to query the Ingestion Service, Fraud Scoring Engine, and Case Database directly, all client interactions route through a dedicated Node.js BFF gateway.
* **Benefits in Financial Context:**
  - *Payload Optimization:* Internal domain entities contain extensive technical metadata, full feature arrays, and audit headers. The BFF filters and reshapes these objects into lean View Models optimized for analyst triage cards, reducing payload sizes by 70%.
  - *Connection Aggregation:* Hundreds of active fraud analysts maintaining open WebSocket feeds would overwhelm internal core microservices. The BFF multiplexes these connections, maintaining a single persistent subscription to the underlying message bus.
* **Cost & Risk Trade-offs:**
  - *Additional Hop:* Adds a single network hop (< 2ms) between the browser and the case data store.
  - *Maintenance Overhead:* Engineering teams must maintain the BFF codebase alongside frontend and backend services.
  - *Architectural Rationale:* Decoupling the high-churn UI lifecycle from high-reliability financial core services is an industry standard that dramatically increases development velocity and operational safety.

---

#### 3. Multi-Tier Caching (L1 Local In-Memory + L2 Distributed Redis)
* **The Architecture:** Microservices employ a two-tier caching strategy:
  - **L1 Cache (Caffeine in Java / Ristretto in Go):** Microsecond-speed in-process memory cache for static reference data (e.g., country code risk weights, sanction BIN lists, active business rule definitions).
  - **L2 Cache (Redis Enterprise Cluster):** Sub-millisecond distributed cache for dynamic sliding-window transaction counters and cardholder velocity states.
* **Benefits in Financial Context:**
  - *Elimination of Database Bottlenecks:* Evaluating 1,000 TPS with 10 historical lookups per transaction equals 10,000 queries per second. Querying relational databases at this rate would require massive, prohibitively expensive database hardware. Redis handles 100,000+ ops/sec at sub-millisecond latency.
* **Cost & Risk Trade-offs:**
  - *Cache Invalidation & Consistency Risk:* In distributed financial systems, stale cache data can lead to false negatives (e.g., an attacker executing 5 transactions across different channels within 2 seconds might bypass velocity checks if caches are out of sync).
  - *Architectural Rationale:* Mitigated by setting aggressive Time-To-Live (TTL) values (e.g., 60 seconds on velocity keys) and using Redis atomic operations (`INCRBY`, `EXPIRE`) to guarantee consistency without distributed locking.

---

#### 4. Event-Driven Architecture (EDA) & Event Sourcing
* **The Architecture:** All core state transitions are captured as an immutable sequence of events published to Apache Kafka and archived in S3 WORM storage. State is derived by replaying events.
* **Benefits in Financial Context:**
  - *Auditability & Non-Repudiation:* Financial regulations strictly prohibit updating database records "in-place" without an immutable audit trail. Event sourcing inherently provides non-repudiation: every decision is provably linked to the exact event stream that triggered it.
  - *Time-Travel Debugging:* If an ML model misclassifies a transaction or an automated rule fails, engineers can reconstruct the exact system state at that microsecond by replaying events up to that timestamp.
* **Cost & Risk Trade-offs:**
  - *Eventual Consistency:* Downstream views (such as the analyst case queue) are eventually consistent with the transaction ingestion stream (typically by < 100ms).
  - *Architectural Rationale:* In fraud operations, sub-second eventual consistency is completely acceptable because human analyst triage operates on human reaction timescales (seconds), whereas transaction capture remains strictly consistent and durable in Kafka.
"""

def get_html():
    return """
<section id="section-7" class="report-section">
  <div class="section-header">
    <span class="section-number">07</span>
    <div class="section-title-wrap">
      <h2>Architectural Patterns Evaluation &amp; Cost-Benefit Analysis</h2>
      <p class="section-subtitle">Evaluating Service Mesh, Backend-for-Frontend, Multi-Tier Caching, and Event Sourcing against financial risk.</p>
    </div>
  </div>

  <h3>7.1 Cross-Cutting Architectural Patterns Matrix</h3>
  <div class="table-container">
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 18%;">Architectural Pattern</th>
          <th style="width: 27%;">Scalability Contribution</th>
          <th style="width: 27%;">Resilience Contribution</th>
          <th style="width: 28%;">Security &amp; Governance Contribution</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Service Mesh</strong><br>(Istio / Envoy)</td>
          <td>Decouples networking from code; enables fine-grained client-side load balancing.</td>
          <td>Transparent circuit breakers, retries with jitter, and canary traffic shifting.</td>
          <td><span class="badge badge-primary">Zero-Trust mTLS:</span> Automated X.509 certificate rotation every 24h; strict PCI-DSS v4.0 compliance.</td>
        </tr>
        <tr>
          <td><strong>Backend-for-Frontend</strong><br>(BFF Pattern)</td>
          <td>Shields core services from chatty UI traffic; multiplexes 500+ analyst connections.</td>
          <td>Isolates UI crashes from payment pipelines; graceful degradation on DB errors.</td>
          <td><span class="badge badge-success">Data Masking:</span> Sanitizes card tokens before browser rendering; enforces fine-grained OIDC RBAC.</td>
        </tr>
        <tr>
          <td><strong>Multi-Tier Caching</strong><br>(L1 Local + L2 Redis)</td>
          <td>Offloads 95% of state reads from databases; supports 100,000+ ops/sec for velocity.</td>
          <td>Local L1 cache serves heuristic defaults if the distributed Redis cluster fails over.</td>
          <td><span class="badge badge-warning">Encrypted State:</span> TLS in-transit and AES-256 at-rest; ephemeral keys expire via automated TTLs.</td>
        </tr>
        <tr>
          <td><strong>Event Sourcing &amp; EDA</strong><br>(Apache Kafka)</td>
          <td>Scales linearly with topic partitions; supports 1,000 to 10,000+ TPS seamlessly.</td>
          <td>Absorbs extreme traffic bursts; isolates service outages; enables replay reconstruction.</td>
          <td><span class="badge badge-primary">Immutable Provenance:</span> Non-repudiable audit log fulfilling BCBS 239 and Basel III legal standards.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h3>7.2 Critical Cost-Benefit &amp; Risk Rationale</h3>
  <div class="card-grid">
    <div class="info-card">
      <div class="card-title">Service Mesh Latency Overhead</div>
      <p>Envoy sidecars introduce 0.8ms to 1.5ms of network hop latency. In our 45ms execution budget, this overhead represents ~5% of total budget. The trade-off is decisively justified by automated mutual TLS 1.3 encryption across all pods and granular canary release controls.</p>
    </div>
    <div class="info-card">
      <div class="card-title">Eventual Consistency in Fraud Operations</div>
      <p>Event-driven choreography introduces sub-second eventual consistency (&lt; 100ms) between transaction occurrence and analyst UI queue insertion. In financial fraud operations, this microsecond delay is completely imperceptible to human operators while providing 100% decoupling.</p>
    </div>
  </div>
</section>
"""

