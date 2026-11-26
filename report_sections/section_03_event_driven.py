"""
Section 3: Event-Driven Communication & Messaging Backbone
"""

def get_markdown():
    return r"""## 3. Event-Driven Communication & Messaging Backbone

### 3.1 Event-Driven Paradigm Rationale
In high-volume financial architectures processing 1,000+ transactions per second, point-to-point synchronous HTTP/REST communication across internal microservices is fundamentally unviable. Synchronous chaining introduces compounding latency ($L_{total} = \sum L_i$), cascading thread pool starvation, and vulnerable failure domains where a degraded downstream case database can block transaction ingress.

The system utilizes an **Event-Driven Choreography** pattern built on **Apache Kafka**. By decoupling producers from consumers via a partitioned, immutable distributed commit log, the architecture achieves:
1. **Traffic Smoothing & Backpressure Absorption:** Payment bursts (surging to 2,500+ TPS on Black Friday or payroll cycles) are safely absorbed in Kafka partition buffers without dropping transactions or exhausting worker threads. Downstream consumers pull records at their optimal sustained capacity.
2. **Replayability & Event Sourcing:** Because transactions are immutable events preserved in Kafka's distributed log (and cold-archived in WORM object storage), any downstream microservice can rebuild its local state, recover from catastrophic database corruption, or re-process historical traffic simply by rewinding its consumer group offset.
3. **Partition Key Ordering:** By partitioning topics by `account_id` or `cardholder_token`, all events for a given bank account arrive sequentially at the exact same partition. This guarantees strict causal ordering for velocity and state calculations without requiring expensive distributed distributed locks.

---

### 3.2 Canonical Event Catalog & Taxonomy

| Event Name & Topic | What is it? | When is it emitted? | Why is it emitted? | Publisher | Consumer(s) | Trigger for Consumer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`TransactionReceivedEvent`**<br>`financial.trans.received.v1` | Raw transaction ingress record with tokenized PAN and trace context. | Immediately upon successful edge perimeter validation and tokenization. | Decouples network ingress from downstream stateful enrichment and initiates the audit trail. | **Ingestion Gateway (IGS)** | 1. Feature Aggregator<br>2. Compliance Archiver | New message arrival in Kafka partition. |
| **`TransactionEnrichedEvent`**<br>`financial.trans.enriched.v1` | Transaction combined with 48-dimensional computed temporal/spatial feature vector. | Emitted after Flink computes rolling window velocities and Redis state. | Provides the Fraud Scoring Engine with full behavioral context without redundant DB queries. | **Feature Aggregator (FAS)** | 1. Fraud Scoring Engine<br>2. Compliance Archiver | New message arrival on enriched topic. |
| **`FraudEvaluatedEvent`**<br>`financial.fraud.evaluated.v1` | Scoring verdict (`ALLOW`, `CHALLENGE`, `BLOCK`), probability score $S \in [0.0, 1.0]$, and top SHAP attributions. | Emitted after dual-stage rule and ML model execution. | Records classification decision for all transactions, feeding downstream automated rules and BI reporting. | **Fraud Scoring Engine (FSE)** | 1. Downstream Action Svc<br>2. Core Banking Feed<br>3. Compliance Archiver | New message arrival on evaluated topic. |
| **`FraudAlertRaisedEvent`**<br>`financial.fraud.alert.v1` | High-confidence fraud alert packet (Score $S \ge 0.75$) with prioritization metadata. | Emitted simultaneously with evaluated event when risk threshold $\theta_{alert}$ is breached. | Routes high-risk transactions directly to human fraud analysts for immediate real-time review. | **Fraud Scoring Engine (FSE)** | 1. Case Management BFF<br>2. Ops Notification Hub | New message arrival on alert topic. |
| **`CaseStatusChangedEvent`**<br>`case.events.v1` | State change event (`ASSIGNED`, `CONFIRMED_FRAUD`, `FALSE_POSITIVE`) with analyst notes. | When an analyst resolves or transitions a fraud case in the console. | Triggers permanent card blocking, updates ML training labels, and records analyst audit log. | **Case Management BFF (CMS)** | 1. Downstream Action Svc<br>2. ML Model Training Store<br>3. Compliance Archiver | HTTP/WebSocket mutation from analyst. |
| **`ComplianceReplayRequestedEvent`**<br>`compliance.trans.replay.v1` | Historical transaction packet re-injected from WORM storage for backtesting. | When a compliance officer or ML engineer triggers a historical replay. | Enables bit-for-bit regulatory backtesting or candidate model evaluation against historical ground truth. | **Compliance Replay Coordinator (CAR)** | 1. Shadow Fraud Scoring Engine (Isolated Group) | Admin API trigger. |

---

### 3.3 Canonical Event Schema Specifications
The platform enforces schema governance using the **Confluent Schema Registry** with Apache Avro serialization. Below are the canonical JSON Schema representations for the core domain events:

#### 1. `TransactionReceivedEvent` Schema (`financial.trans.received.v1`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "TransactionReceivedEvent",
  "type": "object",
  "required": ["metadata", "payload", "cryptographic_hash"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["event_id", "correlation_id", "traceparent", "event_timestamp", "schema_version"],
      "properties": {
        "event_id": { "type": "string", "format": "uuid" },
        "correlation_id": { "type": "string", "format": "uuid" },
        "traceparent": { "type": "string", "pattern": "^00-[0-9a-f]{32}-[0-9a-f]{16}-01$" },
        "event_timestamp": { "type": "string", "format": "date-time" },
        "schema_version": { "type": "string", "const": "1.4.0" },
        "ingress_channel": { "type": "string", "enum": ["CARD_POS", "CARD_CNP", "FEDNOW", "SEPA_INSTANT", "ACH", "WIRE"] }
      }
    },
    "payload": {
      "type": "object",
      "required": ["transaction_id", "account_id", "cardholder_token", "amount", "currency", "merchant_id", "ip_address"],
      "properties": {
        "transaction_id": { "type": "string", "format": "uuid" },
        "account_id": { "type": "string", "pattern": "^AC-[0-9]{8,12}$" },
        "cardholder_token": { "type": "string", "pattern": "^tkn_pan_[0-9a-zA-Z]{12,24}$" },
        "amount": { "type": "number", "minimum": 0.01 },
        "currency": { "type": "string", "pattern": "^[A-Z]{3}$" },
        "merchant_id": { "type": "string" },
        "merchant_category_code": { "type": "string", "pattern": "^[0-9]{4}$" },
        "ip_address": { "type": "string", "format": "ipv4" },
        "device_fingerprint_id": { "type": "string" },
        "gps_latitude": { "type": "number", "minimum": -90.0, "maximum": 90.0 },
        "gps_longitude": { "type": "number", "minimum": -180.0, "maximum": 180.0 }
      }
    },
    "cryptographic_hash": {
      "type": "string",
      "description": "SHA-256 HMAC of payload using HSM root key for tamper-proofing"
    }
  }
}
```

#### 2. `FraudAlertRaisedEvent` Schema (`financial.fraud.alert.v1`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "FraudAlertRaisedEvent",
  "type": "object",
  "required": ["alert_id", "transaction_id", "account_id", "fraud_score", "priority", "shap_attributions"],
  "properties": {
    "alert_id": { "type": "string", "format": "uuid" },
    "transaction_id": { "type": "string", "format": "uuid" },
    "account_id": { "type": "string" },
    "fraud_score": { "type": "number", "minimum": 0.75, "maximum": 1.0 },
    "priority": { "type": "string", "enum": ["P1_CRITICAL", "P2_HIGH", "P3_ELEVATED"] },
    "triggered_rules": {
      "type": "array",
      "items": { "type": "string" }
    },
    "model_metadata": {
      "type": "object",
      "properties": {
        "model_name": { "type": "string", "const": "ensemble_lightgbm_dnn" },
        "model_version": { "type": "string", "const": "v2.3.1" },
        "inference_latency_ms": { "type": "number" }
      }
    },
    "shap_attributions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["feature_name", "attribution_value", "relative_weight"],
        "properties": {
          "feature_name": { "type": "string" },
          "attribution_value": { "type": "number" },
          "relative_weight": { "type": "string" }
        }
      }
    }
  }
}
```

---

### 3.4 Kafka Consumer Architecture, Offset Management & Exactly-Once Scaling
A fundamental challenge in event-driven financial architectures is ensuring that when microservice consumer groups scale horizontally (e.g., expanding from 4 pods to 16 or 32 pods during a transaction surge), message consumption and state transitions remain strictly **Exactly-Once**. 

In naive Kafka deployments, horizontal scaling triggers a "Consumer Group Rebalance" that revokes partition assignments. If in-flight records are uncommitted or offsets are committed asynchronously, the new consumer instance will re-consume already-processed events, generating duplicate fraud alerts, erroneous ledger holds, or corrupted rolling velocity windows.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│             EXACTLY-ONCE CONSUMER SCALING & REBALANCE ARCHITECTURE                     │
├────────────────────────────────┬───────────────────────────┬───────────────────────────┤
│ 1. Cooperative Sticky Assign   │ 2. Rebalance Listener     │ 3. Atomic Offset Commits  │
│ Only migrated partitions stop  │ onPartitionsRevoked:      │ Stream Hops: sendOffsetsTo│
│ Unaffected consumers continue  │ Drains in-flight records  │   Transaction (Kafka EOS) │
│ Zero stop-the-world pauses     │ Synchronous offset flush  │ DB Sinks: DB Transaction  │
│ Seamless dynamic scale-out     │ Local state checkpoint    │   (Entity + Offset)       │
└────────────────────────────────┴───────────────────────────┴───────────────────────────┘
```

#### 1. Incremental Cooperative Rebalancing (`CooperativeStickyAssignor`)
- *The Flaw of Eager Rebalancing:* The legacy Kafka eager rebalance protocol forced all consumers in a group to revoke all assigned partitions simultaneously, halting processing across the entire consumer fleet ("stop-the-world" pause) and discarding in-memory states.
- *The Solution:* The platform enforces `partition.assignment.strategy = org.apache.kafka.clients.consumer.CooperativeStickyAssignor`. Under this protocol, when KEDA spins up new consumer pods:
  1. Only the specific subset of partitions being transferred to the new consumer replica is revoked.
  2. All other consumer pods continue reading and committing their existing partitions without interruption.
  3. Partitions stick to their existing consumers whenever possible, preserving hot in-memory caches and minimizing state re-hydration overhead.

#### 2. Consumer Rebalance Listener Lifecycle Management
Every consumer pod registers an explicit `ConsumerRebalanceListener` that coordinates offset commits and state drainage during scale-out, scale-in, or pod evacuation events:
- **`onPartitionsRevoked(Collection<TopicPartition> partitions)`:**
  1. *Immediate Poll Halt:* The consumer pauses polling on the revoked partitions.
  2. *In-Flight Record Drain:* The worker thread pool finishes processing all records currently buffered in the local worker queue for those partitions.
  3. *Synchronous Offset Flush:* For non-transactional consumers, the listener calls `consumer.commitSync(currentOffsets)` to commit the exact last successfully processed offset for the revoked partitions to `__consumer_offsets`.
  4. *State Checkpoint:* Local RocksDB state or sliding window state is flushed to persistent storage before relinquishing partition ownership.
- **`onPartitionsAssigned(Collection<TopicPartition> partitions)`:**
  1. The new pod receives the partition assignment.
  2. It queries Kafka or the external transactional offset store to identify the exact starting offset (`committed + 1`).
  3. It initializes local window caches and begins polling with zero risk of re-processing uncommitted records.
- **`onPartitionsLost(Collection<TopicPartition> partitions)`:**
  - Invoked if a consumer experiences a network partition or heartbeat failure (`max.poll.interval.ms` exceeded) and is ejected from the group. The listener immediately aborts in-flight transactions, cleans up local uncommitted memory state, and refrains from committing offsets to prevent overwriting progress made by the reassigned consumer.

#### 3. Exactly-Once Processing (EOS) via Kafka Transactional API (Stream-to-Stream Hops)
For microservices that consume from an upstream topic and produce to a downstream topic (e.g., `Feature Aggregation Service` consuming `trans.raw.v1` and emitting `trans.enriched.v1`, and `Fraud Scoring Engine` consuming `trans.enriched.v1` and emitting `fraud.evaluated.v1`), the platform implements **Kafka Transactional Processing**:
1. **Deterministic `transactional.id` Assignment:** Each consumer pod is assigned a static, deterministic transactional ID tied to its partition assignment (e.g., `fse-scoring-p12`).
2. **Atomic Consume-Transform-Produce Cycle:**
   ```
   producer.beginTransaction();
   ConsumerRecords<String, Transaction> records = consumer.poll(Duration.ofMillis(10));
   for (ConsumerRecord<String, Transaction> record : records) {
       EnrichedTransaction enriched = enrichFeatures(record.value());
       producer.send(new ProducerRecord<>("financial.trans.enriched.v1", enriched));
   }
   // CRUCIAL: Offset committed INSIDE the transaction, not via consumer.commitSync()
   producer.sendOffsetsToTransaction(currentOffsets, consumerGroupId);
   producer.commitTransaction();
   ```
3. **Behavior During Rebalance or Crash:**
   - If a pod crashes or a rebalance occurs before `commitTransaction()`, the transaction aborts automatically.
   - Downstream consumers configured with `isolation.level = read_committed` will **never see the uncommitted output records** (the broker's Last Stable Offset - LSO conceals uncommitted transactional messages).
   - The newly assigned consumer pod resumes consumption from the last committed offset. Zero duplicates are emitted downstream!
4. **Zombie Fencing:** If an evicted pod attempts to write after a rebalance, the Kafka broker rejects the write with a `ProducerFencedException` because the new consumer's transaction coordinator incremented the `producer_epoch` for that `transactional.id`.

#### 4. Atomic Database-Coupled Offset Commit Pattern (Stream-to-Store Sinks)
For microservices that persist state to external databases (e.g., `Case Management BFF` consuming `fraud.alert.v1` and inserting case records into PostgreSQL), Kafka's transactional API cannot coordinate distributed transactions across database boundaries. 
To guarantee exactly-once processing during horizontal scaling, the platform implements the **Transactional Sink Pattern**:
1. The microservice stores the Kafka partition offset in the **exact same relational database transaction** as the case entity:
   ```sql
   BEGIN TRANSACTION;
   INSERT INTO fraud_cases (case_id, transaction_id, account_id, fraud_score, status)
   VALUES ('ALT-9041', 'TX-89104', 'AC-11209', 0.94, 'NEW');
   
   INSERT INTO kafka_consumer_offsets (consumer_group, topic_name, partition_id, last_committed_offset)
   VALUES ('case-mgmt-group', 'financial.fraud.alert.v1', 12, 482910)
   ON CONFLICT (consumer_group, topic_name, partition_id)
   DO UPDATE SET last_committed_offset = EXCLUDED.last_committed_offset;
   COMMIT;
   ```
2. When horizontal scaling triggers a rebalance and a new pod is assigned partition 12, in `onPartitionsAssigned()`, the pod queries the database:
   ```sql
   SELECT last_committed_offset FROM kafka_consumer_offsets 
   WHERE consumer_group = 'case-mgmt-group' AND topic_name = 'financial.fraud.alert.v1' AND partition_id = 12;
   ```
3. The pod explicitly calls `consumer.seek(partition12, last_committed_offset + 1)`.
4. **Guaranteed Outcome:** If a pod crashes or rebalances mid-write, the database transaction rolls back completely. The new pod re-reads from the exact last persisted DB offset. Under no circumstances can duplicate case records or phantom alerts be created during horizontal scaling.

---

### 3.5 Explicit Architectural Deviations from Event-Driven Patterns
While event-driven choreography is the optimal default pattern, dogmatic adherence to pure event-driven principles introduces unacceptable latency and consistency challenges in specific financial contexts. The architecture deliberately implements three synchronous deviations:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              SYNCHRONOUS DEVIATIONS                                    │
├────────────────────────────────┬───────────────────────────┬───────────────────────────┤
│ 1. Synchronous Payment Gate    │ 2. Analyst BFF Queries     │ 3. In-Memory State Cache  │
│ [Card Rail] ──► [Gateway]      │ [Browser] ──► [BFF]       │ [Flink] ──► [Redis]       │
│      gRPC Block < 35ms         │   GraphQL/REST Query      │     Direct In-Memory      │
│ Approve / Challenge / Decline  │ Case Details, Search, Hist│ Velocity Counters < 1ms   │
└────────────────────────────────┴───────────────────────────┴───────────────────────────┘
```

1. **Deviation 1: Synchronous gRPC Path for Inline Card Payment Authorization**
   * *The Problem:* Card network payment switches (Visa/Mastercard) and point-of-sale terminals require a blocking response within 100 milliseconds to approve or decline a purchase. If the bank does not reply within this window, the terminal times out, resulting in a dropped transaction and merchant cart abandonment.
   * *The Architectural Decision:* The platform supports an optional **Synchronous Fast-Path**. The Ingestion Gateway dispatches a high-priority synchronous gRPC request to a specialized, pre-warmed instance of the Rule & Heuristic Scoring Engine. This service executes a sub-35ms evaluation (evaluating hard sanction blocks, velocity counters from Redis, and a quantized LightGBM model) and returns an immediate `APPROVE`, `CHALLENGE`, or `DECLINE` decision back to the payment rail. Simultaneously, the transaction is emitted to Kafka for asynchronous deep graph evaluation and audit capture.
2. **Deviation 2: Synchronous REST / GraphQL Querying in the Analyst BFF**
   * *The Problem:* When a fraud analyst clicks on an active case, the operations console requires immediate retrieval of historical account dossiers, related merchant transaction graphs, and prior case notes. Polling an event stream for ad-hoc user query responses creates high latency, complex state machines, and poor user experience.
   * *The Architectural Decision:* The Analyst BFF queries read-replicas of the Amazon Aurora PostgreSQL Case Database and historical query views synchronously via REST / GraphQL. This guarantees snappy UI navigation (< 50ms) while keeping the transaction processing pipeline strictly asynchronous.
3. **Deviation 3: Synchronous Distributed In-Memory Cache Access (Redis Enterprise)**
   * *The Problem:* In the Feature Aggregation Service, computing velocity counters (e.g., "How many transactions has Card X performed in the last 5 minutes across all global channels?") requires immediate access to state. Emitting an event to request state from another service and awaiting an event response would double Kafka round-trips, ballooning latency by 15-30ms.
   * *The Architectural Decision:* Flink workers make synchronous, non-blocking in-memory calls over pipelined TCP connections directly to a co-located Redis Enterprise cluster. Lookups complete in less than 800 microseconds ($< 0.8$ ms), maintaining the strict P99 latency budget.
"""

