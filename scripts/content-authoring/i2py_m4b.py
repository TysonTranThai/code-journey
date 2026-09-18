#!/usr/bin/env python3
"""Module 4 practices: tokens, layout, container, components, motion, dashboard build."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_practice, fn_wrap

MOD = "advanced-css-ui-engineering"


def css_test(name, checks, hint):
    """Build a declaration-checking test from a list of (regex, message) pairs."""
    lines = []
    for rx, msg in checks:
        msg_js = msg.replace("\\", "\\\\").replace('"', '\\"')
        lines.append('if (!/%s/i.test(css)) throw new Error("%s");' % (rx, msg_js))
    return (name, "\n".join(lines), hint)


def css_challenge(cid, title, prompt, boilerplate, tests, level, vi):
    """A CSS challenge whose tests receive the learner's code as `css`."""
    tests_out = []
    for (n, code, h) in tests:
        preamble = "const css = code;"
        tests_out.append({"name": n, "code": preamble + "\n" + code, "hint": h})
    return {
        "id": cid,
        "title": title,
        "prompt": prompt,
        "difficulty": "intermediate",
        "level": level,
        "boilerplate": boilerplate,
        "tests": tests_out,
    }, vi


# ── tokens-practice ─────────────────────────────────────────────────────────
ch1, vi1 = css_challenge(
    "i2-token-theme",
    "Dark Theme via Tokens",
    "Starting from the light tokens in the boilerplate, add a `[data-theme=\"dark\"]` scope that re-declares `--color-bg` and `--color-fg` with dark values, and make the `.card` consume ONLY tokens (no raw colors).",
    ':root {\n  --color-bg: #ffffff;\n  --color-fg: #111827;\n  --color-accent: #2563eb;\n}\n\n/* your dark theme + card styles */\n\n.card {\n  /* consume tokens only */\n}\n',
    [
        css_test(
            "dark scope re-declares bg and fg tokens",
            [
                (r'data-theme=["\']?dark["\']?\]\s*{', "Add a [data-theme=\"dark\"] scope."),
                (r'data-theme[^{]*{[^}]*--color-bg\s*:', "Re-declare --color-bg inside the dark scope."),
                (r'data-theme[^{]*{[^}]*--color-fg\s*:', "Re-declare --color-fg inside the dark scope."),
            ],
            "[data-theme=\"dark\"] { --color-bg: #0b1120; --color-fg: #e2e8f0; } — pick any dark values.",
        ),
        css_test(
            "card consumes tokens, not raw colors",
            [
                (r'\.card\s*{[^}]*var\(\s*--color-bg', "The card's background should come from var(--color-bg)."),
                (r'\.card\s*{[^}]*var\(\s*--color-fg', "The card's text color should come from var(--color-fg)."),
                (r'\.card\s*{(?![^}]*#[0-9a-f]{3,8})', "No raw hex colors inside .card — tokens only."),
            ],
            "background: var(--color-bg); color: var(--color-fg);",
        ),
    ],
    "guided",
    {
        "title": "Theme tối qua token",
        "prompt": "Bắt đầu từ các token sáng trong boilerplate, thêm một phạm vi `[data-theme=\"dark\"]` khai báo lại `--color-bg` và `--color-fg` với giá trị tối, và làm cho `.card` chỉ tiêu thụ TOKEN (không màu thô).",
        "tests": [
            {"name": "phạm vi tối khai báo lại token bg và fg", "hint": "[data-theme=\"dark\"] { --color-bg: #0b1120; --color-fg: #e2e8f0; } — chọn giá trị tối tùy ý."},
            {"name": "card tiêu thụ token, không màu thô", "hint": "background: var(--color-bg); color: var(--color-fg);"},
        ],
    },
)
write_practice(
    MOD, "tokens-practice",
    "Design Tokens — Practice",
    "Tokens as an API: a dark theme scope, accent computation with calc(), and a spacing scale consumed consistently.",
    "Design Token — Luyện tập",
    "Token như một API: phạm vi theme tối, tính toán màu nhấn bằng calc(), và thang khoảng cách được dùng nhất quán.",
    "custom-properties-theming", 15, "intermediate",
    [ch1],
    { "i2-token-theme": vi1 },
    [
        ["i2-token-theme",
         ':root {\n  --color-bg: #ffffff;\n  --color-fg: #111827;\n  --color-accent: #2563eb;\n}\n[data-theme="dark"] {\n  --color-bg: #0b1120;\n  --color-fg: #e2e8f0;\n}\n.card {\n  background: var(--color-bg);\n  color: var(--color-fg);\n  border: 1px solid var(--color-accent);\n}',
         ':root {\n  --color-bg: #ffffff;\n  --color-fg: #111827;\n}\n.card {\n  background: #ffffff;\n  color: #111827;\n}'],
    ],
)

