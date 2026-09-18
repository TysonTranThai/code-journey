#!/usr/bin/env python3
"""Module 5: typescript-essentials — lessons + practices + checkpoint.

The sandbox runs JavaScript, so TypeScript challenges grade the CONCEPTS via
plain-JS twins: runtime narrowing (typeof/in guards), result shapes generics
produce, and typed-API response validation. Lesson MDX teaches real TS syntax.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_module, write_lesson, write_checkpoint, write_practice, fn_wrap

MOD = "typescript-essentials"

write_module(
    MOD,
    "TypeScript Essentials",
    "Types as design tools, not bureaucracy: inference, unions and narrowing, generics, unknown at the boundaries — and the errors types catch before runtime.",
    "TypeScript Cốt Lõi",
    "Kiểu dữ liệu như công cụ thiết kế, không phải thủ tục hành chính: suy diễn kiểu, union và narrowing, generics, unknown ở biên giới — và những lỗi mà kiểu bắt được trước cả runtime.",
    [
        "why-types",
        "everyday-types",
        "unions-narrowing",
        "generics",
        "unknown-never",
        "typing-apis-dom",
        "type-safe-checkpoint",
    ],
    [
        "inference-practice",
        "unions-practice",
        "generics-practice",
        "boundaries-practice",
        "ts-client-practice",
    ],
)

# ── why-types ───────────────────────────────────────────────────────────────
write_lesson(
    MOD, "why-types",
    "Why Types Exist",
    "The failure modes types prevent, inference vs annotation, structural typing, and strict mode as a philosophy.",
    13,
    """
JavaScript fails at runtime: `user.nmae` is `undefined` three screens away
from the typo. TypeScript moves whole classes of those failures to the editor,
before the code ever runs.

## What types buy you

~~~ts
function subtotal(items: CartItem[]): number {
  return items.reduce((sum, i) => sum + i.price * i.qty, 0);
}
subtotal("cart");                 // ✗ compile error
subtotal([{ price: 5, qty: 2 }]); // ✓ — and price/qty autocomplete
~~~

Renaming a field updates every usage; a missed callsite turns red. That is not
ceremony — it is a searchable, checkable contract.

## Inference first, annotations at boundaries

TypeScript infers most types — annotate where inference cannot help:

~~~ts
const rates = [0.2, 0.15];            // inferred: number[]
function tax(amount: number) { ... }  // boundary: parameters
const total = tax(100);               // inferred: number
~~~

Annotating every local is noise; annotating nothing pushes surprises to call
sites. The convention: annotate function parameters and exported APIs, let
locals infer.

## Structural typing

TypeScript types by **shape**, not name — any object with the right members
fits, no inheritance required:

~~~ts
type Point = { x: number; y: number };
const p = { x: 1, y: 2, label: "origin" }; // OK: has x and y (extra is fine here)
~~~

Run `tsc --noEmit` as your gate: it checks without emitting. Strict mode
(`strict: true`) enables the checks that matter — null checking above all.
""",
    "Vì Sao Types Tồn Tại",
    "Các chế độ lỗi mà types ngăn chặn, suy diễn so với chú thích kiểu, structural typing, và strict mode như một triết lý.",
    """
JavaScript thất bại lúc runtime: `user.nmae` là `undefined` ở cách ba màn
hình khỏi chỗ gõ sai. TypeScript chuyển cả một lớp lỗi đó về editor — trước
khi code kịp chạy.

## Types mua cho bạn gì

~~~ts
function subtotal(items: CartItem[]): number {
  return items.reduce((sum, i) => sum + i.price * i.qty, 0);
}
subtotal("cart");                 // ✗ lỗi khi compile
subtotal([{ price: 5, qty: 2 }]); // ✓ — và price/qty có autocomplete
~~~

Đổi tên một trường thì mọi chỗ dùng được cập nhật; chỗ nào bỏ sót sẽ đỏ ngay.
Đó không phải nghi lễ — đó là hợp đồng tìm được bằng tìm kiếm và kiểm tra được
bằng máy.

## Suy diễn trước, chú thích ở biên giới

