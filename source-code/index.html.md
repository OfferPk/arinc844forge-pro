\<\!DOCTYPE html\>  
\<html lang="en"\>  
\<head\>  
  \<meta charset="UTF-8"\>  
  \<meta name="viewport" content="width=device-width, initial-scale=1.0"\>  
  \<title\>ARINC844Forge Pro — Commercial Aviation Electronic Logbook (ELB)\</title\>  
  \<style\>  
    :root {  
      \--bg-dark: \#0a0f18;  
      \--card-bg: \#111927;  
      \--card-border: \#1e293b;  
      \--primary: \#38bdf8;  
      \--accent: \#0ea5e9;  
      \--success: \#10b981;  
      \--warning: \#f59e0b;  
      \--danger: \#ef4444;  
      \--text: \#f1f5f9;  
      \--text-muted: \#94a3b8;  
      \--font-mono: 'JetBrains Mono', 'Fira Code', monospace;  
    }  
    \* { box-sizing: border-box; margin: 0; padding: 0; }  
    body {  
      background: var(--bg-dark);  
      color: var(--text);  
      font-family: \-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;  
      padding: 1.5rem;  
      line-height: 1.5;  
    }  
    header {  
      display: flex;  
      justify-content: space-between;  
      align-items: center;  
      padding-bottom: 1.5rem;  
      border-bottom: 1px solid var(--card-border);  
      margin-bottom: 1.5rem;  
    }  
    .brand {  
      display: flex;  
      align-items: center;  
      gap: 1rem;  
    }  
    .logo-badge {  
      background: linear-gradient(135deg, \#0284c7, \#0369a1);  
      color: white;  
      padding: 0.5rem 0.8rem;  
      border-radius: 6px;  
      font-weight: 800;  
      font-size: 1.1rem;  
      letter-spacing: 1px;  
    }  
    .brand-title h1 {  
      font-size: 1.4rem;  
      font-weight: 700;  
      color: \#fff;  
    }  
    .brand-title p {  
      font-size: 0.85rem;  
      color: var(--text-muted);  
    }  
    .status-badge {  
      display: inline-flex;  
      align-items: center;  
      gap: 0.5rem;  
      padding: 0.4rem 0.8rem;  
      border-radius: 9999px;  
      font-size: 0.85rem;  
      font-weight: 600;  
      background: rgba(16, 185, 129, 0.15);  
      color: \#34d399;  
      border: 1px solid rgba(16, 185, 129, 0.3);  
    }  
    .nav-tabs {  
      display: flex;  
      gap: 0.5rem;  
      margin-bottom: 1.5rem;  
      border-bottom: 1px solid var(--card-border);  
      padding-bottom: 0.5rem;  
    }  
    .tab-btn {  
      background: transparent;  
      border: none;  
      color: var(--text-muted);  
      padding: 0.6rem 1.2rem;  
      border-radius: 6px;  
      cursor: pointer;  
      font-weight: 600;  
      font-size: 0.9rem;  
      transition: all 0.2s;  
    }  
    .tab-btn:hover {  
      background: rgba(255, 255, 255, 0.05);  
      color: var(--text);  
    }  
    .tab-btn.active {  
      background: var(--card-bg);  
      color: var(--primary);  
      border: 1px solid var(--card-border);  
    }  
    .grid-2 {  
      display: grid;  
      grid-template-columns: 1fr 1fr;  
      gap: 1.5rem;  
    }  
    .grid-3 {  
      display: grid;  
      grid-template-columns: repeat(3, 1fr);  
      gap: 1.5rem;  
    }  
    .card {  
      background: var(--card-bg);  
      border: 1px solid var(--card-border);  
      border-radius: 8px;  
      padding: 1.25rem;  
      margin-bottom: 1.5rem;  
    }  
    .card-header {  
      display: flex;  
      justify-content: space-between;  
      align-items: center;  
      margin-bottom: 1rem;  
      padding-bottom: 0.5rem;  
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);  
    }  
    .card-title {  
      font-size: 1.05rem;  
      font-weight: 600;  
      color: var(--primary);  
      display: flex;  
      align-items: center;  
      gap: 0.5rem;  
    }  
    .data-row {  
      display: flex;  
      justify-content: space-between;  
      padding: 0.4rem 0;  
      border-bottom: 1px solid rgba(255, 255, 255, 0.03);  
      font-size: 0.9rem;  
    }  
    .data-row .label { color: var(--text-muted); }  
    .data-row .val { font-weight: 500; font-family: var(--font-mono); }  
    table {  
      width: 100%;  
      border-collapse: collapse;  
      margin-top: 0.5rem;  
      font-size: 0.88rem;  
    }  
    th, td {  
      padding: 0.6rem;  
      text-align: left;  
      border-bottom: 1px solid var(--card-border);  
    }  
    th {  
      color: var(--text-muted);  
      font-weight: 600;  
      background: rgba(0, 0, 0, 0.2);  
    }  
    .badge {  
      display: inline-block;  
      padding: 0.2rem 0.5rem;  
      border-radius: 4px;  
      font-size: 0.75rem;  
      font-weight: 600;  
      font-family: var(--font-mono);  
    }  
    .badge-rectified { background: rgba(16, 185, 129, 0.2); color: \#34d399; }  
    .badge-mel { background: rgba(245, 158, 11, 0.2); color: \#fbbf24; }  
    .badge-open { background: rgba(239, 68, 68, 0.2); color: \#f87171; }  
    .btn {  
      background: var(--accent);  
      color: white;  
      border: none;  
      padding: 0.5rem 1rem;  
      border-radius: 6px;  
      cursor: pointer;  
      font-weight: 600;  
      font-size: 0.85rem;  
      transition: background 0.2s;  
    }  
    .btn:hover { background: \#0284c7; }  
    .btn-outline {  
      background: transparent;  
      border: 1px solid var(--card-border);  
      color: var(--text);  
    }  
    .btn-outline:hover { background: rgba(255, 255, 255, 0.05); }  
    .code-block {  
      background: \#060910;  
      border: 1px solid var(--card-border);  
      border-radius: 6px;  
      padding: 1rem;  
      font-family: var(--font-mono);  
      font-size: 0.82rem;  
      color: \#38bdf8;  
      overflow-x: auto;  
    }  
    .tab-content { display: none; }  
    .tab-content.active { display: block; }  
  \</style\>  
\</head\>  
\<body\>

  \<header\>  
    \<div class="brand"\>  
      \<div class="logo-badge"\>ARINC 844\</div\>  
      \<div class="brand-title"\>  
        \<h1\>ARINC844Forge Pro — Electronic Logbook (ELB)\</h1\>  
        \<p\>Normative Commercial Aviation ELB & Digital Airworthiness Release System\</p\>  
      \</div\>  
    \</div\>  
    \<div style="display: flex; gap: 1rem; align-items: center;"\>  
      \<div class="status-badge" id="airworthiness-badge"\>  
        \<span\>●\</span\> AIRCRAFT AIRWORTHY — RELEASED TO SERVICE  
      \</div\>  
      \<button class="btn" onclick="runNormativeAudit()"\>Run 10-Point Audit\</button\>  
    \</div\>  
  \</header\>

  \<nav class="nav-tabs"\>  
    \<button class="tab-btn active" onclick="switchTab('sector')"\>Sector Flight Log\</button\>  
    \<button class="tab-btn" onclick="switchTab('defects')"\>Discrepancies (PIREP/MAREP)\</button\>  
    \<button class="tab-btn" onclick="switchTab('mel')"\>MEL Deferrals\</button\>  
    \<button class="tab-btn" onclick="switchTab('release')"\>Airworthiness Release\</button\>  
    \<button class="tab-btn" onclick="switchTab('arinc429')"\>ARINC 429 Bus\</button\>  
    \<button class="tab-btn" onclick="switchTab('auditor')"\>Compliance Auditor\</button\>  
  \</nav\>

  \<\!-- TAB: SECTOR FLIGHT LOG \--\>  
  \<div id="tab-sector" class="tab-content active"\>  
    \<div class="grid-3"\>  
      \<div class="card"\>  
        \<div class="card-header"\>\<span class="card-title"\>Aircraft Registry\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Tail Number:\</span\>\<span class="val"\>A6-EGA\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Airframe Type:\</span\>\<span class="val"\>Boeing 777-300ER\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Serial / MSN:\</span\>\<span class="val"\>MSN-60124\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Operator:\</span\>\<span class="val"\>Emirates Airline\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Total Airframe Hours:\</span\>\<span class="val"\>18,452.3 hrs\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Total Airframe Cycles:\</span\>\<span class="val"\>4,120 cycles\</span\>\</div\>  
      \</div\>  
      \<div class="card"\>  
        \<div class="card-header"\>\<span class="card-title"\>Active Sector Leg\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Sector Record ID:\</span\>\<span class="val"\>SEC-20261016-UAE844\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Flight Number:\</span\>\<span class="val"\>UAE844\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Route:\</span\>\<span class="val"\>OMDB (DXB) → EGLL (LHR)\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Sched Departure:\</span\>\<span class="val"\>03:00 UTC\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Sector Status:\</span\>\<span class="val" style="color:\#34d399;"\>RELEASED\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Electronic Logbook:\</span\>\<span class="val"\>ARINC 844 Ed. 1\</span\>\</div\>  
      \</div\>  
      \<div class="card"\>  
        \<div class="card-header"\>\<span class="card-title"\>OOOI Timings & Fuel\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Block Out / In:\</span\>\<span class="val"\>03:05 / 10:45 UTC\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Takeoff / Touchdown:\</span\>\<span class="val"\>03:20 / 10:35 UTC\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Block / Flight Hours:\</span\>\<span class="val"\>7.67h / 7.25h\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Fuel Uplift (kg):\</span\>\<span class="val"\>74,500 kg\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Fuel Burn (kg):\</span\>\<span class="val"\>62,300 kg\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Fuel Remaining (kg):\</span\>\<span class="val"\>12,200 kg\</span\>\</div\>  
      \</div\>  
    \</div\>  
  \</div\>

  \<\!-- TAB: DEFECTS \--\>  
  \<div id="tab-defects" class="tab-content"\>  
    \<div class="card"\>  
      \<div class="card-header"\>  
        \<span class="card-title"\>Technical Log Discrepancies (PIREP / MAREP)\</span\>  
        \<button class="btn btn-outline" onclick="alert('Opening defect submission modal')"\>+ Log Discrepancy\</button\>  
      \</div\>  
      \<table\>  
        \<thead\>  
          \<tr\>  
            \<th\>Defect ID\</th\>  
            \<th\>Type\</th\>  
            \<th\>ATA Chapter\</th\>  
            \<th\>System / Component\</th\>  
            \<th\>Discrepancy Description\</th\>  
            \<th\>Status\</th\>  
            \<th\>Disposition / Rectification\</th\>  
          \</tr\>  
        \</thead\>  
        \<tbody\>  
          \<tr\>  
            \<td style="font-family:var(--font-mono); color:var(--primary);"\>DEF-844-01\</td\>  
            \<td\>\<span class="badge" style="background:\#1e3a8a; color:\#93c5fd;"\>PIREP\</span\>\</td\>  
            \<td\>ATA 21-31\</td\>  
            \<td\>Air Conditioning / Outflow Valve\</td\>  
            \<td\>Forward outflow valve position indication intermittent flicker during descent passing FL150.\</td\>  
            \<td\>\<span class="badge badge-mel"\>DEFERRED MEL\</span\>\</td\>  
            \<td\>Deferred per MEL 21-31-01 Cat C (10-Day interval). Operational test satisfactory.\</td\>  
          \</tr\>  
          \<tr\>  
            \<td style="font-family:var(--font-mono); color:var(--primary);"\>DEF-844-02\</td\>  
            \<td\>\<span class="badge" style="background:\#374151; color:\#e5e7eb;"\>MAREP\</span\>\</td\>  
            \<td\>ATA 33-41\</td\>  
            \<td\>Exterior Lighting / Strobe\</td\>  
            \<td\>Right wingtip navigation strobe light found unserviceable on preflight walkaround.\</td\>  
            \<td\>\<span class="badge badge-rectified"\>RECTIFIED\</span\>\</td\>  
            \<td\>Replaced strobe power supply unit P/N 33-41-01-A per AMM 33-41-00. Functional test passed.\</td\>  
          \</tr\>  
        \</tbody\>  
      \</table\>  
    \</div\>  
  \</div\>

  \<\!-- TAB: MEL \--\>  
  \<div id="tab-mel" class="tab-content"\>  
    \<div class="grid-2"\>  
      \<div class="card"\>  
        \<div class="card-header"\>\<span class="card-title"\>Active MEL Item: DEF-844-01\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>MEL Reference:\</span\>\<span class="val"\>MEL 21-31-01\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>ATA Chapter:\</span\>\<span class="val"\>21-31 Pressure Control\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>MEL Deferral Category:\</span\>\<span class="val" style="color:\#fbbf24;"\>CAT C (10 Calendar Days)\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Date Logged:\</span\>\<span class="val"\>2026-10-16 02:15 UTC\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Rectification Limit:\</span\>\<span class="val" style="color:\#34d399;"\>2026-10-26 23:59 UTC\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Days Remaining:\</span\>\<span class="val"\>10 Days 21 Hours\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Dispatch Condition:\</span\>\<span class="val"\>(M) Verified manual mode operational\</span\>\</div\>  
      \</div\>  
      \<div class="card"\>  
        \<div class="card-header"\>\<span class="card-title"\>MEL Interval Norms (ARINC 844 / MMEL)\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Category A:\</span\>\<span class="val"\>Specified in Remarks (e.g. 1 flight, 24h)\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Category B:\</span\>\<span class="val"\>3 Consecutive Calendar Days (72h)\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Category C:\</span\>\<span class="val"\>10 Consecutive Calendar Days\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Category D:\</span\>\<span class="val"\>120 Consecutive Calendar Days\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Repetitive Inspections:\</span\>\<span class="val"\>(O) / (M) Tracking enabled\</span\>\</div\>  
      \</div\>  
    \</div\>  
  \</div\>

  \<\!-- TAB: RELEASE \--\>  
  \<div id="tab-release" class="tab-content"\>  
    \<div class="grid-2"\>  
      \<div class="card"\>  
        \<div class="card-header"\>\<span class="card-title"\>LAME Certificate of Release to Service (CRS)\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Certifying Engineer:\</span\>\<span class="val"\>Tariq Al-Maktoum\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>License Number:\</span\>\<span class="val"\>UAE-GCAA-66-8442 (Part 66 B2)\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Authorization:\</span\>\<span class="val"\>Part 145 / CAR 145\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Timestamp:\</span\>\<span class="val"\>2026-10-16 02:40:00 UTC\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Signature Status:\</span\>\<span class="val" style="color:\#34d399;"\>CRYPTOGRAPHICALLY VERIFIED\</span\>\</div\>  
        \<p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.5rem; font-style:italic;"\>  
          "I hereby certify that the work specified, except as otherwise noted, has been carried out in accordance with CAR M / Part 145 and in respect to that work the aircraft is considered ready for release to service."  
        \</p\>  
      \</div\>  
      \<div class="card"\>  
        \<div class="card-header"\>\<span class="card-title"\>Pilot-in-Command (PIC) Acceptance\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Commander:\</span\>\<span class="val"\>Capt. Alexander Vance\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>License Number:\</span\>\<span class="val"\>FAA-ATPL-1844902\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Flight Number:\</span\>\<span class="val"\>UAE844 (OMDB → EGLL)\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Timestamp:\</span\>\<span class="val"\>2026-10-16 02:50:00 UTC\</span\>\</div\>  
        \<div class="data-row"\>\<span class="label"\>Acceptance Status:\</span\>\<span class="val" style="color:\#34d399;"\>SIGNED & ACCEPTED\</span\>\</div\>  
        \<p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.5rem; font-style:italic;"\>  
          "I accept aircraft A6-EGA for flight UAE844 with all open deferred defects reviewed and compliant with dispatch conditions."  
        \</p\>  
      \</div\>  
    \</div\>  
    \<div class="card"\>  
      \<div class="card-header"\>\<span class="card-title"\>FAA AC 120-78A Cryptographic Log Chaining\</span\>\</div\>  
      \<div class="code-block" id="chain-display"\>  
\[GENESIS\] Block 0 \-\> Hash: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  
\[BLOCK 1\] Action: SECTOR\_OPEN \| Ref: SEC-20261016-UAE844 \| Hash: a7f891b0c9e...  
\[BLOCK 2\] Action: DEFECT\_LOGGED \| Ref: DEF-844-01 \| Hash: 83c9d2f10ae...  
\[BLOCK 3\] Action: CRS\_SIGNED \| Ref: UAE-GCAA-66-8442 \| Hash: b41ef8c0a9...  
\[BLOCK 4\] Action: PIC\_ACCEPTED \| Ref: FAA-ATPL-1844902 \| Hash: d99a81c04f...  
      \</div\>  
    \</div\>  
  \</div\>

  \<\!-- TAB: ARINC 429 \--\>  
  \<div id="tab-arinc429" class="tab-content"\>  
    \<div class="card"\>  
      \<div class="card-header"\>\<span class="card-title"\>Avionics Discrete Bus Synthesizer (ARINC 429 Part 1)\</span\>\</div\>  
      \<div class="grid-2"\>  
        \<div\>  
          \<h4 style="color:\#38bdf8; margin-bottom:0.5rem;"\>Label 232 (Octal): Airworthiness Dispatch Status\</h4\>  
          \<div class="code-block"\>  
Hex:     0xB008EC9A  
Binary:  1011 0000 0000 1000 1110 1100 1001 1010  
Label:   0x9A (Octal 232\)  
Bits 11-13 (State):  011 (Released to Service)  
Bit 14 (LAME CRS):   1 (Certified)  
Bit 15 (PIC Accept): 1 (Accepted)  
Bits 16-19 (MELs):   0001 (1 Active Deferred MEL)  
Bit 32 (Parity):     1 (Odd Parity Valid)  
          \</div\>  
        \</div\>  
        \<div\>  
          \<h4 style="color:\#38bdf8; margin-bottom:0.5rem;"\>Label 233 (Octal): Sector Sequence & Log Revision\</h4\>  
          \<div class="code-block"\>  
Hex:     0xB014B09B  
Binary:  1011 0000 0001 0100 1011 0000 1001 1011  
Label:   0x9B (Octal 233\)  
Bits 11-18 (Sector): 0010 1100 (Sector 44\)  
Bits 19-24 (Rev):    0001 01 (Chain Revision 5\)  
Bits 29-30 (SSM):    11 (Normal Operation)  
Bit 32 (Parity):     1 (Odd Parity Valid)  
          \</div\>  
        \</div\>  
      \</div\>  
    \</div\>  
  \</div\>

  \<\!-- TAB: COMPLIANCE AUDITOR \--\>  
  \<div id="tab-auditor" class="tab-content"\>  
    \<div class="card"\>  
      \<div class="card-header"\>  
        \<span class="card-title"\>Normative Aviation Electronic Logbook Regulatory Audit\</span\>  
        \<span id="audit-score" style="font-family:var(--font-mono); color:\#34d399; font-weight:700;"\>10 / 10 CHECKS PASSED (100.0%)\</span\>  
      \</div\>  
      \<div id="audit-results-list"\>  
        \<\!-- Rendered by JS \--\>  
      \</div\>  
    \</div\>  
  \</div\>

  \<script src="arinc844-engine.js"\>\</script\>  
  \<script src="arinc844-auditor.js"\>\</script\>  
  \<script\>  
    function switchTab(tabId) {  
      document.querySelectorAll('.tab-btn').forEach(b \=\> b.classList.remove('active'));  
      document.querySelectorAll('.tab-content').forEach(c \=\> c.classList.remove('active'));  
      event.target.classList.add('active');  
      document.getElementById('tab-' \+ tabId).classList.add('active');  
    }

    function runNormativeAudit() {  
      switchTab('auditor');  
      const engine \= new ARINC844Engine();  
      const auditor \= new ARINC844Auditor(engine);  
      const res \= auditor.audit();

      document.getElementById('audit-score').innerText \= \`\${res.passedCount} / \${res.totalTests} CHECKS PASSED (\${res.scorePct}%)\`;

      const container \= document.getElementById('audit-results-list');  
      container.innerHTML \= res.results.map(r \=\> \`  
        \<div style="padding: 0.8rem; margin-bottom: 0.5rem; background: rgba(255,255,255,0.02); border-left: 4px solid \${r.passed ? '\#10b981' : '\#ef4444'}; border-radius: 4px;"\>  
          \<div style="display:flex; justify-content:space-between; align-items:center;"\>  
            \<strong style="color:\${r.passed ? '\#34d399' : '\#f87171'}"\>\${r.id}: \${r.rule}\</strong\>  
            \<span class="badge \${r.passed ? 'badge-rectified' : 'badge-open'}"\>\${r.passed ? 'PASS' : 'FAIL'}\</span\>  
          \</div\>  
          \<div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;"\>Standard: \${r.standard}\</div\>  
          \<div style="font-size:0.85rem; color:\#cbd5e1; margin-top:0.2rem;"\>\${r.details}\</div\>  
        \</div\>  
      \`).join('');  
    }

    window.onload \= function() {  
      runNormativeAudit();  
    };  
  \</script\>  
\</body\>  
\</html\>  
