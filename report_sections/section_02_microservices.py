"""
Section 2: Functional Decomposition & Core Microservices Architecture
"""

def get_markdown():
    return r"""## 2. Functional Decomposition & Core Microservices Architecture

### 2.1 Bounded Contexts & Decomposition Rationale
In accordance with Domain-Driven Design (DDD) principles, the fraud detection problem domain is partitioned into distinct, loosely coupled bounded contexts. Monolithic architectures fail at high throughput because stateful feature accumulation, GPU-intensive machine learning inference, high-frequency human analyst querying, and regulatory archival compete for identical memory, CPU, and thread pool resources.

By decoupling these workloads into six specialized microservices, each service scales independently according to its compute and I/O characteristics:

```
[ Ingress Rails ] ──► [ Ingestion Gateway (IGS) ] ──► [ Kafka: trans.raw.v1 ]
                                                              │
                    ┌─────────────────────────────────────────┴─────────────────────────┐
                    ▼                                                                   ▼
       [ Feature Aggregator (FAS) ]                                        [ Compliance & Replay (CAR) ]
                    │ (Redis L2 State)                                                  │
                    ▼                                                      (S3 Object Lock WORM)
       [ Kafka: trans.enriched.v1 ]
                    │
                    ▼
       [ Fraud Scoring Engine (FSE) ] ──► [ Kafka: fraud.evaluated.v1 ]
                    │                                   │
                    ▼ (Score >= 0.75)                   ▼
         [ Kafka: fraud.alert.v1 ]           [ Downstream Action Svc (NDS) ]
                    │                                   │
                    ▼                        (Card Freeze / 3DS Push)
       [ Case Management BFF (CMS) ]
                    │ (WSS Push)
                    ▼
       [ Analyst Web Console (UI) ]
```

---

### 2.2 Detailed Microservice Specifications

#### Service 1: Ingestion Gateway Service (IGS)
* **Primary Responsibility:** Acts as the high-throughput, perimeter security and validation gateway for all inbound financial transactions originating from card networks (Visa/Mastercard), instant rails (FedNow/SEPA Instant), SWIFT, digital banking apps, and core ledger services.
* **Core Functions:**
  1. *Perimeter Authentication & Authorization:* Enforces Mutual TLS (mTLS 1.3) and verifies JSON Web Tokens (JWT) / OAuth2 scopes.
  2. *Schema Validation & Normalization:* Validates incoming ISO 8583 / ISO 20022 / JSON payloads against strict Avro schemas.
  3. *PII Tokenization & HSM Integration:* Interacts with a Hardware Security Module (HSM) / HashiCorp Vault to tokenize Primary Account Numbers (PAN), replacing sensitive PANs with format-preserving tokens (`tkn_pan_89104`).
  4. *Distributed Tracing Context Injection:* Extracts or generates W3C `traceparent` headers and injects them into the transaction metadata.
  5. *Idempotent Event Emission:* Computes a canonical SHA-256 idempotency hash across `(account_id, amount, merchant_id, timestamp)` to filter duplicate requests before publishing to Kafka.
* **Inputs:** Synchronous HTTPS / gRPC POST requests containing raw financial transaction payloads.
* **Outputs:**
  - Emits `TransactionReceivedEvent` to Kafka topic `financial.trans.received.v1`.
  - Returns `HTTP 202 Accepted` with a tracking `transaction_id` for asynchronous flows, or blocks for synchronous inline verdicts.
* **Trigger:** Synchronous HTTP/gRPC invocation from payment networks or digital channels.
* **Implementation Tech:** Go 1.23 for minimal memory footprint, zero GC-pause overhead, and sub-millisecond execution.

---

#### Service 2: Feature Aggregation & State Service (FAS)
* **Primary Responsibility:** Maintains real-time temporal and spatial feature state across sliding time windows (1 minute, 5 minutes, 1 hour, 24 hours, 30 days) to compute velocity, behavioral divergence, and geographical feasibility metrics.
* **Core Functions:**
  1. *Sliding Window Velocity Accumulation:* Computes transaction counts, aggregate transaction sums, and standard deviation curves per account and per card token over rolling windows.
  2. *Geographic Velocity Analysis:* Calculates the Haversine distance between current transaction IP/terminal GPS and the last known transaction location, dividing by elapsed time to identify "impossible travel" velocity (> 800 km/h).
  3. *Cross-Channel Divergence:* Tracks distinct merchant category codes (MCC), international IP addresses, and sudden deviations from cardholder baselines.
  4. *Distributed State Interaction:* Reads and mutates low-latency in-memory state stored in a distributed Redis Enterprise cluster.
* **Inputs:** Consumes `TransactionReceivedEvent` from Kafka topic `financial.trans.received.v1`.
* **Outputs:** Emits `TransactionEnrichedEvent` (containing raw transaction data + computed 48-dimensional feature vector) to Kafka topic `financial.trans.enriched.v1`.
* **Trigger:** Asynchronous message arrival on `financial.trans.received.v1`.
* **Implementation Tech:** Apache Flink / Kafka Streams with RocksDB local state backend and Redis Enterprise L2 caching.

---

#### Service 3: Fraud Scoring & Evaluation Engine Service (FSE)
* **Primary Responsibility:** Evaluates enriched transactions using a dual-stage decisioning pipeline combining deterministic business rules with machine learning inference models to assign an actionable fraud probability score.
* **Core Functions:**
  1. *Deterministic Rule Pipeline (Stage 1):* Executes pre-compiled boolean rules (OFAC sanctions blacklists, hard-blocked BIN lists, impossible travel flags, velocity threshold breaches).
  2. *Machine Learning Inference Pipeline (Stage 2):* Dispatches the normalized feature vector to Triton Inference Server, executing an ensemble of:
     - **LightGBM / XGBoost Model (ONNX Runtime):** Highly optimized for tabular tabular feature scoring (< 4ms).
     - **Deep Autoencoder Anomaly Detector (PyTorch / TensorRT):** Identifies novel, unseen fraud patterns based on reconstruction error.
  3. *Explainable AI (XAI) Attribution:* Computes TreeSHAP (SHapley Additive exPlanations) values to extract the top 5 predictive features contributing to the fraud score (e.g., `+0.42` due to velocity spike, `+0.31` due to foreign IP).
  4. *Decision Thresholding:* Classifies transaction into:
     - `ALLOW` (Risk Score $S < 0.50$)
     - `CHALLENGE / REVIEW` ($0.50 \le S < 0.75$)
     - `BLOCK / HIGH FRAUD` ($S \ge 0.75$)
* **Inputs:** Consumes `TransactionEnrichedEvent` from Kafka topic `financial.trans.enriched.v1`.
* **Outputs:**
  - Emits `FraudEvaluatedEvent` for all transactions to `financial.fraud.evaluated.v1`.
  - Emits `FraudAlertRaisedEvent` to `financial.fraud.alert.v1` for transactions with $S \ge 0.75$.
* **Trigger:** Asynchronous message arrival on `financial.trans.enriched.v1`.
* **Implementation Tech:** C++ / Python Triton Inference Server containerized on GPU/CPU node pools, managed via Quarkus/Go orchestration sidecars.

---

#### Service 4: Case Management & Analyst Gateway (BFF) Service (CMS)
* **Primary Responsibility:** Acts as the Backend-for-Frontend (BFF) orchestrator and case state machine for fraud operations teams, routing alerts to human analysts in real time and managing case lifecycles.
* **Core Functions:**
  1. *Alert Aggregation & View Model Construction:* Merges Kafka fraud alert events with historical account records from PostgreSQL, customer KYC profiles, and device fingerprint intelligence to create an analyst-optimized View Model.
  2. *Real-Time Push Streaming:* Maintains active WebSocket (WSS / STOMP) persistent connections to authenticated fraud analyst browsers, pushing high-priority alerts with sub-200ms latency.
  3. *Case Lifecycle State Machine:* Enforces valid case state transitions:
     $$\text{NEW} \longrightarrow \text{ASSIGNED} \longrightarrow \text{UNDER\_INVESTIGATION} \longrightarrow \{\text{CONFIRMED\_FRAUD} \mid \text{FALSE\_POSITIVE}\}$$
  4. *Analyst Action Handling:* Accepts triage decisions (e.g., "Confirm Fraud & Block Card", "Mark False Positive & Whitelist"), writes case notes, records analyst identity, and issues audit events.
* **Inputs:**
  - Consumes `FraudAlertRaisedEvent` from Kafka topic `financial.fraud.alert.v1`.
  - Inbound WebSocket connections and REST/GraphQL mutations from the Analyst Console.
* **Outputs:**
  - Real-time WebSocket push frames to fraud analyst web clients.
  - CRUD operations against Amazon Aurora PostgreSQL Multi-AZ Case Database.
  - Emits `CaseStatusChangedEvent` to Kafka topic `case.events.v1`.
* **Trigger:** Kafka alert events or analyst UI HTTP/WebSocket requests.
* **Implementation Tech:** Node.js 22 (Fastify) / TypeScript for asynchronous WebSocket connection handling, backed by Prisma / PgBouncer.

---

#### Service 5: Compliance, Audit & Replay Service (CAR)
* **Primary Responsibility:** Provides immutable, Write-Once-Read-Many (WORM) audit archiving and deterministic replay capabilities across the entire transaction lifecycle to satisfy BCBS 239, Basel III, PCI-DSS v4.0, and regulatory audits.
* **Core Functions:**
  1. *Continuous Stream Archival:* Consumes from all production Kafka topics (`trans.raw`, `trans.enriched`, `fraud.evaluated`, `case.events`), buffering them into 60-second micro-batches.
  2. *Columnar Compaction & Deduplication:* Compresses events into Apache Parquet format using Zstandard (ZSTD) compression (yielding ~6:1 compression ratios) and indexes them via Apache Iceberg.
  3. *WORM Immutability Enforcement:* Writes Parquet partitions into Amazon S3 / Google Cloud Storage with **Object Lock enabled in Compliance Mode** (retention period locked for 7 years; cannot be overwritten or deleted even by the cloud root account).
  4. *Deterministic Replay Orchestrator:* Exposes an administrative API allowing compliance officers or data scientists to specify a historical timeframe $[T_1, T_2]$, spin up isolated replay worker pods, and inject historical transactions into an isolated replay Kafka topic (`compliance.trans.replay.v1`) to evaluate new candidate ML models against historical ground truth without contaminating production metrics.
  5. *Reconciliation & Parity Auditing:* Executes hourly verification jobs ensuring total ingested transactions match total archived transactions ($\Delta = 0$).
* **Inputs:** Consumes all domain events from Kafka topics; receives replay invocation parameters via Admin API.
* **Outputs:**
  - Immutable Iceberg Parquet files in S3/GCS Object Lock storage.
  - Replayed transaction events published to isolated topic `compliance.trans.replay.v1`.
  - Cryptographically signed audit reconciliation reports.
* **Trigger:** Continuous event consumption from Kafka; on-demand execution via Compliance Admin API.
* **Implementation Tech:** Go / Java Spark Archiver worker pods with AWS S3 Object Lock SDK.

---

#### Service 6: Notification & Downstream Action Service (NDS)
* **Primary Responsibility:** Translates automated fraud scoring decisions and analyst dispositions into real-time operational enforcement actions across the bank's core infrastructure.
* **Core Functions:**
  1. *Automated Pre-Emptive Card Freeze:* Dispatches gRPC commands to the Card Issuer Processor (Visa DPS / Mastercard DebitSwitch) to freeze compromised card tokens immediately.
  2. *Payment Settlement Holding:* Instructs Core Banking ledger engines to place a suspense hold on outgoing real-time clearing transfers (FedNow/SEPA).
  3. *Step-Up 3DS & Customer Verification:* Interacts with notification gateways (Twilio, Apple Push Notification Service, Firebase Cloud Messaging) to send real-time push challenges or SMS One-Time Passwords (OTP) to the cardholder.
* **Inputs:** Consumes `FraudEvaluatedEvent` (filtered for risk score $S \ge 0.75$) and `CaseStatusChangedEvent` (for manual analyst confirmations).
* **Outputs:** Synchronous gRPC / Webhook calls to Core Banking, Card Issuer APIs, and Push Notification Providers.
* **Trigger:** High-risk evaluation event or analyst case confirmation event.
* **Implementation Tech:** Java Quarkus (Reactive Engine) with Mutiny and resilience circuit breakers (MicroProfile Fault Tolerance).

---

### 2.3 Inter-Service Coupling & Communication Analysis
Architectural coupling directly influences system availability, latency, and operational risk in a financial ecosystem. The table below analyzes the coupling dimensions across the platform:

| Coupling Dimension | Platform Characteristic & Mitigation | Architectural Assessment |
| :--- | :--- | :--- |
| **Afferent vs. Efferent Coupling** | Core domain services (FSE, FAS) have low efferent coupling (they only depend on Kafka and their local/cache state). Ingestion Gateway has high afferent coupling (entry point) but zero direct downstream service dependencies. | **Exceptional Fault Isolation:** A failure in Case Management or Triton ML cannot cascade upstream to crash Ingestion. |
| **Temporal Coupling** | With the exception of the optional synchronous payment gate, all inter-service communication is asynchronous via Kafka log persistence. | **Zero Temporal Coupling:** Ingestion continues to acknowledge payments even if Feature Aggregation or Case Management is temporarily undergoing pod rolling upgrades. |
| **Schema Coupling** | Microservices exchange strictly versioned binary Avro records validated by an enterprise Schema Registry (Confluent / Karapace). Schema evolution rules enforce backward and forward compatibility (Full Transitive Compatibility). | **Managed Schema Coupling:** Fields can be added with default values without breaking upstream producers or downstream consumers. |
| **Deployment Coupling** | Each microservice is packaged as an independent container, deployed via GitOps (ArgoCD), and managed under its own CI/CD pipeline and semantic versioning tag. | **Zero Deployment Coupling:** Teams can deploy a new version of the Fraud Scoring Engine without re-deploying Ingestion or Case Management. |
"""