# ── layout-practice ─────────────────────────────────────────────────────────
ch2, vi2 = css_challenge(
    "i2-auto-gallery",
    "Auto-Wrapping Gallery",
    "Build `.gallery` as a grid whose columns wrap automatically: each track at least `180px`, all sharing leftover space equally, with `1rem` gaps — no media queries allowed.",
    '<div class="gallery">\n  <div class="tile">1</div>\n  <div class="tile">2</div>\n  <div class="tile">3</div>\n  <div class="tile">4</div>\n</div>\n\n<style>\n  /* your grid */\n</style>\n',
    [
        css_test(
            "grid with auto tracks and min 180px",
            [
                (r'\.gallery\s*{[^}]*display\s*:\s*grid', "The gallery must be a grid container."),
                (r'\.gallery\s*{[^}]*repeat\(\s*auto-(fit|fill)\s*,\s*minmax\(\s*180px\s*,\s*1fr\s*\)\s*\)', "Columns: repeat(auto-fit, minmax(180px, 1fr))."),
                (r'\.gallery\s*{[^}]*gap\s*:\s*1rem', "Space tiles with gap: 1rem."),
            ],
            "grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem;",
        ),
        css_test(
            "no media queries needed",
            [
                (r'^(?!.*@media)', "This layout should need no @media — auto-fit handles the wrapping."),
            ],
            "The whole point of auto-fit: the grid reflows without breakpoints.",
        ),
    ],
    "guided",
    {
        "title": "Gallery tự xuống dòng",
        "prompt": "Dựng `.gallery` thành grid có các cột tự xuống dòng: mỗi track tối thiểu `180px`, chia đều phần không gian còn lại, gap `1rem` — không được dùng media query.",
        "tests": [
            {"name": "grid với auto track và min 180px", "hint": "grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem;"},
            {"name": "không cần media query", "hint": "Điểm mạnh của auto-fit: grid tự reflow mà không cần breakpoint."},
        ],
    },
)
ch3, vi3 = css_challenge(
    "i2-app-shell",
    "Dashboard Shell with Areas",
    "Lay out `.shell` with named grid areas: `head head` on top, `side main` in the middle row, `side foot` at the bottom; sidebar fixed at `220px`, main column flexible.",
    '<div class="shell">\n  <header>h</header>\n  <aside>s</aside>\n  <main>m</main>\n  <footer>f</footer>\n</div>\n\n<style>\n.shell { /* areas + columns */ }\nheader { grid-area: head; }\naside { grid-area: side; }\nmain { grid-area: main; }\nfooter { grid-area: foot; }\n</style>\n',
    [
        css_test(
            "areas and columns defined",
            [
                (r'\.shell\s*{[^}]*display\s*:\s*grid', "The shell must be a grid."),
                (r'\.shell\s*{[^}]*grid-template-areas\s*:[^;}]*head\s+head', 'Rows start with "head head".'),
                (r'\.shell\s*{[^}]*grid-template-areas\s*:[^;}]*side\s+main', 'Middle row: "side main".'),
                (r'\.shell\s*{[^}]*grid-template-areas\s*:[^;}]*side\s+foot', 'Bottom row: "side foot".'),
                (r'\.shell\s*{[^}]*grid-template-columns\s*:[^;}]*220px', "Sidebar column fixed at 220px."),
                (r'\.shell\s*{[^}]*grid-template-columns\s*:[^;}]*1fr', "Main column takes the rest (1fr)."),
            ],
            'grid-template-areas: "head head" "side main" "side foot"; grid-template-columns: 220px 1fr;',
        ),
    ],
    "independent",
    {
        "title": "Khung Dashboard với areas",
        "prompt": "Bố trí `.shell` bằng named grid areas: `head head` ở trên, `side main` ở giữa, `side foot` ở dưới; sidebar cố định `220px`, cột chính co giãn.",
        "tests": [
            {"name": "areas và cột được định nghĩa", "hint": 'grid-template-areas: "head head" "side main" "side foot"; grid-template-columns: 220px 1fr;'},
        ],
    },
)
write_practice(
    MOD, "layout-practice",
    "Advanced Layout — Practice",
    "Auto-wrapping galleries and named-area application shells — grid decisions without breakpoints.",
    "Layout nâng cao — Luyện tập",
    "Gallery tự xuống dòng và khung ứng dụng với named areas — các quyết định grid không cần breakpoint.",
    "advanced-grid-flexbox", 20, "intermediate",
    [ch2, ch3],
    { "i2-auto-gallery": vi2, "i2-app-shell": vi3 },
    [
        ["i2-auto-gallery",
         '.gallery {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));\n  gap: 1rem;\n}',
         '.gallery { display: grid; grid-template-columns: 200px; }'],
        ["i2-app-shell",
         '.shell {\n  display: grid;\n  grid-template-areas:\n    "head head"\n    "side main"\n    "side foot";\n  grid-template-columns: 220px 1fr;\n}',
         '.shell { display: grid; }'],
    ],
)

