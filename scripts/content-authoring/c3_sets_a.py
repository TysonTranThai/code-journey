#!/usr/bin/env python3
"""Author Course 3 (Advanced HTML) practice sets — part A: html-architecture + accessible-names. EN + VI overlays."""
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


# ─────────────────────────── Set 1: html-architecture ───────────────────────────
pset(
    "html-architecture-practice",
    "Document Architecture — Practice",
    "Kiến trúc tài liệu — Luyện tập",
    "Rebuild a broken blog page's architecture, build an outline from requirements, and repair heading hacks.",
    "Kiến trúc lại một trang blog hỏng, dựng dàn ý từ yêu cầu, và sửa các cách hack heading.",
    "html-architecture",
    25,
)

DOC_SKELETON = r"""if (!/<!DOCTYPE\s+html>/i.test(code)) {
  throw new Error("Start with <!DOCTYPE html>.");
}
if (!/<html[^>]*\slang\s*=\s*["'][^"']+["']/i.test(code)) {
  throw new Error("<html> needs a lang attribute.");
}
if (!/<meta[^>]*charset/i.test(code)) {
  throw new Error('The head needs <meta charset="UTF-8">.');
}
const t = code.match(/<title>([\s\S]*?)<\/title>/i);
if (!t || !t[1].trim()) {
  throw new Error("Add a non-empty <title>.");
}"""

challenge(
    "html-architecture-practice",
    "i3-arch-rebuild",
    {
        "title": "Rebuild the Blog Architecture",
        "prompt": "Rebuild the blog page from the brief: complete document (doctype, html lang, charset, title); an <hgroup> wrapping the page <h1> and a subtitle (<p> or <span>); exactly one <h1>; heading levels never skip; a comments region as <section aria-labelledby=\"…\"> whose label is a real heading inside it; and a reader comment as a nested <article aria-labelledby=\"…\"> inside the post article. Content is yours — structure is graded.",
        "difficulty": "advanced",
        "level": "guided",
        "boilerplate": "<!-- Rebuild the blog page -->\n\n",
        "tests": [
            {
                "name": "complete document skeleton",
                "code": DOC_SKELETON,
                "hint": "Same skeleton as always: doctype, html lang, charset, title.",
            },
            {
                "name": "one h1 in an hgroup with a subtitle",
                "code": r"""const h1s = (code.match(/<h1[\s>]/gi) || []).length;
if (h1s !== 1) {
  throw new Error("Exactly one <h1> (found " + h1s + ").");
}
const hg = code.match(/<hgroup[\s>][\s\S]*?<\/hgroup>/i);
if (!hg) {
  throw new Error("Wrap the title and subtitle in an <hgroup>.");
}
if (!/<h1[\s>]/i.test(hg[0])) {
  throw new Error("The <hgroup> must contain the page <h1>.");
}
const sub = hg[0].replace(/<h1[\s>][\s\S]*?<\/h1>/i, "");
if (!/<(p|span)[\s>][^>]*>[^<]*\S/i.test(sub)) {
  throw new Error("Add a non-empty subtitle (<p> or <span>) inside the <hgroup>.");
}""",
                "hint": "The subtitle is part of the same heading — it lives in the hgroup, not in a new heading level.",
            },
            {
                "name": "outline never skips a level",
                "code": r"""const levels = [...code.matchAll(/<h([1-6])[\s>]/gi)].map((m) => Number(m[1]));
if (levels.length < 3) {
  throw new Error("The page needs at least three headings (h1 + section headings).");
}
let prev = 0;
for (const level of levels) {
  if (level > prev + 1) {
    throw new Error("Heading levels must not skip (h" + prev + " followed by h" + level + ").");
  }
  prev = level;
}""",
                "hint": "Walk the headings in document order: each one may step down at most one level from the previous.",
            },
            {
                "name": "comments region labelled by its heading",
                "code": r"""const sec = code.match(/<section[^>]*aria-labelledby\s*=\s*["']([^"']+)["'][^>]*>([\s\S]*?)<\/section>/i);
if (!sec) {
  throw new Error('Give the comments region <section aria-labelledby="...">.');
}
const labelId = sec[1];
if (!new RegExp("id\\s*=\\s*[\"']" + labelId + "[\"']").test(sec[2])) {
  throw new Error('aria-labelledby "' + labelId + '" must point at an id inside this section.');
}
if (!new RegExp("<h[1-6][\\s>][^>]*id\\s*=\\s*[\"']" + labelId + "[\"']").test(sec[2])) {
  throw new Error("Point aria-labelledby at a real heading element inside the section.");
}""",
                "hint": "The section borrows its heading as its name: the id lives on the <h2> (or h3), not on a wrapper.",
            },
            {
                "name": "nested comment article named by its heading",
                "code": r"""const arts = [...code.matchAll(/<article([^>]*)>/gi)];
if (arts.length < 2) {
  throw new Error("Nest a comment <article> inside the post article (2 <article> tags expected).");
}
const inner = arts[arts.length - 1][1];
const m = inner.match(/aria-labelledby\s*=\s*["']([^"']+)["']/i);
if (!m) {
  throw new Error("Name the comment article with aria-labelledby.");
}
if (!new RegExp("id\\s*=\\s*[\"']" + m[1] + "[\"']").test(code)) {
  throw new Error('aria-labelledby points at missing id "' + m[1] + '".');
}""",
                "hint": "The innermost article is the comment — it needs its own aria-labelledby pointing at its heading's id.",
            },
        ],
    },
    {
        "title": "Kiến trúc lại trang blog",
        "prompt": "Dựng lại trang blog theo đề bài: tài liệu hoàn chỉnh (doctype, html lang, charset, title); một <hgroup> bọc <h1> của trang và một dòng phụ (<p> hoặc <span>); đúng một <h1>; heading không bỏ cấp; vùng bình luận là <section aria-labelledby=\"…\"> được đặt tên bằng một heading thật bên trong; và một bình luận là <article aria-labelledby=\"…\"> lồng trong article của bài viết. Nội dung tùy bạn — cấu trúc được chấm điểm.",
        "tests": [
            {"name": "bộ xương tài liệu hoàn chỉnh", "hint": "Bộ xương quen thuộc: doctype, html lang, charset, title."},
            {"name": "một h1 trong hgroup kèm dòng phụ", "hint": "Dòng phụ là một phần của cùng heading — nó nằm trong hgroup, không phải một cấp heading mới."},
            {"name": "dàn ý không bỏ cấp", "hint": "Đi theo thứ tự heading trong tài liệu: mỗi heading chỉ được đi xuống tối đa một cấp so với cái trước."},
            {"name": "vùng bình luận được đặt tên bằng heading", "hint": "Section mượn heading làm tên: id nằm trên <h2> (hoặc h3), không phải trên một thùng bọc."},
            {"name": "article bình luận lồng và có tên", "hint": "Article sâu nhất chính là bình luận — nó cần aria-labelledby riêng trỏ vào id của heading của nó."},
        ],
    },
)

