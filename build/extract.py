import os, re, json

BASE = r"F:\知识库\我的知识库"
# 输出目录由本文件位置推导（build\ 的上级），别写死。
# 2026-10-21 踩过：写死成 F:\Ai\ETF知识卡，目录搬到 F:\Ai\apps\ 之后就断了。
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

G1, G2, G3, G4, G5 = "认知地基", "路线A · 定投", "路线B · 波段", "实战工具", "基础与书架"
G6, G7 = "交易手册 · 人读", "短线"

# 分区顺序，改这里一处即可（不要在两处 sort 里各写一遍）
ORDER = [G1, G2, G3, G4, G5, G6, G7]

MAP = {
    # ---- 认知地基 ----
    "均值回归": (G1, "投资原理"), "坚实基础理论与空中楼阁理论": (G1, "投资原理"),
    "安全边际": (G1, "投资原理"), "市场先生": (G1, "投资原理"),
    "成本拖累": (G1, "投资原理"), "投资与投机之分": (G1, "投资原理"),
    "投资的第四维度": (G1, "投资原理"), "投资相对主义": (G1, "投资原理"),
    "有效市场假说": (G1, "投资原理"), "第二层次思维": (G1, "投资原理"),
    "钟摆与周期": (G1, "投资原理"), "随机漫步": (G1, "投资原理"),
    "买得好而不是买好的": (G1, "投资原理"), "回报三变量公式": (G1, "投资原理"),
    "三种漫步步伐": (G1, "投资原理"), "现代投资组合理论": (G1, "投资原理"),
    "指数化投资": (G1, "投资原理"), "安全边际读表法": (G1, "投资原理"),
    "财富转移五路径": (G1, "投资原理"),
    "风险是永久损失": (G1, "风险与心理"), "增值的不对称性": (G1, "风险与心理"),
    "防御型投资者纪律": (G1, "风险与心理"),
    "交易认知偏差": (G1, "决策与偏差"), "前景理论": (G1, "决策与偏差"),
    "后见之明与结果偏见": (G1, "决策与偏差"), "心理账户": (G1, "决策与偏差"),
    "系统1与系统2": (G1, "决策与偏差"), "外部意见预测法": (G1, "决策与偏差"),
    # ---- 路线A · 定投 ----
    "低估是一个区域": (G2, "理念与估值"), "盈利收益率定投法": (G2, "理念与估值"),
    "资产与现金流": (G2, "理念与估值"), "金鹅与瘦鹅": (G2, "理念与估值"),
    "复利三来源": (G2, "理念与估值"), "定投双核制": (G2, "理念与估值"),
    "价格围绕价值波动": (G2, "理念与估值"),
    "定投计划落纸面": (G2, "计划与执行"), "三类定投计划模板": (G2, "计划与执行"),
    "分批投入存量资金": (G2, "计划与执行"), "定投收益放大器": (G2, "计划与执行"),
    "智能定投（定期不定额）": (G2, "计划与执行"), "定投频率选择": (G2, "计划与执行"),
    "指数基金费用清单": (G2, "计划与执行"), "分红再投入与填权": (G2, "计划与执行"),
    "生命周期资产配置": (G2, "配置与择时"), "股债50-50再平衡": (G2, "配置与择时"),
    "股债差择时": (G2, "配置与择时"), "双轨并用决策": (G2, "配置与择时"),
    "安全提款率": (G2, "配置与择时"), "余钱投资三原则": (G2, "配置与择时"),
    "李大霄四大风向标": (G2, "配置与择时"), "李大霄底部五判据": (G2, "配置与择时"),
    "高估五类": (G2, "配置与择时"), "淡泊勇气坚持": (G2, "配置与择时"),
    "定投止盈三法": (G2, "止盈与策略"), "金字塔法买入策略": (G2, "止盈与策略"),
    "网格交易法": (G2, "止盈与策略"), "二八轮动策略": (G2, "止盈与策略"),
    "核心-卫星策略": (G2, "止盈与策略"),
    # ---- 路线B · 波段 ----
    "N值": (G3, "系统与规则"), "R乘数": (G3, "系统与规则"),
    "期望值": (G3, "系统与规则"), "机械交易系统": (G3, "系统与规则"),
    "唐奇安突破入场": (G3, "系统与规则"), "海龟加仓": (G3, "系统与规则"),
    "三重滤网交易系统": (G3, "系统与规则"), "短线纪律核对表": (G3, "系统与规则"),
    "路线B大样本回测": (G3, "系统与规则"), "震荡状态识别检验": (G3, "系统与规则"),
    "止跌企稳三信号": (G3, "进场信号"), "③线口径诊断": (G3, "进场信号"),
    "支撑与压力的画法": (G3, "进场信号"), "突破真假三验证": (G3, "进场信号"),
    "蜡烛图三原则": (G3, "进场信号"), "主线雷达判据验证": (G3, "进场信号"),
    "新赛道研究五步法": (G3, "进场前研究"), "厄尔尼诺顺序": (G3, "进场前研究"),
    "离场三闸门": (G3, "离场与止损"), "海龟止损": (G3, "离场与止损"),
    "海龟退出": (G3, "离场与止损"), "止损触发三问": (G3, "离场与止损"),
    "成本口径与止损基准": (G3, "离场与止损"),
    "海龟头寸规模": (G3, "资金与风险"), "资金管理四上限": (G3, "资金与风险"),
    "2%与6%法则": (G3, "资金与风险"),
    "概率思维": (G3, "心理与择时"), "概率思维训练": (G3, "心理与择时"),
    "赢家态度": (G3, "心理与择时"), "情绪风险": (G3, "心理与择时"),
    "为结果负责": (G3, "心理与择时"), "最小阻力线": (G3, "心理与择时"),
    "内幕消息陷阱": (G3, "心理与择时"), "让利润奔跑": (G3, "心理与择时"),
    "试探建仓与加码": (G3, "心理与择时"), "等待最佳时机": (G3, "心理与择时"),
    "CANSLIM选股法": (G3, "选股（成长股）"), "欧奈尔买卖纪律": (G3, "选股（成长股）"),
    "杯柄突破买点": (G3, "选股（成长股）"), "趋势持股与卖出信号清单": (G3, "选股（成长股）"),
    "投资错误清单": (G3, "选股（成长股）"), "欧奈尔成长股准则20条": (G3, "选股（成长股）"),
    # ---- 基础 ----
    "读财报看景气": (G5, "看财报"), "财务诡计识别框架": (G5, "看财报"),
    "财报排雷清单": (G5, "看财报"), "会计恒等式与三表勾稽": (G5, "看财报"),
}

