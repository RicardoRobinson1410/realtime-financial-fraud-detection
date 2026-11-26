"""
Script to generate all 6 high-resolution SVG architecture diagrams for the
Real-Time Financial Fraud Detection System.
"""
import os

DIAGRAMS_DIR = os.path.join(os.path.dirname(__file__), "diagrams")
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

def get_diagram_1():
    """Diagram 1: End-to-End Solution Architecture (C4 Container Diagram)"""
    return '''<svg viewBox="0 0 1200 780" width="100%" height="780" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <linearGradient id="k8sGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e1e38" />
      <stop offset="100%" stop-color="#17172b" />
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.4"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#38bdf8"/>
    </marker>
    <marker id="arrowOrange" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#fb923c"/>
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#34d399"/>
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#f87171"/>
    </marker>
    <marker id="arrowPurple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#c084fc"/>
    </marker>
  </defs>

  <!-- Background Canvas -->
  <rect width="1200" height="780" fill="url(#bgGrad)" rx="12" />
  <rect x="15" y="15" width="1170" height="750" fill="none" stroke="#334155" stroke-width="1.5" rx="10" />

  <!-- Title Bar -->
  <text x="35" y="48" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700">Figure 1: Solution Architecture Diagram (C4 Container View)</text>
  <text x="35" y="70" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12">Cloud-Native, Real-Time Financial Fraud Detection Platform (Peak: 1,000 TPS | Latency P99 &lt; 45ms)</text>

  <!-- REGION 1: External Rails & Ingress (Left) -->
  <rect x="35" y="90" width="160" height="520" rx="8" fill="#1e293b" stroke="#475569" stroke-width="1" filter="url(#shadow)"/>
  <rect x="35" y="90" width="160" height="32" rx="8" fill="#334155" />
  <text x="115" y="111" fill="#f1f5f9" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Payment Ingress Rails</text>

  <!-- Card: Visa / MC / Swift -->
  <rect x="45" y="135" width="140" height="65" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
  <text x="115" y="158" fill="#e2e8f0" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Card Networks</text>
  <text x="115" y="174" fill="#94a3b8" font-family="sans-serif" font-size="9" text-anchor="middle">Visa / MC / Amex</text>
  <text x="115" y="188" fill="#38bdf8" font-family="monospace" font-size="9" text-anchor="middle">ISO 8583 / 20022</text>

  <!-- Card: Real-time Rails (FedNow / SEPA) -->
  <rect x="45" y="215" width="140" height="65" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
  <text x="115" y="238" fill="#e2e8f0" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Instant Payments</text>
  <text x="115" y="254" fill="#94a3b8" font-family="sans-serif" font-size="9" text-anchor="middle">FedNow / SEPA Instant</text>
  <text x="115" y="268" fill="#38bdf8" font-family="monospace" font-size="9" text-anchor="middle">Sub-second Clearing</text>

  <!-- Card: Core Banking System -->
  <rect x="45" y="295" width="140" height="65" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
  <text x="115" y="318" fill="#e2e8f0" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Core Banking System</text>
  <text x="115" y="334" fill="#94a3b8" font-family="sans-serif" font-size="9" text-anchor="middle">DDA / Ledger / Accts</text>
  <text x="115" y="348" fill="#38bdf8" font-family="monospace" font-size="9" text-anchor="middle">REST / gRPC TLS 1.3</text>

  <!-- Card: Mobile & Online Banking -->
  <rect x="45" y="375" width="140" height="65" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
  <text x="115" y="398" fill="#e2e8f0" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Digital Channels</text>
  <text x="115" y="414" fill="#94a3b8" font-family="sans-serif" font-size="9" text-anchor="middle">Mobile Apps / Web</text>
  <text x="115" y="428" fill="#38bdf8" font-family="monospace" font-size="9" text-anchor="middle">OAuth2 / OIDC JWT</text>

  <!-- Card: Edge Gateway & Tokenizer -->
  <rect x="45" y="460" width="140" height="135" rx="6" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5"/>
  <text x="115" y="482" fill="#c7d2fe" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Edge API Gateway</text>
  <text x="115" y="498" fill="#a5b4fc" font-family="sans-serif" font-size="9" text-anchor="middle">Envoy / Kong Ingress</text>
  <line x1="55" y1="506" x2="175" y2="506" stroke="#4338ca" stroke-width="1" />
  <text x="55" y="522" fill="#e0e7ff" font-family="sans-serif" font-size="9">&#8226; WAF &amp; DDoS Shield</text>
  <text x="55" y="538" fill="#e0e7ff" font-family="sans-serif" font-size="9">&#8226; mTLS Termination</text>
  <text x="55" y="554" fill="#e0e7ff" font-family="sans-serif" font-size="9">&#8226; Rate Limiter (Token Bkt)</text>
  <text x="55" y="570" fill="#e0e7ff" font-family="sans-serif" font-size="9">&#8226; PAN Tokenizer (HSM)</text>

  <!-- Connectors from Rails to Gateway -->
  <path d="M 185 167 L 210 167 L 210 500 L 185 500" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="3,3" />
  <path d="M 185 247 L 205 247 L 205 520 L 185 520" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="3,3" />
  <path d="M 185 327 L 200 327 L 200 540 L 185 540" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="3,3" />

  <!-- REGION 2: Kubernetes Service Mesh Platform (Center) -->
  <rect x="225" y="90" width="670" height="520" rx="8" fill="url(#k8sGrad)" stroke="#6366f1" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="225" y="90" width="670" height="32" rx="8" fill="#312e81" />
  <text x="560" y="111" fill="#e0e7ff" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Cloud-Native Microservices Mesh (Kubernetes EKS / GKE + Istio Service Mesh)</text>

  <!-- Gateway to Ingestion Service Arrow -->
  <line x1="185" y1="527" x2="245" y2="527" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)" />
  <text x="215" y="520" fill="#38bdf8" font-family="sans-serif" font-size="8" text-anchor="middle">HTTPS/gRPC</text>

  <!-- Service 1: Ingestion Gateway Service -->
  <rect x="245" y="475" width="160" height="105" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="325" y="497" fill="#38bdf8" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Ingestion Gateway Svc</text>
  <text x="325" y="512" fill="#94a3b8" font-family="monospace" font-size="9" text-anchor="middle">Go 1.23 | KEDA Scaled</text>
  <line x1="255" y1="520" x2="395" y2="520" stroke="#334155" stroke-width="1" />
  <text x="255" y="535" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Schema Validate (Avro)</text>
  <text x="255" y="549" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Idempotency Check</text>
  <text x="255" y="563" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; W3C Trace Injection</text>

  <!-- Central Apache Kafka Event Backbone -->
  <rect x="245" y="325" width="630" height="120" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="2"/>
  <rect x="245" y="325" width="630" height="26" rx="8" fill="#78350f" />
  <text x="560" y="342" fill="#fef3c7" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Event Backbone: Apache Kafka Enterprise (32 Partitions / Topic | KRaft Quorum | 3-AZ Replicated)</text>

  <!-- Kafka Topics visual boxes -->
  <rect x="260" y="360" width="130" height="42" rx="4" fill="#1e293b" stroke="#fb923c" stroke-width="1"/>
  <text x="325" y="377" fill="#fb923c" font-family="monospace" font-size="9" font-weight="700" text-anchor="middle">trans.raw.v1</text>
  <text x="325" y="392" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Key: account_id</text>

  <rect x="410" y="360" width="145" height="42" rx="4" fill="#1e293b" stroke="#34d399" stroke-width="1"/>
  <text x="482" y="377" fill="#34d399" font-family="monospace" font-size="9" font-weight="700" text-anchor="middle">trans.enriched.v1</text>
  <text x="482" y="392" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Features Attached</text>

  <rect x="575" y="360" width="145" height="42" rx="4" fill="#1e293b" stroke="#f87171" stroke-width="1"/>
  <text x="647" y="377" fill="#f87171" font-family="monospace" font-size="9" font-weight="700" text-anchor="middle">fraud.evaluated.v1</text>
  <text x="647" y="392" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Score &amp; Decision</text>

  <rect x="740" y="360" width="120" height="42" rx="4" fill="#1e293b" stroke="#ef4444" stroke-width="1.5"/>
  <text x="800" y="377" fill="#ef4444" font-family="monospace" font-size="9" font-weight="700" text-anchor="middle">fraud.alert.v1</text>
  <text x="800" y="392" fill="#fca5a5" font-family="sans-serif" font-size="8" text-anchor="middle">Score &gt;= 0.75</text>

  <text x="560" y="425" fill="#94a3b8" font-family="monospace" font-size="8" text-anchor="middle">Dead Letter Queues (DLQ): trans.raw.dlq | trans.enriched.dlq | fraud.eval.dlq (Poison Pill Quarantine)</text>

  <!-- Ingestion produces to trans.raw.v1 -->
  <line x1="325" y1="475" x2="325" y2="408" stroke="#fb923c" stroke-width="2" marker-end="url(#arrowOrange)"/>
  <text x="335" y="445" fill="#fb923c" font-family="sans-serif" font-size="8">Publish Event</text>

  <!-- Service 2: Feature Aggregation Service -->
  <rect x="420" y="475" width="170" height="105" rx="6" fill="#1e293b" stroke="#34d399" stroke-width="1.5"/>
  <text x="505" y="497" fill="#34d399" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Feature Aggregation Svc</text>
  <text x="505" y="512" fill="#94a3b8" font-family="monospace" font-size="9" text-anchor="middle">Apache Flink / Streams</text>
  <line x1="430" y1="520" x2="580" y2="520" stroke="#334155" stroke-width="1" />
  <text x="430" y="535" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Velocity &amp; Frequency Windows</text>
  <text x="430" y="549" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Geo-Distance Velocity Check</text>
  <text x="430" y="563" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Historical Spending Deviation</text>

  <!-- In-Memory Distributed Cache (Redis) -->
  <rect x="420" y="620" width="170" height="55" rx="6" fill="#450a0a" stroke="#ef4444" stroke-width="1.5"/>
  <text x="505" y="642" fill="#fca5a5" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Redis Enterprise Cluster</text>
  <text x="505" y="658" fill="#f87171" font-family="monospace" font-size="8.5" text-anchor="middle">L2 Feature Cache (&lt;1ms)</text>

  <!-- Connectors for Feature Aggregator -->
  <path d="M 370 405 L 370 460 L 450 460 L 450 475" fill="none" stroke="#fb923c" stroke-width="1.5" marker-end="url(#arrowOrange)"/>
  <line x1="505" y1="580" x2="505" y2="614" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="2,2" marker-end="url(#arrowRed)"/>
  <line x1="535" y1="475" x2="535" y2="408" stroke="#34d399" stroke-width="2" marker-end="url(#arrowGreen)"/>
  <text x="545" y="445" fill="#34d399" font-family="sans-serif" font-size="8">Publish Enriched</text>

  <!-- Service 3: Fraud Scoring & ML Inference Engine -->
  <rect x="620" y="475" width="180" height="105" rx="6" fill="#1e293b" stroke="#f87171" stroke-width="1.5"/>
  <text x="710" y="497" fill="#f87171" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Fraud Scoring Engine</text>
  <text x="710" y="512" fill="#94a3b8" font-family="monospace" font-size="9" text-anchor="middle">Triton Inference | &lt;15ms</text>
  <line x1="630" y1="520" x2="790" y2="520" stroke="#334155" stroke-width="1" />
  <text x="630" y="535" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Rule Engine (Sanctions, Lists)</text>
  <text x="630" y="549" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; LightGBM / ONNX Ensemble</text>
  <text x="630" y="563" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Deep Autoencoder Anomaly</text>

  <!-- Connector from Enriched Topic to Scoring Engine -->
  <line x1="647" y1="405" x2="647" y2="470" stroke="#34d399" stroke-width="1.5" marker-end="url(#arrowGreen)"/>
  <!-- Scoring Engine publishes Evaluated and Alert -->
  <line x1="720" y1="475" x2="720" y2="408" stroke="#f87171" stroke-width="2" marker-end="url(#arrowRed)"/>
  <path d="M 770 475 L 770 430 L 810 430 L 810 408" fill="none" stroke="#ef4444" stroke-width="2" marker-end="url(#arrowRed)"/>

  <!-- Service 4: Notification & Downstream Action Service -->
  <rect x="245" y="145" width="180" height="100" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="335" y="167" fill="#38bdf8" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Downstream Action Svc</text>
  <text x="335" y="182" fill="#94a3b8" font-family="monospace" font-size="9" text-anchor="middle">Java Quarkus / Reactive</text>
  <line x1="255" y1="190" x2="415" y2="190" stroke="#334155" stroke-width="1" />
  <text x="255" y="205" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Automated Card Lock</text>
  <text x="255" y="219" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; 3DS Step-Up Challenge (SMS)</text>
  <text x="255" y="233" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Core Rail Settlement Block</text>

  <!-- Connector from Evaluated Topic to Downstream Action Svc -->
  <path d="M 647 360 L 647 280 L 335 280 L 335 251" fill="none" stroke="#f87171" stroke-width="1.5" marker-end="url(#arrowRed)"/>

  <!-- Service 5: Case Management & Analyst BFF Service -->
  <rect x="680" y="145" width="200" height="150" rx="6" fill="#1e293b" stroke="#c084fc" stroke-width="1.5"/>
  <text x="780" y="167" fill="#c084fc" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Case Management &amp; BFF</text>
  <text x="780" y="182" fill="#94a3b8" font-family="monospace" font-size="9" text-anchor="middle">Node.js 22 / Fastify</text>
  <line x1="690" y1="190" x2="870" y2="190" stroke="#334155" stroke-width="1" />
  <text x="690" y="205" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Alert Triage &amp; Queue Mgmt</text>
  <text x="690" y="219" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; WebSocket Hub (STOMP/Push)</text>
  <text x="690" y="233" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; SHAP Attribution Aggregation</text>
  <text x="690" y="247" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; RBAC &amp; Audit Trail</text>
  <rect x="690" y="258" width="180" height="28" rx="4" fill="#0f172a" stroke="#818cf8" stroke-width="1"/>
  <text x="780" y="276" fill="#c7d2fe" font-family="sans-serif" font-size="9" text-anchor="middle">PostgreSQL Case Store (Multi-AZ)</text>

  <!-- Connector from Alert Topic to Case Mgmt BFF -->
  <path d="M 800 360 L 800 301" fill="none" stroke="#ef4444" stroke-width="2" marker-end="url(#arrowRed)"/>

  <!-- REGION 3: Frontend & Analyst Console (Top Right) -->
  <rect x="920" y="90" width="250" height="230" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="920" y="90" width="250" height="32" rx="8" fill="#0369a1" />
  <text x="1045" y="111" fill="#f0f9ff" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Fraud Analyst Real-Time Console</text>

  <rect x="935" y="135" width="220" height="170" rx="6" fill="#0f172a" stroke="#0ea5e9" stroke-width="1"/>
  <text x="1045" y="155" fill="#e0f2fe" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">React 19 / Next.js SPA</text>
  <text x="945" y="175" fill="#bae6fd" font-family="sans-serif" font-size="8.5">&#8226; WebSocket Live Alert Stream</text>
  <text x="945" y="191" fill="#bae6fd" font-family="sans-serif" font-size="8.5">&#8226; DOM Virtualized Feed (10k items)</text>
  <text x="945" y="207" fill="#bae6fd" font-family="sans-serif" font-size="8.5">&#8226; Explainable AI (SHAP Radar Chart)</text>
  <text x="945" y="223" fill="#bae6fd" font-family="sans-serif" font-size="8.5">&#8226; 1-Click Freeze / Whitelist / Escalate</text>
  <text x="945" y="239" fill="#bae6fd" font-family="sans-serif" font-size="8.5">&#8226; TanStack Query Optimistic Cache</text>
  <text x="945" y="255" fill="#bae6fd" font-family="sans-serif" font-size="8.5">&#8226; Web Worker Background Filter</text>
  <rect x="945" y="268" width="200" height="26" rx="4" fill="#0369a1" />
  <text x="1045" y="285" fill="#ffffff" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">Analyst Response Time &lt; 2.5s</text>

  <!-- BFF to Frontend WebSocket Arrow -->
  <line x1="880" y1="215" x2="914" y2="215" stroke="#38bdf8" stroke-width="2" stroke-dasharray="3,3" marker-end="url(#arrow)"/>
  <text x="900" y="205" fill="#38bdf8" font-family="sans-serif" font-size="8" text-anchor="middle">WSS</text>

  <!-- REGION 4: Compliance, Audit & Replay (Bottom Right) -->
  <rect x="920" y="340" width="250" height="270" rx="8" fill="#1e293b" stroke="#a855f7" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="920" y="340" width="250" height="32" rx="8" fill="#6b21a8" />
  <text x="1045" y="361" fill="#faf5ff" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Compliance, Audit &amp; Replay (CAR)</text>

  <!-- Service 6: Compliance Replay Service -->
  <rect x="935" y="385" width="220" height="95" rx="6" fill="#0f172a" stroke="#c084fc" stroke-width="1"/>
  <text x="1045" y="405" fill="#f3e8ff" font-family="sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">Compliance &amp; Replay Engine</text>
  <text x="945" y="425" fill="#e9d5ff" font-family="sans-serif" font-size="8.5">&#8226; Immutable Stream Archival</text>
  <text x="945" y="440" fill="#e9d5ff" font-family="sans-serif" font-size="8.5">&#8226; BCBS 239 / Basel III Compliance</text>
  <text x="945" y="455" fill="#e9d5ff" font-family="sans-serif" font-size="8.5">&#8226; Deterministic Replay Worker Pool</text>
  <text x="945" y="470" fill="#e9d5ff" font-family="sans-serif" font-size="8.5">&#8226; Shadow Model Backtesting</text>

  <!-- Immutable Storage (S3 Object Lock / WORM) -->
  <rect x="935" y="495" width="220" height="100" rx="6" fill="#2e1065" stroke="#d8b4fe" stroke-width="1.5"/>
  <text x="1045" y="517" fill="#f5d0fe" font-family="sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">WORM Compliance Lakehouse</text>
  <text x="1045" y="533" fill="#e879f9" font-family="sans-serif" font-size="9" text-anchor="middle">AWS S3 / GCS Object Lock (7-Yr Retention)</text>
  <line x1="945" y1="540" x2="1145" y2="540" stroke="#701a75" stroke-width="1" />
  <text x="945" y="556" fill="#fdf4ff" font-family="sans-serif" font-size="8.5">&#8226; Apache Iceberg on Parquet (ZSTD)</text>
  <text x="945" y="571" fill="#fdf4ff" font-family="sans-serif" font-size="8.5">&#8226; Bit-for-bit Deterministic Replay</text>
  <text x="945" y="586" fill="#fdf4ff" font-family="sans-serif" font-size="8.5">&#8226; Hourly Reconciliation Checksums</text>

  <!-- Connectors to Compliance -->
  <path d="M 875 385 L 900 385 L 900 420 L 929 420" fill="none" stroke="#c084fc" stroke-width="1.5" marker-end="url(#arrowPurple)"/>
  <line x1="1045" y1="480" x2="1045" y2="489" stroke="#d8b4fe" stroke-width="1.5" marker-end="url(#arrowPurple)"/>

  <!-- REGION 5: Enterprise Observability & Telemetry (Bottom Full Strip) -->
  <rect x="35" y="625" width="1135" height="135" rx="8" fill="#090d16" stroke="#0284c7" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="35" y="625" width="1135" height="26" rx="8" fill="#0369a1" />
  <text x="600" y="642" fill="#f0f9ff" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Enterprise Unified Observability, Telemetry &amp; SLO Management Layer (OpenTelemetry Standard)</text>

  <!-- Sub-components in Observability -->
  <rect x="50" y="660" width="240" height="85" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
  <text x="170" y="678" fill="#38bdf8" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Distributed Tracing (Tempo/Jaeger)</text>
  <text x="60" y="696" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; W3C TraceContext Injected into Kafka</text>
  <text x="60" y="711" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; End-to-end Span Propagation</text>
  <text x="60" y="726" fill="#38bdf8" font-family="sans-serif" font-size="8" font-weight="700">&#8226; SLO: E2E P99 Latency &lt; 45ms</text>

  <rect x="310" y="660" width="240" height="85" rx="6" fill="#1e293b" stroke="#34d399" stroke-width="1"/>
  <text x="430" y="678" fill="#34d399" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Metrics &amp; SLOs (Prometheus)</text>
  <text x="320" y="696" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Transaction Throughput &amp; Error Rate</text>
  <text x="320" y="711" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Kafka Consumer Lag &amp; Pod Saturation</text>
  <text x="320" y="726" fill="#34d399" font-family="sans-serif" font-size="8" font-weight="700">&#8226; SLO: Pipeline Availability &gt;= 99.99%</text>

  <rect x="570" y="660" width="240" height="85" rx="6" fill="#1e293b" stroke="#fb923c" stroke-width="1"/>
  <text x="690" y="678" fill="#fb923c" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Centralized Logging (Loki)</text>
  <text x="580" y="696" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; JSON Structured Logs with trace_id</text>
  <text x="580" y="711" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; FluentBit Agent on K8s DaemonSets</text>
  <text x="580" y="726" fill="#fb923c" font-family="sans-serif" font-size="8" font-weight="700">&#8226; PII &amp; PAN Data Masked at Ingress</text>

  <rect x="830" y="660" width="325" height="85" rx="6" fill="#1e293b" stroke="#c084fc" stroke-width="1"/>
  <text x="992" y="678" fill="#c084fc" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Cross-Pillar Correlation &amp; Grafana</text>
  <text x="840" y="696" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Prometheus Exemplars link Metric Spike -&gt; Trace ID</text>
  <text x="840" y="711" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Single Click Jump: Trace Waterfall -&gt; Microservice Logs</text>
  <text x="840" y="726" fill="#c084fc" font-family="sans-serif" font-size="8" font-weight="700">&#8226; Automated PagerDuty &amp; Slack Alerting Integrations</text>

</svg>'''

