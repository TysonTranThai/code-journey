#!/usr/bin/env python3
"""Module 4: advanced-css-ui-engineering — lessons + practices."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_module, write_lesson, write_checkpoint, write_practice, fn_wrap

MOD = "advanced-css-ui-engineering"

write_module(
    MOD,
    "Advanced CSS & UI Engineering",
    "Engineer interfaces, not just style them: custom properties and theming, cascade layers, container queries, fluid type, advanced Grid/Flexbox, and motion with respect.",
    "CSS nâng cao & Kỹ thuật UI",
    "Thiết kế giao diện một cách kỹ thuật, không chỉ tô màu: custom properties và theming, cascade layers, container queries, chữ động, Grid/Flexbox nâng cao, và chuyển động có trách nhiệm.",
    [
        "custom-properties-theming",
        "cascade-layers",
        "container-queries",
        "advanced-grid-flexbox",
        "component-states-a11y",
        "motion-reduced-motion",
        "ui-system-checkpoint",
    ],
    [
        "tokens-practice",
        "layout-practice",
        "container-practice",
        "components-practice",
        "motion-practice",
        "dashboard-build-practice",
    ],
)

# ── custom-properties-theming ───────────────────────────────────────────────
write_lesson(
    MOD, "custom-properties-theming",
    "Custom Properties & Theming",
    "Design tokens as custom properties, cascade-driven theming, light/dark via prefers-color-scheme, and computed values with var() and calc().",
    15,
    """
Custom properties (CSS variables) are the backbone of maintainable CSS:
**tokens** that cascade, inherit, and can change per-scope — something
preprocessor variables never could.

## Tokens

~~~css
:root {
  --color-bg: #ffffff;
  --color-fg: #111827;
  --color-accent: #2563eb;
  --radius: 8px;
  --space-1: 0.25rem;
}
.card {
  background: var(--color-bg);
  border-radius: var(--radius);
  padding: calc(4 * var(--space-1));
}
~~~

`var()` reads at *use time* through the cascade; `calc()` computes lengths from
tokens. Change `--color-bg` on any subtree and every usage updates.

## Theming is just re-declaration

Because tokens cascade, a theme is a scope that re-declares them:

~~~css
[data-theme="dark"] {
  --color-bg: #0b1120;
  --color-fg: #e2e8f0;
}
~~~

Every component using `var(--color-bg)` is now dark-mode aware with zero
component changes. Honor the system preference by default and let an explicit
choice override:

~~~css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { /* dark tokens */ }
}
~~~

## Fallbacks and invalid at computed-value time

`var(--missing, #333)` provides a fallback. A property referencing an undefined
var becomes *invalid at computed-value time* — it falls back to its inherited
or initial value, which is rarely what you want. Define tokens at `:root` and
treat them as an API.
""",
    "Custom Properties & Theming",
    "Design token như custom properties, theming bằng cascade, sáng/tối qua prefers-color-scheme, và giá trị tính được với var() cùng calc().",
    """
Custom properties (biến CSS) là xương sống của CSS dễ bảo trì: **token** có thể
cascade, kế thừa, và đổi giá trị theo từng phạm vi — điều biến của preprocessor
chưa bao giờ làm được.

## Token

~~~css
:root {
  --color-bg: #ffffff;
  --color-fg: #111827;
  --color-accent: #2563eb;
  --radius: 8px;
  --space-1: 0.25rem;
}
.card {
  background: var(--color-bg);
  border-radius: var(--radius);
  padding: calc(4 * var(--space-1));
}
~~~

`var()` đọc *tại thời điểm sử dụng* qua cascade; `calc()` tính chiều dài từ
token. Đổi `--color-bg` trên bất kỳ cây con nào và mọi chỗ dùng nó cập nhật
theo.

## Theming chỉ là khai báo lại

Nhờ token cascade, một theme chỉ là một phạm vi khai báo lại chúng:

~~~css
[data-theme="dark"] {
  --color-bg: #0b1120;
  --color-fg: #e2e8f0;
}
~~~

