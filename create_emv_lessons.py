#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create full EMV course lessons 04-10
"""

import os

# Define lessons content (simplified but complete structure)
lessons = {
    4: {
        "title": "APDU Commands",
        "subtitle": "Application Protocol Data Unit",
        "sections": """
            <div class="section">
                <h2>🎯 Mục Tiêu</h2>
                <p>Hiểu APDU là gì và cách sử dụng các lệnh cơ bản: SELECT, READ RECORD, GET PROCESSING OPTIONS.</p>
            </div>
            
            <div class="section">
                <h2>📖 APDU Command Structure</h2>
                <p><strong>Command APDU:</strong> CLA | INS | P1 | P2 | Lc | Data | Le</p>
                <p><strong>Response APDU:</strong> Data | SW1 | SW2</p>
                
                <div class="code-block">
// SELECT PPSE
00 A4 04 00 0E 325041592E5359532E4444463031 00

CLA = 00 (ISO standard)
INS = A4 (SELECT)
P1  = 04 (Select by name)
P2  = 00 (First occurrence)
Lc  = 0E (14 bytes data)
Data = "2PAY.SYS.DDF01"
Le  = 00 (Max response)
                </div>
            </div>
            
            <div class="section">
                <h2>📱 Android Example</h2>
                <div class="code-block">
IsoDep isoDep = IsoDep.get(tag);
isoDep.connect();

byte[] cmd = {0x00, (byte)0xA4, 0x04, 0x00, 0x0E, ...};
byte[] response = isoDep.transceive(cmd);

// Check status
int sw1 = response[response.length-2] & 0xFF;
int sw2 = response[response.length-1] & 0xFF;

if (sw1 == 0x90 && sw2 == 0x00) {
    Log.i("APDU", "Success!");
}
                </div>
            </div>
        """
    },
    5: {
        "title": "EMV Tags & TLV",
        "subtitle": "Tag-Length-Value Encoding",
        "sections": """
            <div class="section">
                <h2>🎯 TLV Structure</h2>
                <p>TLV = Tag (định danh) + Length (độ dài) + Value (giá trị)</p>
                
                <div class="code-block">
// Example: PAN tag
5A 08 45321234 56789010

Tag    = 5A (PAN)
Length = 08 (8 bytes)
Value  = 4532123456789010
                </div>
            </div>
            
            <div class="section">
                <h2>📋 Common EMV Tags</h2>
                <table>
                    <tr><th>Tag</th><th>Name</th><th>Description</th></tr>
                    <tr><td>5A</td><td>PAN</td><td>Primary Account Number</td></tr>
                    <tr><td>5F20</td><td>Cardholder Name</td><td>Name on card</td></tr>
                    <tr><td>5F24</td><td>Expiry Date</td><td>YYMMDD format</td></tr>
                    <tr><td>9F26</td><td>Cryptogram</td><td>Application Cryptogram</td></tr>
                    <tr><td>9F27</td><td>CID</td><td>Cryptogram Info Data</td></tr>
                </table>
            </div>
        """
    },
    6: {
        "title": "Cryptography trong EMV",
        "subtitle": "RSA, DES, SHA và MAC",
        "sections": """
            <div class="section">
                <h2>🔐 RSA trong EMV</h2>
                <p>RSA được dùng cho:</p>
                <ul>
                    <li>Card authentication (SDA, DDA, CDA)</li>
                    <li>Key management</li>
                    <li>Digital signatures</li>
                </ul>
                
                <div class="info-box">
                    <p><strong>Key Sizes:</strong> 1024-bit, 2048-bit RSA</p>
                    <p><strong>Private Key:</strong> Stored in secure element</p>
                    <p><strong>Public Key:</strong> In ICC certificate</p>
                </div>
            </div>
            
            <div class="section">
                <h2>🔒 DES/3DES</h2>
                <p>Dùng cho:</p>
                <ul>
                    <li>PIN encryption</li>
                    <li>MAC generation</li>
                    <li>Session key derivation</li>
                </ul>
            </div>
        """
    },
    7: {
        "title": "Card Authentication",
        "subtitle": "SDA, DDA và CDA",
        "sections": """
            <div class="section">
                <h2>🎯 3 Phương Pháp Authentication</h2>
                
                <h3>1. SDA (Static Data Authentication)</h3>
                <ul>
                    <li>Signature tĩnh, không đổi</li>
                    <li>Security: ★★☆☆☆</li>
                    <li>Dễ implement nhất</li>
                </ul>
                
                <h3>2. DDA (Dynamic Data Authentication)</h3>
                <ul>
                    <li>Card ký challenge từ terminal</li>
                    <li>Security: ★★★★☆</li>
                    <li>Phổ biến nhất</li>
                </ul>
                
                <h3>3. CDA (Combined DDA/AC)</h3>
                <ul>
                    <li>Kết hợp DDA + Application Cryptogram</li>
                    <li>Security: ★★★★★</li>
                    <li>An toàn nhất</li>
                </ul>
            </div>
        """
    },
    8: {
        "title": "Android NFC & EMV",
        "subtitle": "Đọc Thẻ EMV Bằng NFC",
        "sections": """
            <div class="section">
                <h2>📱 Full Android Example</h2>
                
                <div class="code-block">
