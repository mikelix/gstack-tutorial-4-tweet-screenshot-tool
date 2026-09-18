# -*- coding: utf-8 -*-
"""Slide content for gstack Tutorial No.4, both languages in one structure.

Same L(en, zh) pattern as gstack-tutorial-3's deck_content.py (see that
file's own header for the rationale) -- each string is a pair, so EN/ZH
cannot drift apart in slide count or structure; they are generated from the
same list by _build/build_deck.py.

Source policy (per the privacy review, docs/TUTORIAL_4_PRIVACY_REVIEW.md):
every claim on every slide traces to reviews/, docs/external_ai_mentor.md,
PLAN.md, TUTORIAL.md, TODOS.md, or README.md. ChatGPT-gstack-20260917.pdf is
never quoted or embedded -- it is private source only. No metric on any
slide is invented; where this project's own record states something was
NOT verified, the slide says so rather than implying otherwise.
"""


class L(tuple):
    __slots__ = ()

    def __new__(cls, en, zh):
        return super().__new__(cls, (en, zh))


T = L


def pick(v, lang):
    i = 0 if lang == "en" else 1
    if isinstance(v, L):
        return pick(v[i], lang)
    if isinstance(v, dict):
        return {k: pick(x, lang) for k, x in v.items()}
    if isinstance(v, list):
        return [pick(x, lang) for x in v]
    if isinstance(v, tuple):
        return tuple(pick(x, lang) for x in v)
    return v