Mọi component dùng `var(--color-bg)` giờ biết dark mode mà không cần sửa gì.
Hãy tôn trọng tùy chọn hệ thống làm mặc định và cho lựa chọn tường minh ghi đè:

~~~css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { /* token tối */ }
}
~~~

## Fallback và invalid at computed-value time

`var(--missing, #333)` cung cấp fallback. Một thuộc tính tham chiếu var chưa
định nghĩa sẽ trở thành *invalid at computed-value time* — nó rơi về giá trị
kế thừa hoặc mặc định, hiếm khi là điều bạn muốn. Hãy định nghĩa token ở
`:root` và coi chúng như một API.
""",
)

# ── cascade-layers ──────────────────────────────────────────────────────────
write_lesson(
    MOD, "cascade-layers",
    "Cascade Layers & Specificity Without Tears",
    "@layer to order the cascade deliberately, specificity math, :where() for zero-specificity resets, and isolation strategies.",
    13,
    """
The cascade is not an accident to fight — it is a system to order. `@layer`
gives you explicit control.

## Layers beat specificity

Declarations in a **later** layer win over earlier ones — regardless of
specificity:

~~~css
@layer reset, base, components, utilities;

@layer reset {
  * { margin: 0; }
}
@layer components {
  .btn { padding: 0.5rem 1rem; }
}
@layer utilities {
  .p-0 { padding: 0 !important-free; } /* utilities beat components */
}
~~~

(That comment is a marker, not syntax — utilities win because the layer is
declared later.) A `.p-0` utility now overrides component padding without
`!important`, because `utilities` outranks `components` by layer order.

## The ordering rule

Layer order is fixed at first declaration: `@layer reset, base, components,
utilities;` sets the priority low→high. Un-layered styles beat all layered
styles — that is how overrides ship last.

## :where() — specificity you can spend

`:where(...)` contributes **zero** specificity, perfect for resets that must
always lose:

~~~css
:where(h1, h2, h3) { margin-block: 0.5em; }
~~~

Any author rule now beats it. `:is()` is the same list but *takes* the highest
specificity of its arguments — use it when the match should count.

## When to reach for each

- Layers: organize whole stylesheets; make third-party CSS overridable.
- `:where()`: resets and defaults that must be cheap to override.
- `!important`: last resort, then only for utility layers by convention.
""",
    "Cascade Layers & Specificity Không Cần Khóc Lóc",
    "@layer để điều phối cascade một cách chủ đích, tính specificity, :where() cho reset có specificity bằng 0, và các chiến lược cô lập.",
    """
Cascade không phải điều ngẫu nhiên để chống lại — nó là một hệ thống để sắp
xếp. `@layer` trao cho bạn quyền kiểm soát tường minh.

## Layer thắng specificity

Khai báo trong layer **sau** thắng layer trước — bất kể specificity:

~~~css
@layer reset, base, components, utilities;

@layer reset {
  * { margin: 0; }
}
@layer components {
  .btn { padding: 0.5rem 1rem; }
}
@layer utilities {
  .p-0 { padding: 0; } /* utilities thắng components nhờ thứ tự layer */
}
~~~

Một utility `.p-0` giờ ghi đè padding của component mà không cần `!important`,
vì layer `utilities` đứng trên `components` theo thứ tự layer.

## Quy tắc thứ tự

Thứ tự layer được cố định ngay lần khai báo đầu: `@layer reset, base,
components, utilities;` thiết lập độ ưu tiên thấp→cao. Style không nằm trong
layer nào thắng mọi layer — đó là cách các bản ghi đè được đặt ở cuối.

## :where() — specificity mà bạn có thể tiêu

`:where(...)` đóng góp **zero** specificity — hoàn hảo cho reset luôn phải thua:

~~~css
:where(h1, h2, h3) { margin-block: 0.5em; }
~~~

Bất kỳ quy tắc nào của tác giả giờ đều thắng nó. `:is()` cùng danh sách đó
nhưng *chiếm* specificity cao nhất trong các đối số — dùng khi phép khớp cần
được tính.

## Khi nào dùng cái nào

