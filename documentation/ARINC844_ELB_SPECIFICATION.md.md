# ARINC Report 844 Commercial Aviation Electronic Logbook (ELB) Technical Specification

## 1\. Executive Summary & Regulatory Authority

The **ARINC Report 844** specification defines the industry standard architecture, data interfaces, operational procedures, and airworthiness criteria for **Electronic Logbook (ELB)** software and hardware deployed on commercial passenger and cargo aircraft. ELB systems replace legacy paper aircraft technical logs (ATLs), flight crew journey logs, and cabin discrepancy books.

Compliant with:

- **ARINC Report 844**: Guide for Electronic Logbook (ELB) Design and Implementation  
- **FAA AC 120-78A / AC 120-78B**: Electronic Signatures, Electronic Recordkeeping, and Electronic Manuals  
- **EASA AMC 20-22**: Aircraft Electronic Flight Bag (EFB) and Electronic Technical Log (ETL) Systems  
- **ICAO Annex 6 Part I & ICAO Doc 9760**: Airworthiness Manual for Commercial Air Transport  
- **ATA Spec 100 / Spec 2200**: Standard Information Format for Maintenance Data

---

## 2\. System Architecture & Information Model

### 2.1 Core Subsystems

1. **Flight Leg & OOOI Engine**:  
     
   - Captures automated Out-Off-On-In (OOOI) discrete flight phase transitions.  
   - Calculates block time, flight hours, takeoff/landing counts, and airframe/engine cycle deltas.  
   - Computes continuous fuel uplift, departure fuel, en-route burn, and shut-down fuel balance.

   

2. **Technical Discrepancy & Defect Manager (PIREP / MAREP)**:  
     
   - Distinguishes Pilot Reports (PIREP, flight crew observations) from Maintenance Reports (MAREP, line technician observations).  
   - Classifies each defect by ATA 100/2200 chapter (e.g., ATA 21 Air Conditioning, ATA 33 Lights).  
   - Manages defect status lifecycle: `OPEN` \-\> `TROUBLESHOOTING` \-\> `DEFERRED_MEL` \-\> `RECTIFIED` \-\> `CLOSED`.

   

3. **Minimum Equipment List (MEL) & CDL Tracking Engine**:  
     
   - Regulates dispatch in accordance with the operator's approved MEL derived from Master MEL (MMEL).  
   - Enforces strict rectification intervals:  
     - **Category A**: As specified in remarks (fixed flight count or calendar hours).  
     - **Category B**: 3 consecutive calendar days (72 hours).  
     - **Category C**: 10 consecutive calendar days.  
     - **Category D**: 120 consecutive calendar days.  
   - Tracks operational (O) and maintenance (M) dispatch prerequisites.

   

4. **Cryptographic Airworthiness Release & Non-Repudiation**:  
     
   - Dual-authorization architecture:  
     - **LAME Part 145 / Part 66 CRS**: Certificate of Release to Service affirming maintenance work complies with CAR M / Part 145\.  
     - **Pilot-in-Command (PIC) Acceptance**: Legal operational acceptance under FAR 91.7 / 121.363.  
   - Cryptographic signature binding incorporating user certificate, timestamp, license ID, and SHA-256 payload digest.  
   - Sequential tamper-evident hash chaining where each log entry cryptographically encapsulates the previous entry's hash.

   

5. **ARINC 429 Avionics Bus Discrete Interface**:  
     
   - Transmits airworthiness dispatch state directly to aircraft Core Integrated Avionics (e.g., Boeing AIMS / Airbus PRIM):  
     - **Label 232 (Octal 232 / Hex 0x9A)**: ELB Airworthiness Dispatch Status & MEL Count.  
     - **Label 233 (Octal 233 / Hex 0x9B)**: Active Sector Leg & Logbook Revision Sequence.  
   - Formatted in 32-bit ARINC 429 words featuring Bit 32 odd parity verification.

---

## 3\. ARINC 429 Word Bit Encoding Specifications

### Label 232: Airworthiness Dispatch Status

| Bits | Function | Encoding / Valid Values |
| :---- | :---- | :---- |
| 1–8 | Label (Octal 232 / Hex 0x9A) | `1001 1010` (Reversed transmission order) |
| 9–10 | Source / Destination Identifier (SDI) | `00` (All receivers) |
| 11–13 | Airworthiness State | `000`\=Grounded, `001`\=Unsigned, `010`\=MEL Valid, `011`\=Released |
| 14 | LAME CRS Signed | `0`\=Unsigned, `1`\=Certified & Signed |
| 15 | PIC Accepted | `0`\=Unaccepted, `1`\=Accepted |
| 16–19 | Active Deferred MEL Count | `0000` to `1111` (0 to 15 items) |
| 20 | Gatelink Ground Sync Active | `0`\=Offline, `1`\=Synchronizing |
| 21–28 | Reserved / Spare | `0000 0000` |
| 29–30 | Sign / Status Matrix (SSM) | `11` \= Normal Operation |
| 31 | Reserved | `0` |
| 32 | Parity Bit | Odd parity over bits 1–31 |

### Label 233: Sector Leg & Logbook Revision

| Bits | Function | Encoding / Valid Values |
| :---- | :---- | :---- |
| 1–8 | Label (Octal 233 / Hex 0x9B) | `1001 1011` |
| 9–10 | Source / Destination Identifier (SDI) | `00` |
| 11–18 | Sector Leg Number | `0` to `255` (Current flight sequence number) |
| 19–24 | Cryptographic Hash Chain Revision | `0` to `63` (Sequential block depth) |
| 25–28 | Reserved / Spare | `0000` |
| 29–30 | Sign / Status Matrix (SSM) | `11` \= Normal Operation |
| 31 | Reserved | `0` |
| 32 | Parity Bit | Odd parity over bits 1–31 |

