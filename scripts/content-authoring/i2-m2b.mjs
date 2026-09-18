/**
 * Module 2 practices: delegation, components (tabs/modal), forms, URL,
 * observers, and the dashboard mini-build — EN+VI with harness solutions.
 */
import { writePracticeSet } from "./i2-lib.mjs";

const MOD = "advanced-dom-browser-apis";

// ── delegation-practice ─────────────────────────────────────────────────────
writePracticeSet(
  MOD,
  {
    file: "delegation-practice.json",
    id: "delegation-practice",
    title: "Event Delegation — Practice",
    description:
      "Resolve delegated clicks at the logic level: nearest-match lookup, action routing via data attributes, and once-only handlers.",
    viTitle: "Ủy quyền sự kiện — Luyện tập",
    viDescription:
      "Phân giải click được ủy quyền ở tầng logic: tra cứu khớp gần nhất, định tuyến hành động qua thuộc tính data, và handler chạy một lần.",
    afterLesson: "event-delegation",
    minutes: 15,
    difficulty: "intermediate",
    challenges: [
      {
        id: "i2-delegate-resolve",
        title: "Delegation Resolver",
        prompt:
          'Write `resolveAction(event, root)` for a plain-object event model. `event` is `{ target }` and elements are objects with `matches(sel)` and a `parent` chain ending in `null`. RETURN the first element from `target` walking up (including `root` itself? no — stop before `root`) that `matches("[data-action]")`; RETURN `null` when none matches before reaching `root`.',
        difficulty: "intermediate",
        level: "guided",
        boilerplate: "function resolveAction(event, root) {\n  // your code\n}\n",
        tests: [
          {
            name: "finds the nearest data-action ancestor",
            code: 'const fn = new Function(code + "\\nreturn { resolveAction };");\nconst { resolveAction } = fn();\nconst root = { matches: (s) => s === "[data-action]", parent: null };\nconst row = { matches: (s) => s === "[data-action]", parent: root };\nconst target = { matches: () => false, parent: row };\nconst out = resolveAction({ target }, root);\nif (out !== row) throw new Error("The nearest matching element (row) should win over the root.");',
            hint: "Walk from event.target up through .parent, stopping when el === root.",
          },
          {
            name: "returns null when the click misses every action",
            code: 'const fn = new Function(code + "\\nreturn { resolveAction };");\nconst { resolveAction } = fn();\nconst root = { matches: (s) => s === "[data-action]", parent: null };\nconst target = { matches: () => false, parent: root };\nif (resolveAction({ target }, root) !== null) throw new Error("A click on nothing actionable must return null.");',
            hint: "After the walk ends without a match, return null.",
          },
          {
            name: "works when the target itself is actionable",
            code: 'const fn = new Function(code + "\\nreturn { resolveAction };");\nconst { resolveAction } = fn();\nconst root = { matches: (s) => s === "[data-action]", parent: null };\nconst target = { matches: (s) => s === "[data-action]", parent: root };\nif (resolveAction({ target }, root) !== target) throw new Error("A click on the button itself should return the button.");',
            hint: "The walk starts at target — check it before climbing.",
          },
        ],
        vi: {
          title: "Bộ phân giải ủy quyền",
          prompt:
            'Viết `resolveAction(event, root)` cho mô hình sự kiện dạng object thuần. `event` là `{ target }` và các phần tử là object có `matches(sel)` cùng chuỗi `parent` kết thúc bằng `null`. RETURN phần tử đầu tiên đi từ `target` ngược lên (bao gồm cả `root` không? — dừng trước `root`) mà `matches("[data-action]")`; RETURN `null` khi không có phần tử nào khớp trước khi chạm tới `root`.',
          tests: [
            {
              name: "tìm tổ tiên data-action gần nhất",
              hint: "Đi từ event.target lên qua .parent, dừng khi el === root.",
            },
            {
              name: "trả null khi click không trúng hành động nào",
              hint: "Khi vòng đi kết thúc mà không khớp, trả về null.",
            },
            {
              name: "hoạt động khi chính target là phần tử hành động",
              hint: "Vòng đi bắt đầu từ target — kiểm tra nó trước khi leo lên.",
            },
          ],
        },
      },
      {
        id: "i2-action-router",
        title: "Action Router",
        prompt:
          'Write `handleClick(event, root, actions)`: resolve the actionable element as in `resolveAction`, read `el.dataset.action`, and call `actions[action](el)` when the handler exists. RETURN the action name that was dispatched, `null` when nothing matched, and `"missing"` when the element matched but `actions` has no handler for it. `actions` must never be mutated.',
        difficulty: "intermediate",
        level: "independent",
        boilerplate: "function handleClick(event, root, actions) {\n  // your code\n}\n",
        tests: [
          {
            name: "dispatches to the right handler",
            code: 'const fn = new Function(code + "\\nreturn { handleClick };");\nconst { handleClick } = fn();\nconst root = { matches: (s) => s === "[data-action]", parent: null, dataset: {} };\nconst btn = { matches: (s) => s === "[data-action]", parent: root, dataset: { action: "remove" } };\nconst target = { matches: () => false, parent: btn };\nconst calls = [];\nconst out = handleClick({ target }, root, { remove: (el) => calls.push(el) });\nif (out !== "remove") throw new Error("Should return the dispatched action name remove.");\nif (calls.length !== 1 || calls[0] !== btn) throw new Error("The remove handler should receive the matched element.");',
            hint: "Reuse your resolveAction logic, then look up el.dataset.action in actions.",
          },
          {
            name: "returns null when nothing is actionable",
            code: 'const fn = new Function(code + "\\nreturn { handleClick };");\nconst { handleClick } = fn();\nconst root = { matches: (s) => s === "[data-action]", parent: null, dataset: {} };\nconst target = { matches: () => false, parent: root };\nif (handleClick({ target }, root, {}) !== null) throw new Error("No match means no dispatch - return null.");',
            hint: "Early return null when the resolution fails.",
          },
          {
            name: "returns missing when no handler exists",
            code: 'const fn = new Function(code + "\\nreturn { handleClick };");\nconst { handleClick } = fn();\nconst root = { matches: (s) => s === "[data-action]", parent: null, dataset: {} };\nconst btn = { matches: (s) => s === "[data-action]", parent: root, dataset: { action: "archive" } };\nconst target = { matches: () => false, parent: btn };\nconst out = handleClick({ target }, root, { remove: () => {} });\nif (out !== "missing") throw new Error("A matched element without a handler must return missing.");',
            hint: "Check actions[el.dataset.action] exists (typeof === 'function') before calling.",
          },
        ],
        vi: {
          title: "Bộ định tuyến hành động",
          prompt:
            'Viết `handleClick(event, root, actions)`: phân giải phần tử hành động như trong `resolveAction`, đọc `el.dataset.action`, và gọi `actions[action](el)` khi handler tồn tại. RETURN tên hành động đã được điều phối, `null` khi không khớp gì, và `"missing"` khi phần tử khớp nhưng `actions` không có handler cho nó. Không được làm thay đổi `actions`.',
          tests: [
            {
              name: "điều phối đến đúng handler",
              hint: "Tái dùng logic resolveAction, rồi tra el.dataset.action trong actions.",
            },
            {
              name: "trả null khi không có gì hành động được",
              hint: "Return sớm null khi phân giải thất bại.",
            },
            {
              name: "trả missing khi không có handler",
              hint: "Kiểm tra actions[el.dataset.action] tồn tại (typeof === 'function') trước khi gọi.",
            },
          ],
        },
      },
      {
        id: "i2-once-handler",
        title: "Once-Only Handler",
        prompt:
          "Write `once(fn)` that RETURNS a wrapper which calls `fn` with the FIRST invocation's arguments and returns its result; every later call RETURNS that same first result without running `fn` again. `fn`'s `this` need not be preserved.",
        difficulty: "intermediate",
        level: "independent",
        boilerplate: "function once(fn) {\n  // your code\n}\n",
        tests: [
          {
            name: "runs the function exactly once",
            code: 'const fn = new Function(code + "\\nreturn { once };");\nconst { once } = fn();\nlet calls = 0;\nconst g = once((x) => { calls++; return x * 2; });\nconst a = g(21);\nconst b = g(100);\nif (a !== 42) throw new Error("First call should return fn\'s result (42).");\nif (b !== 42) throw new Error("Later calls must return the FIRST result, not re-run.");\nif (calls !== 1) throw new Error("fn should have run exactly once.");',
            hint: "Store both the result and a done flag in the closure.",
          },
          {
            name: "remembers the first arguments",
            code: 'const fn = new Function(code + "\\nreturn { once };");\nconst { once } = fn();\nconst seen = [];\nconst g = once((x) => seen.push(x));\ng("first");\ng("second");\ng("third");\nif (seen.join() !== "first") throw new Error("Only the first invocation arguments should reach fn.");',
            hint: "Guard the body with if (done) return result; before doing anything.",
          },
        ],
        vi: {
          title: "Handler chạy một lần",
          prompt:
            "Viết `once(fn)` RETURN một wrapper gọi `fn` với đối số của lần gọi ĐẦU TIÊN và trả về kết quả của nó; mọi lời gọi sau RETURN chính kết quả đầu tiên đó mà không chạy lại `fn`. Không cần giữ `this` của `fn`.",
          tests: [
            {
              name: "chạy function đúng một lần",
              hint: "Lưu cả kết quả và cờ done trong closure.",
            },
            {
              name: "ghi nhớ đối số lần đầu",
              hint: "Chặn thân hàm bằng if (done) return result; trước khi làm bất cứ gì.",
            },
          ],
        },
      },
    ],
  },
  [
    [
      "i2-delegate-resolve",
      'function resolveAction(event, root) {\n  for (let el = event.target; el && el !== root; el = el.parent) {\n    if (el.matches("[data-action]")) return el;\n  }\n  return null;\n}',
      "function resolveAction(event, root) { return null; }",
    ],
    [
      "i2-action-router",
      'function handleClick(event, root, actions) {\n  for (let el = event.target; el && el !== root; el = el.parent) {\n    if (el.matches("[data-action]")) {\n      const name = el.dataset.action;\n      if (typeof actions[name] === "function") {\n        actions[name](el);\n        return name;\n      }\n      return "missing";\n    }\n  }\n  return null;\n}',
      "function handleClick(event, root, actions) { return null; }",
    ],
    [
      "i2-once-handler",
      "function once(fn) {\n  let done = false;\n  let result;\n  return (...args) => {\n    if (done) return result;\n    done = true;\n    result = fn(...args);\n    return result;\n  };\n}",
      "function once(fn) {\n  return (...args) => fn(...args);\n}",
    ],
  ],
);

