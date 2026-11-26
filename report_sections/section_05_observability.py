"""
Section 5: Enterprise Observability & Telemetry Framework
"""

def get_markdown():
    return r"""## 5. Enterprise Observability & Telemetry Framework

### 5.1 Telemetry Architecture: OpenTelemetry Standard
In a distributed, event-driven banking architecture handling 1,000 TPS, traditional server monitoring and isolated log grepping are completely obsolete. When an unexpected latency spike or classification anomaly occurs, operators must be able to trace a transaction's journey across network hops, Kafka topic partitions, in-memory caches, and GPU inference models with sub-millisecond precision.

The platform establishes an enterprise observability pipeline standardized on **OpenTelemetry (OTel)**. OpenTelemetry provides vendor-neutral APIs, SDKs, and tooling that decouple application instrumentation from backend telemetry storage systems:

```
[ Microservices Fleet (Go, Java, Python, Node) ]
                   │
         OTLP gRPC (Port 4317)
                   ▼
┌─────────────────────────────────────────────────────────────┐
│          OpenTelemetry Collector Pipeline (DaemonSet)       │
├──────────────────────────────┬──────────────────────────────┤
│ Receivers: OTLP gRPC / HTTP  │ Processors: Batch, PII Mask  │
├──────────────────────────────┴──────────────────────────────┤
│ Exporters: Fanout to 3 Pillars                              │
└──────┬───────────────────────┬───────────────────────┬──────┘
       ▼                       ▼                       ▼
 [ Prometheus ]         [ Grafana Tempo ]        [ Grafana Loki ]
 (Metrics TSDB)         (Traces / S3)            (Structured Logs)
       │                       │                       │
       └───────────────────────┼───────────────────────┘
                               ▼
            [ Unified Grafana Enterprise Console ]
           (SLO Dashboards, Exemplars & Incident UI)
```

1. **Instrumentation & W3C TraceContext Propagation:** Every microservice is instrumented with the language-specific OpenTelemetry SDK. For asynchronous Kafka messaging, the OTel instrumentation intercepts Kafka producer and consumer records, injecting and extracting the standard W3C `traceparent` (e.g., `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`) directly into Kafka record binary headers. This guarantees uninterrupted causal trace continuity across asynchronous boundaries.
2. **OpenTelemetry Collector Fleet:** Deployed as a Kubernetes `DaemonSet` on every worker node, local collector agents receive telemetry over low-latency Unix domain sockets or localhost gRPC. The collector pipeline applies:
   - **Memory Limiter & Batching:** Buffers spans, metrics, and logs to optimize network transmission overhead.
   - **PII / PCI Scrubbing Processor:** Dynamically masks card numbers, account balances, and customer names before data leaves the cluster node boundary.
   - **Standardized Resource Attributes:** Automatically injects metadata (`environment=production`, `region=us-east-1`, `cluster_id=k8s-prod-fin`, `git_sha`, `k8s_pod_name`).

---

### 5.2 The Three Telemetry Pillars
The platform establishes deep operational visibility across three unified pillars:

#### 1. Distributed Tracing (Grafana Tempo / Jaeger)
- **Tracing Topology:** Every transaction generates a root span at the Ingestion Gateway. Child spans are spawned for Kafka publication, Flink feature retrieval, Redis TCP lookups, Triton inference execution, database updates, and WebSocket push frames.
- **Cost-Effective Object Storage:** Grafana Tempo utilizes Amazon S3 / Google Cloud Storage as its underlying trace store. This enables **100% trace sampling** for all non-ALLOW transactions and high-confidence alerts, ensuring zero blindspots for compliance investigations at 1/10th the cost of traditional SSD-backed trace databases.

#### 2. Centralized Metrics & Golden Signals (Prometheus / VictoriaMetrics)
- **Metric Collection:** High-resolution dimensional metrics scraped every 10 seconds. Microservices expose Micrometer / Prometheus endpoints tracking Google's Four Golden Signals:
  1. *Latency:* Request and inference duration histograms across granular percentiles (P50, P90, P99, P99.9).
  2. *Traffic:* Real-time throughput (TPS) per ingress rail and Kafka topic.
  3. *Errors:* HTTP 5xx codes, Kafka consumer deserialization errors, and DLQ diversion rates.
  4. *Saturation:* Kafka consumer lag per partition, Triton GPU memory utilization, and thread pool exhaustion.

#### 3. Centralized Logging (Grafana Loki)
- **Structured JSON Logging:** Microservices emit structured JSON logs exclusively to `stdout`. FluentBit agents tail container logs and ship them to Grafana Loki.
- **Log Indexing by Labels:** Rather than indexing entire log payloads (which causes massive storage bloat in systems like Elasticsearch), Loki indexes metadata labels (`app`, `env`, `pod`, `level`, `error_code`). Full log bodies are searched using LogQL with extreme efficiency.

---

### 5.3 Cross-Pillar Telemetry Correlation Strategy
The critical operational breakthrough of this platform is the **deterministic cross-linking** between metrics, traces, and logs, eliminating the dreaded "swivel-chair" debugging during high-severity production incidents:

```
[ Metric Spike Alert ] ──► [ Click Prometheus Exemplar ]
                                   │
                                   ▼ Extracts trace_id
                       [ Tempo Trace Waterfall ]
                        (Pinpoints Triton Model Hang)
                                   │
                                   ▼ Click "Logs for this Span"
                       [ Filtered Loki Log Lines ]
                        (CUDA Out of Memory in Pod)
```

1. **Metrics $\longrightarrow$ Traces via Prometheus Exemplars:** When a latency histogram bucket records an outlier (e.g., a transaction taking 82ms), Prometheus captures an **Exemplar**—attaching the exact `trace_id` of that specific outlier transaction to the metric data point. In Grafana, clicking on a spike in the latency graph instantly opens the exact trace waterfall in Tempo.
2. **Traces $\longrightarrow$ Logs via TraceId / SpanId Injection:** The logging framework automatically extracts the active OpenTelemetry `trace_id` and `span_id` from the thread execution context and injects them into every log record. From any span in the Tempo waterfall view, an operator can click "Logs for this Span" to view the exact log lines emitted by that specific pod during that specific millisecond window.
3. **Cross-Cutting Universal Key (`transaction_id`):** Every log, metric attribute, trace span, and compliance audit file indexes the canonical `transaction_id` and `account_id`, allowing compliance auditors and forensic investigators to execute a single search query that aggregates every technical and business artifact associated with a transaction.

---

### 5.4 Key Performance Metrics & Formal Service Level Objectives (SLOs)
To ensure the system remains accountable to business and legal requirements, the platform defines three specific, measurable, and objective **Service Level Objectives (SLOs)** backed by strict **Service Level Indicators (SLIs)**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 CORE PRODUCTION SLOs                                   │
├────────────────────────────────┬───────────────────────────┬───────────────────────────┤
│ SLO 1: Classification Latency  │ SLO 2: Pipeline Error Rate │ SLO 3: Audit Completeness │
│ P99 <= 45ms (Rolling 5m)       │ Error Rate < 0.01% (1h)   │ 100% Captured in < 15s    │
│ Target: 99.0% Compliance       │ Target: 99.99% Error-Free │ Zero Event Loss (Delta=0) │
└────────────────────────────────┴───────────────────────────┴───────────────────────────┘
```

#### SLO 1: Real-Time End-to-End Classification Latency
* **Business Justification:** Legal compliance with instant payment networks (FedNow / SEPA Instant) requires classification decisions before funds settle. Any latency above 50ms risks payment terminal timeouts and customer friction.
* **Objective (SLO):** **99.0% of all non-batch transactions must complete end-to-end fraud classification in $\le 45$ milliseconds**, measured across any rolling 5-minute window.
* **Service Level Indicator (SLI):**
  $$\text{SLI}_{latency} = \frac{\sum \text{rate}\left(\text{fraud\_detection\_e2e\_duration\_seconds\_bucket}\{le="0.045"\}[5m]\right)}{\sum \text{rate}\left(\text{fraud\_detection\_e2e\_duration\_seconds\_count}[5m]\right)} \ge 0.990$$
* **Measurement Boundary:** Measured from the exact microsecond the Ingestion Gateway receives the HTTP/gRPC request to the microsecond the `FraudEvaluatedEvent` is committed to Kafka.

#### SLO 2: Fraud Scoring Pipeline Availability & Error Rate
* **Business Justification:** In financial services, dropped transactions result in unmonitored fraud or false card declines, directly damaging bank reputation and merchant trust.
* **Objective (SLO):** **The fraud scoring engine and feature aggregation pipeline must achieve less than 0.01% error rate (99.99% error-free processing)** over any rolling 1-hour window.
* **Service Level Indicator (SLI):**
  $$\text{SLI}_{errors} = 1 - \frac{\sum \text{rate}\left(\text{http\_requests\_total}\{status=\sim"5.." \}[1h]\right) + \sum \text{rate}\left(\text{kafka\_processing\_errors\_total}[1h]\right)}{\sum \text{rate}\left(\text{transactions\_processed\_total}[1h]\right)} \ge 0.9999$$
* **Measurement Boundary:** Includes HTTP 5xx ingress errors, unhandled serialization exceptions, and messages diverted to the Dead Letter Queue (DLQ).

#### SLO 3: Compliance Audit Capture Completeness & Replay Fidelity
* **Business Justification:** Basel Committee (BCBS 239) and legal compliance rules mandate that 100% of financial transactions must be captured immutably. Failing to capture even 0.001% of records during a regulatory audit incurs severe financial fines.
* **Objective (SLO):** **100% of transactions ingested by the platform must be immutably persisted to WORM compliance storage within 15 seconds**, and daily reconciliation checksum audits must demonstrate **zero event loss ($\Delta = 0$)**.
* **Service Level Indicator (SLI):**
  $$\text{SLI}_{audit} = \left(\text{transactions\_ingested\_total} - \text{audit\_persisted\_transactions\_total}\right) \equiv 0 \quad (\text{within } T+15s)$$
* **Measurement Boundary:** Automated hourly reconciliation workers compare the monotonic sequence offsets committed to Kafka against the row count and SHA-256 batch manifests stored in the S3 Iceberg lakehouse.

---

### 5.5 Error Budgets, Alerting Tiers & Incident Operationalization
The platform adopts Google Site Reliability Engineering (SRE) **Multi-Window Multi-Burn-Rate Alerting**. Rather than alerting on raw thresholds (which causes alert fatigue), alerts fire when the **Error Budget** is burning at a rate that threatens the monthly SLO:

| Alert Tier | Burn Rate & Condition | Notification Channel | Operational Action / Playbook |
| :--- | :--- | :--- | :--- |
| **P1 Critical** | **14.4x Burn Rate** (2% budget consumed in 1 hour) OR Latency P99 > 80ms for 2 mins. | PagerDuty (Automated phone call to primary on-call SRE & Lead Architect). | Immediate incident bridge. Automated circuit breakers trigger heuristic fallback mode; traffic is routed to warm standby zone. |
| **P2 Major** | **6x Burn Rate** (5% budget consumed in 6 hours) OR Kafka Consumer Lag > 5,000 msgs. | PagerDuty & Slack `#fraud-ops-critical`. | On-call engineer investigates pod autoscaling bottlenecks, database connection pools, or Triton model latency. |
| **P3 Minor** | **1x Burn Rate** (10% budget consumed in 3 days) OR DLQ count > 50 records. | Jira Ticket created & Slack `#fraud-ops-warning`. | Non-urgent triage during normal business hours; data engineers analyze poisoned payload formats. |
"""

