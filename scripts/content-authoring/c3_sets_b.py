#!/usr/bin/env python3
"""Author Course 3 (Advanced HTML) practice sets — part B: native-disclosure-dialogs + popovers-invokers + responsive-media. EN + VI overlays."""
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


# ─────────────────── Set 3: native-disclosure-dialogs ───────────────────
pset(
    "native-disclosure-dialogs-practice",
    "Native Disclosure & Dialogs — Practice",
    "Disclosure & dialog gốc — Luyện tập",
    "Build a native FAQ accordion, a confirmation dialog with backdrop and autofocus, then debug a hand-rolled modal.",
    "Dựng accordion FAQ gốc, một dialog xác nhận với backdrop và autofocus, rồi sửa một modal tự chế.",
    "native-disclosure-dialogs",
    25,
)

challenge(
    "native-disclosure-dialogs-practice",
    "i3-dialog-faq",
    {
        "title": "Native FAQ Accordion",
        "prompt": "Build the FAQ accordion for a product page: at least three sibling <details> elements that all share the same name=\"faq\" (opening one closes the others), each with a non-empty <summary> question and answer content after the summary. No JavaScript anywhere.",
        "difficulty": "advanced",
        "level": "guided",
        "boilerplate": "<!-- FAQ accordion -->\n\n",
        "tests": [
            {
                "name": "three or more sibling details",
                "code": r"""const n = (code.match(/<details[\s>]/gi) || []).length;
if (n < 3) {
  throw new Error("At least three <details> elements expected (found " + n + ").");
}""",
                "hint": "Every FAQ entry is one <details> with a <summary> and the answer as content.",
            },
            {
                "name": "accordion name shared by all",
                "code": r"""const names = [...code.matchAll(/<details([^>]*)>/gi)].map((m) => {
  const a = m[1].match(/name\s*=\s*["']([^"']*)["']/i);
  return a ? a[1] : null;
});
if (names.some((n) => !n)) {
  throw new Error("Every <details> needs a name attribute.");
}
const unique = [...new Set(names)];
if (unique.length !== 1) {
  throw new Error("All siblings must share ONE name value — that is what makes them an accordion.");
}""",
                "hint": "The shared name attribute is the whole trick: same name = exclusive accordion, per details.",
            },
            {
                "name": "every summary is non-empty",
                "code": r"""const sums = [...code.matchAll(/<summary[^>]*>([\s\S]*?)<\/summary>/gi)].map((m) =>
  m[1].replace(/<[^>]*>/g, "").trim()
);
if (sums.length < 3) {
  throw new Error("Each <details> needs a <summary>.");
}
const empty = sums.filter((s) => !s).length;
if (empty > 0) {
  throw new Error(empty + " <summary> element(s) are empty — the question is the accessible name.");
}""",
                "hint": "The summary is what gets announced and clicked — it must carry the visible question.",
            },
            {
                "name": "answers live after the summary",
                "code": r"""const ds = [...code.matchAll(/<details[^>]*>([\s\S]*?)<\/details>/gi)];
if (ds.length < 3) throw new Error("Three <details> expected.");
for (const d of ds) {
  const body = d[1].replace(/<summary[^>]*>[\s\S]*?<\/summary>/i, "").replace(/<[^>]*>/g, "").trim();
  if (!body) {
    throw new Error("A <details> has no answer content after its <summary>.");
  }
}""",
                "hint": "Content that is not the <summary> is the disclosed answer — each item needs one.",
            },
        ],
    },
    {
        "title": "Accordion FAQ gốc",
        "prompt": "Dựng accordion FAQ cho một trang sản phẩm: ít nhất ba phần tử <details> anh em cùng dùng chung name=\"faq\" (mở một cái thì các cái khác đóng), mỗi cái có <summary> không rỗng là câu hỏi và nội dung trả lời phía sau summary. Không dùng JavaScript.",
        "tests": [
            {"name": "ba phần tử details trở lên", "hint": "Mỗi mục FAQ là một <details> với <summary> và câu trả lời làm nội dung."},
            {"name": "cùng một tên accordion", "hint": "Thuộc tính name dùng chung là toàn bộ mẹo: cùng name = accordion loại trừ, theo chuẩn details."},
            {"name": "mọi summary không rỗng", "hint": "Summary là thứ được thông báo và bấm — nó phải mang câu hỏi hiển thị."},
            {"name": "câu trả lời nằm sau summary", "hint": "Nội dung không phải <summary> chính là phần được mở ra — mỗi mục cần một cái."},
        ],
    },
)

