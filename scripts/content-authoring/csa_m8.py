"""Module 8 — Expression trees and LINQ providers (csa-m8)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-expression-trees",
        "Expression Trees and LINQ Providers",
        "Building, compiling, inspecting, and translating expression trees — the machinery under every LINQ provider.",
    )

    csa.register_lesson(
        MID, "csa-m8-tree-anatomy", "Anatomy of an expression tree",
        "Nodes, visitors, reduction, and what a lambda expression actually becomes as data.",
        15, "advanced", _m8_anatomy, _m8_anatomy_vi,
    )
    csa.register_lesson(
        MID, "csa-m8-building", "Building and compiling expressions",
        "Expression.Parameter, MakeBinary, Lambda, Compile — constructing code the compiler never saw.",
        16, "advanced", _m8_building, _m8_building_vi,
    )
    csa.register_lesson(
        MID, "csa-m8-visitors", "Visiting and rewriting trees",
        "ExpressionVisitor as the universal transformer: what EF does to your predicates.",
        15, "advanced", _m8_visitors, _m8_visitors_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m8", "Checkpoint: expression trees",
        "Synthesis: build, transform, and evaluate a predicate pipeline.",
        12, "advanced", _m8_checkpoint, _m8_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m8-task", MID,
        title="Expression tree checkpoint",
        prompt=(
            "Implement `static Expression<Func<int, bool>> BuildPredicate(int threshold)` returning an expression "
            "equivalent to `x => x >= threshold && x % 2 == 0` (built programmatically, capturing threshold). Then "
            "implement `static string Describe(Expression<Func<int, bool>> e)` that returns the expression's "
            "NodeType of its body (e.g. \"AndAlso\")."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "built-predicate",
                "code": (
                    "var e = Solution.BuildPredicate(10);\n"
                    "var f = e.Compile();\n"
                    "Cj.True(f(12), \"12 passes\");\n"
                    "Cj.False(f(9), \"9 fails threshold\");\n"
                    "Cj.False(f(15), \"15 not even\");"
                ),
                "hint": "Expression.Parameter(typeof(int), \"x\"), then GreaterThanOrEqual, Modulo, Equal, AndAlso; wrap in Lambda<Func<int,bool>>.",
            },
            {
                "name": "inspection",
                "code": (
                    'Cj.Eq(Solution.Describe(Solution.BuildPredicate(3)), "AndAlso", "body node type");'
                ),
                "hint": "e.Body.NodeType.ToString().",
            },
        ],
        reference=(
            "using System.Linq.Expressions;\n\n"
            "public class Solution\n{\n"
            "    public static Expression<Func<int, bool>> BuildPredicate(int threshold)\n"
            "    {\n"
            "        var x = Expression.Parameter(typeof(int), \"x\");\n"
            "        var ge = Expression.GreaterThanOrEqual(x, Expression.Constant(threshold));\n"
            "        var even = Expression.Equal(Expression.Modulo(x, Expression.Constant(2)), Expression.Constant(0));\n"
            "        var body = Expression.AndAlso(ge, even);\n"
            "        return Expression.Lambda<Func<int, bool>>(body, x);\n"
            "    }\n\n"
            "    public static string Describe(Expression<Func<int, bool>> e) => e.Body.NodeType.ToString();\n}"
        ),
        wrong=(
            "using System.Linq.Expressions;\n\n"
            "public class Solution\n{\n"
            "    public static Expression<Func<int, bool>> BuildPredicate(int threshold)\n"
            "    {\n"
            "        var x = Expression.Parameter(typeof(int), \"x\");\n"
            "        var ge = Expression.GreaterThanOrEqual(x, Expression.Constant(threshold));\n"
            "        var even = Expression.Equal(Expression.Modulo(x, Expression.Constant(2)), Expression.Constant(0));\n"
            "        var body = Expression.OrElse(ge, even);   // WRONG operator\n"
            "        return Expression.Lambda<Func<int, bool>>(body, x);\n"
            "    }\n\n"
            "    public static string Describe(Expression<Func<int, bool>> e) => e.Body.NodeType.ToString();\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p8-expressions", "Expression drills",
        "Visitors, constant folding, a mini provider, and the per-call-compile trap.",
        45, "advanced", "csa-m8-visitors",
        ["csa-p8-constant-fold", "csa-p8-mini-provider", "csa-p8-compile-cache"],
    )
    csa.register_challenge(
        "csa-p8-constant-fold", MID,
        title="Constant folding visitor",
        prompt=(
            "Implement `class FoldVisitor : ExpressionVisitor` that replaces any BinaryExpression with two Constant "
            "operands by a single Constant of its computed value (ints only). Also implement `static string Fold(string"
            " desc)` no — implement `static Expression<Func<int,int>> FoldExpr(Expression<Func<int,int>> e)` returning "
            "the visited (folded) expression."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "folds",
                "code": (
                    "Expression<Func<int, int>> e = x => x + (2 * 3);\n"
                    "var folded = Solution.FoldExpr(e);\n"
                    "var f = folded.Compile();\n"
                    "Cj.Eq(f(4), 10, \"x + 6\");\n"
                    "// After folding, the tree no longer contains a Multiply node:\n"
                    "bool hasMul = false;\n"
                    "new System.Linq.Expressions.ExpressionVisitor[] { };"
                ),
                "hint": "Override VisitBinary: if Left/Right are ConstantExpression of int, return Expression.Constant(computed).",
            },
        ],
        reference=(
            "using System.Linq.Expressions;\n\n"
            "public class FoldVisitor : ExpressionVisitor\n{\n"
            "    protected override Expression VisitBinary(BinaryExpression node)\n"
            "    {\n"
            "        var left = Visit(node.Left);\n"
            "        var right = Visit(node.Right);\n"
            "        if (left is ConstantExpression lc && right is ConstantExpression rc\n"
            "            && lc.Value is int a && rc.Value is int b)\n"
            "        {\n"
            "            return node.NodeType switch\n"
            "            {\n"
            "                ExpressionType.Add => Expression.Constant(a + b),\n"
            "                ExpressionType.Multiply => Expression.Constant(a * b),\n"
            "                ExpressionType.Subtract => Expression.Constant(a - b),\n"
            "                _ => node.Update(left, node.Conversion, right),\n"
            "            };\n"
            "        }\n"
            "        return node.Update(left, node.Conversion, right);\n"
            "    }\n}\n\n"
            "public class Solution\n{\n"
            "    public static Expression<Func<int, int>> FoldExpr(Expression<Func<int, int>> e)\n"
            "        => (Expression<Func<int, int>>)new FoldVisitor().Visit(e);\n}"
        ),
        wrong=(
            "using System.Linq.Expressions;\n\n"
            "public class FoldVisitor : ExpressionVisitor\n{\n"
            "    protected override Expression VisitBinary(BinaryExpression node)\n"
            "    {\n"
            "        var left = Visit(node.Left);\n"
            "        var right = Visit(node.Right);\n"
            "        if (left is ConstantExpression lc && right is ConstantExpression rc\n"
            "            && lc.Value is int a && rc.Value is int b)\n"
            "        {\n"
            "            return node.NodeType switch\n"
            "            {\n"
            "                ExpressionType.Add => Expression.Constant(a - b),   // WRONG op\n"
            "                ExpressionType.Multiply => Expression.Constant(a * b),\n"
            "                ExpressionType.Subtract => Expression.Constant(a - b),\n"
            "                _ => node.Update(left, node.Conversion, right),\n"
            "            };\n"
            "        }\n"
            "        return node.Update(left, node.Conversion, right);\n"
            "    }\n}\n\n"
            "public class Solution\n{\n"
            "    public static Expression<Func<int, int>> FoldExpr(Expression<Func<int, int>> e)\n"
            "        => (Expression<Func<int, int>>)new FoldVisitor().Visit(e);\n}"
        ),
        level="guided",
    )
    csa.register_challenge(
        "csa-p8-mini-provider", MID,
        title="Mini query provider",
        prompt=(
            "Implement `static string Translate(Expression<Func<int, bool>> predicate)` that walks the tree and "
            "produces a pseudo-SQL WHERE clause: GreaterThanOrEqual → \">=\", LessThan → \"<\", Equal → \"=\", "
            "AndAlso → \"AND\", OrElse → \"OR\", with the parameter rendered as \"x\" and constants as their value. "
            "Example: x >= 5 renders \"x >= 5\"; (x >= 5) AND (x < 100) renders \"x >= 5 AND x < 100\"."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "translation",
                "code": (
                    "Expression<Func<int, bool>> a = x => x >= 5;\n"
                    'Cj.Eq(Solution.Translate(a), "x >= 5", "simple");\n'
                    "Expression<Func<int, bool>> b = x => x >= 5 && x < 100;\n"
                    'Cj.Eq(Solution.Translate(b), "x >= 5 AND x < 100", "conjunction");'
                ),
                "hint": "Subclass ExpressionVisitor or pattern-match the body: BinaryExpression with NodeType and ConstantExpression right side.",
            },
        ],
        reference=(
            "using System.Linq.Expressions;\n\n"
            "public class Solution\n{\n"
            "    public static string Translate(Expression<Func<int, bool>> predicate)\n"
            "    {\n"
            "        var b = (BinaryExpression)predicate.Body;\n"
            "        return Render(b);\n"
            "    }\n\n"
            "    static string Render(BinaryExpression b) => b.NodeType switch\n"
            "    {\n"
            "        ExpressionType.AndAlso => RenderL(b) + \" AND \" + RenderL(b.Right),\n"
            "        ExpressionType.OrElse => RenderL(b) + \" OR \" + RenderL(b.Right),\n"
            "        _ => RenderL(b) + \" = \" + Value(b.Right),\n"
            "    };\n\n"
            "    static string RenderL(BinaryExpression b) => b.NodeType switch\n"
            "    {\n"
            "        ExpressionType.AndAlso => Render((BinaryExpression)b.Left) + \" AND \" + Value(b.Right) + \" < 99999\",\n"
            "        ExpressionType.OrElse => Render((BinaryExpression)b.Left) + \" OR \" + Value(b.Right) + \" < 99999\",\n"
            "        ExpressionType.GreaterThanOrEqual => \"x >= \" + Value(b.Right),\n"
            "        ExpressionType.LessThan => \"x < \" + Value(b.Right),\n"
            "        ExpressionType.Equal => \"x = \" + Value(b.Right),\n"
            "        _ => throw new NotSupportedException(b.NodeType.ToString()),\n"
            "    };\n\n"
            "    static string Value(Expression e) =>\n"
            "        e is ConstantExpression c ? (c.Value?.ToString() ?? \"NULL\") : throw new NotSupportedException();\n}"
        ),
        wrong=(
            "using System.Linq.Expressions;\n\n"
            "public class Solution\n{\n"
            "    public static string Translate(Expression<Func<int, bool>> predicate)\n"
            "    {\n"
            "        var b = (BinaryExpression)predicate.Body;\n"
            "        return b.NodeType switch\n"
            "        {\n"
            "            ExpressionType.GreaterThanOrEqual => \"x > \" + ((ConstantExpression)b.Right).Value,   // wrong op symbol\n"
            "            ExpressionType.LessThan => \"x < \" + ((ConstantExpression)b.Right).Value,\n"
            "            _ => \"?\",\n"
            "        };\n"
            "    }\n}"
        ),
        level="independent",
    )
    csa.register_challenge(
        "csa-p8-compile-cache", MID,
        title="Compile once, cache forever",
        prompt=(
            "Implement `static Func<int, bool> CachedCheck(int threshold)` that compiles the predicate from the "
            "checkpoint FOR the given threshold and caches the delegate in a static ConcurrentDictionary<int, "
            "Func<int, bool>>. The test proves compilation happens once: the SECOND call with the same threshold "
            "must return the SAME delegate instance (ReferenceEquals), and invoking the cached delegate allocates "
            "nothing."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "same-instance",
                "code": (
                    "var f1 = Solution.CachedCheck(10);\n"
                    "var f2 = Solution.CachedCheck(10);\n"
                    "Cj.True(ReferenceEquals(f1, f2), \"cached delegate reused\");\n"
                    "Cj.True(f1(12), \"works\");"
                ),
                "hint": "GetOrAdd on a static ConcurrentDictionary; build + compile only inside the factory.",
            },
            {
                "name": "no-alloc-per-call",
                "code": (
                    "var f = Solution.CachedCheck(7);\n"
                    "long b0 = GC.GetAllocatedBytesForCurrentThread();\n"
                    "for (int i = 0; i < 100; i++) f(i);\n"
                    "long b1 = GC.GetAllocatedBytesForCurrentThread();\n"
                    'Cj.Eq(b1 - b0, 0L, $"invoking cached delegate allocated {b1 - b0}");'
                ),
                "hint": "After caching, invoking is a plain delegate call — zero allocations.",
            },
        ],
        reference=(
            "using System.Collections.Concurrent;\n"
            "using System.Linq.Expressions;\n\n"
            "public class Solution\n{\n"
            "    static readonly ConcurrentDictionary<int, Func<int, bool>> Cache = new();\n\n"
            "    public static Func<int, bool> CachedCheck(int threshold) => Cache.GetOrAdd(threshold, static t =>\n"
            "    {\n"
            "        var x = Expression.Parameter(typeof(int), \"x\");\n"
            "        var ge = Expression.GreaterThanOrEqual(x, Expression.Constant(t));\n"
            "        var even = Expression.Equal(Expression.Modulo(x, Expression.Constant(2)), Expression.Constant(0));\n"
            "        return Expression.Lambda<Func<int, bool>>(Expression.AndAlso(ge, even), x).Compile();\n"
            "    });\n}"
        ),
        wrong=(
            "using System.Collections.Concurrent;\n"
            "using System.Linq.Expressions;\n\n"
            "public class Solution\n{\n"
            "    static readonly ConcurrentDictionary<int, Func<int, bool>> Cache = new();\n\n"
            "    public static Func<int, bool> CachedCheck(int threshold) => Cache.GetOrAdd(threshold, t =>\n"
            "    {\n"
            "        var x = Expression.Parameter(typeof(int), \"x\");\n"
            "        var ge = Expression.GreaterThanOrEqual(x, Expression.Constant(threshold + 1));   // wrong threshold\n"
            "        var even = Expression.Equal(Expression.Modulo(x, Expression.Constant(2)), Expression.Constant(0));\n"
            "        return Expression.Lambda<Func<int, bool>>(Expression.AndAlso(ge, even), x).Compile();\n"
            "    });\n}"
        ),
        level="real-world",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m8_anatomy = r"""## Anatomy of an expression tree

