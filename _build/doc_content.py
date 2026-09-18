# -*- coding: utf-8 -*-
"""Executive-memo content for gstack Tutorial No.4's Word document.

Follows gstack-tutorial-3's actual precedent (see that project's own
_build/doc_content.py): this is a SEPARATE, shorter, hand-authored
executive-memo content module, NOT a literal Markdown-to-DOCX conversion of
TUTORIAL.md. The Markdown tutorial is the comprehensive learner document;
this is the compressed course-note / executive companion. Consistency
between the two is checked mechanically (see _build/verify_doc_structure.py
and docs/TUTORIAL_4_DOCUMENT_MANIFEST.md's provenance table), not by
generating one from the other.

Reuses the L(en, zh) / pick() bilingual pattern from deck_content.py so this
module's own EN/ZH content cannot drift apart in structure.

Source policy (per docs/TUTORIAL_4_PRIVACY_REVIEW.md): every claim traces to
reviews/, docs/external_ai_mentor.md, PLAN.md, TUTORIAL.md, TODOS.md, or
README.md. ChatGPT-gstack-20260917.pdf is private source only -- never
quoted or embedded. No invented metrics; unverified items are named as such.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from deck_content import L, pick  # noqa: F401  (re-exported for build_docx.py)

DOC = {
    "kicker": L("gstack Tutorial No. 4", "gstack 教程 #4"),
    "title": L(
        "From AI Planning to Working Production Software",
        "从 AI 规划到可用的生产级软件",
    ),
    "subtitle": L(
        "An executive memo on running a second, independent AI as a review "
        "and prompt-drafting layer above gstack's specialist roles",
        "关于在 gstack 专业角色之上运行第二个独立 AI 作为复核与提示词起草层的"
        "高管备忘录",
    ),
    "meta": [
        L("Educational engineering case study", "教育性工程案例研究"),
        L(
            "Companion document to TUTORIAL.md / TUTORIAL.zh.md "
            "(the full walkthrough)",
            "配套文档，完整版见 TUTORIAL.md / TUTORIAL.zh.md",
        ),
        L(
            "No private identifiers appear in this document -- see "
            "docs/TUTORIAL_4_DOCUMENT_PRIVACY_CHECK.md",
            "本文档不含任何私人标识信息——见 "
            "docs/TUTORIAL_4_DOCUMENT_PRIVACY_CHECK.md",
        ),
    ],
    "exec_heading": L("Executive Summary", "执行摘要"),
    "exec_paras": [
        L(
            "This memo summarizes how a real application -- a tweet "
            "screenshot tool -- was planned, reviewed, built, tested, and "
            "shipped to production using gstack's specialist AI roles, plus "
            "one addition: a second, independent AI in a separate session "
            "whose only job was translating gstack's raw output into the "
            "next precise instruction.",
            "本备忘录总结了一个真实应用——推文截图工具——如何借助 gstack "
            "的专业 AI 角色，外加一项新增机制，完成规划、复核、构建、测试并"
            "上线生产环境：一个独立会话中运行的第二个 AI，其唯一职责是把 "
            "gstack 的原始输出翻译成下一条精确指令。",
        ),
        L(
            "The project's own record is used as evidence, not narrative "
            "color: a five-review audit trail, a mandatory high-risk spike "
            "that caught a silent-wrong-output bug no automated check would "
            "have found, and an honest disclosure of every known "
            "limitation that shipped with V1.",
            "本项目自身的记录被用作证据，而不是叙事装饰：一条五轮复核的"
            "审计轨迹、一次强制性的高风险验证性小试（它抓到了一个任何自动化"
            "检查都无法发现的静默错误输出 bug），以及对随 V1 一同上线的每一"
            "项已知局限的坦诚披露。",
        ),
        L(
            "The full teaching material -- nineteen Parts, a troubleshooting "
            "section, and three appendices -- lives in TUTORIAL.md and its "
            "Chinese counterpart. This memo is deliberately shorter: it "
            "exists for a reader who wants the shape of the system and its "
            "headline evidence, not the full walkthrough.",
            "完整的教学材料——十九个部分、一个故障排查章节、三个附录——收录"
            "在 TUTORIAL.md 及其中文版中。本备忘录刻意更短：它面向那些只想"
            "了解这套体系的整体轮廓和关键证据、而不需要完整走一遍教程的"
            "读者。",
        ),
    ],
    "metrics_heading": L("At a Glance", "概览数据"),
    "metrics_caption": L(
        "Every figure below is a direct count from this project's own "
        "review files -- none is estimated or rounded for effect.",
        "以下每一项数字都是从本项目自身的复核文件中直接统计得出——没有一项"
        "是估算或为了效果而取整的。",
    ),
    "metrics_headers": [L("Metric", "指标"), L("Value", "数值")],
    "metrics_rows": [
        [L("Development stages run (of 16 defined)", "运行的开发阶段数（共 16 阶段）"), L("15", "15")],
        [L("CEO review findings resolved individually", "CEO 复核中逐一解决的发现项"), L("25", "25")],
        [L("Independent-review cross-model tensions found", "独立复核发现的跨模型张力"), L("8", "8")],
        [L("...accepted / softened / skipped", "……其中采纳 / 软化 / 跳过"), L("6 / 1 / 1", "6 / 1 / 1")],
        [L("Engineering-review findings (B1-B5)", "工程复核发现项（B1-B5）"), L("5", "5")],
        [L("...classified BLOCKER", "……分类为阻断项"), L("1 (B1)", "1（B1）")],
        [L("Evidence Ladder levels defined", "证据阶梯层级数"), L("10", "10")],
        [L("Core production flows verified", "已验证的核心生产流程"), L("2 (single tweet, thread)", "2（单推文、Thread）")],
        [L("Known limitations disclosed at ship", "上线时披露的已知局限"), L("5", "5")],
        [L("Human-only authorization gates", "仅限人类操作的授权关卡"), L("2", "2")],
    ],
    "toc_heading": L("Contents", "目录"),
    "toc": [
        L("Operating Model", "运营模型"),
        L("Product and Architecture", "产品与架构"),
        L("Review System", "复核体系"),
        L("The High-Risk Spike (T1.5)", "高风险验证性小试（T1.5）"),
        L("The Evidence Ladder", "证据阶梯"),
        L("AI and Human Responsibilities", "AI 与人类的职责划分"),
        L("Browser QA and Human-in-the-Loop Testing", "浏览器 QA 与人机协同测试"),
        L("Rapid Finalization", "快速收尾"),
        L("Production Outcome", "生产环境结果"),
        L("Known Limitations", "已知局限"),
        L("Reusable Workflow", "可复用工作流"),
        L("Key Lessons", "关键教训"),
        L("Metrics and Evidence Summary", "指标与证据总结"),
        L("Tutorial 4.1: Post-Launch Iteration", "教程 4.1：上线之后的迭代"),
        L("Definition of Done and Release Status", "完成定义与发布状态"),
    ],
    "sections": [
        {
            "title": L("Operating Model", "运营模型"),
            "blocks": [
                ("p", L(
                    "\"AI writes code\" describes one stage out of nineteen "
                    "this project actually ran. The real loop places a "
                    "second, independent AI -- the External AI Mentor -- "
                    "above gstack's own specialist roles, translating each "
                    "stage's raw output into the next stage's precision "
                    "prompt, with a human gate after every stage.",
                    "\"AI 写代码\"描述的只是本项目实际运行的十九个阶段中的"
                    "一个。真正的循环是在 gstack 自身的专业角色之上，运行"
                    "第二个独立的 AI——外部 AI 导师——把每个阶段的原始输出"
                    "翻译成下一阶段的精确提示词，并在每个阶段之后设置人工"
                    "关卡。",
                )),
                ("code", [
                    "Human -> External AI Mentor -> optimized prompt",
                    "      -> gstack specialist role -> evidence",
                    "      -> human gate -> next stage",
                ]),
                ("p", L(
                    "Full detail on this pattern, including four sourced "
                    "examples of the mentor correcting a real error, is in "
                    "docs/external_ai_mentor.md.",
                    "关于这一模式的完整细节，包括导师纠正真实错误的四个有"
                    "据可查的实例，见 docs/external_ai_mentor.md。",
                )),
            ],
        },
        {
            "title": L("Product and Architecture", "产品与架构"),
            "blocks": [
                ("p", L(
                    "The Tweet Screenshot Tool: paste a tweet URL, render a "
                    "pixel-accurate live preview, customize it, export as "
                    "PNG, clipboard image, or a shareable link. A second "
                    "mode assembles a manual thread and exports one "
                    "combined image. V1 shipped both, on Next.js, deployed "
                    "to Vercel.",
                    "推文截图工具：粘贴一条推文链接，渲染出像素级还原的"
                    "实时预览，进行自定义，导出为 PNG、剪贴板图片或可分享"
                    "链接。第二种模式手动组装一个 thread，导出为一张合并"
                    "图片。V1 两种模式均已上线，基于 Next.js，部署在 "
                    "Vercel。",
                )),
                ("table",
                 [L("Component", "组件"), L("Role", "角色")],
                 [
                     [L("react-tweet", "react-tweet"), L("Fetches via X's free public syndication endpoint", "通过 X 的免费公共联合供稿端点抓取")],
                     [L("/api/tweet/[id]", "/api/tweet/[id]"), L("Server-side hop -- required because the endpoint blocks browser CORS", "服务端中转——因为该端点会阻止浏览器 CORS 请求")],
                     [L("modern-screenshot", "modern-screenshot"), L("DOM to PNG export, only at capture time", "DOM 转 PNG 导出，仅在捕获时使用")],
                     [L("/api/image-proxy", "/api/image-proxy"), L("SSRF-hardened; only needed for export, not live preview", "经过 SSRF 加固；仅导出需要，实时预览不需要")],
                 ],
                 [3, 4]),
                ("callout", L(
                    "No paid API was used anywhere in this architecture -- "
                    "verified live before the architecture was chosen, not "
                    "assumed.",
                    "本架构中任何环节都未使用付费 API——这是在选定架构之前"
                    "实际验证过的，不是假设。",
                )),
            ],
        },
        {
            "title": L("Review System", "复核体系"),
            "blocks": [
                ("p", L(
                    "Five reviews, each producing individually-resolved "
                    "findings rather than a batch approval: AI CEO (scope, "
                    "positioning), Security and UX (embedded in the CEO "
                    "review), Independent Second Opinion (8 cross-model "
                    "tensions), Engineering Review (5 findings, B1 a "
                    "blocker), and Ship / DevOps.",
                    "五轮复核，每一轮都产出逐一解决的发现项，而不是批量"
                    "通过：AI CEO（范围、定位）、安全与 UX（嵌入 CEO "
                    "复核中）、独立第二意见（8 项跨模型张力）、工程复核"
                    "（5 项发现，B1 为阻断项）、以及上线 / DevOps。",
                )),
                ("h2", L("A stated gap", "一个明确声明的缺口")),
                ("p", L(
                    "No dedicated Project Manager role ran separately -- "
                    "the CEO review's own task breakdown covered the "
                    "function. Recorded as a stated gap, not silently "
                    "absorbed.",
                    "没有单独运行专门的项目经理角色——CEO 复核自身的任务"
                    "拆解承担了这一职能。这被记录为明确声明的缺口，而不是"
                    "被悄悄吸收。",
                )),
            ],
        },
        {
            "title": L("The High-Risk Spike (T1.5)", "高风险验证性小试（T1.5）"),
            "blocks": [
                ("p", L(
                    "The engineering review's single most consequential "
                    "finding (B1): the planned image-proxy fix had never "
                    "actually been wired to any real DOM element. A "
                    "mandatory spike was inserted before broad "
                    "implementation to resolve this with real code.",
                    "工程复核中最具实质影响的单一发现（B1）：计划中的图片"
                    "代理修复其实从未真正接到任何真实的 DOM 元素上。在大规模"
                    "实现之前插入了一次强制性的验证性小试，用真实代码解决"
                    "这个问题。",
                )),
                ("code", [
                    "Assumption:  the fix should just work once wired up",
                    "Experiment:  read the library's real compiled source",
                    "Result:      \"success\" -- no exception thrown",
                    "Bug found:   exported avatar showed a broken-image icon",
                    "Root cause:  a blob: URL doesn't survive re-loading",
                    "             inside modern-screenshot's cloned SVG",
                    "Fix:         a self-contained base64 data: URL",
                    "Proof:       corrected PNG read directly -- avatar",
                    "             correct; capture time 1046ms -> 468ms",
                ]),
                ("callout", L(
                    "Successful execution is not proof of correct output.",
                    "执行成功不等于输出正确。",
                )),
            ],
        },
        {
            "title": L("The Evidence Ladder", "证据阶梯"),
            "blocks": [
                ("p", L(
                    "Ten levels, idea through human production test. The "
                    "avatar bug hid at level 5 (\"local browser succeeds\") "
                    "-- a level that looks like proof and usually isn't. "
                    "Nothing below level 7 (an exported artifact actually "
                    "inspected) counted as evidence for a pixel-generation "
                    "feature in this project.",
                    "十个层级，从想法到生产环境人工测试。头像 bug 藏在"
                    "第 5 层（\"本地浏览器跑通了\"）——这一层看起来像证据，"
                    "但通常不是。在本项目中，对于一个像素生成类功能，第 7 "
                    "层以下（导出产物经过实际检查）不算作证据。",
                )),
                ("table",
                 [L("Level", "层级"), L("What it removes uncertainty about", "消除的不确定性")],
                 [
                     [L("5. Local browser \"succeeds\"", "5. 本地浏览器\"跑通了\""), L("The trap -- looks like proof, usually isn't", "陷阱——看起来像证据，通常不是")],
                     [L("7. Exported artifact inspected", "7. 导出产物经过检查"), L("What actually caught the avatar bug", "实际抓到头像 bug 的那一层")],
                     [L("10. Human production test", "10. 生产环境人工测试"), L("Whether the shipped thing holds up", "真正上线的东西是否经得住考验")],
                 ],
                 [3, 4]),
            ],
        },
        {
            "title": L("AI and Human Responsibilities", "AI 与人类的职责划分"),
            "blocks": [
                ("bullets", [
                    (L("AI:", "AI："), L(
                        "Analysis, implementation, repeatable and "
                        "exhaustive verification, drafting review findings",
                        "分析、实现、可重复且详尽的验证、起草复核发现",
                    )),
                    (L("Human:", "人类："), L(
                        "Judgment, account authorization, the ship decision "
                        "-- every one of these stayed a human gate, no "
                        "exception this project made",
                        "判断、账户授权、上线决策——这些始终是人工关卡，"
                        "本项目没有任何例外",
                    )),
                ]),
            ],
        },
        {
            "title": L("Browser QA and Human-in-the-Loop Testing", "浏览器 QA 与人机协同测试"),
            "blocks": [
                ("p", L(
                    "Three separate evidence layers: automated tests "
                    "(deterministic logic), AI browser QA via Aside (real "
                    "application behavior in a real browser), and human "
                    "testing (usability and perceived correctness). None "
                    "substitutes for another.",
                    "三个独立的证据层：自动化测试（确定性逻辑）、通过 "
                    "Aside 完成的 AI 浏览器 QA（真实浏览器中的真实应用"
                    "行为）、以及人工测试（可用性与主观正确性感受）。三者"
                    "互不可替代。",
                )),
                ("p", L(
                    "Reported by the user, not independently verifiable by "
                    "the AI: local testing (dev server, Aside, exported PNG "
                    "visually inspected) and production testing (deployed "
                    "Vercel URL, core flow repeated and confirmed).",
                    "由用户报告，AI 无法独立验证——正是这一点使其有意义："
                    "本地测试（开发服务器、Aside、导出的 PNG 经过视觉检查）"
                    "和生产环境测试（已部署的 Vercel URL，重复核心流程并"
                    "确认）。",
                )),
            ],
        },
        {
            "title": L("Rapid Finalization", "快速收尾"),
            "blocks": [
                ("p", L(
                    "A deliberate mode switch from \"investigate "
                    "everything\" to \"fix release-critical issues, "
                    "document the rest, ship.\" Triggered by an External AI "
                    "Mentor intervention after a debugging session ran long "
                    "with no isolated root cause.",
                    "从\"调查一切\"到\"修复上线关键问题、记录其余问题、"
                    "然后上线\"的刻意模式切换。由外部 AI 导师在一次调试"
                    "会话跑了很久却未孤立出根本原因后进行的一次干预所触发。",
                )),
                ("table",
                 [L("Fix now", "立即修复"), L("Defer, documented", "推迟，记录在案")],
                 [
                     [L("Build failures, crashes", "构建失败、崩溃"), L("Minor styling", "细枝末节的样式问题")],
                     [L("Core export failure", "核心导出失败"), L("Speculative refactors", "投机性重构")],
                     [L("Serious security issues", "严重安全问题"), L("V2 functionality", "V2 功能")],
                 ],
                 [3.25, 3.25]),
            ],
        },
        {
            "title": L("Production Outcome", "生产环境结果"),
            "blocks": [
                ("p", L(
                    "Both core flows -- single tweet and thread -- verified "
                    "working against the live deployed URL via real-browser "
                    "automation and human confirmation. No fatal console "
                    "errors observed in the tested flows.",
                    "两条核心流程——单推文和 thread——均通过真实浏览器自动化"
                    "和人工确认，针对已部署的线上 URL 验证可用。在已测试的"
                    "流程中未观察到致命的控制台错误。",
                )),
                ("p", L(
                    "Deployment used npx vercel (no global CLI install); "
                    "account login and authorization were performed by a "
                    "human, in their own terminal and browser, before the "
                    "AI completed the deployment sequence.",
                    "部署使用 npx vercel（无需全局安装 CLI）；账户登录和"
                    "授权由人类在自己的终端和浏览器中完成，之后 AI 才完成"
                    "余下的部署流程。",
                )),
            ],
        },
        {
            "title": L("Known Limitations", "已知局限"),
            "blocks": [
                ("table",
                 [L("Item", "项目"), L("Status", "状态")],
                 [
                     [L("Rate limiting on public API routes", "公共 API 路由的限流"), L("Planned, reviewed twice, never implemented", "已计划，复核过两次，从未实现")],
                     [L("Thread share-link style restoration", "Thread 分享链接样式恢复"), L("Known bug, root cause not found", "已知 bug，根本原因未找到")],
                     [L("Video / emoji / multi-image export", "视频 / emoji / 多图导出"), L("Implemented, not empirically verified", "已实现，未经实证验证")],
                     [L("Safari / iOS clipboard", "Safari / iOS 剪贴板"), L("Implemented, not verified on real Safari", "已实现，未在真实 Safari 上验证")],
                     [L("Automated test suite", "自动化测试套件"), L("Not written -- a stated process gap", "未编写——一个明确声明的流程缺口")],
                 ],
                 [3.5, 3]),
                ("p", L(
                    "None of these block the two verified core flows -- "
                    "each is named explicitly rather than discovered by a "
                    "reader the hard way.",
                    "以上没有一项阻碍两条已验证的核心流程——每一项都在此处"
                    "明确说明，而不是等读者自己艰难地发现。",
                )),
            ],
        },
        {
            "title": L("Reusable Workflow", "可复用工作流"),
            "blocks": [
                ("p", L(
                    "The reusable asset from this project is not its code "
                    "-- it is the 16-stage development system that produced "
                    "it, written out in full in "
                    "docs/GSTACK_REUSABLE_PROJECT_WORKFLOW.md, sized to the "
                    "next project rather than copied wholesale.",
                    "本项目产出的可复用资产不是它的代码——而是产出它的那套"
                    "16 阶段开发体系，完整写在 "
                    "docs/GSTACK_REUSABLE_PROJECT_WORKFLOW.md 中，应根据"
                    "下一个项目的规模调整，而不是整体照搬。",
                )),
            ],
        },
        {
            "title": L("Key Lessons", "关键教训"),
            "blocks": [
                ("bullets", [
                    (L("", ""), L(
                        "A green function call can still produce the wrong "
                        "artifact -- the avatar bug is the proof",
                        "一次函数调用返回成功，产出物仍然可能是错的——"
                        "头像 bug 就是证明",
                    )),
                    (L("", ""), L(
                        "Independent review should challenge assumptions, "
                        "not just approve the first draft",
                        "独立复核应当质疑假设，而不仅仅是批准初稿",
                    )),
                    (L("", ""), L(
                        "Known limitations do not automatically block "
                        "shipping when they are explicit and bounded",
                        "已知局限只要明确且有边界，就不会自动阻碍上线",
                    )),
                    (L("", ""), L(
                        "Humans retain consequential authorization and the "
                        "ship decision, with no exception",
                        "人类始终保留具有实质影响的授权和上线决策，没有"
                        "任何例外",
                    )),
                ]),
            ],
        },
        {
            "title": L("Metrics and Evidence Summary", "指标与证据总结"),
            "blocks": [
                ("p", L(
                    "See the At a Glance table on the cover page for the "
                    "full figure set. Every figure traces to a specific "
                    "review file in this repository -- see "
                    "docs/TUTORIAL_4_DOCUMENT_MANIFEST.md for the complete "
                    "provenance table.",
                    "完整数据集见封面页的\"概览数据\"表。每一项数字都可"
                    "追溯到本仓库中的具体复核文件——完整的溯源表见 "
                    "docs/TUTORIAL_4_DOCUMENT_MANIFEST.md。",
                )),
            ],
        },
        {
            "title": L("Tutorial 4.1: Post-Launch Iteration", "教程 4.1：上线之后的迭代"),
            "blocks": [
                ("p", L(
                    "A second, later session on the same codebase, run "
                    "after the app above was already live. Full narrative: "
                    "TUTORIAL.md / TUTORIAL.zh.md Parts 20-23. Four "
                    "findings carried the strongest lessons.",
                    "同一个代码库上第二次、更晚的会话，在上文的应用已经"
                    "上线之后进行。完整叙述见 TUTORIAL.md / TUTORIAL.zh.md "
                    "第 20-23 部分。四项发现携带了最有分量的教训。",
                )),
                ("h2", L("A shipped product judged unfinished", "一个被判定为未完成的已上线产品")),
                ("p", L(
                    "The app was functionally correct and already in "
                    "production, yet a human design review found it read "
                    "as an engineering prototype: no navigation between its "
                    "two modes, unstyled controls, three export buttons of "
                    "identical visual weight. A redesign (\"Quiet Creator "
                    "Tool\") shipped after a human-approved gate -- with "
                    "export architecture reconfirmed byte-identical before "
                    "and after.",
                    "该应用在功能上是正确的，并且已经在生产环境中运行，"
                    "但一次人工设计复核认为它读起来像一个工程原型：两种"
                    "模式之间没有导航、控件没有样式、三个导出按钮视觉权重"
                    "完全相同。一次重新设计（\"安静的创作工具\"）在人工"
                    "批准的关卡之后上线——导出架构在修改前后被重新确认为"
                    "逐字节相同。",
                )),
                ("h2", L("A missing card, traced to its real layer", "一张缺失的卡片，被追溯到它真正所在的那一层")),
                ("p", L(
                    "A quoted X Broadcast rendered as text and a bare link "
                    "instead of X.com's rich card. Tracing the pipeline "
                    "layer by layer found the free syndication data itself "
                    "never includes broadcast card metadata -- confirmed "
                    "against X's own oEmbed endpoint. Classified as a known "
                    "upstream limitation, not a bug; a native-video control "
                    "case confirmed ordinary media was unaffected.",
                    "一条被引用的 X Broadcast 渲染成了纯文本和一个裸链接，"
                    "而不是 X.com 的富卡片。逐层追溯这条流水线，发现免费"
                    "的 syndication 数据本身就从未包含 broadcast 卡片元"
                    "数据——这一点已对照 X 自己的 oEmbed 端点得到确认。"
                    "被归类为已知的上游限制，而不是 bug；一个原生视频"
                    "对照案例确认普通媒体不受影响。",
                )),
                ("h2", L("The wrong hypothesis, killed fast", "被快速杀死的错误假设")),
                ("p", L(
                    "A media-heavy thread's export timed out. The obvious "
                    "hypothesis -- too large for the requested scale -- was "
                    "disproven in one step: 1x, 2x, and 3x all failed at "
                    "the identical ~8.2-second mark. The real cause lived "
                    "in a third-party library's video-cloning code: it "
                    "waits for a browser event that a never-played video "
                    "will never fire, hanging forever.",
                    "一个媒体密集型 thread 的导出超时了。显而易见的假设——"
                    "对所请求的倍率来说体积太大——被一步证伪：1x、2x、3x "
                    "全部在相同的约 8.2 秒时刻失败。真正的原因藏在第三方"
                    "库的视频克隆代码里：它在等待一个从未播放过的视频"
                    "永远不会触发的浏览器事件，从而永远挂起。",
                )),
                ("code", [
                    "Scale  Result  Time to failure",
                    "1x     FAIL    ~8.2s",
                    "2x     FAIL    ~8.2s",
                    "3x     FAIL    ~8.2s   <- identical, not size-scaled",
                ]),
                ("callout", L(
                    "Identical failure time at every scale disproved the "
                    "size hypothesis in one experiment -- no timeout was "
                    "ever raised as the fix.",
                    "每个倍率下完全相同的失败耗时，用一次实验就证伪了"
                    "体积假设——超时时间从未被当作修复方案调大过。",
                )),
                ("h2", L("A promise resolving is not a human looking", "一个 promise resolve 了，不等于一个人亲眼看过")),
                ("p", L(
                    "The fixed export's clipboard-copy path had sat "
                    "unverified since the original release. A human closed "
                    "that gap the only way it actually closes: copying the "
                    "image on the live production app, pasting it into "
                    "Windows 11 Paint, and looking at the result.",
                    "修复后导出的剪贴板复制路径，自最初发布以来就一直"
                    "未经验证。一位人工用唯一真正能闭合这个缺口的方式"
                    "闭合了它：在线上生产应用中复制图片，粘贴进 Windows "
                    "11 画图，然后亲眼看结果。",
                )),
            ],
        },
        {
            "title": L("Definition of Done and Release Status", "完成定义与发布状态"),
            "blocks": [
                ("bullets", [
                    (L("Markdown tutorial:", "Markdown 教程："), L("complete, EN/ZH structural parity verified mechanically", "已完成，中英文结构一致性已机械化验证")),
                    (L("Privacy review:", "隐私复核："), L("complete for all source material and this document's built output", "已完成，覆盖所有源材料及本文档的构建输出")),
                    (L("Known limitations:", "已知局限："), L("documented, not hidden", "已记录，未被隐藏")),
                    (L("Public push:", "公开推送："), L("NOT performed as part of this documentation phase", "本文档阶段未执行")),
                ]),
                ("callout", L(
                    "Status: DOCUMENTATION_READY_WITH_KNOWN_LIMITATIONS -- "
                    "see the full completion report for the exact basis of "
                    "this status.",
                    "状态：DOCUMENTATION_READY_WITH_KNOWN_LIMITATIONS——"
                    "该状态的确切依据见完整的完成报告。",
                )),
            ],
        },
    ],
}