challenge(
    "html-architecture-practice",
    "i3-arch-outline",
    {
        "title": "Outline from Requirements",
        "prompt": "Build the heading skeleton of a field-guide page — headings only, filler content allowed: exactly one <h1>; exactly three <h2> chapters; exactly two <h3> sections under each chapter (six total); at least one <h4> inside the third chapter; a <footer>; every heading has visible text; levels never skip. Include the full document skeleton (doctype, lang, charset, title).",
        "difficulty": "advanced",
        "level": "independent",
        "boilerplate": "<!-- Field guide outline -->\n\n",
        "tests": [
            {
                "name": "complete document skeleton",
                "code": DOC_SKELETON,
                "hint": "Doctype, html lang, charset, title — the skeleton travels with every challenge now.",
            },
            {
                "name": "exact outline shape",
                "code": r"""const count = (re) => (code.match(re) || []).length;
const h1 = count(/<h1[\s>]/gi);
const h2 = count(/<h2[\s>]/gi);
const h3 = count(/<h3[\s>]/gi);
const h4 = count(/<h4[\s>]/gi);
if (h1 !== 1) throw new Error("Exactly one <h1> (found " + h1 + ").");
if (h2 !== 3) throw new Error("Exactly three <h2> chapters (found " + h2 + ").");
if (h3 !== 6) throw new Error("Six <h3> sections — two per chapter (found " + h3 + ").");
if (h4 < 1) throw new Error("The third chapter needs at least one <h4>.");""",
                "hint": "Count before you write: 1 h1, 3 h2, 6 h3, and an h4 nested in chapter three.",
            },
            {
                "name": "no skips, no empty headings",
                "code": r"""const levels = [...code.matchAll(/<h([1-6])[\s>]/gi)].map((m) => Number(m[1]));
let prev = 0;
for (const level of levels) {
  if (level > prev + 1) {
    throw new Error("Heading levels must not skip (h" + prev + " followed by h" + level + ").");
  }
  prev = level;
}
const texts = [...code.matchAll(/<h[1-6]\b[^>]*>([\s\S]*?)<\/h[1-6]>/gi)].map((m) =>
  m[1].replace(/<[^>]*>/g, "").trim()
);
const empty = texts.filter((t) => !t).length;
if (empty > 0) {
  throw new Error("Every heading needs visible text (" + empty + " empty).");
}""",
                "hint": "Two habits in one check: monotone descent (never skip down) and no placeholder headings.",
            },
            {
                "name": "footer present",
                "code": r"""if (!/<footer[\s>][\s\S]*?<\/footer>/i.test(code)) {
  throw new Error("Add a <footer>.");
}""",
                "hint": "The page closes with a <footer> — the site name lives there.",
            },
        ],
    },
    {
        "title": "Dàn ý từ yêu cầu",
        "prompt": "Dựng bộ khung heading của một trang cẩm nang — chỉ heading, nội dung điền tùy ý: đúng một <h1>; đúng ba <h2> làm chương; đúng hai <h3> dưới mỗi chương (tổng sáu); ít nhất một <h4> trong chương thứ ba; một <footer>; mọi heading đều có văn bản hiển thị; không bỏ cấp. Kèm bộ xương tài liệu đầy đủ (doctype, lang, charset, title).",
        "tests": [
            {"name": "bộ xương tài liệu hoàn chỉnh", "hint": "Doctype, html lang, charset, title — bộ xương đi cùng mọi thử thách từ giờ."},
            {"name": "hình dáng dàn ý chính xác", "hint": "Đếm trước khi viết: 1 h1, 3 h2, 6 h3, và một h4 lồng trong chương ba."},
            {"name": "không bỏ cấp, không heading rỗng", "hint": "Hai thói quen trong một phép kiểm: đi xuống đều cấp và không có heading giữ chỗ."},
            {"name": "có footer", "hint": "Trang kết thúc bằng <footer> — tên site nằm ở đó."},
        ],
    },
)