SLIDES = [

    # 1 -------------------------------------------------------------- cover
    ("cover", {
        "kicker": T("gstack tutorial no. 4", "gstack 教程 #4"),
        "title": T(
            "From AI Planning to Working Production Software",
            "从 AI 规划到可运行的生产级软件",
        ),
        "subtitle": T(
            "A worked example of running a second, independent AI as gstack's "
            "review and drafting layer — and the evidence ladder that caught "
            "a real, silent bug before ship.",
            "一个真实案例：让第二个独立的 AI 充当 gstack 的复核与起草层——"
            "以及在上线前抓住一个真实的、静默的 bug 的那条证据阶梯。",
        ),
        "meta": T(
            [
                "Subject: Tweet Screenshot Tool (Next.js, Vercel)",
                "Built and shipped in one session, 2026-09-17",
                "Source: reviews/01-05, docs/external_ai_mentor.md, TUTORIAL.md",
            ],
            [
                "主题：Tweet Screenshot Tool（Next.js, Vercel）",
                "一次会话内完成构建并上线，2026-09-17",
                "来源：reviews/01-05、docs/external_ai_mentor.md、TUTORIAL.md",
            ],
        ),
    }),

    # 2 ------------------------------------------------------------ bullets
    ("bullets", {
        "kicker": T("mental model", "心智模型"),
        "title": T(
            "“AI writes code” is an incomplete description of what actually happened",
            "“AI 写代码” 这句话，并不足以描述实际发生的事",
        ),
        "bullets": T(
            [
                ("Not one model.", "A separate AI mentor reviewed and drafted gstack's key prompts, in its own session."),
                ("Not one pass.", "CEO, outside-voice, and engineering review each caught what the previous one missed."),
                ("Not unverified.", "The bug that mattered was caught by looking at exported pixels — not by a check passing."),
                ("Not autonomous.", "Scope, deployment, and ship each went through an explicit human gate."),
            ],
            [
                ("不是一个模型。", "一个独立的 AI 导师，在自己的会话里复核并起草了 gstack 的关键提示词。"),
                ("不是一次通过。", "CEO 复核、外部意见、工程复核——每一层都抓住了上一层漏掉的东西。"),
                ("不是没有验证。", "真正重要的 bug，是靠查看导出的像素抓住的——而不是靠检查通过。"),
                ("不是自主运行。", "范围、部署、上线，每一个都经过明确的人工把关。"),
            ],
        ),
        "source": T("reviews/01-05; docs/external_ai_mentor.md", "reviews/01-05；docs/external_ai_mentor.md"),
    }),

    # 3 -------------------------------------------------------------- table
    ("table", {
        "kicker": T("the operating model", "运作模型"),
        "title": T(
            "A second AI translates gstack's output into the next precision prompt",
            "第二个 AI 把 gstack 的输出翻译成下一条精确提示词",
        ),
        "lead": T(
            "Every arrow crosses through the human. The mentor never touches "
            "the repository or talks to gstack directly.",
            "图中每一个箭头都要经过人类。导师从不接触代码仓库，也从不直接与 "
            "gstack 对话。",
        ),
        "headers": T(["Step", "What happens"], ["步骤", "发生了什么"]),
        "rows": T(
            [
                ["1. You", "Read gstack's output. Decide what matters."],
                ["2. External AI mentor", "Separate session. Translates, corrects, drafts the reply."],
                ["3. Optimized prompt", "Ready to paste — not a summary of what to say."],
                ["4. gstack specialist role", "CEO, engineer, QA, or DevOps, inside Claude Code."],
                ["5. Evidence", "Code, test output, browser QA, exported artifact."],
                ["6. Human gate", "You verify. You decide the next move."],
            ],
            [
                ["1. 你", "阅读 gstack 的输出，判断什么才重要。"],
                ["2. 外部 AI 导师", "独立会话。负责翻译、纠正、起草回复。"],
                ["3. 经过优化的提示词", "可以直接粘贴发送——不是“该说什么”的概述。"],
                ["4. gstack 专家角色", "在 Claude Code 内运行的 CEO、工程师、QA 或 DevOps。"],
                ["5. 证据", "代码、测试输出、浏览器 QA、导出的成品。"],
                ["6. 人工把关", "由你验证，由你决定下一步。"],
            ],
        ),
        "widths": [4.2, 7.6],
        "source": T("docs/external_ai_mentor.md", "docs/external_ai_mentor.md"),
    }),

    # 4 -------------------------------------------------------------- table
    ("table", {
        "title": T(
            "Five gstack roles ran end to end — one, the PM pass, did not run separately",
            "五个 gstack 角色全程运行——唯有 PM 这一轮没有单独执行",
        ),
        "lead": T(
            "The External AI Mentor sits above this table, not as a row inside it — see slide 3.",
            "外部 AI 导师凌驾于本表格之上，而非表内的一行——见第 3 页。",
        ),
        "headers": T(["Role", "Mechanism", "Ran this project?"],
                     ["角色", "机制", "本项目是否运行"]),
        "rows": T(
            [
                ["CEO", "/plan-ceo-review", "Yes"],
                ["PM", "Not run separately", "No — stated gap"],
                ["Architecture / Security / UX", "Embedded in CEO review", "Yes, not separate roles"],
                ["Second Opinion", "Fresh-context subagent", "Yes — same-model fallback"],
                ["Engineer / Eng Review", "/plan-eng-review + mentor charter", "Yes"],
                ["QA / Browser QA", "Manual QC + Aside", "Yes"],
                ["DevOps / Ship", "Ship Mode (mentor-authored)", "Yes"],
            ],
            [
                ["CEO", "/plan-ceo-review", "是"],
                ["PM", "未单独运行", "否——如实陈述的缺口"],
                ["架构 / 安全 / UX", "嵌入 CEO 复核之中", "是，未作为独立角色"],
                ["第二意见", "全新上下文的子智能体", "是——同模型兜底方案"],
                ["工程师 / 工程复核", "/plan-eng-review + 导师撰写的章程", "是"],
                ["QA / 浏览器 QA", "人工质检 + Aside", "是"],
                ["DevOps / 上线", "“上线模式”（导师撰写）", "是"],
            ],
        ),
        "widths": [2.6, 3.6, 3.6],
        "source": T("PLAN.md §2; reviews/01-05", "PLAN.md §2；reviews/01-05"),
    }),

    # 5 ------------------------------------------------------------ two_col
    ("two_col", {
        "title": T(
            "V1 shipped both tweet modes; automatic thread discovery and paid APIs were explicitly rejected",
            "V1 上线了两种推文模式；自动串联串文与付费 API 均被明确拒绝"
        ),
        "left": T(
            ("IN SCOPE",
             [
                 "Single tweet: paste URL, customize, export PNG / clipboard / share link",
                 "Thread mode: manual multi-URL builder, reorder, combined export",
                 "No paid X API — free public syndication endpoint only",
             ],
             "GOOD"),
            ("已纳入范围",
             [
                 "单条推文：粘贴链接、自定义样式、导出 PNG / 剪贴板 / 分享链接",
                 "串文模式：手动添加多条链接、排序、合并导出",
                 "不使用付费 X API——仅用免费的公开聚合接口",
             ],
             "GOOD"),
        ),
        "right": T(
            ("OUT OF SCOPE (STATED)",
             [
                 "Automatic thread discovery — no free data source supports it",
                 "Browser extension for one-click capture",
                 "Public headless generation API / CLI",
             ],
             "BAD"),
            ("明确排除在范围之外",
             [
                 "自动发现串文——没有免费数据源能支持",
                 "一键截取的浏览器扩展",
                 "公开的无头生成 API / 命令行工具",
             ],
             "BAD"),
        ),
        "source": T("reviews/01-ceo-review.md; TODOS.md", "reviews/01-ceo-review.md；TODOS.md"),
    }),

    # 6 -------------------------------------------------------------- table
    ("table", {
        "title": T(
            "A server-side hop and a hardened proxy work around what a free API can't do",
            "用服务端中转和加固代理，绕开免费 API 做不到的事"
        ),
        "headers": T(["Component", "Role"], ["组件", "作用"]),
        "rows": T(
            [
                ["Next.js", "App Router, TypeScript, hosted on Vercel"],
                ["react-tweet", "Fetches via X's free public syndication endpoint"],
                ["Server route", "/api/tweet/[id] — server-side only; CORS blocks direct browser fetch"],
                ["Image proxy", "SSRF-hardened: exact-host allowlist, https-only, size cap, MIME check"],
                ["modern-screenshot", "DOM → PNG export, routed through the proxy at capture time"],
            ],
            [
                ["Next.js", "App Router，TypeScript，部署在 Vercel"],
                ["react-tweet", "通过 X 的免费公开聚合接口获取数据"],
                ["服务端路由", "/api/tweet/[id]——仅服务端；CORS 阻止浏览器直接请求"],
                ["图片代理", "SSRF 加固：精确主机白名单、仅 HTTPS、大小上限、MIME 校验"],
                ["modern-screenshot", "DOM → PNG 导出，在捕获时经由代理转发"],
            ],
        ),
        "widths": [3.4, 8.4],
        "source": T("README.md “Architecture note”; reviews/01, 04", "README.md “Architecture note”；reviews/01、04"),
    }),

    # 7 -------------------------------------------------------------- table
    ("table", {
        "title": T(
            "A genuinely independent pass corrected the plan on four real points",
            "一次真正独立的复核，在四个真实问题上修正了计划"
        ),
        "headers": T(["Tension", "Why it mattered", "Resolution"], ["张力点", "为何重要", "解决方式"]),
        "rows": T(
            [
                ["Rate limit vs. “no secrets”", "Serverless in-memory counters reset every cold start — a limiter built that way would silently do nothing", "Corrected: real limiting needs shared state (Upstash/KV)"],
                ["Safari clipboard gesture", "The approved fix would break on Safari/iOS's synchronous-gesture requirement", "ClipboardItem wraps a Promise<Blob>, never awaited first"],
                ["Video export undefined", "Would have shipped as “whatever frame happens to paint,” randomly", "Poster-frame swap + play-icon badge"],
                ["Thread URL length uncapped", "A real thread could silently break its own share link", "Hard cap ≈ 12 tweets, explicit message"],
            ],
            [
                ["限流 与 “无需密钥” 的矛盾", "无服务器架构下内存计数器每次冷启动都会重置——这样搭出的限流器会静默失效", "已修正：真正的限流需要共享状态（Upstash/KV）"],
                ["Safari 剪贴板手势要求", "已批准的修复方案，在 Safari/iOS 要求的同步手势链下会失效", "ClipboardItem 直接包裹 Promise<Blob>，不预先 await"],
                ["视频导出行为未定义", "本会随机导出“浏览器碰巧渲染到的那一帧”", "海报帧替换 + 播放图标徽章"],
                ["串文分享链接长度无上限", "真实的串文可能悄悄破坏自己的分享链接", "硬性上限约 12 条推文，附带明确提示"],
            ],
        ),
        "widths": [3.0, 4.4, 3.4],
        "source": T("reviews/03-eng-review.md (OV-1 to OV-4)", "reviews/03-eng-review.md（OV-1 至 OV-4）"),
    }),

    # 8 -------------------------------------------------------------- table
    ("table", {
        "title": T(
            "The single most consequential finding: a planned fix was never wired to real code",
            "全项目最关键的一项发现：计划中的修复从未真正接入代码"
        ),
        "headers": T(["Finding", "What was actually wrong", "Remedy"], ["发现", "问题所在", "补救措施"]),
        "rows": T(
            [
                ["B1 — Image proxy never wired", "react-tweet renders plain <img> at pbs.twimg.com; nothing in the plan rewired that", "Mandatory T1.5 spike inserted before broad implementation"],
                ["B2 — Proxy hardening incomplete", "No redirect re-validation, protocol check, size cap, or MIME check", "All four added before any code existed"],
                ["B3 — Images not awaited before capture", "Same silent-wrong-output bug class as the font race the CEO review had already found", "await Promise.all(images.map(img => img.decode()))"],
            ],
            [
                ["B1 —— 图片代理从未接入", "react-tweet 直接渲染指向 pbs.twimg.com 的 <img>；计划从未把它重新接过来", "在大规模实现之前插入强制性的 T1.5 验证性小试"],
                ["B2 —— 代理加固不完整", "缺少重定向再校验、协议检查、大小上限、MIME 校验", "在任何代码存在之前，四项全部补齐"],
                ["B3 —— 捕获前未等待图片加载完成", "与 CEO 复核已发现的字体竞态属于同一类静默输出错误", "await Promise.all(images.map(img => img.decode()))"],
            ],
        ),
        "widths": [3.2, 4.4, 3.2],
        "source": T("reviews/03-eng-review.md; reviews/04-qa-report.md", "reviews/03-eng-review.md；reviews/04-qa-report.md"),
    }),

    # 9 -------------------------------------------------------------- table
    ("table", {
        "kicker": T("the high-risk spike", "高风险验证性小试"),
        "title": T(
            "T1.5: one mandatory spike, gated on real evidence, not more planning",
            "T1.5：一次强制性的小试，靠真实证据推进，而非更多计划"
        ),
        "headers": T(["Step", "What happened"], ["步骤", "发生了什么"]),
        "rows": T(
            [
                ["1. Assumption", "The image-proxy fix should just work once wired up"],
                ["2. Experiment", "Read the library's real source; wire fetchFn to the proxy"],
                ["3. First result", "“Success” — no exception was thrown"],
                ["4. Bug found", "Exported PNG: a broken-image icon where the avatar should be"],
                ["5. Fix", "blob: URL → base64 data: URL, proven visually"],
            ],
            [
                ["1. 假设", "图片代理的修复方案，接上去应该就能用"],
                ["2. 实验", "直接阅读库的真实源码；把 fetchFn 接到代理上"],
                ["3. 第一次结果", "“成功”——没有抛出任何异常"],
                ["4. 发现 bug", "导出的 PNG：头像本该出现的位置是一个“图片损坏”图标"],
                ["5. 修复", "blob: URL → base64 data: URL，并以视觉证据确认"],
            ],
        ),
        "widths": [3.6, 8.2],
        "source": T("reviews/04-qa-report.md", "reviews/04-qa-report.md"),
    }),

    # 10 -------------------------------------------------------------- quote
    ("quote", {
        "kicker": T("successful execution ≠ correct output", "执行成功 ≠ 输出正确"),
        "quote": T(
            "modern-screenshot reported success.\nNo exception was thrown.\nAnd the image was still wrong.",
            "modern-screenshot 报告了成功。\n没有抛出任何异常。\n而图片依然是错的。",
        ),
        "attrib": T(
            "The avatar bug — the strongest evidence in this project that a "
            "passing check is not proof of a correct result. reviews/04-qa-report.md",
            "头像 bug——本项目中最有力的证据，说明“检查通过”并不等于"
            "“结果正确”。reviews/04-qa-report.md",
        ),
    }),

    # 11 ------------------------------------------------------------ bullets
    ("bullets", {
        "title": T(
            "Every QA checkpoint ran through a real browser, not a headless approximation",
            "每一个 QA 检查点都在真实浏览器中运行，而非用无头浏览器近似模拟"
        ),
        "bullets": T(
            [
                ("Real browser.", "Aside — an AI-native browser — drove every checkpoint from the T1.5 spike through the production smoke test, on Windows 11."),
                ("Deterministic races.", "Network-delay injection forced the stale-request race to reproduce on demand, instead of hoping to catch it by luck."),
                ("Visual inspection.", "Real downloaded PNGs were read and visually inspected — this is what actually caught the avatar bug."),
                ("Production checks.", "The same checks ran again against the live deployed URL after shipping, not just localhost."),
            ],
            [
                ("真实浏览器。", "Aside——一款 AI 原生浏览器——在 Windows 11 上驱动了从 T1.5 小试到生产环境冒烟测试的每一个检查点。"),
                ("确定性的竞态复现。", "通过注入网络延迟，让“过期请求”这种竞态问题可以按需复现，而不是寄望于运气抓到它。"),
                ("视觉检查。", "真实下载的 PNG 被读取并亲眼检查——正是这一步真正抓住了头像 bug。"),
                ("生产环境检查。", "上线之后，同样的检查在真实部署的 URL 上又跑了一遍，而不只是本地环境。"),
            ],
        ),
        "source": T("reviews/04-qa-report.md", "reviews/04-qa-report.md"),
    }),

    # 12 -------------------------------------------------------------- table
    ("table", {
        "title": T(
            "One step in this project has no AI substitute: a human looking at the result",
            "本项目中有一步是任何 AI 都无法替代的：由人亲眼查看结果"
        ),
        "lead": T(
            "Reported by the user, not independently verifiable by the AI — "
            "that is exactly the point.",
            "由用户自行报告，AI 无法独立验证——而这正是关键所在。",
        ),
        "headers": T(["Step", "What happened"], ["步骤", "发生了什么"]),
        "rows": T(
            [
                ["1. Localhost", "Human launched the app themselves"],
                ["2. Export", "Downloaded a real PNG"],
                ["3. Visual check", "Inspected the file directly"],
                ["4. Production", "Repeated the same check against the deployed Vercel URL"],
            ],
            [
                ["1. 本地环境", "由人亲自启动应用"],
                ["2. 导出", "下载一张真实的 PNG"],
                ["3. 视觉检查", "直接查看文件本身"],
                ["4. 生产环境", "对已部署的 Vercel URL 重复同样的检查"],
            ],
        ),
        "widths": [3.4, 8.4],
        "source": T("reviews/04-qa-report.md; reviews/05-ship.md", "reviews/04-qa-report.md；reviews/05-ship.md"),
    }),

    # 13 ------------------------------------------------------------- table
    ("table", {
        "title": T(
            "Ten levels from idea to proof; the avatar bug hid at level 3",
            "从想法到证据共十层；头像 bug 就藏在第 3 层"
        ),
        "headers": T(["Level", "What it actually removes uncertainty about"], ["层级", "它真正消除的是哪一种不确定性"]),
        "rows": T(
            [
                ["1. Idea", "Nothing about feasibility yet"],
                ["2. Code compiles / builds", "Type correctness only"],
                ["3. Local browser “succeeds”", "Looks like proof — usually isn't. The trap the avatar bug hid in."],
                ["4. Deterministic browser test", "A specific, hard-to-reproduce failure, made repeatable"],
                ["5. Exported artifact inspected", "“No error” ≠ “correct output” — this caught the avatar bug"],
                ["6. Human manual test", "Blind spots automated checks share"],
                ["7. Production + human production test", "Works with real infrastructure, for real"],
            ],
            [
                ["1. 想法", "关于可行性还什么都没证明"],
                ["2. 代码能编译 / 构建", "只证明了类型正确"],
                ["3. 本地浏览器“成功了”", "看起来像证据——通常不是。头像 bug 正是藏在这个陷阱里。"],
                ["4. 确定性的浏览器测试", "让一个特定的、难以复现的故障变得可以按需复现"],
                ["5. 导出成品被亲眼检查", "“没有报错” ≠ “输出正确”——正是这一层抓住了头像 bug"],
                ["6. 人工手动测试", "抓住自动化检查共有的盲区"],
                ["7. 生产环境 + 人工在生产环境测试", "证明在真实基础设施上确实可用"],
            ],
        ),
        "widths": [4.0, 7.8],
        "source": T("reviews/04-qa-report.md (full 10-level version)", "reviews/04-qa-report.md（完整 10 层版本）"),
    }),

    # 14 -------------------------------------------------------------- table
    ("table", {
        "title": T(
            "Ship Mode: stop debugging, document what's known, minimal QC, ship",
            "上线模式：停止调试、记录已知情况、最低限度质检、上线"
        ),
        "headers": T(["Step", "What it means"], ["步骤", "含义"]),
        "rows": T(
            [
                ["1. Stop", "End open-ended debugging on a schedule, not whenever it happens to resolve"],
                ["2. Document", "Record what's verified and what isn't — not silence, not a vague note"],
                ["3. Minimal QC", "One rapid Aside smoke test, not a full re-audit"],
                ["4. Ship", "Deploy once the core flow passes build + smoke test"],
            ],
            [
                ["1. 停止", "按计划结束开放式调试，而不是拖到“碰巧解决”为止"],
                ["2. 记录", "写清楚哪些已验证、哪些没有——不是沉默，也不是含糊的备注"],
                ["3. 最低限度质检", "一次快速的 Aside 冒烟测试，而不是完整的重新审计"],
                ["4. 上线", "核心流程通过构建 + 冒烟测试后即部署"],
            ],
        ),
        "widths": [3.4, 8.4],
        "source": T("reviews/05-ship.md; docs/external_ai_mentor.md", "reviews/05-ship.md；docs/external_ai_mentor.md"),
    }),

    # 15 ------------------------------------------------------------ bullets
    ("bullets", {
        "title": T(
            "Both core flows verified working in production, not just in development",
            "两条核心流程都已在生产环境中验证可用，而不只是在开发环境"
        ),
        "bullets": T(
            [
                ("Live.", "Deployed to Vercel — the first deployment for a new project becomes production directly."),
                ("Single tweet.", "Paste URL → customize → export PNG / clipboard / share link — verified in production."),
                ("Thread mode.", "Manual multi-tweet builder → combined export — verified in production."),
                ("Verified, not assumed.", "Confirmed via real-browser automation, and reported by the user as manually tested."),
            ],
            [
                ("已上线。", "已部署到 Vercel——新项目的第一次部署会直接成为生产环境。"),
                ("单条推文。", "粘贴链接 → 自定义样式 → 导出 PNG / 剪贴板 / 分享链接——已在生产环境验证。"),
                ("串文模式。", "手动多条推文构建 → 合并导出——已在生产环境验证。"),
                ("经过验证，而非假设。", "通过真实浏览器自动化确认，并由用户报告已完成人工测试。"),
            ],
        ),
        "source": T("reviews/05-ship.md; README.md", "reviews/05-ship.md；README.md"),
    }),

    # 16 -------------------------------------------------------------- table
    ("table", {
        "title": T(
            "Four known gaps, stated in release notes — not hidden",
            "四个已知缺口，写进发布说明——而非隐藏"
        ),
        "headers": T(["Item", "Status"], ["项目", "状态"]),
        "rows": T(
            [
                ["Rate limiting on both public API routes", "Planned, reviewed twice, never implemented"],
                ["Safari / iOS clipboard", "Implemented, not empirically verified on real Safari"],
                ["Video / emoji / multi-image export", "Implemented, not empirically verified"],
                ["Thread share-link style restoration", "Investigated one bounded pass; root cause not found"],
            ],
            [
                ["两条公开 API 路由的限流", "已计划、已复核两次，但从未实现"],
                ["Safari / iOS 剪贴板", "已实现，但未在真实 Safari 上做实证验证"],
                ["视频 / 表情符号 / 多图导出", "已实现，但未做实证验证"],
                ["串文分享链接的样式还原", "调查了一轮有限的排查；未能找到根因"],
            ],
        ),
        "widths": [6.2, 5.6],
        "source": T("TODOS.md; reviews/05-ship.md", "TODOS.md；reviews/05-ship.md"),
    }),

    # 17 ------------------------------------------------------------ bullets
    ("bullets", {
        "title": T(
            "One debugging session ran long because no time budget was set before it started",
            "一次调试之所以拖得太久，是因为开始前没有设定时间上限"
        ),
        "bullets": T(
            [
                ("The cost.", "The thread-style bug consumed the largest single block of investigation time in the project."),
                ("What was tried.", "Strict Mode toggling, a full cache clear, a server restart — all before stopping."),
                ("The lesson.", "Set an explicit time/attempt budget on any single bug investigation before starting it, not after it's already run long."),
                ("The second gap.", "No automated test suite was written despite the plan specifying one — every scenario needed a real, currently-live tweet found by hand."),
            ],
            [
                ("代价。", "串文样式的这个 bug，消耗了本项目里单次排查耗时最长的一段时间。"),
                ("尝试过什么。", "切换 Strict Mode、彻底清缓存、重启服务器——直到最后才停下来。"),
                ("这一课。", "在开始排查任何一个 bug 之前，就先设定明确的时间/尝试次数上限，而不是等它已经拖久了才想起来。"),
                ("第二个缺口。", "尽管计划里明确写了要做自动化测试，但最终并未编写——每个场景都要靠人手动去找一条真实的、仍然存在的推文。"),
            ],
        ),
        "source": T("reviews/05-ship.md (“Where time was spent”)", "reviews/05-ship.md（“时间花在哪里”）"),
    }),

    # 18 ------------------------------------------------------------- table
    ("table", {
        "title": T(
            "The same sequence generalizes: frame, review, de-risk, build, verify, ship",
            "同一套流程可以推广：框定问题、复核、去风险、构建、验证、上线"
        ),
        "lead": T(
            "Full chain: problem framing → CEO → PM → architecture → "
            "review → high-risk spike → build → browser QA → human QA "
            "→ minimal QC → deploy.",
            "完整链条：框定问题 → CEO → PM → 架构 → 复核 → 高风险验证性小试 → "
            "构建 → 浏览器 QA → 人工 QA → 最低限度质检 → 部署。",
        ),
        "headers": T(["Stage", "What happens"], ["阶段", "发生了什么"]),
        "rows": T(
            [
                ["1. Frame", "Problem framing, premise challenge"],
                ["2. Plan & review", "CEO → PM → architecture → independent review"],
                ["3. De-risk", "High-risk spike, gated before broad implementation"],
                ["4. Build", "Implementation against the reviewed plan"],
                ["5. Verify", "Browser QA + human QA — not either alone"],
                ["6. Ship", "Minimal QC, deploy"],
            ],
            [
                ["1. 框定问题", "问题框定、前提假设的质疑"],
                ["2. 规划与复核", "CEO → PM → 架构 → 独立复核"],
                ["3. 去风险", "高风险验证性小试，在大规模实现前先行把关"],
                ["4. 构建", "按已复核的计划实施"],
                ["5. 验证", "浏览器 QA + 人工 QA——缺一不可"],
                ["6. 上线", "最低限度质检，部署"],
            ],
        ),
        "widths": [3.4, 8.4],
        "source": T("PLAN.md; reviews/01-05", "PLAN.md；reviews/01-05"),
    }),

    # 19 ------------------------------------------------------------ two_col
    ("two_col", {
        "title": T(
            "Humans hold judgment and authorization; AI holds repeatable, exhaustive verification",
            "人类掌握判断与授权；AI 承担可重复、穷举式的验证工作"
        ),
        "left": T(
            ("HUMAN",
             [
                 "Judgment: does this actually look right?",
                 "Authorization: account logins, real money, real credentials",
                 "The ship decision, every time",
             ],
             "NAVY"),
            ("人类",
             [
                 "判断：这东西看起来真的对吗？",
                 "授权：账号登录、真实资金、真实凭证",
                 "每一次的上线决策",
             ],
             "NAVY"),
        ),
        "right": T(
            ("AI",
             [
                 "Analysis: reading library source, security checklists",
                 "Implementation: following the reviewed plan",
                 "Repetitive verification: the same QC loop, dozens of times, zero fatigue",
             ],
             "GOOD"),
            ("AI",
             [
                 "分析：阅读库的源码、安全检查清单",
                 "实现：按已复核的计划执行",
                 "重复性验证：同一套质检循环，跑几十遍也不会疲劳",
             ],
             "GOOD"),
        ),
        "source": T("reviews/05-ship.md (“Human/AI responsibility”)", "reviews/05-ship.md（“人类/AI 职责分工”）"),
    }),

    # 20 ------------------------------------------------------------ bullets
    ("bullets", {
        "kicker": T("final lessons", "最终启示"),
        "title": T(
            "Six lessons this project actually earned, not six generic best practices",
            "本项目真正换来的六条启示，而非六条泛泛而谈的最佳实践"
        ),
        "bullets": T(
            [
                ("1.", "A passing check is not proof of correct output — look at the artifact."),
                ("2.", "An independent reviewer catches what a self-reviewer structurally cannot."),
                ("3.", "A reviewed decision isn't shipped until the code is checked, not the plan."),
                ("4.", "Set a debugging time budget before starting, not after it's run long."),
                ("5.", "Never let an AI perform account authorization — that stays human."),
                ("6.", "State known gaps in release notes. Silence about limits reads as a claim."),
            ],
            [
                ("1.", "检查通过不等于输出正确——去看那个成品本身。"),
                ("2.", "独立的复核者，能抓住自我复核在结构上抓不住的东西。"),
                ("3.", "决策被复核，不等于已交付——要检查代码，而不是计划。"),
                ("4.", "在调试开始之前就设定时间上限，而不是拖久了才想起来。"),
                ("5.", "绝不让 AI 执行账号授权——这道关卡永远由人类把守。"),
                ("6.", "把已知缺口写进发布说明。对局限保持沉默，本身就是一种宣称。"),
            ],
        ),
        "source": T("reviews/04-qa-report.md; reviews/05-ship.md; docs/external_ai_mentor.md",
                    "reviews/04-qa-report.md；reviews/05-ship.md；docs/external_ai_mentor.md"),
    }),

    # 21 -------------------------------------------------------------- table
    ("table", {
        "kicker": T("tutorial 4.1 — product design review", "教程 4.1 —— 产品设计复核"),
        "title": T(
            "A working product that still read as an engineering prototype",
            "一个能用、却依然读起来像工程原型的产品"
        ),
        "lead": T(
            "Shipped and functionally correct is a different claim from "
            "trustworthy at first glance.",
            "已上线且功能正确，和第一眼就值得信任，是两个不同的结论。",
        ),
        "headers": T(["Gap found", "Fix shipped"], ["发现的差距", "上线的修复"]),
        "rows": T(
            [
                ["No header or navigation", "Persistent header; Single Tweet / Thread now cross-linked"],
                ["Plain, unstyled input", "Styled control, two-column preview + inspector layout"],
                ["Three export buttons, equal weight", "One primary action, two visibly secondary"],
                ["375px horizontal overflow (confirmed bug)", "Fixed; re-verified mechanically"],
            ],
            [
                ["没有头部或导航", "持久化头部；Single Tweet / Thread 现已互相链接"],
                ["朴素、无样式的输入框", "已样式化的控件，预览+检查面板两栏布局"],
                ["三个导出按钮，权重相同", "一个主要操作，两个明显次要的操作"],
                ["375px 下的水平溢出（已确认的 bug）", "已修复；已机械化重新验证"],
            ],
        ),
        "widths": [5.5, 6.3],
        "source": T("docs/DESIGN_REVIEW_4_1_HUMAN_REVIEW.md; docs/DESIGN_REVIEW_4_1_RELEASE.md",
                    "docs/DESIGN_REVIEW_4_1_HUMAN_REVIEW.md；docs/DESIGN_REVIEW_4_1_RELEASE.md"),
    }),

    # 22 -------------------------------------------------------------- table
    ("table", {
        "kicker": T("tutorial 4.1 — the X Broadcast boundary", "教程 4.1 —— X Broadcast 的边界"),
        "title": T(
            "Before fixing a missing output, find the layer where it disappears",
            "在修复一个缺失的输出之前，先找到它消失的那一层"
        ),
        "lead": T(
            "X's free syndication data never includes broadcast card "
            "metadata — confirmed by reading the raw payload, not guessed.",
            "X 的免费 syndication 数据从未包含 broadcast 卡片元数据"
            "——这是通过直接读取原始数据确认的，不是猜测。",
        ),
        "headers": T(["Layer", "Result"], ["层", "结果"]),
        "rows": T(
            [
                ["X.com original page", "Rich animated Broadcast card — visible"],
                ["Free syndication payload", "URL entity only — no card, poster, or title"],
                ["react-tweet library", "No card/broadcast concept anywhere in source"],
                ["This app + export", "Text + link — matches upstream data exactly"],
            ],
            [
                ["X.com 原始页面", "丰富的动态 Broadcast 卡片——可见"],
                ["免费 syndication 数据", "仅有 URL 实体——没有卡片、封面图或标题"],
                ["react-tweet 库", "源码任何地方都没有卡片/broadcast 概念"],
                ["本应用 + 导出", "文本+链接——与上游数据完全一致"],
            ],
        ),
        "widths": [4.5, 7.3],
        "source": T("TODOS.md; docs/DESIGN_REVIEW_4_1_RELEASE.md — classified as known upstream limitation, not a bug",
                    "TODOS.md；docs/DESIGN_REVIEW_4_1_RELEASE.md ——归类为已知上游限制，非 bug"),
    }),

    # 23 -------------------------------------------------------------- quote
    ("quote", {
        "kicker": T("tutorial 4.1 — the wrong hypothesis, killed fast", "教程 4.1 —— 被快速杀死的错误假设"),
        "quote": T(
            "1x, 2x, and 3x all failed at the identical ~8.2-second mark.\n"
            "A real size problem fails later at 1x than at 3x.\n"
            "Identical timing didn't weakly suggest — it disproved the hypothesis.",
            "1x、2x、3x 全部在相同的约 8.2 秒时刻失败。\n"
            "一个真实的体积问题，会在 1x 时更晚失败、3x 时更早失败。\n"
            "完全相同的耗时不是弱证据——它直接证伪了这个假设。",
        ),
        "attrib": T(
            "Real cause: modern-screenshot awaits a `seeked` event a never-played "
            "video will never fire. Fix: swap <video> for its poster on an "
            "off-screen clone, before the library ever sees it. src/lib/export-image.ts",
            "真正的原因：modern-screenshot 在等待一个从未播放过的视频永远不会"
            "触发的 `seeked` 事件。修复：在库看到它之前，先在一份屏幕外的克隆"
            "上把 <video> 换成它的封面图。src/lib/export-image.ts",
        ),
    }),

    # 24 ------------------------------------------------------------ bullets
    ("bullets", {
        "kicker": T("tutorial 4.1 — the human evidence ladder, extended", "教程 4.1 —— 延伸后的人工证据阶梯"),
        "title": T(
            "“The promise resolved” and “a human pasted it and looked” are different claims",
            "“承诺 resolve 了”和“一个人粘贴之后亲眼看过”是两个不同的结论"
        ),
        "bullets": T(
            [
                ("Printed before export.", "A PDF of the thread page, captured before the export attempt, proved the DOM had rendered correctly — independent of what export did next."),
                ("Production, not just local.", "Download PNG and Copy image were both re-run against the live deployed URL after the fix, not only on localhost."),
                ("Cross-application, by hand.", "The copied image was pasted into Windows 11 Paint and visually confirmed — closing a clipboard claim left unverified since the original tutorial."),
                ("Still no AI substitute.", "No automated check in this project's history could have formulated either of Tutorial 4.1's two bugs — a human found both."),
            ],
            [
                ("导出之前先打印出来。", "一份在尝试导出之前就打印出来的 thread 页面 PDF，证明了 DOM 渲染正确——独立于导出接下来做了什么。"),
                ("不只是本地，是生产环境。", "修复之后，Download PNG 和 Copy image 都针对线上已部署的 URL 重新跑了一遍，不只是本地环境。"),
                ("跨应用、亲手确认。", "复制出来的图片被粘贴进 Windows 11 画图并经过肉眼确认——闭合了一个自最初那份教程以来就一直未经验证的剪贴板声明。"),
                ("依然没有 AI 可以替代。", "本项目历史上没有任何自动化检查能够表述出教程 4.1 里的这两个 bug 中的任何一个——两个都是被人工发现的。"),
            ],
        ),
        "source": T("docs/DESIGN_REVIEW_4_1_RELEASE.md — human manual verification",
                    "docs/DESIGN_REVIEW_4_1_RELEASE.md ——人工手动验证"),
    }),
]
