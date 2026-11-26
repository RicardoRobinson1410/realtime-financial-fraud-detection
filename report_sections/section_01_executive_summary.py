"""
Section 1: Executive Summary & Project Context
"""

def get_markdown():
    return r"""# Next-Generation Cloud-Native Real-Time Financial Fraud Detection Platform
## Solution Architecture & Operationalization Report

**Document Reference:** `SAR-FINFRAUD-2026-V1.0`  
**Classification:** Internal Highly Confidential — Enterprise Architecture & Risk Governance  
**Author:** Principal Solutions Architect, Financial Services Cloud Architecture  
**Stakeholder Distribution:** Enterprise Architecture Board, Chief Risk Officer (CRO), Chief Information Security Officer (CISO), VP of Engineering, Financial Regulatory Compliance  
**Target Environment:** Multi-Zone Cloud-Native Infrastructure (AWS / Azure / GCP)  
**System Baseline:** Peak 1,000 TPS Sustained | P99 Latency < 45ms | 100% WORM Compliance Replayability  

---

## 1. Executive Summary & Project Context

### 1.1 The Business Challenge & Regulatory Imperative
For over a decade, the financial institution relied on a monolithic, batch-oriented fraud detection engine. Designed in an era of multi-day clearing cycles, this legacy platform processed transaction logs during overnight batch processing windows ($T+1$ to $T+3$). While the institution has successfully migrated and uplifted the vast majority of its core retail and commercial banking services to a cloud-native topology, this legacy fraud system remained a critical vulnerability and the single largest operational laggard in the bank's architecture.

The batch paradigm imposes severe business liabilities and existential regulatory risks:
1. **Capital Slippage & Unrecoverable Losses:** Fraudulent transactions (such as account takeovers, credential stuffing, authorized push payment fraud, and synthetic identity card rings) are identified hours or days after funds have cleared and exited the banking rail. By the time an analyst reviews an overnight batch report, funds have been laundered across multiple crypto off-ramps or offshore accounts, resulting in tens of millions of dollars in net annual charge-off losses.
2. **Impending Legal & Regulatory Compliance Mandates:** Financial regulators globally have mandated real-time fraud monitoring. In the United States, the Federal Reserve's **FedNow** instant clearing network and the Clearing House's Real-Time Payments (RTP) require immediate transaction validation. In the European Union, the **Instant Payments Regulation (IPR)** mandates 24/7 instant euro transfers within 10 seconds, coupled with mandatory Verification of Payee (VoP). In the United Kingdom, the **Payment Systems Regulator (PSR)** rules enforce mandatory 50:50 reimbursement of Authorized Push Payment (APP) fraud by sending and receiving banks within five business days, radically shifting fraud liability directly onto the balance sheet of the institution.
3. **Basel Committee on Banking Supervision (BCBS 239) & Basel III Operational Risk:** Global regulatory bodies require institutions to maintain absolute risk data aggregation capabilities, immutable transaction provenance, and deterministic audit replayability for a minimum of seven years. Failing to provide bit-for-bit replay of historical transactions through the exact decisioning pipeline during a regulatory audit incurs severe administrative sanctions and increased capital reserve requirements.

To resolve these systemic deficiencies, the bank has committed capital investment to design and operationalize a **Next-Generation Real-Time Financial Fraud Detection System**.

---

### 1.2 System Requirements & Technical Problem Decomposition
The core mandate is to translate high-level business drivers into rigorous, measurable engineering objectives:

| Business & Regulatory Requirement | Technical Challenge | Architectural Objective & SLA/SLO |
| :--- | :--- | :--- |
| **Real-Time Transaction Analysis** | Synchronous or near-real-time scoring before funds settle or exit the rail. | Sub-100ms total round-trip latency. Internal fraud scoring engine execution budget: **P99 $\le 45$ ms** at the 99th percentile. |
| **Immutable Audit & Replayability** | Basel III / BCBS 239 legal compliance requiring exact historical reconstruction. | **100% Write-Once-Read-Many (WORM)** event capture in object storage. Deterministic replay pipeline capable of replaying any historical time-slice without corrupting production state. |
| **Peak Volume Throughput** | Daily transaction peaks during business hours, Black Friday, and payroll dates. | **1,000 Transactions Per Second (TPS)** sustained baseline peak throughput, with architecture engineered for burst headroom up to 3,000 TPS. |
| **Elastic Cost-Effective Scaling** | Preventing 24/7 provisioning of peak hardware while absorbing sudden surges. | **Dynamic Horizontal Autoscaling (KEDA)** driven by Kafka topic lag and CPU/memory pressure. Dynamic range from 100 TPS (night trough) to 1,000+ TPS peak. |
| **Real-Time Analyst Operations Console** | Operations team needs immediate visibility into high-confidence fraud. | **Sub-second push alerting (< 200ms)** via WebSocket/Server-Sent Events to a virtualized React frontend, complete with Explainable AI (SHAP) feature attributions. |
| **Enterprise Observability & Operability** | Proactive failure detection, compliance reporting, and zero unmonitored blindspots. | **OpenTelemetry-native telemetry**, Prometheus metrics, Grafana Tempo distributed tracing, Loki structured logging, and formal SLOs with error budget alerting. |

---

### 1.3 Architectural Vision & Guiding Principles
To satisfy these strict non-functional requirements without compromising security or resilience, the target architecture adheres to five foundational principles:

1. **Event-Driven Choreography over Orchestration:** Eliminate single-point bottlenecks and tight coupling. Components communicate asynchronously via an event backbone (Apache Kafka), buffering unpredictable payment traffic and isolating service failures.
2. **Dual-Track Evaluation (Synchronous Gate vs. Deep Asynchronous Stream):** For card-not-present (CNP) pre-authorizations requiring an inline decline decision, provide a high-speed synchronous gRPC evaluation path (< 35ms). Simultaneously, feed the asynchronous streaming classification pipeline for full graph-based feature aggregation and case management.
3. **Immutability & Event Sourcing by Design:** Every state change, from transaction ingestion to analyst disposition, is modeled as an immutable event. The audit log is not an afterthought; it is the canonical source of truth.
4. **Zero-Trust Security & PII Protection:** Strict Mutual TLS (mTLS) 1.3 with cryptographic workload identity (SPIFFE/SPIRE) across the entire microservice mesh. Primary Account Numbers (PAN) and Personally Identifiable Information (PII) are tokenized at the edge ingress boundary, ensuring downstream analytical engines never process raw sensitive financial data.
5. **Decoupled Lifecycle for Human Analyst Operations:** The fraud analyst operations console is decoupled from the transaction processing pipeline via the Backend-for-Frontend (BFF) pattern, ensuring high analyst query volumes do not degrade transaction classification throughput.
"""