challenge(
    "native-disclosure-dialogs-practice",
    "i3-dialog-confirm",
    {
        "title": "Confirmation Dialog",
        "prompt": "Build a 'Delete file?' confirmation dialog: a <dialog id=\"confirm-delete\"> named via aria-labelledby pointing at its own heading; a form method=\"dialog\" inside it with a destructive button and a safe Cancel button carrying autofocus; a <style> block styling dialog::backdrop. Full document skeleton required.",
        "difficulty": "advanced",
        "level": "independent",
        "boilerplate": "<!-- Confirmation dialog page -->\n\n",
        "tests": [
            {
                "name": "dialog element with id",
                "code": r"""if (!/<dialog[^>]*\bid\s*=\s*["']confirm-delete["'][^>]*>/i.test(code)) {
  throw new Error('Add <dialog id="confirm-delete">.');
}""",
                "hint": "The dialog element is the component — no divs, no role fakes.",
            },
            {
                "name": "named by its heading",
                "code": r"""const dlg = code.match(/<dialog[^>]*>([\s\S]*?)<\/dialog>/i);
if (!dlg) throw new Error("Keep the <dialog>.");
const m = dlg[0].match(/aria-labelledby\s*=\s*["']([^"']+)["']/i) ||
  code.match(/<dialog[^>]*aria-labelledby\s*=\s*["']([^"']+)["']/i);
if (!m) {
  throw new Error("Name the dialog with aria-labelledby.");
}
const heading = new RegExp("<h[1-6][\\s>][^>]*id\\s*=\\s*[\"']" + m[1] + "[\"']").test(dlg[0]);
if (!heading) {
  throw new Error('aria-labelledby "' + m[1] + '" must point at a heading inside the dialog.');
}""",
                "hint": "Give the dialog's <h2> an id and reference it from the dialog's aria-labelledby.",
            },
            {
                "name": "method=dialog form with two buttons",
                "code": r"""const dlg = code.match(/<dialog[^>]*>([\s\S]*?)<\/dialog>/i);
if (!dlg) throw new Error("Keep the <dialog>.");
if (!/<form[^>]*method\s*=\s*["']dialog["'][^>]*>/i.test(dlg[0])) {
  throw new Error('Put a <form method="dialog"> inside the dialog.');
}
const btns = (dlg[0].match(/<button[\s>]/gi) || []).length;
if (btns < 2) {
  throw new Error("The dialog needs both a destructive and a safe (Cancel) button.");
}""",
                "hint": "method=\"dialog\" closes the dialog on submit and exposes returnValue — the platform's own wiring.",
            },
            {
                "name": "autofocus on the safe action",
                "code": r"""const dlg = code.match(/<dialog[^>]*>([\s\S]*?)<\/dialog>/i);
if (!dlg) throw new Error("Keep the <dialog>.");
const af = [...dlg[0].matchAll(/<button([^>]*)>([\s\S]*?)<\/button>/gi)].find((b) =>
  /autofocus/i.test(b[1])
);
if (!af) {
  throw new Error("One button inside the dialog needs autofocus.");
}
if (/delete|remove|confirm/i.test(af[2].replace(/<[^>]*>/g, ""))) {
  throw new Error("autofocus must be on the SAFE action (Cancel), not the destructive one.");
}""",
                "hint": "Focus lands where autofocus says — put it on Cancel so Enter can't fire the deletion.",
            },
            {
                "name": "backdrop is styled",
                "code": r"""if (!/<style[\s>][\s\S]*::backdrop/i.test(code)) {
  throw new Error("Style dialog::backdrop in a <style> block.");
}""",
                "hint": "::backdrop is the pseudo-element behind a modal dialog — dim it so the page reads as blocked.",
            },
        ],
    },
    {
        "title": "Dialog xác nhận",
        "prompt": "Dựng dialog xác nhận 'Xóa file?': một <dialog id=\"confirm-delete\"> được đặt tên qua aria-labelledby trỏ vào heading của chính nó; một form method=\"dialog\" bên trong với nút phá hủy và nút Cancel an toàn mang autofocus; một khối <style> trang trí dialog::backdrop. Yêu cầu bộ xương tài liệu đầy đủ.",
        "tests": [
            {"name": "phần tử dialog với id", "hint": "Phần tử dialog chính là component — không div, không giả role."},
            {"name": "được đặt tên bằng heading", "hint": "Cấp cho <h2> của dialog một id rồi tham chiếu từ aria-labelledby của dialog."},
            {"name": "form method=dialog với hai nút", "hint": "method=\"dialog\" đóng dialog khi submit và trao returnValue — dây nối gốc của nền tảng."},
            {"name": "autofocus trên hành động an toàn", "hint": "Focus rơi đúng nơi autofocus chỉ — đặt trên Cancel để Enter không bắn ra phép xóa."},
            {"name": "backdrop được trang trí", "hint": "::backdrop là pseudo-element phía sau modal dialog — làm mờ nó để trang đọc là bị chặn."},
        ],
    },
)

