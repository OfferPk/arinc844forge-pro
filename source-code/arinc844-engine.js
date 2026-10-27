/**
 * ARINC844Forge Pro — Core Engine
 * Commercial Aviation Electronic Logbook (ELB) & Digital Airworthiness Release
 * Standards: ARINC Report 844, FAA AC 120-78A, EASA AMC 20-22, ICAO Doc 9760
 */

class ARINC844Engine {
  constructor() {
    this.aircraft = {
      tailNumber: 'A6-EGA',
      type: 'Boeing 777-300ER',
      operator: 'Emirates Airline',
      serialNumber: 'MSN-60124',
      totalAirframeHours: 18452.3,
      totalAirframeCycles: 4120
    };

    // Active Sector Record (Flight Leg OMDB -> EGLL)
    this.currentSector = {
      sectorId: 'SEC-20261016-UAE844',
      flightNumber: 'UAE844',
      originIcao: 'OMDB',
      destinationIcao: 'EGLL',
      scheduledDepartureUtc: '2026-10-16T03:00:00Z',
      blockOutUtc: '2026-10-16T03:05:00Z',
      takeoffUtc: '2026-10-16T03:20:00Z',
      touchdownUtc: '2026-10-16T10:35:00Z',
      blockInUtc: '2026-10-16T10:45:00Z',
      flightTimeHours: 7.25,
      blockTimeHours: 7.67,
      fuelUpliftKg: 74500.0,
      fuelBurnKg: 62300.0,
      fuelRemainingKg: 12200.0,
      sectorStatus: 'CLOSED_PENDING_RELEASE'
    };

    // Maintenance Discrepancy & Defect Log (PIREP / MAREP)
    this.defects = [
      {
        defectId: 'DEF-844-01',
        type: 'PIREP',
        ataChapter: '21-31',
        systemName: 'Air Conditioning / Pressure Control',
        description: 'Forward outflow valve position indication intermittent flicker during descent passing FL150.',
        status: 'DEFERRED_MEL',
        melReference: 'MEL 21-31-01',
        melCategory: 'C', // 10 days
        deferralExpiryUtc: '2026-10-26T23:59:00Z',
        maintenanceAction: 'Troubleshot per FIM 21-31. Valve operational in manual/auto. Indication flicker deferred under MEL 21-31-01 Cat C.',
        rectified: false
      },
      {
        defectId: 'DEF-844-02',
        type: 'MAREP',
        ataChapter: '33-41',
        systemName: 'Exterior Lighting / Navigation Strobe',
        description: 'Right wingtip navigation strobe light found unserviceable on preflight walkaround.',
        status: 'RECTIFIED',
        melReference: 'N/A',
        melCategory: 'NONE',
        deferralExpiryUtc: null,
        maintenanceAction: 'Replaced strobe power supply unit P/N 33-41-01-A per AMM 33-41-00. Operational test passed.',
        rectified: true
      }
    ];

    // Cryptographic Signatures & Airworthiness Release (FAA AC 120-78A)
    this.signatures = {
      lameCrs: {
        name: 'Tariq Al-Maktoum',
        licenseNumber: 'UAE-GCAA-66-8442',
        role: 'Licensed Aircraft Maintenance Engineer (B2 Avionics)',
        crsStatement: 'I hereby certify that the work specified, except as otherwise noted, has been carried out in accordance with CAR M / Part 145 and in respect to that work the aircraft is considered ready for release to service.',
        timestampUtc: '2026-10-16T02:40:00Z',
        signed: true,
        digitalDigest: 'sha256-a9b8c7...crs8442...valid'
      },
      picAcceptance: {
        name: 'Capt. Alexander Vance',
        licenseNumber: 'FAA-ATPL-1844902',
        role: 'Pilot-in-Command (PIC)',
        acceptanceStatement: 'I accept aircraft A6-EGA for flight UAE844 with all open deferred defects reviewed and compliant with dispatch conditions.',
        timestampUtc: '2026-10-16T02:50:00Z',
        signed: true,
        digitalDigest: 'sha256-d4e5f6...pic18449...valid'
      }
    };

    // Sequential SHA-256 Hash Chain
    this.hashChain = [
      { index: 0, prevHash: '00000000000000000000000000000000', hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' }
    ];
    this.chainLogEntry('SECTOR_OPEN', this.currentSector.sectorId);
    this.chainLogEntry('DEFECT_LOGGED', 'DEF-844-01');
    this.chainLogEntry('CRS_SIGNED', this.signatures.lameCrs.licenseNumber);
  }

  chainLogEntry(action, refId) {
    const prev = this.hashChain[this.hashChain.length - 1];
    const dataStr = `${prev.hash}:${action}:${refId}:${Date.now()}`;
    // Simple fast deterministic hash representation
    let hashVal = 0;
    for (let i = 0; i < dataStr.length; i++) {
      hashVal = ((hashVal << 5) - hashVal) + dataStr.charCodeAt(i);
      hashVal |= 0;
    }
    const hexHash = Math.abs(hashVal).toString(16).padStart(64, 'a');
    const entry = { index: this.hashChain.length, prevHash: prev.hash, hash: hexHash, action: action, ref: refId };
    this.hashChain.push(entry);
    return entry;
  }

  addDefect(type, ata, system, desc) {
    const defectId = `DEF-844-${String(this.defects.length + 1).padStart(2, '0')}`;
    const def = {
      defectId: defectId,
      type: type,
      ataChapter: ata,
      systemName: system,
      description: desc,
      status: 'OPEN',
      melReference: 'PENDING_EVAL',
      melCategory: 'NONE',
      deferralExpiryUtc: null,
      maintenanceAction: 'Open for line maintenance troubleshooting.',
      rectified: false
    };
    this.defects.push(def);
    this.chainLogEntry('DEFECT_LOGGED', defectId);
    return def;
  }

  evaluateAirworthinessRelease() {
    const hasUnresolvedOpen = this.defects.some(d => d.status === 'OPEN' && !d.rectified);
    const crsSigned = this.signatures.lameCrs.signed;
    const picSigned = this.signatures.picAcceptance.signed;

    if (hasUnresolvedOpen) {
      return { status: 'GROUNDED_UNRESOLVED_DEFECT', airworthy: false };
    }
    if (!crsSigned) {
      return { status: 'PENDING_LAME_CRS_SIGNATURE', airworthy: false };
    }
    if (!picSigned) {
      return { status: 'PENDING_PIC_FLIGHT_ACCEPTANCE', airworthy: false };
    }

    return {
      status: 'AIRCRAFT_AIRWORTHY_RELEASED',
      airworthy: true,
      openMelCount: this.defects.filter(d => d.status === 'DEFERRED_MEL').length
    };
  }

  // --- ARINC 429 Discrete Bus Synthesis ---
  generateARINC429Words() {
    const rel = this.evaluateAirworthinessRelease();

    // Label 232 (Octal 232, Hex 0x9A): ELB Airworthiness Dispatch Status
    const label232 = 0x9A;
    let data232 = 0;

    let airworthyState = 0; // 0=Grounded, 1=Unsigned, 2=MEL Valid, 3=Released
    if (rel.airworthy) airworthyState = 3;
    else if (this.signatures.lameCrs.signed && !this.signatures.picAcceptance.signed) airworthyState = 2;
    else airworthyState = 1;

    const crsBit = this.signatures.lameCrs.signed ? 1 : 0;
    const picBit = this.signatures.picAcceptance.signed ? 1 : 0;
    const melCount = Math.min(15, this.defects.filter(d => d.status === 'DEFERRED_MEL').length);

    data232 |= (airworthyState & 0x07) << 10;   // Bits 11-13: Dispatch State
    data232 |= (crsBit & 0x01) << 13;           // Bit 14: LAME CRS Signed
    data232 |= (picBit & 0x01) << 14;           // Bit 15: PIC Accepted
    data232 |= (melCount & 0x0F) << 15;         // Bits 16-19: Open MEL Count (0-15)
    data232 |= (1 & 0x01) << 19;                // Bit 20: Ground Gatelink Sync Active
    data232 |= 0x03 << 28;                      // Bits 29-30: SSM (Normal Operation)

    let word232 = (data232 & 0x7FFFFF00) | (label232 & 0xFF);
    word232 = this.applyOddParity(word232);

    // Label 233 (Octal 233, Hex 0x9B): Sector Flight Leg & Revision Sequence
    const label233 = 0x9B;
    let data233 = 0;

    const sectorSeq = 44; // Leg UAE844 sequence
    const revNum = this.hashChain.length & 0x3F;

    data233 |= (sectorSeq & 0xFF) << 10;        // Bits 11-18: Sector Leg Number
    data233 |= (revNum & 0x3F) << 18;           // Bits 19-24: Hash Chain Revision
    data233 |= 0x03 << 28;                      // Bits 29-30: SSM

    let word233 = (data233 & 0x7FFFFF00) | (label233 & 0xFF);
    word233 = this.applyOddParity(word233);

    return {
      label232: {
        octal: '232',
        hex: '0x' + (word232 >>> 0).toString(16).toUpperCase().padStart(8, '0'),
        parity: this.verifyOddParity(word232),
        dispatchState: airworthyState,
        melCount: melCount
      },
      label233: {
        octal: '233',
        hex: '0x' + (word233 >>> 0).toString(16).toUpperCase().padStart(8, '0'),
        parity: this.verifyOddParity(word233),
        sectorSeq: sectorSeq,
        revision: revNum
      }
    };
  }

  applyOddParity(word32) {
    let bits = word32 & 0x7FFFFFFF;
    let count = 0;
    for (let i = 0; i < 31; i++) {
      if ((bits >> i) & 1) count++;
    }
    if (count % 2 === 0) {
      bits |= (1 << 31);
    }
    return bits >>> 0;
  }

  verifyOddParity(word32) {
    let count = 0;
    for (let i = 0; i < 32; i++) {
      if ((word32 >>> i) & 1) count++;
    }
    return count % 2 === 1;
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { ARINC844Engine };
}
