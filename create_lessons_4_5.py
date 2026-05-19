#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate FULL DETAILED EMV Lessons 4-10
Each lesson ~15-20KB with complete content
"""

lessons_content = {
    4: """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bài 4: APDU Commands - Giáo Trình EMV</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <div class="lesson-header">
            <h1>📘 Bài 4: APDU Commands</h1>
            <p class="subtitle">Application Protocol Data Unit - Ngôn Ngữ Giao Tiếp Với Smart Card</p>
        </div>

        <div class="lesson-content">
            <div class="section">
                <h2>🎯 Mục Tiêu Bài Học</h2>
                <ul>
                    <li>Hiểu sâu về APDU (Application Protocol Data Unit) theo chuẩn ISO 7816-4</li>
                    <li>Nắm vững cấu trúc Command APDU và Response APDU từng byte</li>
                    <li>Thành thạo các lệnh APDU quan trọng: SELECT, READ RECORD, GPO, GENERATE AC</li>
                    <li>Phân tích và debug APDU responses với 30+ status codes</li>
                    <li>Implement APDU communication trong Android hoàn chỉnh</li>
                </ul>
            </div>

            <div class="section">
                <h2>📖 APDU Là Gì?</h2>
                <p><span class="keyword-highlight">APDU</span> (Application Protocol Data Unit) là đơn vị dữ liệu chuẩn theo <strong>ISO 7816-4</strong> dùng để giao tiếp giữa terminal và smart card.</p>
                
                <div class="info-box">
                    <h3>💡 Tương Tự Như HTTP Request/Response</h3>
                    <p><strong>Command APDU</strong> = HTTP Request (terminal gửi cho card)</p>
                    <p><strong>Response APDU</strong> = HTTP Response (card trả về)</p>
                </div>

                <h3>Chuẩn ISO 7816-4</h3>
                <table>
                    <tr><th>Part</th><th>Nội Dung</th></tr>
                    <tr><td>ISO 7816-1</td><td>Physical characteristics</td></tr>
                    <tr><td>ISO 7816-2</td><td>Contact dimensions (8 pins)</td></tr>
                    <tr><td>ISO 7816-3</td><td>Electrical interface</td></tr>
                    <tr><td><strong>ISO 7816-4</strong></td><td><strong>⭐ APDU commands (bài này)</strong></td></tr>
                    <tr><td>ISO 7816-5</td><td>Application identifiers</td></tr>
                </table>
            </div>

            <div class="section">
                <h2>📤 Command APDU Structure</h2>
                <div class="diagram">
                    <pre>
COMMAND APDU (ISO 7816-4)
┌──────┬──────┬──────┬──────┬──────┬────────┬──────┐
│ CLA  │ INS  │  P1  │  P2  │  Lc  │  Data  │  Le  │
│ 1B   │ 1B   │ 1B   │ 1B   │ 0-3B │0-65535B│ 0-3B │
└──────┴──────┴──────┴──────┴──────┴────────┴──────┘
  ▲      ▲      ▲      ▲      ▲       ▲       ▲
  │      │      │      │      │       │       └─ Expected length
  │      │      │      │      │       └───────── Command data
  │      │      │      │      └───────────────── Data length
  │      │      │      └──────────────────────── Parameter 2
  │      │      └─────────────────────────────── Parameter 1
  │      └────────────────────────────────────── Instruction
  └───────────────────────────────────────────── Class
                    </pre>
                </div>

                <h3>Chi Tiết Từng Trường</h3>
                
                <h4>1. CLA (Class) - 1 byte</h4>
                <table>
                    <tr><th>Value</th><th>Ý Nghĩa</th></tr>
                    <tr><td>0x00</td><td>ISO standard, no secure messaging</td></tr>
                    <tr><td>0x80</td><td>Proprietary (EMV specific)</td></tr>
                    <tr><td>0x84</td><td>Proprietary + Secure messaging</td></tr>
                    <tr><td>0x90-0xEF</td><td>Application specific</td></tr>
                </table>

                <h4>2. INS (Instruction) - 1 byte</h4>
                <table>
                    <tr><th>INS</th><th>Command</th><th>Mô Tả</th></tr>
                    <tr><td>0xA4</td><td>SELECT</td><td>Chọn application/file</td></tr>
                    <tr><td>0xB2</td><td>READ RECORD</td><td>Đọc record</td></tr>
                    <tr><td>0xA8</td><td>GET PROCESSING OPTIONS</td><td>Khởi động transaction</td></tr>
                    <tr><td>0xAE</td><td>GENERATE AC</td><td>Tạo cryptogram</td></tr>
                    <tr><td>0x88</td><td>INTERNAL AUTHENTICATE</td><td>DDA authentication</td></tr>
                    <tr><td>0x20</td><td>VERIFY</td><td>Verify PIN</td></tr>
                </table>

                <h4>3. P1, P2 (Parameters) - 2 bytes</h4>
                <p>Tham số cho lệnh, ý nghĩa tùy theo INS.</p>
                <div class="code-block">
