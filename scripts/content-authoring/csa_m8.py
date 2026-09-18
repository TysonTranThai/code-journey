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
            'Implement `class FoldVisitor : ExpressionVisitor` that replaces any BinaryExpression with two Constant operands by a single Constant of its computed value (ints only; support Add, Multiply, Subtract). Folding must be RECURSIVE: once inner binary nodes fold to constants, the enclosing binary folds too. Also implement `static Expression<Func<int,int>> FoldExpr(Expression<Func<int,int>> e)` returning the visited (folded) expression.'
        ),
        difficulty='advanced',
        tests=[
            {
                "name": 'folds',
                "code": (
                    'Expression<Func<int, int>> e = x => 2 + 3 + x;\nvar folded = Solution.FoldExpr(e);\nvar f = folded.Compile();\nCj.Eq(f(4), 9, "(2+3)+x must fold to 5+x");\nint constAdds = 0;\nnew Visitor(v =>\n{\n    if (v is BinaryExpression b && v.NodeType == ExpressionType.Add\n        && b.Left is ConstantExpression && b.Right is ConstantExpression) constAdds++;\n}).Visit(folded);\nCj.Eq(constAdds, 0, "no constant-only Add remains — inner folds, then the enclosing node folds too");'
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