challenge(
    "native-disclosure-dialogs-practice",
    "i3-dialog-debug",
    {
        "title": "Debug: The Hand-Rolled Modal",
        "prompt": "This page's 'modal' is a div with role=\"dialog\" toggled by a class, and its FAQ accordions are <details> whose name attributes disagree, one with an empty summary. Rebuild properly: a real <dialog> opened via a button using commandfor/command (or form method=\"dialog\"/script showModal with its id), accordions sharing ONE name, and no empty summaries.",
        "difficulty": "advanced",
        "level": "debugging",
        "boilerplate": """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Settings</title></head>
<body>
  <h1>Workspace settings</h1>
  <div class="modal" role="dialog" aria-label="Danger zone">
    <h2>Delete workspace?</h2>
    <button onclick="closeModal()">Cancel</button>
  </div>
  <details name="faq-open"><summary>Can I undo?</summary><p>No.</p></details>
  <details name="faq-closed"><summary></summary><p>Maybe.</p></details>
  <script>
    function closeModal(){ document.querySelector('.modal').classList.remove('open'); }
  </script>
</body>
</html>
""",
        "tests": [
            {
                "name": "real dialog replaces the div",
                "code": r"""if (/<div[^>]*role\s*=\s*["']dialog["']/i.test(code)) {
  throw new Error('Replace the div role="dialog" with a real <dialog> element.');
}
if (!/<dialog[\s>]/i.test(code)) {
  throw new Error("Add a <dialog> element for the modal.");
}""",
                "hint": "role=\"dialog\" on a div gets none of the platform: no top layer, no inert page, no Escape.",
            },
            {
                "name": "dialog is actually openable",
                "code": r"""const dlg = code.match(/<dialog[^>]*\bid\s*=\s*["']([^"']+)["'][^>]*>/i);
if (!dlg) throw new Error("Give the <dialog> an id.");
const id = dlg[1];
const wired =
  new RegExp("commandfor\\s*=\\s*[\"']" + id + "[\"']").test(code) ||
  new RegExp("showModal\\s*\\(\\s*\\)?[\\s\\S]{0,120}" + id + "|" + id + "[\\s\\S]{0,120}showModal").test(code) ||
  new RegExp("getElementById\\([\"']" + id + "[\"']\\)[\\s\\S]{0,40}showModal").test(code);
if (!wired) {
  throw new Error('Wire an opener to the dialog: commandfor="' + id + '" or showModal() on it.');
}""",
                "hint": "Either the 2026 way (command/commandfor) or one showModal() line — but something must open it.",
            },
            {
                "name": "accordions share one name",
                "code": r"""const names = [...code.matchAll(/<details([^>]*)>/gi)].map((m) => {
  const a = m[1].match(/name\s*=\s*["']([^"']*)["']/i);
  return a ? a[1] : null;
});
if (names.length < 2) throw new Error("Keep both <details> accordions.");
if (names.some((n) => !n)) throw new Error("Every <details> needs a name.");
if ([...new Set(names)].length !== 1) {
  throw new Error("Both accordions must share the SAME name value.");
}""",
                "hint": "'faq-open' vs 'faq-closed' are two separate groups — pick one name for both.",
            },
            {
                "name": "no empty summaries",
                "code": r"""const sums = [...code.matchAll(/<summary[^>]*>([\s\S]*?)<\/summary>/gi)].map((m) =>
  m[1].replace(/<[^>]*>/g, "").trim()
);
if (sums.some((s) => !s)) {
  throw new Error("An empty <summary> announces nothing — write the question in it.");
}""",
                "hint": "The summary is the accessible name of the disclosure — empty means invisible to users.",
            },
        ],
    },
    {
        "title": "Debug: modal tự chế",
        "prompt": "'Modal' của trang này là một div với role=\"dialog\" bật tắt bằng class, và các accordion FAQ là <details> với thuộc tính name bất đồng bộ, một cái có summary rỗng. Dựng lại đúng chuẩn: một <dialog> thật được mở qua nút dùng commandfor/command (hoặc form method=\"dialog\"/script showModal với id của nó), các accordion dùng chung MỘT name, và không còn summary rỗng.",
        "tests": [
            {"name": "dialog thật thay div", "hint": "role=\"dialog\" trên div không nhận được gì từ nền tảng: không top layer, không inert page, không Escape."},
            {"name": "dialog mở được thật sự", "hint": "Hoặc cách 2026 (command/commandfor) hoặc một dòng showModal() — nhưng phải có thứ gì đó mở được nó."},
            {"name": "accordion dùng chung một name", "hint": "'faq-open' với 'faq-closed' là hai nhóm riêng — chọn một name cho cả hai."},
            {"name": "không summary rỗng", "hint": "Summary là accessible name của disclosure — rỗng nghĩa là vô hình với người dùng."},
        ],
    },
)

# ─────────────────── Set 4: popovers-invokers ───────────────────
pset(
    "popovers-invokers-practice",
    "Popovers & Invokers — Practice",
    "Popover & invoker — Luyện tập",
    "Build a popover menu and a manual toast, then convert a JS-driven dialog to invoker commands and debug a wrong popover flavor.",
    "Dựng menu popover và toast manual, rồi chuyển một dialog chạy JS sang invoker commands và sửa một popover chọn sai kiểu.",
    "popovers-invokers",
    25,
)

