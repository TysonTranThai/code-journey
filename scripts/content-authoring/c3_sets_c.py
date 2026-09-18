#!/usr/bin/env python3
"""Author Course 3 (Advanced HTML) practice sets — part C: sandboxed-embeds-metadata + docs-hub-project. EN + VI overlays."""
import json, os

BASE = "src/content/tracks/web-development/courses/web-development-advanced/modules/advanced-html/practices"


def w(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def challenge(set_id, cid, en, vi):
    d = f"{BASE}/{set_id}/challenges"
    w(f"{d}/{cid}.json", {"id": cid, **en})
    w(f"{d}/{cid}.vi.json", vi)


def pset(sid, title, vi_title, description, vi_description, after, minutes):
    w(f"{BASE}/{sid}.json", {
        "id": sid,
        "title": title,
        "description": description,
        "afterLesson": after,
        "minutes": minutes,
        "difficulty": "advanced",
        "challenges": [],
    })
    w(f"{BASE}/{sid}.vi.json", {"title": vi_title, "description": vi_description})


# ─────────────────── Set 6: sandboxed-embeds-metadata ───────────────────
pset(
    "sandboxed-embeds-metadata-practice",
    "Sandboxed Embeds & Metadata — Practice",
    "Nhúng an toàn & metadata — Luyện tập",
    "Choose sandbox tokens per embed scenario, build a complete machine-readable head, then debug an iframe shipped wide open.",
    "Chọn token sandbox theo từng tình huống nhúng, dựng một head máy đọc được hoàn chỉnh, rồi sửa một iframe bị ship không sandbox.",
    "sandboxed-embeds-metadata",
    25,
)

challenge(
    "sandboxed-embeds-metadata-practice",
    "i3-embed-sandbox",
    {
        "title": "Sandbox a Third-Party Widget",
        "prompt": "Embed a chat widget (https://chat.example.com/widget) that needs scripts and form submission only: iframe with sandbox=\"allow-scripts allow-forms\", a title, loading=\"lazy\", and explicit width/height. Then, below it, embed a trusted static report from YOUR OWN origin as <iframe src=\"report.html\" sandbox=\"allow-scripts allow-same-origin\"> (safe because it is first-party).",
        "difficulty": "advanced",
        "level": "guided",
        "boilerplate": "<!-- Two embeds, two policies -->\n\n",
        "tests": [
            {
                "name": "untrusted widget is least-privileged",
                "code": r"""const iframes = [...code.matchAll(/<iframe[^>]*>/gi)];
if (iframes.length < 2) throw new Error("Two iframes expected.");
const widget = iframes.find((m) => /chat\.example\.com/i.test(m[0]));
if (!widget) throw new Error("Keep the chat widget iframe.");
const s = (widget[0].match(/sandbox\s*=\s*["']([^"']*)["']/i) || [])[1] || "";
if (!/allow-scripts/i.test(s)) throw new Error("The widget needs allow-scripts to run.");
if (!/allow-forms/i.test(s)) throw new Error("The widget needs allow-forms for its input.");
const risky = s.split(/\s+/).filter((t) =>
  ["allow-same-origin", "allow-top-navigation", "allow-popups"].includes(t.toLowerCase())
);
if (risky.length > 0) {
  throw new Error("Grant only what the widget needs — drop " + risky.join(", ") + ".");
}""",
                "hint": "Least privilege: scripts + forms are the stated need; same-origin, top-navigation and popups are not.",
            },
            {
                "name": "widget has a name and dimensions",
                "code": r"""const widget = [...code.matchAll(/<iframe[^>]*>/gi)].find((m) => /chat\.example\.com/i.test(m[0]));
if (!widget) throw new Error("Keep the chat widget iframe.");
if (!/title\s*=\s*["'][^"']{4,}["']/i.test(widget[0])) {
  throw new Error("The iframe needs a descriptive title (its accessible name).");
}
if (!/width\s*=\s*["']\d+["']/i.test(widget[0]) || !/height\s*=\s*["']\d+["']/i.test(widget[0])) {
  throw new Error("Give the iframe explicit width and height.");
}""",
                "hint": "An unnamed frame announces only 'frame'; lazy loading without dimensions also causes layout shift.",
            },
            {
                "name": "first-party report keeps its origin",
                "code": r"""const report = [...code.matchAll(/<iframe[^>]*>/gi)].find((m) => /report\.html/i.test(m[0]));
if (!report) throw new Error("Keep the first-party report iframe.");
const s = (report[0].match(/sandbox\s*=\s*["']([^"']*)["']/i) || [])[1] || "";
if (!/allow-same-origin/i.test(s)) {
  throw new Error('The trusted report keeps allow-same-origin (it is first-party).');
}""",
                "hint": "Trust is the criterion: first-party content may keep its origin; third-party never does.",
            },
            {
                "name": "lazy where it belongs",
                "code": r"""const widget = [...code.matchAll(/<iframe[^>]*>/gi)].find((m) => /chat\.example\.com/i.test(m[0]));
if (!widget || !/loading\s*=\s*["']lazy["']/i.test(widget[0])) {
  throw new Error('The widget embed should carry loading="lazy".');
}""",
                "hint": "Third-party embeds are prime lazy-loading candidates — off-screen frames should not cost bytes.",
            },
        ],
    },
    {
        "title": "Sandbox một widget bên thứ ba",
        "prompt": "Nhúng một widget chat (https://chat.example.com/widget) chỉ cần script và gửi form: iframe với sandbox=\"allow-scripts allow-forms\", một title, loading=\"lazy\", và width/height tường minh. Sau đó, bên dưới, nhúng một báo cáo tĩnh tin cậy từ CHÍNH ORIGIN CỦA BẠN dạng <iframe src=\"report.html\" sandbox=\"allow-scripts allow-same-origin\"> (an toàn vì nó là first-party).",
        "tests": [
            {"name": "widget không tin cậy ở mức quyền tối thiểu", "hint": "Đặc quyền tối thiểu: script + form là nhu cầu nêu ra; same-origin, top-navigation và popup thì không."},
            {"name": "widget có tên và kích thước", "hint": "Khung không tên chỉ được đọc là 'frame'; lazy loading không có kích thước cũng gây layout shift."},
            {"name": "báo cáo first-party giữ origin của nó", "hint": "Tin cậy là tiêu chí: nội dung first-party có thể giữ origin; bên thứ ba thì không bao giờ."},
            {"name": "lazy đúng chỗ", "hint": "Embed bên thứ ba là ứng viên hàng đầu cho lazy loading — khung ngoài màn hình không nên tốn byte."},
        ],
    },
)

challenge(
    "sandboxed-embeds-metadata-practice",
    "i3-meta-head",
    {
        "title": "Build the Complete Head",
        "prompt": "Write the full <head> of the article page 'Kite CLI — Getting started' (https://docs.example.com/kite/getting-started): charset, viewport, title, meta description, canonical link, og:title + og:description + og:image (absolute URL), hreflang alternates for en and vi, and the same English version marked x-default.",
        "difficulty": "advanced",
        "level": "independent",
        "boilerplate": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <!-- build the rest of the head -->\n</head>\n<body></body>\n</html>\n",
        "tests": [
            {
                "name": "basics first",
                "code": r"""if (!/<meta[^>]*charset/i.test(code)) throw new Error("charset comes first.");
if (!/<meta[^>]*name\s*=\s*["']viewport["'][^>]*content\s*=\s*["'][^"']*width\s*=\s*device-width/i.test(code)) {
  throw new Error("viewport needs width=device-width.");
}
const t = code.match(/<title>([\s\S]*?)<\/title>/i);
if (!t || !t[1].trim()) throw new Error("Add a non-empty <title>.");""",
                "hint": "Encoding, viewport, title — the three tags every page needs before anything else.",
            },
            {
                "name": "canonical names this URL",
                "code": r"""const can = code.match(/<link[^>]*rel\s*=\s*["']canonical["'][^>]*>/i);
if (!can) throw new Error("Add a canonical link.");
if (!/https:\/\/docs\.example\.com\/kite\/getting-started/i.test(can[0])) {
  throw new Error("Canonical must point at THIS page's URL, not the site root.");
}""",
                "hint": "A canonical that points at the homepage consolidates the page away — name the page itself.",
            },
            {
                "name": "open graph trio with absolute image",
                "code": r"""if (!/<meta[^>]*property\s*=\s*["']og:title["']/i.test(code)) throw new Error("og:title missing.");
if (!/<meta[^>]*property\s*=\s*["']og:description["']/i.test(code)) throw new Error("og:description missing.");
const img = code.match(/<meta[^>]*property\s*=\s*["']og:image["'][^>]*content\s*=\s*["']([^"']+)["']/i);
if (!img) throw new Error("og:image missing.");
if (!/^https:\/\//i.test(img[1])) {
  throw new Error("og:image must be an absolute URL — crawlers fetch it out of context.");
}""",
                "hint": "Three OG tags, and the image URL must stand on its own: absolute, not relative.",
            },
            {
                "name": "hreflang alternates plus x-default",
                "code": r"""const en = [...code.matchAll(/<link[^>]*>/gi)].filter((m) => /hreflang\s*=\s*["']en["']/i.test(m[0]));
const vi = [...code.matchAll(/<link[^>]*>/gi)].filter((m) => /hreflang\s*=\s*["']vi["']/i.test(m[0]));
const xd = [...code.matchAll(/<link[^>]*>/gi)].filter((m) => /hreflang\s*=\s*["']x-default["']/i.test(m[0]));
if (en.length === 0) throw new Error('Add <link rel="alternate" hreflang="en">.');
if (vi.length === 0) throw new Error('Add <link rel="alternate" hreflang="vi">.');
if (xd.length === 0) throw new Error('Mark the default version with hreflang="x-default".');""",
                "hint": "Each locale declares itself, and x-default names the version for unmatched languages.",
            },
        ],
    },
    {
        "title": "Dựng head hoàn chỉnh",
        "prompt": "Viết trọn vẹn <head> của trang bài viết 'Kite CLI — Getting started' (https://docs.example.com/kite/getting-started): charset, viewport, title, meta description, canonical, og:title + og:description + og:image (URL tuyệt đối), các bản hreflang alternate cho en và vi, và phiên bản tiếng Anh cũng được đánh dấu x-default.",
        "tests": [
            {"name": "phần cơ bản trước tiên", "hint": "Encoding, viewport, title — ba thẻ mọi trang cần trước bất cứ thứ gì khác."},
            {"name": "canonical gọi tên URL này", "hint": "Canonical trỏ về trang chủ sẽ gộp mất trang — hãy gọi đúng tên chính trang đó."},
            {"name": "bộ ba open graph với ảnh tuyệt đối", "hint": "Ba thẻ OG, và URL ảnh phải tự đứng vững: tuyệt đối, không tương đối."},
            {"name": "hreflang alternate cộng x-default", "hint": "Mỗi locale tự tuyên bố, và x-default chỉ ra phiên bản cho ngôn ngữ không khớp."},
        ],
    },
)

challenge(
    "sandboxed-embeds-metadata-practice",
    "i3-meta-debug",
    {
        "title": "Debug: The Wide-Open Embed",
        "prompt": "This page embeds a comment widget with NO sandbox at all, the iframe has no title, and the page's robots meta blocks indexing of a page that should be public. Repair: add a least-privilege sandbox (the widget renders its comment form — scripts and forms), give the iframe a title, and switch robots to allow indexing but still crawl links (index, follow).",
        "difficulty": "advanced",
        "level": "debugging",
        "boilerplate": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Release notes — Widget</title>
  <meta name="robots" content="noindex, nofollow">
</head>
<body>
  <h1>Release notes</h1>
  <iframe src="https://comments.example.com/thread/42" width="600" height="400"></iframe>
</body>
</html>
""",
        "tests": [
            {
                "name": "widget is sandboxed",
                "code": r"""const f = code.match(/<iframe[^>]*>/i);
if (!f) throw new Error("Keep the embed.");
if (!/\bsandbox\b/i.test(f[0])) {
  throw new Error("The third-party embed must carry the sandbox attribute.");
}""",
                "hint": "No sandbox means full platform privileges for the guest — the first thing a reviewer would flag.",
            },
            {
                "name": "sandbox is least-privilege",
                "code": r"""const f = code.match(/<iframe[^>]*>/i);
const s = (f[0].match(/sandbox\s*=\s*["']([^"']*)["']/i) || [])[1] || "";
if (!/allow-scripts/i.test(s)) throw new Error("The widget needs allow-scripts.");
if (!/allow-forms/i.test(s)) throw new Error("Its comment form needs allow-forms.");
const extra = s.split(/\s+/).filter((t) =>
  ["allow-same-origin", "allow-top-navigation", "allow-popups"].includes(t.toLowerCase())
);
if (extra.length > 0) {
  throw new Error("Drop what it does not need: " + extra.join(", ") + ".");
}""",
                "hint": "Scripts + forms is the whole requirement — same-origin on third-party content is the escalation pair.",
            },
            {
                "name": "iframe has an accessible name",
                "code": r"""const f = code.match(/<iframe[^>]*>/i);
if (!/title\s*=\s*["'][^"']{4,}["']/i.test(f[0])) {
  throw new Error("Give the iframe a descriptive title attribute.");
}""",
                "hint": "Screen-reader users hear 'frame' and nothing else — title is the frame's name.",
            },
            {
                "name": "robots matches intent",
                "code": r"""const r = code.match(/<meta[^>]*name\s*=\s*["']robots["'][^>]*content\s*=\s*["']([^"']*)["']/i);
if (!r) throw new Error("Keep the robots meta.");
const v = r[1].toLowerCase();
if (/noindex/.test(v)) throw new Error("Release notes are public — drop noindex.");
if (/nofollow/.test(v)) throw new Error("Links should still be crawled — drop nofollow.");""",
                "hint": "Public page: 'index, follow' (or no robots meta at all) matches the intent.",
            },
        ],
    },
    {
        "title": "Debug: embed nguyên trạng",
        "prompt": "Trang này nhúng một widget bình luận KHÔNG hề có sandbox, iframe không có title, và meta robots đang chặn chỉ mục một trang lẽ ra phải công khai. Sửa lại: thêm sandbox tối thiểu quyền (widget hiển thị form bình luận — script và form), cấp title cho iframe, và đổi robots sang cho phép chỉ mục nhưng vẫn đi qua liên kết (index, follow).",
        "tests": [
            {"name": "widget được sandbox", "hint": "Không sandbox nghĩa là vị khách được toàn quyền nền tảng — điều đầu tiên người review sẽ phanh phui."},
            {"name": "sandbox ở mức quyền tối thiểu", "hint": "Script + form là toàn bộ yêu cầu — same-origin trên nội dung bên thứ ba chính là cặp leo thang."},
            {"name": "iframe có tên truy cập được", "hint": "Người dùng trình đọc màn hình chỉ nghe 'frame' và không gì nữa — title chính là tên của khung."},
            {"name": "robots đúng ý đồ", "hint": "Trang công khai: 'index, follow' (hoặc bỏ hẳn robots meta) mới khớp ý đồ."},
        ],
    },
)

# ─────────────────── Set 7: docs-hub-project ───────────────────
pset(
    "docs-hub-project-practice",
    "Project: Documentation Hub — Practice",
    "Dự án: Trung tâm tài liệu — Luyện tập",
    "Three decision-verification challenges grade your Documentation Hub artifact, layer by layer: document + architecture, interactive + media, enhancement + metadata.",
    "Ba thử thách quyết định-đối chiếu chấm sản phẩm Trung tâm tài liệu của bạn theo từng tầng: tài liệu + kiến trúc, tương tác + media, nâng cấp + metadata.",
    "docs-hub-project",
    25,
)

challenge(
    "docs-hub-project-practice",
    "i3-project-doc-layer",
    {
        "title": "Project Grade: Document + Architecture",
        "prompt": "GRADED PROJECT CHECKPOINT — build your Documentation Hub page for 'Kite CLI' now (one HTML file), satisfying the document and architecture layers: complete head (charset, viewport, non-empty title, description, canonical https://docs.example.com/kite/, og:title + og:image absolute), one <h1>, no skipped heading levels, <time datetime>, header/nav/main/footer landmarks, nav fragment links resolving to real ids, an <article aria-labelledby> named by a real heading id, footer contact inside <address>.",
        "difficulty": "advanced",
        "level": "real-world",
        "boilerplate": "<!-- Documentation Hub: document + architecture layer -->\n\n",
        "tests": [
            {
                "name": "head is machine-readable",
                "code": r"""if (!/<!DOCTYPE\s+html>/i.test(code)) throw new Error("Start with <!DOCTYPE html>.");
if (!/<html[^>]*\slang\s*=/i.test(code)) throw new Error("<html> needs a lang attribute.");
if (!/<meta[^>]*charset/i.test(code)) throw new Error("charset missing.");
if (!/<meta[^>]*name\s*=\s*["']viewport["']/i.test(code)) throw new Error("viewport missing.");
const t = code.match(/<title>([\s\S]*?)<\/title>/i);
if (!t || !t[1].trim()) throw new Error("Add a non-empty <title>.");
if (!/<meta[^>]*name\s*=\s*["']description["']/i.test(code)) throw new Error("meta description missing.");
if (!/<link[^>]*rel\s*=\s*["']canonical["'][^>]*docs\.example\.com\/kite\//i.test(code)) {
  throw new Error("Canonical link to https://docs.example.com/kite/… is missing.");
}
if (!/<meta[^>]*property\s*=\s*["']og:title["']/i.test(code)) throw new Error("og:title missing.");
const og = code.match(/<meta[^>]*property\s*=\s*["']og:image["'][^>]*content\s*=\s*["']([^"']+)["']/i);
if (!og || !/^https:\/\//i.test(og[1])) {
  throw new Error("og:image must exist and be an absolute URL.");
}""",
                "hint": "Work through the head checklist in order: encoding, viewport, title, description, canonical, OG pair.",
            },
            {
                "name": "heading architecture is sound",
                "code": r"""const h1s = (code.match(/<h1[\s>]/gi) || []).length;
if (h1s !== 1) throw new Error("Exactly one <h1> (found " + h1s + ").");
const levels = [...code.matchAll(/<h([1-6])[\s>]/gi)].map((m) => Number(m[1]));
let prev = 0;
for (const level of levels) {
  if (level > prev + 1) {
    throw new Error("Heading levels must not skip (h" + prev + " followed by h" + level + ").");
  }
  prev = level;
}
if (!/<time[^>]*\bdatetime\s*=\s*["']\d{4}-\d{2}-\d{2}["']/i.test(code)) {
  throw new Error("Mark the last-updated date with <time datetime=\"YYYY-MM-DD\">.");
}""",
                "hint": "One h1, monotone descent, and the date gets a machine-readable datetime.",
            },
            {
                "name": "landmarks and resolved nav links",
                "code": r"""for (const tag of ["header", "nav", "main", "footer"]) {
  if (!new RegExp("<" + tag + "[\\s>]").test(code)) {
    throw new Error("Missing <" + tag + "> landmark.");
  }
}
const nav = code.match(/<nav[\s>][\s\S]*?<\/nav>/i);
if (!nav) throw new Error("Keep the <nav>.");
const frags = nav[0].match(/href\s*=\s*["']#[^"']+["']/gi) || [];
if (frags.length < 2) throw new Error("The nav needs at least two fragment links.");
const ids = [...code.matchAll(/id\s*=\s*["']([^"']+)["']/gi)].map((m) => m[1]);
for (const f of frags) {
  const target = f.replace(/href\s*=\s*["']#/, "").replace(/["']/g, "");
  if (!ids.includes(target)) {
    throw new Error("Nav link #" + target + " has no element with that id.");
  }
}""",
                "hint": "Four landmarks, and every table-of-contents link must land on a real id.",
            },
            {
                "name": "article named by heading, contact in address",
                "code": r"""const art = code.match(/<article[^>]*aria-labelledby\s*=\s*["']([^"']+)["'][^>]*>/i);
if (!art) throw new Error("The docs body should be an <article aria-labelledby=\"…\">.");
if (!new RegExp("<h[1-6][\\s>][^>]*id\\s*=\\s*[\"']" + art[1] + "[\"']").test(code)) {
  throw new Error('aria-labelledby "' + art[1] + '" must point at a real heading id.');
}
if (!/<address[\s>][\s\S]*?<\/address>/i.test(code)) {
  throw new Error("Put the contact line in <address> inside the footer.");
}""",
                "hint": "The article borrows its heading as a name; <address> holds contact info in the footer.",
            },
        ],
    },
    {
        "title": "Chấm dự án: Tầng tài liệu + kiến trúc",
        "prompt": "CHECKPOINT CHẤM DỰ ÁN — hãy dựng ngay trang Trung tâm tài liệu cho 'Kite CLI' (một file HTML), đạt tầng tài liệu và kiến trúc: head hoàn chỉnh (charset, viewport, title không rỗng, description, canonical https://docs.example.com/kite/, og:title + og:image tuyệt đối), một <h1>, không bỏ cấp heading, <time datetime>, các landmark header/nav/main/footer, liên kết fragment trong nav giải quyết được tới id thật, một <article aria-labelledby> được đặt tên bằng id heading thật, thông tin liên hệ trong <address> ở footer.",
        "tests": [
            {"name": "head máy đọc được", "hint": "Đi lần lượt theo danh mục head: encoding, viewport, title, description, canonical, cặp OG."},
            {"name": "kiến trúc heading vững chắc", "hint": "Một h1, đi xuống đều cấp, và ngày tháng nhận datetime máy đọc được."},
            {"name": "landmark và liên kết nav giải quyết được", "hint": "Bốn landmark, và mọi liên kết mục lục phải đáp xuống một id thật."},
            {"name": "article có tên, liên hệ trong address", "hint": "Article mượn heading làm tên; <address> giữ thông tin liên hệ trong footer."},
        ],
    },
)

challenge(
    "docs-hub-project-practice",
    "i3-project-media-layer",
    {
        "title": "Project Grade: Interactive + Media",
        "prompt": "GRADED PROJECT CHECKPOINT — add the interactive and media layers to your Documentation Hub: an FAQ of 3+ sibling <details name=\"faq\"> with non-empty summaries; a <dialog> destructive-action with aria-labelledby, autofocus on the safe button and a method=\"dialog\" form; a hero <picture> with avif + webp sources, JPEG fallback <img> with width/height and alt; a demo <iframe src=\"https://demo.kite.dev/embed\" sandbox=\"allow-scripts\" title loading=\"lazy\">.",
        "difficulty": "advanced",
        "level": "real-world",
        "boilerplate": "<!-- Documentation Hub: interactive + media layer -->\n\n",
        "tests": [
            {
                "name": "named FAQ accordion",
                "code": r"""const ds = [...code.matchAll(/<details([^>]*)>/gi)];
if (ds.length < 3) throw new Error("The FAQ needs at least three <details> items.");
const names = ds.map((m) => (m[1].match(/name\s*=\s*["']([^"']*)["']/i) || [])[1]);
if (names.some((n) => !n)) throw new Error("Every FAQ item needs a name attribute.");
if ([...new Set(names)].length !== 1) {
  throw new Error("All FAQ items must share ONE name value.");
}
const sums = [...code.matchAll(/<summary[^>]*>([\s\S]*?)<\/summary>/gi)].map((m) =>
  m[1].replace(/<[^>]*>/g, "").trim()
);
if (sums.length < 3 || sums.some((s) => !s)) {
  throw new Error("Every <details> needs a non-empty <summary>.");
}""",
                "hint": "One shared name makes them an exclusive accordion; summaries carry the questions.",
            },
            {
                "name": "safe destructive dialog",
                "code": r"""if (!/<dialog[\s>]/i.test(code)) throw new Error("Add the destructive-action <dialog>.");
const dlg = code.match(/<dialog[^>]*>([\s\S]*?)<\/dialog>/i);
if (!dlg) throw new Error("Keep the <dialog>.");
if (!/aria-labelledby\s*=\s*["'][^"']+["']/i.test(dlg[0])) {
  throw new Error("Name the dialog with aria-labelledby.");
}
if (!/<form[^>]*method\s*=\s*["']dialog["']/i.test(dlg[0])) {
  throw new Error('Include a form method="dialog" inside it.');
}
const af = [...dlg[0].matchAll(/<button([^>]*)>([\s\S]*?)<\/button>/gi)].find((b) => /autofocus/i.test(b[1]));
if (!af) throw new Error("One button needs autofocus.");
if (/delete|remove/i.test(af[2].replace(/<[^>]*>/g, ""))) {
  throw new Error("autofocus belongs on the safe (Cancel) button.");
}""",
                "hint": "Named, form-closing, and focused on the safe action — the three dialog requirements.",
            },
            {
                "name": "format-fallback hero",
                "code": r"""const pic = code.match(/<picture[\s>][\s\S]*?<\/picture>/i);
if (!pic) throw new Error("The hero needs a <picture>.");
if (!/<source[^>]*type\s*=\s*["']image\/avif["']/i.test(pic[0])) throw new Error("AVIF source missing.");
if (!/<source[^>]*type\s*=\s*["']image\/webp["']/i.test(pic[0])) throw new Error("WebP source missing.");
const img = pic[0].match(/<img[^>]*>/i);
if (!img) throw new Error("The <picture> needs its fallback <img>.");
if (!/width\s*=\s*["']\d+["']/i.test(img[0]) || !/height\s*=\s*["']\d+["']/i.test(img[0])) {
  throw new Error("The fallback <img> needs width and height.");
}
const alt = (img[0].match(/alt\s*=\s*["']([^"']*)["']/i) || [])[1] || "";
if (alt.trim().length < 4) throw new Error("The hero <img> needs meaningful alt.");""",
                "hint": "Two modern sources, one honest fallback — dimensions and alt on the <img> only.",
            },
            {
                "name": "sandboxed demo embed",
                "code": r"""const f = [...code.matchAll(/<iframe[^>]*>/gi)].find((m) => /demo\.kite\.dev/i.test(m[0]));
if (!f) throw new Error('Add the demo iframe (src="https://demo.kite.dev/embed").');
const s = (f[0].match(/sandbox\s*=\s*["']([^"']*)["']/i) || [])[1] || "";
if (!/allow-scripts/i.test(s)) throw new Error("The demo needs allow-scripts.");
if (/allow-same-origin/i.test(s)) {
  throw new Error("Drop allow-same-origin — third-party demo content never keeps its origin.");
}
if (!/title\s*=\s*["'][^"']{4,}["']/i.test(f[0])) throw new Error("The iframe needs a title.");
if (!/loading\s*=\s*["']lazy["']/i.test(f[0])) throw new Error('The demo embed needs loading="lazy".');""",
                "hint": "Scripts only, named, lazy — the least-privilege third-party embed from the lesson.",
            },
        ],
    },
    {
        "title": "Chấm dự án: Tầng tương tác + media",
        "prompt": "CHECKPOINT CHẤM DỰ ÁN — thêm tầng tương tác và media vào Trung tâm tài liệu của bạn: một FAQ với 3+ phần tử <details name=\"faq\"> anh em có summary không rỗng; một <dialog> hành động phá hủy với aria-labelledby, autofocus trên nút an toàn và form method=\"dialog\"; một hero <picture> với các source avif + webp, <img> dự phòng JPEG mang width/height và alt; một <iframe src=\"https://demo.kite.dev/embed\" sandbox=\"allow-scripts\" title loading=\"lazy\"> demo.",
        "tests": [
            {"name": "accordion FAQ có tên", "hint": "Một name dùng chung biến chúng thành accordion loại trừ; summary mang các câu hỏi."},
            {"name": "dialog phá hủy an toàn", "hint": "Có tên, đóng bằng form, và focus nằm trên hành động an toàn — ba yêu cầu của dialog."},
            {"name": "hero dự phòng định dạng", "hint": "Hai source hiện đại, một bản dự phòng trung thực — kích thước và alt chỉ nằm trên <img>."},
            {"name": "embed demo có sandbox", "hint": "Chỉ script, có tên, lazy — embed bên thứ ba đặc quyền tối thiểu như bài học."},
        ],
    },
)

challenge(
    "docs-hub-project-practice",
    "i3-project-enhance-layer",
    {
        "title": "Project Grade: Enhancement + Metadata",
        "prompt": "GRADED PROJECT CHECKPOINT — finish your Documentation Hub: (1) a 'copy install command' affordance as progressive enhancement — a <details> disclosure containing the command in a <code> block (readable without JS) plus a button inside it with popovertarget-less text 'Copy' marked aria-label=\"Copy install command\"; (2) hreflang alternates for en and vi pointing at https://docs.example.com/en/ and /vi/ paths; (3) a <meta name=\"robots\"> that allows indexing.",
        "difficulty": "advanced",
        "level": "real-world",
        "boilerplate": "<!-- Documentation Hub: enhancement + metadata layer -->\n\n",
        "tests": [
            {
                "name": "install command readable without JS",
                "code": r"""const det = code.match(/<details[\s>][\s\S]*?<\/details>/i);
if (!det) throw new Error("Wrap the install command in a <details> disclosure.");
if (!/<code\b[^>]*>[^<]*(npm|npx|brew|pip|kite)[\s\S]*?<\/code>/i.test(det[0])) {
  throw new Error("Put the install command inside a <code> block in the disclosure.");
}
const sum = det[0].match(/<summary[^>]*>([\s\S]*?)<\/summary>/i);
if (!sum || !sum[1].replace(/<[^>]*>/g, "").trim()) {
  throw new Error("The disclosure needs a non-empty <summary>.");
}""",
                "hint": "A disclosure with the command in <code> works for everyone, script or no script.",
            },
            {
                "name": "copy affordance is named",
                "code": r"""const copy = [...code.matchAll(/<button([^>]*)>([\s\S]*?)<\/button>/gi)].find((b) =>
  /copy/i.test(b[2].replace(/<[^>]*>/g, "")) || /copy/i.test(b[1])
);
if (!copy) throw new Error("Add the Copy button.");
if (!/aria-label\s*=\s*["'][^"']*copy[^"']*["']/i.test(copy[1])) {
  throw new Error('Give the Copy button aria-label="Copy install command".');
}""",
                "hint": "A short 'Copy' button benefits from a fuller name — this is the one aria-label that adds information.",
            },
            {
                "name": "bilingual alternates declared",
                "code": r"""const en = [...code.matchAll(/<link[^>]*>/gi)].some((m) =>
  /hreflang\s*=\s*["']en["']/i.test(m[0]) && /docs\.example\.com\/en\//i.test(m[0])
);
const vi = [...code.matchAll(/<link[^>]*>/gi)].some((m) =>
  /hreflang\s*=\s*["']vi["']/i.test(m[0]) && /docs\.example\.com\/vi\//i.test(m[0])
);
if (!en) throw new Error('Add hreflang="en" pointing at the /en/ path.');
if (!vi) throw new Error('Add hreflang="vi" pointing at the /vi/ path.');""",
                "hint": "Each alternate names its locale AND its path — both must be right.",
            },
            {
                "name": "indexable",
                "code": r"""const r = code.match(/<meta[^>]*name\s*=\s*["']robots["'][^>]*content\s*=\s*["']([^"']*)["']/i);
if (r && /noindex/i.test(r[1])) {
  throw new Error("Docs are public — the robots meta must not say noindex.");
}""",
                "hint": "Either omit robots entirely or write index, follow — public documentation wants to be found.",
            },
        ],
    },
    {
        "title": "Chấm dự án: Tầng nâng cấp + metadata",
        "prompt": "CHECKPOINT CHẤM DỰ ÁN — hoàn thiện Trung tâm tài liệu của bạn: (1) nâng cấp tăng tiến cho 'copy install command' — một <details> chứa lệnh trong khối <code> (đọc được không cần JS) cộng một nút 'Copy' bên trong với aria-label=\"Copy install command\"; (2) các bản hreflang alternate cho en và vi trỏ tới đường dẫn https://docs.example.com/en/ và /vi/; (3) một <meta name=\"robots\"> cho phép chỉ mục.",
        "tests": [
            {"name": "lệnh cài đọc được không cần JS", "hint": "Một disclosure chứa lệnh trong <code> phục vụ được tất cả mọi người, có script hay không."},
            {"name": "nút copy được đặt tên", "hint": "Nút 'Copy' ngắn lợi từ một cái tên đầy đủ hơn — đây là aria-label hiếm hoi thực sự thêm thông tin."},
            {"name": "hai bản alternate song ngữ", "hint": "Mỗi alternate vừa gọi tên locale vừa gọi đúng đường dẫn — cả hai phải chuẩn."},
            {"name": "có thể được chỉ mục", "hint": "Hoặc bỏ hẳn robots hoặc viết index, follow — tài liệu công khai muốn được tìm thấy."},
        ],
    },
)

print("Part C done: sets 6-7 (6 challenges) written.")