def get_html():
    return """
<section id="section-5" class="report-section">
  <div class="section-header">
    <span class="section-number">05</span>
    <div class="section-title-wrap">
      <h2>Enterprise Observability &amp; Telemetry Framework</h2>
      <p class="section-subtitle">OpenTelemetry standardization, the Three Pillars, cross-telemetry correlation, and formal SLOs.</p>
    </div>
  </div>

  <h3>5.1 OpenTelemetry Standard &amp; Pipeline Architecture</h3>
  <p>In a distributed, event-driven banking architecture handling 1,000 TPS, traditional server monitoring and isolated log grepping are completely obsolete. When an unexpected latency spike or classification anomaly occurs, operators must be able to trace a transaction's journey across network hops, Kafka topic partitions, in-memory caches, and GPU inference models with sub-millisecond precision.</p>

  <div class="card-grid">
    <div class="info-card">
      <div class="card-title">Distributed Tracing (Tempo)</div>
      <p>W3C <code>traceparent</code> headers injected into Kafka record headers guarantee unbroken trace waterfalls across asynchronous messaging boundaries with 100% sampling on fraud alerts.</p>
    </div>
    <div class="info-card">
      <div class="card-title">Metrics &amp; SLOs (Prometheus)</div>
      <p>Continuous scraping of Google's Four Golden Signals (Latency histograms, Throughput TPS, Error rates, Kafka consumer lag, and GPU saturation) scraped every 10 seconds.</p>
    </div>
    <div class="info-card">
      <div class="card-title">Centralized Logs (Loki)</div>
      <p>Structured JSON logs with automated injection of <code>trace_id</code> and <code>span_id</code>. Automated FluentBit masking sanitizes all PAN and PII before leaving the node.</p>
    </div>
    <div class="info-card">
      <div class="card-title">Cross-Pillar Correlation</div>
      <p>Prometheus Exemplars link metric latency spikes directly to Trace IDs. From Tempo, a single click pulls all matching Loki logs for that microsecond window.</p>
    </div>
  </div>

  <h3>5.2 Formal Service Level Objectives (SLOs)</h3>
  <p>To ensure the system remains accountable to business and legal requirements, the platform defines three specific, measurable, and objective <strong>Service Level Objectives (SLOs)</strong> backed by strict <strong>Service Level Indicators (SLIs)</strong>:</p>

  <div class="slo-card">
    <div class="slo-header">
      <span class="slo-title">SLO 1: End-to-End Classification Latency (P99)</span>
      <span class="slo-target">Target: &ge; 99.0% Compliance</span>
    </div>
    <div class="slo-body">
      <p><strong>Objective:</strong> 99.0% of all non-batch transactions must complete end-to-end fraud classification (from ingestion receipt to evaluation event emission) in <strong>&le; 45 milliseconds</strong> over any rolling 5-minute window.</p>
      <div class="code-block-header">Service Level Indicator (SLI) Query</div>
      <pre><code>sum(rate(fraud_detection_e2e_duration_seconds_bucket{le="0.045"}[5m]))
/ sum(rate(fraud_detection_e2e_duration_seconds_count[5m])) >= 0.990</code></pre>
    </div>
  </div>

  <div class="slo-card">
    <div class="slo-header">
      <span class="slo-title">SLO 2: Fraud Scoring Pipeline Availability &amp; Error Rate</span>
      <span class="slo-target">Target: &ge; 99.99% Error-Free</span>
    </div>
    <div class="slo-body">
      <p><strong>Objective:</strong> The fraud scoring engine and feature aggregation pipeline must achieve less than 0.01% error rate (<strong>99.99% error-free processing</strong>) over any rolling 1-hour window.</p>
      <div class="code-block-header">Service Level Indicator (SLI) Query</div>
      <pre><code>1 - (sum(rate(http_requests_total{status=~"5.."}[1h])) + sum(rate(kafka_processing_errors_total[1h])))
/ sum(rate(transactions_processed_total[1h])) >= 0.9999</code></pre>
    </div>
  </div>

  <div class="slo-card">
    <div class="slo-header">
      <span class="slo-title">SLO 3: Compliance Audit Capture Completeness &amp; Replay Fidelity</span>
      <span class="slo-target">Target: 100% Deterministic Parity</span>
    </div>
    <div class="slo-body">
      <p><strong>Objective:</strong> 100% of transactions ingested by the system must be immutably persisted to WORM compliance storage within 15 seconds, and hourly reconciliation checksum audits must verify <strong>zero event loss (&Delta; = 0)</strong>.</p>
      <div class="code-block-header">Service Level Indicator (SLI) Query</div>
      <pre><code>(transactions_ingested_total - audit_persisted_transactions_total) == 0 (verified at T + 15s)</code></pre>
    </div>
  </div>

  <h3>5.3 Error Budget &amp; Alerting Tiers</h3>
  <div class="table-container">
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 15%;">Alert Tier</th>
          <th style="width: 35%;">Burn Rate &amp; Trigger Condition</th>
          <th style="width: 25%;">Notification Channel</th>
          <th style="width: 25%;">Operational Action</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="badge badge-danger">P1 Critical</span></td>
          <td>14.4x Burn Rate (2% budget consumed in 1h) OR P99 Latency &gt; 80ms for 2m.</td>
          <td>PagerDuty Phone Call to SRE &amp; Lead Architect.</td>
          <td>Immediate incident bridge; automated circuit breakers trigger rule-based fallback.</td>
        </tr>
        <tr>
          <td><span class="badge badge-warning">P2 Major</span></td>
          <td>6x Burn Rate (5% budget consumed in 6h) OR Kafka Lag &gt; 5,000 messages.</td>
          <td>PagerDuty &amp; Slack <code>#fraud-ops-critical</code>.</td>
          <td>Investigate pod autoscaling bottlenecks or Triton GPU inference queues.</td>
        </tr>
        <tr>
          <td><span class="badge badge-primary">P3 Minor</span></td>
          <td>1x Burn Rate (10% budget consumed in 3d) OR DLQ count &gt; 50 records.</td>
          <td>Jira Ticket &amp; Slack <code>#fraud-ops-warning</code>.</td>
          <td>Non-urgent triage during business hours; investigate poisoned payload formats.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
"""