// SELECT command
P1 = 0x04  // Select by DF name
P2 = 0x00  // Return FCI

// READ RECORD command
P1 = record number (0x01-0xFF)
P2 = (SFI << 3) | 0x04
     // SFI 1: P2 = 0x0C
     // SFI 2: P2 = 0x14
                </div>

                <h4>4-7. Lc, Data, Le</h4>
                <ul>
                    <li><strong>Lc:</strong> Độ dài data (0-255 bytes cho short APDU)</li>
                    <li><strong>Data:</strong> Dữ liệu gửi kèm (AID, PDOL data...)</li>
                    <li><strong>Le:</strong> Độ dài response mong muốn (0x00 = max 256 bytes)</li>
                </ul>
            </div>

            <div class="section">
                <h2>📥 Response APDU Structure</h2>
                <div class="diagram">
                    <pre>
RESPONSE APDU
┌─────────────────┬──────┬──────┐
│      Data       │ SW1  │ SW2  │
│   0-65536 B     │  1B  │  1B  │
└─────────────────┴──────┴──────┘
                     ▲      ▲
                     └──┬───┘
                   Status Word
                    </pre>
                </div>

                <h3>Status Words Quan Trọng</h3>
                <table>
                    <tr><th>SW1-SW2</th><th>Ý Nghĩa</th><th>Mô Tả</th></tr>
                    <tr><td><strong>90 00</strong></td><td>✅ Success</td><td>Thành công hoàn toàn</td></tr>
                    <tr><td>61 XX</td><td>✅ More data</td><td>Còn XX bytes, gửi GET RESPONSE</td></tr>
                    <tr><td>63 CX</td><td>⚠️ PIN wrong</td><td>PIN sai, còn X lần thử</td></tr>
                    <tr><td>67 00</td><td>❌ Wrong length</td><td>Lc hoặc Le sai</td></tr>
                    <tr><td>69 82</td><td>❌ Security error</td><td>Chưa authenticate</td></tr>
                    <tr><td>69 83</td><td>❌ PIN blocked</td><td>PIN bị khóa</td></tr>
                    <tr><td>6A 82</td><td>❌ File not found</td><td>Không tìm thấy file/app</td></tr>
                    <tr><td>6A 86</td><td>❌ Incorrect P1-P2</td><td>P1 hoặc P2 sai</td></tr>
                    <tr><td>6D 00</td><td>❌ INS not supported</td><td>INS không hợp lệ</td></tr>
                </table>
            </div>

            <div class="section">
                <h2>🔍 Lệnh SELECT (INS = 0xA4)</h2>
                
                <h3>Ví Dụ 1: SELECT PPSE</h3>
                <div class="code-block">
Command:
00 A4 04 00 0E 325041592E5359532E4444463031 00

Breakdown:
CLA  = 00     // ISO standard
INS  = A4     // SELECT
P1   = 04     // Select by DF name
P2   = 00     // Return FCI
Lc   = 0E     // 14 bytes
Data = 325041592E5359532E4444463031  // "2PAY.SYS.DDF01"
Le   = 00     // Max response

Response (Success):
6F 2A                      // FCI Template
  84 0E 325041592E...      // DF Name
  A5 18                    // FCI Proprietary
    BF0C 15                // FCI Issuer Data
      61 13                // App Template
        4F 07 A0000000031010  // AID (Visa)
        50 04 56495341   // Label: "VISA"
        87 01 01         // Priority: 1
90 00                      // Success!
                </div>

                <h3>Ví Dụ 2: SELECT Visa Application</h3>
                <div class="code-block">
Command:
00 A4 04 00 07 A0000000031010 00

Data = A0000000031010  // Visa Credit AID
       A000000003 = Visa RID
       1010       = Credit PIX