def get_html():
    return """
<section id="section-1" class="report-section">
  <div class="section-header">
    <span class="section-number">01</span>
    <div class="section-title-wrap">
      <h2>Executive Summary &amp; Project Context</h2>
      <p class="section-subtitle">Business challenges, regulatory imperatives, technical problem decomposition, and guiding principles.</p>
    </div>
  </div>

  <div class="callout callout-danger">
    <div class="callout-icon">&#9888;</div>
    <div class="callout-body">
      <h4>Urgent Regulatory Mandate</h4>
      <p>Impending instant payment mandates (FedNow, SEPA Instant, and UK PSR mandatory reimbursement rules) legally obligate financial institutions to detect and intercept fraudulent transactions in real time before funds settle. Failing to replace the legacy batch platform exposes the institution to tens of millions of dollars in unrecoverable liability and regulatory capital sanctions.</p>
    </div>
  </div>

  <h3>1.1 The Business Challenge &amp; Regulatory Imperative</h3>
  <p>For over a decade, the financial institution relied on a monolithic, batch-oriented fraud detection engine. Designed in an era of multi-day clearing cycles, this legacy platform processed transaction logs during overnight batch processing windows (T+1 to T+3). While the institution has successfully migrated and uplifted the vast majority of its core retail and commercial banking services to a cloud-native topology, this legacy fraud system remained a critical vulnerability and the single largest operational laggard in the bank's architecture.</p>

  <p>The batch paradigm imposes severe business liabilities and existential regulatory risks:</p>
  <ul class="bullet-list">
    <li><strong>Capital Slippage &amp; Unrecoverable Losses:</strong> Fraudulent transactions (such as account takeovers, credential stuffing, authorized push payment fraud, and synthetic identity card rings) are identified hours or days after funds have cleared and exited the banking rail. By the time an analyst reviews an overnight batch report, funds have been laundered across multiple crypto off-ramps or offshore accounts, resulting in tens of millions of dollars in net annual charge-off losses.</li>
    <li><strong>Impending Legal &amp; Regulatory Compliance Mandates:</strong> Financial regulators globally have mandated real-time fraud monitoring. In the United States, the Federal Reserve's <strong>FedNow</strong> instant clearing network and the Clearing House's Real-Time Payments (RTP) require immediate transaction validation. In the European Union, the <strong>Instant Payments Regulation (IPR)</strong> mandates 24/7 instant euro transfers within 10 seconds, coupled with mandatory Verification of Payee (VoP). In the United Kingdom, the <strong>Payment Systems Regulator (PSR)</strong> rules enforce mandatory 50:50 reimbursement of Authorized Push Payment (APP) fraud by sending and receiving banks within five business days, radically shifting fraud liability directly onto the balance sheet of the institution.</li>
    <li><strong>Basel Committee on Banking Supervision (BCBS 239) &amp; Basel III Operational Risk:</strong> Global regulatory bodies require institutions to maintain absolute risk data aggregation capabilities, immutable transaction provenance, and deterministic audit replayability for a minimum of seven years. Failing to provide bit-for-bit replay of historical transactions through the exact decisioning pipeline during a regulatory audit incurs severe administrative sanctions and increased capital reserve requirements.</li>
  </ul>

  <h3>1.2 System Requirements &amp; Technical Problem Decomposition</h3>
  <p>The core mandate is to translate high-level business drivers into rigorous, measurable engineering objectives:</p>

  <div class="table-container">
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 25%;">Business / Regulatory Requirement</th>
          <th style="width: 35%;">Technical Challenge</th>
          <th style="width: 40%;">Architectural Objective &amp; Target SLA/SLO</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Real-Time Transaction Analysis</strong></td>
          <td>Synchronous or near-real-time scoring before funds settle or exit the rail.</td>
          <td>Sub-100ms total round-trip latency. Internal fraud scoring engine execution budget: <span class="badge badge-success">P99 &le; 45ms</span> at the 99th percentile.</td>
        </tr>
        <tr>
          <td><strong>Immutable Audit &amp; Replayability</strong></td>
          <td>Basel III / BCBS 239 legal compliance requiring exact historical reconstruction.</td>
          <td><span class="badge badge-primary">100% WORM</span> event capture in object storage. Deterministic replay pipeline capable of replaying any historical time-slice without corrupting production state.</td>
        </tr>
        <tr>
          <td><strong>Peak Volume Throughput</strong></td>
          <td>Daily transaction peaks during business hours, Black Friday, and payroll dates.</td>
          <td><span class="badge badge-warning">1,000 TPS</span> sustained baseline peak throughput, with architecture engineered for burst headroom up to 3,000 TPS.</td>
        </tr>
        <tr>
          <td><strong>Elastic Cost-Effective Scaling</strong></td>
          <td>Preventing 24/7 provisioning of peak hardware while absorbing sudden surges.</td>
          <td><strong>Dynamic Horizontal Autoscaling (KEDA)</strong> driven by Kafka topic lag and CPU/memory pressure. Dynamic range from 100 TPS (night trough) to 1,000+ TPS peak.</td>
        </tr>
        <tr>
          <td><strong>Real-Time Analyst Operations Console</strong></td>
          <td>Operations team needs immediate visibility into high-confidence fraud.</td>
          <td><strong>Sub-second push alerting (&lt; 200ms)</strong> via WebSocket/Server-Sent Events to a virtualized React frontend, complete with Explainable AI (SHAP) feature attributions.</td>
        </tr>
        <tr>
          <td><strong>Enterprise Observability &amp; Operability</strong></td>
          <td>Proactive failure detection, compliance reporting, and zero unmonitored blindspots.</td>
          <td><strong>OpenTelemetry-native telemetry</strong>, Prometheus metrics, Grafana Tempo distributed tracing, Loki structured logging, and formal SLOs with error budget alerting.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h3>1.3 Architectural Vision &amp; Guiding Principles</h3>
  <p>To satisfy these strict non-functional requirements without compromising security or resilience, the target architecture adheres to five foundational principles:</p>
  <div class="card-grid">
    <div class="info-card">
      <div class="card-title">1. Event-Driven Choreography</div>
      <p>Components communicate asynchronously via an event backbone (Apache Kafka), buffering unpredictable payment traffic, isolating failures, and eliminating cascading outages.</p>
    </div>
    <div class="info-card">
      <div class="card-title">2. Dual-Track Evaluation</div>
      <p>A high-speed synchronous gRPC path (&lt; 35ms) serves inline payment authorization blocking, while an asynchronous stream pipeline computes complex rolling graph features.</p>
    </div>
    <div class="info-card">
      <div class="card-title">3. Immutability by Design</div>
      <p>Every transaction, feature snapshot, and decision is modeled as an immutable event persisted to WORM storage for 7-year regulatory determinism.</p>
    </div>
    <div class="info-card">
      <div class="card-title">4. Zero-Trust Security &amp; Tokenization</div>
      <p>Strict mTLS 1.3 across the mesh. PAN and PII are tokenized at the edge ingress boundary so analytical engines never handle plain financial credentials.</p>
    </div>
  </div>
</section>
"""