TOOLS = {
    "ETF交易系统": (G4, "交易系统"), "ETF交易系统速查卡": (G4, "交易系统"),
    "进场准备模板": (G4, "模板与速查"), "离场步骤模板": (G4, "模板与速查"),
    "定投加档速查": (G4, "模板与速查"), "国债逆回购速查卡": (G4, "模板与速查"),
    "周复盘模板": (G4, "模板与速查"), "新赛道研究工作表": (G4, "模板与速查"),
    "观察池模板": (G4, "模板与速查"), "券商到价提醒模板": (G4, "模板与速查"),
    "主线雷达操作手册": (G4, "工具与数据"), "同花顺金融数据CLI": (G4, "工具与数据"),
    "行情数据源可用性": (G4, "工具与数据"), "报告预判对账": (G4, "工具与数据"),
    "ETF书籍导读": (G4, "工具与数据"),
}
TOOL_SKIP = ("判断台账", "建仓日志", "v1.17修订草案", "进场准备_2026-09-18", "复盘笔记_", "周复盘_", "观察池_2026", "ETF复盘主页")
BOOK_LIST = {"海龟交易法则","交易心理分析","股票大作手回忆录","指数基金投资指南","共同基金常识","漫步华尔街","以交易为生","期货市场技术分析","日本蜡烛图技术新解","投资最重要的事","聪明的投资者","思考快与慢","笑傲股市","李大霄投资战略","指数基金投资从入门到精通","一本书读懂财报","世界上最简单的会计书","像格雷厄姆一样读财报","手把手教你读财报","财务诡计"}


def parse_fm(txt):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", txt, re.S)
    if not m:
        return {}, txt
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" in line and not line.strip().startswith("#"):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, txt[m.end():]


def norm_status(s):
    if "已学" in s and "未学" not in s:
        return "已学"
    if "未学" in s or "待消化" in s:
        return "未学"
    if any(k in s for k in ("使用中", "进行中", "启用")):
        return "使用中"
    return "未学"


def extract_oneliner(body):
    lines = body.split("\n")
    quoted, started = [], False
    for ln in lines:
        if ln.startswith(">"):
            quoted.append(ln)
            started = True
        elif started:
            break
    if not quoted:
        return ""
    text = " ".join(q.lstrip(">").strip() for q in quoted)
    text = re.sub(r"\*\*", "", text)
    m = re.search(r"一句话[：:]\s*(.*)", text)
    if m:
        return m.group(1).strip()
    return text.strip()


def clean_body(body):
    body = re.sub(r"\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]", lambda m: m.group(1).split("/")[-1], body)
    return body.strip()


def slug(t, i):
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", t).strip("-")
    return f"{i:03d}-{s[:40]}"


cards, report = [], []
skipped = []