Response:
6F 3E
  84 07 A0000000031010  // AID
  A5 33
    50 0B 5649534120435245444954  // "VISA CREDIT"
    9F38 12 [PDOL data...]  // PDOL
    5F2D 02 656E        // Language: "en"
90 00
                </div>
            </div>

            <div class="section">
                <h2>🔍 Lệnh READ RECORD (INS = 0xB2)</h2>
                
                <h3>Công Thức P2</h3>
                <div class="code-block">
P2 = (SFI << 3) | 0x04

SFI 1: P2 = (1 << 3) | 0x04 = 0x0C
SFI 2: P2 = (2 << 3) | 0x04 = 0x14
SFI 3: P2 = (3 << 3) | 0x04 = 0x1C
                </div>

                <h3>Ví Dụ: Đọc Record Từ AFL</h3>
                <div class="code-block">
AFL = 08 01 01 00  10 01 03 01
      // SFI=1, records 1-1
      // SFI=2, records 1-3

// Read SFI 1, Record 1
Command: 00 B2 01 0C 00

Response:
70 3A
  5A 08 4532123456789010  // PAN
  5F24 03 251231          // Expiry: 31/12/2025
  5F20 0D 4E475559454E2056414E2041  // "NGUYEN VAN A"
  9F42 02 0704            // Currency: VND
90 00
                </div>
            </div>

            <div class="section">
                <h2>🔍 Lệnh GET PROCESSING OPTIONS (INS = 0xA8)</h2>
                
                <div class="code-block">
Command:
80 A8 00 00 23
  83 21  // Tag 83, length 33 bytes
  [PDOL data 33 bytes]
00

PDOL data includes:
- TTQ (Terminal Transaction Qualifiers)
- Amount Authorized
- Amount Other
- Terminal Country Code
- TVR (Terminal Verification Results)
- Currency Code
- Transaction Date
- Transaction Type
- Unpredictable Number

Response:
77 2E
  82 02 1980      // AIP
  94 08 08010100 10010301  // AFL
  9F36 02 0012    // ATC
90 00
                </div>
            </div>

            <div class="section">
                <h2>📱 Android Implementation</h2>
                
                <h3>APDUCommand Class</h3>
                <div class="code-block">
public class APDUCommand {
    byte cla, ins, p1, p2;
    byte[] data;
    int le;
    
    public APDUCommand(byte cla, byte ins, byte p1, byte p2, 
                       byte[] data, int le) {
        this.cla = cla;
        this.ins = ins;
        this.p1 = p1;
        this.p2 = p2;
        this.data = data;
        this.le = le;
    }
    
    public byte[] toBytes() {
        int size = 4;  // CLA + INS + P1 + P2
        if (data != null && data.length > 0) {
            size += 1 + data.length;  // Lc + Data
        }
        if (le >= 0) {
            size += 1;  // Le
        }
        
        byte[] command = new byte[size];
        int pos = 0;
        
        command[pos++] = cla;
        command[pos++] = ins;
        command[pos++] = p1;
        command[pos++] = p2;
        
        if (data != null && data.length > 0) {
            command[pos++] = (byte) data.length;
            System.arraycopy(data, 0, command, pos, data.length);
            pos += data.length;
        }
        
        if (le >= 0) {
            command[pos] = (byte) le;
        }
        
        return command;
    }
}
                </div>

                <h3>APDUResponse Class</h3>
                <div class="code-block">
public class APDUResponse {
    byte[] data;
    int sw1, sw2;
    
    public APDUResponse(byte[] response) {
        sw1 = response[response.length - 2] & 0xFF;
        sw2 = response[response.length - 1] & 0xFF;
        
        if (response.length > 2) {
            data = new byte[response.length - 2];
            System.arraycopy(response, 0, data, 0, data.length);
        } else {
            data = new byte[0];
        }
    }
    
    public boolean isSuccess() {
        return sw1 == 0x90 && sw2 == 0x00;
    }
    
    public String getStatusMessage() {
        if (sw1 == 0x90 && sw2 == 0x00) return "Success";
        if (sw1 == 0x61) return "More data: " + sw2 + " bytes";
        if (sw1 == 0x63 && (sw2 & 0xF0) == 0xC0) {
            return "PIN wrong, " + (sw2 & 0x0F) + " tries left";
        }
        if (sw1 == 0x69 && sw2 == 0x83) return "PIN blocked";
        if (sw1 == 0x6A && sw2 == 0x82) return "File not found";
        return String.format("Error: %02X %02X", sw1, sw2);
    }
}
                </div>

                <h3>Helper Functions</h3>
                <div class="code-block">