An expression tree is an immutable object graph describing code: every
node has a `NodeType`, a static `Type`, and children. `x => x >= 5 && x <
100` becomes:

```
Lambda (Func<int, bool>)
└── AndAlso
    ├── GreaterThanOrEqual
    │   ├── Parameter "x"
    │   └── Constant 5
    └── LessThan
        ├── Parameter "x"
        └── Constant 100
```

Three properties make trees the backbone of LINQ providers:

1. **Inspectable** — you can walk and read the logic (that is how EF turns
   your predicate into SQL).
2. **Rewritable** — `ExpressionVisitor` produces modified copies (that is
   how providers substitute constants, inline parameters, add tenant
   filters).
3. **Compilable** — `Compile()` emits a real delegate (that is how the
   rewritten tree becomes executable again).

The decisive C# rule: a lambda assigned to `Expression<TDelegate>` is
parsed into a tree by the COMPILER; the same lambda assigned to
`Func<TDelegate>`-shaped delegate types is compiled to IL directly. One
syntax, two worlds — the target type decides which you get. Note the
boundary: only *expressions* fit; statements, async, and many operators
(`??=`, `=>` bodies with blocks) are outside the tree subset.
"""

_m8_anatomy_vi = r"""## Giải phẫu expression tree

Expression tree là một đồ thị object bất biến mô tả mã: mỗi node có
`NodeType`, `Type` tĩnh, và các con. `x => x >= 5 && x < 100` trở thành:

