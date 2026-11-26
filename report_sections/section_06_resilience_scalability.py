"""
Section 6: Scalability & Resilience Engineering
"""

def get_markdown():
    return r"""## 6. Scalability & Resilience Engineering

### 6.1 Single Points of Failure (SPOFs) Identification & Mitigation
Financial mission-critical architectures must be engineered under the assumption that any individual hardware node, network link, cloud availability zone, or software component can and will fail abruptly. The platform systematically identifies and neutralizes all potential Single Points of Failure:

| Potential Single Point of Failure (SPOF) | Failure Scenario & Business Impact | Architectural Mitigation Strategy | Residual Risk & Recovery Time Objective (RTO) |
| :--- | :--- | :--- | :--- |
| **Apache Kafka Broker Failure / Partition Loss** | Loss of an entire cloud availability zone causes Kafka broker nodes to drop offline. | Deploy across **3 Availability Zones (AZ)** with a Replication Factor of 3 ($\text{RF}=3$) and $\text{min.insync.replicas}=2$. Kafka cluster uses **KRaft Quorum** (eliminating ZooKeeper SPOF). Producers use `acks=all`. | **RTO < 2 seconds:** Zero data loss ($\text{RPO}=0$). Partitions automatically fail over to in-sync replica. |
| **Distributed In-Memory Cache (Redis) Failure** | Redis node crash or network partition prevents Feature Aggregator from retrieving velocity counters. | **Redis Enterprise Cluster** with active-active multi-AZ replication, automatic Sentinel failover, and Append-Only File (AOF) persistence. Microservices implement **Resilience4j Circuit Breakers** with local in-memory LRU cache fallback. | **RTO < 3 seconds:** If Redis fails, Flink gracefully falls back to local RocksDB state checkpoints with degraded feature flags. |
| **Triton ML Model Inference Hang / Crash** | Sudden GPU memory leak or complex payload causes Triton model inference to exceed execution timeout (> 20ms). | All inference calls pass through an **Envoy Sidecar Circuit Breaker** with a strict 20ms hard deadline. If Triton times out or trips the breaker (5% error rate), traffic instantly falls back to an embedded **Heuristic Rule Engine** (Lightweight Decision Rules). | **RTO = 0 (Immediate Fallback):** Zero dropped transactions. The heuristic engine processes the transaction in < 2ms, tagging the record with `fallback_mode=true`. |
| **PostgreSQL Case Database Crash** | Storage exhaustion or primary node hardware failure takes down Case Management database. | **Amazon Aurora PostgreSQL Multi-AZ** with automated storage auto-scaling and synchronous standby replication (sub-30s failover). The Kafka `financial.fraud.alert.v1` topic retains alerts for 14 days, buffering all incoming alerts while the database recovers. | **RTO < 30 seconds:** Zero alert loss. Case BFF pods pause offset commits until Aurora completes failover, then cleanly resume ingestion. |

---

### 6.2 Data Loss Prevention, Idempotency & Disaster Recovery
In high-frequency financial platforms, message duplication (due to network retries) and message loss (due to uncommitted crashes) are severe threats. The architecture guarantees zero data loss and exact deduplication through a multi-tier defense:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              DATA LOSS MITIGATION MATRIX                               │
├────────────────────────────────┬───────────────────────────┬───────────────────────────┤
│ Tier 1: Idempotent Ingestion   │ Tier 2: Transactional Log │ Tier 3: WORM Audit Store  │
│ SHA-256 HMAC Payload Hash      │ acks=all, min.isr=2       │ S3 Object Lock (7 Years)  │
│ Drops Network Retries at Gate  │ Manual Offset Commit Post │ Cannot be deleted even by │
│ Zero Duplicate Records Emitted │ Successful DB/State Write │ Cloud Root Account (WORM) │
└────────────────────────────────┴───────────────────────────┴───────────────────────────┘
```

1. **Idempotent Ingestion & Deduplication:** Network instability between payment rails and the bank's gateway frequently triggers client-side retries. The Ingestion Gateway computes a deterministic canonical SHA-256 hash from `(account_id, amount, merchant_id, timestamp)`. It checks this hash against a distributed 60-second Redis filter. If a retry arrives, the gateway returns the previously cached acknowledgment without publishing a duplicate event to Kafka. Furthermore, Kafka producers enable `enable.idempotence=true`, guaranteeing that broker-side TCP retries never produce duplicate log entries.
2. **Post-Processing Offset Commit Discipline:** Consumers never commit offsets automatically (`enable.auto.commit=false`). Consumer pods commit their Kafka partition offset **only after** the transaction has been fully processed, written to local state/database, or published to the next downstream topic. If a pod crashes mid-execution, the replacement pod spins up, re-consumes the record from the last committed offset, and completes processing without data loss.
3. **Dead-Letter Queue (DLQ) & Poison Pill Quarantine:** Malformed payloads or records that trigger unhandled runtime exceptions are retried 3 times with exponential backoff and jitter. If processing still fails, the message is diverted to a dedicated **Dead-Letter Queue** (`financial.trans.received.dlq`). The main consumer pipeline continues processing without head-of-line blocking. Dedicated DLQ alerting notifies engineers, who can inspect the quarantined payload and replay it once patched.
4. **WORM Storage Disaster Recovery:** The canonical source of truth for the bank is the Amazon S3 / Google Cloud Storage compliance lakehouse, configured with **Object Lock in Compliance Mode**. Even in the cataclysmic event of total Kafka cluster corruption, the entire event backbone can be restored and re-hydrated from the immutable S3 Parquet logs.

---

### 6.3 Compliance Replay Pipeline & Audit Reconstruction
A cornerstone requirement of Basel III and BCBS 239 is the ability to perform **deterministic historical transaction replay**. Financial regulators frequently require banks to demonstrate how their automated models would have classified historical transactions under specific conditions, or to evaluate whether a new machine learning model introduces discriminatory bias or false-positive regressions.

The architecture provides a dedicated **Compliance Replay Pipeline**:

```
[ Compliance Admin API ] ──► [ Replay Coordinator Svc ]
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
      [ S3 WORM Compliance Store ]        [ Replay Worker Pods (KEDA) ]
      (Columnar Parquet Datasets)                      │
                                                       ▼ Injects Events
                                        [ Topic: trans.replay.v1 ]
                                                       │
                                                       ▼
                                        [ Shadow Scoring Engine ]
                                        (Evaluates Candidate v2.4)
                                                       │
                                                       ▼
                                        [ Audit Diff Report Generator ]
                                        (Validates Zero Impact on Prod)
```

1. **Replay Triggering:** A Compliance Officer or ML Data Scientist invokes the Replay API:
   ```json
   POST /v1/compliance/replay
   {
     "start_time": "2026-03-01T00:00:00Z",
     "end_time": "2026-03-07T23:59:59Z",
     "target_model_version": "candidate_xgb_v2.4",
     "replay_speed_multiplier": 50
   }
   ```
2. **Lakehouse Slicing:** The Replay Coordinator queries the Apache Iceberg catalog, identifying the exact Parquet partition files matching the requested timestamp range.
3. **Isolated Replay Stream:** Dynamic Replay Worker pods (scaled via KEDA) stream historical transaction records from S3 using Apache Arrow and publish them into a strictly **isolated Kafka topic** (`compliance.trans.replay.v1`). The original transaction timestamp is preserved in the message header (`x-original-timestamp`).
4. **Shadow Scoring & Model Governance:** A dedicated **Shadow Scoring Engine** consumes from the replay topic, evaluating transactions against the candidate model version. The shadow engine is barred from invoking Downstream Action APIs or pushing alerts to live fraud analysts.
5. **Reconciliation Diff Engine:** A model governance engine compares original historical classifications against the candidate model's classifications, generating an automated audit report detailing:
   - Changes in precision and recall.
   - Reduction in false positive rates.
   - SHAP explainability shift across demographic segments.
   - Bit-for-bit event parity verification with original immutable audit manifests.

---

### 6.4 Comprehensive Scaling Strategies Across System Components
To satisfy the dual imperatives of sustaining a peak load of 1,000 transactions per second (with surge headroom up to 3,000+ TPS) and maintaining cost efficiency during off-peak troughs (100 TPS), the platform implements dedicated scaling strategies across three fundamental layers: **Individual Microservices**, **Analytic Workloads**, and **Event Messaging**.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        COMPREHENSIVE THREE-TIER SCALING MATRIX                         │
├────────────────────────────────┬───────────────────────────┬───────────────────────────┤
│ 1. Individual Microservices    │ 2. Analytic & ML Workloads│ 3. Event Messaging & EOS  │
│ • KEDA Lag-Driven Autoscaling  │ • Flink Reactive Streaming│ • 32 Partitions (account) │
│ • Fast Startup (< 50ms Go)     │ • Triton Dynamic Batching │ • CooperativeStickyAssign │
│ • PodDisruptionBudgets (PDB)   │ • INT8/FP16 Quantization  │ • Rebalance Listeners     │
│ • AZ-Spread Anti-Affinity      │ • Iceberg Partition Prune │ • Transactional EOS & Sink│
└────────────────────────────────┴───────────────────────────┴───────────────────────────┘
```

---

#### 1. Scaling Individual Microservices
The platform distinguishes between stateless network-facing services and event-processing worker fleets:
* **Ingestion Gateway (Go 1.23) & Case BFF (Node.js 22):**
  - *Scaling Triggers:* Scaled via **KEDA** based on inbound HTTP request rates, active TCP connection counts, and CPU pressure (target: 65% utilization).
  - *Fast Container Startup:* Compiled Go binaries spin up in **< 40 milliseconds**; Node.js Fastify pods initialize in **< 350 milliseconds**. This near-instantaneous startup allows the cluster to absorb traffic spikes without requiring over-provisioned idle capacity.
  - *High Availability & Disruption Budgets:* Every microservice deployment specifies a `PodDisruptionBudget` (`minAvailable: 75%`) and inter-pod anti-affinity rules (`topologyKey: topology.kubernetes.io/zone`). This guarantees that during rolling node upgrades or cluster autoscaling events, pods are evenly distributed across 3 Availability Zones with zero capacity drops.
  - *Connection Pooling & HTTP/2 Multiplexing:* Ingestion proxies maintain long-lived, multiplexed HTTP/2 and gRPC connections to upstream payment switches, eliminating TCP handshake and TLS negotiation overhead on a per-transaction basis.
* **Downstream Action Service (Java Quarkus Reactive):**
  - *Reactive Non-Blocking Engine:* Uses Eclipse Vert.x and Mutiny reactive streams to handle 10,000+ concurrent outbound notification requests (SMS, card freezes, core ledger holds) on a minimal thread pool, scaling horizontally via KEDA lag triggers on `financial.fraud.evaluated.v1`.

---

#### 2. Scaling Analytic & Machine Learning Workloads
Analytic and inference workloads represent the most computationally intensive components of the platform, requiring specialized scaling mechanisms across stream processing, deep learning, and lakehouse querying:

* **Stateful Stream Processing Analytics (Apache Flink / Kafka Streams):**
  - *Keyed State Partitioning:* The Feature Aggregation Service maintains sliding velocity windows (1m, 5m, 1h, 24h) keyed by `account_id`. Flink distributes these stateful keys across 32 parallel task slots, aligning 1:1 with Kafka topic partitions.
  - *RocksDB State Backend & Incremental Checkpoints:* Large historical state windows are persisted in local RocksDB instances backed by high-speed NVMe SSDs. Asynchronous incremental checkpointing writes state deltas to Amazon S3 every 30 seconds, bounding recovery time.
  - *Flink Reactive Mode Scaling:* When KEDA scales Flink TaskManager pods up or down in response to sustained volume changes, Flink’s **Reactive Mode** automatically rescales job parallelism, redistributing RocksDB state partitions across available workers without requiring manual job restarts or state re-hydration from scratch.
* **Machine Learning Inference Workloads (Triton Inference Server):**
  - *Dynamic Server-Side Batching:* Machine learning models running on GPUs experience severe throughput penalties if executed one record at a time. Triton implements **Dynamic Request Batching**, collecting incoming transaction vectors over a 2-millisecond sliding window to assemble micro-batches of 16 to 32 transactions. This elevates GPU Tensor Core utilization from 18% to **over 85%**, quadrupling inference throughput while adding less than 2ms of latency.
  - *Model Concurrency & Execution Instances:* Triton hosts multiple concurrent execution instances of the LightGBM and Deep Autoencoder models across available GPU/CPU cores, servicing independent requests in parallel without lock contention.
  - *Model Quantization (INT8 / FP16):* Pre-trained models are compiled into optimized **NVIDIA TensorRT** engines using 8-bit integer (INT8) quantization with calibration caches. This slashes inference memory consumption by 75% and reduces execution latency from 28ms to **< 10ms**.
  - *Autonomous GPU Node Autoscaling:* AWS Karpenter / GKE Cluster Autoscaler monitors GPU pod pending queues, automatically provisioning dedicated GPU worker instances (EC2 `g5.xlarge` with NVIDIA A10G) in under 45 seconds during severe load spikes.
* **Analytical Lakehouse Query Scaling (Apache Iceberg & Distributed Engines):**
  - *Columnar Parquet & Zstandard (ZSTD) Compression:* Raw transactions and evaluation decisions are written to S3 in columnar Parquet format using ZSTD compression level 7, achieving a 6:1 compression ratio and minimizing storage I/O.
  - *Partition Pruning:* Iceberg tables are partitioned hierarchically by `year=YYYY/month=MM/day=DD/hour=HH`. When compliance officers or fraud data scientists query a specific 4-hour window, the query planner executes **metadata partition pruning**, skipping 99.9% of historical lakehouse files.
  - *Decoupled Serverless Query Compute:* Analytical queries are executed via distributed SQL engines (Trino / AWS Athena) where query execution nodes scale independently from the underlying S3 Object Lock storage, preventing analytics queries from contending with real-time stream ingestion.

---

#### 3. Scaling Event Messaging & Exactly-Once Semantics during Horizontal Scaling
The event messaging layer is the nervous system of the architecture. Scaling event messaging requires precise coordination between **Kafka topic partitioning**, **consumer group rebalancing**, and **offset commit discipline** to guarantee that scaling events never introduce duplicate processing or unhandled records.

* **Kafka Partitioning Topology & Uniform Load Distribution:**
  - *32 Partitions per Topic:* The baseline 1,000 TPS load is distributed across 32 partitions, yielding an average throughput of **~31.25 messages per second per partition**. This provides enormous operational headroom: a single well-tuned consumer pod can easily process 1,200+ records/sec. During super-peak surges of 3,000+ TPS, each partition processes ~93 msgs/sec, well within single-core processing limits.
  - *Partition Key Strategy:* Records are partitioned using a Murmur2 hash of the `account_id`. Because retail and commercial bank account numbers are evenly distributed across customer bases, traffic distributes symmetrically across all 32 partitions with zero hot-spotting.
* **Consumer Group Rebalancing & Horizontal Scaling Lifecycle:**
  When KEDA detects rising consumer lag and scales consumer pods from 4 to 16 or 32 replicas (or scales down during off-peak periods), Kafka must reassign partitions among group members. The architecture eliminates scaling vulnerabilities through four mechanisms:
  
  1. *Incremental Cooperative Rebalancing (`CooperativeStickyAssignor`):*
     - The platform enforces `partition.assignment.strategy = org.apache.kafka.clients.consumer.CooperativeStickyAssignor`.
     - *Why it matters:* In legacy eager rebalancing, *all* consumers were forced to stop processing, revoke all partitions, and rejoin the group, causing a catastrophic "stop-the-world" latency spike during the exact moments when traffic was surging.
     - *Under Cooperative Rebalancing:* Only the specific subset of partitions migrating to the newly scaled consumer pod is revoked. Unaffected consumer pods continue processing their assigned partitions without dropping a single millisecond of throughput.
  
  2. *The `ConsumerRebalanceListener` Lifecycle:*
     Every consumer pod registers a lifecycle listener that manages offset commits and in-flight records when partitions are reassigned:
     - **`onPartitionsRevoked(Collection<TopicPartition> partitions)`:**
       1. The consumer immediately ceases polling for new records on the revoked partitions.
       2. The consumer thread pool **drains all currently buffered in-flight records** for those partitions, completing feature computation or database insertion.
       3. The consumer executes a **synchronous offset commit (`commitSync()`)** for the drained partitions, ensuring that Kafka's `__consumer_offsets` topic reflects the exact last successfully processed record.
       4. Local partition state (e.g., in-memory window buffers) is checkpointed and flushed before partition ownership is relinquished.
     - **`onPartitionsAssigned(Collection<TopicPartition> partitions)`:**
       1. The newly assigned consumer initializes local state.
       2. It fetches the committed offset from Kafka (or queries the database offset table for sink services).
       3. It calls `consumer.seek()` to start reading strictly from the next unprocessed record (`committed_offset + 1`).
     - **`onPartitionsLost(Collection<TopicPartition> partitions)`:**
       - Invoked if the consumer drops offline due to a network partition or heartbeat expiration (`max.poll.interval.ms` exceeded). The listener immediately discards local uncommitted buffers and aborts active transactions, preventing the zombie instance from overwriting progress made by the reassigned consumer.

  3. *Exactly-Once Processing (EOS) in Stream Hops via Kafka Transactional API:*
     For stream-to-stream processing hops (`Feature Aggregator` consuming `trans.raw.v1` and emitting `trans.enriched.v1`, and `Fraud Scoring Engine` consuming `trans.enriched.v1` and emitting `fraud.evaluated.v1`), the platform implements **Kafka Transactions**:
     - *Mechanism:* Each consumer instance is assigned a static, unique `transactional.id` (e.g., `fse-eval-worker-<partition_id>`).
     - *Atomic Execution Loop:*
       ```java
       producer.beginTransaction();
       ConsumerRecords<String, Transaction> batch = consumer.poll(Duration.ofMillis(10));
       for (ConsumerRecord<String, Transaction> record : batch) {
           EvaluationResult result = evaluateFraudModel(record.value());
           producer.send(new ProducerRecord<>("financial.fraud.evaluated.v1", result));
       }
       // Atomically commit consumer offset INSIDE the Kafka transaction
       producer.sendOffsetsToTransaction(currentOffsets, "fraud-scoring-group");
       producer.commitTransaction();
       ```
     - *Behavior During Scale-Out / Rebalance:* If a consumer pod is evicted or rebalanced mid-batch, the uncommitted Kafka transaction is aborted automatically by the broker. Downstream consumers configured with `isolation.level = read_committed` will **never read the aborted records**. The newly assigned consumer resumes from the last committed offset, guaranteeing 100% exactly-once processing with zero duplicate messages.
     - *Zombie Fencing:* If a lagging pod awakens after a rebalance, Kafka brokers reject any write attempts because the transaction coordinator incremented the `producer_epoch` for that `transactional.id`, throwing a `ProducerFencedException`.

  4. *Atomic Database-Coupled Offset Storage for Sink Services:*
     For microservices that write directly to external datastores (such as `Case Management BFF` inserting alerts into Amazon Aurora PostgreSQL), Kafka transactions cannot span external relational databases. To guarantee exactly-once processing during horizontal scaling, the service implements the **Transactional Sink Pattern**:
     - *Atomic Dual-Write:* In the exact same PostgreSQL ACID transaction that inserts the fraud case, the service updates a dedicated `kafka_consumer_offsets` table:
       ```sql
       BEGIN TRANSACTION;
       INSERT INTO fraud_cases (case_id, transaction_id, account_id, fraud_score, status)
       VALUES ('ALT-9041', 'TX-89104', 'AC-11209', 0.94, 'NEW');
       
       INSERT INTO kafka_consumer_offsets (consumer_group, topic_name, partition_id, offset)
       VALUES ('case-mgmt-group', 'financial.fraud.alert.v1', 12, 482910)
       ON CONFLICT (consumer_group, topic_name, partition_id)
       DO UPDATE SET offset = EXCLUDED.offset;
       COMMIT;
       ```
     - *Deterministic Rebalance Seek:* When a new pod is assigned partition 12 during horizontal scaling, its `onPartitionsAssigned()` hook queries:
       ```sql
       SELECT offset FROM kafka_consumer_offsets 
       WHERE consumer_group = 'case-mgmt-group' AND topic_name = 'financial.fraud.alert.v1' AND partition_id = 12;
       ```
       The pod immediately executes `consumer.seek(partition12, offset + 1)`.
     - *Result:* Even if pod scaling or network failures crash worker instances mid-execution, the database transaction guarantees that case creation and offset commits succeed or fail together atomically. Duplicate alerts and phantom cases are mathematically eliminated.

"""