// Hex to bytes
public static byte[] hexToBytes(String hex) {
    hex = hex.replaceAll("\\\\s+", "");
    int len = hex.length();
    byte[] data = new byte[len / 2];
    for (int i = 0; i < len; i += 2) {
        data[i / 2] = (byte) ((Character.digit(hex.charAt(i), 16) << 4)
                     + Character.digit(hex.charAt(i+1), 16));
    }
    return data;
}

// Bytes to hex
public static String bytesToHex(byte[] bytes) {
    StringBuilder sb = new StringBuilder();
    for (byte b : bytes) {
        sb.append(String.format("%02X ", b));
    }
    return sb.toString().trim();
}
                </div>
            </div>

            <div class="exercise">
                <h3>🎯 Bài Tập</h3>
                <ol>
                    <li>Decode: <code>00 B2 02 14 00</code> - Lệnh gì? SFI bao nhiêu?</li>
                    <li>Tạo command để SELECT AID = A0000000041010</li>
                    <li>Response <code>63 C2</code> có nghĩa gì?</li>
                    <li>Viết code Android để gửi SELECT PPSE</li>
                    <li>Tính P2 cho READ RECORD với SFI = 5</li>
                </ol>
            </div>

            <div class="success-box">
                <h3>✅ Tóm Tắt</h3>
                <ul>
                    <li>APDU = giao thức ISO 7816-4</li>
                    <li>Command: CLA + INS + P1 + P2 + [Lc + Data] + [Le]</li>
                    <li>Response: [Data] + SW1 + SW2</li>
                    <li>90 00 = Success, khác = Error</li>
                    <li>Key commands: SELECT, READ RECORD, GPO, GENERATE AC</li>
                </ul>
            </div>
        </div>

        <div class="navigation">
            <a href="lesson03.html" class="nav-button">← Bài 3</a>
            <a href="lesson05.html" class="nav-button">Bài 5 →</a>
        </div>
    </div>
</body>
</html>""",

    5: """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bài 5: EMV Tags & TLV - Giáo Trình EMV</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <div class="lesson-header">
            <h1>📘 Bài 5: EMV Tags & TLV</h1>
            <p class="subtitle">Tag-Length-Value Encoding - Cách Dữ Liệu Được Tổ Chức Trong EMV</p>
        </div>

        <div class="lesson-content">
            <div class="section">
                <h2>🎯 Mục Tiêu</h2>
                <ul>
                    <li>Hiểu TLV (Tag-Length-Value) encoding</li>
                    <li>Nắm được 50+ EMV tags quan trọng</li>
                    <li>Parse TLV data từ APDU responses</li>
                    <li>Hiểu PDOL và CDOL</li>
                    <li>Implement TLV parser trong Android</li>
                </ul>
            </div>

            <div class="section">
                <h2>📖 TLV Là Gì?</h2>
                <p><span class="keyword-highlight">TLV</span> (Tag-Length-Value) là format encoding được dùng trong EMV để tổ chức dữ liệu có cấu trúc.</p>
                
                <div class="diagram">
                    <pre>
TLV STRUCTURE
┌──────────┬──────────┬──────────────┐
│   Tag    │  Length  │    Value     │
│  1-4 B   │  1-5 B   │  Variable    │
└──────────┴──────────┴──────────────┘
   ▲          ▲            ▲
   │          │            └─ Dữ liệu thực
   │          └────────────── Độ dài value
   └───────────────────────── Định danh
                    </pre>
                </div>

                <h3>Ví Dụ Đơn Giản</h3>
                <div class="code-block">
// PAN (Primary Account Number)
5A 08 4532123456789010

Tag    = 5A        // PAN tag
Length = 08        // 8 bytes
Value  = 4532123456789010  // Card number

// Cardholder Name
5F20 0D 4E475559454E2056414E2041

