"""Module 18 — NativeAOT, trimming, and deployment models (csa-m18)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-aot-deployment",
        "NativeAOT, Trimming, and Deployment Models",
        "How .NET ships: framework-dependent, self-contained, trimmed, AOT — the tradeoffs and the reflection tax.",
    )

    csa.register_lesson(
        MID, "csa-m18-deployment-models", "The deployment spectrum",
        "Framework-dependent vs self-contained vs single-file vs ReadyToRun vs NativeAOT — costs and fits.",
        15, "advanced", _m18_models, _m18_models_vi,
    )
    csa.register_lesson(
        MID, "csa-m18-trimming", "Trimming and the reflection tax",
        "How the linker decides what survives, why reflection breaks, and the annotations that fix it.",
        16, "advanced", _m18_trimming, _m18_trimming_vi,
    )
    csa.register_lesson(
        MID, "csa-m18-aot-mindset", "The AOT mindset: runtime services, statically",
        "What NativeAOT removes (JIT, dynamic code), what it demands (static everything), and source generators as the bridge.",
        15, "advanced", _m18_aot, _m18_aot_vi,
    )
    csa.register_lesson(
        MID, "csa-m18-config-concepts", "Configuration, startup, and the compile-time contract",
        "AppContext data, configuration sources, and turning runtime decisions into compile-time decisions.",
        14, "advanced", _m18_config, _m18_config_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m18", "Checkpoint: deployment and AOT",
        "Synthesis: reason about deployment choices and write trim-safe reflection.",
        12, "advanced", _m18_checkpoint, _m18_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m18-task", MID,
        title="Deployment/AOT checkpoint",
        prompt=(
            "Implement `static string DeploymentDescription(bool selfContained, bool trimmed, bool aot)`: return "
            "\"framework-dependent\" when selfContained=false; \"self-contained\" when selfContained && !trimmed && "
            "!aot; \"trimmed\" when selfContained && trimmed && !aot; \"aot\" when aot (regardless of trimmed — AOT "
            "implies it). Then implement `static bool IsTrimCompatible(string reflectionPattern)` returning false "
            "for patterns the linker cannot prove: \"assembly scanning\", \"activator by name\", \"json by string "
            "type name\"; true for \"source generated serializer\", \"generic constraint\", \"explicit registration\"."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "deployment-desc",
                "code": (
                    'Cj.Eq(Solution.DeploymentDescription(false, false, false), "framework-dependent", "no runtime bundled");\n'
                    'Cj.Eq(Solution.DeploymentDescription(true, false, false), "self-contained", "runtime bundled");\n'
                    'Cj.Eq(Solution.DeploymentDescription(true, true, false), "trimmed", "trimmed IL");\n'
                    'Cj.Eq(Solution.DeploymentDescription(true, true, true), "aot", "AOT wins");\n'
                    'Cj.Eq(Solution.DeploymentDescription(true, false, true), "aot", "AOT implies trimmed");'
                ),
                "hint": "Check aot first, then selfContained, then trimmed.",
            },
            {
                "name": "trim-compat",
                "code": (
                    'Cj.False(Solution.IsTrimCompatible("assembly scanning"), "linker cannot prove dynamic discovery");\n'
                    'Cj.False(Solution.IsTrimCompatible("activator by name"), "no type survives without a reference");\n'
                    'Cj.True(Solution.IsTrimCompatible("source generated serializer"), "generated code is static");\n'
                    'Cj.True(Solution.IsTrimCompatible("explicit registration"), "referenced = kept");'
                ),
                "hint": "A set of safe patterns vs known-dynamic patterns; everything dynamic loses.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static string DeploymentDescription(bool selfContained, bool trimmed, bool aot)\n"
            "    {\n"
            "        if (aot) return \"aot\";\n"
            "        if (!selfContained) return \"framework-dependent\";\n"
            "        if (trimmed) return \"trimmed\";\n"
            "        return \"self-contained\";\n"
            "    }\n\n"
            "    private static readonly HashSet<string> SafePatterns = new()\n"
            "    {\n"
            "        \"source generated serializer\", \"generic constraint\", \"explicit registration\"\n"
            "    };\n\n"
            "    public static bool IsTrimCompatible(string reflectionPattern)\n"
            "        => SafePatterns.Contains(reflectionPattern);\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static string DeploymentDescription(bool selfContained, bool trimmed, bool aot)\n"
            "    {\n"
            "        if (!selfContained) return \"framework-dependent\";\n"
            "        if (trimmed) return \"trimmed\";   // WRONG: checked before aot — AOT is never reported\n"
            "        if (aot) return \"aot\";\n"
            "        return \"self-contained\";\n"
            "    }\n\n"
            "    public static bool IsTrimCompatible(string reflectionPattern)\n"
            "        => !reflectionPattern.Contains(\"scanning\");   // WRONG: 'activator by name' slips through\n"
            "}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p18-aot", "Deployment drills",
        "Trim-safety reasoning, dynamic-features audit, and startup-cost arithmetic.",
        45, "advanced", "csa-m18-trimming",
        ["csa-p18-reflection-audit", "csa-p18-size-math"],
    )
    csa.register_challenge(
        "csa-p18-reflection-audit", MID,
        title="Reflection audit",
        prompt=(
            "Given a type, list which reflection operations would break under aggressive trimming: implement "
            "`static List<string> Audit(Type t)` returning descriptions for each operation that survives trimming "
            "statically: include \"gettype-of-t\" if t is a compile-time visible type (always true here), "
            "\"declared-fields\" if it has fields (GetFields always works on kept types), \"attribute-read\" if it "
            "has attributes, \"constructor-invoke\" if it has a parameterless ctor — but NEVER include "
            "\"scan-all-types\" (never survives). The test verifies both the includes and the absent scan entry."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "audit-kept-type",
                "code": (
                    "var ops = Solution.Audit(typeof(Sample));\n"
                    'Cj.True(ops.Contains("gettype-of-t"), "kept type introspects fine");\n'
                    'Cj.True(ops.Contains("declared-fields"), "fields readable");\n'
                    'Cj.False(ops.Contains("scan-all-types"), "assembly scanning never survives");'
                ),
                "hint": "typeof(Sample) is a direct reference → the type (and its members) is kept; scanning is never provable.",
            },
        ],
        reference=(
            "public class Sample\n{\n"
            "    public int Value;\n"
            "    [Obsolete(\"demo\")]\n"
            "    public void Legacy() { }\n"
            "}\n\n"
            "public class Solution\n{\n"
            "    public static List<string> Audit(Type t)\n"
            "    {\n"
            "        var ops = new List<string> { \"gettype-of-t\" };\n"
            "        if (t.GetFields(BindingFlags.Public | BindingFlags.Instance).Length > 0)\n"
            "            ops.Add(\"declared-fields\");\n"
            "        if (t.GetMethods().Any(m => m.GetCustomAttributes().Any()))\n"
            "            ops.Add(\"attribute-read\");\n"
            "        if (t.GetConstructor(Type.EmptyTypes) is not null)\n"
            "            ops.Add(\"constructor-invoke\");\n"
            "        // \"scan-all-types\" deliberately absent: never trim-provable.\n"
            "        return ops;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Sample\n{\n"
            "    public int Value;\n"
            "    [Obsolete(\"demo\")]\n"
            "    public void Legacy() { }\n"
            "}\n\n"
            "public class Solution\n{\n"
            "    public static List<string> Audit(Type t)\n"
            "    {\n"
            "        var ops = new List<string> { \"gettype-of-t\", \"scan-all-types\" };   // WRONG: scanning claimed safe\n"
            "        ops.Add(\"declared-fields\");\n"
            "        return ops;\n"
            "    }\n}"
        ),
        level="independent",
    )
    csa.register_challenge(
        "csa-p18-size-math", MID,
        title="Startup and size arithmetic",
        prompt=(
            "Implement `static (long bytes, double startupMs) DeployCost(string model, int appBytes, double "
            "jitMs)` describing deployment costs conceptually: \"framework-dependent\" → bytes = appBytes + "
            "60_000_000 runtime is NOT bundled (return appBytes, jitMs + 120 for first-call JIT); "
            "\"self-contained\" → bytes = appBytes + 65_000_000, startupMs = jitMs + 120; \"trimmed\" → bytes = "
            "appBytes + 25_000_000, startupMs = jitMs + 120; \"aot\" → bytes = appBytes + 18_000_000, startupMs = "
            "2.0 (no JIT). The graded point: AOT pays no JIT tax; the others all carry it."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "cost-table",
                "code": (
                    "var (b1, s1) = Solution.DeployCost(\"framework-dependent\", 1_000_000, 80);\n"
                    'Cj.Eq(b1, 1_000_000, "runtime not bundled");\n'
                    'Cj.True(Math.Abs(s1 - 200) < 0.001, "JIT tax applies");\n'
                    "var (b2, s2) = Solution.DeployCost(\"aot\", 1_000_000, 80);\n"
                    'Cj.Eq(b2, 19_000_000, "compact runtime baked in");\n'
                    'Cj.True(Math.Abs(s2 - 2.0) < 0.001, "no JIT tax");'
                ),
                "hint": "Switch on model; return the tuple per the table. AOT ignores jitMs entirely.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static (long bytes, double startupMs) DeployCost(string model, int appBytes, double jitMs)\n"
            "        => model switch\n"
            "        {\n"
            "            \"framework-dependent\" => (appBytes, jitMs + 120),\n"
            "            \"self-contained\" => (appBytes + 65_000_000L, jitMs + 120),\n"
            "            \"trimmed\" => (appBytes + 25_000_000L, jitMs + 120),\n"
            "            \"aot\" => (appBytes + 18_000_000L, 2.0),\n"
            "            _ => throw new ArgumentException($\"unknown model {model}\"),\n"
            "        };\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static (long bytes, double startupMs) DeployCost(string model, int appBytes, double jitMs)\n"
            "        => model switch\n"
            "        {\n"
            "            \"framework-dependent\" => (appBytes, 0),   // WRONG: JIT happens on framework-dependent too\n"
            "            \"self-contained\" => (appBytes + 65_000_000L, jitMs + 120),\n"
            "            \"trimmed\" => (appBytes + 25_000_000L, jitMs + 120),\n"
            "            \"aot\" => (appBytes + 18_000_000L, jitMs + 120),   // WRONG: AOT has no JIT\n"
            "            _ => throw new ArgumentException($\"unknown model {model}\"),\n"
            "        };\n}"
        ),
        level="independent",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m18_models = r"""## The deployment spectrum

