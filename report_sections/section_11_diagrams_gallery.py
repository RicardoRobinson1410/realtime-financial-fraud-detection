"""
Section 11: Architecture Diagrams Gallery & Visual Walkthrough
"""

from build_diagrams import (
    get_diagram_1,
    get_diagram_2,
    get_diagram_3,
    get_diagram_4,
    get_diagram_5,
    get_diagram_6
)

def get_markdown():
    return """## 11. Architecture Diagrams Gallery & Visual Walkthrough

This section provides a structured visual walkthrough of the six core architectural diagrams that underpin the Next-Generation Real-Time Fraud Detection Platform.

---

### Figure 1: Solution Architecture Diagram (C4 Container View)
* **Architectural Purpose:** Provides a comprehensive macro-level structural view of the solution, illustrating external payment ingress channels, perimeter security gateways, core microservices within the Kubernetes service mesh, the Apache Kafka event backbone, the distributed Redis cache, the ML Triton inference cluster, the Analyst Console, the WORM compliance lakehouse, and the unified observability plane.
* **Component Interactions & Data Flow:**
  1. *Perimeter Ingress:* Card networks (Visa/MC), Instant Rails (FedNow/SEPA Instant), Core Banking, and Digital Channels route traffic through Envoy/Kong Edge Gateways (handling WAF, mTLS, and HSM PAN tokenization).
  2. *Microservices Core:* The Go-based Ingestion Gateway publishes raw events to Apache Kafka. The Feature Aggregator maintains temporal sliding windows in Redis. The Fraud Scoring Engine coordinates deterministic rules with Triton ML inference.
  3. *Downstream & Operations:* Evaluated high-risk events trigger automated card holds via the Downstream Action Service, while alerting fraud analysts in real time over WebSockets managed by the Analyst BFF.
  4. *Compliance & Observability:* All events stream continuously into S3 WORM storage for 7-year audit retention, while OpenTelemetry collectors capture metrics, traces, and logs.

*(See Figure 1 embedded in the compiled PDF deliverable and `diagrams/diagram_1_solution_architecture.svg`)*

---

### Figure 2: Event-Driven Messaging Backbone & Exactly-Once Scaling Architecture
* **Architectural Purpose:** Details the asynchronous pub/sub messaging architecture, topic partition topologies (32 partitions keyed by `account_id`), Avro schema registry governance, consumer groups, Dead-Letter Queue (DLQ) poison-pill quarantine mechanisms, and the **Exactly-Once Horizontal Scaling Lifecycle** (CooperativeStickyAssignor, ConsumerRebalanceListeners, Kafka Transactional API offset commits, and atomic database sink commits).
* **Topic Routing & Consumer Flow:**
  - `financial.trans.received.v1` (Produced by Ingestion Gateway $\to$ Consumed by Feature Aggregator with CooperativeStickyAssignor & Compliance Archiver).
  - `financial.trans.enriched.v1` (Produced by Feature Aggregator via Transactional EOS $\to$ Consumed by Fraud Scoring Engine & Compliance Archiver).
  - `financial.fraud.evaluated.v1` (Produced by Scoring Engine via Transactional EOS $\to$ Consumed by Downstream Action Service & Compliance Archiver).
  - `financial.fraud.alert.v1` (Produced by Scoring Engine $\to$ Consumed by Case Management BFF via Atomic PostgreSQL Sink commits).
  - `case.events.v1` (Produced by Case BFF $\to$ Consumed by Downstream Enforcement, ML Training Store & Compliance Archiver).
  - `compliance.trans.replay.v1` (Produced by Replay Coordinator $\to$ Consumed by Shadow Scoring Engine in isolation).

*(See Figure 2 embedded in the compiled PDF deliverable and `diagrams/diagram_2_event_messaging_backbone.svg`)*

---

### Figure 3: End-to-End Transaction Flow Sequence Diagram
* **Architectural Purpose:** Traces the exact millisecond-by-millisecond journey of a high-risk financial transaction from its initial origination at a payment terminal through ingestion, stateful enrichment, machine learning classification, automated enforcement, real-time analyst alerting, and immutable compliance archival.
* **Step-by-Step Chronological Journey:**
  1. *0.0ms:* Payment network dispatches transaction payload to API Gateway.
  2. *4.0ms:* Ingestion Service validates schema, tokenizes PAN, and produces `trans.received.v1` to Kafka.
  3. *6.0ms:* Ingestion returns HTTP 202 Accepted (or holds for synchronous fast-path). S3 WORM archiver asynchronously captures raw event.
  4. *12.0ms:* Feature Aggregator consumes raw event, executes sub-millisecond Redis lookups, computes 48-feature vector, and emits `trans.enriched.v1`.
  5. *24.0ms:* Fraud Scoring Engine runs rule checks (<2ms) and Triton ML inference (<10ms). Transaction is classified as high-risk ($S = 0.94$). Emits `fraud.alert.v1`.
  6. *30.0ms:* Downstream Action Service triggers pre-emptive card freeze via Card Issuer API.
  7. *45.0ms:* Case Management BFF receives alert, writes case record to PostgreSQL, and pushes WebSocket frame to active Analyst Console.
  8. *2.5s:* Human analyst reviews SHAP radar chart, confirms fraud, and issues disposition, completing the lifecycle audit trail.

*(See Figure 3 embedded in the compiled PDF deliverable and `diagrams/diagram_3_transaction_flow_sequence.svg`)*

---

### Figure 4: Fraud Analyst Console & Backend-for-Frontend (BFF) Architecture
* **Architectural Purpose:** Illustrates the high-performance user experience architecture, showing the decoupled React 19 single-page application, DOM virtualization, client-side caching, background Web Workers, WebSocket connection hubs, Redis Pub/Sub cluster fan-out, and the PostgreSQL case repository.

*(See Figure 4 embedded in the compiled PDF deliverable and `diagrams/diagram_4_analyst_frontend_bff.svg`)*

---

### Figure 5: Enterprise Observability & Telemetry Correlation Architecture
* **Architectural Purpose:** Details the OpenTelemetry instrumentation pipeline, demonstrating how metrics, distributed traces, and structured logs are correlated via W3C TraceContext headers and Prometheus Exemplars, enabling single-click incident diagnosis from metric spikes directly to pod logs.

*(See Figure 5 embedded in the compiled PDF deliverable and `diagrams/diagram_5_enterprise_observability.svg`)*

---

### Figure 6: Compliance Audit, Immutable Storage & Historical Replay Subsystem
* **Architectural Purpose:** Delineates the Write-Once-Read-Many (WORM) storage architecture, S3 Object Lock compliance configuration, Apache Iceberg partitioning, and the isolated historical replay pipeline used for regulatory auditing and candidate machine learning model backtesting.

*(See Figure 6 embedded in the compiled PDF deliverable and `diagrams/diagram_6_compliance_audit_replay.svg`)*
"""