TypeScript suy diễn hầu hết kiểu — chỉ chú thích nơi suy diễn không giúp được:

~~~ts
const rates = [0.2, 0.15];            // tự suy diễn: number[]
function tax(amount: number) { ... }  // biên giới: tham số
const total = tax(100);               // tự suy diễn: number
~~~

Chú thích từng biến cục bộ là ồn ào; không chú thích gì thì đẩy bất ngờ về chỗ
gọi. Quy ước: chú thích tham số hàm và API export, biến cục bộ để TypeScript
tự suy.

## Structural typing

TypeScript phân loại theo **hình dạng**, không phải tên — bất kỳ object nào có
đúng các thành viên đều khớp, không cần kế thừa:

~~~ts
type Point = { x: number; y: number };
const p = { x: 1, y: 2, label: "origin" }; // OK: có x và y (thừa label không sao)
~~~

Hãy chạy `tsc --noEmit` làm cổng kiểm tra: nó kiểm mà không sinh file. Strict
mode (`strict: true`) bật các kiểm tra quan trọng — null checking trên hết.
""",
)

# ── everyday-types ──────────────────────────────────────────────────────────
write_lesson(
    MOD, "everyday-types",
    "Everyday Types",
    "Primitives, arrays, objects, optional and readonly members, type aliases vs interfaces, and literal types.",
    14,
    """
The vocabulary you will use daily.

## Objects, optional, readonly

~~~ts
type User = {
  id: number;
  email: string;
  displayName?: string;      // may be absent — type is string | undefined
  readonly createdAt: Date;  // cannot be reassigned
};
~~~

`?` changes the type AND the shape-check: callers may omit it. `readonly`
blocks reassignment (not deep freezing).

## Aliases and interfaces

~~~ts
type ID = string | number;          // aliases: unions, primitives, generics
interface Repo { url: string; }     // interfaces: object shapes, extendable
interface Repo { stars: number; }   // declaration merging (feature or footgun)
~~~

Either works for objects; reach for `type` when you need unions, mapped types,
or utilities; `interface` when a library expects to extend your shape. Consistency
matters more than the choice.

## Literal types

A literal type is one exact value — combined with unions, it becomes an enum
without the enum:

~~~ts
type Direction = "north" | "east" | "south" | "west";
type Size = "sm" | "md" | "lg";
function move(dir: Direction, by: Size) { ... }
move("up", "md"); // ✗ "up" is not assignable
~~~

Arrays and tuples: `string[]` is many strings; `[string, number]` is exactly
two, typed per position — useful for key/value pairs and fixed results.
""",
    "Các Kiểu Hằng Ngày",
    "Kiểu nguyên thủy, mảng, object, thành phần optional và readonly, type alias so với interface, và literal type.",
    """
Từ vựng bạn sẽ dùng mỗi ngày.

## Object, optional, readonly

~~~ts
type User = {
  id: number;
  email: string;
  displayName?: string;      // có thể vắng mặt — kiểu là string | undefined
  readonly createdAt: Date;  // không thể gán lại
};
~~~

Dấu `?` đổi cả kiểu lẫn phép kiểm tra hình dạng: chỗ gọi được phép bỏ qua.
`readonly` chặn việc gán lại (không phải đóng băng sâu).

## Alias và interface

~~~ts
type ID = string | number;          // alias: union, primitive, generics
interface Repo { url: string; }     // interface: hình dạng object, có thể extends
interface Repo { stars: number; }   // declaration merging (tính năng hay bẫy)
~~~

Cả hai đều dùng được cho object; chọn `type` khi cần union, mapped type hay
utility; chọn `interface` khi thư viện muốn extends hình dạng của bạn. Tính
nhất quán quan trọng hơn lựa chọn.

## Literal type

Literal type là một giá trị duy nhất — kết hợp với union, nó trở thành enum mà
không cần enum:

~~~ts
type Direction = "north" | "east" | "south" | "west";
type Size = "sm" | "md" | "lg";
function move(dir: Direction, by: Size) { ... }
move("up", "md"); // ✗ "up" không thuộc Direction
~~~