challenge(
    "html-architecture-practice",
    "i3-arch-debug",
    {
        "title": "Debug: Heading Soup",
        "prompt": "This city-guide page was built by someone who styled first and architected never: two <h1>s, a skipped level, a div pretending to be a heading with role=\"heading\", and a <section> with no name. Repair the architecture: exactly one <h1>, no skipped levels, real heading elements only, and every <section> named via aria-labelledby pointing at a real heading inside it. Keep the document skeleton intact.",
        "difficulty": "advanced",
        "level": "debugging",
        "boilerplate": """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>City Guide</title></head>
<body>
  <h1>City Guide</h1>
  <h3>Old Town</h3>
  <div role="heading" aria-level="2">Districts</div>
  <section>
    <p>Cobbled streets and cafes.</p>
  </section>
  <h1>Food Scene</h1>
  <h2>Markets</h2>
  <article>
    <h3>Night market</h3>
    <p>Open Fridays.</p>
    <section>
      <h4>Getting there</h4>
      <p>Bus 12.</p>
    </section>
  </article>
</body>
</html>
""",
        "tests": [
            {
                "name": "exactly one h1",
                "code": r"""const h1s = (code.match(/<h1[\s>]/gi) || []).length;
if (h1s !== 1) {
  throw new Error("Exactly one <h1> (found " + h1s + ") — demote the second to an <h2>.");
}""",
                "hint": "'Food Scene' is a chapter of this page, not a new page — it becomes the second <h2>.",
            },
            {
                "name": "no skipped levels",
                "code": r"""const levels = [...code.matchAll(/<h([1-6])[\s>]/gi)].map((m) => Number(m[1]));
let prev = 0;
for (const level of levels) {
  if (level > prev + 1) {
    throw new Error("Heading levels must not skip (h" + prev + " followed by h" + level + ").");
  }
  prev = level;
}""",
                "hint": "h1 directly followed by h3 is the skip — 'Old Town' should be an h2.",
            },
            {
                "name": "no fake headings",
                "code": r"""if (/role\s*=\s*["']heading["']/i.test(code)) {
  throw new Error('Replace the role="heading" hack with a real heading element.');
}""",
                "hint": "The styled div is a symptom — make it the <h2> it always should have been.",
            },
            {
                "name": "every section is labelled",
                "code": r"""const secs = [...code.matchAll(/<section([^>]*)>/gi)];
if (secs.length === 0) {
  throw new Error("Keep the section — label it instead of deleting it.");
}
for (const s of secs) {
  const m = s[1].match(/aria-labelledby\s*=\s*["']([^"']+)["']/i);
  if (!m) {
    throw new Error("A <section> is missing aria-labelledby.");
  }
  if (!new RegExp("id\\s*=\\s*[\"']" + m[1] + "[\"']").test(code)) {
    throw new Error('aria-labelledby points at missing id "' + m[1] + '".');
  }
}""",
                "hint": "Each section borrows a heading: give the heading an id and reference it from the section's aria-labelledby.",
            },
        ],
    },
    {
        "title": "Debug: súp heading",
        "prompt": "Trang hướng dẫn thành phố này được dựng bởi người trình bày trước và kiến trúc sau: hai <h1>, một chỗ bỏ cấp, một div giả làm heading với role=\"heading\", và một <section> không có tên. Hãy sửa kiến trúc: đúng một <h1>, không bỏ cấp, chỉ dùng phần tử heading thật, và mọi <section> được đặt tên qua aria-labelledby trỏ vào một heading thật bên trong. Giữ nguyên bộ xương tài liệu.",
        "tests": [
            {"name": "đúng một h1", "hint": "'Food Scene' là một chương của trang này, không phải một trang mới — nó trở thành <h2> thứ hai."},
            {"name": "không bỏ cấp", "hint": "h1 đi thẳng vào h3 chính là chỗ bỏ cấp — 'Old Town' phải là h2."},
            {"name": "không heading giả", "hint": "Cái div được trình bày đẹp là triệu chứng — hãy biến nó thành <h2> mà nó vốn đáng là."},
            {"name": "mọi section đều có tên", "hint": "Mỗi section mượn một heading: cấp cho heading một id rồi tham chiếu từ aria-labelledby của section."},
        ],
    },
)