challenge(
    "popovers-invokers-practice",
    "i3-popover-menu",
    {
        "title": "Popover Action Menu",
        "prompt": "Build a 'Row actions' menu with zero JavaScript: a button with popovertarget=\"row-menu\" opening a <div id=\"row-menu\" popover> that contains at least two action buttons and one close button using popovertarget=\"row-menu\" popovertargetaction=\"hide\".",
        "difficulty": "advanced",
        "level": "guided",
        "boilerplate": "<!-- Row actions popover -->\n\n",
        "tests": [
            {
                "name": "invoker targets the popover",
                "code": r"""const inv = code.match(/<button[^>]*popovertarget\s*=\s*["']row-menu["'][^>]*>/i);
if (!inv) {
  throw new Error('Add an invoker button with popovertarget="row-menu".');
}""",
                "hint": "popovertarget on the button is the whole wiring — no addEventListener needed.",
            },
            {
                "name": "popover element exists",
                "code": r"""const pop = code.match(/<(div|ul|menu|nav)[^>]*\bid\s*=\s*["']row-menu["'][^>]*>/i);
if (!pop) throw new Error('Add the element with id="row-menu".');
if (!/\bpopover\b/i.test(pop[0])) {
  throw new Error('The target element needs the popover attribute.');
}""",
                "hint": "The id the button targets must carry popover — that is what turns it into a popover.",
            },
            {
                "name": "menu holds real actions",
                "code": r"""const start = code.search(/<(div|ul|menu|nav)[^>]*\bid\s*=\s*["']row-menu["'][^>]*>/i);
if (start === -1) throw new Error('Add the element with id="row-menu".');
const seg = code.slice(start);
const end = seg.search(/<\/(div|ul|menu|nav)>/i);
const inner = end === -1 ? seg : seg.slice(0, end);
const btns = (inner.match(/<button[\s>]/gi) || []).length;
if (btns < 3) {
  throw new Error("The popover needs at least two action buttons plus the close button.");
}""",
                "hint": "Two actions and one close = three buttons inside the popover.",
            },
            {
                "name": "close button hides its own popover",
                "code": r"""const close = [...code.matchAll(/<button([^>]*)>([\s\S]*?)<\/button>/gi)].find((b) =>
  /popovertargetaction\s*=\s*["']hide["']/i.test(b[1])
);
if (!close) {
  throw new Error('Add a close button with popovertargetaction="hide".');
}
if (!/popovertarget\s*=\s*["']row-menu["']/i.test(close[1])) {
  throw new Error('The close button must target the popover itself: popovertarget="row-menu".');
}""",
                "hint": "A button inside the popover that targets it with action=hide is the idiomatic close affordance.",
            },
        ],
    },
    {
        "title": "Menu hành động dạng popover",
        "prompt": "Dựng menu 'Row actions' với không một dòng JavaScript: một nút với popovertarget=\"row-menu\" mở một <div id=\"row-menu\" popover> chứa ít nhất hai nút hành động và một nút đóng dùng popovertarget=\"row-menu\" popovertargetaction=\"hide\".",
        "tests": [
            {"name": "nút gọi trỏ tới popover", "hint": "popovertarget trên nút là toàn bộ dây nối — không cần addEventListener."},
            {"name": "phần tử popover tồn tại", "hint": "Id mà nút trỏ tới phải mang thuộc tính popover — thứ biến nó thành popover."},
            {"name": "menu có hành động thật", "hint": "Hai hành động cộng một nút đóng = ba nút bên trong popover."},
            {"name": "nút đóng tự ẩn popover của nó", "hint": "Một nút bên trong popover tự trỏ vào nó với action=hide là cách đóng chuẩn mực."},
        ],
    },
)