Mảng và tuple: `string[]` là nhiều chuỗi; `[string, number]` là đúng hai phần
tử, từng vị trí một kiểu — hữu ích cho cặp key/value và kết quả cố định.
""",
)

# ── unions-narrowing ────────────────────────────────────────────────────────
write_lesson(
    MOD, "unions-narrowing",
    "Unions & Narrowing: Modeling Reality",
    "Union types for either/or data, discriminated unions with a kind tag, exhaustiveness with never, and runtime type guards.",
    15,
    """
Real data is often "one of several shapes". Unions model that honestly; the
compiler then forces you to handle every case.

## Narrowing

TypeScript follows your runtime checks:

~~~ts
function format(value: string | number) {
  if (typeof value === "string") return value.trim(); // here: string
  return value.toFixed(2);                            // here: number
}
~~~

`typeof`, `instanceof`, `in`, and truthiness all narrow — no casts needed when
the check is real.

## Discriminated unions

Give each variant a literal tag and every switch becomes checked:

~~~ts
type Request =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "success"; data: string[] }
  | { kind: "error"; message: string };

function render(r: Request) {
  switch (r.kind) {
    case "idle": return "Nothing yet";
    case "loading": return "Loading…";
    case "success": return r.data.join(", ");  // r.data exists ONLY here
    case "error": return r.message;
    default: { const _never: never = r; return ""; }
  }
}
~~~

The `default` trick: assigning to `never` fails to compile the moment someone
adds a variant without handling it — exhaustiveness enforced by the type
system.

## Type guards

A predicate function narrows wherever it is used:

~~~ts
function isUser(v: unknown): v is User {
  return typeof v === "object" && v !== null && "id" in v && "email" in v;
}
~~~

That `v is User` return type is the contract between runtime checking and
compile-time knowledge — the heart of the boundary practice below.
""",
    "Union & Narrowing: Mô Hình hóa Thực Tế",
    "Union type cho dữ liệu hoặc-như-vậy, discriminated union với thẻ kind, kiểm tra đầy đủ với never, và type guard lúc runtime.",
    """
Dữ liệu thật thường là "một trong vài hình dạng". Union mô hình hóa điều đó
một cách trung thực; rồi compiler buộc bạn phải xử lý mọi trường hợp.

## Narrowing

TypeScript đi theo các kiểm tra runtime của bạn:

~~~ts
function format(value: string | number) {
  if (typeof value === "string") return value.trim(); // tại đây: string
  return value.toFixed(2);                            // tại đây: number
}
~~~

`typeof`, `instanceof`, `in`, và độ chân thực đều thu hẹp kiểu — không cần cast
khi phép kiểm tra là thật.

## Discriminated union

Gắn cho mỗi biến thể một thẻ literal và mọi switch đều được kiểm tra:

~~~ts
type Request =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "success"; data: string[] }
  | { kind: "error"; message: string };

function render(r: Request) {
  switch (r.kind) {
    case "idle": return "Nothing yet";
    case "loading": return "Loading…";
    case "success": return r.data.join(", ");  // r.data CHỈ tồn tại ở đây
    case "error": return r.message;
    default: { const _never: never = r; return ""; }
  }
}
~~~

Mẹo `default`: gán vào `never` sẽ không biên dịch được ngay khi ai đó thêm một
biến thể mà chưa xử lý — tính đầy đủ được hệ kiểu bảo đảm.

## Type guard

Một hàm vị từ thu hẹp kiểu ở mọi nơi nó được dùng:

~~~ts
function isUser(v: unknown): v is User {
  return typeof v === "object" && v !== null && "id" in v && "email" in v;
}
~~~

Kiểu trả về `v is User` chính là hợp đồng giữa kiểm tra runtime và hiểu biết
compile-time — trái tim của bài luyện về biên giới bên dưới.
""",
)

# ── generics ────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "generics",
    "Generics: Reuse With Type Safety",
    "Type parameters, inference at call sites, constraints with extends, and utility types you will actually use.",
    15,
    """
Generics are functions for types: one implementation, types vary per use,
and the compiler tracks each use separately.

## The idea

