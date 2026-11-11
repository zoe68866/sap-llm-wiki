"""簡報檢查：HTML 做好後，用瀏覽器實際打開每一張投影片檢查。

檢查項目：
1. 投影片張數與標題要和 outline.md 一致
2. 每張投影片都要有出處（.src）
3. 內容不能超出畫面、壓到下方的出處列
4. 不能有表情符號
5. 內容下方的空白不能超過投影片高度的 30%（內容擠在上方、畫面不平衡）

（第 5 項是第一次人工看截圖後新增的：程式只檢查超出畫面，沒發現內容都擠在上方）

需要 playwright：pip install playwright && playwright install chromium
用法：python checks/check_slides.py
"""
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
outline = (ROOT / "outline.md").read_text(encoding="utf-8")
titles = [t.split(" ", 1)[1] for t in re.findall(r"\n## (\d\d .+)", outline)]
html = (ROOT / "index.html").read_text(encoding="utf-8")
problems = []

if re.search("[\\U0001F000-\\U0001FAFF\\u2600-\\u27BF\\uFE0F]", html):
    problems.append(("全部", "有表情符號"))

with sync_playwright() as p:
    page = p.chromium.launch().new_page(viewport={"width": 1320, "height": 800})
    page.goto((ROOT / "index.html").as_uri())
    n = page.locator(".slide").count()
    if n != len(titles):
        problems.append(("全部", f"投影片 {n} 張，大綱 {len(titles)} 張"))
    for k in range(n):
        page.goto((ROOT / "index.html").as_uri() + f"#{k + 1}")
        page.reload()
        info = page.evaluate("""() => {
          const s = document.querySelector('.slide.active');
          const h = s.querySelector('h1, h2');
          const src = s.querySelector('.src');
          let bottom = 0;
          s.querySelectorAll(':scope > *:not(.src), .body > *').forEach(e => {
            bottom = Math.max(bottom, e.getBoundingClientRect().bottom);
          });
          return {title: h ? h.textContent.trim() : '', hasSrc: !!src,
                  srcTop: src ? src.getBoundingClientRect().top : 0, bottom: bottom,
                  height: s.getBoundingClientRect().height};
        }""")
        no = f"{k + 1:02d}"
        if k < len(titles) and info["title"] != titles[k]:
            problems.append((no, f"標題「{info['title']}」和大綱「{titles[k]}」不同"))
        if not info["hasSrc"]:
            problems.append((no, "沒有出處"))
        elif info["bottom"] > info["srcTop"] + 1:
            problems.append((no, f"內容超出畫面 {info['bottom'] - info['srcTop']:.0f}px"))
        elif k > 0 and (info["srcTop"] - info["bottom"]) / info["height"] > 0.30:
            problems.append((no, f"下方空白 {(info['srcTop'] - info['bottom']) / info['height']:.0%}，內容擠在上方"))

print(f"檢查 {len(titles)} 張投影片，發現 {len(problems)} 個問題")
for no, kind in problems:
    print(f"- [{no}] {kind}")