# ─────────────────────────── Set 2: accessible-names ───────────────────────────
pset(
    "accessible-names-practice",
    "Accessible Names — Practice",
    "Accessible name — Luyện tập",
    "Label icon buttons with hidden text, name landmark regions, then debug a form where every name is subtly broken.",
    "Đặt tên cho nút icon bằng văn bản ẩn, đặt tên cho các vùng landmark, rồi sửa một biểu mẫu mà mọi cái tên đều hỏng tinh vi.",
    "accessible-names",
    25,
)

challenge(
    "accessible-names-practice",
    "i3-name-icon-button",
    {
        "title": "Name the Icon Buttons",
        "prompt": "Build a toolbar with three icon-only buttons — close, search, settings — each named with aria-labelledby pointing at visually hidden text (use the hidden attribute or a class), each <svg> icon marked aria-hidden=\"true\". Add one normal text button labeled Save — which must NOT carry an aria-label (it names itself).",
        "difficulty": "advanced",
        "level": "guided",
        "boilerplate": "<!-- Toolbar -->\n\n",
        "tests": [
            {
                "name": "three icon-only buttons labelled",
                "code": r"""const btns = [...code.matchAll(/<button([^>]*)>([\s\S]*?)<\/button>/gi)];
let labelled = 0;
for (const b of btns) {
  const m = b[1].match(/aria-labelledby\s*=\s*["']([^"']+)["']/i);
  if (m) {
    labelled++;
    if (!new RegExp("id\\s*=\\s*[\"']" + m[1] + "[\"']").test(code)) {
      throw new Error('aria-labelledby points at missing id "' + m[1] + '".');
    }
    const vis = b[2].replace(/<[^>]*>/g, "").trim();
    if (vis) {
      throw new Error("An icon button still has visible text — move the label to hidden text.");
    }
  }
}
if (labelled < 3) {
  throw new Error("Three icon-only buttons need aria-labelledby (found " + labelled + ").");
}""",
                "hint": "Icon-only means the visible text is empty — the name must come from a hidden element via aria-labelledby.",
            },
            {
                "name": "hidden labels carry real words",
                "code": r"""const refs = [...code.matchAll(/aria-labelledby\s*=\s*["']([^"']+)["']/gi)].map((m) => m[1]);
if (refs.length === 0) {
  throw new Error("No aria-labelledby found.");
}
for (const ref of refs) {
  const el = new RegExp("id\\s*=\\s*[\"']" + ref + "[\"'][^>]*>([\\s\\S]*?)<", "i").exec(code);
  if (!el || !el[1].replace(/<[^>]*>/g, "").trim()) {
    throw new Error('The label for "' + ref + '" is empty — hidden text still needs words.');
  }
}""",
                "hint": "Hidden from sight, not from meaning: each referenced element must contain non-empty text.",
            },
            {
                "name": "icons silent to assistive tech",
                "code": r"""const svgs = [...code.matchAll(/<svg([^>]*)>/gi)];
if (svgs.length < 3) {
  throw new Error("Give each icon button an <svg> icon (3 expected).");
}
const unmarked = svgs.filter((s) => !/aria-hidden\s*=\s*["']true["']/i.test(s[1])).length;
if (unmarked > 0) {
  throw new Error(unmarked + " <svg> icon(s) are not aria-hidden — decorative icons must be silent.");
}""",
                "hint": "The icon is decoration; the hidden text is the name. aria-hidden=\"true\" keeps the icon out of the name.",
            },
            {
                "name": "text button names itself",
                "code": r"""const btns = [...code.matchAll(/<button([^>]*)>([\s\S]*?)<\/button>/gi)];
const save = btns.find((b) => /save/i.test(b[2].replace(/<[^>]*>/g, "")));
if (!save) {
  throw new Error("Add the 'Save' text button.");
}
if (/aria-label\s*=\s*["'][^"']+["']/i.test(save[1])) {
  throw new Error("The Save button names itself — remove the redundant aria-label.");
}""",
                "hint": "First rule of ARIA: a button with visible text already has a name — adding aria-label only risks a mismatch.",
            },
        ],
    },
    {
        "title": "Đặt tên cho nút icon",
        "prompt": "Dựng một thanh công cụ với ba nút chỉ có icon — close, search, settings — mỗi nút được đặt tên bằng aria-labelledby trỏ vào văn bản ẩn (dùng thuộc tính hidden hoặc class), mỗi icon <svg> được đánh dấu aria-hidden=\"true\". Thêm một nút văn bản bình thường mang nhãn Save — nút này KHÔNG được có aria-label (nó tự có tên).",
        "tests": [
            {"name": "ba nút icon có tên", "hint": "Icon-only nghĩa là văn bản hiển thị rỗng — tên phải đến từ một phần tử ẩn qua aria-labelledby."},
            {"name": "nhãn ẩn mang từ ngữ thật", "hint": "Ẩn khỏi mắt, không ẩn khỏi ý nghĩa: mỗi phần tử được tham chiếu phải chứa văn bản không rỗng."},
            {"name": "icon im lặng với công nghệ hỗ trợ", "hint": "Icon là trang trí; văn bản ẩn mới là tên. aria-hidden=\"true\" giữ icon khỏi lọt vào tên."},
            {"name": "nút văn bản tự có tên", "hint": "Quy tắc số một của ARIA: nút có văn bản hiển thị thì đã có tên — thêm aria-label chỉ tạo rủi ro lệch tên."},
        ],
    },
)