~~~ts
function first<T>(items: T[]): T | undefined {
  return items[0];
}
const a = first(["x", "y"]);   // T inferred as string → a: string | undefined
const b = first([1, 2]);       // T inferred as number → b: number | undefined
~~~

Call-site inference means you rarely write the angle brackets — you get them
from context.

## Constraints

When the body needs capabilities beyond `unknown`, constrain:

~~~ts
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map((i) => i[key]);
}
pluck(users, "email"); // ✓ — and "emial" is a compile error
~~~

`K extends keyof T` ties the key to keys that actually exist on T — a typo
becomes a compile-time error instead of `undefined` at runtime.

## Utility types

The built-ins cover 90% of needs:

- `Partial<T>` — all fields optional (patch/update payloads)
- `Pick<T, K>` / `Omit<T, K>` — select or remove fields (public view of a row)
- `ReturnType<typeof fn>` — capture what a function gives back
- `Record<K, V>` — typed dictionaries

~~~ts
type PublicUser = Omit<User, "passwordHash">;
function updateUser(id: number, patch: Partial<User>) { ... }
~~~

Use generics when the SHAPE relationship matters (in → out); use `unknown`
when you truly accept anything.
""",
    "Generics: Tái Sử Dụng Có An Toàn Kiểu",
    "Tham số kiểu, suy diễn tại chỗ gọi, ràng buộc với extends, và các utility type bạn sẽ thực sự dùng.",
    """
Generics là hàm dành cho kiểu: một cài đặt, kiểu thay đổi theo từng cách dùng,
và compiler theo dõi từng cách dùng một cách riêng biệt.

## Ý tưởng

~~~ts
function first<T>(items: T[]): T | undefined {
  return items[0];
}
const a = first(["x", "y"]);   // T tự suy là string → a: string | undefined
const b = first([1, 2]);       // T tự suy là number → b: number | undefined
~~~

Suy diễn tại chỗ gọi nghĩa là bạn hiếm khi phải viết dấu ngoặc nhọn — chúng đến
từ ngữ cảnh.

## Ràng buộc

Khi thân hàm cần khả năng vượt ngoài `unknown`, hãy ràng buộc:

~~~ts
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map((i) => i[key]);
}
pluck(users, "email"); // ✓ — và "emial" là lỗi compile
~~~

`K extends keyof T` buộc key phải là key thật sự tồn tại trên T — một lỗi gõ
trở thành lỗi compile thay vì `undefined` lúc runtime.

## Utility types

Các công cụ có sẵn phủ 90% nhu cầu:

- `Partial<T>` — mọi trường thành optional (payload cập nhật)
- `Pick<T, K>` / `Omit<T, K>` — chọn hoặc loại trường (bản công khai của một dòng)
- `ReturnType<typeof fn>` — bắt lấy những gì hàm trả về
- `Record<K, V>` — dictionary có kiểu

~~~ts
type PublicUser = Omit<User, "passwordHash">;
function updateUser(id: number, patch: Partial<User>) { ... }
~~~

Dùng generics khi MỐI QUAN HỆ hình dạng quan trọng (vào → ra); dùng `unknown`
khi bạn thật sự chấp nhận mọi thứ.
""",
)

# ── unknown-never ───────────────────────────────────────────────────────────
write_lesson(
    MOD, "unknown-never",
    "unknown, never, and Honest Boundaries",
    "any vs unknown, narrowing unknown safely, never for impossible states, and where each belongs in a codebase.",
    12,
    """
## any: the off switch

`any` opts out of checking — assignable to and from everything. It silences the
error today and reintroduces the runtime crash tomorrow. Every `any` in a
codebase is a hole in the contract.

## unknown: the honest version

`unknown` accepts anything too — but you must narrow before use:

~~~ts
function parse(input: unknown) {
  // input.foo            ✗ — unknown is not usable yet
  if (typeof input === "string") return input.trim();   // ✓ narrowed
  if (isUser(input)) return renderUser(input);          // ✓ guard
  throw new Error("Unexpected payload");
}
~~~

