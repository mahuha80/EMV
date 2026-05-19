#!/usr/bin/env python3
import os

BASE = "/Users/vinhnt0111/Desktop/MCP/emv_course/lessons"

lessons = [
    ("lesson07", "07", "Card Authentication", "SDA, DDA, CDA", "lesson06.html", "lesson08.html"),
    ("lesson08", "08", "Android NFC", "Đọc Thẻ Android", "lesson07.html", "lesson09.html"),
    ("lesson09", "09", "Thực Hành", "Đọc Thẻ Thật", "lesson08.html", "lesson10.html"),
    ("lesson10", "10", "Best Practices", "PCI DSS", "lesson09.html", "../index.html")
]

for filename, num, title, subtitle, prev_link, next_link in lessons:
    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Bài {num}: {title}</title>
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<div class="container">
<div class="lesson-header">
<h1>Bài {num}: {title}</h1>
<p>{subtitle}</p>
</div>
<div class="lesson-content">
<p>Nội dung chi tiết...</p>
</div>
<div class="navigation">
<a href="{prev_link}">Trước</a>
<a href="{next_link}">Sau</a>
</div>
</div>
</body>
</html>"""

    with open(f"{BASE}/{filename}.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Created {filename}.html")

print("Done!")