def get_html():
    return """
<section id="section-6" class="report-section">
  <div class="section-header">
    <span class="section-number">06</span>
    <div class="section-title-wrap">
      <h2>Scalability &amp; Resilience Engineering</h2>
      <p class="section-subtitle">Single Points of Failure mitigations, data loss prevention, deterministic replay pipelines, and KEDA elastic scaling.</p>
    </div>
  </div>

  <h3>6.1 Single Points of Failure (SPOFs) Identification &amp; Mitigation</h3>
  <p>Financial mission-critical architectures must be engineered under the assumption that any individual hardware node, network link, cloud availability zone, or software component can and will fail abruptly. The platform systematically identifies and neutralizes all potential Single Points of Failure:</p>

  <div class="table-container">
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 20%;">Potential SPOF</th>
          <th style="width: 25%;">Failure Scenario &amp; Impact</th>
          <th style="width: 35%;">Architectural Mitigation Strategy</th>
          <th style="width: 20%;">Target RTO / RPO</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Kafka Broker Failure</strong></td>
          <td>Loss of an entire cloud availability zone causes Kafka broker nodes to drop offline.</td>
          <td>Deploy across <strong>3 Availability Zones</strong> with Replication Factor 3 ($\text{RF}=3$) and $\text{min.insync.replicas}=2$. KRaft Quorum eliminates ZooKeeper SPOF.</td>
          <td><span class="badge badge-success">RPO = 0</span><br><span class="badge badge-primary">RTO &lt; 2s</span></td>
        </tr>
        <tr>
          <td><strong>Redis Cache Failure</strong></td>
          <td>Redis node crash prevents Feature Aggregator from retrieving rolling velocity state.</td>
          <td><strong>Redis Enterprise Multi-AZ Cluster</strong> with active-active Sentinel failover and AOF persistence. Microservices implement Resilience4j circuit breakers with local LRU fallback.</td>
          <td><span class="badge badge-success">Graceful Degradation</span><br><span class="badge badge-primary">RTO &lt; 3s</span></td>
        </tr>
        <tr>
          <td><strong>Triton ML Model Crash</strong></td>
          <td>GPU memory lock causes inference latency to exceed budget (&gt; 20ms).</td>
          <td>Envoy Sidecar Circuit Breakers enforce 20ms hard deadlines. On timeout, traffic instantly diverts to an embedded <strong>Heuristic Rule Engine</strong> (&lt; 2ms).</td>
          <td><span class="badge badge-success">RTO = 0</span><br>(Immediate Heuristic Fallback)</td>
        </tr>
        <tr>
          <td><strong>Case Database Outage</strong></td>
          <td>Hardware failure takes down primary PostgreSQL instance.</td>
          <td><strong>Amazon Aurora Multi-AZ</strong> with automated sub-30s failover. Kafka buffers fraud alerts for up to 14 days without dropping records while the database recovers.</td>
          <td><span class="badge badge-success">Zero Alert Loss</span><br><span class="badge badge-primary">RTO &lt; 30s</span></td>
        </tr>
      </tbody>
    </table>
  </div>

  <h3>6.2 Compliance Replay Pipeline &amp; Audit Reconstruction</h3>
  <p>A cornerstone requirement of Basel III and BCBS 239 is the ability to perform <strong>deterministic historical transaction replay</strong>. The platform establishes an automated replay pipeline:</p>

  <div class="card-grid">
    <div class="info-card">
      <div class="card-title">1. WORM Immutability</div>
      <p>All production Kafka streams are batch-compacted into Apache Parquet/Iceberg format and written to S3 Object Lock in Compliance Mode (7-year mandatory retention).</p>
    </div>
    <div class="info-card">
      <div class="card-title">2. Isolated Replay Topic</div>
      <p>Replay worker pods stream historical Parquet slices into an isolated Kafka topic (<code>trans.replay.v1</code>), preserving original timestamps without impacting production.</p>
    </div>
    <div class="info-card">
      <div class="card-title">3. Shadow Scoring Sandbox</div>
      <p>A dedicated Shadow Scoring Engine evaluates replayed transactions against new candidate models (v2.4) to benchmark false positive reductions before production release.</p>
    </div>
    <div class="info-card">
      <div class="card-title">4. Automated Parity Audits</div>
      <p>Hourly reconciliation workers compute checksums verifying that 100% of ingested Kafka events exist in the immutable WORM lakehouse with zero data loss (&Delta; = 0).</p>
    </div>
  </div>

  <h3>6.3 Comprehensive Scaling Strategies Across System Components</h3>
  <p>To sustain peak volumes of 1,000 TPS (with surge headroom up to 3,000+ TPS) while maintaining cost efficiency during off-peak night troughs (100 TPS), the platform implements dedicated scaling strategies across <strong>Individual Microservices</strong>, <strong>Analytic Workloads</strong>, and <strong>Event Messaging</strong>:</p>

  <div class="card-grid">
    <div class="info-card">
      <div class="card-title">1. Individual Microservices</div>
      <p>Stateless Go and Node.js pods scaled via KEDA on Kafka lag and HTTP rates. Sub-50ms cold starts, PodDisruptionBudgets (<code>minAvailable: 75%</code>), and cross-AZ anti-affinity spread ensure continuous availability.</p>
    </div>
    <div class="info-card">
      <div class="card-title">2. Analytic &amp; ML Workloads</div>
      <p>Flink Reactive Mode rescales stateful sliding windows across RocksDB partitions. Triton dynamically micro-batches GPU inference (2ms window) and runs INT8 TensorRT models, with Karpenter scaling GPU node pools.</p>
    </div>
    <div class="info-card">
      <div class="card-title">3. Event Messaging Topology</div>
      <p>32 partitions per topic keyed by <code>account_id</code> handle up to 3,000+ TPS uniformly. Storage-optimized brokers with KRaft quorum guarantee zero partition hot-spotting and sub-second failover.</p>
    </div>
    <div class="info-card">
      <div class="card-title">4. Exactly-Once Scaling (EOS)</div>
      <p>CooperativeStickyAssignor revokes only migrated partitions. Stream hops use Kafka Transactions (<code>sendOffsetsToTransaction</code>), while DB sinks commit Kafka offsets atomically inside the PostgreSQL ACID case transaction.</p>
    </div>
  </div>

  <div class="table-container">
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 22%;">Scaling Pillar</th>
          <th style="width: 48%;">Mechanism &amp; Rebalance Protocol</th>
          <th style="width: 30%;">Operational Guarantee</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Stateless Services</strong><br>(Ingress &amp; BFF)</td>
          <td>KEDA scales pod replicas based on request rates and consumer lag. Envoy maintains long-lived HTTP/2 multiplexed connections.</td>
          <td><span class="badge badge-success">Elastic Dynamic Range:</span> 4 to 32 pods; sub-50ms container initialization.</td>
        </tr>
        <tr>
          <td><strong>Analytic Workloads</strong><br>(Flink &amp; Triton)</td>
          <td>Flink Reactive Mode automatically redistributes RocksDB state partitions. Triton dynamically micro-batches inference requests over 2ms windows.</td>
          <td><span class="badge badge-primary">4x GPU Throughput:</span> INT8 quantization keeps model inference &lt; 10ms at 1,000 TPS.</td>
        </tr>
        <tr>
          <td><strong>Stream-to-Stream Hops</strong><br>(Feature Agg &amp; Scoring)</td>
          <td>Kafka Transactional API: <code>producer.sendOffsetsToTransaction()</code> commits offsets inside the transaction. Rebalances abort in-flight transactions with zombie fencing.</td>
          <td><span class="badge badge-success">Strictly Exactly-Once:</span> Downstream <code>read_committed</code> consumers never read aborted records.</td>
        </tr>
        <tr>
          <td><strong>Stream-to-Store Sinks</strong><br>(Case BFF &amp; Archiver)</td>
          <td>Transactional Sink Pattern: Consumer offset is committed in the <strong>exact same PostgreSQL ACID transaction</strong> as the case record. On rebalance, the pod seeks to <code>offset + 1</code>.</td>
          <td><span class="badge badge-warning">Zero Duplicate Cases:</span> Database rollback prevents phantom alerts during scale-out.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
"""