challenge(
    "popovers-invokers-practice",
    "i3-popover-toast",
    {
        "title": "Toast and Filter Popover",
        "prompt": "Two flavors, right tool each: (1) a toast notification as popover=\"manual\" (no light dismiss) that carries its own close button (popovertarget + popovertargetaction=\"hide\"); (2) a filter panel as a plain auto popover (light dismiss expected). Distinct ids; no JavaScript.",
        "difficulty": "advanced",
        "level": "independent",
        "boilerplate": "<!-- Toast + filter popover -->\n\n",
        "tests": [
            {
                "name": "manual toast with explicit close",
                "code": r"""const toast = code.match(/<[^>]*popover\s*=\s*["']manual["'][^>]*\bid\s*=\s*["']([^"']+)["'][^>]*>/i) ||
  code.match(/<[^>]*\bid\s*=\s*["']([^"']+)["'][^>]*popover\s*=\s*["']manual["'][^>]*>/i);
if (!toast) {
  throw new Error('The toast needs popover="manual" and an id.');
}
const tid = toast[1];
const closer = [...code.matchAll(/<button([^>]*)>/gi)].find((b) =>
  new RegExp("popovertarget\\s*=\\s*[\"']" + tid + "[\"']", "i").test(b[1]) &&
  /popovertargetaction\s*=\s*["']hide["']/i.test(b[1])
);
if (!closer) {
  throw new Error("A manual popover never light-dismisses — it needs its own close button (action=hide).");
}""",
                "hint": "manual means the platform will never close it for you — the close button is not optional.",
            },
            {
                "name": "auto popover for the filter panel",
                "code": r"""const auto = code.match(/<[^>]*\bpopover(\s*=\s*["']auto["'])?[^>]*>/i);
if (!auto) {
  throw new Error("Add the filter panel as an auto popover (bare popover attribute).");
}""",
                "hint": "Bare popover (or popover=\"auto\") gets light dismiss — the right flavor for a transient panel.",
            },
            {
                "name": "two distinct ids",
                "code": r"""const pEls = [...code.matchAll(/<[^>]*\bpopover(\s*=\s*["'][^"']*["'])?\b[^>]*>/gi)];
const ids = pEls.map((m) => (m[0].match(/\bid\s*=\s*["']([^"']+)["']/i) || [])[1]).filter(Boolean);
if (new Set(ids).size < 2) {
  throw new Error("Toast and filter panel need distinct ids on their popover elements.");
}""",
                "hint": "Each popover is its own element with its own id — the invokers reference them individually.",
            },
        ],
    },
    {
        "title": "Toast và popover bộ lọc",
        "prompt": "Hai kiểu, mỗi việc một công cụ đúng: (1) một thông báo toast dạng popover=\"manual\" (không light dismiss) tự mang nút đóng (popovertarget + popovertargetaction=\"hide\"); (2) một panel bộ lọc dạng popover auto thuần (mong đợi light dismiss). Hai id khác nhau; không dùng JavaScript.",
        "tests": [
            {"name": "toast manual với nút đóng tường minh", "hint": "manual nghĩa là nền tảng sẽ không bao giờ đóng hộ bạn — nút đóng không phải tùy chọn."},
            {"name": "popover auto cho panel bộ lọc", "hint": "popover trần (hoặc popover=\"auto\") được light dismiss — kiểu đúng cho panel tạm thời."},
            {"name": "hai id khác nhau", "hint": "Mỗi popover là một phần tử riêng với id riêng — các nút gọi tham chiếu từng cái."},
        ],
    },
)

challenge(
    "popovers-invokers-practice",
    "i3-popover-debug",
    {
        "title": "Debug: JS Dialog → Invoker Commands",
        "prompt": "This delete-confirmation dialog is driven by onclick handlers calling showModal()/close(). Convert it to 2026-standard invoker commands: the open button uses commandfor=\"delete-confirm\" command=\"show-modal\", the close button inside the dialog uses commandfor=\"delete-confirm\" command=\"close\", and every onclick attribute is gone. Keep the <dialog id=\"delete-confirm\">.",
        "difficulty": "advanced",
        "level": "debugging",
        "boilerplate": """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Danger zone</title></head>
<body>
  <h1>Danger zone</h1>
  <button onclick="openDelete()">Delete project…</button>
  <dialog id="delete-confirm">
    <h2>Delete this project?</h2>
    <p>All issues and labels go with it.</p>
    <button onclick="closeDelete()">Cancel</button>
    <button onclick="deleteProject()">Delete forever</button>
  </dialog>
  <script>
    function openDelete(){ document.getElementById('delete-confirm').showModal(); }
    function closeDelete(){ document.getElementById('delete-confirm').close(); }
    function deleteProject(){ /* … */ }
  </script>
</body>
</html>
""",
        "tests": [
            {
                "name": "open button uses show-modal command",
                "code": r"""if (!/<button[^>]*commandfor\s*=\s*["']delete-confirm["'][^>]*command\s*=\s*["']show-modal["']/i.test(code) &&
    !/<button[^>]*command\s*=\s*["']show-modal["'][^>]*commandfor\s*=\s*["']delete-confirm["']/i.test(code)) {
  throw new Error('The open button needs commandfor="delete-confirm" command="show-modal".');
}""",
                "hint": "command=\"show-modal\" on a button is the declarative showModal() — same platform behavior, no JS.",
            },
            {
                "name": "close button uses close command",
                "code": r"""const dlg = code.match(/<dialog[^>]*>([\s\S]*?)<\/dialog>/i);
if (!dlg) throw new Error("Keep the <dialog>.");
const inside = dlg[1].match(/<button[^>]*commandfor\s*=\s*["']delete-confirm["'][^>]*command\s*=\s*["']close["']/i) ||
  dlg[1].match(/<button[^>]*command\s*=\s*["']close["'][^>]*commandfor\s*=\s*["']delete-confirm["']/i);
if (!inside) {
  throw new Error('A button inside the dialog needs command="close" targeting delete-confirm.');
}""",
                "hint": "The Cancel button keeps working without its onclick — command=\"close\" does the job.",
            },
            {
                "name": "no onclick handlers remain",
                "code": r"""const handlers = (code.match(/\sonclick\s*=/gi) || []).length;
if (handlers > 1) {
  throw new Error("Remove the open/close onclick handlers — only the real action may keep custom JS.");
}""",
                "hint": "Open and close are platform commands now; only the destructive action itself may still call code.",
            },
            {
                "name": "dialog intact",
                "code": r"""if (!/<dialog[^>]*\bid\s*=\s*["']delete-confirm["'][^>]*>/i.test(code)) {
  throw new Error('Keep <dialog id="delete-confirm">.');
}""",
                "hint": "The invoker model drives the same dialog element — nothing about the dialog itself changes.",
            },
        ],
    },
    {
        "title": "Debug: dialog JS → invoker commands",
        "prompt": "Dialog xác nhận xóa này được điều khiển bằng các handler onclick gọi showModal()/close(). Chuyển sang invoker commands chuẩn 2026: nút mở dùng commandfor=\"delete-confirm\" command=\"show-modal\", nút đóng bên trong dialog dùng commandfor=\"delete-confirm\" command=\"close\", và mọi thuộc tính onclick biến mất. Giữ nguyên <dialog id=\"delete-confirm\">.",
        "tests": [
            {"name": "nút mở dùng lệnh show-modal", "hint": "command=\"show-modal\" trên nút chính là showModal() dạng khai báo — cùng hành vi nền tảng, không JS."},
            {"name": "nút đóng dùng lệnh close", "hint": "Nút Cancel vẫn hoạt động mà không cần onclick — command=\"close\" làm trọn công việc."},
            {"name": "không còn handler onclick", "hint": "Mở và đóng giờ là lệnh của nền tảng; chỉ hành động phá hủy thật sự mới có thể giữ code riêng."},
            {"name": "dialog nguyên vẹn", "hint": "Mô hình invoker điều khiển cùng phần tử dialog — bản thân dialog không đổi."},
        ],
    },
)