# ── container-practice ──────────────────────────────────────────────────────
ch4, vi4 = css_challenge(
    "i2-container-card",
    "Container-Responsive Card",
    "Make `.slot` a size container, then inside `@container (min-width: 420px)` give `.card` a two-column grid (`120px 1fr`). Below that width the card stays a single column — all without media queries.",
    '<div class="slot">\n  <article class="card">\n    <div class="thumb">img</div>\n    <div class="body">text</div>\n  </article>\n</div>\n\n<style>\n  /* container setup + @container rule */\n</style>\n',
    [
        css_test(
            "slot is a size container",
            [
                (r'\.slot\s*{[^}]*container-type\s*:\s*inline-size', "Mark .slot with container-type: inline-size."),
            ],
            "container-type: inline-size;",
        ),
        css_test(
            "card switches to two columns inside the container query",
            [
                (r'@container\s*\([^)]*min-width\s*:\s*420px[^)]*\)', "Add @container (min-width: 420px)."),
                (r'@container[^{]*{[^@]*\.card\s*{[^}]*grid-template-columns\s*:\s*120px\s+1fr', "Inside the query, .card uses grid-template-columns: 120px 1fr."),
                (r'^(?!.*@media)', "No @media anywhere — containers do the adapting."),
            ],
            "@container (min-width: 420px) { .card { display: grid; grid-template-columns: 120px 1fr; } }",
        ),
    ],
    "guided",
    {
        "title": "Card responsive theo container",
        "prompt": "Biến `.slot` thành size container, rồi bên trong `@container (min-width: 420px)` cho `.card` grid hai cột (`120px 1fr`). Nhỏ hơn mức đó, card vẫn một cột — tất cả không cần media query.",
        "tests": [
            {"name": "slot là size container", "hint": "container-type: inline-size;"},
            {"name": "card đổi sang hai cột bên trong container query", "hint": "@container (min-width: 420px) { .card { display: grid; grid-template-columns: 120px 1fr; } }"},
        ],
    },
)
write_practice(
    MOD, "container-practice",
    "Container Queries — Practice",
    "Components that adapt to their own box: a container-responsive card and fluid type with clamp().",
    "Container Queries — Luyện tập",
    "Component tự thích ứng với hộp của nó: card responsive theo container và chữ động với clamp().",
    "container-queries", 15, "intermediate",
    [ch4],
    { "i2-container-card": vi4 },
    [
        ["i2-container-card",
         '.slot { container-type: inline-size; }\n@container (min-width: 420px) {\n  .card {\n    display: grid;\n    grid-template-columns: 120px 1fr;\n  }\n}',
         '.slot {}\n.card { display: grid; grid-template-columns: 120px 1fr; }'],
    ],
)