- Layer: tổ chức cả stylesheet; làm CSS bên thứ ba dễ bị ghi đè.
- `:where()`: reset và mặc định mà việc ghi đè phải rẻ.
- `!important`: phương án cuối, và theo quy ước chỉ dành cho layer utility.
""",
)

# ── container-queries ───────────────────────────────────────────────────────
write_lesson(
    MOD, "container-queries",
    "Container Queries: Components That Adapt",
    "Query a component's own box instead of the viewport — the shift from page-responsive to component-responsive design.",
    14,
    """
Media queries ask "how wide is the *viewport*?" Container queries ask "how wide
is *my box*?" — which is what components actually need.

## Setup

~~~css
.card-wrapper { container-type: inline-size; }

@container (min-width: 400px) {
  .card { display: grid; grid-template-columns: 96px 1fr; }
}
~~~

`container-type: inline-size` marks the element as a size container on the
inline axis. The `@container` rule applies its styles **based on the nearest
ancestor container** — the same `.card` can be horizontal in a wide sidebar slot
and vertical in a narrow one, with no JavaScript and no viewport assumptions.

## Why this changes architecture

With media queries, a component's looks depend on where the *page* is — so
reusing a card in two layouts means duplicating breakpoints. With containers,
the component owns its responsive behavior; drop it anywhere and it adapts.
This is the foundation of design systems built from independent parts.

## Fluid type with clamp()

Between fixed breakpoints, `clamp()` interpolates smoothly:

~~~css
h1 { font-size: clamp(1.75rem, 1rem + 3vw, 3.5rem); }
/* min, preferred (grows with viewport), max */
~~~

Pair `clamp()` with container-query layout and components stay readable from
320px to ultrawide without a single extra breakpoint.
""",
    "Container Queries: Component Tự Thích Ứng",
    "Truy vấn chính hộp của component thay vì viewport — bước chuyển từ responsive theo trang sang responsive theo component.",
    """
Media query hỏi "viewport *rộng bao nhiêu*?" Container query hỏi "hộp của tôi
*rộng bao nhiêu*?" — chính là điều component thực sự cần.

## Cài đặt

~~~css
.card-wrapper { container-type: inline-size; }

@container (min-width: 400px) {
  .card { display: grid; grid-template-columns: 96px 1fr; }
}
~~~

`container-type: inline-size` đánh dấu phần tử là size container trên trục
inline. Quy tắc `@container` áp style của nó **dựa trên container tổ tiên gần
nhất** — cùng một `.card` có thể nằm ngang trong một ô sidebar rộng và xếp dọc
trong ô hẹp, không cần JavaScript và không giả định gì về viewport.

## Vì sao điều này thay đổi kiến trúc

Với media query, diện mạo của component phụ thuộc vào vị trí của *trang* — nên
dùng lại một card trong hai layout đồng nghĩa với nhân đôi breakpoint. Với
container, component tự sở hữu hành vi responsive của mình; thả vào đâu cũng
tự thích ứng. Đây là nền móng của hệ thống thiết kế xây từ các phần độc lập.

## Chữ động với clamp()

Giữa các breakpoint cố định, `clamp()` nội suy mượt:

~~~css
h1 { font-size: clamp(1.75rem, 1rem + 3vw, 3.5rem); }
/* min, preferred (tăng theo viewport), max */
~~~

Kết hợp `clamp()` với layout theo container query và component luôn dễ đọc từ
320px đến siêu rộng mà không cần thêm breakpoint nào.
""",
)

# ── advanced-grid-flexbox ───────────────────────────────────────────────────
write_lesson(
    MOD, "advanced-grid-flexbox",
    "Advanced Grid & Flexbox",
    "Named areas, auto-fit minmax, subgrid ideas, flex-grow math, and choosing grid vs flex per layout problem.",
    16,
    """
You know both systems from Beginner; now use them deliberately.

## Grid: areas and auto-fit

Template areas make layouts readable as diagrams:

~~~css
.dashboard {
  display: grid;
  grid-template-areas:
    "head head"
    "side main"
    "side foot";
  grid-template-columns: 240px 1fr;
}
~~~