def add(title, rel, fm, body, cat):
    if cat is None:
        skipped.append(rel); return
    cards.append({
        "title": title, "category": cat[0], "sub": cat[1],
        "type": fm.get("type", ""), "status": norm_status(fm.get("状态", "")),
        "oneliner": extract_oneliner(body), "source": rel,
        "body": clean_body(body),
    })

for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in (".obsidian", ".trash", ".workbuddy")]
    for f in files:
        if not f.endswith(".md"):
            continue
        p = os.path.join(root, f)
        rel = os.path.relpath(p, BASE).replace("\\", "/")
        txt = open(p, encoding="utf-8").read()
        fm, body = parse_fm(txt)
        name = os.path.splitext(f)[0]
        title = fm.get("标题") or name

        if rel.startswith("07-复盘笔记/ETF/交易手册-人读/"):
            # 人读手册。必须排在下面的 07-复盘笔记/ETF/ 前面，否则会被那条吃掉
            add(title, rel, fm, body, (G6, "人读手册"))

        elif rel.startswith("07-复盘笔记/短线/"):
            if "/短线手册-人读/" in rel:
                add(title, rel, fm, body, (G7, "人读手册"))
            elif "/短线系统/" in rel:
                # 判断台账将来会填真实交易判断，仓库是公开的，不进
                if "判断台账" in name:
                    skipped.append(rel); continue
                add(title, rel, fm, body, (G7, "系统与回测"))
            # 交易记录 / 每日复盘 目前是空目录，忽略

        elif rel.startswith("07-复盘笔记/ETF/"):
            if any(k in rel for k in TOOL_SKIP):
                continue
            cat = TOOLS.get(name) or TOOLS.get(re.sub(r"（.*?）", "", title))
            add(title, rel, fm, body, cat)
        elif rel.startswith("02-来源卡/"):
            if "/笔记/" in rel:
                add(title, rel, fm, body, (G5, "ETF 与指数"))
            elif name in BOOK_LIST or fm.get("domain") == "etf":
                add(title, rel, fm, body, (G5, "书卡"))
        elif rel.startswith("03-知识/"):
            cat = MAP.get(name) or MAP.get(re.sub(r"（.*?）", "", name))
            add(title, rel, fm, body, cat)

def sort_key(c):
    """分区 → 子组 → 篇内顺序。

    两个新分区是人读手册，文件名带 00-01-02 序号，必须按文件名排。
    按标题排会乱：标题里的「先看这里」不含序号，会被汉字编码顺序甩到中间去。
    老分区沿用按标题排，不动它们的现状。
    """
    ci = ORDER.index(c["category"])
    if c["category"] in (G6, G7):
        return (ci, c["sub"], os.path.basename(c["source"]))
    return (ci, c["sub"], c["title"])


cards.sort(key=sort_key)
for c in cards:
    c["id"] = c["source"]

json.dump({"meta": {"count": len(cards)}, "cards": cards},
          open(os.path.join(OUT, "cards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

report.append(f"卡片总数: {len(cards)}")
report.append(f"JSON 大小: {os.path.getsize(os.path.join(OUT,'cards.json'))/1024:.0f} KB")
report.append(f"正文总字数: {sum(len(c['body']) for c in cards)}")
report.append(f"有一句话的卡: {sum(1 for c in cards if c['oneliner'])}/{len(cards)}")
report.append("")
report.append("=== 分组统计 ===")
from collections import Counter
gc = Counter((c["category"], c["sub"]) for c in cards)
cur = None
for (g, s), n in sorted(gc.items(), key=lambda x: (ORDER.index(x[0][0]), x[0][1])):
    if g != cur:
        report.append(f"\n【{g}】"); cur = g
    report.append(f"   {s}: {n}")
report.append("")
report.append(f"=== 未分类被跳过 ({len(skipped)}) ===")
for s in sorted(set(skipped)):
    report.append("  " + s)
report.append("")
report.append("=== 前 8 张样例 ===")
for c in cards[:8]:
    report.append(f"\n[{c['id']}] {c['title']}  ({c['category']} / {c['sub']}) [{c['type']}/{c['status']}]")
    report.append(f"   一句话: {c['oneliner'][:80]}")

# 报告写到 build\ 下，别写进 WorkBuddy 工作区（那种目录随时会被清理）
_rpt = os.path.join(OUT, "build", "extract-report.txt")
open(_rpt, "w", encoding="utf-8").write("\n".join(report))
print("done", len(cards))
print("报告:", _rpt)
# 顺便把分组统计打到屏幕上，跑 更新卡片.bat 时能直接看见
if "=== 分组统计 ===" in report:
    i = report.index("=== 分组统计 ===")
    for ln in report[i + 1:]:
        if ln.startswith("==="):
            break
        if ln.strip():
            print(ln)