def get_diagram_2():
    """Diagram 2: Event Flow & Pub/Sub Messaging Backbone Diagram"""
    return '''<svg viewBox="0 0 1200 750" width="100%" height="750" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
    <filter id="shadow2" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000000" flood-opacity="0.35"/>
    </filter>
    <marker id="arBlue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#38bdf8"/>
    </marker>
    <marker id="arOrange" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#fb923c"/>
    </marker>
    <marker id="arGreen" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#34d399"/>
    </marker>
    <marker id="arRed" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#f87171"/>
    </marker>
    <marker id="arPurple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#c084fc"/>
    </marker>
  </defs>

  <rect width="1200" height="750" fill="url(#bgGrad2)" rx="12" />
  <rect x="15" y="15" width="1170" height="720" fill="none" stroke="#334155" stroke-width="1.5" rx="10" />

  <!-- Title -->
  <text x="35" y="48" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700">Figure 2: Event-Driven Messaging Backbone &amp; Exactly-Once Scaling Architecture</text>
  <text x="35" y="70" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12">Topic Partitioning, CooperativeStickyAssignor, Consumer Offset Commit Protocols &amp; Rebalance State Management</text>

  <!-- COLUMN 1: Producers (Left) -->
  <rect x="35" y="95" width="190" height="520" rx="8" fill="#1e293b" stroke="#475569" stroke-width="1" filter="url(#shadow2)"/>
  <rect x="35" y="95" width="190" height="32" rx="8" fill="#334155"/>
  <text x="130" y="116" fill="#f1f5f9" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Event Producers</text>

  <!-- Producer 1 -->
  <rect x="45" y="140" width="170" height="75" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>
  <text x="130" y="165" fill="#38bdf8" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Ingestion Gateway</text>
  <text x="130" y="183" fill="#94a3b8" font-family="sans-serif" font-size="8.5" text-anchor="middle">HTTP/gRPC Ingress Pods</text>
  <text x="130" y="199" fill="#38bdf8" font-family="monospace" font-size="8.5" text-anchor="middle">Idempotent Producer (acks=all)</text>

  <!-- Producer 2 -->
  <rect x="45" y="240" width="170" height="75" rx="6" fill="#0f172a" stroke="#34d399" stroke-width="1.2"/>
  <text x="130" y="265" fill="#34d399" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Feature Aggregator</text>
  <text x="130" y="283" fill="#94a3b8" font-family="sans-serif" font-size="8.5" text-anchor="middle">Flink Stream Processor</text>
  <text x="130" y="299" fill="#34d399" font-family="monospace" font-size="8.5" text-anchor="middle">Transactional Producer ID</text>

  <!-- Producer 3 -->
  <rect x="45" y="340" width="170" height="75" rx="6" fill="#0f172a" stroke="#f87171" stroke-width="1.2"/>
  <text x="130" y="365" fill="#f87171" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Fraud Scoring Engine</text>
  <text x="130" y="383" fill="#94a3b8" font-family="sans-serif" font-size="8.5" text-anchor="middle">Triton Inference Ensemble</text>
  <text x="130" y="399" fill="#f87171" font-family="monospace" font-size="8.5" text-anchor="middle">Transactional ID (EOS Hop)</text>

  <!-- Producer 4 -->
  <rect x="45" y="440" width="170" height="75" rx="6" fill="#0f172a" stroke="#c084fc" stroke-width="1.2"/>
  <text x="130" y="465" fill="#c084fc" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Case Mgmt / Analyst UI</text>
  <text x="130" y="483" fill="#94a3b8" font-family="sans-serif" font-size="8.5" text-anchor="middle">BFF / Analyst Action API</text>
  <text x="130" y="499" fill="#c084fc" font-family="monospace" font-size="8.5" text-anchor="middle">Atomic DB Sink Commits</text>

  <!-- Producer 5 -->
  <rect x="45" y="535" width="170" height="65" rx="6" fill="#0f172a" stroke="#e879f9" stroke-width="1.2"/>
  <text x="130" y="560" fill="#e879f9" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Replay Coordinator</text>
  <text x="130" y="578" fill="#94a3b8" font-family="sans-serif" font-size="8.5" text-anchor="middle">Historical Backtest Injector</text>

  <!-- COLUMN 2: Apache Kafka Topic Topology (Center) -->
  <rect x="250" y="95" width="480" height="520" rx="8" fill="#0b1329" stroke="#f59e0b" stroke-width="1.5" filter="url(#shadow2)"/>
  <rect x="250" y="95" width="480" height="32" rx="8" fill="#78350f"/>
  <text x="490" y="116" fill="#fef3c7" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Apache Kafka Topic Topology (32 Partitions | Key: account_id | acks=all)</text>

  <!-- Topic 1 -->
  <rect x="265" y="135" width="450" height="80" rx="6" fill="#1e293b" stroke="#fb923c" stroke-width="1.2"/>
  <text x="280" y="155" fill="#fb923c" font-family="monospace" font-size="10.5" font-weight="700">Topic: financial.trans.received.v1</text>
  <text x="695" y="155" fill="#94a3b8" font-family="sans-serif" font-size="8.5" text-anchor="end">Partitions: 32 | Retention: 7d</text>
  <text x="280" y="172" fill="#cbd5e1" font-family="sans-serif" font-size="8">Payload: Raw transaction message, ISO 20022 fields, tokenized PAN, timestamp, channel, IP, device</text>
  <text x="280" y="187" fill="#94a3b8" font-family="monospace" font-size="7.5">Key: transaction.account_id | Schema: Avro ID: 1042 (Schema Registry)</text>
  <rect x="280" y="193" width="220" height="15" rx="3" fill="#334155"/>
  <text x="285" y="204" fill="#f8fafc" font-family="monospace" font-size="7.5">DLQ: financial.trans.received.dlq</text>

  <!-- Topic 2 -->
  <rect x="265" y="225" width="450" height="80" rx="6" fill="#1e293b" stroke="#34d399" stroke-width="1.2"/>
  <text x="280" y="245" fill="#34d399" font-family="monospace" font-size="10.5" font-weight="700">Topic: financial.trans.enriched.v1</text>
  <text x="695" y="245" fill="#94a3b8" font-family="sans-serif" font-size="8.5" text-anchor="end">Partitions: 32 | Retention: 3d</text>
  <text x="280" y="262" fill="#cbd5e1" font-family="sans-serif" font-size="8">Payload: Raw payload + 5m/1h velocity counters, rolling sums, geo-distance velocity, risk flags</text>
  <text x="280" y="277" fill="#94a3b8" font-family="monospace" font-size="7.5">Key: transaction.account_id | Schema: Avro ID: 1043</text>
  <rect x="280" y="283" width="220" height="15" rx="3" fill="#334155"/>
  <text x="285" y="294" fill="#f8fafc" font-family="monospace" font-size="7.5">DLQ: financial.trans.enriched.dlq</text>

  <!-- Topic 3 -->
  <rect x="265" y="315" width="450" height="80" rx="6" fill="#1e293b" stroke="#f87171" stroke-width="1.2"/>
  <text x="280" y="335" fill="#f87171" font-family="monospace" font-size="10.5" font-weight="700">Topic: financial.fraud.evaluated.v1</text>
  <text x="695" y="335" fill="#94a3b8" font-family="sans-serif" font-size="8.5" text-anchor="end">Partitions: 32 | Retention: 7d</text>
  <text x="280" y="352" fill="#cbd5e1" font-family="sans-serif" font-size="8">Payload: Evaluation verdict (ALLOW / CHALLENGE / BLOCK), score [0.0-1.0], SHAP feature contributions</text>
  <text x="280" y="367" fill="#94a3b8" font-family="monospace" font-size="7.5">Key: transaction.transaction_id | Schema: Avro ID: 1044</text>
  <rect x="280" y="373" width="220" height="15" rx="3" fill="#334155"/>
  <text x="285" y="384" fill="#f8fafc" font-family="monospace" font-size="7.5">DLQ: financial.fraud.evaluated.dlq</text>

  <!-- Topic 4 -->
  <rect x="265" y="405" width="450" height="80" rx="6" fill="#1e293b" stroke="#ef4444" stroke-width="1.5"/>
  <text x="280" y="425" fill="#ef4444" font-family="monospace" font-size="10.5" font-weight="700">Topic: financial.fraud.alert.v1</text>
  <text x="695" y="425" fill="#fca5a5" font-family="sans-serif" font-size="8.5" text-anchor="end">Partitions: 16 | Retention: 14d</text>
  <text x="280" y="442" fill="#cbd5e1" font-family="sans-serif" font-size="8">Payload: High-confidence fraud alert (score &gt;= 0.75), alert priority (P1/P2/P3), top explainability drivers</text>
  <text x="280" y="457" fill="#94a3b8" font-family="monospace" font-size="7.5">Key: transaction.account_id | Schema: Avro ID: 1045</text>
  <rect x="280" y="463" width="220" height="15" rx="3" fill="#334155"/>
  <text x="285" y="474" fill="#f8fafc" font-family="monospace" font-size="7.5">DLQ: financial.fraud.alert.dlq</text>

  <!-- Topic 5: Replay & Case -->
  <rect x="265" y="495" width="450" height="80" rx="6" fill="#1e293b" stroke="#c084fc" stroke-width="1.2"/>
  <text x="280" y="515" fill="#c084fc" font-family="monospace" font-size="10.5" font-weight="700">Topic: compliance.trans.replay.v1 &amp; case.events.v1</text>
  <text x="695" y="515" fill="#94a3b8" font-family="sans-serif" font-size="8.5" text-anchor="end">Partitions: 32 | Isolated Shadow</text>
  <text x="280" y="532" fill="#cbd5e1" font-family="sans-serif" font-size="8">Payload: Replayed historical transaction packets; Case disposition changes (Analyst CONFIRMED / FALSE_POS)</text>
  <text x="280" y="547" fill="#94a3b8" font-family="monospace" font-size="7.5">Key: account_id / case_id | Strict isolation from live production metrics</text>

  <!-- Producer to Topic Arrows -->
  <line x1="215" y1="175" x2="260" y2="175" stroke="#fb923c" stroke-width="2" marker-end="url(#arOrange)"/>
  <line x1="215" y1="265" x2="260" y2="265" stroke="#34d399" stroke-width="2" marker-end="url(#arGreen)"/>
  <line x1="215" y1="365" x2="260" y2="365" stroke="#f87171" stroke-width="2" marker-end="url(#arRed)"/>
  <line x1="215" y1="475" x2="260" y2="535" stroke="#c084fc" stroke-width="2" marker-end="url(#arPurple)"/>
  <line x1="215" y1="565" x2="260" y2="545" stroke="#e879f9" stroke-width="2" marker-end="url(#arPurple)"/>

  <!-- COLUMN 3: Consumer Groups (Right) -->
  <rect x="755" y="95" width="410" height="520" rx="8" fill="#1e293b" stroke="#475569" stroke-width="1" filter="url(#shadow2)"/>
  <rect x="755" y="95" width="410" height="32" rx="8" fill="#334155"/>
  <text x="960" y="116" fill="#f1f5f9" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Consumer Groups &amp; Downstream Processors</text>

  <!-- CG 1: Feature Aggregation -->
  <rect x="770" y="135" width="380" height="80" rx="6" fill="#0f172a" stroke="#34d399" stroke-width="1.2"/>
  <text x="785" y="155" fill="#34d399" font-family="sans-serif" font-size="10.5" font-weight="700">CG: feature-agg-group (CooperativeStickyAssignor)</text>
  <text x="785" y="172" fill="#cbd5e1" font-family="sans-serif" font-size="8">Reads: trans.received.v1 | Sliding window state maintained in RocksDB / Redis</text>
  <text x="785" y="187" fill="#94a3b8" font-family="sans-serif" font-size="8">EOS: sendOffsetsToTransaction() commits offsets atomically inside Kafka txn</text>
  <text x="785" y="202" fill="#34d399" font-family="monospace" font-size="7.5">Scales: KEDA Consumer Lag &gt; 150 msgs/part | Zero stop-the-world pauses</text>

  <!-- CG 2: Fraud Scoring Engine -->
  <rect x="770" y="225" width="380" height="80" rx="6" fill="#0f172a" stroke="#f87171" stroke-width="1.2"/>
  <text x="785" y="245" fill="#f87171" font-family="sans-serif" font-size="10.5" font-weight="700">CG: fraud-scoring-group (Transactional EOS Hop)</text>
  <text x="785" y="262" fill="#cbd5e1" font-family="sans-serif" font-size="8">Reads: trans.enriched.v1 | Triton ML Ensemble (Dynamic Batch 2ms window)</text>
  <text x="785" y="277" fill="#94a3b8" font-family="sans-serif" font-size="8">Rebalance: onPartitionsRevoked() drains in-flight inference; aborts uncommitted</text>
  <text x="785" y="292" fill="#f87171" font-family="monospace" font-size="7.5">Zombie Fencing: Broker fences old pods via transactional.id &amp; epoch</text>

  <!-- CG 3: Case Management BFF & Real-Time Alerting -->
  <rect x="770" y="315" width="380" height="80" rx="6" fill="#0f172a" stroke="#ef4444" stroke-width="1.5"/>
  <text x="785" y="335" fill="#ef4444" font-family="sans-serif" font-size="10.5" font-weight="700">CG: case-management-group (Transactional Sink)</text>
  <text x="785" y="352" fill="#cbd5e1" font-family="sans-serif" font-size="8">Reads: fraud.alert.v1 | Atomic Dual-Write: Case record + Kafka offset in PostgreSQL</text>
  <text x="785" y="367" fill="#cbd5e1" font-family="sans-serif" font-size="8">Rebalance Seek: onPartitionsAssigned() queries DB offset table &amp; seeks deterministically</text>
  <text x="785" y="382" fill="#ef4444" font-family="monospace" font-size="7.5">Guaranteed Outcome: Zero duplicate alerts, phantom cases, or dropped records</text>

  <!-- CG 4: Downstream Action & Automated Enforcement -->
  <rect x="770" y="405" width="380" height="80" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>
  <text x="785" y="425" fill="#38bdf8" font-family="sans-serif" font-size="10.5" font-weight="700">CG: downstream-action-group (8 Pods / Quarkus)</text>
  <text x="785" y="442" fill="#cbd5e1" font-family="sans-serif" font-size="8">Reads: fraud.evaluated.v1 (Filtered for BLOCK/CHALLENGE decisions)</text>
  <text x="785" y="457" fill="#cbd5e1" font-family="sans-serif" font-size="8">Idempotent Card Lock: Processor API uses transaction_id as idempotency key</text>
  <text x="785" y="472" fill="#38bdf8" font-family="monospace" font-size="7.5">Execution SLA: &lt; 50ms | In-flight drain ensures no hold commands dropped</text>

  <!-- CG 5: Compliance Lakehouse Archival & Replay -->
  <rect x="770" y="495" width="380" height="80" rx="6" fill="#0f172a" stroke="#c084fc" stroke-width="1.2"/>
  <text x="785" y="515" fill="#c084fc" font-family="sans-serif" font-size="10.5" font-weight="700">CG: compliance-archiver-group &amp; shadow-replay</text>
  <text x="785" y="532" fill="#cbd5e1" font-family="sans-serif" font-size="8">Reads ALL Topics | Streams batches into S3/GCS Object Lock WORM storage</text>
  <text x="785" y="547" fill="#cbd5e1" font-family="sans-serif" font-size="8">Shadow Replay Group consumes trans.replay.v1 without mutating production</text>
  <text x="785" y="562" fill="#c084fc" font-family="monospace" font-size="7.5">Compliance Retention: 7 Years WORM (BCBS 239) | Checksum Parity &Delta; = 0</text>

  <!-- Topic to CG Connectors -->
  <line x1="715" y1="175" x2="765" y2="175" stroke="#34d399" stroke-width="2" marker-end="url(#arGreen)"/>
  <line x1="715" y1="265" x2="765" y2="265" stroke="#f87171" stroke-width="2" marker-end="url(#arRed)"/>
  <line x1="715" y1="445" x2="765" y2="355" stroke="#ef4444" stroke-width="2" marker-end="url(#arRed)"/>
  <line x1="715" y1="355" x2="765" y2="445" stroke="#38bdf8" stroke-width="2" marker-end="url(#arBlue)"/>
  <line x1="715" y1="535" x2="765" y2="535" stroke="#c084fc" stroke-width="2" marker-end="url(#arPurple)"/>

  <!-- HORIZONTAL EXACTLY-ONCE SCALING PROTOCOL BANNER (Bottom) -->
  <rect x="35" y="625" width="1130" height="100" rx="8" fill="#18182f" stroke="#38bdf8" stroke-width="1.5" filter="url(#shadow2)"/>
  <rect x="35" y="625" width="1130" height="24" rx="8" fill="#0369a1"/>
  <text x="600" y="641" fill="#f0f9ff" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">EXACTLY-ONCE HORIZONTAL SCALING &amp; CONSUMER REBALANCE PROTOCOL LIFECYCLE</text>

  <rect x="50" y="655" width="265" height="60" rx="5" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
  <text x="182" y="672" fill="#38bdf8" font-family="sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">1. Cooperative Sticky Assignor</text>
  <text x="60" y="688" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; KEDA triggers pod scale-out (Lag &gt; 150)</text>
  <text x="60" y="702" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; Revokes ONLY migrated partitions</text>

  <rect x="330" y="655" width="270" height="60" rx="5" fill="#1e293b" stroke="#34d399" stroke-width="1"/>
  <text x="465" y="672" fill="#34d399" font-family="sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">2. ConsumerRebalanceListener</text>
  <text x="340" y="688" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; onPartitionsRevoked(): In-flight drain</text>
  <text x="340" y="702" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; commitSync() flushes last processed offset</text>

  <rect x="615" y="655" width="265" height="60" rx="5" fill="#1e293b" stroke="#f87171" stroke-width="1"/>
  <text x="747" y="672" fill="#f87171" font-family="sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">3. Stream Hops: Transactional EOS</text>
  <text x="625" y="688" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; sendOffsetsToTransaction() in Kafka txn</text>
  <text x="625" y="702" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; Aborts mid-batch; broker zombie fencing</text>

  <rect x="895" y="655" width="255" height="60" rx="5" fill="#1e293b" stroke="#c084fc" stroke-width="1"/>
  <text x="1022" y="672" fill="#c084fc" font-family="sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">4. Sink Services: Atomic DB Commits</text>
  <text x="905" y="688" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; Dual-write: Case record + Offset in PostgreSQL</text>
  <text x="905" y="702" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; onPartitionsAssigned() seeks from DB table</text>

</svg>'''

