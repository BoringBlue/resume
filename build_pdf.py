from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "resume.pdf"
PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

INK = colors.HexColor("#29253A")
MUTED = colors.HexColor("#6F687D")
PAPER = colors.HexColor("#FFFDF8")
CORAL = colors.HexColor("#FF6F69")
CORAL_FADE = colors.HexColor("#FFF0EE")
CORAL_TEXT = colors.HexColor("#C44750")
SKY = colors.HexColor("#6ECBFF")
SKY_FADE = colors.HexColor("#EEF9FF")
SKY_TEXT = colors.HexColor("#2178A6")
LINE = colors.HexColor("#D9D3C9")
WHITE = colors.white

FONT_PATH = "/System/Library/Fonts/Supplemental/Songti.ttc"
pdfmetrics.registerFont(TTFont("ResumeSong", FONT_PATH, subfontIndex=0))

BODY = ParagraphStyle("body", fontName="ResumeSong", fontSize=8.1, leading=11.5, textColor=INK)
BODY_MUTED = ParagraphStyle("body-muted", parent=BODY, textColor=MUTED)
SMALL = ParagraphStyle("small", fontName="ResumeSong", fontSize=7.1, leading=9.7, textColor=INK)
SMALL_MUTED = ParagraphStyle("small-muted", parent=SMALL, textColor=MUTED)
COMPANY = ParagraphStyle("company", fontName="ResumeSong", fontSize=14.5, leading=17.5, textColor=INK)
COMPANY_SMALL = ParagraphStyle("company-small", fontName="ResumeSong", fontSize=11.5, leading=14, textColor=INK)
PAGE_TITLE = ParagraphStyle("page-title", fontName="ResumeSong", fontSize=29, leading=33, textColor=INK)
PROJECT_TITLE = ParagraphStyle("project-title", fontName="ResumeSong", fontSize=19, leading=22, textColor=INK)
CARD_TITLE = ParagraphStyle("card-title", fontName="ResumeSong", fontSize=12.2, leading=14.5, textColor=INK)


def text(canvas: Canvas, value: str, style: ParagraphStyle, x: float, top: float, width: float) -> float:
    paragraph = Paragraph(escape(value).replace("\n", "<br/>"), style)
    _, height = paragraph.wrap(width, PAGE_H)
    paragraph.drawOn(canvas, x, top - height)
    return height


def label(canvas: Canvas, value: str, x: float, y: float, color=INK, size=7.2) -> None:
    canvas.setFillColor(color)
    canvas.setFont("ResumeSong", size)
    canvas.drawString(x, y, value)


def rule(canvas: Canvas, x1: float, y: float, x2: float, color=LINE, width=0.7) -> None:
    canvas.setStrokeColor(color)
    canvas.setLineWidth(width)
    canvas.line(x1, y, x2, y)


def card(canvas: Canvas, x: float, y: float, width: float, height: float, fill=PAPER, radius=8) -> None:
    canvas.setFillColor(fill)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.8)
    canvas.roundRect(x, y, width, height, radius, fill=1, stroke=1)


def chip(canvas: Canvas, value: str, x: float, y: float, fill=SKY_FADE, size=6.6) -> float:
    width = pdfmetrics.stringWidth(value, "ResumeSong", size) + 12
    canvas.setFillColor(fill)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.55)
    canvas.roundRect(x, y - 3, width, 13, 6.5, fill=1, stroke=1)
    label(canvas, value, x + 6, y, INK, size)
    return width


def chip_row(canvas: Canvas, values: list[str], x: float, y: float, fills=None, gap=5) -> None:
    cursor = x
    palette = fills or [CORAL_FADE, SKY_FADE]
    for index, value in enumerate(values):
        cursor += chip(canvas, value, cursor, y, palette[index % len(palette)]) + gap


def bullet_list(canvas: Canvas, items: list[str], x: float, top: float, width: float, style=BODY) -> float:
    current = top
    for item in items:
        canvas.setFillColor(CORAL)
        canvas.circle(x + 2.4, current - 5.4, 2.2, fill=1, stroke=0)
        height = text(canvas, item, style, x + 11, current, width - 11)
        current -= height + 3.5
    return current


def header(canvas: Canvas, page: int, title_text: str) -> None:
    label(canvas, "石女士  /  AI Agent 应用开发与后端工程", MARGIN, PAGE_H - 17 * mm, INK, 7.3)
    canvas.setFillColor(MUTED)
    canvas.setFont("ResumeSong", 7.3)
    canvas.drawRightString(PAGE_W - MARGIN - 18, PAGE_H - 17 * mm, title_text)
    canvas.setFillColor(CORAL if page == 1 else SKY)
    canvas.circle(PAGE_W - MARGIN - 11, PAGE_H - 15.8 * mm, 3.2, fill=1, stroke=0)
    label(canvas, f"0{page}", PAGE_W - MARGIN - 6, PAGE_H - 17 * mm, INK, 7.3)
    rule(canvas, MARGIN, PAGE_H - 21 * mm, PAGE_W - MARGIN, LINE, 0.8)