Rule of thumb: `unknown` for anything that crosses a boundary you do not
control — network responses, JSON.parse, localStorage, third-party callbacks.

## never: the impossible type

`never` is the type of values that cannot exist: a function that always throws,
or the exhaustiveness check from the unions lesson. When the compiler computes
"there are no remaining cases", the result is `never` — assigning it forces the
check.

## Where each belongs

- Parameters you truly accept anything: `unknown` + narrow.
- Values you construct that are impossible: design them away, or `never`.
- `any`: only in genuinely untyped legacy seams, with a comment and a plan.
""",
    "unknown, never, và Biên Giới Trung Thực",
    "any so với unknown, thu hẹp unknown một cách an toàn, never cho trạng thái không thể, và vị trí của từng loại trong codebase.",
    """
## any: công tắc ngắt

`any` từ chối kiểm tra — gán được với mọi thứ và mọi thứ gán được vào nó. Nó
làm tắt lỗi hôm nay và tái xuất crash runtime ngày mai. Mỗi `any` trong codebase
là một lỗ hổng trong hợp đồng.

## unknown: phiên bản trung thực

`unknown` cũng nhận mọi thứ — nhưng bạn phải thu hẹp trước khi dùng:

~~~ts
function parse(input: unknown) {
  // input.foo            ✗ — unknown chưa dùng được
  if (typeof input === "string") return input.trim();   // ✓ đã thu hẹp
  if (isUser(input)) return renderUser(input);          // ✓ guard
  throw new Error("Unexpected payload");
}
~~~

Nguyên tắc: `unknown` cho bất cứ thứ gì vượt qua biên giới bạn không kiểm soát
— phản hồi mạng, JSON.parse, localStorage, callback của bên thứ ba.

## never: kiểu không thể

`never` là kiểu của những giá trị không thể tồn tại: hàm luôn luôn throw, hoặc
phép kiểm tra đầy đủ trong bài union. Khi compiler tính ra "không còn trường
hợp nào", kết quả là `never` — việc gán nó ép phép kiểm tra xảy ra.

## Mỗi loại thuộc về đâu

- Tham số mà bạn thật sự nhận mọi thứ: `unknown` + thu hẹp.
- Giá trị bạn dựng mà không thể xảy ra: thiết kế lại cho hết chuyện đó, hoặc `never`.
- `any`: chỉ ở những điểm nối legacy chưa có kiểu, kèm chú thích và kế hoạch bỏ nó.
""",
)

# ── typing-apis-dom ─────────────────────────────────────────────────────────
write_lesson(
    MOD, "typing-apis-dom",
    "Typing APIs & the DOM",
    "Response DTOs, validating before trusting, discriminated fetch results, and typed DOM access patterns.",
    14,
    """
Types are most valuable exactly where data arrives from the outside.

## DTOs at the edge

Model the server's response as a type, then VALIDATE before trusting it —
types are compile-time only; the network does not read them:

~~~ts
type TaskDTO = { id: string; title: string; done: boolean };

function isTask(v: unknown): v is TaskDTO {
  return (
    typeof v === "object" && v !== null &&
    typeof (v as any).id === "string" &&
    typeof (v as any).title === "string" &&
    typeof (v as any).done === "boolean"
  );
}
~~~

A runtime guard + compile-time type is the standard pairing: the guard protects
runtime, the type documents and checks the rest of the program.

## Discriminated fetch results

Combine with the unions lesson — an API client that cannot lie:

~~~ts
type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; status: number };

async function getJSON<T>(url: string): Promise<ApiResult<T>> { ... }
~~~

Callers MUST check `ok` before touching `data` — the loading/error UI contract
from Module 3, now enforced by the compiler.

## DOM access is also a boundary

`document.querySelector` returns `Element | null`. Narrow honestly:

~~~ts
const btn = document.querySelector<HTMLButtonElement>("#submit");
if (!btn) throw new Error("#submit missing");   // or return early
btn.disabled = true;                             // HTMLButtonElement members
~~~

The generic parameter is a claim you are making about the selector — keep the
null check; the type does not make the element exist.
""",
    "Gán Kiểu cho API & DOM",
    "Response DTO, kiểm tra trước khi tin, kết quả fetch dạng discriminated union, và các mẫu truy cập DOM có kiểu.",
    """