One .NET app, five shipping models — each answering "where does the
runtime come from, and when is code compiled?":

| Model | Ships runtime? | Compile moment | Size | Startup | Fits |
|---|---|---|---|---|---|
| Framework-dependent | no (uses installed/host) | JIT at run | ~app | JIT tax | servers with shared runtimes |
| Self-contained | yes, full | JIT at run | ~65MB+ | JIT tax | version-pinned deployments |
| Trimmed self-contained | yes, pruned | JIT at run | ~25MB | JIT tax | CLIs, containers |
| ReadyToRun | yes, precompiled | publish (tier-1-ish) | +30%ish | low | server startup-sensitive |
| NativeAOT | yes, linked | publish (fully) | ~18MB | ~ms | serverless, small containers |

The two axes — runtime bundling and compile timing — are independent-ish
but shape each other: AOT necessarily bundles a (smaller, different)
runtime because it cannot rely on the JIT host.

Deciding factors in practice:

1. **Who controls the host?** Shared runtime = framework-dependent (tiny
   diffs, shared patching). Locked-down containers = self-contained
   (pinned, reproducible).
2. **Startup sensitivity?** Serverless/CLI = AOT or R2R. Long-running
   services mostly amortize JIT warmup.
3. **Dynamic features in use?** Heavy reflection (plugins, config-driven
   activation) fights trimming and AOT — Module 18's core tradeoff.