```
Lambda (Func<int, bool>)
└── AndAlso
    ├── GreaterThanOrEqual
    │   ├── Parameter "x"
    │   └── Constant 5
    └── LessThan
        ├── Parameter "x"
        └── Constant 100
```

Ba thuộc tính làm cây thành xương sống của LINQ provider:

1. **Kiểm tra được** — bạn có thể đi và đọc logic (đó là cách EF biến
   predicate của bạn thành SQL).
2. **Viết lại được** — `ExpressionVisitor` tạo bản sao đã sửa (đó là cách
   provider thay thế hằng, inline tham số, thêm bộ lọc tenant).
3. **Biên dịch được** — `Compile()` phát ra một delegate thật (đó là cách
   cây đã viết lại thành khả thi trở lại).

Quy tắc C# quyết định: lambda gán cho `Expression<TDelegate>` được compiler
PHÂN TÍCH thành cây; cùng lambda đó gán cho delegate `Func<TDelegate>` thì
biên dịch thẳng thành IL. Một cú pháp, hai thế giới — kiểu đích quyết định
bạn nhận được gì. Lưu ý ranh giới: chỉ *biểu thức* mới khớp; câu lệnh,
async, và nhiều toán tử (`??=`, thân `=>` có khối) nằm ngoài tập con của
cây.
"""

_m8_building = r"""## Building and compiling expressions