# ── components-practice (JS logic) ──────────────────────────────────────────
write_practice(
    MOD, "components-practice",
    "Component Systems — Practice",
    "State machines for real widgets: a disclosure, a sortable-table reducer, and a focus-trap plan as pure logic.",
    "Hệ thống Component — Luyện tập",
    "Máy trạng thái cho widget thật: một disclosure, reducer cho bảng sắp xếp, và kế hoạch focus-trap dưới dạng logic thuần.",
    "component-states-a11y", 20, "intermediate",
    [
        {
            "id": "i2-disclosure",
            "title": "Disclosure Widget Logic",
            "prompt": "Write `createDisclosure()` returning `{ toggle, isOpen, state }`: internal `open` boolean starts false; `toggle()` flips it and RETURNS the new state string (`\"expanded\"`/`\"collapsed\"`); `state()` returns `{ open, ariaExpanded: open ? \"true\" : \"false\", hidden: !open }` — exactly the attributes a real widget would set.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function createDisclosure() {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "toggle flips and reports the state",
                    "code": fn_wrap("createDisclosure", "createDisclosure") + "\nconst d = createDisclosure();\nif (d.isOpen()) throw new Error(\"Starts closed.\");\nif (d.toggle() !== \"expanded\") throw new Error(\"First toggle returns 'expanded'.\");\nif (!d.isOpen()) throw new Error(\"Now open.\");\nif (d.toggle() !== \"collapsed\") throw new Error(\"Second toggle returns 'collapsed'.\");",
                    "hint": "A closure over one boolean.",
                },
                {
                    "name": "state exposes the accessibility attributes",
                    "code": fn_wrap("createDisclosure", "createDisclosure") + "\nconst d = createDisclosure();\nlet s = d.state();\nif (s.ariaExpanded !== \"false\" || s.hidden !== true) throw new Error(\"Closed: aria-expanded 'false', hidden true.\");\nd.toggle();\ns = d.state();\nif (s.ariaExpanded !== \"true\" || s.hidden !== false) throw new Error(\"Open: aria-expanded 'true', hidden false.\");",
                    "hint": "aria-* attributes are strings; hidden is boolean.",
                },
            ],
        },
        {
            "id": "i2-sort-reducer",
            "title": "Sortable Table Reducer",
            "prompt": "Write `sortRows(rows, key, dir)` that RETURNS rows sorted by `key` (`\"asc\"` or `\"desc\"`, numbers and strings both supported) WITHOUT mutating the input, and `nextSortDir(current)` that cycles `\"asc\" → \"desc\" → \"asc\"`. Stability: equal keys keep their original order.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function sortRows(rows, key, dir) {\n  // your code\n}\n\nfunction nextSortDir(current) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "sorts asc and desc without mutating",
                    "code": fn_wrap("sortRows, nextSortDir", "sortRows, nextSortDir") + "\nconst rows = [{ n: \"c\" }, { n: \"a\" }, { n: \"b\" }];\nconst asc = sortRows(rows, \"n\", \"asc\");\nif (asc.map((r) => r.n).join() !== \"a,b,c\") throw new Error(\"Ascending order.\");\nif (rows.map((r) => r.n).join() !== \"c,a,b\") throw new Error(\"The input array must stay untouched.\");\nconst desc = sortRows(rows, \"n\", \"desc\");\nif (desc.map((r) => r.n).join() !== \"c,b,a\") throw new Error(\"Descending order.\");\nif (nextSortDir(\"asc\") !== \"desc\" || nextSortDir(\"desc\") !== \"asc\") throw new Error(\"Direction cycles.\");",
                    "hint": "[...rows].sort((a, b) => dir === 'asc' ? cmp(a,b) : cmp(b,a)) with a comparison that handles strings and numbers.",
                },
                {
                    "name": "stable for equal keys and numeric-safe",
                    "code": fn_wrap("sortRows, nextSortDir", "sortRows, nextSortDir") + "\nconst rows = [{ id: 1, n: 10 }, { id: 2, n: 9 }, { id: 3, n: 10 }];\nconst out = sortRows(rows, \"n\", \"asc\");\nif (out.map((r) => r.id).join() !== \"2,1,3\") throw new Error(\"Equal keys (10) keep original order: 1 before 3.\");",
                    "hint": "Return cmp !== 0 ? cmp : 0 — Array.sort is stable in modern engines.",
                },
            ],
        },
        {
            "id": "i2-focus-plan",
            "title": "Modal Focus Plan",
            "prompt": "Write `focusPlan({ focusables, currentIndex })` returning the NEXT index when Tab is pressed forward and the PREVIOUS when Shift+Tab (`{ forward }` is boolean). Wrap around at both ends. Also return `restoreTo` — always the value passed as `restoreIndex` (the opener) in the result object.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function focusPlan({ focusables, currentIndex, forward, restoreIndex }) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "moves forward and back with wrap-around",
                    "code": fn_wrap("focusPlan", "focusPlan") + "\nconst f = { focusables: 3, currentIndex: 0, forward: true, restoreIndex: 9 };\nif (focusPlan(f).next !== 1) throw new Error(\"Tab from 0 goes to 1.\");\nif (focusPlan({ ...f, currentIndex: 2 }).next !== 0) throw new Error(\"Tab from the last wraps to 0.\");\nif (focusPlan({ ...f, forward: false, currentIndex: 0 }).next !== 2) throw new Error(\"Shift+Tab from 0 wraps to the last.\");",
                    "hint": "(currentIndex + (forward ? 1 : -1) + n) % n.",
                },
                {
                    "name": "always carries the restore target",
                    "code": fn_wrap("focusPlan", "focusPlan") + "\nconst out = focusPlan({ focusables: 3, currentIndex: 1, forward: true, restoreIndex: 7 });\nif (out.restoreTo !== 7) throw new Error(\"restoreTo must echo restoreIndex — the element to refocus on close.\");\nif (out.next !== 2) throw new Error(\"Normal next calculation still applies.\");",
                    "hint": "Return { next, restoreTo: restoreIndex }.",
                },
            ],
        },
    ],
    {
        "i2-disclosure": {
            "title": "Logic Disclosure Widget",
            "prompt": "Viết `createDisclosure()` trả về `{ toggle, isOpen, state }`: biến `open` bên trong khởi đầu false; `toggle()` đảo nó và RETURN chuỗi trạng thái mới (`\"expanded\"`/`\"collapsed\"`); `state()` trả về `{ open, ariaExpanded: open ? \"true\" : \"false\", hidden: !open }` — đúng những thuộc tính mà widget thật sẽ đặt.",
            "tests": [
                {"name": "toggle đảo và báo trạng thái", "hint": "Một closure trên một boolean."},
                {"name": "state bộc lộ các thuộc tính accessibility", "hint": "Thuộc tính aria-* là chuỗi; hidden là boolean."},
            ],
        },
        "i2-sort-reducer": {
            "title": "Reducer bảng sắp xếp",
            "prompt": "Viết `sortRows(rows, key, dir)` RETURN các dòng đã sắp theo `key` (`\"asc\"` hoặc `\"desc\"`, hỗ trợ cả số và chuỗi) KHÔNG làm thay đổi input, và `nextSortDir(current)` quay vòng `\"asc\" → \"desc\" → \"asc\"`. Ổn định: key bằng nhau giữ nguyên thứ tự gốc.",
            "tests": [
                {"name": "sắp asc và desc không đụng vào input", "hint": "[...rows].sort((a, b) => dir === 'asc' ? cmp(a,b) : cmp(b,a)) với hàm so sánh xử lý cả chuỗi lẫn số."},
                {"name": "ổn định với key bằng nhau và an toàn với số", "hint": "Return cmp !== 0 ? cmp : 0 — Array.sort ổn định trên các engine hiện đại."},
            ],
        },
        "i2-focus-plan": {
            "title": "Kế hoạch focus cho modal",
            "prompt": "Viết `focusPlan({ focusables, currentIndex })` trả về chỉ số TIẾP THEO khi Tab đi tới và chỉ số TRƯỚC khi Shift+Tab (`{ forward }` là boolean). Quay vòng ở cả hai đầu. Đồng thời trả về `restoreTo` — luôn là giá trị `restoreIndex` được truyền vào (phần tử mở) trong object kết quả.",
            "tests": [
                {"name": "di chuyển tới/lui với quay vòng", "hint": "(currentIndex + (forward ? 1 : -1) + n) % n."},
                {"name": "luôn mang theo đích khôi phục", "hint": "Return { next, restoreTo: restoreIndex }."},
            ],
        },
    },
    [
        ["i2-disclosure", "function createDisclosure() {\n  let open = false;\n  return {\n    toggle() {\n      open = !open;\n      return open ? \"expanded\" : \"collapsed\";\n    },\n    isOpen() {\n      return open;\n    },\n    state() {\n      return {\n        open,\n        ariaExpanded: open ? \"true\" : \"false\",\n        hidden: !open,\n      };\n    },\n  };\n}", "function createDisclosure() {\n  let open = true;\n  return {\n    toggle() { open = !open; return \"expanded\"; },\n    isOpen() { return open; },\n    state() { return { open, ariaExpanded: \"true\", hidden: false }; },\n  };\n}"],
        ["i2-sort-reducer", "function sortRows(rows, key, dir) {\n  return [...rows].sort((a, b) => {\n    const av = a[key];\n    const bv = b[key];\n    let cmp;\n    if (typeof av === \"number\" && typeof bv === \"number\") {\n      cmp = av - bv;\n    } else {\n      cmp = String(av).localeCompare(String(bv));\n    }\n    return dir === \"asc\" ? cmp : -cmp;\n  });\n}\nfunction nextSortDir(current) {\n  return current === \"asc\" ? \"desc\" : \"asc\";\n}", "function sortRows(rows, key, dir) {\n  rows.sort((a, b) => (a[key] > b[key] ? 1 : -1));\n  return rows;\n}\nfunction nextSortDir(current) {\n  return \"asc\";\n}"],
        ["i2-focus-plan", "function focusPlan({ focusables, currentIndex, forward, restoreIndex }) {\n  const n = focusables;\n  const next = (currentIndex + (forward ? 1 : -1) + n) % n;\n  return { next, restoreTo: restoreIndex };\n}", "function focusPlan({ focusables, currentIndex, forward, restoreIndex }) {\n  return { next: forward ? currentIndex + 1 : currentIndex - 1, restoreTo: restoreIndex };\n}"],
    ],
)

