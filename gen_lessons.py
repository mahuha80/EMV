#!/usr/bin/env python3
import os

BASE = "/Users/vinhnt0111/Desktop/MCP/emv_course/lessons"

lessons = {
    "lesson07": ("Card Authentication", "SDA, DDA, CDA", "06", "08"),
    "lesson08": ("Android NFC & EMV", "Lập Trình Đọc Th", "07", "09"),
    "lesson09": ("Đọc Thẻ Thực Tế", "Hướng Dẫn Thực Hành", "08", "10"),
    "lesson10": ("Best Practices", "PCI DSS & Security", "09", "../index")
}

for key, (title, subtitle, prev, next_) in lessons.items():
    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Bài {key[-2:]}: {title}</title>
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<div class="container">
<div class="lesson-header">
<h1>Bài {key[-2:]}: {title}</h1>
<p>{subtitle}</p>
</div>
<div class="lesson-content">
<p>Nội dung chi tiết đang được hoàn thiện...</p>
</div>
<div class="navigation">
<a href="lesson{prev}.html">Trước</a>
<a href="{'lesson' + next_ + '.html' if not next_.startswith('..') else next_ + '.html'}">Sau</a>
</div>
</div>
</body>
</html>"""

    with open(f"{BASE}/{key}.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Created {key}.html")