def get_diagram_3():
    """Diagram 3: End-to-End Transaction Flow Sequence Diagram"""
    return '''<svg viewBox="0 0 1200 800" width="100%" height="800" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
    <marker id="sqArBlue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#38bdf8"/>
    </marker>
    <marker id="sqArGreen" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#34d399"/>
    </marker>
    <marker id="sqArRed" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#f87171"/>
    </marker>
    <marker id="sqArPurple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#c084fc"/>
    </marker>
  </defs>

  <rect width="1200" height="800" fill="url(#bgGrad3)" rx="12" />
  <rect x="15" y="15" width="1170" height="770" fill="none" stroke="#334155" stroke-width="1.5" rx="10" />

  <!-- Title -->
  <text x="35" y="46" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700">Figure 3: End-to-End Transaction Flow &amp; Classification Journey</text>
  <text x="35" y="68" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12">Sequence Diagram: Ingestion, Streaming Feature Enrichment, Triton ML Scoring, Real-time Analyst Alerting, and WORM Audit</text>

  <!-- Lifeline Columns (Headers) -->
  <!-- 1. Client / Rail -->
  <rect x="40" y="85" width="105" height="40" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
  <text x="92" y="105" fill="#38bdf8" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Payment Rail</text>
  <text x="92" y="118" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Visa / FedNow</text>
  <line x1="92" y1="125" x2="92" y2="760" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,4"/>

  <!-- 2. Gateway -->
  <rect x="160" y="85" width="105" height="40" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
  <text x="212" y="105" fill="#38bdf8" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">API Gateway</text>
  <text x="212" y="118" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Envoy / WAF</text>
  <line x1="212" y1="125" x2="212" y2="760" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,4"/>

  <!-- 3. Ingestion Svc -->
  <rect x="280" y="85" width="105" height="40" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
  <text x="332" y="105" fill="#38bdf8" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Ingestion Svc</text>
  <text x="332" y="118" fill="#94a3b8" font-family="monospace" font-size="8" text-anchor="middle">Go 1.23</text>
  <line x1="332" y1="125" x2="332" y2="760" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,4"/>

  <!-- 4. Kafka Event Backbone -->
  <rect x="400" y="85" width="115" height="40" rx="6" fill="#78350f" stroke="#fb923c" stroke-width="1"/>
  <text x="457" y="105" fill="#fef3c7" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Apache Kafka</text>
  <text x="457" y="118" fill="#fed7aa" font-family="monospace" font-size="8" text-anchor="middle">Topics Backbone</text>
  <line x1="457" y1="125" x2="457" y2="760" stroke="#78350f" stroke-width="1.5" stroke-dasharray="4,4"/>

  <!-- 5. Feature Agg & Redis -->
  <rect x="530" y="85" width="115" height="40" rx="6" fill="#1e293b" stroke="#34d399" stroke-width="1"/>
  <text x="587" y="105" fill="#34d399" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Feature Aggregator</text>
  <text x="587" y="118" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Flink + Redis L2</text>
  <line x1="587" y1="125" x2="587" y2="760" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,4"/>

  <!-- 6. Fraud Scoring Engine -->
  <rect x="660" y="85" width="115" height="40" rx="6" fill="#1e293b" stroke="#f87171" stroke-width="1"/>
  <text x="717" y="105" fill="#f87171" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Scoring Engine</text>
  <text x="717" y="118" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Triton / XGBoost</text>
  <line x1="717" y1="125" x2="717" y2="760" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,4"/>

  <!-- 7. Case BFF -->
  <rect x="790" y="85" width="105" height="40" rx="6" fill="#1e293b" stroke="#c084fc" stroke-width="1"/>
  <text x="842" y="105" fill="#c084fc" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Case BFF Svc</text>
  <text x="842" y="118" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Node.js + Postgres</text>
  <line x1="842" y1="125" x2="842" y2="760" stroke="#334155" stroke-width="1.2" stroke-dasharray="4,4"/>

  <!-- 8. Analyst UI -->
  <rect x="910" y="85" width="105" height="40" rx="6" fill="#0369a1" stroke="#38bdf8" stroke-width="1"/>
  <text x="962" y="105" fill="#ffffff" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Analyst Console</text>
  <text x="962" y="118" fill="#bae6fd" font-family="sans-serif" font-size="8" text-anchor="middle">React 19 / WSS</text>
  <line x1="962" y1="125" x2="962" y2="760" stroke="#0369a1" stroke-width="1.2" stroke-dasharray="4,4"/>

  <!-- 9. Compliance S3 WORM -->
  <rect x="1030" y="85" width="125" height="40" rx="6" fill="#4c1d95" stroke="#d8b4fe" stroke-width="1"/>
  <text x="1092" y="105" fill="#f5d0fe" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Compliance WORM</text>
  <text x="1092" y="118" fill="#e9d5ff" font-family="sans-serif" font-size="8" text-anchor="middle">S3 Object Lock</text>
  <line x1="1092" y1="125" x2="1092" y2="760" stroke="#4c1d95" stroke-width="1.2" stroke-dasharray="4,4"/>

  <!-- Sequence Steps -->

  <!-- Step 1: Ingress POST -->
  <line x1="92" y1="150" x2="210" y2="150" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#sqArBlue)"/>
  <text x="151" y="143" fill="#e0f2fe" font-family="sans-serif" font-size="8.5" text-anchor="middle">1. POST /v1/trans (Auth, PAN, $5,400)</text>

  <!-- Step 2: Gateway to Ingestion -->
  <line x1="212" y1="175" x2="330" y2="175" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#sqArBlue)"/>
  <text x="271" y="168" fill="#e0f2fe" font-family="sans-serif" font-size="8.5" text-anchor="middle">2. mTLS Validate &amp; Tokenize PAN</text>

  <!-- Step 3: Ingestion publishes trans.raw.v1 -->
  <line x1="332" y1="205" x2="455" y2="205" stroke="#fb923c" stroke-width="1.8" marker-end="url(#sqArBlue)"/>
  <text x="393" y="198" fill="#fed7aa" font-family="sans-serif" font-size="8.5" text-anchor="middle">3. Produce trans.received.v1 (Key: Acct)</text>

  <!-- Fast ACK to Payment Rail (Asynchronous Processing Path) -->
  <line x1="332" y1="230" x2="214" y2="230" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="3,3" marker-end="url(#sqArBlue)"/>
  <line x1="212" y1="235" x2="94" y2="235" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="3,3" marker-end="url(#sqArBlue)"/>
  <text x="210" y="224" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">HTTP 202 Accepted (Async Deep Scoring Path &lt; 4ms)</text>

  <!-- Step 4: Compliance captures raw event -->
  <path d="M 457 245 L 490 245 L 490 260 L 1090 260" fill="none" stroke="#d8b4fe" stroke-width="1.2" stroke-dasharray="2,2" marker-end="url(#sqArPurple)"/>
  <text x="770" y="254" fill="#e9d5ff" font-family="sans-serif" font-size="8" text-anchor="middle">4. WORM Audit Sink persists raw transaction to S3 Object Lock (Immutable 7-Yr Record)</text>

  <!-- Step 5: Feature Aggregator consumes raw -->
  <line x1="457" y1="285" x2="585" y2="285" stroke="#fb923c" stroke-width="1.5" marker-end="url(#sqArGreen)"/>
  <text x="522" y="278" fill="#fed7aa" font-family="sans-serif" font-size="8.5" text-anchor="middle">5. Consume trans.received.v1</text>

  <!-- Activation: Feature lookup in Redis -->
  <rect x="582" y="295" width="10" height="40" fill="#34d399" rx="2"/>
  <path d="M 592 305 C 625 305 625 325 594 325" fill="none" stroke="#34d399" stroke-width="1.2"/>
  <text x="635" y="318" fill="#a7f3d0" font-family="sans-serif" font-size="8">L2 Redis Lookup (Velocity, Geo-Diff &lt; 2ms)</text>

  <!-- Step 6: Produce trans.enriched.v1 -->
  <line x1="587" y1="350" x2="459" y2="350" stroke="#34d399" stroke-width="1.8" marker-end="url(#sqArGreen)"/>
  <text x="523" y="343" fill="#a7f3d0" font-family="sans-serif" font-size="8.5" text-anchor="middle">6. Produce trans.enriched.v1</text>

  <!-- Step 7: Fraud Scoring Engine consumes enriched -->
  <line x1="457" y1="380" x2="715" y2="380" stroke="#34d399" stroke-width="1.5" marker-end="url(#sqArRed)"/>
  <text x="587" y="373" fill="#a7f3d0" font-family="sans-serif" font-size="8.5" text-anchor="middle">7. Consume trans.enriched.v1 (Partition-Aligned)</text>

  <!-- Activation: Scoring Engine Inference -->
  <rect x="712" y="390" width="10" height="55" fill="#f87171" rx="2"/>
  <path d="M 722 400 C 765 400 765 435 724 435" fill="none" stroke="#f87171" stroke-width="1.2"/>
  <text x="775" y="410" fill="#fca5a5" font-family="sans-serif" font-size="8">Triton Inference Server (LightGBM + DNN)</text>
  <text x="775" y="423" fill="#fca5a5" font-family="sans-serif" font-size="8">Score: 0.94 (HIGH RISK) | SHAP Top: Foreign IP, $ Velocity</text>

  <!-- Step 8: Produce fraud.evaluated.v1 & fraud.alert.v1 -->
  <line x1="717" y1="460" x2="459" y2="460" stroke="#f87171" stroke-width="1.8" marker-end="url(#sqArRed)"/>
  <text x="588" y="453" fill="#fca5a5" font-family="sans-serif" font-size="8.5" text-anchor="middle">8. Produce fraud.evaluated.v1 &amp; fraud.alert.v1 (Score &gt;= 0.75)</text>

  <!-- Step 9: Downstream Action triggers automated card lock -->
  <path d="M 457 480 L 150 480 L 150 505 L 94 505" fill="none" stroke="#f87171" stroke-width="1.5" marker-end="url(#sqArRed)"/>
  <text x="270" y="497" fill="#fca5a5" font-family="sans-serif" font-size="8" text-anchor="middle">9. Automated Pre-Emptive Card Freeze &amp; SMS Challenge</text>

  <!-- Step 10: Case BFF consumes fraud.alert.v1 -->
  <line x1="457" y1="530" x2="840" y2="530" stroke="#ef4444" stroke-width="1.8" marker-end="url(#sqArPurple)"/>
  <text x="650" y="523" fill="#fca5a5" font-family="sans-serif" font-size="8.5" text-anchor="middle">10. Consume fraud.alert.v1 (Insert Case into PostgreSQL)</text>

  <!-- Step 11: BFF pushes alert to Analyst via WebSocket -->
  <line x1="842" y1="560" x2="960" y2="560" stroke="#38bdf8" stroke-width="2" marker-end="url(#sqArBlue)"/>
  <text x="901" y="552" fill="#38bdf8" font-family="sans-serif" font-size="8.5" font-weight="700" text-anchor="middle">11. WSS Push Alert (Frame: Latency &lt; 200ms)</text>

  <!-- Step 12: Analyst UI renders alert -->
  <rect x="957" y="570" width="10" height="60" fill="#0284c7" rx="2"/>
  <text x="975" y="585" fill="#e0f2fe" font-family="sans-serif" font-size="8">Analyst Console: Highlight High-Risk Alert</text>
  <text x="975" y="600" fill="#e0f2fe" font-family="sans-serif" font-size="8">SHAP Radar Chart + Geo-Discrepancy View</text>
  <text x="975" y="615" fill="#fca5a5" font-family="sans-serif" font-size="8" font-weight="700">Analyst Clicks: [CONFIRM FRAUD &amp; BLOCK]</text>

  <!-- Step 13: Analyst Action POST to BFF -->
  <line x1="962" y1="640" x2="844" y2="640" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#sqArBlue)"/>
  <text x="903" y="633" fill="#e0f2fe" font-family="sans-serif" font-size="8.5" text-anchor="middle">13. POST /v1/cases/1042/disposition (Confirmed)</text>

  <!-- Step 14: BFF updates Case DB & Emits case.updated.v1 -->
  <line x1="842" y1="670" x2="459" y2="670" stroke="#c084fc" stroke-width="1.8" marker-end="url(#sqArPurple)"/>
  <text x="650" y="663" fill="#e9d5ff" font-family="sans-serif" font-size="8.5" text-anchor="middle">14. Produce case.updated.v1 (Analyst Disposition Logged)</text>

  <!-- Step 15: Compliance archives complete case outcome -->
  <path d="M 457 690 L 490 690 L 490 710 L 1090 710" fill="none" stroke="#d8b4fe" stroke-width="1.5" marker-end="url(#sqArPurple)"/>
  <text x="770" y="703" fill="#e9d5ff" font-family="sans-serif" font-size="8" text-anchor="middle">15. Final Case Lifecycle Audit Manifest committed to WORM S3 (Full Audit Trail Complete)</text>

  <!-- Latency Box Summary across bottom -->
  <rect x="40" y="725" width="1120" height="40" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
  <text x="600" y="742" fill="#38bdf8" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">LATENCY BUDGET RECONCILIATION (P99 TARGET: &lt; 45ms Scoring | &lt; 200ms Analyst Push)</text>
  <text x="600" y="756" fill="#cbd5e1" font-family="sans-serif" font-size="8" text-anchor="middle">Ingress &amp; Tokenize: 4ms | Kafka Network Pub: 2ms | Flink Feature Window &amp; Redis: 6ms | Triton Ensemble ML: 12ms | Alert Pub &amp; WSS Push: 14ms | Total E2E: ~38ms</text>

</svg>'''