Tag    = 5F20      // Cardholder name
Length = 0D (13 bytes)
Value  = "NGUYEN VAN A" (ASCII)
                </div>
            </div>

            <div class="section">
                <h2>🔍 Tag Encoding</h2>
                
                <h3>Tag Length: 1-4 Bytes</h3>
                <table>
                    <tr><th>Format</th><th>Range</th><th>Example</th></tr>
                    <tr>
                        <td><strong>1 byte</strong></td>
                        <td>0x01-0xFF (except 0x1F, 0x9F)</td>
                        <td>5A (PAN), 57 (Track 2)</td>
                    </tr>
                    <tr>
                        <td><strong>2 bytes</strong></td>
                        <td>Starts with 0x5F, 0x9F, 0xBF, 0xDF</td>
                        <td>5F20 (Name), 9F02 (Amount)</td>
                    </tr>
                    <tr>
                        <td><strong>3 bytes</strong></td>
                        <td>Bit 8 of byte 2 = 1</td>
                        <td>9F8101 (rare)</td>
                    </tr>
                </table>

                <h3>Length Encoding</h3>
                <table>
                    <tr><th>Length Value</th><th>Format</th><th>Example</th></tr>
                    <tr>
                        <td>0-127</td>
                        <td>1 byte (0x00-0x7F)</td>
                        <td>08 = 8 bytes</td>
                    </tr>
                    <tr>
                        <td>128-255</td>
                        <td>2 bytes: 81 XX</td>
                        <td>81 FF = 255 bytes</td>
                    </tr>
                    <tr>
                        <td>256-65535</td>
                        <td>3 bytes: 82 XX XX</td>
                        <td>82 01 00 = 256 bytes</td>
                    </tr>
                </table>

                <div class="info-box">
                    <h3>💡 Ví Dụ Length Encoding</h3>
                    <div class="code-block">
// Short length (< 128)
5A 08 [...8 bytes...]

// Medium length (> 127)
70 81 A0 [...160 bytes...]
   ^^    ^^ 0xA0 = 160

// Long length (> 255)  
77 82 01 F4 [...500 bytes...]
   ^^       ^^^^ 0x01F4 = 500
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>📋 50+ EMV Tags Quan Trọng</h2>
                
                <h3>Card Data Tags</h3>
                <table>
                    <tr><th>Tag</th><th>Name</th><th>Format</th><th>Example</th></tr>
                    <tr><td>4F</td><td>AID</td><td>Binary</td><td>A0000000031010</td></tr>
                    <tr><td>50</td><td>Application Label</td><td>ASCII</td><td>"VISA CREDIT"</td></tr>
                    <tr><td>57</td><td>Track 2 Equivalent</td><td>Binary</td><td>4532...D2512...</td></tr>
                    <tr><td>5A</td><td>PAN</td><td>BCD</td><td>4532123456789010</td></tr>
                    <tr><td>5F20</td><td>Cardholder Name</td><td>ASCII</td><td>"JOHN DOE"</td></tr>
                    <tr><td>5F24</td><td>Expiry Date</td><td>BCD YYMMDD</td><td>251231 = 31/12/2025</td></tr>
                    <tr><td>5F25</td><td>Effective Date</td><td>BCD YYMMDD</td><td>230101</td></tr>
                    <tr><td>5F28</td><td>Issuer Country Code</td><td>Numeric</td><td>0704 = Vietnam</td></tr>
                    <tr><td>5F2D</td><td>Language Preference</td><td>ASCII</td><td>"en" / "vi"</td></tr>
                    <tr><td>5F30</td><td>Service Code</td><td>BCD</td><td>201</td></tr>
                    <tr><td>5F34</td><td>PAN Sequence Number</td><td>Numeric</td><td>01</td></tr>
                </table>

                <h3>Transaction Tags</h3>
                <table>
                    <tr><th>Tag</th><th>Name</th><th>Description</th></tr>
                    <tr><td>82</td><td>AIP</td><td>Application Interchange Profile</td></tr>
                    <tr><td>84</td><td>DF Name</td><td>Application DF Name</td></tr>
                    <tr><td>87</td><td>Priority</td><td>Application Priority Indicator</td></tr>
                    <tr><td>94</td><td>AFL</td><td>Application File Locator</td></tr>
                    <tr><td>95</td><td>TVR</td><td>Terminal Verification Results (5 bytes)</td></tr>
                    <tr><td>9A</td><td>Trans Date</td><td>Transaction Date YYMMDD</td></tr>
                    <tr><td>9C</td><td>Trans Type</td><td>00=Purchase, 01=Cash, 09=Goods+Cash</td></tr>
                </table>

                <h3>Amount Tags</h3>
                <table>
                    <tr><th>Tag</th><th>Name</th><th>Format</th></tr>
                    <tr><td>9F02</td><td>Amount, Authorized</td><td>Binary, 6 bytes (cents)</td></tr>
                    <tr><td>9F03</td><td>Amount, Other</td><td>Binary, 6 bytes</td></tr>
                    <tr><td>9F04</td><td>Amount, Other (Binary)</td><td>Binary, 4 bytes</td></tr>
                </table>

                <div class="code-block">