Types có giá trị nhất đúng ở nơi dữ liệu đi vào từ bên ngoài.

## DTO ở rìa hệ thống

Mô hình hóa phản hồi của server thành một kiểu, rồi KIỂM TRA trước khi tin —
types chỉ tồn tại lúc compile; mạng không đọc chúng:

~~~ts
type TaskDTO = { id: string; title: string; done: boolean };

function isTask(v: unknown): v is TaskDTO {
  return (
    typeof v === "object" && v !== null &&
    typeof (v as any).id === "string" &&
    typeof (v as any).title === "string" &&
    typeof (v as any).done === "boolean"
  );
}
~~~

Cặp chuẩn là runtime guard + compile-time type: guard bảo vệ runtime, type tài
liệu hóa và kiểm tra phần còn lại của chương trình.

## Kết quả fetch dạng discriminated

Kết hợp với bài union — một API client không thể nói dối:

~~~ts
type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; status: number };

async function getJSON<T>(url: string): Promise<ApiResult<T>> { ... }
~~~

Chỗ gọi BẮT BUỘC kiểm tra `ok` trước khi đụng vào `data` — hợp đồng
loading/error của Module 3, giờ được compiler bảo đảm.

## Truy cập DOM cũng là biên giới

`document.querySelector` trả về `Element | null`. Thu hẹp một cách trung thực:

~~~ts
const btn = document.querySelector<HTMLButtonElement>("#submit");
if (!btn) throw new Error("#submit missing");   // hoặc return sớm
btn.disabled = true;                             // thành viên của HTMLButtonElement
~~~

Tham số generic là lời khẳng định bạn đưa ra về selector — vẫn phải giữ null
check; kiểu không làm phần tử tồn tại.
""",
)

# ── checkpoint ──────────────────────────────────────────────────────────────
write_checkpoint(
    MOD,
    "type-safe-checkpoint",
    "Checkpoint: Type-Safe Client Logic",
    "Prove the typing mindset in runnable logic: runtime validators, a discriminated result pipeline, and generic narrowing helpers.",
    20,
    """
The sandbox runs JavaScript, so this checkpoint verifies the RUNTIME halves of
the module's patterns — the exact guards and shapes your TypeScript types will
describe. If the logic is right, the types write themselves.

1. `isUser(v)` — a validator returning true only for well-formed user objects.
2. `parseWith(v, validator, fallback)` — validate-or-fallback wrapper.
3. `apiGet(kind)` — a fake client returning discriminated results and a
   handler that must check `ok` before touching data.
""",
    "Kiểm tra kiến thức: Logic Client An Toàn Kiểu",
    "Chứng minh tư duy gán kiểu bằng logic chạy được: validator runtime, pipeline kết quả dạng discriminated, và hàm thu hẹp kiểu dạng generic.",
    """
Sandbox chạy JavaScript, nên bài kiểm tra này xác minh phần RUNTIME của các
mẫu trong module — chính là các guard và hình dạng mà type TypeScript của bạn
sẽ mô tả. Logic đúng thì type tự viết được.

1. `isUser(v)` — một validator chỉ trả true với object user hợp chuẩn.
2. `parseWith(v, validator, fallback)` — wrapper validate-hoặc-fallback.
3. `apiGet(kind)` — một client giả trả kết quả discriminated và một handler
   bắt buộc kiểm tra `ok` trước khi đụng vào data.