# ── motion-practice ─────────────────────────────────────────────────────────
ch5, vi5 = css_challenge(
    "i2-motion-reduced",
    "Motion That Respects Preferences",
    "Give `.panel` a transform-based open/close transition (`transform 0.25s`), then add a `prefers-reduced-motion: reduce` block that effectively disables animation and transition durations globally.",
    '<style>\n  .panel {\n    /* transition on transform */\n  }\n  .panel.is-closed {\n    /* closed state */\n  }\n\n  /* reduced motion block */\n</style>\n',
    [
        css_test(
            "transform transition with a duration",
            [
                (r'\.panel\s*{[^}]*transition\s*:[^;}]*transform', "Transition the transform property."),
                (r'\.panel\s*{[^}]*transition\s*:[^;}]*0?\.?\d+m?s', "The transition needs a duration (e.g. 0.25s)."),
                (r'\.panel\.is-closed\s*{[^}]*transform\s*:', "The closed state moves via transform (e.g. translateX(-100%))."),
            ],
            ".panel { transition: transform 0.25s ease; } .panel.is-closed { transform: translateX(-100%); }",
        ),
        css_test(
            "reduced-motion block neutralizes durations",
            [
                (r'@media\s*\(\s*prefers-reduced-motion\s*:\s*reduce\s*\)', "Add the prefers-reduced-motion: reduce media query."),
                (r'@media\s*\(\s*prefers-reduced-motion\s*:\s*reduce\s*\)[^{]*{[\s\S]*animation-duration', "Neutralize animation-duration inside the block."),
                (r'@media\s*\(\s*prefers-reduced-motion\s*:\s*reduce\s*\)[^{]*{[\s\S]*transition-duration', "Neutralize transition-duration inside the block."),
            ],
            "@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }",
        ),
    ],
    "guided",
    {
        "title": "Chuyển động tôn trọng tùy chọn",
        "prompt": "Cho `.panel` một transition mở/đóng dựa trên transform (`transform 0.25s`), rồi thêm khối `prefers-reduced-motion: reduce` vô hiệu hóa hiệu quả thời lượng animation và transition trên toàn cục.",
        "tests": [
            {"name": "transition transform với thời lượng", "hint": ".panel { transition: transform 0.25s ease; } .panel.is-closed { transform: translateX(-100%); }"},
            {"name": "khối reduced-motion vô hiệu thời lượng", "hint": "@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }"},
        ],
    },
)
write_practice(
    MOD, "motion-practice",
    "Motion — Practice",
    "Cheap, considerate animation: a transform-driven drawer and a global reduced-motion policy.",
    "Chuyển động — Luyện tập",
    "Animation rẻ và tinh tế: drawer dẫn động bằng transform và chính sách reduced-motion toàn cục.",
    "motion-reduced-motion", 12, "intermediate",
    [ch5],
    { "i2-motion-reduced": vi5 },
    [
        ["i2-motion-reduced",
         '.panel {\n  transition: transform 0.25s ease;\n}\n.panel.is-closed {\n  transform: translateX(-100%);\n}\n@media (prefers-reduced-motion: reduce) {\n  *, *::before, *::after {\n    animation-duration: 0.01ms !important;\n    transition-duration: 0.01ms !important;\n  }\n}',
         '.panel {\n  transition: width 0.25s;\n}\n.panel.is-closed {\n  width: 0;\n}'],
    ],
)