# ─────────────────── Set 5: responsive-media ───────────────────
pset(
    "responsive-media-practice",
    "Responsive Media — Practice",
    "Media responsive — Luyện tập",
    "Build a format-fallback hero, spec a srcset/sizes image from requirements, then debug a gallery where every attribute lies.",
    "Dựng hero dự phòng định dạng, đặc tả ảnh srcset/sizes từ yêu cầu, rồi sửa một gallery mà mọi thuộc tính đều nói dối.",
    "responsive-media",
    25,
)

challenge(
    "responsive-media-practice",
    "i3-media-hero",
    {
        "title": "Format-Fallback Hero",
        "prompt": "Build the hero image of a product page as a <picture>: an AVIF source, a WebP source, and a JPEG fallback on the inner <img>; the <img> carries intrinsic width=\"1600\" height=\"800\", meaningful alt (4+ characters), and fetchpriority=\"high\".",
        "difficulty": "advanced",
        "level": "guided",
        "boilerplate": "<!-- Hero picture -->\n\n",
        "tests": [
            {
                "name": "avif and webp sources",
                "code": r"""const sources = [...code.matchAll(/<source([^>]*)>/gi)].map((m) => m[1]);
const avif = sources.some((s) => /type\s*=\s*["']image\/avif["']/i.test(s));
const webp = sources.some((s) => /type\s*=\s*["']image\/webp["']/i.test(s));
if (!avif) throw new Error('Add <source type="image/avif">.');
if (!webp) throw new Error('Add <source type="image/webp">.');""",
                "hint": "Sources are tried top-down: newest format first, oldest last.",
            },
            {
                "name": "img fallback with dimensions",
                "code": r"""const img = code.match(/<img[^>]*>/i);
if (!img) throw new Error("The <picture> needs an inner <img> fallback.");
if (!/width\s*=\s*["']1600["']/i.test(img[0]) || !/height\s*=\s*["']800["']/i.test(img[0])) {
  throw new Error('The <img> needs width="1600" height="800" — the browser reserves the box from these.');
}""",
                "hint": "Intrinsic dimensions on the <img> kill layout shift — they live on the img, never on a source.",
            },
            {
                "name": "alt lives on the img",
                "code": r"""const img = code.match(/<img[^>]*>/i);
if (!img) throw new Error("Keep the <img>.");
const alt = (img[0].match(/alt\s*=\s*["']([^"']*)["']/i) || [])[1] || "";
if (alt.trim().length < 4) {
  throw new Error("The <img> needs meaningful alt text (4+ characters).");
}
if (/<source[^>]*\balt\s*=/i.test(code)) {
  throw new Error("alt belongs on the <img> only — sources have no alt.");
}""",
                "hint": "One image, one name: alt sits on the fallback <img> and serves every source.",
            },
            {
                "name": "hero priority is high",
                "code": r"""const img = code.match(/<img[^>]*>/i);
if (!img) throw new Error("Keep the <img>.");
if (!/fetchpriority\s*=\s*["']high["']/i.test(img[0])) {
  throw new Error('The hero needs fetchpriority="high" — it is the LCP image.');
}""",
                "hint": "The largest visible image is the LCP candidate — pull it forward with fetchpriority.",
            },
        ],
    },
    {
        "title": "Hero dự phòng định dạng",
        "prompt": "Dựng ảnh hero của một trang sản phẩm dạng <picture>: một source AVIF, một source WebP, và bản dự phòng JPEG trên <img> bên trong; <img> mang width=\"1600\" height=\"800\" nội tại, alt có ý nghĩa (4+ ký tự), và fetchpriority=\"high\".",
        "tests": [
            {"name": "các source avif và webp", "hint": "Các source được thử từ trên xuống: định dạng mới nhất trước, cũ nhất sau."},
            {"name": "img dự phòng với kích thước", "hint": "Kích thước nội tại trên <img> triệt tiêu layout shift — chúng nằm trên img, không bao giờ trên source."},
            {"name": "alt nằm trên img", "hint": "Một ảnh, một tên: alt nằm trên <img> dự phòng và phục vụ mọi source."},
            {"name": "ưu tiên hero là high", "hint": "Ảnh hiển thị lớn nhất là ứng viên LCP — kéo nó lên trước bằng fetchpriority."},
        ],
    },
)