4. **Platform matrix?** AOT compiles per-OS/architecture; JIT binaries
   (R2R too) are per-rid bundles you select at publish.

Container math makes this concrete: a trimmed self-contained ASP.NET Core
image runs ~110MB vs ~220MB untrimmed; NativeAOT minimal APIs land under
40MB with sub-20ms startup. For scale-to-zero platforms, that startup
number IS the cost model.
"""

_m18_models_vi = r"""## Phổ triển khai

Một app .NET, năm mô hình vận chuyển — mỗi mô hình trả lời "runtime đến từ
đâu, và code được compile khi nào?":

| Mô hình | Kèm runtime? | Thời điểm compile | Kích thước | Khởi động | Phù hợp |
|---|---|---|---|---|---|
| Framework-dependent | không (dùng host đã cài) | JIT lúc chạy | ~app | thuế JIT | server dùng chung runtime |
| Self-contained | có, đầy đủ | JIT lúc chạy | ~65MB+ | thuế JIT | triển khai ghim phiên bản |
| Trimmed self-contained | có, cắt tỉa | JIT lúc chạy | ~25MB | thuế JIT | CLI, container |
| ReadyToRun | có, precompiled | publish (kiểu tier-1) | +30% | thấp | service nhạy khởi động |
| NativeAOT | có, linked | publish (hoàn toàn) | ~18MB | ~ms | serverless, container nhỏ |

