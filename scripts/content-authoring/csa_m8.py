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
        title='Constant-folding visitor',
        prompt=(
            'Implement `class FoldVisitor : ExpressionVisitor` that replaces any BinaryExpression with two Constant operands by a single Constant of its computed value (ints only; support Add, Multiply, Subtract). Folding must be RECURSIVE: once inner binary nodes fold to constants, the enclosing binary folds too. The test builds the tree with explicit Expression.* calls because the compiler already constant-folds lambda literals at compile time — x => 2 + 3 + x arrives as (5 + x) with nothing left to fold. Also implement `static Expression<Func<int,int>> FoldExpr(Expression<Func<int,int>> e)` returning the visited (folded) expression.'
        ),
        difficulty='advanced',
        tests=[
            {
                "name": 'folds',
                "code": (
                    '// The compiler constant-folds lambda literals: x => 2 + 3 + x arrives as (5 + x).\n// Build the tree with the Expression API so the visitor genuinely has work to do:\nvar x = Expression.Parameter(typeof(int), "x");\nExpression<Func<int, int>> e =\n    Expression.Lambda<Func<int, int>>(\n        Expression.Add(Expression.Add(Expression.Constant(2), Expression.Constant(3)), x), x);\nvar folded = Solution.FoldExpr(e);\nvar f = folded.Compile();\nCj.Eq(f(4), 9, "(2+3)+x must fold to 5+x");\nint constAdds = 0;\nnew Visitor(v =>\n{\n    if (v is BinaryExpression b && v.NodeType == ExpressionType.Add\n        && b.Left is ConstantExpression && b.Right is ConstantExpression) constAdds++;\n}).Visit(folded);\nCj.Eq(constAdds, 0, "no constant-only Add remains — inner folds, then the enclosing node folds too");'
                ),
                "hint": 'Override VisitBinary: Visit the operands FIRST, then if both are int constants return Expression.Constant(computed) — recursing makes (2+3) fold before the outer Add sees it.',
            },
        ],
        reference=(
            'using System.Linq.Expressions;\n\npublic class FoldVisitor : ExpressionVisitor\n{\n    protected override Expression VisitBinary(BinaryExpression node)\n    {\n        var left = Visit(node.Left);\n        var right = Visit(node.Right);\n        if (left is ConstantExpression lc && right is ConstantExpression rc\n            && lc.Value is int a && rc.Value is int b)\n        {\n            return node.NodeType switch\n            {\n                ExpressionType.Add => Expression.Constant(a + b),\n                ExpressionType.Multiply => Expression.Constant(a * b),\n                ExpressionType.Subtract => Expression.Constant(a - b),\n                _ => node.Update(left, node.Conversion, right),\n            };\n        }\n        return node.Update(left, node.Conversion, right);\n    }\n}\n\npublic class Solution\n{\n    public static Expression<Func<int, int>> FoldExpr(Expression<Func<int, int>> e)\n        => (Expression<Func<int, int>>)new FoldVisitor().Visit(e);\n}\n\npublic class Visitor : ExpressionVisitor\n{\n    private readonly Action<Expression> _see;\n    public Visitor(Action<Expression> see) { _see = see; }\n    public override Expression? Visit(Expression? node)\n    {\n        if (node is not null) _see(node);\n        return base.Visit(node);\n    }\n}'
        ),
        wrong=(
            'using System.Linq.Expressions;\n\npublic class FoldVisitor : ExpressionVisitor\n{\n    protected override Expression VisitBinary(BinaryExpression node)\n    {\n        var left = Visit(node.Left);\n        var right = Visit(node.Right);\n        if (left is ConstantExpression lc && right is ConstantExpression rc\n            && lc.Value is int a && rc.Value is int b)\n        {\n            return node.NodeType switch\n            {\n                ExpressionType.Add => Expression.Constant(a - b),   // WRONG op\n                ExpressionType.Multiply => Expression.Constant(a * b),\n                ExpressionType.Subtract => Expression.Constant(a - b),\n                _ => node.Update(left, node.Conversion, right),\n            };\n        }\n        return node.Update(left, node.Conversion, right);\n    }\n}\n\npublic class Solution\n{\n    public static Expression<Func<int, int>> FoldExpr(Expression<Func<int, int>> e)\n        => (Expression<Func<int, int>>)new FoldVisitor().Visit(e);\n}\n\npublic class Visitor : ExpressionVisitor\n{\n    private readonly Action<Expression> _see;\n    public Visitor(Action<Expression> see) { _see = see; }\n    public override Expression? Visit(Expression? node)\n    {\n        if (node is not null) _see(node);\n        return base.Visit(node);\n    }\n}'
        ),
        level='guided',
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
            "        => Render(predicate.Body);\n\n"
            "    static string Render(Expression e) => e switch\n"
            "    {\n"
            "        BinaryExpression b => b.NodeType switch\n"
            "        {\n"
            "            ExpressionType.AndAlso => Render(b.Left) + \" AND \" + Render(b.Right),\n"
            "            ExpressionType.OrElse => Render(b.Left) + \" OR \" + Render(b.Right),\n"
            "            ExpressionType.GreaterThanOrEqual => Param(b.Left) + \" >= \" + Value(b.Right),\n"
            "            ExpressionType.LessThan => Param(b.Left) + \" < \" + Value(b.Right),\n"
            "            ExpressionType.Equal => Param(b.Left) + \" = \" + Value(b.Right),\n"
            "            _ => throw new NotSupportedException(b.NodeType.ToString()),\n"
            "        },\n"
            "        _ => throw new NotSupportedException(e.NodeType.ToString()),\n"
            "    };\n\n"
            "    static string Param(Expression e) => e is ParameterExpression p ? p.Name : \"?\";\n\n"
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
        title='Compile once, cache forever',
        prompt=(
            'Implement `static Func<int, bool> CachedCheck(int threshold)` that compiles the predicate `x => x >= threshold && x % 2 == 0` for the given threshold and caches the delegate in a static ConcurrentDictionary<int, Func<int, bool>>. The test proves compilation happens once: the SECOND call with the same threshold must return the SAME delegate instance (ReferenceEquals), invoking the cached delegate allocates nothing, and the boundary is exact — CachedCheck(10) accepts 10.'
        ),
        difficulty='advanced',
        tests=[
            {
                "name": 'same-instance',
                "code": (
                    'var f1 = Solution.CachedCheck(10);\nvar f2 = Solution.CachedCheck(10);\nCj.True(ReferenceEquals(f1, f2), "cached delegate reused");\nCj.True(f1(10), "boundary exact: 10 >= 10 accepted");\nCj.True(f1(12), "works above");\nCj.False(f1(9), "below rejected");'
                ),
                "hint": 'GetOrAdd on a static ConcurrentDictionary; build + compile only inside the factory.',
            },
            {
                "name": 'no-alloc-per-call',
                "code": (
                    'var f = Solution.CachedCheck(7);\nlong b0 = GC.GetAllocatedBytesForCurrentThread();\nfor (int i = 0; i < 100; i++) f(i);\nlong b1 = GC.GetAllocatedBytesForCurrentThread();\nCj.Eq(b1 - b0, 0L, $"invoking cached delegate allocated {b1 - b0}");'
                ),
                "hint": 'After caching, invoking is a plain delegate call — zero allocations.',
            },
        ],
        reference=(
            'using System.Collections.Concurrent;\nusing System.Linq.Expressions;\n\npublic class Solution\n{\n    static readonly ConcurrentDictionary<int, Func<int, bool>> Cache = new();\n\n    public static Func<int, bool> CachedCheck(int threshold) => Cache.GetOrAdd(threshold, static t =>\n    {\n        var x = Expression.Parameter(typeof(int), "x");\n        var ge = Expression.GreaterThanOrEqual(x, Expression.Constant(t));\n        var even = Expression.Equal(Expression.Modulo(x, Expression.Constant(2)), Expression.Constant(0));\n        return Expression.Lambda<Func<int, bool>>(Expression.AndAlso(ge, even), x).Compile();\n    });\n}'
        ),
        wrong=(
            'using System.Collections.Concurrent;\nusing System.Linq.Expressions;\n\npublic class Solution\n{\n    static readonly ConcurrentDictionary<int, Func<int, bool>> Cache = new();\n\n    public static Func<int, bool> CachedCheck(int threshold) => Cache.GetOrAdd(threshold, t =>\n    {\n        var x = Expression.Parameter(typeof(int), "x");\n        var ge = Expression.GreaterThanOrEqual(x, Expression.Constant(threshold + 1));   // wrong boundary\n        var even = Expression.Equal(Expression.Modulo(x, Expression.Constant(2)), Expression.Constant(0));\n        return Expression.Lambda<Func<int, bool>>(Expression.AndAlso(ge, even), x).Compile();\n    });\n}'
        ),
        level='guided',
    )