""",
    {
        "id": "i2-ts-checkpoint",
        "title": "Type-Safe Client Logic Check",
        "prompt": "Implement three typing-discipline helpers:\n\n1. `isUser(v)` — RETURN true only when `v` is an object (not null, not array) with a string `id`, string `email` containing \"@\", and optional string `name` (absent or string).\n2. `parseWith(v, validator, fallback)` — RETURN `{ ok: true, value }` when `validator(v)` is true, else `{ ok: false, fallback }`.\n3. `handleApi(result)` — `result` is `{ ok: true, data }` or `{ ok: false, status }`. RETURN the data string when ok, else `\"HTTP \" + status`. It must never read `.data` on a failure object.",
        "difficulty": "intermediate",
        "boilerplate": "// 1) isUser(v)\n\n// 2) parseWith(v, validator, fallback)\n\n// 3) handleApi(result)\n",
        "tests": [
            {
                "name": "isUser accepts only well-formed users",
                "code": fn_wrap("isUser, parseWith, handleApi", "isUser, parseWith, handleApi") + "\nif (isUser({ id: \"u1\", email: \"a@b.co\" }) !== true) throw new Error(\"Minimal valid user accepted.\");\nif (isUser({ id: \"u1\", email: \"a@b.co\", name: \"Ada\" }) !== true) throw new Error(\"Optional name present is fine.\");\nif (isUser({ id: 7, email: \"a@b.co\" }) !== false) throw new Error(\"Numeric id must fail.\");\nif (isUser({ id: \"u1\", email: \"nope\" }) !== false) throw new Error(\"Email without @ must fail.\");\nif (isUser([\"u1\", \"a@b.co\"]) !== false) throw new Error(\"Arrays are not users.\");\nif (isUser(null) !== false) throw new Error(\"null is not a user.\");",
                "hint": "Check typeof v === 'object' && v !== null && !Array.isArray(v), then each field's typeof; email must include '@'.",
            },
            {
                "name": "parseWith validates or falls back",
                "code": fn_wrap("isUser, parseWith, handleApi", "isUser, parseWith, handleApi") + "\nconst good = parseWith({ id: \"u1\", email: \"a@b.co\" }, isUser, null);\nif (good.ok !== true || good.value.email !== \"a@b.co\") throw new Error(\"Valid input flows through as { ok: true, value }.\");\nconst bad = parseWith(\"junk\", isUser, \"default\");\nif (bad.ok !== false || bad.fallback !== \"default\") throw new Error(\"Invalid input returns { ok: false, fallback }.\");",
                "hint": "validator(v) ? { ok: true, value: v } : { ok: false, fallback }.",
            },
            {
                "name": "handleApi checks ok before data",
                "code": fn_wrap("isUser, parseWith, handleApi", "isUser, parseWith, handleApi") + "\nif (handleApi({ ok: true, data: \"tasks\" }) !== \"tasks\") throw new Error(\"Success returns the data.\");\nif (handleApi({ ok: false, status: 503 }) !== \"HTTP 503\") throw new Error(\"Failure returns 'HTTP ' + status.\");",
                "hint": "result.ok ? result.data : \"HTTP \" + result.status.",
            },
        ],
    },
    {
        "title": "Kiểm tra kiến thức: Logic Client An Toàn Kiểu",
        "prompt": "Cài đặt ba hàm kỷ luật kiểu:\n\n1. `isUser(v)` — RETURN true CHỈ khi `v` là object (không phải null, không phải mảng) với `id` là chuỗi, `email` là chuỗi chứa \"@\", và `name` tùy chọn (vắng mặt hoặc là chuỗi).\n2. `parseWith(v, validator, fallback)` — RETURN `{ ok: true, value }` khi `validator(v)` đúng, nếu không `{ ok: false, fallback }`.\n3. `handleApi(result)` — `result` là `{ ok: true, data }` hoặc `{ ok: false, status }`. RETURN chuỗi data khi ok, nếu không `\"HTTP \" + status`. Không bao giờ được đọc `.data` trên object thất bại.",
        "tests": [
            {"name": "isUser chỉ chấp nhận user hợp chuẩn", "hint": "Kiểm tra typeof v === 'object' && v !== null && !Array.isArray(v), rồi typeof từng trường; email phải chứa '@'."},
            {"name": "parseWith kiểm tra hoặc rơi về fallback", "hint": "validator(v) ? { ok: true, value: v } : { ok: false, fallback }."},
            {"name": "handleApi kiểm tra ok trước khi đụng vào data", "hint": "result.ok ? result.data : \"HTTP \" + result.status."},
        ],
    },
)

print("Module 5 lessons + checkpoint written.")