def get_diagram_4():
    """Diagram 4: Real-Time Analyst Frontend & BFF Streaming Architecture"""
    return '''<svg viewBox="0 0 1200 680" width="100%" height="680" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
    <filter id="shadow4" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000000" flood-opacity="0.35"/>
    </filter>
    <marker id="feArBlue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#38bdf8"/>
    </marker>
    <marker id="feArPurple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#c084fc"/>
    </marker>
    <marker id="feArGreen" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#34d399"/>
    </marker>
  </defs>

  <rect width="1200" height="680" fill="url(#bgGrad4)" rx="12" />
  <rect x="15" y="15" width="1170" height="650" fill="none" stroke="#334155" stroke-width="1.5" rx="10" />

  <!-- Title -->
  <text x="35" y="48" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700">Figure 4: Fraud Analyst Console &amp; Backend-for-Frontend (BFF) Architecture</text>
  <text x="35" y="70" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12">High-Frequency WebSocket Streaming, Virtualized DOM Recycling, Optimistic UI State &amp; Explainable AI (SHAP)</text>

  <!-- SECTION 1: Client Browser Application (Left Half) -->
  <rect x="35" y="95" width="530" height="550" rx="8" fill="#111827" stroke="#0ea5e9" stroke-width="1.5" filter="url(#shadow4)"/>
  <rect x="35" y="95" width="530" height="32" rx="8" fill="#0284c7"/>
  <text x="300" y="116" fill="#ffffff" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Analyst Single Page Application (React 19 / Next.js 15)</text>

  <!-- UI Sub-blocks -->
  <!-- 1. Real-time WebSocket Client -->
  <rect x="50" y="145" width="230" height="110" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
  <text x="165" y="167" fill="#38bdf8" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">WebSocket / SSE Client</text>
  <text x="60" y="187" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; STOMP over WSS Protocol</text>
  <text x="60" y="202" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Heartbeat &amp; Exponential Reconnect</text>
  <text x="60" y="217" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Priority Alert Multiplexing</text>
  <text x="60" y="232" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Backpressure Throttle Buffer</text>

  <!-- 2. TanStack Query & Zustand State -->
  <rect x="300" y="145" width="245" height="110" rx="6" fill="#1e293b" stroke="#34d399" stroke-width="1"/>
  <text x="422" y="167" fill="#34d399" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">State Management &amp; Cache</text>
  <text x="310" y="187" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; TanStack Query v5 (Server State)</text>
  <text x="310" y="202" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Optimistic UI Updates on Action</text>
  <text x="310" y="217" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Zustand Store (Active Filter / Selection)</text>
  <text x="310" y="232" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; IndexedDB Persistence for Offline Drafts</text>

  <!-- 3. Virtualized Alert Grid -->
  <rect x="50" y="275" width="495" height="140" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
  <text x="297" y="297" fill="#fb923c" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">DOM-Virtualized Alert Grid (TanStack Virtual)</text>
  <rect x="65" y="310" width="465" height="24" rx="4" fill="#334155"/>
  <text x="75" y="326" fill="#f8fafc" font-family="monospace" font-size="8.5">ALERT ID | TIMESTAMP | ACCOUNT | RISK | AMOUNT | STATUS | ACTION</text>
  <rect x="65" y="338" width="465" height="20" rx="3" fill="#450a0a"/>
  <text x="75" y="352" fill="#fca5a5" font-family="monospace" font-size="8">#ALT-9041 | 12:44:01.02 | AC-89104 | 0.94 | $5,400 | CRITICAL | [DISPATCH]</text>
  <rect x="65" y="362" width="465" height="20" rx="3" fill="#1e293b"/>
  <text x="75" y="376" fill="#fed7aa" font-family="monospace" font-size="8">#ALT-9040 | 12:43:58.89 | AC-11209 | 0.82 | $1,250 | HIGH     | [REVIEW]</text>
  <text x="297" y="402" fill="#94a3b8" font-family="sans-serif" font-size="8.5" text-anchor="middle">Recycles 20 visible DOM elements from an in-memory queue of 15,000+ alerts (60 FPS scrolling)</text>

  <!-- 4. Web Worker for Background Compute -->
  <rect x="50" y="435" width="230" height="95" rx="6" fill="#1e293b" stroke="#c084fc" stroke-width="1"/>
  <text x="165" y="455" fill="#c084fc" font-family="sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">Dedicated Web Worker</text>
  <text x="60" y="475" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Client-side Fuzzy Search &amp; Filter</text>
  <text x="60" y="490" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Risk Score Histogram Bucketing</text>
  <text x="60" y="505" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Zero Main-Thread Jank / Freeze</text>

  <!-- 5. Explainable AI & Action Bar -->
  <rect x="300" y="435" width="245" height="95" rx="6" fill="#1e293b" stroke="#f87171" stroke-width="1"/>
  <text x="422" y="455" fill="#f87171" font-family="sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">Explainability (SHAP) View</text>
  <text x="310" y="475" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; SHAP Waterfall / Feature Radar</text>
  <text x="310" y="490" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; IP Geolocation vs Previous 24h</text>
  <text x="310" y="505" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; 1-Click Triage: [Freeze] [Whitelist]</text>

  <!-- Client-side connectivity status -->
  <rect x="50" y="550" width="495" height="35" rx="4" fill="#064e3b" stroke="#34d399" stroke-width="1"/>
  <text x="297" y="572" fill="#a7f3d0" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">&#10003; WSS Connected: bff.internal.bank.com | Latency: 18ms | Active Channel: fraud-alerts-p1</text>

  <!-- SECTION 2: Backend-for-Frontend (BFF) Gateway (Right Half) -->
  <rect x="620" y="95" width="545" height="550" rx="8" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5" filter="url(#shadow4)"/>
  <rect x="620" y="95" width="545" height="32" rx="8" fill="#4338ca"/>
  <text x="892" y="116" fill="#e0e7ff" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Analyst BFF Gateway Tier (Node.js 22 / Fastify Cluster)</text>

  <!-- BFF Sub-blocks -->
  <!-- 1. WebSocket Gateway Hub -->
  <rect x="640" y="145" width="240" height="110" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
  <text x="760" y="167" fill="#38bdf8" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">WebSocket Connection Hub</text>
  <text x="650" y="187" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Manages 500+ Concurrent Analysts</text>
  <text x="650" y="202" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; STOMP Topic Subscriptions</text>
  <text x="650" y="217" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Client Ping/Pong Heartbeats (10s)</text>
  <text x="650" y="232" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Role-Based Topic Access Filter</text>

  <!-- 2. Redis Pub/Sub Fanout -->
  <rect x="905" y="145" width="240" height="110" rx="6" fill="#450a0a" stroke="#ef4444" stroke-width="1"/>
  <text x="1025" y="167" fill="#fca5a5" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Redis Pub/Sub Fanout Hub</text>
  <text x="915" y="187" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Synchronizes Horizontal BFF Pods</text>
  <text x="915" y="202" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Broadcasts Alerts across all Nodes</text>
  <text x="915" y="217" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Analyst Presence &amp; Active Locks</text>
  <text x="915" y="232" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Sub-millisecond Relay Latency</text>

  <!-- 3. Data Aggregator & ViewModel Transformer -->
  <rect x="640" y="275" width="505" height="110" rx="6" fill="#1e293b" stroke="#34d399" stroke-width="1.2"/>
  <text x="892" y="297" fill="#34d399" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Data Aggregation &amp; ViewModel Transformer</text>
  <text x="655" y="320" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Merges Kafka Alert Event + PostgreSQL Case History + Customer CRM Dossier + Device Fingerprint</text>
  <text x="655" y="337" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Eliminates Over-fetching: Serves tailored GraphQL / REST payloads strictly required by the UI view</text>
  <text x="655" y="354" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Response Compression (Brotli / Gzip) &amp; ETag HTTP Caching for static reference datasets</text>
  <text x="655" y="371" fill="#34d399" font-family="monospace" font-size="8">Saves 70% Bandwidth vs Raw Microservice Entity Exposure</text>

  <!-- 4. Case Management Store & Kafka Link -->
  <rect x="640" y="405" width="240" height="120" rx="6" fill="#1e293b" stroke="#c084fc" stroke-width="1"/>
  <text x="760" y="425" fill="#c084fc" font-family="sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">Kafka Alert Consumer</text>
  <text x="650" y="445" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Consumes: fraud.alert.v1</text>
  <text x="650" y="460" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Deserializes Avro Payload</text>
  <text x="650" y="475" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Publishes: case.updated.v1</text>
  <text x="650" y="490" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Enforces Strict Idempotency</text>
  <text x="650" y="505" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Emits Audit Metric Telemetry</text>

  <!-- 5. PostgreSQL Case Database -->
  <rect x="905" y="405" width="240" height="120" rx="6" fill="#1e293b" stroke="#818cf8" stroke-width="1"/>
  <text x="1025" y="425" fill="#c7d2fe" font-family="sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">PostgreSQL Case Store</text>
  <text x="915" y="445" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Case Entity &amp; State Machine</text>
  <text x="915" y="460" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Analyst Notes &amp; Disposition Log</text>
  <text x="915" y="475" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Multi-AZ Aurora Read Replicas</text>
  <text x="915" y="490" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Partitioned by created_month</text>
  <text x="915" y="505" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Connection Pooling (PgBouncer)</text>

  <!-- Security & RBAC Footer -->
  <rect x="640" y="550" width="505" height="35" rx="4" fill="#312e81" stroke="#818cf8" stroke-width="1"/>
  <text x="892" y="572" fill="#e0e7ff" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">Zero-Trust RBAC: OIDC OAuth2 Token Validation | Analyst Session Audit Logged to SIEM</text>

  <!-- Bidirectional Connection Between Client and BFF -->
  <line x1="565" y1="200" x2="635" y2="200" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="4,4" marker-end="url(#feArBlue)"/>
  <line x1="635" y1="215" x2="565" y2="215" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="4,4" marker-end="url(#feArBlue)"/>
  <text x="600" y="190" fill="#38bdf8" font-family="sans-serif" font-size="8" text-anchor="middle">WSS / SSE</text>
  <text x="600" y="235" fill="#34d399" font-family="sans-serif" font-size="8" text-anchor="middle">REST / GraphQL</text>

</svg>'''

