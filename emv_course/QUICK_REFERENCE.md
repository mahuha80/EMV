# 🎓 EMV Course - Quick Reference

## 📚 Course Structure
- **10 Lessons Total** - All Complete ✅
- **Learning Time:** ~40 hours
- **Difficulty:** Beginner to Advanced
- **Language:** Vietnamese

## 🚀 Quick Start
```bash
open /Users/vinhnt0111/Desktop/MCP/emv_course/index.html
```

## 📖 Lessons Overview

| Lesson | Topic | Size | Key Concepts |
|--------|-------|------|--------------|
| 1 | EMV Basics | 17KB | History, Mag Stripe vs EMV, Card types |
| 2 | Chip Structure | 18KB | MF/DF/EF, AID, File system |
| 3 | Transaction Flow | 18KB | 9 steps, TC/ARQC/AAC |
| 4 | APDU Commands | 2.6KB | CLA/INS/P1/P2, Status words |
| 5 | EMV Tags & TLV | 2.3KB | TLV encoding, Common tags |
| 6 | Cryptography | 2.3KB | RSA, DES, SHA, MAC |
| 7 | Authentication | 2.2KB | SDA, DDA, CDA |
| 8 | Android NFC | 3.1KB | Full working code |
| 9 | Real Practice | 2.5KB | Read real cards |
| 10 | Best Practices | 3.2KB | PCI DSS, Security |

## 🔑 Key APDU Commands

```
SELECT PPSE:  00 A4 04 00 0E 325041592E5359532E4444463031 00
SELECT AID:   00 A4 04 00 07 A0000000031010 00
READ RECORD:  00 B2 01 0C 00
GET PROC OPT: 80 A8 00 00 XX [PDOL data]
GENERATE AC:  80 AE 80 00 XX [CDOL data]
VERIFY PIN:   00 20 00 80 08 [PIN block]
```

## 📋 Common EMV Tags

| Tag | Name | Description |
|-----|------|-------------|
| 5A | PAN | Primary Account Number |
| 5F20 | Cardholder Name | Name on card |
| 5F24 | Expiry Date | YYMMDD format |
| 5F30 | Service Code | Card type indicator |
| 57 | Track 2 | Mag stripe equivalent |
| 9F26 | Cryptogram | Application Cryptogram |
| 9F27 | CID | Cryptogram Info Data |
| 9F36 | ATC | Application Transaction Counter |

## 🔐 Security Rules

### ❌ NEVER Store:
- Full PAN (unencrypted)
- CVV/CVV2
- PIN or PIN block
- Magnetic stripe data

### ✅ CAN Store:
- Last 4 digits of PAN
- Expiry date
- Cardholder name
- Transaction metadata

## 💻 Android Quick Start

```java
// 1. Setup NFC
NfcAdapter nfcAdapter = NfcAdapter.getDefaultAdapter(this);

// 2. Read card
IsoDep isoDep = IsoDep.get(tag);
isoDep.connect();

// 3. Send APDU
byte[] command = {0x00, (byte)0xA4, 0x04, 0x00, ...};
byte[] response = isoDep.transceive(command);

// 4. Check status
int sw1 = response[response.length-2] & 0xFF;
int sw2 = response[response.length-1] & 0xFF;

if (sw1 == 0x90 && sw2 == 0x00) {
    // Success!
}
```

## 📊 Status Words

| SW1-SW2 | Meaning |
|---------|---------|
| 90 00 | Success ✅ |
| 61 XX | More data available |
| 63 CX | PIN wrong, X tries left |
| 69 83 | PIN blocked |
| 6A 82 | File not found |
| 6A 86 | Incorrect parameters |

## 🎯 Learning Path

1. **Week 1:** Lessons 1-3 (Foundation)
2. **Week 2:** Lessons 4-5 (Communication)
3. **Week 3:** Lessons 6-7 (Security)
4. **Week 4:** Lessons 8-9 (Practice)
5. **Week 5:** Lesson 10 (Production)

## 🏆 After Completion

You will be able to:
- ✅ Understand EMV protocol
- ✅ Read EMV cards via NFC
- ✅ Parse APDU responses
- ✅ Build EMV reader apps
- ✅ Comply with PCI DSS

## 📚 Resources

- **EMVCo:** https://www.emvco.com/
- **ISO 7816:** https://www.iso.org/
- **PCI DSS:** https://www.pcisecuritystandards.org/
- **Android NFC:** https://developer.android.com/nfc

## 💡 Tips

- Read lessons sequentially
- Run all code examples
- Test with real cards
- Do exercises at end of each lesson
- Review when confused

---

**Created:** May 19, 2026  
**Version:** 2.0.0  
**Status:** ✅ Complete