challenge(
    "accessible-names-practice",
    "i3-name-regions",
    {
        "title": "Name the Regions",
        "prompt": "Build a page with exactly two <nav> landmarks — 'Primary' and 'Footer' — distinguished by distinct aria-label values; a <main>; and two <section> regions, each named via aria-labelledby pointing at its own real heading. Exactly one <h1>. Full document skeleton included.",
        "difficulty": "advanced",
        "level": "independent",
        "boilerplate": "<!-- Two navs, two named sections -->\n\n",
        "tests": [
            {
                "name": "two navs with distinct names",
                "code": r"""const navs = [...code.matchAll(/<nav([^>]*)>/gi)];
if (navs.length !== 2) {
  throw new Error("Exactly two <nav> landmarks expected (found " + navs.length + ").");
}
const labels = navs.map((n) => {
  const m = n[1].match(/aria-label\s*=\s*["']([^"']*)["']/i);
  return m ? m[1].trim() : "";
});
if (labels.some((l) => !l)) {
  throw new Error("Both navs need an aria-label.");
}
if (labels[0].toLowerCase() === labels[1].toLowerCase()) {
  throw new Error("The two navs have identical names — distinguish them (Primary / Footer).");
}""",
                "hint": "Unnamed navs all announce 'navigation' — give each one its own aria-label.",
            },
            {
                "name": "main landmark present",
                "code": r"""if (!/<main[\s>][\s\S]*?<\/main>/i.test(code)) {
  throw new Error("Add a <main> landmark.");
}""",
                "hint": "The primary content lives in <main> — screen readers jump there first.",
            },
            {
                "name": "two sections named by headings",
                "code": r"""const secs = [...code.matchAll(/<section([^>]*)>/gi)].filter((s) =>
  /aria-labelledby/i.test(s[1])
);
if (secs.length < 2) {
  throw new Error("Two sections need aria-labelledby.");
}
for (const s of secs) {
  const m = s[1].match(/aria-labelledby\s*=\s*["']([^"']+)["']/i);
  const heading = new RegExp("<h[1-6][\\s>][^>]*id\\s*=\\s*[\"']" + m[1] + "[\"']").test(code);
  if (!heading) {
    throw new Error('Section aria-labelledby "' + m[1] + '" must point at a real heading id.');
  }
}""",
                "hint": "Borrow the visible heading: id on the <h2>, aria-labelledby on the <section>.",
            },
            {
                "name": "one h1 and skeleton",
                "code": r"""const h1s = (code.match(/<h1[\s>]/gi) || []).length;
if (h1s !== 1) throw new Error("Exactly one <h1> (found " + h1s + ").");
if (!/<!DOCTYPE\s+html>/i.test(code)) throw new Error("Start with <!DOCTYPE html>.");
if (!/<html[^>]*\slang\s*=/i.test(code)) throw new Error("<html> needs a lang attribute.");""",
                "hint": "One page, one h1 — the landmarks do not change that.",
            },
        ],
    },
    {
        "title": "Đặt tên cho các vùng",
        "prompt": "Dựng một trang với đúng hai <nav> landmark — 'Primary' và 'Footer' — phân biệt bằng hai giá trị aria-label khác nhau; một <main>; và hai vùng <section>, mỗi vùng được đặt tên qua aria-labelledby trỏ vào heading thật của chính nó. Đúng một <h1>. Kèm bộ xương tài liệu đầy đủ.",
        "tests": [
            {"name": "hai nav với hai tên khác nhau", "hint": "Nav không tên đều được đọc là 'navigation' — cho mỗi cái một aria-label riêng."},
            {"name": "có landmark main", "hint": "Nội dung chính nằm trong <main> — trình đọc màn hình nhảy tới đó đầu tiên."},
            {"name": "hai section được đặt tên bằng heading", "hint": "Mượn heading hiển thị: id trên <h2>, aria-labelledby trên <section>."},
            {"name": "một h1 và bộ xương", "hint": "Một trang, một h1 — các landmark không làm thay đổi điều đó."},
        ],
    },
)

