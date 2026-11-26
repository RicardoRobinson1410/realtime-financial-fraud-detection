"""
Master script to generate:
1. SOLUTION_ARCHITECTURE_REPORT.md (Complete Markdown Report)
2. build/report.html (Publication-Grade HTML with Embedded SVGs and Executive Styling)
3. Solution_Architecture_Report_Fraud_Detection.pdf (Final PDF Deliverable via Edge headless)
4. PDF Verification & Thumbnail Rendering (via pypdf and pypdfium2)
"""

import os
import subprocess
import time
import pypdf
import pypdfium2

from report_sections import (
    section_01_executive_summary,
    section_02_microservices,
    section_03_event_driven,
    section_04_frontend_bff,
    section_05_observability,
    section_06_resilience_scalability,
    section_07_patterns_evaluation,
    section_08_tech_stack,
    section_09_critical_tradeoffs,
    section_10_standout_strategies,
    section_11_diagrams_gallery,
    section_12_roadmap_conclusion
)

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(WORKSPACE_DIR, "build")
os.makedirs(BUILD_DIR, exist_ok=True)

MD_FILE_PATH = os.path.join(WORKSPACE_DIR, "SOLUTION_ARCHITECTURE_REPORT.md")
HTML_FILE_PATH = os.path.join(BUILD_DIR, "report.html")
PDF_FILE_PATH = os.path.join(WORKSPACE_DIR, "Solution_Architecture_Report_Fraud_Detection.pdf")