def get_diagram_5():
    """Diagram 5: Enterprise Observability & Telemetry Correlation Architecture"""
    return '''<svg viewBox="0 0 1200 680" width="100%" height="680" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
    <filter id="shadow5" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000000" flood-opacity="0.35"/>
    </filter>
    <marker id="obArBlue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#38bdf8"/>
    </marker>
    <marker id="obArGreen" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#34d399"/>
    </marker>
    <marker id="obArOrange" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#fb923c"/>
    </marker>
    <marker id="obArPurple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#c084fc"/>
    </marker>
  </defs>

  <rect width="1200" height="680" fill="url(#bgGrad5)" rx="12" />
  <rect x="15" y="15" width="1170" height="650" fill="none" stroke="#334155" stroke-width="1.5" rx="10" />

  <!-- Title -->
  <text x="35" y="48" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700">Figure 5: Enterprise Observability &amp; Telemetry Correlation Architecture</text>
  <text x="35" y="70" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12">Unified OpenTelemetry Pipeline, Cross-Pillar Correlation (Metrics -&gt; Exemplars -&gt; Traces -&gt; Logs) &amp; SLO Monitoring</text>

  <!-- LAYER 1: Microservice Telemetry Sources (Top) -->
  <rect x="35" y="95" width="1130" height="120" rx="8" fill="#1e293b" stroke="#475569" stroke-width="1.2" filter="url(#shadow5)"/>
  <rect x="35" y="95" width="1130" height="26" rx="8" fill="#334155"/>
  <text x="600" y="113" fill="#f1f5f9" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Instrumented Microservice Fleet (OpenTelemetry SDK | W3C TraceContext Injected into HTTP / gRPC / Kafka Record Headers)</text>

  <!-- Service boxes across top -->
  <rect x="50" y="130" width="165" height="70" rx="5" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
  <text x="132" y="150" fill="#38bdf8" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Ingestion Gateway</text>
  <text x="132" y="167" fill="#cbd5e1" font-family="monospace" font-size="8" text-anchor="middle">OTel Go SDK</text>
  <text x="132" y="182" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Injects: traceparent</text>

  <rect x="235" y="130" width="165" height="70" rx="5" fill="#0f172a" stroke="#34d399" stroke-width="1"/>
  <text x="317" y="150" fill="#34d399" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Feature Aggregator</text>
  <text x="317" y="167" fill="#cbd5e1" font-family="monospace" font-size="8" text-anchor="middle">OTel Java/Flink</text>
  <text x="317" y="182" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Propagates Kafka Spans</text>

  <rect x="420" y="130" width="165" height="70" rx="5" fill="#0f172a" stroke="#f87171" stroke-width="1"/>
  <text x="502" y="150" fill="#f87171" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Scoring Engine</text>
  <text x="502" y="167" fill="#cbd5e1" font-family="monospace" font-size="8" text-anchor="middle">OTel C++ / Python</text>
  <text x="502" y="182" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Triton Inference Spans</text>

  <rect x="605" y="130" width="165" height="70" rx="5" fill="#0f172a" stroke="#c084fc" stroke-width="1"/>
  <text x="687" y="150" fill="#c084fc" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Case BFF Gateway</text>
  <text x="687" y="167" fill="#cbd5e1" font-family="monospace" font-size="8" text-anchor="middle">OTel Node.js SDK</text>
  <text x="687" y="182" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">WSS &amp; REST Traces</text>

  <rect x="790" y="130" width="165" height="70" rx="5" fill="#0f172a" stroke="#e879f9" stroke-width="1"/>
  <text x="872" y="150" fill="#e879f9" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Compliance &amp; Replay</text>
  <text x="872" y="167" fill="#cbd5e1" font-family="monospace" font-size="8" text-anchor="middle">OTel Go / Spark</text>
  <text x="872" y="182" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Iceberg Sink Audit Spans</text>

  <rect x="975" y="130" width="175" height="70" rx="5" fill="#0f172a" stroke="#fb923c" stroke-width="1"/>
  <text x="1062" y="150" fill="#fb923c" font-family="sans-serif" font-size="10" font-weight="700" text-anchor="middle">Kafka &amp; Infra Mesh</text>
  <text x="1062" y="167" fill="#cbd5e1" font-family="monospace" font-size="8" text-anchor="middle">JMX / Istio Envoy</text>
  <text x="1062" y="182" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Broker Metrics &amp; Lag</text>

  <!-- LAYER 2: OpenTelemetry Collector Pipeline (Center Top) -->
  <rect x="35" y="240" width="1130" height="95" rx="8" fill="#0c1e33" stroke="#0284c7" stroke-width="1.5" filter="url(#shadow5)"/>
  <text x="600" y="260" fill="#38bdf8" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">OpenTelemetry Collector Pipeline (DaemonSet on Kubernetes Nodes + Regional Collector Gateways)</text>

  <!-- Connectors from Services down to Collector -->
  <line x1="132" y1="200" x2="132" y2="238" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#obArBlue)"/>
  <line x1="317" y1="200" x2="317" y2="238" stroke="#34d399" stroke-width="1.5" marker-end="url(#obArGreen)"/>
  <line x1="502" y1="200" x2="502" y2="238" stroke="#f87171" stroke-width="1.5" marker-end="url(#obArOrange)"/>
  <line x1="687" y1="200" x2="687" y2="238" stroke="#c084fc" stroke-width="1.5" marker-end="url(#obArPurple)"/>
  <line x1="872" y1="200" x2="872" y2="238" stroke="#e879f9" stroke-width="1.5" marker-end="url(#obArPurple)"/>
  <line x1="1062" y1="200" x2="1062" y2="238" stroke="#fb923c" stroke-width="1.5" marker-end="url(#obArOrange)"/>

  <!-- Collector Internals -->
  <rect x="50" y="275" width="240" height="45" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
  <text x="170" y="295" fill="#38bdf8" font-family="sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">Receivers: OTLP gRPC / HTTP</text>
  <text x="170" y="310" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Port 4317 / 4318, Zipkin, Prometheus</text>

  <rect x="310" y="275" width="480" height="45" rx="4" fill="#1e293b" stroke="#34d399" stroke-width="1"/>
  <text x="550" y="295" fill="#34d399" font-family="sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">Processors: Memory Limiter | Batching | PII Scrubbing (PAN / SSN Masking)</text>
  <text x="550" y="310" fill="#cbd5e1" font-family="sans-serif" font-size="8" text-anchor="middle">Attribute Injection: env=prod, region=us-east-1, tenant_id=bank_core, k8s_pod</text>

  <rect x="810" y="275" width="340" height="45" rx="4" fill="#1e293b" stroke="#fb923c" stroke-width="1"/>
  <text x="980" y="295" fill="#fb923c" font-family="sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">Exporters: Fanout to 3 Pillars</text>
  <text x="980" y="310" fill="#94a3b8" font-family="sans-serif" font-size="8" text-anchor="middle">Prometheus Remote Write | Tempo gRPC | Loki HTTP</text>

  <!-- LAYER 3: The Three Specialized Telemetry Backends (Center Bottom) -->
  <!-- Column 1: Metrics & SLOs (Prometheus) -->
  <rect x="35" y="360" width="355" height="155" rx="8" fill="#1e293b" stroke="#34d399" stroke-width="1.5" filter="url(#shadow5)"/>
  <rect x="35" y="360" width="355" height="26" rx="8" fill="#065f46"/>
  <text x="212" y="378" fill="#d1fae5" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">PILLAR 1: Metrics TSDB (Prometheus / VictoriaMetrics)</text>
  <text x="45" y="405" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Golden Signals: Latency, Traffic (1,000 TPS), Errors, Saturation</text>
  <text x="45" y="422" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Kafka Consumer Lag &amp; Broker Disk IOPS</text>
  <text x="45" y="439" fill="#34d399" font-family="sans-serif" font-size="8.5" font-weight="700">&#8226; SLO 1: P99 End-to-End Latency &lt; 45ms (Rolling 5m)</text>
  <text x="45" y="456" fill="#34d399" font-family="sans-serif" font-size="8.5" font-weight="700">&#8226; SLO 2: Pipeline Error Rate &lt; 0.01% (99.99% Success)</text>
  <rect x="45" y="468" width="335" height="36" rx="4" fill="#0f172a" stroke="#059669" stroke-width="1"/>
  <text x="212" y="482" fill="#a7f3d0" font-family="sans-serif" font-size="8.5" font-weight="700" text-anchor="middle">Exemplar Support: Attaches Trace ID directly</text>
  <text x="212" y="496" fill="#a7f3d0" font-family="sans-serif" font-size="8" text-anchor="middle">to Histogram latency bucket data points</text>

  <!-- Column 2: Distributed Tracing (Grafana Tempo) -->
  <rect x="410" y="360" width="370" height="155" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5" filter="url(#shadow5)"/>
  <rect x="410" y="360" width="370" height="26" rx="8" fill="#075985"/>
  <text x="595" y="378" fill="#e0f2fe" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">PILLAR 2: Distributed Traces (Grafana Tempo / S3)</text>
  <text x="420" y="405" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; End-to-End Trace Waterfall from Ingestion -&gt; Model -&gt; Alert</text>
  <text x="420" y="422" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Captures Asynchronous Kafka Span Parent-Child Links</text>
  <text x="420" y="439" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Cost-Effective Object Storage (S3) Backing (100% Sampling)</text>
  <text x="420" y="456" fill="#38bdf8" font-family="sans-serif" font-size="8.5" font-weight="700">&#8226; Sub-second Trace Lookup by trace_id or transaction_id</text>
  <rect x="420" y="468" width="350" height="36" rx="4" fill="#0f172a" stroke="#0284c7" stroke-width="1"/>
  <text x="595" y="482" fill="#bae6fd" font-family="sans-serif" font-size="8.5" font-weight="700" text-anchor="middle">W3C TraceContext: traceparent &amp; tracestate</text>
  <text x="595" y="496" fill="#bae6fd" font-family="sans-serif" font-size="8" text-anchor="middle">Embedded in Kafka Record Headers for Zero Context Loss</text>

  <!-- Column 3: Centralized Logs (Grafana Loki) -->
  <rect x="800" y="360" width="365" height="155" rx="8" fill="#1e293b" stroke="#fb923c" stroke-width="1.5" filter="url(#shadow5)"/>
  <rect x="800" y="360" width="365" height="26" rx="8" fill="#9a3412"/>
  <text x="982" y="378" fill="#ffedd5" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">PILLAR 3: Centralized Logs (Grafana Loki)</text>
  <text x="810" y="405" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Structured JSON logs with auto-injected metadata</text>
  <text x="810" y="422" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Indexed by Labels: app, env, pod, level, error_code</text>
  <text x="810" y="439" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; PII-Cleaned: Card numbers truncated to last 4 digits</text>
  <text x="810" y="456" fill="#fb923c" font-family="sans-serif" font-size="8.5" font-weight="700">&#8226; High-throughput Ingestion (FluentBit DaemonSet)</text>
  <rect x="810" y="468" width="345" height="36" rx="4" fill="#0f172a" stroke="#ea580c" stroke-width="1"/>
  <text x="982" y="482" fill="#fed7aa" font-family="sans-serif" font-size="8.5" font-weight="700" text-anchor="middle">Auto-Correlation: trace_id &amp; span_id</text>
  <text x="982" y="496" fill="#fed7aa" font-family="sans-serif" font-size="8" text-anchor="middle">Allows instant log filtering matching exact active trace span</text>

  <!-- Connectors from Collector to 3 Pillars -->
  <line x1="212" y1="335" x2="212" y2="358" stroke="#34d399" stroke-width="2" marker-end="url(#obArGreen)"/>
  <line x1="595" y1="335" x2="595" y2="358" stroke="#38bdf8" stroke-width="2" marker-end="url(#obArBlue)"/>
  <line x1="982" y1="335" x2="982" y2="358" stroke="#fb923c" stroke-width="2" marker-end="url(#obArOrange)"/>

  <!-- LAYER 4: Unified Grafana Dashboard & Cross-Pillar Correlation Flow (Bottom) -->
  <rect x="35" y="535" width="1130" height="120" rx="8" fill="#18182f" stroke="#c084fc" stroke-width="1.5" filter="url(#shadow5)"/>
  <rect x="35" y="535" width="1130" height="26" rx="8" fill="#581c87"/>
  <text x="600" y="553" fill="#f3e8ff" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Unified Observability Operations Console (Grafana Enterprise + Incident Correlation Workflow)</text>

  <!-- Step 1: Metric Spike -->
  <rect x="50" y="570" width="220" height="70" rx="6" fill="#1e293b" stroke="#34d399" stroke-width="1.2"/>
  <text x="160" y="590" fill="#34d399" font-family="sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">Step 1: Metric Spike Alert</text>
  <text x="60" y="608" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; P99 Latency reaches 52ms</text>
  <text x="60" y="622" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; Alertmanager fires P1 alert</text>

  <!-- Arrow Step 1 -> 2 -->
  <line x1="270" y1="605" x2="310" y2="605" stroke="#c084fc" stroke-width="2" marker-end="url(#obArPurple)"/>

  <!-- Step 2: Exemplar Click -->
  <rect x="320" y="570" width="240" height="70" rx="6" fill="#1e293b" stroke="#c084fc" stroke-width="1.2"/>
  <text x="440" y="590" fill="#c084fc" font-family="sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">Step 2: Exemplar Drilldown</text>
  <text x="330" y="608" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; Operator clicks outlier point on graph</text>
  <text x="330" y="622" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; Extracts exact trace_id: a81f4c...</text>

  <!-- Arrow Step 2 -> 3 -->
  <line x1="560" y1="605" x2="600" y2="605" stroke="#c084fc" stroke-width="2" marker-end="url(#obArPurple)"/>

  <!-- Step 3: Tempo Trace Waterfall -->
  <rect x="610" y="570" width="250" height="70" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
  <text x="735" y="590" fill="#38bdf8" font-family="sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">Step 3: Tempo Trace Waterfall</text>
  <text x="620" y="608" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; Visualizes span timing across all hops</text>
  <text x="620" y="622" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; Identifies 34ms hang in Triton inference</text>

  <!-- Arrow Step 3 -> 4 -->
  <line x1="860" y1="605" x2="900" y2="605" stroke="#c084fc" stroke-width="2" marker-end="url(#obArPurple)"/>

  <!-- Step 4: Contextual Logs & Remediation -->
  <rect x="910" y="570" width="240" height="70" rx="6" fill="#1e293b" stroke="#fb923c" stroke-width="1.2"/>
  <text x="1030" y="590" fill="#fb923c" font-family="sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">Step 4: Filtered Loki Logs</text>
  <text x="920" y="608" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; 1-Click: "Logs for this Span"</text>
  <text x="920" y="622" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; Root Cause: GPU CUDA worker lock</text>

</svg>'''

