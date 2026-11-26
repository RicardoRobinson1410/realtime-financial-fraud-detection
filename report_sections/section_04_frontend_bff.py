"""
Section 4: Real-Time Analyst Frontend & BFF Architecture
"""

def get_markdown():
    return r"""## 4. Real-Time Analyst Frontend & BFF Architecture

### 4.1 Fraud Operations Console Requirements
A high-volume fraud detection platform is only as effective as the speed and accuracy of the human operations team that triages high-risk alerts. When sophisticated fraud attacks occur (e.g., account takeover blitzes or coordinated card fraud rings), the operational console is subjected to sudden floods of incoming alerts.

The frontend must satisfy four strict engineering requirements:
1. **Sub-Second Alert Latency:** High-confidence alerts ($S \ge 0.75$) must appear on an analyst's screen within **< 200 milliseconds** of model classification.
2. **Zero UI Freezing (60 FPS Under Heavy Load):** Even when processing an incoming surge of 15,000+ alerts, the interface must never drop frames, freeze scroll positions, or experience UI thread jank.
3. **Explainable AI (XAI) Drilldowns:** Financial regulations (including GDPR Article 22 and FCRA in the US) mandate that automated credit and fraud rejections must be explainable. The console must display TreeSHAP feature contribution charts (e.g., indicating that a transaction was flagged because the IP address was located in Lagos while the physical card chip was used in London 12 minutes prior).
4. **Active Concurrency & Case Locking:** Prevent multiple analysts from inadvertently triaging or conflicting on the same fraud case simultaneously through real-time presence indicators and distributed mutex locks.

---

### 4.2 Real-Time Ingestion Protocol: WebSockets vs. Server-Sent Events
To stream live alerts from the cloud platform to analyst browsers, the architecture evaluated Server-Sent Events (SSE) versus WebSockets (WSS).

| Criteria | Server-Sent Events (SSE) | WebSocket (WSS with STOMP) | Architectural Verdict |
| :--- | :--- | :--- | :--- |
| **Directionality** | Unidirectional (Server $\to$ Client only). Client actions must use separate HTTP POSTs. | Full-duplex bidirectional communication over a single persistent TCP socket. | **Hybrid Selection:**<br>1. **WebSocket (WSS/STOMP)** for the high-frequency real-time alert feed, analyst presence heartbeats, and live case locking.<br>2. **HTTP/2 REST/GraphQL** for mutative case actions and large historical dossier queries. |
| **Connection Overhead** | Minimal. Runs over standard HTTP/2 multiplexed streams; handles reconnections natively. | Low after handshake. Requires stateful connection tracking across load balancers. |
| **Protocol Governance** | Plain text event streams. No standard message framing or sub-protocols. | Rich sub-protocol ecosystem (**STOMP** over WebSocket provides native pub/sub, destination queues, and ACK frames). |
| **Proxy & Firewall Compatibility** | Traverses standard corporate corporate enterprise firewalls with zero friction. | Occasionally blocked by legacy HTTP proxies unless upgraded through standard port 443 with TLS. |

---

### 4.3 Backend-for-Frontend (BFF) Pattern Implementation
Directly connecting browser applications to underlying microservices is an anti-pattern that leads to severe over-fetching, chatty mobile/web networks, and tight coupling with internal database schemas. The platform introduces a dedicated **Analyst BFF Service** built in Node.js 22 (Fastify) and TypeScript:

```
[ Active Analysts ] ──WSS/REST──► [ Analyst BFF Cluster (Node.js) ]
                                          │            ▲
                    ┌─────────────────────┼────────────┴────────┐
                    ▼                     ▼                     ▼
         [ Redis Pub/Sub Hub ]  [ Aurora PostgreSQL ]  [ Kafka: fraud.alert.v1 ]
           (Analyst Presence &    (Case Entities &       (Consumes New Alerts)
            Cluster Fan-Out)       Audit History)
```

1. **Aggregation & ViewModel Transformation:** When a new `FraudAlertRaisedEvent` is received from Kafka, the BFF automatically queries internal services to hydrate the alert with customer KYC risk tiers, cardholder account standing, recent chargeback history, and device fingerprint intelligence. It strips unneeded fields and constructs a lightweight, UI-tailored JSON ViewModel, reducing network payload size by **over 70%** compared to raw microservice representations.
2. **Horizontal Cluster Synchronization via Redis Pub/Sub:** In a production deployment with multiple BFF pod replicas behind an Application Load Balancer, analysts may be connected to different BFF instances. The BFF cluster uses a Redis Enterprise Pub/Sub backbone to fan out incoming alerts and synchronize active case locks instantly across all pods.
3. **Session Management & Zero-Trust RBAC:** The BFF validates OIDC JSON Web Tokens (JWT) issued by the bank's enterprise identity provider (Okta / Azure AD / Ping Identity). Fine-grained Role-Based Access Control (RBAC) ensures Tier 1 junior analysts can only view unmasked card tokens and trigger customer verification SMS, while Tier 2 senior investigators have permissions to initiate permanent account closures and Law Enforcement referral packages.

---

### 4.4 Frontend Performance Optimizations
To maintain fluid 60 FPS performance and prevent browser memory exhaustion during high-volume fraud attacks, four core client-side optimizations are implemented:

#### 1. DOM Virtualization & Windowing (`TanStack Virtual`)
Standard web browsers experience severe rendering degradation when rendering more than 500 complex DOM nodes simultaneously. The console employs **DOM Virtualization (Windowing)**. 
Regardless of whether there are 50 alerts or 25,000 alerts queued in the client application's memory store, the virtualized grid dynamically renders **only the ~20 visible DOM elements** currently within the user's viewport, recycling DOM nodes as the user scrolls. Memory consumption remains strictly bounded at $< 80\text{ MB}$, and scrolling remains perfectly smooth at 60 FPS.

#### 2. Client-Side Caching & Optimistic UI Updates (`TanStack Query`)
The frontend uses `TanStack Query` (React Query) for robust server-state management. When an analyst clicks "Confirm Fraud & Block Card", the console:
- Immediately updates the local UI optimistically (marking the alert as resolved and removing it from the active queue).
- Dispatches the asynchronous mutation request to the BFF in the background.
- If the server confirms, the cache is finalized; if an error occurs, the UI seamlessly rolls back and notifies the analyst with actionable error diagnostics.

#### 3. Web Worker Background Thread Offloading
Heavy computational operations—such as fuzzy text searching across 10,000 in-memory alert items, multi-field filtering (e.g., "Filter by MCC = 5732 AND Risk Score > 0.85"), and histogram bucket calculations—are offloaded to a dedicated browser **Web Worker thread**. By executing data crunching off the main JavaScript execution thread, the UI thread remains completely unblocked and receptive to user interactions.

#### 4. Priority Lane Routing & Alert Debouncing
Incoming alerts arrive at an in-memory client buffer. A priority routing engine ensures:
- **P1 Critical Alerts ($S \ge 0.90$):** Bypass all client-side buffers and are immediately inserted into the top of the alert feed, triggering an audible chime and visual border pulse.
- **P2 / P3 Elevated Alerts ($0.75 \le S < 0.90$):** Are debounced into 250ms batch flushes, preventing continuous DOM micro-refreshes from jarring the analyst's focus.
"""