def get_html():
    return """
<section id="section-3" class="report-section">
  <div class="section-header">
    <span class="section-number">03</span>
    <div class="section-title-wrap">
      <h2>Event-Driven Communication &amp; Messaging Backbone</h2>
      <p class="section-subtitle">Choreography rationale, Kafka topic topology, event taxonomy, canonical schemas, and synchronous deviations.</p>
    </div>
  </div>

  <h3>3.1 Event-Driven Paradigm Rationale</h3>
  <p>In high-volume financial architectures processing 1,000+ transactions per second, point-to-point synchronous HTTP/REST communication across internal microservices is fundamentally unviable. Synchronous chaining introduces compounding latency, cascading thread pool starvation, and vulnerable failure domains where a degraded downstream case database can block transaction ingress.</p>
  <p>The system utilizes an <strong>Event-Driven Choreography</strong> pattern built on <strong>Apache Kafka</strong>. By decoupling producers from consumers via a partitioned, immutable distributed commit log, the architecture achieves:</p>
  <ul class="bullet-list">
    <li><strong>Traffic Smoothing &amp; Backpressure Absorption:</strong> Payment bursts (surging to 2,500+ TPS on Black Friday or payroll cycles) are safely absorbed in Kafka partition buffers without dropping transactions. Downstream consumers pull records at their optimal sustained capacity.</li>
    <li><strong>Replayability &amp; Event Sourcing:</strong> Because transactions are immutable events preserved in Kafka's distributed log (and cold-archived in WORM object storage), any downstream microservice can rebuild its local state, recover from catastrophic database corruption, or re-process historical traffic simply by rewinding its consumer group offset.</li>
    <li><strong>Partition Key Ordering:</strong> By partitioning topics by <code>account_id</code> or <code>cardholder_token</code>, all events for a given bank account arrive sequentially at the exact same partition. This guarantees strict causal ordering for velocity and state calculations without requiring expensive distributed locks.</li>
  </ul>

  <h3>3.2 Canonical Event Catalog &amp; Taxonomy</h3>
  <div class="table-container">
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 22%;">Event Name &amp; Topic</th>
          <th style="width: 25%;">What &amp; When?</th>
          <th style="width: 25%;">Why? (Business Purpose)</th>
          <th style="width: 14%;">Publisher</th>
          <th style="width: 14%;">Consumer(s)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>TransactionReceivedEvent</strong><br><code>financial.trans.received.v1</code></td>
          <td>Raw transaction ingress record with tokenized PAN. Emitted immediately upon edge validation.</td>
          <td>Decouples network ingress from downstream stateful enrichment and initiates the audit trail.</td>
          <td><span class="badge badge-primary">Ingestion Gateway</span></td>
          <td>Feature Aggregator,<br>Compliance Archiver</td>
        </tr>
        <tr>
          <td><strong>TransactionEnrichedEvent</strong><br><code>financial.trans.enriched.v1</code></td>
          <td>Transaction merged with 48-dim temporal and spatial feature vector after Flink processing.</td>
          <td>Provides the Scoring Engine with full behavioral context without redundant DB queries.</td>
          <td><span class="badge badge-success">Feature Aggregator</span></td>
          <td>Fraud Scoring Engine,<br>Compliance Archiver</td>
        </tr>
        <tr>
          <td><strong>FraudEvaluatedEvent</strong><br><code>financial.fraud.evaluated.v1</code></td>
          <td>Scoring verdict (ALLOW/CHALLENGE/BLOCK), score [0.0-1.0], and top SHAP attributions.</td>
          <td>Records classification decision for all transactions, feeding automated enforcement and BI.</td>
          <td><span class="badge badge-danger">Scoring Engine</span></td>
          <td>Downstream Action Svc,<br>Compliance Archiver</td>
        </tr>
        <tr>
          <td><strong>FraudAlertRaisedEvent</strong><br><code>financial.fraud.alert.v1</code></td>
          <td>High-confidence fraud alert packet (Score &ge; 0.75) with triage priority metadata.</td>
          <td>Routes high-risk transactions directly to human fraud analysts for immediate real-time review.</td>
          <td><span class="badge badge-danger">Scoring Engine</span></td>
          <td>Case Management BFF,<br>Ops Alert Hub</td>
        </tr>
        <tr>
          <td><strong>CaseStatusChangedEvent</strong><br><code>case.events.v1</code></td>
          <td>Case lifecycle transition (ASSIGNED, CONFIRMED, FALSE_POS) with analyst notes.</td>
          <td>Triggers permanent card blocking, updates ML training ground-truth, and writes analyst audit log.</td>
          <td><span class="badge badge-primary" style="background:#7c3aed;">Case Mgmt BFF</span></td>
          <td>Downstream Action Svc,<br>ML Training Store</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h3>3.3 Kafka Consumer Offset Management &amp; Exactly-Once Scaling</h3>
  <p>A fundamental challenge in event-driven financial architectures is ensuring that when microservice consumer groups scale horizontally (e.g., expanding from 4 pods to 16 or 32 pods during a transaction surge), message consumption and state transitions remain strictly <strong>Exactly-Once</strong>.</p>
  
  <div class="card-grid">
    <div class="info-card">
      <div class="card-title">1. Cooperative Sticky Assignor</div>
      <p>Using <code>CooperativeStickyAssignor</code>, scaling pods triggers incremental rebalancing. Only the specific partitions migrating to the new pod are revoked; all unaffected consumers continue processing with zero stop-the-world pauses.</p>
    </div>
    <div class="info-card">
      <div class="card-title">2. Consumer Rebalance Listener</div>
      <p><code>onPartitionsRevoked()</code> halts polling, drains in-flight records from memory, executes a synchronous offset flush (<code>commitSync</code>), and flushes local state before yielding partition ownership.</p>
    </div>
    <div class="info-card">
      <div class="card-title">3. Exactly-Once Stream Hops (EOS)</div>
      <p>Stream hops (Feature Aggregator, Scoring Engine) use Kafka Transactions. Consumer offsets are committed <em>inside</em> the transaction via <code>sendOffsetsToTransaction()</code>, aborting cleanly on crash with broker zombie fencing.</p>
    </div>
    <div class="info-card">
      <div class="card-title">4. Atomic Database Sink Offsets</div>
      <p>For Case Management (writing to PostgreSQL), the consumer offset is committed in the <strong>exact same ACID transaction</strong> as the case record. On rebalance, the new pod queries the DB and seeks directly to the committed offset.</p>
    </div>
  </div>

  <h3>3.4 Explicit Architectural Deviations from Event-Driven Patterns</h3>
  <p>While event-driven choreography is the optimal default pattern, dogmatic adherence to pure event-driven principles introduces unacceptable latency and consistency challenges in specific financial contexts. The architecture deliberately implements three synchronous deviations:</p>

  <div class="card-grid">
    <div class="info-card">
      <div class="card-title" style="color:#0284c7;">1. Synchronous gRPC Payment Gate</div>
      <p>Card network payment switches (Visa/Mastercard) require a blocking response within 100ms. An optional <strong>Synchronous Fast-Path</strong> executes sub-35ms rule and quantized ML evaluation, returning an immediate APPROVE/DECLINE to the terminal while asynchronously emitting to Kafka for deep scoring and audit.</p>
    </div>
    <div class="info-card">
      <div class="card-title" style="color:#7c3aed;">2. Synchronous REST/GraphQL in Analyst BFF</div>
      <p>When an analyst clicks an active case, the console requires immediate retrieval of historical account dossiers, past transactions, and case notes. Synchronous queries against PostgreSQL read-replicas guarantee snappy UI navigation (&lt; 50ms) without polling event streams.</p>
    </div>
    <div class="info-card">
      <div class="card-title" style="color:#dc2626;">3. Synchronous In-Memory Cache (Redis)</div>
      <p>Computing rolling velocity counters in Feature Aggregation requires immediate state access. Synchronous non-blocking TCP calls to co-located Redis Enterprise complete in &lt; 800 microseconds (&lt; 0.8ms), avoiding multi-hop messaging latency in the critical path.</p>
    </div>
  </div>
</section>
"""