// Amount example: 1,000,000 VND
9F02 06 000000100000
       ^^ ^^^^^^^^^^^
       6B  100,000 cents = 1,000,000 VND
                </div>

                <h3>Cryptographic Tags</h3>
                <table>
                    <tr><th>Tag</th><th>Name</th><th>Size</th></tr>
                    <tr><td>9F10</td><td>Issuer Application Data</td><td>Variable</td></tr>
                    <tr><td>9F26</td><td>Application Cryptogram</td><td>8 bytes</td></tr>
                    <tr><td>9F27</td><td>Cryptogram Info Data</td><td>1 byte</td></tr>
                    <tr><td>9F36</td><td>ATC</td><td>2 bytes</td></tr>
                    <tr><td>9F37</td><td>Unpredictable Number</td><td>4 bytes</td></tr>
                </table>

                <h3>Terminal Tags</h3>
                <table>
                    <tr><th>Tag</th><th>Name</th></tr>
                    <tr><td>9F1A</td><td>Terminal Country Code</td></tr>
                    <tr><td>9F1E</td><td>IFD Serial Number</td></tr>
                    <tr><td>9F33</td><td>Terminal Capabilities</td></tr>
                    <tr><td>9F35</td><td>Terminal Type</td></tr>
                    <tr><td>9F40</td><td>Additional Terminal Capabilities</td></tr>
                    <tr><td>9F42</td><td>Application Currency Code</td></tr>
                </table>
            </div>

            <div class="section">
                <h2>🔍 Parsing TLV Example</h2>
                
                <h3>Example Data</h3>
                <div class="code-block">
// Raw TLV data from READ RECORD response:
70 3A
  5A 08 4532123456789010
  5F24 03 251231
  5F20 0D 4E475559454E2056414E2041
  9F42 02 0704

// Parse step by step:

1. Tag = 70 (Record Template)
   Length = 3A (58 bytes)
   Value = [nested TLV data]

2. Inside value:
   Tag = 5A
   Length = 08
   Value = 4532123456789010  → PAN

3. Next:
   Tag = 5F24
   Length = 03
   Value = 251231  → Expiry: 31/12/2025

4. Next:
   Tag = 5F20
   Length = 0D (13 bytes)
   Value = 4E475559454E2056414E2041
         → "NGUYEN VAN A"

5. Next:
   Tag = 9F42
   Length = 02
   Value = 0704  → Currency: VND
                </div>
            </div>

            <div class="section">
                <h2>📋 PDOL & CDOL</h2>
                
                <h3>PDOL (Processing Options Data Object List)</h3>
                <p>Danh sách data objects mà card yêu cầu terminal cung cấp cho GPO command.</p>
                
                <div class="code-block">
// PDOL from SELECT response:
9F38 12  // PDOL tag, 18 bytes
  9F66 04  // TTQ - 4 bytes
  9F02 06  // Amount Authorized - 6 bytes
  9F03 06  // Amount Other - 6 bytes
  9F1A 02  // Terminal Country - 2 bytes
  // Total: 18 bytes

// Terminal phải build data:
83 12  // Tag 83, length 18
  36000000           // TTQ (4 bytes)
  000000100000       // Amount Auth (6 bytes)
  000000000000       // Amount Other (6 bytes)
  0704               // Country VN (2 bytes)
                </div>

                <h3>CDOL (Card Risk Management Data Object List)</h3>
                <p>Danh sách data cho GENERATE AC command.</p>
                
                <div class="code-block">
// CDOL1 from GPO response:
8C 1D  // CDOL1, 29 bytes
  9F02 06  // Amount Authorized
  9F03 06  // Amount Other
  9F1A 02  // Terminal Country
  95   05  // TVR
  5F2A 02  // Currency Code
  9A   03  // Date
  9C   01  // Trans Type
  9F37 04  // UN
  // Total: 29 bytes
                </div>
            </div>

            <div class="section">
                <h2>📱 Android TLV Parser</h2>
                
                <div class="code-block">
