#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add navigation header to all pages"""
import os
import re

BASE_DIR = "/Users/vinhnt0111/Desktop/MCP/emv_course"
LESSONS_DIR = f"{BASE_DIR}/lessons"

# Navigation header HTML
NAV_HEADER = """    <nav class="top-nav">
        <div class="nav-container">
            <a href="../index.html" class="nav-logo">🎓 EMV Course</a>
            <div class="nav-menu">
                <a href="../index.html">Trang Chủ</a>
                <a href="lesson01.html">Bài 1</a>
                <a href="lesson02.html">Bài 2</a>
                <a href="lesson03.html">Bài 3</a>
                <a href="lesson04.html">Bài 4</a>
                <a href="lesson05.html">Bài 5</a>
                <a href="lesson06.html">Bài 6</a>
                <a href="lesson07.html">Bài 7</a>
                <a href="lesson08.html">Bài 8</a>
                <a href="lesson09.html">Bài 9</a>
                <a href="lesson10.html">Bài 10</a>
            </div>
        </div>
    </nav>
"""

NAV_HEADER_INDEX = """    <nav class="top-nav">
        <div class="nav-container">
            <a href="index.html" class="nav-logo">🎓 EMV Course</a>
            <div class="nav-menu">
                <a href="index.html">Trang Chủ</a>
                <a href="lessons/lesson01.html">Bài 1</a>
                <a href="lessons/lesson02.html">Bài 2</a>
                <a href="lessons/lesson03.html">Bài 3</a>
                <a href="lessons/lesson04.html">Bài 4</a>
                <a href="lessons/lesson05.html">Bài 5</a>
                <a href="lessons/lesson06.html">Bài 6</a>
                <a href="lessons/lesson07.html">Bài 7</a>
                <a href="lessons/lesson08.html">Bài 8</a>
                <a href="lessons/lesson09.html">Bài 9</a>
                <a href="lessons/lesson10.html">Bài 10</a>
            </div>
        </div>
    </nav>
"""

# CSS for navigation
NAV_CSS = """
/* Top Navigation */
.top-nav {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-logo {
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
    padding: 15px 0;
}

.nav-logo:hover {
    opacity: 0.8;
}

.nav-menu {
    display: flex;
    gap: 5px;
    flex-wrap: wrap;
}

.nav-menu a {
    color: white;
    text-decoration: none;
    padding: 10px 15px;
    border-radius: 5px;
    transition: background 0.3s;
    font-size: 0.9rem;
}

.nav-menu a:hover {
    background: rgba(255,255,255,0.2);
}

@media (max-width: 768px) {
    .nav-container {
        flex-direction: column;
        gap: 10px;
    }
    
    .nav-menu {
        justify-content: center;
    }
    
    .nav-menu a {
        padding: 8px 10px;
        font-size: 0.85rem;
    }
}
"""

def add_nav_to_lessons():
    """Add navigation to all lesson files"""
    for i in range(1, 11):
        filename = f"{LESSONS_DIR}/lesson{i:02d}.html"
        if not os.path.exists(filename):
            continue

        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Insert nav after <body> tag
        if '<body>' in content and '<nav class="top-nav">' not in content:
            content = content.replace('<body>', f'<body>\n{NAV_HEADER}')

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Added nav to lesson{i:02d}.html")
        else:
            print(f"  lesson{i:02d}.html already has nav or missing <body> tag")

def add_nav_to_index():
    """Add navigation to index.html"""
    filename = f"{BASE_DIR}/index.html"

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    if '<body>' in content and '<nav class="top-nav">' not in content:
        content = content.replace('<body>', f'<body>\n{NAV_HEADER_INDEX}')

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ Added nav to index.html")

def update_css():
    """Add navigation styles to CSS"""
    css_file = f"{BASE_DIR}/styles.css"

    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()

    if '.top-nav' not in css_content:
        css_content += '\n' + NAV_CSS

        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        print("✓ Added navigation styles to CSS")

# Run all
print("Adding navigation headers...")
add_nav_to_lessons()
add_nav_to_index()
update_css()
print("\n✅ Navigation headers added to all pages!")