// AndroidManifest.xml
&lt;uses-permission android:name="android.permission.NFC"/&gt;
&lt;uses-feature android:name="android.hardware.nfc" android:required="true"/&gt;

// Activity
private NfcAdapter nfcAdapter;

@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    nfcAdapter = NfcAdapter.getDefaultAdapter(this);
}

@Override
protected void onNewIntent(Intent intent) {
    super.onNewIntent(intent);
    Tag tag = intent.getParcelableExtra(NfcAdapter.EXTRA_TAG);
    readEMVCard(tag);
}

private void readEMVCard(Tag tag) {
    IsoDep isoDep = IsoDep.get(tag);
    try {
        isoDep.connect();
        
        // 1. SELECT PPSE
        byte[] selectPPSE = hexToBytes("00A404000E325041592E5359532E44444630310");
        byte[] response = isoDep.transceive(selectPPSE);
        
        // 2. Parse response và extract AID
        String aid = parseAID(response);
        
        // 3. SELECT AID
        byte[] selectAID = buildSelectCommand(aid);
        response = isoDep.transceive(selectAID);
        
        // 4. GET PROCESSING OPTIONS
        byte[] gpo = buildGPOCommand();
        response = isoDep.transceive(gpo);
        
        // 5. READ RECORDS
        List&lt;byte[]&gt; records = readAllRecords(isoDep, parseAFL(response));
        
        // 6. Extract card data
        String pan = extractPAN(records);
        String expiry = extractExpiry(records);
        
        Log.i("EMV", "PAN: " + pan + ", Expiry: " + expiry);
        
    } catch (Exception e) {
        e.printStackTrace();
    } finally {
        try { isoDep.close(); } catch (Exception e) {}
    }
}
                </div>
            </div>
        """
    },
    9: {
        "title": "Đọc Thẻ Thực Tế",
        "subtitle": "Thực Hành Với Thẻ ATM/Credit Card",
        "sections": """
            <div class="section">
                <h2>🎯 Step-by-Step Guide</h2>
                
                <h3>Bước 1: Setup NFC Reader</h3>
                <ol>
                    <li>Enable NFC trên điện thoại</li>
                    <li>Install app NFC reader (hoặc tự code)</li>
                    <li>Chuẩn bị thẻ EMV (ATM/Credit)</li>
                </ol>
                
                <h3>Bước 2: Đọc Dữ Liệu</h3>
                <div class="warning-box">
                    <p><strong>Lưu ý:</strong> Chỉ đọc dữ liệu PUBLIC!</p>
                    <ul>
                        <li>✅ READ: PAN (masked), Expiry, Cardholder name</li>
                        <li>❌ KHÔNG ĐỌC: PIN, CVV, Full PAN</li>
                    </ul>
                </div>
                
                <h3>Bước 3: Parse & Display</h3>
                <p>Data thường thấy:</p>
                <ul>
                    <li>Card Number (6 số đầu + 4 số cuối)</li>
                    <li>Expiry Date (MM/YY)</li>
                    <li>Cardholder Name</li>
                    <li>Transaction History (max 10 giao dịch)</li>
                </ul>
            </div>
        """
    },
    10: {
        "title": "Best Practices & Security",
        "subtitle": "PCI DSS Compliance và Optimization",
        "sections": """
            <div class="section">
                <h2>🔒 Security Best Practices</h2>
                
                <h3>1. PCI DSS Compliance</h3>
                <div class="danger-box">
                    <p><strong>TUYỆT ĐỐI KHÔNG:</strong></p>
                    <ul>
                        <li>❌ Lưu trữ full PAN (không mã hóa)</li>
                        <li>❌ Lưu trữ CVV/CVV2</li>
                        <li>❌ Lưu trữ PIN hoặc PIN block</li>
                        <li>❌ Log sensitive data</li>
                    </ul>
                </div>
                
                <h3>2. Allowed Data</h3>
                <div class="success-box">
                    <p><strong>CÓ THỂ LƯU:</strong></p>
                    <ul>
                        <li>✅ Last 4 digits của PAN</li>
                        <li>✅ Expiry date</li>
                        <li>✅ Cardholder name</li>
                        <li>✅ Transaction amount, date, time</li>
                    </ul>
                </div>
                
                <h3>3. Error Handling</h3>
                <div class="code-block">