challenge(
    "responsive-media-practice",
    "i3-media-srcset",
    {
        "title": "Spec an Image from Requirements",
        "prompt": "A product card image renders at 300px on phones (100vw) and 300px inside a 3-column grid on desktop (30vw). Author the <img>: srcset with at least three w-descriptor candidates (300w/600w/900w), a correct sizes attribute reflecting those two conditions, width=\"900\" height=\"600\", alt, and decoding=\"async\". Then add a below-the-fold illustration img with loading=\"lazy\" and its own alt.",
        "difficulty": "advanced",
        "level": "independent",
        "boilerplate": "<!-- Product card + illustration -->\n\n",
        "tests": [
            {
                "name": "three w-descriptor candidates",
                "code": r"""const ss = code.match(/srcset\s*=\s*["']([^"']+)["']/i);
if (!ss) throw new Error("Add a srcset attribute.");
const widths = [...ss[1].matchAll(/(\d+)w\b/gi)].map((m) => Number(m[1]));
if (widths.length < 3 || !widths.includes(300) || !widths.includes(600) || !widths.includes(900)) {
  throw new Error("srcset needs 300w, 600w and 900w candidates.");
}""",
                "hint": "w-descriptors are the real pixel widths of the files — 1x/2x/3x of a 300px slot.",
            },
            {
                "name": "sizes reflects the layout",
                "code": r"""const sizes = code.match(/sizes\s*=\s*["']([^"']+)["']/i);
if (!sizes) throw new Error("Add a sizes attribute.");
const s = sizes[1];
if (!/100vw/i.test(s) || !/30vw/i.test(s)) {
  throw new Error('sizes must express both conditions: "(max-width: …) 100vw, 30vw".');
}
if (!/max-width/i.test(s)) {
  throw new Error("The phone condition needs a media query: (max-width: …) 100vw first.");
}""",
                "hint": "sizes is a media-condition list: phone case first, then the desktop slot width.",
            },
            {
                "name": "intrinsic dimensions and alt",
                "code": r"""const img = code.match(/<img[^>]*srcset[^>]*>/i);
if (!img) throw new Error("Keep the srcset image.");
if (!/width\s*=\s*["']900["']/i.test(img[0]) || !/height\s*=\s*["']600["']/i.test(img[0])) {
  throw new Error('The card image needs width="900" height="600".');
}
const alt = (img[0].match(/alt\s*=\s*["']([^"']*)["']/i) || [])[1] || "";
if (alt.trim().length < 4) {
  throw new Error("Both images need meaningful alt (4+ characters).");
}""",
                "hint": "width/height describe the largest candidate's aspect ratio; the browser derives the box.",
            },
            {
                "name": "lazy illustration, async decode",
                "code": r"""const lazy = [...code.matchAll(/<img[^>]*>/gi)].find((m) =>
  /loading\s*=\s*["']lazy["']/i.test(m[0])
);
if (!lazy) throw new Error('The below-the-fold illustration needs loading="lazy".');
if (!/decoding\s*=\s*["']async["']/i.test(code)) {
  throw new Error('Add decoding="async" to the product card image.');
}""",
                "hint": "One hero eager, the rest lazy — and decoding=\"async\" keeps decode work off the main thread.",
            },
        ],
    },
    {
        "title": "Đặc tả ảnh từ yêu cầu",
        "prompt": "Ảnh thẻ sản phẩm hiển thị 300px trên điện thoại (100vw) và 300px trong lưới 3 cột trên desktop (30vw). Hãy viết <img>: srcset với ít nhất ba ứng viên w-descriptor (300w/600w/900w), thuộc tính sizes đúng phản ánh hai điều kiện đó, width=\"900\" height=\"600\", alt, và decoding=\"async\". Sau đó thêm một ảnh minh họa dưới màn hình đầu với loading=\"lazy\" và alt riêng.",
        "tests": [
            {"name": "ba ứng viên w-descriptor", "hint": "w-descriptor là bề rộng pixel thật của các file — 1x/2x/3x của ô 300px."},
            {"name": "sizes phản ánh layout", "hint": "sizes là danh sách điều kiện media: trường hợp điện thoại trước, rồi bề rộng ô desktop."},
            {"name": "kích thước nội tại và alt", "hint": "width/height mô tả tỷ lệ của ứng viên lớn nhất; trình duyệt tự suy ra chiếc hộp."},
            {"name": "minh họa lazy, giải mã async", "hint": "Một hero eager, phần còn lại lazy — và decoding=\"async\" giữ việc giải mã khỏi luồng chính."},
        ],
    },
)