def get_html():
    return """
<section id="section-2" class="report-section">
  <div class="section-header">
    <span class="section-number">02</span>
    <div class="section-title-wrap">
      <h2>Functional Decomposition &amp; Core Microservices Architecture</h2>
      <p class="section-subtitle">Domain boundaries, responsibilities, input/output schemas, triggers, and coupling analysis.</p>
    </div>
  </div>

  <h3>2.1 Bounded Contexts &amp; Functional Decomposition</h3>
  <p>In accordance with Domain-Driven Design (DDD) principles, the fraud detection problem domain is partitioned into distinct, loosely coupled bounded contexts. Monolithic architectures fail at high throughput because stateful feature accumulation, GPU-intensive machine learning inference, high-frequency human analyst querying, and regulatory archival compete for identical memory, CPU, and thread pool resources.</p>
  <p>By decoupling these workloads into six specialized microservices, each service scales independently according to its compute and I/O characteristics:</p>

  <div class="microservice-grid">
    <!-- Service 1 -->
    <div class="microservice-card">
      <div class="ms-header">
        <span class="ms-code">IGS</span>
        <div class="ms-title-block">
          <h4>1. Ingestion Gateway Service</h4>
          <span class="ms-tech">Go 1.23 | KEDA Scaled</span>
        </div>
      </div>
      <p class="ms-desc">Perimeter ingress, mTLS termination, schema validation, rate-limiting, HSM PAN tokenization, W3C trace injection, and idempotent raw event publishing.</p>
      <div class="ms-io-box">
        <div><strong>Inputs:</strong> Synchronous HTTPS / gRPC POST (ISO 8583 / ISO 20022 / JSON).</div>
        <div><strong>Outputs:</strong> <code>financial.trans.received.v1</code> event to Kafka; HTTP 202 Accepted.</div>
        <div><strong>Trigger:</strong> External payment network API or digital banking rail.</div>
      </div>
    </div>

    <!-- Service 2 -->
    <div class="microservice-card">
      <div class="ms-header">
        <span class="ms-code" style="background:#059669;">FAS</span>
        <div class="ms-title-block">
          <h4>2. Feature Aggregation Service</h4>
          <span class="ms-tech">Apache Flink / Kafka Streams | Redis L2</span>
        </div>
      </div>
      <p class="ms-desc">Real-time stateful stream processing computing velocity sliding windows (5m, 1h, 24h), geographic impossible travel distance, and spending deviations.</p>
      <div class="ms-io-box">
        <div><strong>Inputs:</strong> Consumes <code>financial.trans.received.v1</code> from Kafka; reads/writes Redis.</div>
        <div><strong>Outputs:</strong> Emits <code>financial.trans.enriched.v1</code> with 48-dim feature vector.</div>
        <div><strong>Trigger:</strong> Message arrival on raw transaction topic.</div>
      </div>
    </div>

    <!-- Service 3 -->
    <div class="microservice-card">
      <div class="ms-header">
        <span class="ms-code" style="background:#dc2626;">FSE</span>
        <div class="ms-title-block">
          <h4>3. Fraud Scoring Engine</h4>
          <span class="ms-tech">Triton Inference | LightGBM + Autoencoder</span>
        </div>
      </div>
      <p class="ms-desc">Dual-stage evaluation: Deterministic rules (sanctions, blacklists) + Triton ML ensemble. Generates risk probability score and TreeSHAP explainability attributions in &lt;15ms.</p>
      <div class="ms-io-box">
        <div><strong>Inputs:</strong> Consumes <code>financial.trans.enriched.v1</code> from Kafka.</div>
        <div><strong>Outputs:</strong> Emits <code>financial.fraud.evaluated.v1</code> and <code>financial.fraud.alert.v1</code>.</div>
        <div><strong>Trigger:</strong> Message arrival on enriched transaction topic.</div>
      </div>
    </div>

    <!-- Service 4 -->
    <div class="microservice-card">
      <div class="ms-header">
        <span class="ms-code" style="background:#7c3aed;">CMS</span>
        <div class="ms-title-block">
          <h4>4. Case Management &amp; BFF</h4>
          <span class="ms-tech">Node.js 22 Fastify | PostgreSQL Aurora</span>
        </div>
      </div>
      <p class="ms-desc">Backend-for-Frontend (BFF) orchestrating alert lifecycle, case state machine, analyst assignments, and real-time push streaming over WebSockets (WSS/STOMP) to analyst UI.</p>
      <div class="ms-io-box">
        <div><strong>Inputs:</strong> Consumes <code>financial.fraud.alert.v1</code>; WebSocket &amp; REST analyst requests.</div>
        <div><strong>Outputs:</strong> Real-time WSS frames; Case DB updates; emits <code>case.events.v1</code>.</div>
        <div><strong>Trigger:</strong> Fraud alert event or analyst web interaction.</div>
      </div>
    </div>

    <!-- Service 5 -->
    <div class="microservice-card">
      <div class="ms-header">
        <span class="ms-code" style="background:#9333ea;">CAR</span>
        <div class="ms-title-block">
          <h4>5. Compliance, Audit &amp; Replay</h4>
          <span class="ms-tech">Go / Spark | S3 Object Lock WORM</span>
        </div>
      </div>
      <p class="ms-desc">Immutable WORM archiving of all streams to S3 Object Lock in Compliance Mode (7-year retention). Manages deterministic historical replay into isolated shadow topics.</p>
      <div class="ms-io-box">
        <div><strong>Inputs:</strong> Consumes all domain Kafka topics; Admin Replay API triggers.</div>
        <div><strong>Outputs:</strong> Parquet/Iceberg datasets; publishes to <code>compliance.trans.replay.v1</code>.</div>
        <div><strong>Trigger:</strong> Continuous stream consumption; Admin API invocation.</div>
      </div>
    </div>

    <!-- Service 6 -->
    <div class="microservice-card">
      <div class="ms-header">
        <span class="ms-code" style="background:#0284c7;">NDS</span>
        <div class="ms-title-block">
          <h4>6. Downstream Action Service</h4>
          <span class="ms-tech">Java Quarkus Reactive | Core Banking gRPC</span>
        </div>
      </div>
      <p class="ms-desc">Executes automated enforcement actions: Pre-emptive card freeze via Card Processor, settlement suspense hold on Core Banking, and 3DS push challenge dispatch to cardholders.</p>
      <div class="ms-io-box">
        <div><strong>Inputs:</strong> Consumes <code>financial.fraud.evaluated.v1</code> and <code>case.events.v1</code>.</div>
        <div><strong>Outputs:</strong> gRPC / Webhook calls to Core Banking, Card Issuer APIs, Twilio.</div>
        <div><strong>Trigger:</strong> High-risk score evaluation or confirmed analyst disposition.</div>
      </div>
    </div>
  </div>

  <h3>2.2 Inter-Service Coupling &amp; Communication Analysis</h3>
  <p>Architectural coupling directly influences system availability, latency, and operational risk in a financial ecosystem. The table below analyzes the coupling dimensions across the platform:</p>

  <div class="table-container">
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 25%;">Coupling Dimension</th>
          <th style="width: 45%;">Platform Characteristic &amp; Mitigation</th>
          <th style="width: 30%;">Architectural Assessment</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Afferent vs. Efferent Coupling</strong></td>
          <td>Core domain services (FSE, FAS) have low efferent coupling (they only depend on Kafka and local/cache state). Ingestion Gateway has high afferent coupling (perimeter entry) but zero direct downstream service dependencies.</td>
          <td><span class="badge badge-success">Fault Isolation:</span> Failures in Case Management or Triton ML cannot cascade upstream to crash Ingestion.</td>
        </tr>
        <tr>
          <td><strong>Temporal Coupling</strong></td>
          <td>With the exception of the optional synchronous payment gate, all inter-service communication is asynchronous via Kafka log persistence.</td>
          <td><span class="badge badge-success">Zero Temporal Coupling:</span> Ingestion acknowledges payments even if downstream consumers are undergoing rolling restarts.</td>
        </tr>
        <tr>
          <td><strong>Schema Coupling</strong></td>
          <td>Microservices exchange strictly versioned binary Avro records validated by an enterprise Schema Registry (Confluent / Karapace). Schema evolution rules enforce backward and forward compatibility (Full Transitive Compatibility).</td>
          <td><span class="badge badge-primary">Managed Evolution:</span> Fields can be added with default values without breaking upstream producers or downstream consumers.</td>
        </tr>
        <tr>
          <td><strong>Deployment Coupling</strong></td>
          <td>Each microservice is packaged as an independent container, deployed via GitOps (ArgoCD), and managed under its own CI/CD pipeline and semantic versioning tag.</td>
          <td><span class="badge badge-success">Zero Deployment Coupling:</span> ML scoring models or frontend BFF services deploy independently without coordination.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
"""