Hai trục — việc gộp runtime và thời điểm compile — độc lập nhưng định hình
nhau: AOT tất yếu gộp một runtime (nhỏ hơn, khác biệt) vì nó không thể dựa
vào host JIT.

Các yếu tố quyết định trong thực tế:

1. **Ai kiểm soát host?** Runtime dùng chung = framework-dependent (diff
   nhỏ, vá dùng chung). Container khoá chặt = self-contained (ghim, tái
   lập được).
2. **Nhạy khởi động?** Serverless/CLI = AOT hoặc R2R. Service chạy dài
   phần lớn khấu trừ warmup JIT.
3. **Đang dùng tính năng động?** Reflection nặng (plugin, kích hoạt theo
   config) đối đầu trimming và AOT — mối đánh đổi lõi của Module 18.
4. **Ma trận nền tảng?** AOT compile cho từng OS/kiến trúc; binary JIT
   (và cả R2R) là bundle theo-rid bạn chọn lúc publish.

Phép tính container làm cho nó cụ thể: image ASP.NET Core trimmed
self-contained chạy ~110MB so với ~220MB chưa trim; NativeAOT minimal API
dưới 40MB với khởi động dưới 20ms. Với nền tảng scale-to-zero, con số
khởi động đó CHÍNH LÀ mô hình chi phí.
"""

_m18_trimming = r"""## Trimming and the reflection tax

The trimmer (ILLink) walks the call graph from your entry points,
discarding every type/member it cannot prove used. "Cannot prove used" is
the operative phrase — not "unused":

```csharp
var t = Type.GetType(configValue)!;      // string comes from config at RUNTIME
Activator.CreateInstance(t);             // trimmer saw a string, not a type
// → every type COULD be referenced; the trimmer must assume all of them
//   or (with trimming on) assume none — either way, you break or you bloat
```

What breaks, and the fix:

| Dynamic pattern | Why it breaks | Static replacement |
|---|---|---|
| Type-by-name activation | names are data, not references | explicit factory / `Dictionary<string, Func<T>>` |
| Assembly scanning | whole-assembly reachability is unprovable | attribute + source generator emitting registrations |
| Reflection-based serialization | members via string/attribute paths | source-generated serializers (System.Text.Json) |
| `Activator.CreateInstance<T>` with unconstrained T | no ctor provable | generic constraint `where T : new()` or factory parameter |

The annotations that declare intent:

```csharp
[DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicConstructors)]
private static Type? _handlerType;   // "this Type value is meant to have public ctors kept"

[RequiresUnreferencedCode("uses Type.GetType")]
private static void LoadPlugin(string name) { ... }   // "calling me breaks trimming"
```

`DynamicallyAccessedMembers` preserves named member kinds on a Type-typed
value; `RequiresUnreferencedCode` flags the method so callers get build
warnings — the trim analysis turning reflection habits into compile-time
conversations.

The honest budget: a reflection-light app trims 50–70% of size for free;
a plugin-heavy app fights the linker at every step and should ask whether
it wants trimming at all. The checkpoint's audit challenge encodes the
reasoning: which operations survive, which never do.
"""

_m18_trimming_vi = r"""## Trimming và thuế reflection

Trimmer (ILLink) đi dọc đồ thị lời gọi từ các điểm vào của bạn, vứt bỏ mọi
type/member nó không chứng minh được là có dùng. "Không chứng minh được là
có dùng" là cụm từ then chốt — không phải "không dùng":

```csharp
var t = Type.GetType(configValue)!;      // string đến từ config lúc RUNTIME
Activator.CreateInstance(t);             // trimmer thấy một string, không phải kiểu
// → mọi type ĐỀU có thể được tham chiếu; trimmer phải giả định giữ tất cả
//   hoặc (khi bật trim) giả định không giữ gì — một trong hai, bạn gãy hoặc bạn phình
```

Cái gì gãy, và cách sửa:

| Pattern động | Vì sao gãy | Thay thế tĩnh |
|---|---|---|
| Kích hoạt kiểu theo tên | tên là dữ liệu, không phải tham chiếu | factory tường minh / `Dictionary<string, Func<T>>` |
| Quét assembly | khả năng tiếp cận của cả assembly là không chứng minh được | attribute + source generator phát sinh đăng ký |
| Serialization dựa reflection | thành phần qua đường string/attribute | serializer sinh mã (System.Text.Json) |
| `Activator.CreateInstance<T>` với T không ràng buộc | không ctor nào chứng minh được | ràng buộc generic `where T : new()` hoặc tham số factory |