def get_html():
    return r"""
<section id="section-4" class="report-section">
  <div class="section-header">
    <span class="section-number">04</span>
    <div class="section-title-wrap">
      <h2>Real-Time Analyst Frontend &amp; BFF Architecture</h2>
      <p class="section-subtitle">Real-time WebSocket streaming, Backend-for-Frontend orchestration, DOM virtualization, and Explainable AI (SHAP).</p>
    </div>
  </div>

  <h3>4.1 Fraud Operations Console Requirements</h3>
  <p>A high-volume fraud detection platform is only as effective as the speed and accuracy of the human operations team that triages high-risk alerts. When sophisticated fraud attacks occur (e.g., account takeover blitzes or coordinated card fraud rings), the operational console is subjected to sudden floods of incoming alerts.</p>
  <p>The frontend satisfies four strict engineering requirements:</p>

  <div class="card-grid">
    <div class="info-card">
      <div class="card-title">Sub-Second Latency (&lt; 200ms)</div>
      <p>High-confidence fraud alerts (Score &ge; 0.75) are pushed directly to the analyst's screen within 200 milliseconds of classification via persistent WebSockets.</p>
    </div>
    <div class="info-card">
      <div class="card-title">60 FPS DOM Virtualization</div>
      <p>TanStack Virtual recycles 20 visible DOM elements from an in-memory buffer of 15,000+ items, preventing memory bloat and UI freezing during fraud surges.</p>
    </div>
    <div class="info-card">
      <div class="card-title">Explainable AI (TreeSHAP)</div>
      <p>Visual radar charts display the top 5 predictive drivers (e.g., impossible travel velocity, foreign IP, sudden spending spike) to comply with FCRA and GDPR Art. 22.</p>
    </div>
    <div class="info-card">
      <div class="card-title">Distributed Mutex Case Locking</div>
      <p>Redis Pub/Sub coordinates real-time presence indicators across the analyst team, preventing two investigators from working on the same case concurrently.</p>
    </div>
  </div>

  <h3>4.2 Backend-for-Frontend (BFF) Pattern &amp; Streaming Protocol</h3>
  <p>Directly connecting browser applications to underlying microservices is an anti-pattern that leads to severe over-fetching, chatty mobile/web networks, and tight coupling with internal database schemas. The platform introduces a dedicated <strong>Analyst BFF Service</strong> built in Node.js 22 (Fastify) and TypeScript:</p>

  <div class="callout callout-info">
    <div class="callout-icon">&#8505;</div>
    <div class="callout-body">
      <h4>BFF ViewModel Optimization</h4>
      <p>The BFF hydrates incoming Kafka fraud alerts with customer KYC standing, past chargeback history, and device fingerprint data into a single tailored UI ViewModel. This eliminates chatty network waterfalls and cuts payload size by over 70% compared to raw microservice entity schemas.</p>
    </div>
  </div>

  <div class="table-container">
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 25%;">Optimization Mechanism</th>
          <th style="width: 45%;">Implementation Strategy</th>
          <th style="width: 30%;">Operational Performance Gain</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>DOM Virtualization</strong></td>
          <td>TanStack Virtual renders strictly the ~20 table rows within the active browser viewport, dynamically recycling DOM nodes as the user scrolls.</td>
          <td><span class="badge badge-success">Bounded Memory:</span> &lt; 80MB memory footprint; zero frame drops across 25,000+ alerts.</td>
        </tr>
        <tr>
          <td><strong>Client-Side Caching</strong></td>
          <td>TanStack Query v5 manages server state with optimistic UI mutations on case triage actions (Assign, Freeze, Resolve).</td>
          <td><span class="badge badge-success">Instant Feedback:</span> Sub-10ms perceived latency for analyst triage decisions.</td>
        </tr>
        <tr>
          <td><strong>Web Worker Offloading</strong></td>
          <td>Client-side multi-field filtering, fuzzy text searches, and risk score histogram bucketing run in a separate background Web Worker thread.</td>
          <td><span class="badge badge-primary">Zero Main-Thread Jank:</span> 100% responsiveness on UI input controls.</td>
        </tr>
        <tr>
          <td><strong>Priority Lane Routing</strong></td>
          <td>P1 Critical Alerts ($S \ge 0.90$) bypass queue throttles immediately; P2/P3 alerts are debounced into 250ms batch updates.</td>
          <td><span class="badge badge-warning">Triage Focus:</span> Eliminates continuous visual micro-refreshes for the operator.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
"""