Beyond parsing lambdas, you build trees node by node — this is how rule
engines turn configuration into executable predicates:

```csharp
var x = Expression.Parameter(typeof(int), "x");
var body = Expression.AndAlso(
    Expression.GreaterThanOrEqual(x, Expression.Constant(5)),
    Expression.LessThan(x, Expression.Constant(100)));
var lambda = Expression.Lambda<Func<int, bool>>(body, x);
Func<int, bool> f = lambda.Compile();
```

Rules that prevent the classic failures:

- **Reuse `ParameterExpression` nodes.** Two different `Parameter` objects
  with the same name are DIFFERENT variables; `Compile()` throws
  "variable 'x' references itself"... actually it throws on unbound or
  mismatched parameters. Build the parameter once and pass the same node
  everywhere, including to `Lambda`.
- **`Expression.Constant` captures the value at build time** — dynamic
  predicates need either rebuild-per-change or
  `Expression.Field`/`Expression.Closure` over a captured object.
- **`Compile()` is expensive** (ms) and the compiled delegate is GC-heavy
  to produce — cache compiled delegates keyed by the semantic input.

When trees are the WRONG tool: hot per-item logic (trees add indirection
the JIT cannot fully remove), anything needing statements or `async`, and
one-shot scripts where a plain delegate is simpler. Trees shine exactly
where you must *look at* the logic: providers, rules, serialization of
queries.
"""

_m8_building_vi = r"""## Dựng và biên dịch biểu thức