challenge(
    "responsive-media-practice",
    "i3-media-debug",
    {
        "title": "Debug: The Lying Gallery",
        "prompt": "Every attribute in this gallery is wrong: the hero carries loading=\"lazy\" (it is the LCP), sizes=\"100vw\" on a 300px card slot, no width/height anywhere (layout shift), and an alt was pasted onto a <source>. Repair: hero gets fetchpriority=\"high\" and no lazy; card sizes says 300px; add intrinsic dimensions to both images; move alt to the <img> only.",
        "difficulty": "advanced",
        "level": "debugging",
        "boilerplate": """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Gallery</title></head>
<body>
  <h1>Launch gallery</h1>
  <picture>
    <source type="image/avif" srcset="hero.avif">
    <img src="hero.jpg" alt="Confetti falling over the launch stage" loading="lazy" width="1600" height="800">
  </picture>
  <div class="card">
    <img src="team.jpg" sizes="100vw" alt="The founding team on stage">
  </div>
  <picture>
    <source type="image/webp" srcset="chart.webp" alt="Downloads chart">
    <img src="chart.jpg" width="900" height="500">
  </picture>
</body>
</html>
""",
        "tests": [
            {
                "name": "hero is eager and high priority",
                "code": r"""const hero = code.match(/<picture[\s>][\s\S]*?<img[^>]*hero[^>]*>/i) ||
  [...code.matchAll(/<img[^>]*>/gi)].find((m) => /hero/i.test(m[0]));
if (!hero) throw new Error("Keep the hero image.");
if (/loading\s*=\s*["']lazy["']/i.test(hero[0])) {
  throw new Error("The hero must NOT be lazy — it is the LCP image.");
}
if (!/fetchpriority\s*=\s*["']high["']/i.test(hero[0])) {
  throw new Error('Give the hero fetchpriority="high".');
}""",
                "hint": "Lazy-loading the LCP image is self-sabotage — swap lazy for fetchpriority=\"high\".",
            },
            {
                "name": "card sizes tells the truth",
                "code": r"""const card = [...code.matchAll(/<img[^>]*>/gi)].find((m) => /team/i.test(m[0]));
if (!card) throw new Error("Keep the team image.");
if (!/sizes\s*=\s*["'][^"']*300[^"']*["']/i.test(card[0])) {
  throw new Error("The card slot is 300px — say so in sizes instead of 100vw.");
}""",
                "hint": "sizes=\"100vw\" makes the browser fetch desktop-sized files for a 300px box.",
            },
            {
                "name": "every image has dimensions",
                "code": r"""const imgs = [...code.matchAll(/<img[^>]*>/gi)];
for (const m of imgs) {
  if (!/width\s*=\s*["']\d+["']/i.test(m[0]) || !/height\s*=\s*["']\d+["']/i.test(m[0])) {
    throw new Error("Every <img> needs width and height — the browser reserves the box from them.");
  }
}""",
                "hint": "The chart image lost its dimensions — restore width and height to stop layout shift.",
            },
            {
                "name": "alt only on imgs",
                "code": r"""if (/<source[^>]*\balt\s*=/i.test(code)) {
  throw new Error("Remove alt from the <source> — sources have no alt attribute.");
}
const chart = [...code.matchAll(/<img[^>]*>/gi)].find((m) => /chart/i.test(m[0]));
if (!chart || !(((chart[0].match(/alt\s*=\s*["']([^"']*)["']/i) || [])[1] || "").trim())) {
  throw new Error("The chart <img> needs the alt (4+ characters).");
}""",
                "hint": "alt pasted on a source is dead weight — the img is the one element that carries it.",
            },
        ],
    },
    {
        "title": "Debug: gallery nói dối",
        "prompt": "Mọi thuộc tính trong gallery này đều sai: hero mang loading=\"lazy\" (trong khi nó là LCP), sizes=\"100vw\" trên một ô thẻ 300px, không có width/height ở đâu cả (layout shift), và một alt bị dán lên <source>. Sửa lại: hero nhận fetchpriority=\"high\" và bỏ lazy; sizes của thẻ nói 300px; thêm kích thước nội tại cho cả hai ảnh; chuyển alt về <img> mà thôi.",
        "tests": [
            {"name": "hero eager và ưu tiên cao", "hint": "Lazy-load ảnh LCP là tự phá hoại — đổi lazy lấy fetchpriority=\"high\"."},
            {"name": "sizes của thẻ nói thật", "hint": "sizes=\"100vw\" khiến trình duyệt tải file cỡ desktop cho một chiếc hộp 300px."},
            {"name": "mọi ảnh có kích thước", "hint": "Ảnh chart đánh mất kích thước của mình — phục hồi width và height để chặn layout shift."},
            {"name": "alt chỉ nằm trên img", "hint": "alt dán trên source là vô dụng — img mới là phần tử duy nhất mang nó."},
        ],
    },
)

print("Part B done: sets 3-5 (9 challenges) written.")