For unknown item counts, `repeat(auto-fit, minmax(min, 1fr))` builds columns
that wrap without media queries:

~~~css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}
~~~

`auto-fit` collapses empty tracks (items stretch); `auto-fill` keeps empty
tracks (items keep max width). Pick per intent.

## Flexbox: grow math

`flex: <grow> <shrink> <basis>` — free space distributes by grow ratios after
basis is reserved. `flex: 1` is `1 1 0%`: equal split ignoring content width.
`flex: auto` is `1 1 auto`: split *surplus* while respecting content width —
the difference matters with variable-width content.

## Choosing

- One-dimensional flow (toolbars, tag lists, form rows): **flex**.
- Two-dimensional structure (page shells, galleries, dashboards): **grid**.
- Component internals often use both: grid for the shell, flex inside cells.
""",
    "Grid & Flexbox nâng cao",
    "Named areas, auto-fit minmax, ý tưởng subgrid, phép tính flex-grow, và cách chọn grid hay flex cho từng bài toán layout.",
    """
Bạn đã biết cả hai hệ từ khóa Người mới bắt đầu; giờ hãy dùng chúng một cách
chủ đích.

## Grid: areas và auto-fit

Template areas làm layout đọc được như sơ đồ:

~~~css
.dashboard {
  display: grid;
  grid-template-areas:
    "head head"
    "side main"
    "side foot";
  grid-template-columns: 240px 1fr;
}
~~~

Với số lượng phần tử không biết trước, `repeat(auto-fit, minmax(min, 1fr))`
dựng các cột tự xuống dòng mà không cần media query:

~~~css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}
~~~

`auto-fit` gộp các track rỗng (phần tử giãn hết); `auto-fill` giữ track rỗng
(phần tử giữ chiều rộng tối đa). Chọn theo ý đồ.

## Flexbox: phép tính grow

`flex: <grow> <shrink> <basis>` — không gian dư được phân theo tỷ lệ grow sau
khi basis đã được giữ chỗ. `flex: 1` là `1 1 0%`: chia đều bất kể độ rộng nội
dung. `flex: auto` là `1 1 auto`: chia phần *thừa* trong khi tôn trọng độ rộng
nội dung — khác biệt này quan trọng với nội dung có độ rộng thay đổi.

## Cách chọn

- Luồng một chiều (toolbar, danh sách tag, hàng form): **flex**.
- Cấu trúc hai chiều (khung trang, gallery, dashboard): **grid**.
- Bên trong component thường dùng cả hai: grid cho khung, flex trong từng ô.
""",
)

# ── component-states-a11y ───────────────────────────────────────────────────
write_lesson(
    MOD, "component-states-a11y",
    "Component States & Accessible Interactions",
    "Hover/focus/disabled contract, focus-visible, stacking contexts, accessible modal disclosure, and ARIA only where needed.",
    14,
    """
A component is its states. Engineering them — visibly and accessibly — is the
difference between decoration and UI.

## The state contract

Every interactive element owes: **hover** (affordance), **focus** (keyboard
parity with hover), **active** (feedback), **disabled** (clearly non-interactive,
still perceivable), **aria-disabled** when it must stay focusable. Never remove
focus outlines without a `:focus-visible` replacement:

~~~css
button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
~~~

`:focus-visible` shows rings for keyboard users and skips them for pointer
users — the best of both.

## Stacking contexts

`z-index` only ranks within its **stacking context** — created by position +
z-index, opacity < 1, transform, filter, and more. A modal inside a
`transform: translateY(0)` card cannot rise above a sibling with z-index 10 in
another context. Debug with DevTools' 3D/layers view; fix by keeping overlays
in flat subtrees (often portaled to body).

## Disclosure semantics

For toggled UI, wire semantics with states — no heavy ARIA libraries needed:

~~~html
<button aria-expanded="false" aria-controls="menu">Menu</button>
<div id="menu" hidden>…</div>
~~~