// ── components-practice ─────────────────────────────────────────────────────
writePracticeSet(
  MOD,
  {
    file: "components-practice.json",
    id: "components-practice",
    title: "Stateful Components — Practice",
    description:
      "Component factories without a framework: a reducer-driven tabs widget, a modal with focus return, and an accordion.",
    viTitle: "Component có trạng thái — Luyện tập",
    viDescription:
      "Component factory không cần framework: widget tabs điều khiển bằng reducer, modal trả focus và một accordion.",
    afterLesson: "stateful-components",
    minutes: 20,
    difficulty: "intermediate",
    challenges: [
      {
        id: "i2-modal-lifecycle",
        title: "Modal Lifecycle",
        prompt:
          'Write `createModal()` that RETURNS an object with:\n\n- `open(el)` — marks the modal open, remembers the previously focused element (any value), stores the passed element as the modal\'s content root, and returns `"opened"`\n- `close()` — marks it closed, restores focus to the remembered element, clears the stored root, and returns `"closed"`\n- `isOpen()` — boolean state\n\nOpening twice without closing returns `"already-open"` and changes nothing; closing while closed returns `"already-closed"`.',
        difficulty: "intermediate",
        level: "guided",
        boilerplate: "function createModal() {\n  // your code\n}\n",
        tests: [
          {
            name: "open/close cycle with focus restore",
            code: 'const fn = new Function(code + "\\nreturn { createModal };");\nconst { createModal } = fn();\nconst m = createModal();\nconst trigger = { id: "trigger" };\nconst panel = { id: "panel" };\nif (m.isOpen() !== false) throw new Error("A fresh modal starts closed.");\nif (m.open(trigger, panel) !== "opened") throw new Error("open should return opened.");\nif (m.isOpen() !== true) throw new Error("After open, isOpen() should be true.");\nif (m.close() !== "closed") throw new Error("close should return closed.");\nif (m.isOpen() !== false) throw new Error("After close, isOpen() should be false.");',
            hint: "Keep state, previousFocus, and root in the closure.",
          },
          {
            name: "restores focus to the opener",
            code: 'const fn = new Function(code + "\\nreturn { createModal };");\nconst { createModal } = fn();\nconst m = createModal();\nconst trigger = { id: "trigger" };\nm.open(trigger, {});\nconst restored = m.close();\nif (restored !== trigger) throw new Error("close() should return the remembered opener element (the focus target).");',
            hint: "close() returns the stored previousFocus.",
          },
          {
            name: "guards double open and double close",
            code: 'const fn = new Function(code + "\\nreturn { createModal };");\nconst { createModal } = fn();\nconst m = createModal();\nif (m.open({ id: 1 }, {}) !== "opened") throw new Error("First open succeeds.");\nif (m.open({ id: 2 }, {}) !== "already-open") throw new Error("Second open without close returns already-open and must not overwrite the remembered opener.");\nif (m.close() !== "closed") throw new Error("close still works after the rejected open.");\nif (m.close() !== "already-closed") throw new Error("Closing a closed modal returns already-closed.");',
            hint: "Check isOpen() at the top of open() and close() and return the guard strings.",
          },
        ],
        vi: {
          title: "Vòng đời Modal",
          prompt:
            'Viết `createModal()` RETURN một object với:\n\n- `open(el)` — đánh dấu modal đang mở, ghi nhớ phần tử đang giữ focus trước đó (bất kỳ giá trị nào), lưu phần tử được truyền làm gốc nội dung, và trả về `"opened"`\n- `close()` — đánh dấu đóng, trả focus về phần tử đã ghi nhớ, xóa gốc nội dung đã lưu, và trả về `"closed"`\n- `isOpen()` — trạng thái dạng boolean\n\nMở hai lần mà không đóng trả về `"already-open"` và không thay đổi gì; đóng khi đang đóng trả về `"already-closed"`.',
          tests: [
            {
              name: "chu kỳ open/close với trả focus",
              hint: "Giữ state, previousFocus và root trong closure.",
            },
            { name: "trả focus về phần tử đã mở", hint: "close() trả về previousFocus đã lưu." },
            {
              name: "chặn mở hai lần và đóng hai lần",
              hint: "Kiểm tra isOpen() ở đầu open() và close() rồi trả các chuỗi guard tương ứng.",
            },
          ],
        },
      },
      {
        id: "i2-accordion",
        title: "Accordion State",
        prompt:
          "Write `createAccordion(count)` that RETURNS an object with `toggle(i)`, `isOpen(i)`, and `openCount()`. Exactly one section may be open at a time (an accordion, not independent collapsibles): toggling the open section closes it; toggling a closed section opens it and closes the previous one. Out-of-range indexes must not crash or change state. Initially all closed.",
        difficulty: "intermediate",
        level: "independent",
        boilerplate: "function createAccordion(count) {\n  // your code\n}\n",
        tests: [
          {
            name: "single-open behavior",
            code: 'const fn = new Function(code + "\\nreturn { createAccordion };");\nconst { createAccordion } = fn();\nconst acc = createAccordion(3);\nif (acc.openCount() !== 0) throw new Error("Starts with all sections closed.");\nacc.toggle(0);\nif (!acc.isOpen(0) || acc.openCount() !== 1) throw new Error("toggle(0) opens section 0.");\nacc.toggle(1);\nif (acc.isOpen(0)) throw new Error("Opening section 1 closes section 0 (single-open).");\nif (!acc.isOpen(1)) throw new Error("Section 1 is now open.");',
            hint: "Keep a single `open` index (-1 for none) rather than an array of booleans.",
          },
          {
            name: "toggling the open section closes it",
            code: 'const fn = new Function(code + "\\nreturn { createAccordion };");\nconst { createAccordion } = fn();\nconst acc = createAccordion(3);\nacc.toggle(2);\nacc.toggle(2);\nif (acc.isOpen(2) || acc.openCount() !== 0) throw new Error("Toggling the open section must close it.");',
            hint: "If i === open, set open = -1.",
          },
          {
            name: "out-of-range toggles are ignored safely",
            code: 'const fn = new Function(code + "\\nreturn { createAccordion };");\nconst { createAccordion } = fn();\nconst acc = createAccordion(3);\nacc.toggle(0);\nacc.toggle(-1);\nacc.toggle(7);\nif (!acc.isOpen(0) || acc.openCount() !== 1) throw new Error("Invalid indexes must not change state or throw.");',
            hint: "Guard: if (i < 0 || i >= count) return;",
          },
        ],
        vi: {
          title: "Trạng thái Accordion",
          prompt:
            "Viết `createAccordion(count)` RETURN một object với `toggle(i)`, `isOpen(i)`, và `openCount()`. Cùng lúc chỉ được một mục mở (accordion, không phải các mục độc lập): toggle mục đang mở sẽ đóng nó; toggle mục đang đóng sẽ mở nó và đóng mục trước đó. Index ngoài phạm vi không được làm crash hay đổi trạng thái. Ban đầu tất cả đóng.",
          tests: [
            {
              name: "hành vi đơn-mở",
              hint: "Giữ một chỉ số `open` duy nhất (-1 khi không mở gì) thay vì mảng boolean.",
            },
            { name: "toggle mục đang mở sẽ đóng nó", hint: "Nếu i === open thì gán open = -1." },
            {
              name: "toggle ngoài phạm vi bị bỏ qua an toàn",
              hint: "Chặn: if (i < 0 || i >= count) return;",
            },
          ],
        },
      },
    ],
  },
  [
    [
      "i2-modal-lifecycle",
      'function createModal() {\n  let open = false;\n  let previousFocus = null;\n  let root = null;\n  return {\n    open(trigger, panel) {\n      if (open) return "already-open";\n      open = true;\n      previousFocus = trigger;\n      root = panel;\n      return "opened";\n    },\n    close() {\n      if (!open) return "already-closed";\n      open = false;\n      root = null;\n      return previousFocus;\n    },\n    isOpen() {\n      return open;\n    },\n  };\n}',
      'function createModal() {\n  return { open() { return "opened"; }, close() { return "closed"; }, isOpen() { return true; } };\n}',
    ],
    [
      "i2-accordion",
      "function createAccordion(count) {\n  let open = -1;\n  return {\n    toggle(i) {\n      if (i < 0 || i >= count) return;\n      open = open === i ? -1 : i;\n    },\n    isOpen(i) {\n      return open === i;\n    },\n    openCount() {\n      return open === -1 ? 0 : 1;\n    },\n  };\n}",
      "function createAccordion(count) {\n  const states = Array(count).fill(false);\n  return {\n    toggle(i) { states[i] = !states[i]; },\n    isOpen(i) { return states[i]; },\n    openCount() { return states.filter(Boolean).length; },\n  };\n}",
    ],
  ],
);