try {
    // NFC operations
} catch (TagLostException e) {
    // Card removed too early
    showError("Please keep card near phone");
} catch (IOException e) {
    // Communication error
    showError("Communication failed, try again");
} finally {
    // Always close connection
    if (isoDep != null && isoDep.isConnected()) {
        isoDep.close();
    }
}
                </div>
            </div>
            
            <div class="section">
                <h2>⚡ Performance Optimization</h2>
                <ul>
                    <li>Minimize APDU commands</li>
                    <li>Use timeout appropriately</li>
                    <li>Cache parsed data</li>
                    <li>Handle background threading</li>
                </ul>
            </div>
        """
    }
}

# Generate lessons
for lesson_num, content in lessons.items():
    filename = f"emv_course/lessons/lesson{lesson_num:02d}.html"

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bài {lesson_num}: {content['title']} - Giáo Trình EMV</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <div class="lesson-header">
            <h1>📘 Bài {lesson_num}: {content['title']}</h1>
            <p class="subtitle">{content['subtitle']}</p>
        </div>

        <div class="lesson-content">
            {content['sections']}
            
            <div class="exercise">
                <h3>🎯 Bài Tập</h3>
                <ol>
                    <li>Thực hành với code examples ở trên</li>
                    <li>Test với thẻ EMV thật (nếu có)</li>
                    <li>Research thêm về chủ đề này</li>
                </ol>
            </div>
            
            <div class="success-box">
                <h3>✅ Tóm Tắt Bài {lesson_num}</h3>
                <p>Bạn đã học xong {content['title']}. Chuyển sang bài tiếp theo!</p>
            </div>
        </div>

        <div class="navigation">
            <a href="lesson{lesson_num-1:02d}.html" class="nav-button">← Bài Trước</a>
            <a href="{'lesson' + str(lesson_num+1).zfill(2) + '.html' if lesson_num < 10 else '../index.html'}" class="nav-button">{'Bài Sau →' if lesson_num < 10 else 'Trang Chủ →'}</a>
        </div>
    </div>
</body>
</html>
"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Created lesson{lesson_num:02d}.html - {content['title']}")

print("\n🎉 All 7 lessons created successfully!")
print("Total: 10 lessons complete (1-3 already done, 4-10 now added)")