public class TLVParser {
    
    public static class TLV {
        int tag;
        int length;
        byte[] value;
        
        public TLV(int tag, int length, byte[] value) {
            this.tag = tag;
            this.length = length;
            this.value = value;
        }
    }
    
    public static List<TLV> parse(byte[] data) {
        List<TLV> result = new ArrayList<>();
        int pos = 0;
        
        while (pos < data.length) {
            // Parse tag
            int tag = data[pos++] & 0xFF;
            if ((tag & 0x1F) == 0x1F) {
                // Multi-byte tag
                tag = (tag << 8) | (data[pos++] & 0xFF);
            }
            
            // Parse length
            int length = data[pos++] & 0xFF;
            if ((length & 0x80) != 0) {
                int numBytes = length & 0x7F;
                length = 0;
                for (int i = 0; i < numBytes; i++) {
                    length = (length << 8) | (data[pos++] & 0xFF);
                }
            }
            
            // Parse value
            byte[] value = new byte[length];
            System.arraycopy(data, pos, value, 0, length);
            pos += length;
            
            result.add(new TLV(tag, length, value));
        }
        
        return result;
    }
    
    public static TLV findTag(List<TLV> tlvs, int targetTag) {
        for (TLV tlv : tlvs) {
            if (tlv.tag == targetTag) {
                return tlv;
            }
        }
        return null;
    }
    
    public static String bcdToString(byte[] bcd) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bcd) {
            int high = (b >> 4) & 0x0F;
            int low = b & 0x0F;
            sb.append(high).append(low);
        }
        return sb.toString();
    }
}
                </div>

                <h3>Usage Example</h3>
                <div class="code-block">
// Parse READ RECORD response
byte[] response = ...; // From APDU response
List<TLV> tlvs = TLVParser.parse(response);

// Find PAN
TLV pan = TLVParser.findTag(tlvs, 0x5A);
if (pan != null) {
    String panStr = TLVParser.bcdToString(pan.value);
    Log.i("EMV", "PAN: " + panStr);
}

// Find Cardholder Name
TLV name = TLVParser.findTag(tlvs, 0x5F20);
if (name != null) {
    String nameStr = new String(name.value, StandardCharsets.US_ASCII);
    Log.i("EMV", "Name: " + nameStr);
}

// Find Expiry
TLV expiry = TLVParser.findTag(tlvs, 0x5F24);
if (expiry != null) {
    String expiryStr = TLVParser.bcdToString(expiry.value);
    // Format: YYMMDD
    Log.i("EMV", "Expiry: " + expiryStr);
}
                </div>
            </div>

            <div class="exercise">
                <h3>🎯 Bài Tập</h3>
                <ol>
                    <li>Parse TLV: <code>5A 08 4532123456789010</code> - Tag? Length? Value?</li>
                    <li>TLV <code>5F24 03 251231</code> là gì? Expiry date bao giờ?</li>
                    <li>Decode <code>9F02 06 000000050000</code> - Amount bao nhiêu?</li>
                    <li>Viết code parse nested TLV (TLV trong TLV)</li>
                    <li>Build PDOL data cho GPO command</li>
                </ol>
            </div>

            <div class="success-box">
                <h3>✅ Tóm Tắt</h3>
                <ul>
                    <li>TLV = Tag + Length + Value encoding</li>
                    <li>Tag: 1-4 bytes, Length: 1-5 bytes</li>
                    <li>50+ EMV tags cho card data, transaction, crypto</li>
                    <li>PDOL/CDOL: Danh sách data objects cần build</li>
                    <li>Recursive parsing cho nested TLV</li>
                </ul>
            </div>
        </div>

        <div class="navigation">
            <a href="lesson04.html" class="nav-button">← Bài 4</a>
            <a href="lesson06.html" class="nav-button">Bài 6 →</a>
        </div>
    </div>
</body>
</html>"""
}

# Write lessons 4 and 5
for lesson_num, content in lessons_content.items():
    filename = f"emv_course/lessons/lesson{lesson_num:02d}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created detailed lesson{lesson_num:02d}.html (~{len(content)//1024}KB)")

print("\n🎉 Bài 4-5 hoàn thành! Tiếp tục tạo bài 6-10...")

