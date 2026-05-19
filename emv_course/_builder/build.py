#!/usr/bin/env python3
"""Build all EMV course pages"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from template import lesson_page, index_page
from content_1_2 import INDEX_BODY, LESSON_01, LESSON_02
from content_3_5 import LESSON_03, LESSON_04, LESSON_05
from content_6_10 import LESSON_06, LESSON_07, LESSON_08, LESSON_09, LESSON_10

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
LESSONS_DIR = os.path.join(BASE, "lessons")
os.makedirs(LESSONS_DIR, exist_ok=True)

LESSONS = [
    (1,  "EMV là gì?",                 "Bối cảnh, lịch sử, các thành phần và vai trò trong hệ sinh thái thanh toán",   LESSON_01),
    (2,  "Kiến trúc thẻ EMV",          "Phần cứng chip, ISO 7816-4 file system, AID, PSE & PPSE",                       LESSON_02),
    (3,  "Transaction Flow",           "8 bước theo EMV Book 3, online vs offline, cryptogram TC/ARQC/AAC",             LESSON_03),
    (4,  "APDU Commands",              "ISO/IEC 7816-4: cấu trúc C-APDU & R-APDU, status words, các lệnh EMV",          LESSON_04),
    (5,  "BER-TLV & EMV Tags",         "BER-TLV theo ISO 7816-4 / ASN.1 BER và danh sách tag EMV thông dụng",           LESSON_05),
    (6,  "Cryptography trong EMV",     "RSA, 3DES/AES, SHA, MAC; key hierarchy CA / Issuer / ICC",                      LESSON_06),
    (7,  "Offline Data Authentication","SDA, DDA, CDA — verify certificate chain, chống clone thẻ",                     LESSON_07),
    (8,  "Android NFC + EMV",          "NfcAdapter, IsoDep, Reader Mode, gửi APDU bằng Kotlin",                         LESSON_08),
    (9,  "Demo: Đọc thẻ thật",         "Project Android hoàn chỉnh: SELECT PPSE → SELECT AID → GPO → READ RECORD",      LESSON_09),
    (10, "Bảo mật & PCI DSS",          "PCI DSS v4.0.1, tokenization, P2PE và best practice cho Android",               LESSON_10),
]


def build():
    for num, title, subtitle, body in LESSONS:
        # navigation links
        prev_num = num - 1
        next_num = num + 1
        if num == 1:
            prev_link, prev_label = "../index.html", "Trang chủ"
        else:
            prev_link = f"lesson{prev_num:02d}.html"
            prev_label = f"Bài {prev_num:02d}"
        if num == 10:
            next_link, next_label = "../index.html", "Hoàn tất khóa học"
        else:
            next_link = f"lesson{next_num:02d}.html"
            next_label = f"Bài {next_num:02d}"

        html = lesson_page(num, title, subtitle, body, prev_link, next_link, prev_label, next_label)
        path = os.path.join(LESSONS_DIR, f"lesson{num:02d}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✓ lesson{num:02d}.html ({len(html):,} chars)")

    # index
    idx_html = index_page(INDEX_BODY)
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(idx_html)
    print(f"  ✓ index.html ({len(idx_html):,} chars)")


if __name__ == "__main__":
    print(f"Building EMV course in {BASE}…")
    build()
    print("Done.")

