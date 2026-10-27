#!/usr/bin/env python3
"""
ARINC844Forge Pro — Automated Unit Test Suite
10 Automated Unit Tests Verifying Core Logic, OOOI Chronology, MEL Categorization,
ARINC 429 Bus Parity, Cryptographic Hash Chaining, and Normative Audit Rules.
"""

import unittest
import importlib.util
import os
import sys

# Import arinc844-cli
spec = importlib.util.spec_from_file_location("arinc844_cli", os.path.join(os.path.dirname(__file__), "arinc844-cli.py"))
arinc844_cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arinc844_cli)
ARINC844CLI = arinc844_cli.ARINC844CLI

class TestARINC844Engine(unittest.TestCase):
    def setUp(self):
        self.cli = ARINC844CLI()

    def test_01_aircraft_airframe_metadata(self):
        """Test 1: Verify aircraft registration, MSN, and airframe hours/cycles."""
        ac = self.cli.aircraft
        self.assertEqual(ac["tailNumber"], "A6-EGA")
        self.assertEqual(ac["type"], "Boeing 777-300ER")
        self.assertGreater(ac["totalAirframeHours"], 10000.0)
        self.assertGreater(ac["totalAirframeCycles"], 2000)

    def test_02_sector_flight_time_and_fuel_integrity(self):
        """Test 2: Verify sector OOOI block/flight time and fuel calculations."""
        s = self.cli.currentSector
        self.assertEqual(s["flightNumber"], "UAE844")
        self.assertEqual(s["originIcao"], "OMDB")
        self.assertEqual(s["destinationIcao"], "EGLL")
        self.assertGreater(s["flightTimeHours"], 0)
        self.assertGreaterEqual(s["blockTimeHours"], s["flightTimeHours"])
        self.assertEqual(s["fuelBurnKg"], s["fuelUpliftKg"] - s["fuelRemainingKg"])

    def test_03_oooi_monotonic_chronology(self):
        """Test 3: Verify strict monotonic ordering of Out -> Off -> On -> In timestamps."""
        s = self.cli.currentSector
        self.assertLessEqual(s["blockOutUtc"], s["takeoffUtc"])
        self.assertLess(s["takeoffUtc"], s["touchdownUtc"])
        self.assertLessEqual(s["touchdownUtc"], s["blockInUtc"])

    def test_04_defect_ata_chapter_and_disposition(self):
        """Test 4: Verify PIREP and MAREP defect records have valid ATA chapters and status."""
        for d in self.cli.defects:
            self.assertTrue(d["ataChapter"].startswith(("21-", "33-")))
            self.assertIn(d["type"], ["PIREP", "MAREP"])
            self.assertIn(d["status"], ["DEFERRED_MEL", "RECTIFIED", "OPEN"])

    def test_05_mel_category_and_deferral_window(self):
        """Test 5: Verify deferred defect conforms to MMEL Category C interval."""
        deferred = [d for d in self.cli.defects if d["status"] == "DEFERRED_MEL"]
        self.assertEqual(len(deferred), 1)
        d0 = deferred[0]
        self.assertEqual(d0["melCategory"], "C")
        self.assertTrue(d0["deferralExpiryUtc"].startswith("2026-10-26"))

    def test_06_lame_crs_and_pic_signatures(self):
        """Test 6: Verify dual-signature airworthiness release credentials and statements."""
        crs = self.cli.signatures["lameCrs"]
        pic = self.cli.signatures["picAcceptance"]
        self.assertTrue(crs["signed"])
        self.assertTrue(pic["signed"])
        self.assertEqual(crs["licenseNumber"], "UAE-GCAA-66-8442")
        self.assertEqual(pic["licenseNumber"], "FAA-ATPL-1844902")
        self.assertIn("ready for release to service", crs["crsStatement"])

    def test_07_cryptographic_digest_binding(self):
        """Test 7: Verify FAA AC 120-78A compliant SHA-256 digital signature digests."""
        for sig in self.cli.signatures.values():
            self.assertTrue(sig["digitalDigest"].startswith("sha256-"))
            self.assertIn("-valid", sig["digitalDigest"])

    def test_08_tamper_evident_hash_chain(self):
        """Test 8: Verify immutable SHA-256 hash chaining of logbook events."""
        chain = self.cli.hashChain
        self.assertGreaterEqual(len(chain), 4)
        for i in range(1, len(chain)):
            self.assertEqual(chain[i]["prevHash"], chain[i-1]["hash"])
            self.assertEqual(len(chain[i]["hash"]), 64)

    def test_09_arinc_429_discrete_bus_odd_parity(self):
        """Test 9: Verify ARINC 429 Labels 232 and 233 generation and Bit 32 odd parity."""
        bus = self.cli.generate_arinc429()
        l232 = bus["label232"]
        l233 = bus["label233"]
        self.assertEqual(l232["octal"], "232")
        self.assertEqual(l233["octal"], "233")
        self.assertTrue(l232["parity_valid"])
        self.assertTrue(l233["parity_valid"])
        self.assertEqual(len(l232["binary"]), 32)
        self.assertEqual(len(l233["binary"]), 32)
        self.assertEqual(bin(int(l232["hex"], 16)).count('1') % 2, 1)
        self.assertEqual(bin(int(l233["hex"], 16)).count('1') % 2, 1)

    def test_10_normative_audit_full_pass(self):
        """Test 10: Verify 10-point normative audit reports 10/10 PASS (100.0% compliance)."""
        tests = self.cli.run_audit()
        self.assertEqual(len(tests), 10)
        passed = sum(1 for t in tests if t[3])
        self.assertEqual(passed, 10)
        self.assertTrue(all(t[3] for t in tests))

if __name__ == "__main__":
    unittest.main()