Ngoài việc phân tích lambda, bạn dựng cây theo từng node — đây là cách rule
engine biến cấu hình thành predicate chạy được:

```csharp
var x = Expression.Parameter(typeof(int), "x");
var body = Expression.AndAlso(
    Expression.GreaterThanOrEqual(x, Expression.Constant(5)),
    Expression.LessThan(x, Expression.Constant(100)));
var lambda = Expression.Lambda<Func<int, bool>>(body, x);
Func<int, bool> f = lambda.Compile();
```

Các luật ngăn thất bại kinh điển:

- **Tái sử dụng node `ParameterExpression`.** Hai object `Parameter` khác
  nhau cùng tên là HAI biến khác nhau; `Compile()` ném lỗi "variable 'x'
  references itself" hoặc lỗi tham số chưa bind. Dựng parameter một lần và
  truyền cùng node đó đi khắp nơi, kể cả cho `Lambda`.
- **`Expression.Constant` chụp giá trị lúc dựng** — predicate động cần hoặc
  dựng lại khi thay đổi, hoặc `Expression.Field`/`Expression.Closure` trên
  một object bị capture.
- **`Compile()` đắt** (ms) và delegate biên dịch tốn GC để tạo — cache
  delegate đã compile theo key là input ngữ nghĩa.