# --- recovered lesson MDX variables (regenerated from the last emit) ---
_m8_anatomy = '## Anatomy of an expression tree\n\nAn expression tree is an immutable object graph describing code: every\nnode has a `NodeType`, a static `Type`, and children. `x => x >= 5 && x <\n100` becomes:\n\n```\nLambda (Func<int, bool>)\n└── AndAlso\n    ├── GreaterThanOrEqual\n    │   ├── Parameter "x"\n    │   └── Constant 5\n    └── LessThan\n        ├── Parameter "x"\n        └── Constant 100\n```\n\nThree properties make trees the backbone of LINQ providers:\n\n1. **Inspectable** — you can walk and read the logic (that is how EF turns\n   your predicate into SQL).\n2. **Rewritable** — `ExpressionVisitor` produces modified copies (that is\n   how providers substitute constants, inline parameters, add tenant\n   filters).\n3. **Compilable** — `Compile()` emits a real delegate (that is how the\n   rewritten tree becomes executable again).\n\nThe decisive C# rule: a lambda assigned to `Expression<TDelegate>` is\nparsed into a tree by the COMPILER; the same lambda assigned to\n`Func<TDelegate>`-shaped delegate types is compiled to IL directly. One\nsyntax, two worlds — the target type decides which you get. Note the\nboundary: only *expressions* fit; statements, async, and many operators\n(`??=`, `=>` bodies with blocks) are outside the tree subset.\n'
_m8_anatomy_vi = '## Giải phẫu expression tree\n\nExpression tree là một đồ thị object bất biến mô tả mã: mỗi node có\n`NodeType`, `Type` tĩnh, và các con. `x => x >= 5 && x < 100` trở thành:\n\n```\nLambda (Func<int, bool>)\n└── AndAlso\n    ├── GreaterThanOrEqual\n    │   ├── Parameter "x"\n    │   └── Constant 5\n    └── LessThan\n        ├── Parameter "x"\n        └── Constant 100\n```\n\nBa thuộc tính làm cây thành xương sống của LINQ provider:\n\n1. **Kiểm tra được** — bạn có thể đi và đọc logic (đó là cách EF biến\n   predicate của bạn thành SQL).\n2. **Viết lại được** — `ExpressionVisitor` tạo bản sao đã sửa (đó là cách\n   provider thay thế hằng, inline tham số, thêm bộ lọc tenant).\n3. **Biên dịch được** — `Compile()` phát ra một delegate thật (đó là cách\n   cây đã viết lại thành khả thi trở lại).\n\nQuy tắc C# quyết định: lambda gán cho `Expression<TDelegate>` được compiler\nPHÂN TÍCH thành cây; cùng lambda đó gán cho delegate `Func<TDelegate>` thì\nbiên dịch thẳng thành IL. Một cú pháp, hai thế giới — kiểu đích quyết định\nbạn nhận được gì. Lưu ý ranh giới: chỉ *biểu thức* mới khớp; câu lệnh,\nasync, và nhiều toán tử (`??=`, thân `=>` có khối) nằm ngoài tập con của\ncây.\n'
_m8_building = '## Building and compiling expressions\n\nBeyond parsing lambdas, you build trees node by node — this is how rule\nengines turn configuration into executable predicates:\n\n```csharp\nvar x = Expression.Parameter(typeof(int), "x");\nvar body = Expression.AndAlso(\n    Expression.GreaterThanOrEqual(x, Expression.Constant(5)),\n    Expression.LessThan(x, Expression.Constant(100)));\nvar lambda = Expression.Lambda<Func<int, bool>>(body, x);\nFunc<int, bool> f = lambda.Compile();\n```\n\nRules that prevent the classic failures:\n\n- **Reuse `ParameterExpression` nodes.** Two different `Parameter` objects\n  with the same name are DIFFERENT variables; `Compile()` throws\n  "variable \'x\' references itself"... actually it throws on unbound or\n  mismatched parameters. Build the parameter once and pass the same node\n  everywhere, including to `Lambda`.\n- **`Expression.Constant` captures the value at build time** — dynamic\n  predicates need either rebuild-per-change or\n  `Expression.Field`/`Expression.Closure` over a captured object.\n- **`Compile()` is expensive** (ms) and the compiled delegate is GC-heavy\n  to produce — cache compiled delegates keyed by the semantic input.\n\nWhen trees are the WRONG tool: hot per-item logic (trees add indirection\nthe JIT cannot fully remove), anything needing statements or `async`, and\none-shot scripts where a plain delegate is simpler. Trees shine exactly\nwhere you must *look at* the logic: providers, rules, serialization of\nqueries.\n'
_m8_building_vi = '## Dựng và biên dịch biểu thức\n\nNgoài việc phân tích lambda, bạn dựng cây theo từng node — đây là cách rule\nengine biến cấu hình thành predicate chạy được:\n\n```csharp\nvar x = Expression.Parameter(typeof(int), "x");\nvar body = Expression.AndAlso(\n    Expression.GreaterThanOrEqual(x, Expression.Constant(5)),\n    Expression.LessThan(x, Expression.Constant(100)));\nvar lambda = Expression.Lambda<Func<int, bool>>(body, x);\nFunc<int, bool> f = lambda.Compile();\n```\n\nCác luật ngăn thất bại kinh điển:\n\n- **Tái sử dụng node `ParameterExpression`.** Hai object `Parameter` khác\n  nhau cùng tên là HAI biến khác nhau; `Compile()` ném lỗi "variable \'x\'\n  references itself" hoặc lỗi tham số chưa bind. Dựng parameter một lần và\n  truyền cùng node đó đi khắp nơi, kể cả cho `Lambda`.\n- **`Expression.Constant` chụp giá trị lúc dựng** — predicate động cần hoặc\n  dựng lại khi thay đổi, hoặc `Expression.Field`/`Expression.Closure` trên\n  một object bị capture.\n- **`Compile()` đắt** (ms) và delegate biên dịch tốn GC để tạo — cache\n  delegate đã compile theo key là input ngữ nghĩa.\n\nKhi nào cây là công cụ SAI: logic chạy mỗi phần tử trên đường nóng (cây\nthêm lớp gián tiếp mà JIT không xóa được hết), mọi thứ cần câu lệnh hoặc\n`async`, và script dùng một lần nơi delegate thường đơn giản hơn. Cây tỏa\nsáng đúng nơi bạn phải *nhìn vào* logic: provider, rule, serialization của\nquery.\n'
_m8_visitors = '## Visiting and rewriting trees\n\n`ExpressionVisitor` walks a tree and rebuilds it, calling `VisitXxx` per\nnode kind. Override only what you change; `Visit` handles recursion and\nreconstruction:\n\n```csharp\nclass TenantFilter : ExpressionVisitor\n{\n    protected override Expression VisitBinary(BinaryExpression node)\n    {\n        var left = Visit(node.Left);\n        var right = Visit(node.Right);\n        return node.Update(left, node.Conversion, right);\n    }\n    protected override Expression VisitConstant(ConstantExpression node)\n        => node.Value is int v && v == 42 ? Expression.Constant(43) : node;\n}\n```\n\nThis is precisely what EF Core does: your `Where(o => o.Tenant == "a")`\nis visited, the member access becomes a column, the constant becomes a\nparameter, and the tree is re-emitted as SQL. Visitors are also how you\nimplement optimization passes (constant folding, predicate pushdown) and\nsafety passes (rejecting unsupported constructs with a clear message).\n\nTwo patterns worth knowing: **bottom-up transforms** (fold children first —\nconstant folding) and **top-down guards** (validate before descending —\nprovider translation). Returning the ORIGINAL node (via `node.Update(...)`)\nwhen nothing changed lets the visitor skip rebuilding untouched subtrees —\ncheap immutability in action.\n'
_m8_visitors_vi = '## Đi và viết lại cây\n\n`ExpressionVisitor` đi qua cây và dựng lại nó, gọi `VisitXxx` theo từng loại\nnode. Override chỉ những gì bạn đổi; `Visit` xử lý đệ quy và tái dựng:\n\n```csharp\nclass TenantFilter : ExpressionVisitor\n{\n    protected override Expression VisitBinary(BinaryExpression node)\n    {\n        var left = Visit(node.Left);\n        var right = Visit(node.Right);\n        return node.Update(left, node.Conversion, right);\n    }\n    protected override Expression VisitConstant(ConstantExpression node)\n        => node.Value is int v && v == 42 ? Expression.Constant(43) : node;\n}\n```\n\nĐây chính xác là điều EF Core làm: `Where(o => o.Tenant == "a")` của bạn\nđược visit, truy cập member thành cột, hằng thành tham số, và cây được phát\nlại thành SQL. Visitor cũng là cách bạn hiện thực các lượt tối ưu (constant\nfolding, predicate pushdown) và các lượt an toàn (từ chối cấu trúc không hỗ\ntrợ bằng thông báo rõ ràng).\n\nHai pattern đáng biết: **biến đổi bottom-up** (fold con trước — constant\nfolding) và **guard top-down** (xác thực trước khi đi xuống — dịch provider).\nTrả về node GỐC (qua `node.Update(...)`) khi không đổi gì giúp visitor bỏ\nqua việc dựng lại các cây con nguyên vẹn — tính bất biến giá rẻ đang hoạt\nđộng.\n'
_m8_checkpoint = "## Checkpoint: expression trees\n\nThe graded task exercises build + inspect; the practice set adds rewrite\n(folding), translate (mini provider), and the cache-discipline that keeps\ncompiled trees fast. Master these and EF's behavior stops being magic:\nit is this exact machinery with a SQL emitter at the end.\n"
_m8_checkpoint_vi = '## Checkpoint: expression trees\n\nBài được chấm luyện dựng + soi; practice set bổ sung viết lại (folding),\ndịch (mini provider), và kỷ luật cache giữ cho cây đã compile chạy nhanh.\nThành thạo những điều này thì hành vi của EF hết lãng xẹt: nó chính là bộ\nmáy này với một bộ phát SQL ở cuối.\n'

"""
Authoring notes — regeneration loop: `python3 csa_emit.py` rewrites every
EN/VI JSON + MDX under the course dir, then
`node --import tsx validate-content-csa.ts` proves both locales load.
"""
