"""大綱檢查：產生 HTML 之前，先檢查 outline.md 是否符合 CLAUDE.md 第 6 節。

檢查項目：
1. 每張投影片都要寫「頁面」，而且頁面要在 wiki/ 裡找得到
2. 內容中的年份、數字，要出現在它引用的 wiki 頁面裡
3. 內容不能太長（超過 90 個字就要拆成兩張或刪減）
4. 「最、第一、全球、大多數」這類強調詞，要在引用的 wiki 頁面裡也找得到

（第一次執行後修改：數字改成完整比對，避免 10 被當成 105,000 的一部分而誤判通過；新增第 4 項）

用法：python checks/check_outline.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
text = (ROOT / "outline.md").read_text(encoding="utf-8")
problems = []
CLAIM_WORDS = ["全球最大", "最大", "最常", "最多", "第一", "全球", "大多數", "唯一"]


def nums(t):
    return set(re.findall(r"\d[\d,]*(?:\.\d+)?", re.sub(r"[A-Za-z]+/?\d+", "", t)))

slides = re.split(r"\n## ", text)[1:]
for s in slides:
    title = s.splitlines()[0]
    pages = re.search(r"- 頁面：(.+)", s)
    content = re.search(r"- 內容：(.+)", s)
    if not pages or not content:
        problems.append((title, "格式不完整", "缺少頁面或內容"))
        continue
    names = [p.strip() for p in pages.group(1).split("、")]
    source = ""
    for n in names:
        f = WIKI / n
        if not f.exists():
            problems.append((title, "頁面不存在", n))
        else:
            source += f.read_text(encoding="utf-8")
    body = content.group(1)
    for n in sorted(nums(body) - nums(source)):  # 完整比對，不用「包含」
        problems.append((title, "數字在 wiki 找不到", n))
    for w in CLAIM_WORDS:
        if w in body and w not in source:
            problems.append((title, "強調詞沒有來源", w))
    if len(body) > 90:
        problems.append((title, "內容太長", f"{len(body)} 字"))

print(f"檢查 {len(slides)} 張投影片，發現 {len(problems)} 個問題")
for title, kind, detail in problems:
    print(f"- [{kind}] {title}：{detail}")
