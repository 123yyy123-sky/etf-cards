import json, os

# 目录由本文件位置推导（build\ 的上级），别写死。
# 2026-10-21 踩过：写死成 F:\Ai\ETF知识卡，目录搬到 F:\Ai\apps\ 之后就断了。
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tpl = open(os.path.join(ROOT, "app-template.html"), encoding="utf-8").read()
data = open(os.path.join(ROOT, "cards.json"), encoding="utf-8").read()

# 防止 JSON 里出现 </script> 提前闭合
payload = data.replace("</", "<\\/")
html = tpl.replace("__DATA__", payload)

os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
targets = [
    os.path.join(ROOT, "ETF知识卡.html"),          # 本机单文件版
    os.path.join(ROOT, "docs", "index.html"),      # GitHub Pages 发布版
]
for dest in targets:
    open(dest, "w", encoding="utf-8").write(html)
    print("written:", dest, round(os.path.getsize(dest) / 1024), "KB")

print("cards =", len(json.loads(data)["cards"]))