def get_diagram_6():
    """Diagram 6: Compliance Audit, Immutable Storage & Replay Subsystem"""
    return '''<svg viewBox="0 0 1200 680" width="100%" height="680" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad6" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
    <filter id="shadow6" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000000" flood-opacity="0.35"/>
    </filter>
    <marker id="cpArPurple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#c084fc"/>
    </marker>
    <marker id="cpArBlue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#38bdf8"/>
    </marker>
    <marker id="cpArGreen" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#34d399"/>
    </marker>
  </defs>

  <rect width="1200" height="680" fill="url(#bgGrad6)" rx="12" />
  <rect x="15" y="15" width="1170" height="650" fill="none" stroke="#334155" stroke-width="1.5" rx="10" />

  <!-- Title -->
  <text x="35" y="48" fill="#f8fafc" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="700">Figure 6: Compliance Audit, Immutable Storage &amp; Historical Replay Subsystem</text>
  <text x="35" y="70" fill="#94a3b8" font-family="'Segoe UI', Roboto, sans-serif" font-size="12">WORM S3 Storage (7-Yr Retention), Apache Iceberg Partitioning, Isolated Replay Pipeline &amp; Shadow Scoring</text>

  <!-- SECTION 1: Continuous Audit Ingestion & Compaction (Left Half) -->
  <rect x="35" y="95" width="530" height="550" rx="8" fill="#1e1b4b" stroke="#a855f7" stroke-width="1.5" filter="url(#shadow6)"/>
  <rect x="35" y="95" width="530" height="32" rx="8" fill="#6b21a8"/>
  <text x="300" y="116" fill="#faf5ff" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Continuous Ingestion &amp; Immutable Archival Pipeline</text>

  <!-- Live Topics Feed -->
  <rect x="50" y="145" width="500" height="75" rx="6" fill="#0f172a" stroke="#fb923c" stroke-width="1.2"/>
  <text x="300" y="167" fill="#fb923c" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Live Production Kafka Topics</text>
  <text x="60" y="187" fill="#cbd5e1" font-family="monospace" font-size="8.5">&#8226; trans.received.v1  &#8226; trans.enriched.v1  &#8226; fraud.evaluated.v1  &#8226; case.updated.v1</text>
  <text x="60" y="205" fill="#94a3b8" font-family="sans-serif" font-size="8.5">High-throughput ingestion stream: 1,000 TPS | Peak: 86.4M events/day</text>

  <!-- Kafka Connect / Stream Compactor -->
  <rect x="50" y="245" width="500" height="95" rx="6" fill="#1e293b" stroke="#c084fc" stroke-width="1.2"/>
  <text x="300" y="267" fill="#c084fc" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Audit Archiver &amp; Compaction Engine (KEDA Autoscaled)</text>
  <text x="65" y="288" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Buffers incoming event streams into 60-second micro-batches</text>
  <text x="65" y="303" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Serializes into Apache Parquet with Zstandard (ZSTD) compression (6:1 ratio)</text>
  <text x="65" y="318" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Generates cryptographic SHA-256 batch manifest &amp; digital signature</text>
  <text x="65" y="333" fill="#34d399" font-family="monospace" font-size="8">SLO: Persisted to WORM storage in &lt; 15 seconds from generation</text>

  <!-- Connect Archiver down to Storage -->
  <line x1="300" y1="220" x2="300" y2="243" stroke="#c084fc" stroke-width="2" marker-end="url(#cpArPurple)"/>

  <!-- Immutable Storage (S3 Object Lock) -->
  <rect x="50" y="365" width="500" height="150" rx="6" fill="#2e1065" stroke="#d8b4fe" stroke-width="1.5"/>
  <text x="300" y="388" fill="#f5d0fe" font-family="sans-serif" font-size="11.5" font-weight="700" text-anchor="middle">WORM Compliance Storage (AWS S3 Glacier Instant Retrieval / GCS)</text>
  <text x="300" y="405" fill="#e879f9" font-family="sans-serif" font-size="9" text-anchor="middle">Object Lock in Compliance Mode (Cannot be deleted or overwritten by ANY IAM user for 7 Years)</text>
  <line x1="65" y1="413" x2="535" y2="413" stroke="#701a75" stroke-width="1"/>
  <text x="65" y="430" fill="#fdf4ff" font-family="monospace" font-size="8.5">Partition Scheme: s3://bank-audit-lakehouse/iceberg/</text>
  <text x="85" y="445" fill="#fdf4ff" font-family="monospace" font-size="8">&#8226; table=transactions/year=YYYY/month=MM/day=DD/hour=HH/*.parquet</text>
  <text x="85" y="460" fill="#fdf4ff" font-family="monospace" font-size="8">&#8226; table=evaluations/year=YYYY/month=MM/day=DD/hour=HH/*.parquet</text>
  <text x="85" y="475" fill="#fdf4ff" font-family="monospace" font-size="8">&#8226; table=case_audit/year=YYYY/month=MM/day=DD/hour=HH/*.parquet</text>
  <text x="65" y="495" fill="#a7f3d0" font-family="sans-serif" font-size="8.5">&#8226; BCBS 239 &amp; SEC Rule 17a-4 compliant write-once-read-many guarantees</text>

  <!-- Connect Compactor to S3 -->
  <line x1="300" y1="340" x2="300" y2="363" stroke="#d8b4fe" stroke-width="2" marker-end="url(#cpArPurple)"/>

  <!-- Hourly Checksum Verification -->
  <rect x="50" y="535" width="500" height="50" rx="4" fill="#0f172a" stroke="#34d399" stroke-width="1"/>
  <text x="300" y="555" fill="#34d399" font-family="sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">Automated Reconciliation &amp; Parity Engine</text>
  <text x="300" y="572" fill="#cbd5e1" font-family="sans-serif" font-size="8" text-anchor="middle">Verifies (Kafka Ingested Total - S3 Archived Total == 0) every 60 mins. Raises P1 alert on mismatch.</text>

  <!-- SECTION 2: Deterministic Historical Replay Subsystem (Right Half) -->
  <rect x="620" y="95" width="545" height="550" rx="8" fill="#0c1e33" stroke="#0284c7" stroke-width="1.5" filter="url(#shadow6)"/>
  <rect x="620" y="95" width="545" height="32" rx="8" fill="#075985"/>
  <text x="892" y="116" fill="#e0f2fe" font-family="sans-serif" font-size="12" font-weight="700" text-anchor="middle">Deterministic Historical Replay &amp; Shadow Validation Subsystem</text>

  <!-- Replay Request Trigger -->
  <rect x="640" y="145" width="505" height="75" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
  <text x="892" y="167" fill="#38bdf8" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Replay Coordinator &amp; Compliance API</text>
  <text x="655" y="187" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Admin API for Compliance Officers, Internal Auditors &amp; ML Engineers</text>
  <text x="655" y="203" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Trigger Input: Date Range [T1, T2], Tenant ID, Target Model Version, Replay Speed (1x to 100x)</text>

  <!-- S3 to Replay Coordinator Connector -->
  <path d="M 550 440 L 590 440 L 590 182 L 638 182" fill="none" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="3,3" marker-end="url(#cpArBlue)"/>
  <text x="590" y="290" fill="#38bdf8" font-family="sans-serif" font-size="8" text-anchor="middle" transform="rotate(-90 590 290)">Read Historical Parquet</text>

  <!-- Replay Worker Fleet -->
  <rect x="640" y="245" width="505" height="95" rx="6" fill="#1e293b" stroke="#34d399" stroke-width="1.2"/>
  <text x="892" y="267" fill="#34d399" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Replay Worker Fleet (KEDA Scaled on Demand)</text>
  <text x="655" y="288" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Fetches columnar partition slices from Iceberg lakehouse using Apache Arrow</text>
  <text x="655" y="303" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Injects original event packets into ISOLATED Kafka topic: trans.replay.v1</text>
  <text x="655" y="318" fill="#cbd5e1" font-family="sans-serif" font-size="8.5">&#8226; Preserves original event timestamps in headers (`x-original-timestamp`)</text>
  <text x="655" y="333" fill="#34d399" font-family="monospace" font-size="8">Zero Impact on Live Production Traffic or Analyst Queues</text>

  <line x1="892" y1="220" x2="892" y2="243" stroke="#34d399" stroke-width="2" marker-end="url(#cpArGreen)"/>

  <!-- Shadow Scoring Pipeline -->
  <rect x="640" y="365" width="505" height="150" rx="6" fill="#1e293b" stroke="#f87171" stroke-width="1.2"/>
  <text x="892" y="388" fill="#f87171" font-family="sans-serif" font-size="11" font-weight="700" text-anchor="middle">Shadow Scoring Engine &amp; Candidate Model Sandbox</text>
  <rect x="655" y="402" width="230" height="65" rx="4" fill="#0f172a" stroke="#ef4444" stroke-width="1"/>
  <text x="770" y="420" fill="#fca5a5" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">Isolated Topic: trans.replay.v1</text>
  <text x="665" y="436" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; Partitioned by account_id</text>
  <text x="665" y="450" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; Dedicated replay consumer group</text>

  <rect x="900" y="402" width="230" height="65" rx="4" fill="#0f172a" stroke="#f87171" stroke-width="1"/>
  <text x="1015" y="420" fill="#f87171" font-family="sans-serif" font-size="9" font-weight="700" text-anchor="middle">Candidate ML Model (v2.4)</text>
  <text x="910" y="436" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; Scores replayed transactions</text>
  <text x="910" y="450" fill="#cbd5e1" font-family="sans-serif" font-size="8">&#8226; Computes shadow precision/recall</text>

  <text x="892" y="490" fill="#cbd5e1" font-family="sans-serif" font-size="8.5" text-anchor="middle">Enables risk backtesting against real historical fraud spikes (Black Friday, Tax Year End)</text>
  <text x="892" y="505" fill="#fca5a5" font-family="monospace" font-size="8" text-anchor="middle">No alerts sent to Core Banking or Live Analysts during Replay</text>

  <line x1="892" y1="340" x2="892" y2="363" stroke="#f87171" stroke-width="2" marker-end="url(#cpArPurple)"/>

  <!-- Model Performance Comparison & Diff Report -->
  <rect x="640" y="535" width="505" height="50" rx="4" fill="#0f172a" stroke="#c084fc" stroke-width="1"/>
  <text x="892" y="555" fill="#c084fc" font-family="sans-serif" font-size="9.5" font-weight="700" text-anchor="middle">Model Governance &amp; Audit Diff Report Generator</text>
  <text x="892" y="572" fill="#cbd5e1" font-family="sans-serif" font-size="8" text-anchor="middle">Compares original production decisions with candidate decisions. Computes false positive reduction.</text>

</svg>'''

def main():
    print("Generating SVG diagrams...")
    diagrams = [
        ("diagram_1_solution_architecture.svg", get_diagram_1()),
        ("diagram_2_event_messaging_backbone.svg", get_diagram_2()),
        ("diagram_3_transaction_flow_sequence.svg", get_diagram_3()),
        ("diagram_4_analyst_frontend_bff.svg", get_diagram_4()),
        ("diagram_5_enterprise_observability.svg", get_diagram_5()),
        ("diagram_6_compliance_audit_replay.svg", get_diagram_6()),
    ]
    
    for filename, content in diagrams:
        filepath = os.path.join(DIAGRAMS_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Generated: {filepath} ({len(content)} bytes)")

if __name__ == "__main__":
    main()