Flip `aria-expanded` and `hidden` together from one source of truth. Reach for
`role` only when the platform has no native element (dialogs get native
`<dialog>`); native first, ARIA second.
""",
    "Trạng thái Component & Tương tác Tiếp cận được",
    "Hợp đồng hover/focus/disabled, focus-visible, stacking context, mô tả modal tiếp cận được, và ARIA chỉ khi cần thiết.",
    """
Một component là tổng thể các trạng thái của nó. Thiết kế chúng — nhìn thấy
được và tiếp cận được — là ranh giới giữa trang trí và UI.

## Hợp đồng trạng thái

Mọi phần tử tương tác nợ người dùng: **hover** (gợi ý), **focus** (ngang hàng
với hover khi dùng bàn phím), **active** (phản hồi), **disabled** (rõ ràng
không tương tác nhưng vẫn nhận biết được), và **aria-disabled** khi nó bắt buộc
vẫn giữ focus. Đừng bao giờ bỏ viền focus mà không có `:focus-visible` thay thế:

~~~css
button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
~~~

`:focus-visible` hiện viền cho người dùng bàn phím và bỏ qua với chuột — lợi cả
hai đường.

## Stacking context

`z-index` chỉ xếp hạng trong **stacking context** của nó — được tạo bởi
position + z-index, opacity < 1, transform, filter, và nhiều thứ khác. Một
modal nằm trong card có `transform: translateY(0)` không thể nổi trên phần tử
anh em có z-index 10 ở context khác. Dùng chế độ xem 3D/layers của DevTools để
soi lỗi; sửa bằng cách giữ overlay trong cây phẳng (thường là portal ra body).

## Ngữ nghĩa mô tả/thu gọn

Với UI bật/tắt, hãy nối ngữ nghĩa với trạng thái — không cần thư viện ARIA lớn:

~~~html
<button aria-expanded="false" aria-controls="menu">Menu</button>
<div id="menu" hidden>…</div>
~~~

Đảo `aria-expanded` và `hidden` cùng nhau từ một nguồn sự thật duy nhất. Chỉ
dùng `role` khi nền tảng không có phần tử gốc (dialog có `<dialog>` gốc);
native trước, ARIA sau.
""",
)

# ── motion-reduced-motion ───────────────────────────────────────────────────
write_lesson(
    MOD, "motion-reduced-motion",
    "Motion With Manners",
    "Transitions vs animations, transform/opacity-only performance rules, prefers-reduced-motion, and persisting motion choices.",
    12,
    """
Motion communicates state changes; done carelessly it also communicates
nausea.

## Animate the cheap properties

Only `transform` and `opacity` animate on the compositor without triggering
layout or paint. Everything else (width, top, margin) re-flows the page every
frame:

~~~css
.drawer { transition: transform 0.25s ease; }
.drawer.is-closed { transform: translateX(-100%); }
~~~

Move with transforms; fade with opacity; size with `scale()` when geometry
allows. Duration under ~300ms for interactions; entrance animations may be
slightly longer.

## Respect the preference

Some users turn animations off at the OS level. Honor it globally:

~~~css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
~~~

States still change instantly — information is preserved, movement is not
forced on anyone.

## Transitions vs animations

`transition` reacts to a state change between two values — perfect for hover,
open/close. `@keyframes` animation runs on its own timeline — loops, multi-step
sequences. If you find yourself writing JS to toggle a transition, you probably
wanted a class change; if you need orchestration, keyframes or the Web
Animations API.
""",
    "Chuyển động Có Đúng Mức",
    "Transition so với animation, quy tắc chỉ dùng transform/opacity để đạt hiệu năng, prefers-reduced-motion, và lưu lựa chọn về chuyển động.",
    """
Chuyển động truyền tải thay đổi trạng thái; làm thiếu cẩn thận, nó cũng truyền
tải cả cơn say xe.

## Chỉ animate các thuộc tính rẻ

Chỉ có `transform` và `opacity` được animate trên compositor mà không gây
layout hay paint. Mọi thứ khác (width, top, margin) làm trang re-flow từng
khung hình:

