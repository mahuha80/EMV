"""
EMV Course - Template builder
Generates HTML pages with consistent payment-themed UI
"""

NAV_HTML = '''<nav class="top-nav">
    <div class="nav-container">
        <a href="{base}index.html" class="nav-logo">💳 EMV Academy</a>
        <div class="nav-menu">
            <a href="{base}index.html">Trang chủ</a>
            <a href="{lpath}lesson01.html"{a1}>01</a>
            <a href="{lpath}lesson02.html"{a2}>02</a>
            <a href="{lpath}lesson03.html"{a3}>03</a>
            <a href="{lpath}lesson04.html"{a4}>04</a>
            <a href="{lpath}lesson05.html"{a5}>05</a>
            <a href="{lpath}lesson06.html"{a6}>06</a>
            <a href="{lpath}lesson07.html"{a7}>07</a>
            <a href="{lpath}lesson08.html"{a8}>08</a>
            <a href="{lpath}lesson09.html"{a9}>09</a>
            <a href="{lpath}lesson10.html"{a10}>10</a>
        </div>
    </div>
</nav>'''


def build_nav(active_lesson=0, from_index=False):
    """Build nav, mark active lesson"""
    base = '' if from_index else '../'
    lpath = 'lessons/' if from_index else ''
    attrs = {}
    for i in range(1, 11):
        attrs[f'a{i}'] = ' class="active"' if i == active_lesson else ''
    return NAV_HTML.format(base=base, lpath=lpath, **attrs)


def lesson_page(num, title, subtitle, body_html, prev_link, next_link, prev_label, next_label):
    """Generate full lesson HTML"""
    nav = build_nav(active_lesson=num)
    num_str = f"{num:02d}"
    return f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bài {num_str}: {title} — EMV Academy</title>
<link rel="stylesheet" href="../styles.css">
</head>
<body>
{nav}
<div class="container">
    <div class="lesson-header">
        <h1>Bài {num_str} · {title}</h1>
        <p class="subtitle">{subtitle}</p>
    </div>
    <div class="breadcrumb">
        <a href="../index.html">Trang chủ</a> &rsaquo; Bài {num_str}: {title}
    </div>
    <div class="lesson-content">
{body_html}
    </div>
    <div class="navigation">
        <a href="{prev_link}" class="nav-button">&larr; {prev_label}</a>
        <a href="{next_link}" class="nav-button primary">{next_label} &rarr;</a>
    </div>
</div>
</body>
</html>'''


def index_page(body_html):
    """Generate homepage HTML"""
    nav = build_nav(active_lesson=0, from_index=True)
    return f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EMV Academy — Giáo trình EMV cho Android Developer</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
{nav}
<div class="container">
    <header>
        <h1>💳 EMV Academy</h1>
        <p>Giáo trình EMV chuyên sâu dành cho lập trình viên Android</p>
    </header>
    <div class="content">
{body_html}
    </div>
</div>
</body>
</html>'''