Các annotation khai báo ý định:

```csharp
[DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicConstructors)]
private static Type? _handlerType;   // "giá trị Type này cần giữ public ctor"

[RequiresUnreferencedCode("uses Type.GetType")]
private static void LoadPlugin(string name) { ... }   // "gọi tôi làm hỏng trimming"
```

`DynamicallyAccessedMembers` giữ lại các loại thành phần được nêu trên
một giá trị kiểu Type; `RequiresUnreferencedCode` cắm cờ phương thức để
caller nhận warning lúc build — phân tích trim biến thói quen reflection
thành cuộc đối thoại lúc compile.

Ngân sách trung thực: app nhẹ reflection trim được 50–70% kích thước miễn
phí; app nặng plugin đối đầu linker từng bước và nên tự hỏi có muốn trim
hay không. Thử thách audit trong checkpoint mã hóa suy luận đó: phép toán
nào sống, phép nào không bao giờ.
"""

_m18_aot = r"""## The AOT mindset: runtime services, statically

NativeAOT is not "JIT but earlier" — it removes runtime services:

- **No JIT**: no tiering, no dynamic PGO, no code generation at run.
  Consequences: no `Reflection.Emit`, no `System.Linq.Expressions.Compile()`,
  no dynamically loaded assemblies executing code.
- **No interpreter fallback**: reflection still WORKS for metadata
  reading, but member access paths are precompiled — unreachable members
  don't exist.
- **Static everything**: every type the program might use must be
  reachable at compile time, or preserved explicitly (same annotations as
  trimming, plus AOT-specific warnings).

What you gain: microsecond startup, small self-contained binaries, no
JIT memory, predictable first-request latency, and hard-to-tamper
deployment (no IL to swap on disk).

**Source generators are the bridge.** The industry-wide pattern that
makes AOT viable: move code GENERATION from runtime reflection to compile
time. System.Text.Json's source generator, ASP.NET Core's route/parameter
generators, DI registrations, regex — each replaces a reflective
mechanism with emitted static code:

```csharp
[JsonSourceGenerationOptions(WriteIndented = true)]
[JsonSerializable(typeof(Order))]
partial class OrderJsonContext : JsonSerializerContext { }

JsonSerializer.Serialize(order, OrderJsonContext.Default.Order);
// metadata generated at compile time; no reflection at run
```

The migration mindset: every time code asks "what types exist?" or
"construct this by name," rewrite it as an explicit registration table —
often generated from attributes by your own source generator (Module 8's
skill). The AOT constraint is a forcing function for the architecture the
course has advocated all along: explicit boundaries, static knowledge,
reflection at the edges only.
"""

_m18_aot_vi = r"""## Tư duy AOT: các dịch vụ runtime, theo kiểu tĩnh

NativeAOT không phải "JIT nhưng sớm hơn" — nó loại bỏ các dịch vụ runtime:

- **Không JIT**: không tiering, không dynamic PGO, không sinh mã lúc chạy.
  Hệ quả: không `Reflection.Emit`, không
  `System.Linq.Expressions.Compile()`, không thực thi assembly nạp động.
- **Không interpreter dự phòng**: reflection vẫn HOẠT ĐỘNG với việc đọc
  metadata, nhưng đường truy thành phần là precompiled — thành phần không
  thể với tới sẽ không tồn tại.
- **Tĩnh mọi thứ**: mọi kiểu chương trình có thể dùng phải reachable lúc
  compile, hoặc được giữ tường minh (cùng các annotation như trimming,
  cộng thêm các warning riêng của AOT).

Bạn đổi được gì: khởi động micro giây, binary tự chủ nhỏ, không bộ nhớ
JIT, độ trễ request-đầu tiên dự đoán được, và triển khai khó can thiệp
(không IL trên đĩa để thay thế).

**Source generator là cây cầu.** Pattern toàn ngành làm AOT khả thi:
chuyển việc SINH MÃ từ reflection lúc runtime sang compile time. Source
generator của System.Text.Json, generator route/tham số của ASP.NET Core,
đăng ký DI, regex — mỗi cái thay một cơ chế phản chiếu bằng code tĩnh được
phát sinh:

