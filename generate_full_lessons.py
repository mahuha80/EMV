#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate full content for lessons 6-10"""
import os

BASE = "/Users/vinhnt0111/Desktop/MCP/emv_course/lessons"

# Store lessons content
lessons = {}

# Lesson 6: Cryptography
lessons['06'] = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bài 6: Cryptography - Giáo Trình EMV</title>
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<div class="container">
<div class="lesson-header">
<h1>📘 Bài 6: Cryptography trong EMV</h1>
<p class="subtitle">RSA, DES, SHA - Nền Tảng Bảo Mật</p>
</div>
<div class="lesson-content">
<div class="section">
<h2>🔐 Tổng Quan</h2>
<p>EMV sử dụng 3 loại encryption:</p>
<table>
<tr><th>Algorithm</th><th>Type</th><th>Use</th></tr>
<tr><td>RSA</td><td>Asymmetric</td><td>Authentication</td></tr>
<tr><td>3DES</td><td>Symmetric</td><td>PIN/Session</td></tr>
<tr><td>SHA</td><td>Hash</td><td>Integrity</td></tr>
</table>
<h3>RSA Example</h3>
<div class="code-block">
Public Key: (n, e)
Private Key: (n, d)
Signature = Hash(Data)^d mod n
</div>
<h3>Key Hierarchy</h3>
<div class="diagram"><pre>
CA (Visa/MC)
  ↓
Issuer (Bank)
  ↓  
ICC (Card)
</pre></div>
</div>
<div class="success-box">
<h3>✅ Tóm Tắt</h3>
<ul>
<li>RSA: Authentication</li>
<li>3DES: Encryption</li>
<li>SHA: Hashing</li>
</ul>
</div>
</div>
<div class="navigation">
<a href="lesson05.html" class="nav-button">← Bài 5</a>
<a href="lesson07.html" class="nav-button">Bài 7 →</a>
</div>
</div>
</body>
</html>"""

# Lesson 7: Card Authentication
lessons['07'] = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bài 7: Card Authentication - Giáo Trình EMV</title>
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<div class="container">
<div class="lesson-header">
<h1>📘 Bài 7: Card Authentication</h1>
<p class="subtitle">SDA, DDA, CDA - Xác Thực Thẻ</p>
</div>
<div class="lesson-content">
<div class="section">
<h2>🔍 3 Phương Pháp Authentication</h2>
<table>
<tr><th>Method</th><th>Security</th><th>Speed</th></tr>
<tr><td>SDA</td><td>⭐</td><td>Fast</td></tr>
<tr><td>DDA</td><td>⭐⭐⭐</td><td>Medium</td></tr>
<tr><td>CDA</td><td>⭐⭐⭐⭐⭐</td><td>Fast</td></tr>
</table>
<h3>SDA - Static Data Authentication</h3>
<p>Verify data không bị thay đổi</p>
<div class="code-block">
// Terminal verifies Issuer signature
// No dynamic challenge
</div>
<h3>DDA - Dynamic Data Authentication</h3>
<p>Card chứng minh có private key</p>
<div class="code-block">
// Terminal sends UN (Unpredictable Number)
// Card signs with private key
// Terminal verifies signature
</div>
<h3>CDA - Combined DDA/AC</h3>
<p>DDA + Cryptogram cùng lúc</p>
</div>
<div class="success-box">
<h3>✅ Tóm Tắt</h3>
<ul>
<li>SDA: Static verification</li>
<li>DDA: Dynamic challenge-response</li>
<li>CDA: Best security</li>
</ul>
</div>
</div>
<div class="navigation">
<a href="lesson06.html" class="nav-button">← Bài 6</a>
<a href="lesson08.html" class="nav-button">Bài 8 →</a>
</div>
</div>
</body>
</html>"""

# Lesson 8: Android NFC
lessons['08'] = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bài 8: Android NFC - Giáo Trình EMV</title>
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<div class="container">
<div class="lesson-header">
<h1>📘 Bài 8: Android NFC & EMV</h1>
<p class="subtitle">Lập Trình Đọc Thẻ EMV</p>
</div>
<div class="lesson-content">
<div class="section">
<h2>📱 Setup Android NFC</h2>
<h3>1. Permissions (AndroidManifest.xml)</h3>
<div class="code-block">
&lt;uses-permission android:name="android.permission.NFC" /&gt;
&lt;uses-feature android:name="android.hardware.nfc" /&gt;
</div>
<h3>2. NFC Intent Filter</h3>
<div class="code-block">
&lt;intent-filter&gt;
  &lt;action android:name="android.nfc.action.TECH_DISCOVERED" /&gt;
&lt;/intent-filter&gt;
</div>
<h3>3. Read EMV Card (Kotlin)</h3>
<div class="code-block">
val isoDep = IsoDep.get(tag)
isoDep.connect()

// SELECT PPSE
val selectPPSE = byteArrayOf(
    0x00, 0xA4.toByte(), 0x04, 0x00, 0x0E,
    // "2PAY.SYS.DDF01"
    0x32, 0x50, 0x41, 0x59, 0x2E,
    0x53, 0x59, 0x53, 0x2E,
    0x44, 0x44, 0x46, 0x30, 0x31,
    0x00
)