# ── dashboard-build-practice (mini build, JS) ───────────────────────────────
write_practice(
    MOD, "dashboard-build-practice",
    "Mini Build: Themeable Dashboard Core",
    "Compose the module: a token resolver driving a theme reducer and a widget-layout planner.",
    "Dự án nhỏ: Lõi Dashboard có thể đổi theme",
    "Kết hợp cả module: bộ phân giải token dẫn động reducer theme và bộ lên kế hoạch layout widget.",
    "ui-system-checkpoint", 22, "intermediate",
    [
        {
            "id": "i2-dash-tokens",
            "title": "Token Pipeline",
            "prompt": "Write `buildTheme(base, overrides)` returning the merged token object (`overrides` wins), plus `tokenValue(tokens, path, fallback)` where `path` is dot-separated (e.g. `\"color.bg\"`) resolving nested tokens; return `fallback` for missing paths.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function buildTheme(base, overrides) {\n  // your code\n}\n\nfunction tokenValue(tokens, path, fallback) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "merge with override priority",
                    "code": fn_wrap("buildTheme, tokenValue", "buildTheme, tokenValue") + "\nconst t = buildTheme({ color: { bg: \"white\" }, radius: 8 }, { color: { bg: \"black\" } });\nif (t.color.bg !== \"black\") throw new Error(\"Override wins on conflicts.\");\nif (t.color !== undefined && t.color.radius !== undefined) throw new Error(\"Only specified keys change.\");\nif (t.radius !== 8) throw new Error(\"Unrelated tokens survive.\");",
                    "hint": "Shallow merge is fine unless both values are plain objects — then merge recursively one level per call.",
                },
                {
                    "name": "dot-path resolution with fallback",
                    "code": fn_wrap("buildTheme, tokenValue", "buildTheme, tokenValue") + "\nconst tokens = { color: { bg: \"#fff\", fg: { base: \"#000\" } } };\nif (tokenValue(tokens, \"color.bg\") !== \"#fff\") throw new Error(\"Two-segment path.\");\nif (tokenValue(tokens, \"color.fg.base\") !== \"#000\") throw new Error(\"Three-segment path.\");\nif (tokenValue(tokens, \"color.missing\", \"gray\") !== \"gray\") throw new Error(\"Missing paths return the fallback.\");",
                    "hint": "path.split('.').reduce((o, k) => (o == null ? o : o[k]), tokens) ?? fallback.",
                },
            ],
        },
        {
            "id": "i2-widget-planner",
            "title": "Widget Layout Planner",
            "prompt": "Write `planLayout(widgets, cols)` distributing `widgets` (array of ids) into `cols` columns row-major (like CSS grid auto-placement): RETURN an array of `cols` arrays. `place(widgets, cols, index)` additionally returns the row/column of the widget at `index` as `{ row, col }` (both 0-based).",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function planLayout(widgets, cols) {\n  // your code\n}\n\nfunction place(widgets, cols, index) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "row-major distribution",
                    "code": fn_wrap("planLayout, place", "planLayout, place") + "\nconst cols = planLayout([\"a\", \"b\", \"c\", \"d\", \"e\"], 2);\nif (cols.length !== 2) throw new Error(\"Two column buckets.\");\nif (cols[0].join() !== \"a,c,e\" || cols[1].join() !== \"b,d\") throw new Error(\"Row-major: a b / c d / e — column 0 gets a,c,e.\");",
                    "hint": "cols[i % cols].push(widget) walking the list.",
                },
                {
                    "name": "row and column of an index",
                    "code": fn_wrap("planLayout, place", "planLayout, place") + "\nif (place([\"a\",\"b\",\"c\",\"d\",\"e\"], 2, 3).row !== 1 || place([\"a\",\"b\",\"c\",\"d\",\"e\"], 2, 3).col !== 1) throw new Error(\"Index 3 at 2 cols: row 1, col 1.\");\nif (place([\"a\",\"b\",\"c\",\"d\",\"e\"], 3, 4).row !== 1 || place([\"a\",\"b\",\"c\",\"d\",\"e\"], 3, 4).col !== 1) throw new Error(\"Index 4 at 3 cols: row 1, col 1.\");",
                    "hint": "row = Math.floor(index / cols); col = index % cols.",
                },
            ],
        },
    ],
    {
        "i2-dash-tokens": {
            "title": "Đường ống token",
            "prompt": "Viết `buildTheme(base, overrides)` trả về object token đã hợp nhất (`overrides` thắng), cộng `tokenValue(tokens, path, fallback)` trong đó `path` phân tách bằng dấu chấm (ví dụ `\"color.bg\"`) truy cập token lồng nhau; trả về `fallback` cho path không tồn tại.",
            "tests": [
                {"name": "hợp nhất với độ ưu tiên override", "hint": "Gộp nông là đủ trừ khi cả hai giá trị đều là object thường — khi đó gộp đệ quy một cấp mỗi lần gọi."},
                {"name": "phân giải path chấm với fallback", "hint": "path.split('.').reduce((o, k) => (o == null ? o : o[k]), tokens) ?? fallback."},
            ],
        },
        "i2-widget-planner": {
            "title": "Bộ lên kế hoạch layout widget",
            "prompt": "Viết `planLayout(widgets, cols)` phân bổ `widgets` (mảng id) vào `cols` cột theo kiểu row-major (như auto-placement của CSS grid): RETURN một mảng gồm `cols` mảng con. `place(widgets, cols, index)` bổ sung trả về hàng/cột của widget tại `index` dạng `{ row, col }` (đều bắt đầu từ 0).",
            "tests": [
                {"name": "phân bổ row-major", "hint": "cols[i % số_cột].push(widget) khi đi qua danh sách."},
                {"name": "hàng và cột của một chỉ số", "hint": "row = Math.floor(index / cols); col = index % cols."},
            ],
        },
    },
    [
        ["i2-dash-tokens", "function buildTheme(base, overrides) {\n  const out = { ...base };\n  for (const k of Object.keys(overrides)) {\n    const b = base[k];\n    const o = overrides[k];\n    out[k] = b && o && typeof b === \"object\" && typeof o === \"object\"\n      ? buildTheme(b, o)\n      : o;\n  }\n  return out;\n}\nfunction tokenValue(tokens, path, fallback) {\n  const v = path.split(\".\").reduce((o, k) => (o == null ? undefined : o[k]), tokens);\n  return v === undefined ? fallback : v;\n}", "function buildTheme(base, overrides) {\n  return { ...base, ...overrides };\n}\nfunction tokenValue(tokens, path, fallback) {\n  return fallback;\n}"],
        ["i2-widget-planner", "function planLayout(widgets, cols) {\n  const buckets = Array.from({ length: cols }, () => []);\n  widgets.forEach((w, i) => buckets[i % cols].push(w));\n  return buckets;\n}\nfunction place(widgets, cols, index) {\n  return { row: Math.floor(index / cols), col: index % cols };\n}", "function planLayout(widgets, cols) {\n  return [widgets];\n}\nfunction place(widgets, cols, index) {\n  return { row: 0, col: index };\n}"],
    ],
)

print("Module 4 practices written.")