~~~css
.drawer { transition: transform 0.25s ease; }
.drawer.is-closed { transform: translateX(-100%); }
~~~

Di chuyển bằng transform; mờ dần bằng opacity; đổi kích thước bằng `scale()`
khi hình học cho phép. Thời lượng dưới ~300ms cho tương tác; animation xuất
hiện có thể dài hơn chút.

## Tôn trọng tùy chọn của người dùng

Một số người tắt animation ở cấp hệ điều hành. Hãy tôn trọng điều đó trên toàn
site:

~~~css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
~~~

Trạng thái vẫn đổi ngay lập tức — thông tin được giữ nguyên, chuyển động không
bị ép lên ai.

## Transition so với animation

`transition` phản ứng với một thay đổi trạng thái giữa hai giá trị — hợp với
hover, mở/đóng. Animation `@keyframes` chạy theo timeline riêng — vòng lặp,
chuỗi nhiều bước. Nếu bạn đang viết JS để bật một transition, có lẽ bạn chỉ cần
đổi class; nếu cần biên đạo nhiều bước, hãy dùng keyframes hoặc Web Animations
API.
""",
)

# ── checkpoint ──────────────────────────────────────────────────────────────
write_checkpoint(
    MOD,
    "ui-system-checkpoint",
    "Checkpoint: UI System Logic",
    "Verify the module's reasoning at the logic level: token resolution order, a theme switcher reducer, and motion-preference handling.",
    18,
    """
The practices below run CSS through declaration checks and component logic
through JS. The checkpoint verifies your *reasoning*: token cascade order,
theme state handling, and reduced-motion policy as pure functions.

1. `resolveTokens(scopes)` — later scopes override earlier token by token.
2. `applyTheme(state, action)` — a reducer for theme state with system
   fallback.
3. `motionPolicy(prefersReduced, userSetting)` — decide the effective motion
   mode.
""",
    "Kiểm tra kiến thức: Logic Hệ thống UI",
    "Xác minh suy luận của module ở tầng logic: thứ tự phân giải token, reducer cho bộ chuyển theme, và xử lý tùy chọn chuyển động.",
    """
Các bài luyện bên dưới kiểm tra CSS qua các khai báo và logic component qua
JS. Bài kiểm tra này xác minh *suy luận* của bạn: thứ tự cascade của token,
xử lý trạng thái theme, và chính sách reduced-motion dưới dạng hàm thuần.

1. `resolveTokens(scopes)` — phạm vi sau ghi đè phạm vi trước, tính theo từng
   token.
2. `applyTheme(state, action)` — một reducer cho trạng thái theme có fallback
   về hệ thống.
3. `motionPolicy(prefersReduced, userSetting)` — quyết định chế độ chuyển động
   hiệu dụng.
