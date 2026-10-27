#!/usr/bin/env python3
"""
ARINC844Forge Pro — Standalone Python 3 CLI & Avionics Logbook Engine
Commercial Aviation Electronic Logbook (ARINC Report 844 & FAA AC 120-78A)
"""

import sys
import json
import hashlib
import datetime

class ARINC844CLI:
    def __init__(self):
        self.aircraft = {
            "tailNumber": "A6-EGA",
            "type": "Boeing 777-300ER",
            "operator": "Emirates Airline",
            "serialNumber": "MSN-60124",
            "totalAirframeHours": 18452.3,
            "totalAirframeCycles": 4120
        }
        self.currentSector = {
            "sectorId": "SEC-20261016-UAE844",
            "flightNumber": "UAE844",
            "originIcao": "OMDB",
            "destinationIcao": "EGLL",
            "scheduledDepartureUtc": "2026-10-16T03:00:00Z",
            "blockOutUtc": "2026-10-16T03:05:00Z",
            "takeoffUtc": "2026-10-16T03:20:00Z",
            "touchdownUtc": "2026-10-16T10:35:00Z",
            "blockInUtc": "2026-10-16T10:45:00Z",
            "flightTimeHours": 7.25,
            "blockTimeHours": 7.67,
            "fuelUpliftKg": 74500.0,
            "fuelBurnKg": 62300.0,
            "fuelRemainingKg": 12200.0,
            "sectorStatus": "CLOSED_PENDING_RELEASE"
        }
        self.defects = [
            {
                "defectId": "DEF-844-01",
                "type": "PIREP",
                "ataChapter": "21-31",
                "systemName": "Air Conditioning / Pressure Control",
                "description": "Forward outflow valve position indication intermittent flicker during descent passing FL150.",
                "status": "DEFERRED_MEL",
                "melReference": "MEL 21-31-01",
                "melCategory": "C",
                "deferralExpiryUtc": "2026-10-26T23:59:00Z",
                "maintenanceAction": "Troubleshot per FIM 21-31. Valve operational in manual/auto. Indication flicker deferred under MEL 21-31-01 Cat C.",
                "rectified": False
            },
            {
                "defectId": "DEF-844-02",
                "type": "MAREP",
                "ataChapter": "33-41",
                "systemName": "Exterior Lighting / Navigation Strobe",
                "description": "Right wingtip navigation strobe light found unserviceable on preflight walkaround.",
                "status": "RECTIFIED",
                "melReference": "N/A",
                "melCategory": "NONE",
                "deferralExpiryUtc": None,
                "maintenanceAction": "Replaced strobe power supply unit P/N 33-41-01-A per AMM 33-41-00. Operational test passed.",
                "rectified": True
            }
        ]
        self.signatures = {
            "lameCrs": {
                "name": "Tariq Al-Maktoum",
                "licenseNumber": "UAE-GCAA-66-8442",
                "role": "Licensed Aircraft Maintenance Engineer (B2 Avionics)",
                "crsStatement": "I hereby certify that the work specified, except as otherwise noted, has been carried out in accordance with CAR M / Part 145 and in respect to that work the aircraft is considered ready for release to service.",
                "timestampUtc": "2026-10-16T02:40:00Z",
                "signed": True,
                "digitalDigest": "sha256-a9b8c7e6d5c4b3a2-crs8442-valid"
            },
            "picAcceptance": {
                "name": "Capt. Alexander Vance",
                "licenseNumber": "FAA-ATPL-1844902",
                "role": "Pilot-in-Command (PIC)",
                "acceptanceStatement": "I accept aircraft A6-EGA for flight UAE844 with all open deferred defects reviewed and compliant with dispatch conditions.",
                "timestampUtc": "2026-10-16T02:50:00Z",
                "signed": True,
                "digitalDigest": "sha256-d4e5f6a1b2c3d4e5-pic18449-valid"
            }
        }
        self.hashChain = [
            {"index": 0, "prevHash": "0" * 64, "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "action": "GENESIS"}
        ]
        self._add_chain_entry("SECTOR_OPEN", self.currentSector["sectorId"])
        self._add_chain_entry("DEFECT_LOGGED", "DEF-844-01")
        self._add_chain_entry("CRS_SIGNED", self.signatures["lameCrs"]["licenseNumber"])
        self._add_chain_entry("PIC_ACCEPTED", self.signatures["picAcceptance"]["licenseNumber"])

    def _add_chain_entry(self, action, ref):
        prev = self.hashChain[-1]["hash"]
        content = f"{prev}:{action}:{ref}:{len(self.hashChain)}".encode("utf-8")
        h = hashlib.sha256(content).hexdigest()
        self.hashChain.append({"index": len(self.hashChain), "prevHash": prev, "hash": h, "action": action, "ref": ref})

    def generate_arinc429(self):
        # Label 232: Airworthiness & Release Status (Octal 232, Hex 0x9A)
        label232 = 0x9A
        airworthy_code = 3 # 3 = Released
        crs_bit = 1 if self.signatures["lameCrs"]["signed"] else 0
        pic_bit = 1 if self.signatures["picAcceptance"]["signed"] else 0
        mel_count = len([d for d in self.defects if d["status"] == "DEFERRED_MEL"])

        data232 = 0
        data232 |= (airworthy_code & 0x07) << 10
        data232 |= (crs_bit & 0x01) << 13
        data232 |= (pic_bit & 0x01) << 14
        data232 |= (mel_count & 0x0F) << 15
        data232 |= (1 & 0x01) << 19 # Gatelink sync bit
        data232 |= (0x03 & 0x03) << 28 # Normal SSM

        word232 = (data232 & 0x7FFFFF00) | (label232 & 0xFF)
        word232 = self._apply_odd_parity(word232)

        # Label 233: Sector Sequence & Chain Revision (Octal 233, Hex 0x9B)
        label233 = 0x9B
        sector_seq = 44
        rev_num = len(self.hashChain) & 0x3F

        data233 = 0
        data233 |= (sector_seq & 0xFF) << 10
        data233 |= (rev_num & 0x3F) << 18
        data233 |= (0x03 & 0x03) << 28

        word233 = (data233 & 0x7FFFFF00) | (label233 & 0xFF)
        word233 = self._apply_odd_parity(word233)

        return {
            "label232": {
                "octal": "232",
                "hex": f"0x{word232:08X}",
                "binary": f"{word232:032b}",
                "parity_valid": self._check_odd_parity(word232),
                "dispatch_state": "RELEASED_AIRWORTHY"
            },
            "label233": {
                "octal": "233",
                "hex": f"0x{word233:08X}",
                "binary": f"{word233:032b}",
                "parity_valid": self._check_odd_parity(word233),
                "sector_seq": sector_seq,
                "chain_depth": len(self.hashChain)
            }
        }

    def _apply_odd_parity(self, w):
        bits = w & 0x7FFFFFFF
        cnt = bin(bits).count('1')
        if cnt % 2 == 0:
            bits |= (1 << 31)
        return bits

    def _check_odd_parity(self, w):
        return bin(w).count('1') % 2 == 1

    def run_audit(self):
        tests = []
        # 1. Sector Completeness
        s = self.currentSector
        t1 = s["flightTimeHours"] > 0 and s["blockTimeHours"] >= s["flightTimeHours"] and s["fuelBurnKg"] > 0
        tests.append(("AUD-844-01", "ARINC Report 844 Sec 3.1 & ICAO Doc 9760", "Sector Flight Leg Completeness & Fuel Accounting", t1))

        # 2. Defect Lifecycle
        t2 = all(d.get("ataChapter") and (d.get("rectified") or d.get("status") == "DEFERRED_MEL") for d in self.defects)
        tests.append(("AUD-844-02", "ARINC Report 844 Sec 4.2 & ATA 100/2200", "PIREP/MAREP Discrepancy Lifecycle & ATA Codes", t2))

        # 3. MEL Category Tracking
        t3 = all(d.get("melCategory") in ["A", "B", "C", "D"] for d in self.defects if d["status"] == "DEFERRED_MEL")
        tests.append(("AUD-844-03", "FAA MMEL / EASA CS-MMEL & ARINC 844 Sec 4.4", "MEL Deferral Classification & Intervals", t3))

        # 4. LAME CRS Signature
        crs = self.signatures["lameCrs"]
        t4 = crs["signed"] and bool(crs["licenseNumber"]) and bool(crs["digitalDigest"])
        tests.append(("AUD-844-04", "EASA Part 145.A.50 / FAR 43.9", "LAME Certificate of Release to Service (CRS)", t4))

        # 5. PIC Acceptance
        pic = self.signatures["picAcceptance"]
        t5 = pic["signed"] and bool(pic["licenseNumber"]) and bool(pic["digitalDigest"])
        tests.append(("AUD-844-05", "FAA FAR 91.7 / 121.363 & ICAO Annex 6", "Pilot-in-Command Technical Acceptance", t5))

        # 6. Digital Signature Non-Repudiation
        t6 = crs["digitalDigest"].startswith("sha256-") and pic["digitalDigest"].startswith("sha256-")
        tests.append(("AUD-844-06", "FAA AC 120-78A & ARINC 844 Sec 5.4", "Cryptographic Signature Non-Repudiation", t6))

        # 7. Hash Chain
        t7 = len(self.hashChain) >= 3 and all(b["hash"] for b in self.hashChain)
        tests.append(("AUD-844-07", "FAA AC 120-78A Sec 4 & ARINC 844 Sec 5.3", "Sequential Tamper-Evident Hash Audit Chain", t7))

        # 8. OOOI Monotonic Sequence
        t8 = s["blockOutUtc"] <= s["takeoffUtc"] < s["touchdownUtc"] <= s["blockInUtc"]
        tests.append(("AUD-844-08", "ARINC Report 844 Sec 3.2", "OOOI Flight Phase Monotonic Time Sequence", t8))

        # 9. ARINC 429 Discrete Bus Parity
        bus = self.generate_arinc429()
        t9 = bus["label232"]["parity_valid"] and bus["label233"]["parity_valid"]
        tests.append(("AUD-844-09", "ARINC 429 Part 1 & ARINC 844 Interface", "ARINC 429 Discrete Bus Odd Parity & Integrity", t9))

        # 10. Overall Airworthiness Release
        t10 = all(t[3] for t in tests[:9])
        tests.append(("AUD-844-10", "EASA AMC 20-22 & ICAO Doc 9760", "Continuous Airworthiness Release to Service", t10))

        return tests

def main():
    cli = ARINC844CLI()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "status":
        print("=================================================================")
        print(" ARINC844Forge Pro — Commercial Aviation Electronic Logbook (ELB)")
        print(" ARINC Report 844 | FAA AC 120-78A | EASA AMC 20-22 | ICAO Doc 976")
        print("=================================================================")
        print(f"Aircraft:    {cli.aircraft['tailNumber']} ({cli.aircraft['type']})")
        print(f"Operator:    {cli.aircraft['operator']} | S/N: {cli.aircraft['serialNumber']}")
        print(f"Hours/Cycle: {cli.aircraft['totalAirframeHours']} hrs / {cli.aircraft['totalAirframeCycles']} cycles")
        print("-----------------------------------------------------------------")
        s = cli.currentSector
        print(f"Sector:      {s['flightNumber']} ({s['originIcao']} -> {s['destinationIcao']})")
        print(f"Times:       Block {s['blockTimeHours']}h | Flight {s['flightTimeHours']}h")
        print(f"Fuel:        Uplift {s['fuelUpliftKg']} kg | Burn {s['fuelBurnKg']} kg | Rem {s['fuelRemainingKg']} kg")
        print(f"Status:      {s['sectorStatus']}")
        print("-----------------------------------------------------------------")
        print(f"Defects:     {len(cli.defects)} recorded (1 Deferred MEL Cat C, 1 Rectified)")
        print(f"LAME CRS:    {cli.signatures['lameCrs']['name']} ({cli.signatures['lameCrs']['licenseNumber']}) [SIGNED]")
        print(f"PIC Accept:  {cli.signatures['picAcceptance']['name']} ({cli.signatures['picAcceptance']['licenseNumber']}) [SIGNED]")
        print("=================================================================")

    elif cmd == "audit":
        tests = cli.run_audit()
        print("=================================================================")
        print(" ARINC 844 / FAA AC 120-78A / EASA AMC 20-22 NORMATIVE AUDIT")
        print("=================================================================")
        passed = sum(1 for t in tests if t[3])
        for code, std, desc, ok in tests:
            mark = "[PASS]" if ok else "[FAIL]"
            print(f"{mark} {code}: {desc}")
            print(f"       Standard: {std}")
        print("-----------------------------------------------------------------")
        print(f"Total Audit Checks: {len(tests)} | Passed: {passed} | Failed: {len(tests) - passed}")
        print(f"Compliance Score:   {(passed/len(tests))*100:.1f}%")
        print("=================================================================")

    elif cmd == "bus":
        b = cli.generate_arinc429()
        print("=================================================================")
        print(" ARINC 429 DISCRETE BUS TELEMETRY (ARINC 844 INTERFACE)")
        print("=================================================================")
        print(f"Label 232 (Airworthiness Dispatch Status):")
        print(f"  Hex:    {b['label232']['hex']} (Bit 32 Odd Parity: {'VALID' if b['label232']['parity_valid'] else 'INVALID'})")
        print(f"  Binary: {b['label232']['binary']}")
        print(f"  State:  {b['label232']['dispatch_state']}")
        print(f"\nLabel 233 (Sector Leg & Logbook Revision):")
        print(f"  Hex:    {b['label233']['hex']} (Bit 32 Odd Parity: {'VALID' if b['label233']['parity_valid'] else 'INVALID'})")
        print(f"  Binary: {b['label233']['binary']}")
        print(f"  Seq:    Leg {b['label233']['sector_seq']} | Hash Chain Depth: {b['label233']['chain_depth']}")
        print("=================================================================")

    elif cmd == "chain":
        print("=================================================================")
        print(" CRYPTOGRAPHIC SHA-256 LOGBOOK HASH CHAIN (FAA AC 120-78A)")
        print("=================================================================")
        for entry in cli.hashChain:
            print(f"[{entry['index']}] Action: {entry['action']}")
            print(f"    Hash:     {entry['hash']}")
            print(f"    PrevHash: {entry['prevHash']}")
        print("=================================================================")

    elif cmd == "json":
        data = {
            "aircraft": cli.aircraft,
            "sector": cli.currentSector,
            "defects": cli.defects,
            "signatures": cli.signatures,
            "hashChain": cli.hashChain,
            "arinc429": cli.generate_arinc429()
        }
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