challenge(
    "accessible-names-practice",
    "i3-name-debug",
    {
        "title": "Debug: Broken Names",
        "prompt": "This checkout page's names are quietly broken: the cards image has empty alt, the email label never associates with its field, the promo label's for= points at the wrong id, 'Pay now' is a div role=\"button\", and 'Buy now' hides its visible text behind a conflicting aria-label. Fix every name the right way: real alt text, for/id association, a real <button>, and visible text as the source of truth.",
        "difficulty": "advanced",
        "level": "debugging",
        "boilerplate": """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Checkout</title></head>
<body>
  <h1>Checkout</h1>
  <img src="cards.png" alt="">
  <form>
    <label>Email address</label>
    <input id="email" type="email">
    <label for="promo">Promo code</label>
    <input id="promocode" type="text">
    <div role="button" tabindex="0" class="btn">Pay now</div>
    <button aria-label="Complete your purchase transaction">Buy now</button>
  </form>
</body>
</html>
""",
        "tests": [
            {
                "name": "image gets a real name",
                "code": r"""const img = code.match(/<img[^>]*>/i);
if (!img) throw new Error("Keep the cards image.");
const alt = (img[0].match(/alt\s*=\s*["']([^"']*)["']/i) || [])[1] || "";
if (alt.trim().length < 4) {
  throw new Error("The cards image needs meaningful alt text (4+ characters).");
}""",
                "hint": "alt=\"\" means decorative — accepted payment logos are content. Describe them.",
            },
            {
                "name": "every label is associated",
                "code": r"""const labels = [...code.matchAll(/<label([^>]*)>([\s\S]*?)<\/label>/gi)];
if (labels.length < 2) throw new Error("Keep both labels.");
for (const l of labels) {
  const m = l[1].match(/for\s*=\s*["']([^"']+)["']/i);
  if (m) {
    if (!new RegExp("id\\s*=\\s*[\"']" + m[1] + "[\"']").test(code)) {
      throw new Error('Label for="' + m[1] + '" has no matching input id.');
    }
  } else if (!/<input|<select|<textarea/i.test(l[2])) {
    throw new Error("A label neither uses for= nor wraps its field.");
  }
}""",
                "hint": "Two association paths: <label for> matching the input's id, or wrapping the input. The email label uses neither.",
            },
            {
                "name": "no fake buttons",
                "code": r"""if (/<(div|span)[^>]*role\s*=\s*["']button["']/i.test(code)) {
  throw new Error('Replace the div role="button" with a real <button>.');
}
const realBtns = (code.match(/<button[\s>]/gi) || []).length;
if (realBtns < 2) {
  throw new Error("Both actions should be real <button> elements.");
}""",
                "hint": "role=\"button\" adds the role but not the behavior — focus, Enter/Space, disabled all come free with <button>.",
            },
            {
                "name": "visible text wins on Buy now",
                "code": r"""const buy = [...code.matchAll(/<button([^>]*)>([\s\S]*?)<\/button>/gi)].find((b) =>
  /buy now/i.test(b[2].replace(/<[^>]*>/g, ""))
);
if (!buy) throw new Error("Keep the Buy now button.");
if (/aria-label\s*=/i.test(buy[1])) {
  throw new Error('Remove the aria-label that overrides the visible text "Buy now".');
}""",
                "hint": "Speech users say what they see. When aria-label disagrees with visible text, the name is wrong — delete the aria-label.",
            },
        ],
    },
    {
        "title": "Debug: tên hỏng",
        "prompt": "Các cái tên trên trang thanh toán này hỏng một cách lặng lẽ: ảnh thẻ ngân hàng có alt rỗng, label email không bao giờ được kết nối với trường của nó, for= của label promo trỏ sai id, 'Pay now' là một div role=\"button\", và 'Buy now' che văn bản hiển thị sau một aria-label mâu thuẫn. Sửa mọi cái tên theo cách đúng: alt thật, kết hợp for/id, <button> thật, và văn bản hiển thị là nguồn sự thật.",
        "tests": [
            {"name": "ảnh có tên thật", "hint": "alt=\"\" nghĩa là trang trí — logo cổng thanh toán là nội dung. Hãy mô tả chúng."},
            {"name": "mọi label được kết nối", "hint": "Hai đường kết nối: <label for> khớp id của input, hoặc bọc input bên trong. Label email chẳng dùng đường nào."},
            {"name": "không nút giả", "hint": "role=\"button\" thêm vai trò nhưng không thêm hành vi — focus, Enter/Space, disabled đều đi kèm miễn phí với <button>."},
            {"name": "văn bản hiển thị thắng ở Buy now", "hint": "Người dùng giọng nói đọc theo cái họ thấy. Khi aria-label trái với văn bản hiển thị, tên là sai — xóa aria-label."},
        ],
    },
)

print("Part A done: sets 1-2 (6 challenges) written.")
