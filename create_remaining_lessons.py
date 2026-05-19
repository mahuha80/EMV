#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để tạo các bài học EMV còn thiếu hoặc cần sửa (lessons 3, 6-10)
"""

import os

# Base directory
BASE_DIR = "/Users/vinhnt0111/Desktop/MCP/emv_course/lessons"

# Lesson 3: Transaction Flow (fix corrupted file)
lesson03_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bài 3: Transaction Flow - Giáo Trình EMV</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <div class="lesson-header">
            <h1>📘 Bài 3: EMV Transaction Flow</h1>
            <p class="subtitle">9 Bước Xử Lý Giao Dịch EMV Chi Tiết</p>
        </div>

        <div class="lesson-content">
            <div class="section">
                <h2>🎯 Mục Tiêu Bài Học</h2>
                <ul>
                    <li>Hiểu đầy đủ flow xử lý giao dịch EMV theo chuẩn EMVCo</li>
                    <li>Nắm vững 9 bước transaction từ Application Selection đến Completion</li>
                    <li>Phân biệt online vs offline transaction chi tiết</li>
                    <li>Hiểu vai trò từng APDU command trong transaction</li>
                    <li>Biết cách terminal và card tương tác trong từng bước</li>
                </ul>
            </div>

            <div class="section">
                <h2>📊 Tổng Quan Transaction Flow</h2>
                <p>Giao dịch EMV gồm <strong>9 bước chính</strong> theo chuẩn EMVCo Book 3:</p>

                <div class="diagram">
                    <pre>
EMV TRANSACTION FLOW

┌─────────────────────────────────────────┐
│  STEP 1: APPLICATION SELECTION          │
│  Terminal tìm app trên card (SELECT)    │
└───────────────┬─────────────────────────┘
                ▼
┌─────────────────────────────────────────┐
│  STEP 2: INITIATE APPLICATION           │
│  Card khởi động app (GPO)               │
└───────────────┬─────────────────────────┘
                ▼
┌─────────────────────────────────────────┐
│  STEP 3: READ APPLICATION DATA          │
│  Đọc data từ records (READ RECORD)      │
└───────────────┬─────────────────────────┘
                ▼
┌─────────────────────────────────────────┐
│  STEP 4: DATA AUTHENTICATION            │
│  Verify card authentic (SDA/DDA/CDA)    │
└───────────────┬─────────────────────────┘
                ▼
┌─────────────────────────────────────────┐
│  STEP 5: CARDHOLDER VERIFICATION        │
│  Verify PIN, signature, biometric        │
└───────────────┬─────────────────────────┘
                ▼
┌─────────────────────────────────────────┐
│  STEP 6: TERMINAL RISK MANAGEMENT       │
│  Check amount limits, velocity           │
└───────────────┬─────────────────────────┘
                ▼
┌─────────────────────────────────────────┐
│  STEP 7: TERMINAL ACTION ANALYSIS       │
│  Decide: Approve/Decline/Go Online       │
└───────────────┬─────────────────────────┘
                ▼
┌─────────────────────────────────────────┐
│  STEP 8: CARD ACTION ANALYSIS           │
│  Card generates cryptogram (ARQC/TC/AAC) │
└───────────────┬─────────────────────────┘
                ▼
┌─────────────────────────────────────────┐
│  STEP 9: ONLINE/OFFLINE COMPLETION      │
│  Issuer authorization → Complete         │
└─────────────────────────────────────────┘
                    </pre>
                </div>
            </div>

            <div class="success-box">
                <h3>✅ Tóm Tắt Bài 3</h3>
                <ul>
                    <li>9 bước transaction: Selection → Init → Read → Auth → CVM → Risk → Terminal Action → Card Action → Completion</li>
                    <li>3 loại cryptogram: TC (offline approve), ARQC (online), AAC (decline)</li>
                    <li>Online = issuer validates, Offline = card approves</li>
                    <li>TVR + TAC quyết định transaction outcome</li>
                    <li>Card có thể override terminal decision vì security</li>
                </ul>
            </div>
        </div>

        <div class="navigation">
            <a href="lesson02.html" class="nav-button">← Bài 2: Cấu Trúc Thẻ</a>
            <a href="lesson04.html" class="nav-button">Bài 4: APDU Commands →</a>
        </div>
    </div>
</body>
</html>
"""

# Tạo từng file
with open(os.path.join(BASE_DIR, "lesson03.html"), "w", encoding="utf-8") as f:
    f.write(lesson03_content)
    print("✓ Created lesson03.html")

print("\n✅ Hoàn thành! Đã tạo lesson 3.")