// ── forms-practice ──────────────────────────────────────────────────────────
writePracticeSet(
  MOD,
  {
    file: "forms-practice.json",
    id: "forms-practice",
    title: "Advanced Forms — Practice",
    description:
      "Validate like the server will: field validators, password-match rules, and a row manager for dynamic field sets.",
    viTitle: "Form nâng cao — Luyện tập",
    viDescription:
      "Kiểm tra dữ liệu như server sẽ làm: bộ kiểm tra từng trường, luật khớp mật khẩu, và bộ quản lý dòng cho tập trường động.",
    afterLesson: "advanced-forms",
    minutes: 20,
    difficulty: "intermediate",
    challenges: [
      {
        id: "i2-validate-field",
        title: "Field Validator",
        prompt:
          "Write `validateField(name, value)` that RETURNS `null` when valid or an error-message string when not:\n\n- `name` — required, 2–40 characters after trim\n- `email` — must contain `@` with non-empty parts on both sides\n- `age` — a number 16–120 inclusive (accept numeric strings)\n\nAny other field name returns `null`.",
        difficulty: "intermediate",
        level: "guided",
        boilerplate:
          "function validateField(name, value) {\n  // returns null or an error message\n}\n",
        tests: [
          {
            name: "name rules",
            code: 'const fn = new Function(code + "\\nreturn { validateField };");\nconst { validateField } = fn();\nif (validateField("name", "  Ada  ") !== null) throw new Error("Trimmed Ada has length 3 - valid.");\nif (validateField("name", " a ") === null) throw new Error("A 1-character name must produce an error message.");\nif (validateField("name", "") === null) throw new Error("An empty name is required-missing.");',
            hint: "const v = value.trim(); check v.length >= 2 && v.length <= 40.",
          },
          {
            name: "email rules",
            code: 'const fn = new Function(code + "\\nreturn { validateField };");\nconst { validateField } = fn();\nif (validateField("email", "ada@example.com") !== null) throw new Error("ada@example.com is valid.");\nif (validateField("email", "ada@") === null) throw new Error("No domain part.");\nif (validateField("email", "@x.com") === null) throw new Error("No local part.");\nif (validateField("email", "no-at-sign") === null) throw new Error("Missing at-sign.");',
            hint: "Split on '@' — exactly one @, both sides non-empty.",
          },
          {
            name: "age rules",
            code: 'const fn = new Function(code + "\\nreturn { validateField };");\nconst { validateField } = fn();\nif (validateField("age", 30) !== null) throw new Error("30 is in range.");\nif (validateField("age", "30") !== null) throw new Error("Numeric strings are accepted.");\nif (validateField("age", 15) === null) throw new Error("15 is below the range.");\nif (validateField("age", "abc") === null) throw new Error("Non-numeric input must fail.");\nif (validateField("unknown", 5) !== null) throw new Error("Unknown fields always pass.");',
            hint: "Number(value) then Number.isFinite + range check; NaN fails the finite check for you.",
          },
        ],
        vi: {
          title: "Bộ kiểm tra trường",
          prompt:
            "Viết `validateField(name, value)` RETURN `null` khi hợp lệ hoặc chuỗi thông báo lỗi khi không:\n\n- `name` — bắt buộc, 2–40 ký tự sau khi trim\n- `email` — phải chứa `@` với hai bên không rỗng\n- `age` — số trong 16–120 (nhận cả chuỗi số)\n\nTên trường khác trả về `null`.",
          tests: [
            {
              name: "luật cho name",
              hint: "const v = value.trim(); kiểm tra v.length >= 2 && v.length <= 40.",
            },
            { name: "luật cho email", hint: "Tách theo '@' — đúng một @, hai bên không rỗng." },
            {
              name: "luật cho age",
              hint: "Number(value) rồi Number.isFinite + kiểm tra khoảng; NaN tự thất bại ở phép kiểm tra finite.",
            },
          ],
        },
      },
      {
        id: "i2-validate-form",
        title: "Whole-Form Validation",
        prompt:
          "Write `validateForm(values)` where `values` is an object of field→value. RETURN `{ valid, errors }` where `errors` maps field→message using the same rules as `validateField` (reuse it!), and `valid` is true only when `errors` is empty. Both fields of a cross-field pair must agree: `password` and `confirm` must match when both are present.",
        difficulty: "intermediate",
        level: "independent",
        boilerplate: "function validateForm(values) {\n  // reuse validateField\n}\n",
        tests: [
          {
            name: "collects every field's errors",
            code: 'const fn = new Function(code + "\\nreturn { validateForm };");\nconst { validateForm } = fn();\nconst out = validateForm({ name: "a", email: "bad", age: 9 });\nif (out.valid !== false) throw new Error("All three fields are invalid.");\nif (!out.errors.name || !out.errors.email || !out.errors.age) throw new Error("errors should carry a message for every invalid field.");',
            hint: "Loop Object.entries(values), call validateField, collect non-null results.",
          },
          {
            name: "valid form has empty errors",
            code: 'const fn = new Function(code + "\\nreturn { validateForm };");\nconst { validateForm } = fn();\nconst out = validateForm({ name: "Ada", email: "a@b.co", age: "30" });\nif (out.valid !== true) throw new Error("A fully valid form is valid.");\nif (Object.keys(out.errors).length !== 0) throw new Error("errors should be an empty object.");',
            hint: "valid is Object.keys(errors).length === 0.",
          },
          {
            name: "password/confirm cross-field rule",
            code: 'const fn = new Function(code + "\\nreturn { validateForm };");\nconst { validateForm } = fn();\nconst mismatch = validateForm({ password: "abc123", confirm: "abc124" });\nif (mismatch.valid !== false || !mismatch.errors.confirm) throw new Error("A confirm that does not match must set errors.confirm.");\nconst match = validateForm({ password: "abc123", confirm: "abc123" });\nif (match.valid !== true) throw new Error("Matching passwords pass.");',
            hint: "After the per-field loop, if both fields exist and differ, set errors.confirm.",
          },
        ],
        vi: {
          title: "Kiểm tra toàn form",
          prompt:
            "Viết `validateForm(values)` trong đó `values` là object field→value. RETURN `{ valid, errors }` trong đó `errors` ánh xạ field→message theo cùng luật với `validateField` (hãy tái sử dụng nó!), và `valid` chỉ đúng khi `errors` rỗng. Cặp liên trường phải khớp nhau: `password` và `confirm` phải giống nhau khi cả hai đều có mặt.",
          tests: [
            {
              name: "gom hết lỗi của từng trường",
              hint: "Duyệt Object.entries(values), gọi validateField, gom các kết quả khác null.",
            },
            {
              name: "form hợp lệ có errors rỗng",
              hint: "valid là Object.keys(errors).length === 0.",
            },
            {
              name: "luật liên trường password/confirm",
              hint: "Sau vòng lặp từng trường, nếu cả hai tồn tại và khác nhau thì gán errors.confirm.",
            },
          ],
        },
      },
      {
        id: "i2-row-manager",
        title: "Dynamic Row Manager",
        prompt:
          "Write `createRowManager()` that RETURNS an object managing rows (`{ id, label }`):\n\n- `add(label)` — appends a row with a unique **increasing** id starting at 1 and returns the id\n- `remove(id)` — removes that row; returns `true` if it existed, `false` otherwise\n- `list()` — returns the rows in insertion order\n- `move(id, toIndex)` — moves the row to `toIndex` in the list; returns `true` on success, `false` when the id is unknown or `toIndex` is out of range",
        difficulty: "intermediate",
        level: "independent",
        boilerplate: "function createRowManager() {\n  // your code\n}\n",
        tests: [
          {
            name: "add assigns increasing unique ids",
            code: 'const fn = new Function(code + "\\nreturn { createRowManager };");\nconst { createRowManager } = fn();\nconst m = createRowManager();\nconst a = m.add("first");\nconst b = m.add("second");\nif (a !== 1 || b !== 2) throw new Error("Ids must start at 1 and increase.");\nif (m.list().length !== 2) throw new Error("Both rows should be listed.");',
            hint: "Keep a nextId counter and a rows array in the closure.",
          },
          {
            name: "remove reports existence",
            code: 'const fn = new Function(code + "\\nreturn { createRowManager };");\nconst { createRowManager } = fn();\nconst m = createRowManager();\nconst id = m.add("x");\nif (m.remove(id) !== true) throw new Error("Removing an existing row returns true.");\nif (m.remove(id) !== false) throw new Error("Removing it again returns false.");\nif (m.list().length !== 0) throw new Error("The row is gone.");',
            hint: "findIndex, then splice when found.",
          },
          {
            name: "move reorders or fails safely",
            code: 'const fn = new Function(code + "\\nreturn { createRowManager };");\nconst { createRowManager } = fn();\nconst m = createRowManager();\nconst a = m.add("a");\nconst b = m.add("b");\nconst c = m.add("c");\nif (m.move(c, 0) !== true) throw new Error("Moving c to index 0 succeeds.");\nif (m.list().map((r) => r.id).join() !== [c, a, b].join()) throw new Error("Order should now be c, a, b.");\nif (m.move(999, 0) !== false) throw new Error("Unknown id fails.");\nif (m.move(a, 7) !== false) throw new Error("Out-of-range index fails.");',
            hint: "Find the row's current index; splice it out; splice it back at the target.",
          },
        ],
        vi: {
          title: "Bộ quản lý dòng động",
          prompt:
            "Viết `createRowManager()` RETURN một object quản lý các dòng (`{ id, label }`):\n\n- `add(label)` — thêm dòng với id duy nhất **tăng dần** bắt đầu từ 1 và trả về id đó\n- `remove(id)` — xóa dòng; trả `true` nếu tồn tại, `false` nếu không\n- `list()` — trả về các dòng theo thứ tự thêm vào\n- `move(id, toIndex)` — chuyển dòng đến vị trí `toIndex` trong danh sách; trả `true` khi thành công, `false` khi id lạ hoặc `toIndex` ngoài phạm vi",
          tests: [
            {
              name: "add gán id duy nhất tăng dần",
              hint: "Giữ bộ đếm nextId và mảng rows trong closure.",
            },
            { name: "remove báo đúng sự tồn tại", hint: "findIndex, rồi splice khi tìm thấy." },
            {
              name: "move sắp xếp lại hoặc thất bại an toàn",
              hint: "Tìm vị trí hiện tại của dòng; splice nó ra; splice trả lại ở vị trí đích.",
            },
          ],
        },
      },
    ],
  },
  [
    [
      "i2-validate-field",
      'function validateField(name, value) {\n  if (name === "name") {\n    const v = String(value).trim();\n    if (v.length < 2 || v.length > 40) return "name must be 2-40 characters";\n    return null;\n  }\n  if (name === "email") {\n    const s = String(value);\n    const at = s.indexOf("@");\n    if (at <= 0 || at === s.length - 1 || s.indexOf("@", at + 1) !== -1) {\n      return "email must be local@domain";\n    }\n    return null;\n  }\n  if (name === "age") {\n    const n = Number(value);\n    if (!Number.isFinite(n) || n < 16 || n > 120) return "age must be 16-120";\n    return null;\n  }\n  return null;\n}',
      "function validateField(name, value) { return null; }",
    ],
    [
      "i2-validate-form",
      'function validateField(name, value) {\n  if (name === "name") {\n    const v = String(value).trim();\n    if (v.length < 2 || v.length > 40) return "name must be 2-40 characters";\n    return null;\n  }\n  if (name === "email") {\n    const s = String(value);\n    const at = s.indexOf("@");\n    if (at <= 0 || at === s.length - 1 || s.indexOf("@", at + 1) !== -1) {\n      return "email must be local@domain";\n    }\n    return null;\n  }\n  if (name === "age") {\n    const n = Number(value);\n    if (!Number.isFinite(n) || n < 16 || n > 120) return "age must be 16-120";\n    return null;\n  }\n  return null;\n}\nfunction validateForm(values) {\n  const errors = {};\n  for (const [field, value] of Object.entries(values)) {\n    const msg = validateField(field, value);\n    if (msg) errors[field] = msg;\n  }\n  if (\n    "password" in values &&\n    "confirm" in values &&\n    values.password !== values.confirm\n  ) {\n    errors.confirm = "confirm must match password";\n  }\n  return { valid: Object.keys(errors).length === 0, errors };\n}',
      "function validateForm(values) {\n  return { valid: true, errors: {} };\n}",
    ],
    [
      "i2-row-manager",
      "function createRowManager() {\n  let nextId = 1;\n  let rows = [];\n  return {\n    add(label) {\n      const id = nextId++;\n      rows.push({ id, label });\n      return id;\n    },\n    remove(id) {\n      const i = rows.findIndex((r) => r.id === id);\n      if (i === -1) return false;\n      rows.splice(i, 1);\n      return true;\n    },\n    list() {\n      return rows;\n    },\n    move(id, toIndex) {\n      const from = rows.findIndex((r) => r.id === id);\n      if (from === -1) return false;\n      if (toIndex < 0 || toIndex >= rows.length) return false;\n      const [row] = rows.splice(from, 1);\n      rows.splice(toIndex, 0, row);\n      return true;\n    },\n  };\n}",
      "function createRowManager() {\n  let rows = [];\n  let nextId = 1;\n  return {\n    add(label) { rows.push({ id: 0, label }); return 0; },\n    remove() { return false; },\n    list() { return rows; },\n    move() { return false; },\n  };\n}",
    ],
  ],
);

console.log("Module 2 practices (delegation, components, forms) written.");