def get_html():
    diag1 = get_diagram_1()
    diag2 = get_diagram_2()
    diag3 = get_diagram_3()
    diag4 = get_diagram_4()
    diag5 = get_diagram_5()
    diag6 = get_diagram_6()
    
    return f"""
<section id="section-11" class="report-section page-break-before">
  <div class="section-header">
    <span class="section-number">11</span>
    <div class="section-title-wrap">
      <h2>Architecture Diagrams Gallery &amp; Visual Walkthrough</h2>
      <p class="section-subtitle">Comprehensive visual aids illustrating component interactions, event flows, journeys, and telemetry.</p>
    </div>
  </div>

  <div class="diagram-wrapper page-break-before">
    <div class="diagram-container">
      {diag1}
    </div>
    <div class="diagram-caption">
      <strong>Figure 1: Solution Architecture Diagram (C4 Container View)</strong> &mdash; Microservices mesh, Apache Kafka event backbone, Redis state cache, Triton inference cluster, Analyst BFF, and WORM compliance lakehouse.
    </div>
  </div>

  <div class="diagram-wrapper page-break-before">
    <div class="diagram-container">
      {diag2}
    </div>
    <div class="diagram-caption">
      <strong>Figure 2: Event-Driven Messaging Backbone &amp; Exactly-Once Scaling Architecture</strong> &mdash; 32 partitions per topic, partition key routing by account_id, schema registry governance, CooperativeStickyAssignor, ConsumerRebalanceListeners, and atomic offset commit protocols.
    </div>
  </div>

  <div class="diagram-wrapper page-break-before">
    <div class="diagram-container">
      {diag3}
    </div>
    <div class="diagram-caption">
      <strong>Figure 3: End-to-End Transaction Flow Sequence Diagram</strong> &mdash; Millisecond-by-millisecond transaction journey through ingestion, feature enrichment, Triton ML classification, automated enforcement, analyst WebSocket push, and WORM audit.
    </div>
  </div>

  <div class="diagram-wrapper page-break-before">
    <div class="diagram-container">
      {diag4}
    </div>
    <div class="diagram-caption">
      <strong>Figure 4: Fraud Analyst Console &amp; Backend-for-Frontend (BFF) Architecture</strong> &mdash; React 19 SPA, DOM virtualization (TanStack Virtual), Web Worker background computing, WebSocket push hub, and Redis Pub/Sub cluster fan-out.
    </div>
  </div>

  <div class="diagram-wrapper page-break-before">
    <div class="diagram-container">
      {diag5}
    </div>
    <div class="diagram-caption">
      <strong>Figure 5: Enterprise Observability &amp; Telemetry Correlation Architecture</strong> &mdash; Unified OpenTelemetry pipeline, Prometheus Golden Signals metrics, Tempo distributed tracing, Loki structured logging, and Prometheus Exemplar cross-linking.
    </div>
  </div>

  <div class="diagram-wrapper page-break-before">
    <div class="diagram-container">
      {diag6}
    </div>
    <div class="diagram-caption">
      <strong>Figure 6: Compliance Audit, Immutable Storage &amp; Historical Replay Subsystem</strong> &mdash; Continuous S3 Object Lock WORM ingestion (7-year retention), Apache Iceberg lakehouse compaction, and isolated deterministic replay pipeline for model backtesting.
    </div>
  </div>
</section>
"""