def footer(canvas: Canvas, page: int) -> None:
    rule(canvas, MARGIN, 14 * mm, PAGE_W - MARGIN, LINE, 0.7)
    label(canvas, "i@boringblue.cn  ·  130 2429 2336  ·  杭州", MARGIN, 9 * mm, MUTED, 6.8)
    label(canvas, f"PAGE 0{page} / 02", PAGE_W - MARGIN - 51, 9 * mm, MUTED, 6.8)


def page_one(canvas: Canvas) -> None:
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header(canvas, 1, "个人简介与工作经历")

    # Identity and contact.
    text(canvas, "石女士", PAGE_TITLE, MARGIN, PAGE_H - 30 * mm, 160)
    label(canvas, "AI Agent 应用开发  ·  Python 后端  ·  PHP 后端", MARGIN, PAGE_H - 48 * mm, INK, 9.2)
    label(canvas, "7 年后端开发经验", PAGE_W - MARGIN - 116, PAGE_H - 31 * mm, CORAL_TEXT, 8.3)
    label(canvas, "i@boringblue.cn", PAGE_W - MARGIN - 116, PAGE_H - 38 * mm, INK, 8.3)
    label(canvas, "130 2429 2336  ·  杭州", PAGE_W - MARGIN - 116, PAGE_H - 45 * mm, MUTED, 8.0)

    label(canvas, "PROFILE / 个人简介", MARGIN, PAGE_H - 56 * mm, CORAL_TEXT, 7.5)
    card(canvas, MARGIN, PAGE_H - 86 * mm, CONTENT_W, 24 * mm, SKY_FADE, 7)
    canvas.setFillColor(SKY)
    canvas.roundRect(MARGIN, PAGE_H - 86 * mm, 4, 24 * mm, 2, fill=1, stroke=0)
    text(
        canvas,
        "7 年后端开发经验，长期深耕电商、海外广告营销与联盟业务。熟悉从需求评审、任务拆分、开发联调、测试发布到线上排障的完整交付流程；正在使用 Python、FastAPI 和大模型能力搭建 AI Agent 业务实践。",
        BODY,
        MARGIN + 13,
        PAGE_H - 68 * mm,
        CONTENT_W - 26,
    )

    label(canvas, "EXPERIENCE / 工作经历", MARGIN, PAGE_H - 96 * mm, CORAL_TEXT, 7.5)

    # Current role.
    current_y = 327
    current_h = 221
    card(canvas, MARGIN, current_y, CONTENT_W, current_h, WHITE, 8)
    canvas.setFillColor(CORAL)
    canvas.roundRect(MARGIN, current_y, 4, current_h, 2, fill=1, stroke=0)
    chip(canvas, "CURRENT ROLE", MARGIN + 15, current_y + current_h - 22, CORAL_FADE, 6.4)
    label(canvas, "2023.11 - NOW  /  PHP 后端开发", MARGIN + 108, current_y + current_h - 18, MUTED, 7.2)
    text(canvas, "杭州多麦电子商务股份有限公司", COMPANY, MARGIN + 15, current_y + current_h - 38, CONTENT_W - 30)
    text(
        canvas,
        "海外广告营销与联盟业务平台，连接广告主与流量主，支持活动管理、合作申请、推广链接、订单归因和佣金结算。",
        SMALL_MUTED,
        MARGIN + 15,
        current_y + current_h - 61,
        CONTENT_W - 30,
    )
    bullet_list(
        canvas,
        [
            "参与后台管理系统、广告主端和流量主端的需求开发，后续主要负责流量主端业务。",
            "负责需求评审、任务拆分、排期、开发联调、测试配合、版本发布及线上问题修复。",
            "负责流量主钱包改造，覆盖多币种钱包、结算到账、提现和余额流水等核心功能。",
            "参与 Coze 智能客服对接，以及营销日历、计划、商品等业务接入大模型，支持 AI 分析与搜索。",
        ],
        MARGIN + 15,
        current_y + current_h - 91,
        CONTENT_W - 30,
        SMALL,
    )
    chip_row(canvas, ["PHP", "Phalcon", "MySQL", "ClickHouse", "Kafka", "Redis"], MARGIN + 15, current_y + 20)

    # Previous roles.
    gap = 10
    previous_w = (CONTENT_W - gap) / 2
    previous_y = 76
    previous_h = 232
    previous_roles = [
        {
            "x": MARGIN,
            "accent": SKY,
            "fill": SKY_FADE,
            "date": "2021.04 - 2023.10",
            "role": "PHP 开发工程师",
            "company": "杭州脉象健康科技有限公司",
            "context": "中医舌面、脉象信息采集与分析系统，覆盖设备端、微信端、H5 和 PC 数据展示端。",
            "bullets": [
                "参与需求分析、数据库和系统架构设计、后端开发部署，并与中医专家、算法和前端团队协作。",
                "将面相采集分析接口调用时长从约 15 秒缩短至 5 秒内，并建设服务监控、自动重启和关键接口失败预警。",
            ],
            "tags": ["PHP 8.1", "Webman", "Docker", "Nginx"],
        },
        {
            "x": MARGIN + previous_w + gap,
            "accent": CORAL,
            "fill": CORAL_FADE,
            "date": "2019.09 - 2021.04",
            "role": "PHP 开发",
            "company": "杭州云网电子商务有限公司",
            "context": "电商活动、任务协作和商家工具平台，负责设计开发、部署维护与安全优化。",
            "bullets": [
                "独立完成平台首版本从部署、设计开发到上线运行，并对接淘宝、拼多多、支付宝和微信等第三方能力。",
                "针对订单增长完成分表和存储迁移，并解决大数据量导出内存溢出问题。",
            ],
            "tags": ["PHP 7.2", "Yii 2", "MySQL", "Redis"],
        },
    ]
    for role in previous_roles:
        x = role["x"]
        card(canvas, x, previous_y, previous_w, previous_h, WHITE, 8)
        canvas.setFillColor(role["accent"])
        canvas.roundRect(x, previous_y + previous_h - 4, previous_w, 4, 2, fill=1, stroke=0)
        date_color = SKY_TEXT if role["accent"] == SKY else CORAL_TEXT
        label(canvas, role["date"], x + 14, previous_y + previous_h - 23, date_color, 7.0)
        label(canvas, role["role"], x + 14, previous_y + previous_h - 37, MUTED, 6.8)
        text(canvas, role["company"], COMPANY_SMALL, x + 14, previous_y + previous_h - 51, previous_w - 28)
        text(canvas, role["context"], SMALL_MUTED, x + 14, previous_y + previous_h - 87, previous_w - 28)
        bullet_list(canvas, role["bullets"], x + 14, previous_y + previous_h - 126, previous_w - 28, SMALL)
        chip_row(canvas, role["tags"], x + 14, previous_y + 14, [role["fill"], SKY_FADE])

    footer(canvas, 1)