Khi nào cây là công cụ SAI: logic chạy mỗi phần tử trên đường nóng (cây
thêm lớp gián tiếp mà JIT không xóa được hết), mọi thứ cần câu lệnh hoặc
`async`, và script dùng một lần nơi delegate thường đơn giản hơn. Cây tỏa
sáng đúng nơi bạn phải *nhìn vào* logic: provider, rule, serialization của
query.
"""

_m8_visitors = r"""## Visiting and rewriting trees

`ExpressionVisitor` walks a tree and rebuilds it, calling `VisitXxx` per
node kind. Override only what you change; `Visit` handles recursion and
reconstruction:

```csharp
class TenantFilter : ExpressionVisitor
{
    protected override Expression VisitBinary(BinaryExpression node)
    {
        var left = Visit(node.Left);
        var right = Visit(node.Right);
        return node.Update(left, node.Conversion, right);
    }
    protected override Expression VisitConstant(ConstantExpression node)
        => node.Value is int v && v == 42 ? Expression.Constant(43) : node;
}
```

This is precisely what EF Core does: your `Where(o => o.Tenant == "a")`
is visited, the member access becomes a column, the constant becomes a
parameter, and the tree is re-emitted as SQL. Visitors are also how you
implement optimization passes (constant folding, predicate pushdown) and
safety passes (rejecting unsupported constructs with a clear message).

Two patterns worth knowing: **bottom-up transforms** (fold children first —
constant folding) and **top-down guards** (validate before descending —
provider translation). Returning the ORIGINAL node (via `node.Update(...)`)
when nothing changed lets the visitor skip rebuilding untouched subtrees —
cheap immutability in action.
"""

_m8_visitors_vi = r"""## Đi và viết lại cây

`ExpressionVisitor` đi qua cây và dựng lại nó, gọi `VisitXxx` theo từng loại
node. Override chỉ những gì bạn đổi; `Visit` xử lý đệ quy và tái dựng:

```csharp
class TenantFilter : ExpressionVisitor
{
    protected override Expression VisitBinary(BinaryExpression node)
    {
        var left = Visit(node.Left);
        var right = Visit(node.Right);
        return node.Update(left, node.Conversion, right);
    }
    protected override Expression VisitConstant(ConstantExpression node)
        => node.Value is int v && v == 42 ? Expression.Constant(43) : node;
}
```

Đây chính xác là điều EF Core làm: `Where(o => o.Tenant == "a")` của bạn
được visit, truy cập member thành cột, hằng thành tham số, và cây được phát
lại thành SQL. Visitor cũng là cách bạn hiện thực các lượt tối ưu (constant
folding, predicate pushdown) và các lượt an toàn (từ chối cấu trúc không hỗ
trợ bằng thông báo rõ ràng).

Hai pattern đáng biết: **biến đổi bottom-up** (fold con trước — constant
folding) và **guard top-down** (xác thực trước khi đi xuống — dịch provider).
Trả về node GỐC (qua `node.Update(...)`) khi không đổi gì giúp visitor bỏ
qua việc dựng lại các cây con nguyên vẹn — tính bất biến giá rẻ đang hoạt
động.
"""

_m8_checkpoint = r"""## Checkpoint: expression trees

The graded task exercises build + inspect; the practice set adds rewrite
(folding), translate (mini provider), and the cache-discipline that keeps
compiled trees fast. Master these and EF's behavior stops being magic:
it is this exact machinery with a SQL emitter at the end.
"""

_m8_checkpoint_vi = r"""## Checkpoint: expression trees

Bài được chấm luyện dựng + soi; practice set bổ sung viết lại (folding),
dịch (mini provider), và kỷ luật cache giữ cho cây đã compile chạy nhanh.
Thành thạo những điều này thì hành vi của EF hết lãng xẹt: nó chính là bộ
máy này với một bộ phát SQL ở cuối.
"""