def assemble_markdown():
    print("Assembling Markdown report...")
    sections = [
        section_01_executive_summary.get_markdown(),
        section_02_microservices.get_markdown(),
        section_03_event_driven.get_markdown(),
        section_04_frontend_bff.get_markdown(),
        section_05_observability.get_markdown(),
        section_06_resilience_scalability.get_markdown(),
        section_07_patterns_evaluation.get_markdown(),
        section_08_tech_stack.get_markdown(),
        section_09_critical_tradeoffs.get_markdown(),
        section_10_standout_strategies.get_markdown(),
        section_11_diagrams_gallery.get_markdown(),
        section_12_roadmap_conclusion.get_markdown()
    ]
    full_md = "\n\n---\n\n".join(sections)
    with open(MD_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(full_md)
    print(f"Markdown report generated: {MD_FILE_PATH} ({len(full_md)} characters)")

def assemble_html():
    print("Assembling HTML report with embedded SVGs and executive styling...")
    
    html_sections = [
        section_01_executive_summary.get_html(),
        section_02_microservices.get_html(),
        section_03_event_driven.get_html(),
        section_04_frontend_bff.get_html(),
        section_05_observability.get_html(),
        section_06_resilience_scalability.get_html(),
        section_07_patterns_evaluation.get_html(),
        section_08_tech_stack.get_html(),
        section_09_critical_tradeoffs.get_html(),
        section_10_standout_strategies.get_html(),
        section_11_diagrams_gallery.get_html(),
        section_12_roadmap_conclusion.get_html()
    ]
    
    full_body = "\n".join(html_sections)
    
    css_styles = """
    :root {
      --primary: #1e3a8a;
      --primary-light: #3b82f6;
      --secondary: #0f172a;
      --accent-teal: #0d9488;
      --accent-red: #dc2626;
      --accent-purple: #7c3aed;
      --accent-amber: #d97706;
      --bg-light: #f8fafc;
      --border-color: #e2e8f0;
      --text-main: #1e293b;
      --text-muted: #64748b;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      color: var(--text-main);
      background-color: #ffffff;
      line-height: 1.6;
      font-size: 10pt;
      -webkit-font-smoothing: antialiased;
    }

    @page {
      size: letter;
      margin: 16mm 14mm 16mm 14mm;
      @bottom-right {
        content: "Page " counter(page);
        font-size: 8pt;
        color: #94a3b8;
      }
      @bottom-left {
        content: "CONFIDENTIAL — Real-Time Financial Fraud Detection Platform (SAR-FINFRAUD-2026)";
        font-size: 8pt;
        color: #94a3b8;
      }
    }

    .report-container {
      max-width: 900px;
      margin: 0 auto;
      padding: 10px 15px;
    }

    /* Cover Page */
    .cover-page {
      min-height: 88vh;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      page-break-after: always;
      border-bottom: 2px solid var(--primary);
      padding-bottom: 30px;
      margin-bottom: 25px;
    }

    .cover-badge-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 15px;
    }

    .cover-badge {
      display: inline-block;
      padding: 5px 12px;
      border-radius: 4px;
      font-size: 8pt;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }

    .badge-confidential {
      background-color: #fee2e2;
      color: #991b1b;
      border: 1px solid #f87171;
    }

    .badge-version {
      background-color: #e0f2fe;
      color: #0369a1;
      border: 1px solid #7dd3fc;
    }

    .cover-main {
      margin: 40px 0;
    }

    .cover-pretitle {
      font-size: 12pt;
      font-weight: 600;
      color: var(--accent-teal);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 10px;
    }

    .cover-title {
      font-size: 24pt;
      font-weight: 800;
      color: var(--secondary);
      line-height: 1.25;
      margin-bottom: 15px;
    }

    .cover-subtitle {
      font-size: 12pt;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 30px;
    }

    .metadata-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 15px;
      background: #f8fafc;
      border-radius: 6px;
      overflow: hidden;
      border: 1px solid #e2e8f0;
    }

    .metadata-table td {
      padding: 8px 14px;
      font-size: 9pt;
      border-bottom: 1px solid #e2e8f0;
    }

    .metadata-table tr:last-child td {
      border-bottom: none;
    }

    .metadata-table .meta-label {
      font-weight: 700;
      color: #475569;
      width: 28%;
    }

    .metadata-table .meta-val {
      color: #0f172a;
    }

    /* Table of Contents */
    .toc-section {
      page-break-after: always;
      margin-bottom: 25px;
      padding: 15px 0;
    }

    .toc-title {
      font-size: 15pt;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 16px;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 6px;
    }

    .toc-list {
      list-style: none;
    }

    .toc-item {
      display: flex;
      justify-content: space-between;
      padding: 8px 0;
      border-bottom: 1px dotted #cbd5e1;
      font-size: 9.5pt;
    }

    .toc-item a {
      color: var(--text-main);
      text-decoration: none;
      font-weight: 600;
    }

    .toc-item a:hover {
      color: var(--primary);
    }

    /* Headings & Sections */
    .report-section {
      margin-bottom: 30px;
      page-break-after: auto;
    }

    .section-header {
      display: flex;
      align-items: flex-start;
      margin-bottom: 14px;
      border-bottom: 2px solid var(--border-color);
      padding-bottom: 8px;
      page-break-after: avoid;
    }

    .section-number {
      font-size: 24pt;
      font-weight: 800;
      color: #cbd5e1;
      line-height: 1;
      margin-right: 12px;
    }

    .section-title-wrap h2 {
      font-size: 15pt;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 3px;
    }

    .section-subtitle {
      font-size: 9pt;
      color: var(--text-muted);
      font-style: italic;
    }

    h3 {
      font-size: 12pt;
      font-weight: 700;
      color: var(--secondary);
      margin: 18px 0 8px 0;
      page-break-after: avoid;
    }

    h4 {
      font-size: 10.5pt;
      font-weight: 700;
      color: #334155;
      margin: 14px 0 6px 0;
      page-break-after: avoid;
    }

    p {
      margin-bottom: 10px;
      text-align: justify;
    }

    .bullet-list {
      margin: 8px 0 14px 20px;
    }

    .bullet-list li {
      margin-bottom: 5px;
    }

    /* Callout Boxes */
    .callout {
      display: flex;
      padding: 12px 16px;
      border-radius: 6px;
      margin: 14px 0;
      border-left: 4px solid;
      background: #f8fafc;
      page-break-inside: avoid;
    }

    .callout-icon {
      font-size: 15pt;
      margin-right: 12px;
      line-height: 1.2;
    }

    .callout-body h4 {
      margin-top: 0;
      margin-bottom: 3px;
    }

    .callout-body p {
      margin-bottom: 0;
      font-size: 9pt;
    }

    .callout-danger {
      border-color: var(--accent-red);
      background-color: #fef2f2;
    }
    .callout-danger .callout-icon { color: var(--accent-red); }
    .callout-danger h4 { color: #991b1b; }

    .callout-info {
      border-color: var(--primary-light);
      background-color: #f0f9ff;
    }
    .callout-info .callout-icon { color: var(--primary-light); }
    .callout-info h4 { color: #075985; }

    .callout-success {
      border-color: var(--accent-teal);
      background-color: #f0fdfa;
    }
    .callout-success .callout-icon { color: var(--accent-teal); }
    .callout-success h4 { color: #115e59; }

    /* Tables */
    .table-container {
      margin: 14px 0;
      overflow-x: auto;
      page-break-inside: avoid;
    }

    .data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 8pt;
      border: 1px solid #cbd5e1;
    }

    .data-table th {
      background-color: #1e293b;
      color: #ffffff;
      text-align: left;
      padding: 7px 9px;
      font-weight: 700;
      font-size: 8pt;
      letter-spacing: 0.3px;
    }

    .data-table td {
      padding: 7px 9px;
      border-bottom: 1px solid #e2e8f0;
      vertical-align: top;
    }

    .data-table tr:nth-child(even) {
      background-color: #f8fafc;
    }

    /* Badges */
    .badge {
      display: inline-block;
      padding: 2px 6px;
      border-radius: 3px;
      font-size: 7pt;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }

    .badge-primary { background: #e0e7ff; color: #3730a3; }
    .badge-success { background: #d1fae5; color: #065f46; }
    .badge-warning { background: #fef3c7; color: #92400e; }
    .badge-danger { background: #fee2e2; color: #991b1b; }

    /* Card Grids */
    .card-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin: 14px 0;
      page-break-inside: avoid;
    }

    .info-card {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 10px 12px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .info-card .card-title {
      font-size: 9.5pt;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 5px;
    }

    .info-card p {
      font-size: 8pt;
      color: #334155;
      margin-bottom: 0;
    }

    /* Microservices Grid */
    .microservice-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin: 14px 0;
      page-break-inside: avoid;
    }

    .microservice-card {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 10px 12px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .ms-header {
      display: flex;
      align-items: center;
      margin-bottom: 6px;
    }

    .ms-code {
      display: inline-block;
      padding: 3px 6px;
      background: var(--primary);
      color: #ffffff;
      font-size: 7.5pt;
      font-weight: 800;
      border-radius: 4px;
      margin-right: 8px;
    }

    .ms-title-block h4 {
      margin: 0;
      font-size: 9.5pt;
      font-weight: 700;
    }

    .ms-tech {
      font-size: 7pt;
      color: var(--text-muted);
      font-family: monospace;
    }

    .ms-desc {
      font-size: 8pt;
      color: #334155;
      margin-bottom: 6px;
    }

    .ms-io-box {
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
      padding-top: 5px;
      font-size: 7.5pt;
      color: #475569;
    }

    .ms-io-box div {
      margin-bottom: 2px;
    }

    /* SLO Cards */
    .slo-card {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-left: 4px solid var(--accent-teal);
      border-radius: 6px;
      padding: 10px 14px;
      margin: 10px 0;
      page-break-inside: avoid;
    }

    .slo-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 5px;
    }

    .slo-title {
      font-size: 9.5pt;
      font-weight: 700;
      color: var(--primary);
    }

    .slo-target {
      font-size: 7.5pt;
      font-weight: 800;
      padding: 2px 7px;
      background: #d1fae5;
      color: #065f46;
      border-radius: 4px;
    }

    .slo-body p {
      font-size: 8.5pt;
      margin-bottom: 5px;
    }

    .code-block-header {
      font-size: 7pt;
      font-weight: 700;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-top: 3px;
    }

    pre {
      background: #0f172a;
      color: #f8fafc;
      padding: 6px 10px;
      border-radius: 4px;
      font-family: Consolas, "Liberation Mono", Menlo, Courier, monospace;
      font-size: 7.5pt;
      overflow-x: auto;
      margin-top: 3px;
    }

    code {
      font-family: Consolas, "Liberation Mono", Menlo, Courier, monospace;
      font-size: 8pt;
      background: #f1f5f9;
      color: #0f172a;
      padding: 1px 4px;
      border-radius: 3px;
    }

    pre code {
      background: transparent;
      color: inherit;
      padding: 0;
    }

    /* Diagram Styling */
    .diagram-wrapper {
      margin: 20px 0;
      page-break-inside: avoid;
    }

    .page-break-before {
      page-break-before: always;
    }

    .diagram-container {
      background: #0f172a;
      border-radius: 8px;
      padding: 10px;
      border: 1px solid #334155;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    .diagram-container svg {
      display: block;
      width: 100%;
      height: auto;
    }

    .diagram-caption {
      font-size: 8pt;
      color: #475569;
      margin-top: 6px;
      text-align: center;
      line-height: 1.4;
    }

    .diagram-caption strong {
      color: var(--primary);
    }
    """
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Solution Architecture Report: Real-Time Financial Fraud Detection Platform</title>
  <style>
    {css_styles}
  </style>
</head>
<body>
  <div class="report-container">
    
    <!-- COVER PAGE -->
    <div class="cover-page">
      <div class="cover-badge-row">
        <span class="cover-badge badge-confidential">Confidential &mdash; Highly Restricted</span>
        <span class="cover-badge badge-version">Document Version 1.0 &bull; Approved</span>
      </div>

      <div class="cover-main">
        <div class="cover-pretitle">Enterprise Solution Architecture Report</div>
        <h1 class="cover-title">Next-Generation Cloud-Native Real-Time Financial Fraud Detection Platform</h1>
        <p class="cover-subtitle">
          Architecture, Engineering &amp; Operationalization Blueprint for High-Volume, Low-Latency Transaction Classification, Deterministic WORM Audit Replayability &amp; Real-Time Operations Telemetry.
        </p>

        <table class="metadata-table">
          <tr>
            <td class="meta-label">Author &amp; Role</td>
            <td class="meta-val">Principal Solutions Architect, Financial Services Cloud Architecture</td>
          </tr>
          <tr>
            <td class="meta-label">Target Environment</td>
            <td class="meta-val">Multi-Availability Zone Cloud-Native Infrastructure (AWS / Azure / GCP)</td>
          </tr>
          <tr>
            <td class="meta-label">System Performance Baseline</td>
            <td class="meta-val">1,000 Transactions/Sec (Peak) &bull; P99 Latency &le; 45ms &bull; 99.99% Reliability</td>
          </tr>
          <tr>
            <td class="meta-label">Regulatory Mandates</td>
            <td class="meta-val">BCBS 239, Basel III, PCI-DSS v4.0, GDPR Art. 22, FedNow &amp; SEPA Instant</td>
          </tr>
          <tr>
            <td class="meta-label">Document Reference</td>
            <td class="meta-val"><code>SAR-FINFRAUD-2026-V1.0</code></td>
          </tr>
          <tr>
            <td class="meta-label">Date Ratified</td>
            <td class="meta-val">November 3, 2026</td>
          </tr>
        </table>
      </div>

      <div style="font-size: 8pt; color: #94a3b8; text-align: center; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        &copy; 2026 Global Retail &amp; Commercial Banking Institution. All Rights Reserved. Enterprise Architecture &amp; Risk Governance Board.
      </div>
    </div>

    <!-- TABLE OF CONTENTS -->
    <div class="toc-section">
      <h2 class="toc-title">Table of Contents</h2>
      <ul class="toc-list">
        <li class="toc-item"><a href="#section-1">1. Executive Summary &amp; Project Context</a> <span>03</span></li>
        <li class="toc-item"><a href="#section-2">2. Functional Decomposition &amp; Core Microservices Architecture</a> <span>05</span></li>
        <li class="toc-item"><a href="#section-3">3. Event-Driven Communication &amp; Messaging Backbone</a> <span>07</span></li>
        <li class="toc-item"><a href="#section-4">4. Real-Time Analyst Frontend &amp; BFF Architecture</a> <span>09</span></li>
        <li class="toc-item"><a href="#section-5">5. Enterprise Observability &amp; Telemetry Framework</a> <span>11</span></li>
        <li class="toc-item"><a href="#section-6">6. Scalability &amp; Resilience Engineering</a> <span>12</span></li>
        <li class="toc-item"><a href="#section-7">7. Architectural Patterns Evaluation &amp; Cost-Benefit Analysis</a> <span>15</span></li>
        <li class="toc-item"><a href="#section-8">8. Proposed Technology Stack &amp; Justifications</a> <span>16</span></li>
        <li class="toc-item"><a href="#section-9">9. Critical Evaluation &amp; Financial Services Trade-Offs</a> <span>17</span></li>
        <li class="toc-item"><a href="#section-10">10. Standout Production Strategies: Deployment &amp; Extreme Load</a> <span>18</span></li>
        <li class="toc-item"><a href="#section-11">11. Architecture Diagrams Gallery &amp; Visual Walkthrough</a> <span>19</span></li>
        <li class="toc-item"><a href="#section-12">12. Implementation Roadmap, Migration Strategy &amp; Conclusion</a> <span>26</span></li>
      </ul>
    </div>

    <!-- MAIN BODY SECTIONS -->
    {full_body}

  </div>
</body>
</html>
"""

    with open(HTML_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"HTML report compiled: {HTML_FILE_PATH} ({len(html_template)} characters)")

def compile_pdf():
    print("Compiling PDF deliverable using Microsoft Edge headless...")
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_bin = None
    for p in edge_paths:
        if os.path.exists(p):
            edge_bin = p
            break
            
    if not edge_bin:
        raise FileNotFoundError("Microsoft Edge executable not found!")

    html_url = f"file:///{HTML_FILE_PATH.replace(os.sep, '/')}"
    ps_command = f'& "{edge_bin}" --headless=new --disable-gpu --run-all-compositor-stages-before-draw --print-to-pdf="{PDF_FILE_PATH}" --no-pdf-header-footer "{html_url}"'
    
    start_time = time.time()
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_command], capture_output=True, text=True)
    elapsed = time.time() - start_time
    print(f"Edge execution finished in {elapsed:.2f}s with code {res.returncode}")
    
    # Wait for file to settle
    time.sleep(2)
    if os.path.exists(PDF_FILE_PATH):
        size_bytes = os.path.getsize(PDF_FILE_PATH)
        print(f"Successfully generated PDF: {PDF_FILE_PATH} ({size_bytes:,} bytes)")
    else:
        raise RuntimeError(f"PDF compilation failed! Output: {res.stderr}")

def verify_pdf():
    print("Verifying generated PDF structure and pages...")
    reader = pypdf.PdfReader(PDF_FILE_PATH)
    total_pages = len(reader.pages)
    print(f"PDF Page Count: {total_pages} pages")
    
    text_sample = ""
    for idx in range(min(5, total_pages)):
        text_sample += f"--- Page {idx+1} ---\n" + reader.pages[idx].extract_text()[:250] + "\n"
    
    print("Sample extracted text:")
    try:
        print(text_sample)
    except Exception:
        print(text_sample.encode('ascii', errors='replace').decode('ascii'))
    
    # Render thumbnails of key pages to build/
    print("Rendering sample page previews to verify layout...")
    pdfium_doc = pypdfium2.PdfDocument(PDF_FILE_PATH)
    pages_to_render = [0, 1, 4, 10, total_pages - 1]
    for p_no in pages_to_render:
        if p_no < total_pages:
            page = pdfium_doc.get_page(p_no)
            bitmap = page.render(scale=1.5)
            pil_image = bitmap.to_pil()
            thumb_path = os.path.join(BUILD_DIR, f"page_preview_{p_no+1}.png")
            pil_image.save(thumb_path)
            print(f"Rendered preview: {thumb_path}")

def main():
    assemble_markdown()
    assemble_html()
    compile_pdf()
    verify_pdf()
    print("\nAll deliverables generated and verified successfully!")

if __name__ == "__main__":
    main()