```csharp
[JsonSourceGenerationOptions(WriteIndented = true)]
[JsonSerializable(typeof(Order))]
partial class OrderJsonContext : JsonSerializerContext { }

JsonSerializer.Serialize(order, OrderJsonContext.Default.Order);
// metadata sinh lúc compile; không reflection lúc chạy
```

Tư duy chuyển đổi: mỗi lần code hỏi "có những kiểu nào?" hay "khởi tạo
cái này theo tên," hãy viết lại thành bảng đăng ký tường minh — thường do
source generator của chính bạn sinh từ attribute (kỹ năng Module 8). Ràng
buộc AOT là hàm ép cho kiến trúc mà khóa học luôn ủng hộ: biên tường
minh, tri thức tĩnh, reflection chỉ ở rìa.
"""

_m18_config = r"""## Configuration, startup, and the compile-time contract

Deployment models reshape where decisions live. The runtime-configuration
surface you should reason about deliberately:

**Compile/publish-time switches** (MsBuild properties): `PublishTrimmed`,
`PublishAot`, `PublishReadyToRun`, `InvariantGlobalization` (drops ICU —
smaller images, culture-invariant semantics), `EnableDynamicLoading`
(off for trim, on for plugins). These choose the runtime contract; a
different property set can mean a different bug surface entirely.

**Runtime switches** (env vars): `DOTNET_TieredPGO`, `DOTNET_gcServer`,
`DOTNET_GCDynamicAdaptationMode` — measurable behavior changes with zero
code. Production tuning starts here, not with rewrites: the checkpoint's
cost table is the shape of the reasoning (which costs are structural,
which are tunable).

**The compile-time contract** is the AOT-era discipline: prefer decisions
made at build over decisions made at run, whenever the decision is
knowable at build. DI registrations emitted by generators, routes
generated from method signatures, serializers generated from types —
each moves a failure from production runtime to CI build. The remaining
runtime configuration (endpoints, credentials, feature flags) is exactly
the part that SHOULD be data — the art is the boundary, and the
boundary is a design decision this course keeps making you articulate.
"""

_m18_config_vi = r"""## Cấu hình, khởi động, và hợp đồng lúc compile

Các mô hình triển khai định hình nơi quyết định nằm. Bề mặt cấu hình
runtime mà bạn nên suy luận một cách chủ ý:

**Công tắc lúc compile/publish** (property MsBuild): `PublishTrimmed`,
`PublishAot`, `PublishReadyToRun`, `InvariantGlobalization` (bỏ ICU —
image nhỏ hơn, ngữ nghĩa bất biến văn hóa), `EnableDynamicLoading` (tắt
cho trim, bật cho plugin). Những cái này chọn hợp đồng runtime; một bộ
property khác có thể nghĩa là một bề mặt bug hoàn toàn khác.

**Công tắc lúc runtime** (biến môi trường): `DOTNET_TieredPGO`,
`DOTNET_gcServer`, `DOTNET_GCDynamicAdaptationMode` — thay đổi hành vi đo
được mà không cần code. Tinh chỉnh production bắt đầu từ đây, không phải
viết lại code: bảng chi phí trong checkpoint đúng là hình dạng của suy
luận đó (chi phí nào mang tính cấu trúc, chi phí nào tinh chỉnh được).

**Hợp đồng lúc compile** là kỷ luật thời AOT: ưu tiên quyết định tại build
hơn quyết định lúc chạy, bất cứ nơi nào quyết định đã biết từ lúc build.
Đăng ký DI do generator phát sinh, route sinh từ chữ ký phương thức,
serializer sinh từ kiểu — mỗi cái dời một lỗi từ runtime production về
build trong CI. Phần cấu hình runtime còn lại (endpoint, credential,
feature flag) chính là phần NÊN là dữ liệu — nghệ thuật nằm ở ranh giới,
và ranh giới là một quyết định thiết kế mà khóa học liên tục bắt bạn phát
biểu.
"""

_m18_checkpoint = r"""## Checkpoint: deployment and AOT

The graded task makes the deployment taxonomy and the trim-safety
boundary into executable decisions. Practice adds the reflection audit
(what survives, what never does) and the cost arithmetic that justifies
each model to a budget holder.
"""

_m18_checkpoint_vi = r"""## Checkpoint: triển khai và AOT

Bài được chấm biến hệ thống phân loại triển khai và biên an-toàn-trim
thành các quyết định thực thi được. Practice thêm audit reflection (cái gì
sống, cái gì không bao giờ) và phép tính chi phí biện minh cho từng mô
hình trước người giữ ngân sách."""