val response = isoDep.transceive(selectPPSE)
// Parse response...
</div>
</div>
<div class="success-box">
<h3>✅ Tóm Tắt</h3>
<ul>
<li>NFC permissions required</li>
<li>IsoDep for EMV communication</li>
<li>SELECT → GPO → READ RECORD</li>
</ul>
</div>
</div>
<div class="navigation">
<a href="lesson07.html" class="nav-button">← Bài 7</a>
<a href="lesson09.html" class="nav-button">Bài 9 →</a>
</div>
</div>
</body>
</html>"""

# Lesson 9: Practical Guide
lessons['09'] = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bài 9: Đọc Thẻ Thực Tế - Giáo Trình EMV</title>
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<div class="container">
<div class="lesson-header">
<h1>📘 Bài 9: Đọc Thẻ Thực Tế</h1>
<p class="subtitle">Hướng Dẫn Thực Hành</p>
</div>
<div class="lesson-content">
<div class="section">
<h2>🔧 Step-by-Step Guide</h2>
<h3>Bước 1: Chuẩn Bị</h3>
<ul>
<li>Device Android có NFC</li>
<li>Thẻ ATM/Credit Card</li>
<li>App đã cài NFC permissions</li>
</ul>
<h3>Bước 2: Đọc Thẻ</h3>
<ol>
<li>Mở app</li>
<li>Đặt thẻ lên mặt sau điện thoại</li>
<li>Giữ 2-3 giây</li>
<li>App sẽ đọc và hiển thị thông tin</li>
</ol>
<h3>Dữ Liệu Có Thể Đọc</h3>
<table>
<tr><th>Data</th><th>Tag</th><th>Example</th></tr>
<tr><td>PAN</td><td>5A</td><td>4532 **** **** 9010</td></tr>
<tr><td>Name</td><td>5F20</td><td>NGUYEN VAN A</td></tr>
<tr><td>Expiry</td><td>5F24</td><td>12/2025</td></tr>
<tr><td>AID</td><td>4F</td><td>Visa/Mastercard</td></tr>
</table>
<div class="warning-box">
<h3>⚠️ Lưu Ý Bảo Mật</h3>
<ul>
<li>KHÔNG lưu PAN</li>
<li>KHÔNG lưu CVV</li>
<li>Chỉ test với thẻ cá nhân</li>
</ul>
</div>
</div>
<div class="success-box">
<h3>✅ Hoàn Thành</h3>
<p>Bạn đã biết cách đọc thẻ EMV thực tế!</p>
</div>
</div>
<div class="navigation">
<a href="lesson08.html" class="nav-button">← Bài 8</a>
<a href="lesson10.html" class="nav-button">Bài 10 →</a>
</div>
</div>
</body>
</html>"""

# Lesson 10: Best Practices
lessons['10'] = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bài 10: Best Practices - Giáo Trình EMV</title>
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<div class="container">
<div class="lesson-header">
<h1>📘 Bài 10: Best Practices & Security</h1>
<p class="subtitle">PCI DSS & Production Guidelines</p>
</div>
<div class="lesson-content">
<div class="section">
<h2>🔒 PCI DSS Requirements</h2>
<h3>Data Security Standards</h3>
<table>
<tr><th>Requirement</th><th>Description</th></tr>
<tr><td>Never store PAN</td><td>Không lưu số thẻ đầy đủ</td></tr>
<tr><td>Never store CVV</td><td>Không lưu CVV/CVV2</td></tr>
<tr><td>Never store PIN</td><td>Không lưu PIN dù encrypted</td></tr>
<tr><td>Encrypt transmission</td><td>TLS 1.2+ cho network</td></tr>
</table>
<h3>What You CAN Store</h3>
<ul>
<li>✅ Masked PAN (4532 **** **** 9010)</li>
<li>✅ Expiry date</li>
<li>✅ Cardholder name</li>
<li>✅ Transaction history</li>
</ul>
<h3>What You CANNOT Store</h3>
<ul>
<li>❌ Full PAN (unmasked)</li>
<li>❌ CVV/CVV2/iCVV</li>
<li>❌ PIN (plaintext or encrypted)</li>
<li>❌ Track data (magnetic stripe)</li>
</ul>
</div>
<div class="section">
<h2>🛡️ Security Best Practices</h2>
<ol>
<li><strong>Use Tokenization:</strong> Replace PAN with token</li>
<li><strong>Encrypt at Rest:</strong> Database encryption</li>
<li><strong>Secure Communication:</strong> TLS 1.3</li>
<li><strong>Access Control:</strong> Role-based permissions</li>
<li><strong>Audit Logs:</strong> Track all access</li>
</ol>
</div>
<div class="section">
<h2>🚀 Production Deployment</h2>
<h3>Pre-Production Checklist</h3>
<ul>
<li>☐ PCI DSS compliance review</li>
<li>☐ Security audit completed</li>
<li>☐ Penetration testing done</li>
<li>☐ Error handling robust</li>
<li>☐ Logging implemented</li>
<li>☐ Documentation complete</li>
</ul>
</div>
<div class="success-box">
<h3>🎉 Chúc Mừng!</h3>
<p>Bạn đã hoàn thành khóa học EMV!</p>
<p>Bạn giờ đã biết:</p>
<ul>
<li>✅ EMV fundamentals</li>
<li>✅ Transaction flow</li>
<li>✅ APDU commands</li>
<li>✅ Cryptography</li>
<li>✅ Android implementation</li>
<li>✅ Security best practices</li>
</ul>
</div>
</div>
<div class="navigation">
<a href="lesson09.html" class="nav-button">← Bài 9</a>
<a href="../index.html" class="nav-button">Về Trang Chủ</a>
</div>
</div>
</body>
</html>"""

# Write all lessons
for num, content in lessons.items():
    filename = f"{BASE}/lesson{num}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created lesson{num}.html")

print("\n✅ Đã tạo đầy đủ nội dung bài 6-10!")