""",
    {
        "id": "i2-ui-checkpoint",
        "title": "UI System Logic Check",
        "prompt": "Implement three UI-system helpers:\n\n1. `resolveTokens(scopes)` — `scopes` is an array of token objects applied in order (earliest first). RETURN one merged object; later scopes override earlier ones token by token.\n2. `applyTheme(state, action)` — state is `{ mode: \"light\" | \"dark\" | \"system\", explicit: boolean }`. Actions: `{ type: \"set\", mode }` sets an explicit mode, `{ type: \"reset\" }` returns to `{ mode: \"system\", explicit: false }`. RETURN the new state; never mutate the input.\n3. `motionPolicy(prefersReducedMotion, userSetting)` — `userSetting` is `\"system\" | \"reduced\" | \"full\"`. RETURN `\"reduced\"` when the user explicitly chose reduced OR (user chose system AND prefersReducedMotion is true); otherwise `\"full\"`.",
        "difficulty": "intermediate",
        "boilerplate": "// 1) resolveTokens(scopes)\n\n// 2) applyTheme(state, action)\n\n// 3) motionPolicy(prefersReducedMotion, userSetting)\n",
        "tests": [
            {
                "name": "later scopes override token by token",
                "code": fn_wrap("resolveTokens, applyTheme, motionPolicy", "resolveTokens, applyTheme, motionPolicy") + "\nconst out = resolveTokens([\n  { \"--color-bg\": \"white\", \"--color-fg\": \"black\" },\n  { \"--color-bg\": \"navy\" },\n]);\nif (out[\"--color-bg\"] !== \"navy\") throw new Error(\"Later scopes win per token.\");\nif (out[\"--color-fg\"] !== \"black\") throw new Error(\"Tokens absent from later scopes survive.\");\nconst input = { a: 1 };\nresolveTokens([input]);\nif (input.a !== 1 || Object.keys(input).length !== 1) throw new Error(\"Input scopes must not be mutated.\");",
                "hint": "Reduce with { ...acc, ...scope }.",
            },
            {
                "name": "theme reducer sets, resets, and never mutates",
                "code": fn_wrap("resolveTokens, applyTheme, motionPolicy", "resolveTokens, applyTheme, motionPolicy") + "\nconst s = { mode: \"system\", explicit: false };\nconst set = applyTheme(s, { type: \"set\", mode: \"dark\" });\nif (set.mode !== \"dark\" || set.explicit !== true) throw new Error(\"set makes the mode explicit.\");\nif (s.mode !== \"system\" || s.explicit !== false) throw new Error(\"The input state must not be mutated.\");\nconst reset = applyTheme(set, { type: \"reset\" });\nif (reset.mode !== \"system\" || reset.explicit !== false) throw new Error(\"reset returns to the system default.\");",
                "hint": "Return new objects: { ...state, mode: action.mode, explicit: true }.",
            },
            {
                "name": "motion policy respects explicit and system choices",
                "code": fn_wrap("resolveTokens, applyTheme, motionPolicy", "resolveTokens, applyTheme, motionPolicy") + "\nif (motionPolicy(true, \"full\") !== \"full\") throw new Error(\"An explicit 'full' choice beats the OS preference.\");\nif (motionPolicy(true, \"reduced\") !== \"reduced\") throw new Error(\"Explicit reduced always reduces.\");\nif (motionPolicy(true, \"system\") !== \"reduced\") throw new Error(\"System + prefers-reduced-motion reduces.\");\nif (motionPolicy(false, \"system\") !== \"full\") throw new Error(\"System without the OS preference is full.\");",
                "hint": "userSetting === 'reduced' || (userSetting === 'system' && prefersReducedMotion) ? 'reduced' : 'full'.",
            },
        ],
    },
    {
        "title": "Kiểm tra kiến thức: Logic Hệ thống UI",
        "prompt": "Cài đặt ba hàm hệ thống UI:\n\n1. `resolveTokens(scopes)` — `scopes` là mảng các object token được áp theo thứ tự (sớm nhất trước). RETURN một object hợp nhất; phạm vi sau ghi đè phạm vi trước tính theo từng token.\n2. `applyTheme(state, action)` — state là `{ mode: \"light\" | \"dark\" | \"system\", explicit: boolean }`. Các action: `{ type: \"set\", mode }` đặt mode tường minh, `{ type: \"reset\" }` trả về `{ mode: \"system\", explicit: false }`. RETURN trạng thái mới; không bao giờ làm thay đổi input.\n3. `motionPolicy(prefersReducedMotion, userSetting)` — `userSetting` là `\"system\" | \"reduced\" | \"full\"`. RETURN `\"reduced\"` khi người dùng chọn reduced tường minh HOẶC (user chọn system VÀ prefersReducedMotion là true); nếu không thì `\"full\"`.",
        "tests": [
            {"name": "phạm vi sau ghi đè theo từng token", "hint": "Reduce với { ...acc, ...scope }."},
            {"name": "reducer theme set, reset, không đụng vào input", "hint": "Trả về object mới: { ...state, mode: action.mode, explicit: true }."},
            {"name": "chính sách motion tôn trọng lựa chọn tường minh và hệ thống", "hint": "userSetting === 'reduced' || (userSetting === 'system' && prefersReducedMotion) ? 'reduced' : 'full'."},
        ],
    },
)

print("Module 4 lessons + checkpoint written.")
