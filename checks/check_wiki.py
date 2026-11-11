"""健檢 lint：檢查 wiki 頁面是否符合 CLAUDE.md 第 4 節的規則。

檢查項目：
1. 「## 重點」下的每一條都要有出處 [Sxx]
2. 出處代號要在 raw/ 裡找得到
3. 重點中的年份、數字要出現在它引用的 raw 原文裡
4. 每一頁都要列在 index.md（沒有孤兒頁）
5. 頁面之間的連結要能開啟
6. 只引用廠商來源的重點，要標「（廠商說法）」
7. 教學用的比喻或例子標 [比喻]，不需要出處，但也不能寫年份數字

（第 6、7 項與英文月份對照，是第一次健檢後新增的）

用法：python checks/check_wiki.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
WIKI = ROOT / "wiki"

MONTHS = {"January": "1", "February": "2", "March": "3", "April": "4", "May": "5", "June": "6", "July": "7",
          "August": "8", "September": "9", "October": "10", "November": "11", "December": "12"}


def load(p):
    t = p.read_text(encoding="utf-8")
    for en, n in MONTHS.items():  # 原文是英文月份時，也能對上中文的「12 月」
        t += " " + n if en in t else ""
    return t


raw_text = {p.name[:3]: load(p) for p in RAW.glob("S*.md")}
vendor = {k for k, t in raw_text.items() if "廠商" in t.split("## 原文重點")[0]}
index_text = (WIKI / "index.md").read_text(encoding="utf-8")
problems = []


def numbers_in(text):
    """取出年份與數字，例如 1972、105,000、2.69、20"""
    text = re.sub(r"\[S\d\d\]", "", text)
    text = re.sub(r"[A-Za-z]+/?\d+", "", text)  # 忽略 R/3、S/4HANA、ECC 6.0 這類產品名稱
    return re.findall(r"\d[\d,]*(?:\.\d+)?", text)


for page in sorted(WIKI.glob("*.md")):
    if page.name in ("index.md", "log.md"):
        continue
    text = page.read_text(encoding="utf-8")

    # 4. 孤兒頁
    if f"({page.name})" not in index_text:
        problems.append((page.name, "孤兒頁", "沒有列在 index.md"))

    # 5. 連結
    for link in re.findall(r"\]\(([^)]+\.md)\)", text):
        if not (WIKI / link).exists():
            problems.append((page.name, "壞連結", link))

    # 1~3. 重點區塊
    section = text.split("## 重點", 1)[1].split("## ", 1)[0] if "## 重點" in text else ""
    for line in section.splitlines():
        if not line.startswith("- "):
            continue
        cites = re.findall(r"\[(S\d\d)\]", line)
        short = line[2:40]
        if "[比喻]" in line:
            if numbers_in(line.replace("[比喻]", "")):
                problems.append((page.name, "比喻裡有數字", short))
            continue
        if cites and set(cites) <= vendor and "廠商說法" not in line:
            problems.append((page.name, "廠商來源未標註", short))
        if not cites:
            problems.append((page.name, "缺出處", short))
            continue
        for c in cites:
            if c not in raw_text:
                problems.append((page.name, "出處不存在", f"{c}：{short}"))
        source = "".join(raw_text.get(c, "") for c in cites)
        for n in numbers_in(line):
            if n not in source:
                problems.append((page.name, "數字對不上原文", f"{n}：{short}"))

print(f"檢查 {len(list(WIKI.glob('*.md'))) - 2} 個 wiki 頁面，發現 {len(problems)} 個問題")
for page, kind, detail in problems:
    print(f"- [{kind}] {page}：{detail}")