def page_two(canvas: Canvas) -> None:
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header(canvas, 2, "AI 项目、项目经验与技术能力")

    text(canvas, "项目与能力", PAGE_TITLE, MARGIN, PAGE_H - 30 * mm, 220)
    label(canvas, "业务经验正在向 AI Agent 应用延伸", MARGIN, PAGE_H - 48 * mm, MUTED, 8.5)

    # AI Agent project.
    agent_y = 456
    agent_h = 224
    card(canvas, MARGIN, agent_y, CONTENT_W, agent_h, WHITE, 9)
    canvas.setFillColor(SKY)
    canvas.roundRect(MARGIN, agent_y, 4, agent_h, 2, fill=1, stroke=0)
    chip(canvas, "开发中", MARGIN + 16, agent_y + agent_h - 24, CORAL_FADE, 6.7)
    label(canvas, "PERSONAL PROJECT", MARGIN + 74, agent_y + agent_h - 20, MUTED, 6.8)
    text(canvas, "海外达人合作运营智能体", PROJECT_TITLE, MARGIN + 16, agent_y + agent_h - 43, CONTENT_W - 32)
    text(
        canvas,
        "面向海外广告营销场景，把活动需求、达人筛选和申请报价串成一条可控制、可确认的自动化流程。",
        BODY_MUTED,
        MARGIN + 16,
        agent_y + agent_h - 74,
        CONTENT_W - 32,
    )

    principle_y = agent_y + 80
    principle_gap = 12
    principle_w = (CONTENT_W - 44 - principle_gap) / 2
    for index, (title_value, detail) in enumerate([
        ("模型负责", "理解需求 · 选择工具 · 解释结果"),
        ("代码负责", "校验参数 · 计算报价 · 控制权限"),
    ]):
        x = MARGIN + 16 + index * (principle_w + principle_gap)
        canvas.setFillColor(CORAL_FADE if index == 0 else SKY_FADE)
        canvas.setStrokeColor(LINE)
        canvas.roundRect(x, principle_y, principle_w, 34, 6, fill=1, stroke=1)
        label(canvas, title_value, x + 10, principle_y + 20, CORAL_TEXT if index == 0 else SKY_TEXT, 7.0)
        label(canvas, detail, x + 10, principle_y + 8, INK, 6.7)

    flow_labels = ["活动需求", "达人筛选", "报价建议", "人工确认", "申请草稿"]
    flow_x = MARGIN + 16
    flow_y = agent_y + 24
    flow_gap = 7
    flow_w = (CONTENT_W - 32 - flow_gap * 4) / 5
    for index, value in enumerate(flow_labels):
        x = flow_x + index * (flow_w + flow_gap)
        canvas.setFillColor(CORAL_FADE if index % 2 == 0 else SKY_FADE)
        canvas.setStrokeColor(LINE)
        canvas.roundRect(x, flow_y, flow_w, 36, 6, fill=1, stroke=1)
        label(canvas, f"0{index + 1}", x + 8, flow_y + 22, MUTED, 6.2)
        label(canvas, value, x + 8, flow_y + 9, INK, 7.0)

    # Selected projects.
    label(canvas, "SELECTED PROJECTS / 项目经验", MARGIN, 438, CORAL_TEXT, 7.5)
    project_gap = 9
    project_w = (CONTENT_W - project_gap * 2) / 3
    project_y = 280
    project_h = 142
    projects = [
        ("01", "舌面脉象\n检测仪系统", "舌面、脉象采集与分析；负责数据库、接口、部署与线上优化。", "PHP · WEBMAN · VUE", SKY),
        ("02", "脉象商城\n小程序", "商城二次开发；新增页面 DIY、舌象分析与报告列表模块。", "TP6 · UNIAPP", CORAL),
        ("03", "聚客猫\nSCRM", "活动发布、智能对账和商家工具；完成支付与第三方 API 对接。", "YII 2 · MYSQL", SKY),
    ]
    for index, (number, title_value, description, stack, accent) in enumerate(projects):
        x = MARGIN + index * (project_w + project_gap)
        card(canvas, x, project_y, project_w, project_h, WHITE, 7)
        canvas.setFillColor(accent)
        canvas.roundRect(x, project_y + project_h - 4, project_w, 4, 2, fill=1, stroke=0)
        label(canvas, f"PROJECT {number}", x + 12, project_y + project_h - 21, MUTED, 6.5)
        text(canvas, title_value, CARD_TITLE, x + 12, project_y + project_h - 34, project_w - 24)
        text(canvas, description, SMALL_MUTED, x + 12, project_y + 53, project_w - 24)
        rule(canvas, x + 12, project_y + 27, x + project_w - 12, LINE, 0.6)
        label(canvas, stack, x + 12, project_y + 13, INK, 6.5)

    # Skills.
    label(canvas, "TOOLKIT / 技术能力", MARGIN, 257, CORAL_TEXT, 7.5)
    skills = [
        ("BACKEND", "PHP · Phalcon · Yii · Webman · Python · FastAPI"),
        ("DATA", "MySQL · ClickHouse · Redis · Kafka · 查询优化"),
        ("AI APPLICATION", "Coze · LLM 分析与搜索 · Function Calling · SSE"),
        ("DELIVERY", "Linux · Docker · Nginx · Git · 线上排障"),
    ]
    skill_gap = 12
    skill_w = (CONTENT_W - skill_gap) / 2
    skill_rows = [197, 145]
    for index, (name, values) in enumerate(skills):
        column = index % 2
        row = index // 2
        x = MARGIN + column * (skill_w + skill_gap)
        y = skill_rows[row]
        fill = CORAL_FADE if (index + row) % 2 == 0 else SKY_FADE
        canvas.setFillColor(fill)
        canvas.setStrokeColor(LINE)
        canvas.roundRect(x, y, skill_w, 40, 7, fill=1, stroke=1)
        label(canvas, name, x + 11, y + 24, CORAL_TEXT if fill == CORAL_FADE else SKY_TEXT, 6.5)
        text(canvas, values, SMALL, x + 11, y + 17, skill_w - 22)

    # Education.
    card(canvas, MARGIN, 72, CONTENT_W, 55, WHITE, 7)
    canvas.setFillColor(CORAL)
    canvas.roundRect(MARGIN, 72, 4, 55, 2, fill=1, stroke=0)
    label(canvas, "EDUCATION / 2015 - 2019", MARGIN + 14, 108, CORAL_TEXT, 6.8)
    label(canvas, "杭州电子科技大学信息工程学院  ·  软件工程本科", MARGIN + 14, 91, INK, 8.7)
    label(canvas, "大学英语四级  ·  杭州", PAGE_W - MARGIN - 101, 91, MUTED, 7.3)

    footer(canvas, 2)


canvas = Canvas(str(OUTPUT), pagesize=A4)
canvas.setTitle("石女士 - AI Agent 应用开发 / Python 后端 / PHP 后端")
canvas.setAuthor("石女士")
canvas.setSubject("在线简历 PDF")
page_one(canvas)
canvas.showPage()
page_two(canvas)
canvas.save()
print(OUTPUT)
