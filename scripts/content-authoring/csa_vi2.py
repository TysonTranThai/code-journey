"""VI overlays for C# Advanced challenges — modules 2–13 (m2…m13).

Keys are challenge ids; values: {"title", "prompt", "hints": {test_name: hint}}.
Code identifiers, signatures, and error messages stay in English per the
localization contract (same as Beginner/Intermediate).
"""

VI: dict[str, dict] = {
    "csa-checkpoint-m2-task": {
        "title": "Checkpoint mô hình bộ nhớ",
        "prompt": (
            "Hiện thực `static (int copiedX, int aliasedY) AliasVsCopy()`. Bên trong: tạo struct "
            "`S { public int X; }` với X=1, sao chép sang biến cục bộ thứ hai rồi đặt X của bản sao "
            "bằng 2 (bản gốc phải giữ 1); sau đó tạo mảng `int[] a = {5}`, lấy ref local "
            "`ref int r = ref a[0]`, gán r=7. Trả về (X của struct gốc, a[0])."
        ),
        "hints": {
            "copy-independence": "Gán struct là sao chép; `ref` tạo bí danh ghi xuyên qua.",
            "allocation-shape": "Cả phương thức chỉ được cấp phát tối đa mảng nhỏ (và tuple) — không boxing, không string.",
        },
    },
    "csa-p2-span-parse": {
        "title": "Phân tích mà không cấp phát",
        "prompt": (
            "Hiện thực `static (int a, int b) ParsePair(ReadOnlySpan<char> input)` phân tích hai số "
            "nguyên phân tách bằng dấu phẩy từ span mà KHÔNG cấp phát string nào. Cấm Split, cấm "
            "Substring — cắt span trực tiếp rồi parse. Test đo cấp phát để chứng minh điều đó."
        ),
        "hints": {
            "correctness": "Cắt tại dấu phẩy: input[..i] và input[(i+1)..], rồi int.Parse từng lát.",
            "zero-alloc": "int.Parse(ReadOnlySpan<char>) không bao giờ cấp phát; tuple nằm gọn trong thanh ghi/stack.",
        },
    },
    "csa-p2-defensive-copy": {
        "title": "Bản sao phòng thủ trong thành viên readonly",
        "prompt": (
            "Một struct khả biến nằm trong trường readonly bị sao chép ở mỗi lần truy cập thành viên. "
            "Hiện thực struct `Container` với `private readonly Mut _m;` và `public int Get()` đọc "
            "`_m.Value` hai lần rồi trả về tổng. Hiện thực struct `Mut { public int Value; }`. Bài học: "
            "mỗi lần đọc `_m.Value` đều sao chép trước — hãy hiện thực sao cho TEST (kiểm tra tổng) "
            "đạt; bạn không thể quan sát các bản sao từ bên ngoài, và đó chính là điểm mấu chốt: "
            "chúng vô hình nhưng có thật."
        ),
        "hints": {
            "sum": "Trả về _m.Value + _m.Value.",
        },
    },
    "csa-p2-alloc-budget": {
        "title": "Đạt ngân sách cấp phát",
        "prompt": (
            "Hiện thực `static int[] Squares(int n)` trả về các bình phương 0..n-1 trong mảng MỚI, và "
            "`static int SumSquares(int n)` tính cùng tổng với KHÔNG cấp phát heap (vòng lặp thuần, "
            "cấm LINQ). Test ràng buộc: Squares cấp phát ≤ n*8+64 byte; SumSquares cấp phát đúng 0."
        ),
        "hints": {
            "values": "Squares: new int[n] rồi điền; SumSquares: cộng dồn trong vòng lặp.",
            "budget": "Một mảng n int ≈ 8n byte. SumSquares không được cấp phát cả enumerator — cấm LINQ.",
        },
    },
    "csa-checkpoint-m3-task": {
        "title": "Checkpoint generics",
        "prompt": (
            "Định nghĩa `interface IShape<TSelf> where TSelf : IShape<TSelf>` với "
            "`static abstract string Name { get; }` và `static abstract double Area(double side);`. "
            "Hiện thực `struct Square : IShape<Square>` (Area = side*side) và `struct Circle : "
            "IShape<Circle>` (Area = π·side² dùng Math.PI). Rồi hiện thực `static double "
            "AreaOf<T>(double side) where T : IShape<T> => T.Area(side);` trong lớp `Solution`."
        ),
        "hints": {
            "static-dispatch": "Tham số kiểu cung cấp các thành viên tĩnh — không instance, không reflection.",
            "no-instantiation": "Dispatch static-abstract diễn ra lúc biên dịch — không cấp phát, không instance.",
        },
    },
    "csa-p3-variance-legality": {
        "title": "Tính hợp lệ của variance",
        "prompt": (
            "Hiện thực `static string Variance(IEnumerable<object> xs)` trả về \\\"ok\\\", và chứng minh "
            "contravariance: hiện thực `static Action<string> AsObjectAction(Action<object> a) => a;` "
            "(gán Action<object> cho Action<string> hợp lệ vì T contravariant trong Action<in T>). "
            "Đồng thời hiện thực `static string First(IReadOnlyList<string> list)` trả về list[0] — "
            "IReadOnlyList<out T> là covariant."
        ),
        "hints": {
            "variance-works": "Action<in T>: bộ tiêu thụ object tiêu thụ được string. IReadOnlyList<out T>: đọc được mở rộng.",
        },
    },
    "csa-p3-comparer-contravariance": {
        "title": "Một comparer cho mọi kiểu nhỏ hơn",
        "prompt": (
            "Hiện thực `class Box { public int Weight; }` và một bộ chuyển đổi comparer contravariant: "
            "`static IComparer<Box> ByWeight() => Comparer<Box>.Create((x, y) => "
            "x.Weight.CompareTo(y.Weight));` trong lớp `Solution`. Rồi dùng nó: `static void "
            "Sort(List<Box> boxes)` sắp xếp theo Weight tăng dần tại chỗ bằng comparer."
        ),
        "hints": {
            "sort": "Comparer<T>.Create dựng IComparer<T> từ lambda; List<T>.Sort(comparer) sắp xếp tại chỗ.",
        },
    },
    "csa-p3-generic-math-sum": {
        "title": "Cộng mọi kiểu số",
        "prompt": (
            "Hiện thực `static T Sum<T>(T[] values) where T : INumber<T>` cộng mọi phần tử bắt đầu từ "
            "T.Zero, và `static T Average<T>(T[] values) where T : INumber<T>` trả về Sum / count "
            "(dùng T.CreateTruncating cho count). Chạy được cho int, double, decimal — một hiện thực "
            "duy nhất."
        ),
        "hints": {
            "int": "T.Zero khởi đầu phép gộp; dùng += qua toán tử của INumber<T>.",
            "double": "Cùng mã generic; tham số kiểu mang theo phép arithmetic của riêng nó.",
        },
    },
    "csa-checkpoint-m4-task": {
        "title": "Checkpoint closures",
        "prompt": (
            "Hiện thực `static List<Func<int>> Counters(int n)` trả về n hàm; hàm thứ i trả về giá trị "
            "i tương ứng 0,1,...,n-1 — mỗi counter phải trả về CHỈ SỐ CỦA CHÍNH NÓ (chứng minh bạn "
            "bắt đúng giá trị từng vòng lặp, không phải một biến dùng chung). Rồi hiện thực "
            "`static Func<int> Adder(int start)` trả về hàm cộng đối số vào `start` và trả về TỔNG "
            "CHẠY DẦN (trạng thái phải tồn tại qua các lần gọi — một biến cục bộ khả biến bị bắt)."
        ),
        "hints": {
            "per-iteration-capture": "Bắt một bản sao theo từng vòng lặp (biến foreach/loop theo ngữ nghĩa C# 5+).",
            "persistent-state": "Biến cục bộ bị bắt biến đổi qua các lần gọi — đó chính là trường display class của closure.",
        },
    },
    "csa-p4-capture-audit": {
        "title": "Kiểm toán capture",
        "prompt": (
            "Hiện thực `static int TotalCaptured()`: tạo 10 closure trên một biến đếm dùng chung (cả "
            "10 đều tăng CÙNG một int bị bắt), gọi mỗi hàm một lần, trả về giá trị cuối của biến đếm. "
            "Rồi hiện thực `static int TotalDistinct()` làm tương tự nhưng 10 closure mỗi cái bắt bản "
            "sao RIÊNG; gọi mỗi hàm một lần và trả về tổng của 10 bản sao (mỗi cái 1) = 10."
        ),
        "hints": {
            "shared-vs-distinct": "Dùng chung: một trường display-class tăng 10 lần → 10. Riêng biệt: 10 bản sao, mỗi cái tăng một lần → tổng 10.",
        },
    },
    "csa-p4-composition": {
        "title": "Pipeline hợp thành delegate",
        "prompt": (
            "Hiện thực `static Func<string, string> Pipeline(params Func<string, string>[] steps)` "
            "trả về một delegate áp dụng các bước trái sang phải (bước 1 trước). Rồi hiện thực "
            "`static int InvokeThrice(Func<int> f)` gọi f đúng ba lần và trả về kết quả cuối (kiểm "
            "tra delegate là giá trị hạng nhất)."
        ),
        "hints": {
            "pipeline-order": "Gộp mảng: acc = acc + step theo đúng thứ tự từng bước.",
        },
    },
    "csa-p4-mini-rules": {
        "title": "Mini rule engine",
        "prompt": (
            "Hiện thực `class RuleEngine` với `private readonly List<(string Name, "
            "Func<Dictionary<string,int>, bool>)> _rules = new();`, `public void Add(string name, "
            "Func<Dictionary<string,int>, bool> pred)` và `public List<string> "
            "Evaluate(Dictionary<string,int> ctx)` trả về tên các luật đạt theo thứ tự đăng ký. "
            "Chứng minh closure bắt ngữ cảnh theo tham chiếu tại thời điểm đánh giá."
        ),
        "hints": {
            "rules": "Các lambda bắt ctx theo tham chiếu tới đối tượng dictionary; đánh giá đọc nội dung hiện tại.",
        },
    },
    "csa-checkpoint-m5-task": {
        "title": "Checkpoint reflection",
        "prompt": (
            "Hiện thực `static List<string> PluginNames(Assembly assembly)`: tìm mọi lớp không trừu "
            "tượng trong assembly hiện thực interface `IPlugin` (định nghĩa bên dưới), gọi constructor "
            "không tham số, đọc thuộc tính `Name`, và trả về các tên đã sắp alphabet. Không cache gì — "
            "đúng đắn trước. Định nghĩa `public interface IPlugin { string Name { get; } }` trong file "
            "Solution của bạn."
        ),
        "hints": {
            "discovery": "assembly.GetTypes(), lọc typeof(IPlugin).IsAssignableFrom(t) && !t.IsAbstract, rồi Activator.CreateInstance.",
        },
    },
        "csa-p5-cached-invoke": {
        "title": "Cache lần invoke",
        "prompt": (
            "Hiện thực `static Func<object?, object?> BuildGetter(Type type, string propertyName)` "
            "trả về một DELEGATE đọc thuộc tính instance cho trước qua reflection — và delegate phải "
            "được CACHE: hai lần gọi với cùng (type, name) trả về CÙNG một thể hiện delegate, và khi "
            "gọi, delegate dùng sẵn công việc PropertyInfo đã bắt chứ không resolve lại. Thêm "
            "`static object? Read(object target, string prop) => BuildGetter(target.GetType(), prop)(target);`."
        ),
        "hints": {
            "cached-and-works": "Cache delegate trong static ConcurrentDictionary<(Type, string), Func<object?, object?>>; bắt PropertyInfo bên trong factory.",
            "allocation-profile": "Chạy GetProperty MỘT LẦN bên trong factory được cache; delegate trả về không được resolve lại theo từng lần gọi.",
        },
    },
    "csa-p5-attr-validation": {
        "title": "Xác thực dẫn dắt bởi attribute",
        "prompt": (
            "Định nghĩa `attribute RangeAttribute : Attribute` với `int Min; int Max;` (dùng cho "
            "properties). Hiện thực `static List<string> Validate(object obj)`: với mỗi thuộc tính "
            "instance mang RangeAttribute mà giá trị int nằm ngoài [Min,Max], thêm \\\"Name\\\" của thuộc "
            "tính vào kết quả. Trả về lỗi theo thứ tự khai báo. Lớp cần hỗ trợ: `Account { "
            "[Range(1,120)] public int Age; [Range(0,100)] public int Score; }` (trường, không phải "
            "thuộc tính — hãy hỗ trợ cả field lẫn property)."
        ),
        "hints": {
            "validation": "type.GetMembers(BindingFlags.Public | BindingFlags.Instance); kiểm tra "
                          "MemberInfo.GetCustomAttribute<RangeAttribute>() — xử lý cả FieldInfo và PropertyInfo.",
        },
    },
    "csa-p5-member-scan": {
        "title": "Quét assembly với flags",
        "prompt": (
            "Hiện thực `static List<string> StaticStringMembers(Type type)`: trả về tên của mọi "
            "trường VÀ thuộc tính public static kiểu string, đã sắp xếp. Rồi hiện thực `static int "
            "CountMethods(Type type, string namePrefix)` đếm phương thức public instance có tên bắt "
            "đầu bằng tiền tố (loại trừ property accessor và constructor)."
        ),
        "hints": {
            "scan": "GetFields/GetProperties với BindingFlags.Public | BindingFlags.Static; với phương thức dùng "
                    "BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly.",
        },
    },
    "csa-checkpoint-m6-task": {
        "title": "Checkpoint Roslyn",
        "prompt": (
            "Hiện thực `static string[] PublicMethodNames(string source)`: parse `source` bằng "
            "CSharpSyntaxTree.ParseText, tìm mọi node MethodDeclarationSyntax, và trả về identifier "
            "đã sắp. Rồi hiện thực `static bool Compiles(string source)`: dựng CSharpCompilation "
            "(OutputKind.DynamicallyLinkedLibrary) trên source đó với các reference từ "
            "AppDomain.CurrentDomain.GetAssemblies() lọc IsDynamic == false && Location != "
            "string.Empty, và trả về việc nó có đúng 0 diagnostic lỗi hay không."
        ),
        "hints": {
            "syntax-walk": "tree.GetRoot().DescendantNodes().OfType<MethodDeclarationSyntax>() — thu Identifier.ValueText.",
            "semantic-verify": "CSharpCompilation.Create với syntax trees + references; kiểm tra diags nơi Severity == DiagnosticSeverity.Error.",
        },
    },
    "csa-p6-syntax-count": {
        "title": "Số liệu cú pháp",
        "prompt": (
            "Hiện thực `static (int methods, int classes, int invocations) Metrics(string source)`: "
            "parse source và đếm node MethodDeclarationSyntax, ClassDeclarationSyntax, và "
            "InvocationExpressionSyntax. Đây là công cụ đo mã mà mọi linter bắt đầu với."
        ),
        "hints": {
            "counts": "DescendantNodes().OfType<T>().Count() cho từng loại node.",
        },
    },
    "csa-p6-semantic-resolve": {
        "title": "Resolve ngữ nghĩa",
        "prompt": (
            "Hiện thực `static string TypeOfExpression(string source)`: parse source (một phát biểu "
            "hoặc biểu thức đơn), lấy SemanticModel từ CSharpCompilation, tìm "
            "InvocationExpressionSyntax đầu tiên, và trả về tên kiểu đầy đủ của ContainingType của "
            "phương thức được resolve, hoặc \\\"?\\\" khi không resolve được."
        ),
        "hints": {
            "resolution": "compilation.GetSemanticModel(tree); symbol = model.GetSymbolInfo(invocation).Symbol as "
                          "IMethodSymbol; dùng symbol.ContainingType.ToDisplayString().",
        },
    },
    "csa-p6-diagnostic-scan": {
        "title": "Quét diagnostic",
        "prompt": (
            "Hiện thực `static List<string> CompilerWarnings(string source)`: biên dịch source thành "
            "library và trả về các ID (d.Id) của mọi diagnostic mức WARNING (input cho trước không có "
            "lỗi), khử trùng lặp và sắp xếp. Input phát cảnh báo ví dụ: \\\"public class A { public int "
            "X; }\\\" — CS0169 (trường không dùng) chỉ xuất hiện khi trường private và không bao giờ "
            "được dùng; trường public không cảnh báo, nên dùng \\\"public class A { int y; }\\\" cho trường "
            "hợp cảnh báo."
        ),
        "hints": {
            "warnings": "GetDiagnostics() trả về cả cảnh báo lẫn lỗi; lọc Severity == Warning; Distinct().OrderBy().ToList().",
        },
    },
    "csa-checkpoint-m7-task": {
        "title": "Checkpoint source generator",
        "prompt": (
            "Hiện thực `static (int trees, bool symbolResolved) RunGenerator(string userSource)`: "
            "dựng một generator đọc các lớp đánh dấu `[Gen]` (attribute do chính generator tạo qua "
            "RegisterPostInitializationOutput) và phát ra lớp static `GenCatalog` với một phương thức "
            "cho mỗi lớp được đánh dấu: `public static string Name_X() => \\\"X\\\";`. Parse userSource, "
            "thêm source attribute, chạy CSharpGeneratorDriver, và trả về (số tree sinh ra gồm cả init "
            "output, symbol `GenCatalog` có resolve trong output compilation hay không)."
        ),
        "hints": {
            "generation": "CSharpGeneratorDriver.Create(gen).RunGeneratorsAndUpdateCompilation(comp, out var output, "
                          "out _); kiểm tra output.GetTypeByMetadataName(\\\"GenCatalog\\\").",
        },
    },
    "csa-p7-emitted-source": {
        "title": "Phát source sạch từ generator",
        "prompt": (
            "Hiện thực `static string EmitDto(string className, (string Name, string Type)[] fields)` "
            "trả về một chuỗi source C# hoàn chỉnh, biên dịch được, cho `public sealed record "
            "{className}(...)` với các trường cho trước — dùng kiểu ĐỦ ĐƯỜNG DẪN cho loại không phải "
            "primitive (ví dụ System.DateTime) để output biên dịch mà không cần usings. Primitive "
            "(int, string, bool, double) giữ nguyên."
        ),
        "hints": {
            "compiles-without-usings": "Mã sinh ra không được phụ thuộc usings xung quanh — phát tên đủ đường dẫn cho mọi thứ "
                                       "không phải từ khóa primitive.",
            "primitives-stay-short": "Giữ một bảng ánh xạ từ khóa cho primitive; chỉ qualify phần còn lại.",
        },
    },
        "csa-p7-generator-compile": {
        "title": "Xác minh pipeline biên dịch được",
        "prompt": (
            "Hiện thực `static bool GeneratedCatalogCompiles(string userSource)`: dựng pipeline "
            "generator trong đó Gen2Attribute (do chính generator phát qua RegisterPostInitializationOutput, "
            "AttributeTargets.Class) đánh dấu lớp, và lớp tĩnh GenCatalog2 được sinh ra với một method cho "
            "mỗi lớp được đánh dấu. Chỉ trả về true khi OUTPUT compilation — cả mã người dùng LẪN mã sinh "
            "ra — không còn diagnostic lỗi. Test chứng minh việc kiểm tra output là cần thiết: một lớp người "
            "dùng tên GenCatalog2 xung đột với kiểu được sinh ra và phải trả về false."
        ),
        "hints": {
            "end-to-end": "RunGeneratorsAndUpdateCompilation đưa cho bạn OUTPUT compilation — GetDiagnostics() trên nó "
                          "bao phủ cả cây được sinh ra. Chỉ nhìn genDiags là chưa đủ.",
        },
    },
    "csa-checkpoint-m8-task": {
        "title": "Checkpoint expression tree",
        "prompt": (
            "Hiện thực `static Expression<Func<int, bool>> BuildPredicate(int threshold)` trả về biểu "
            "thức tương đương `x => x >= threshold && x % 2 == 0` (dựng bằng chương trình, bắt "
            "threshold). Rồi hiện thực `static string Describe(Expression<Func<int, bool>> e)` trả về "
            "NodeType của body (ví dụ \\\"AndAlso\\\")."
        ),
        "hints": {
            "built-predicate": "Expression.Parameter(typeof(int), \\\"x\\\"), rồi GreaterThanOrEqual, Modulo, Equal, AndAlso; "
                               "bọc trong Lambda<Func<int,bool>>.",
            "inspection": "e.Body.NodeType.ToString().",
        },
    },
        "csa-p8-constant-fold": {
        "title": "Visitor gấp hằng số",
        "prompt": (
            "Hiện thực `class FoldVisitor : ExpressionVisitor` thay mọi BinaryExpression có hai toán hạng "
            "Constant bằng một Constant của giá trị tính được (chỉ int; hỗ trợ Add, Multiply, Subtract). "
            "Việc gấp phải ĐỆ QUY: khi các node nhị phân bên trong gấp thành hằng số thì node nhị phân bao "
            "ngoài cũng gấp theo. Test dựng cây bằng các lời gọi Expression.* tường minh vì compiler đã tự gấp hằng số trong lambda literal lúc biên dịch — x => 2 + 3 + x đến tay visitor dưới dạng (5 + x), không còn gì để gấp. Rồi hiện thực `static Expression<Func<int,int>> "
            "FoldExpr(Expression<Func<int,int>> e)` trả về biểu thức đã được duyệt (đã gấp)."
        ),
        "hints": {
            "folds": "Ghi đè VisitBinary: Visit các toán hạng TRƯỚC, rồi nếu cả hai là hằng int thì trả về "
                     "Expression.Constant(kết quả) — đệ quy khiến (2+3) gấp trước khi Add bên ngoài nhìn thấy nó.",
        },
    },
    "csa-p8-mini-provider": {
        "title": "Mini query provider",
        "prompt": (
            "Hiện thực `static string Translate(Expression<Func<int, bool>> predicate)` đi bộ cây và "
            "sinh mệnh đề WHERE pseudo-SQL: GreaterThanOrEqual → \\\">=\\\", LessThan → \\\"<\\\", Equal → "
            "\\\"=\\\", AndAlso → \\\"AND\\\", OrElse → \\\"OR\\\", tham số in là \\\"x\\\" và hằng in là giá trị. Ví dụ: x "
            ">= 5 in \\\"x >= 5\\\"; (x >= 5) AND (x < 100) in \\\"x >= 5 AND x < 100\\\"."
        ),
        "hints": {
            "translation": "Kế thừa ExpressionVisitor hoặc pattern-match body: BinaryExpression với NodeType và "
                           "ConstantExpression phía phải.",
        },
    },
        "csa-p8-compile-cache": {
        "title": "Biên dịch một lần, cache mãi mãi",
        "prompt": (
            "Hiện thực `static Func<int, bool> CachedCheck(int threshold)` biên dịch predicate "
            "`x => x >= threshold && x % 2 == 0` CHO threshold cho trước và cache delegate trong static "
            "ConcurrentDictionary<int, Func<int, bool>>. Test chứng minh việc biên dịch xảy ra đúng một "
            "lần: lần gọi THỨ HAI với cùng threshold phải trả về CÙNG một thể hiện delegate "
            "(ReferenceEquals), gọi delegate đã cache không cấp phát gì, và biên giới phải chính xác — "
            "CachedCheck(10) chấp nhận 10."
        ),
        "hints": {
            "same-instance": "GetOrAdd trên static ConcurrentDictionary; dựng + compile chỉ bên trong factory.",
            "no-alloc-per-call": "Sau khi cache, gọi hàm chỉ là một delegate call thuần — không cấp phát.",
        },
    },
    "csa-checkpoint-m9-task": {
        "title": "Checkpoint async",
        "prompt": (
            "Hiện thực `static async ValueTask<int> ReadCachedAsync(int key, Func<int, Task<int>> "
            "slowFetch)`: static ConcurrentDictionary<int,int> cache; khi trúng trả về đồng bộ mà "
            "KHÔNG await (fast path của ValueTask); khi trượt thì await slowFetch và lưu kết quả. Rồi "
            "hiện thực `static async Task<string> WithTimeout(Task<string> work, TimeSpan timeout)` "
            "trả về kết quả của work hoặc ném TimeoutException — dùng CancellationTokenSource với "
            "timeout, và hủy token đã link."
        ),
        "hints": {
            "cache-fast-path": "TryGetValue trước — trả về new ValueTask<int>(value) mà không đụng fetcher.",
            "timeout-fires": "cts.CancelAfter(timeout); await task.WaitAsync(cts.Token) rồi chuyển OperationCanceledException thành TimeoutException.",
        },
    },
    "csa-p9-token-link": {
        "title": "Hủy liên kết (linked cancellation)",
        "prompt": (
            "Hiện thực `static async Task<int> RaceTask(Task<int> a, Task<int> b, CancellationToken "
            "external)` trả về task nào trong a/b hoàn thành trước — và phải ngừng chờ khi external "
            "hủy, ném OperationCanceledException. Dùng "
            "CancellationTokenSource.CreateLinkedTokenSource và Task.WhenAny với đăng ký hủy."
        ),
        "hints": {
            "race-external-cancel": "Link token; đăng ký callback hoàn thành một TaskCompletionSource, WhenAny trên cả hai task "
                                    "cộng task TCS đó.",
            "race-fast-wins": "WhenAny trả về task hoàn thành đầu tiên; trả kết quả của nó.",
        },
    },
    "csa-p9-async-stream": {
        "title": "Pipeline async stream",
        "prompt": (
            "Hiện thực `static async IAsyncEnumerable<int> MultiplyAsync(IAsyncEnumerable<int> source, "
            "int factor)` yield từng phần tử nhân factor, và `static async Task<List<int>> "
            "Collect(IAsyncEnumerable<int> source)` hiện thực hóa stream thành list. Dựng source bằng "
            "async iterator yield 1,2,3 với `await Task.Yield()` giữa các phần tử."
        ),
        "hints": {
            "pipeline": "await foreach (var item in source.ConfigureAwait(false)) — nhân rồi yield return.",
        },
    },
    "csa-p9-value-task-bug": {
        "title": "Chẩn đoán lỗi ValueTask",
        "prompt": (
            "ValueTask có luật nghiêm ngặt: await đúng một lần, không bao giờ await sau khi đã tiêu "
            "thụ, không bao giờ await đồng thời. Hiện thực `static async ValueTask<int> "
            "SafeDouble(ValueTask<int> source)` ĐÚNG: await source một lần và trả kết quả nhân 2. Rồi "
            "hiện thực `static async Task<int> BrokenDouble(ValueTask<int> source)` minh họa mẫu bị "
            "cấm — await hai lần (`var a = await source; var b = await source; return a + b;`). Test "
            "chạy bản SAI trên ValueTask được nâng bởi IValueTaskSource tạo qua "
            "ManualResetValueTaskSourceCore để chứng minh nó ném lỗi/hành xử sai."
        ),
        "hints": {
            "safe-works": "var v = await source; return v * 2.",
        },
    },
    "csa-checkpoint-m10-task": {
        "title": "Checkpoint concurrency",
        "prompt": (
            "Sửa race trên biến đếm: hiện thực `static long CountUnique(int[] values)` trả về số giá "
            "trị phân biệt dùng ConcurrentDictionary như một tập atomic — test dồn 8 task song song "
            "để chứng minh không mất cập nhật. Rồi hiện thực `static bool "
            "TryAddIfAbsent(ConcurrentDictionary<string,int> d, string key, Func<string,int> compute)` "
            "thêm giá trị tính được một cách atomic CHỈ khi key vắng mặt — đúng một lần kể cả khi "
            "các lời gọi song song (không tính hai lần)."
        ),
        "hints": {
            "no-lost-update": "CountUnique có thể dùng worker Parallel/Task, nhưng thao tác trên dictionary dùng chung phải atomic "
                              "(GetOrAdd/TryUpdate), không bao giờ check-then-act.",
            "compute-once": "Factory của GetOrAdd có thể chạy hai lần mà không publish hai lần — cần TryGetValue trước, rồi "
                            "GetOrAdd, rồi so sánh bên nào thắng... hoặc dùng cờ Lazy<int> để tính trùng vô hại nhưng publish vẫn atomic.",
        },
    },
    "csa-p10-volatile": {
        "title": "Chứng minh bug khả kiến",
        "prompt": (
            "Hiện thực `static int SpinUntilFlag(int ms)` busy-wait (vòng lặp Thread.Sleep(1), giới "
            "hạn trong ms) cho đến khi static bool `Flag` — do `static void SetFlag()` đặt — thành "
            "true, trả về 1 nếu thấy, 0 khi hết giờ — nhưng đọc Flag qua `Volatile.Read` để JIT không "
            "thể cache nó trong thanh ghi. Test đặt cờ từ luồng khác giữa chừng và mong thành công."
        ),
        "hints": {
            "cross-thread-flag": "while (!Volatile.Read(ref Flag) && Stopwatch chưa hết ngân sách) Thread.Sleep(1); static bool Flag "
                                 "là trường tĩnh — Volatile.Read(ref Flag) cần dạng ref: khai báo `private static bool _flag;` "
                                 "cùng bộ API Volatile, hoặc để SetFlag/Spin dùng private static bool qua các API Volatile.",
        },
    },
    "csa-p10-deadlock-diagnose": {
        "title": "Xử triệt deadlock",
        "prompt": (
            "Hiện thực `static int SafeTransfer(Account a, Account b, int amount)` chuyển `amount` từ "
            "a sang b bằng `Monitor.TryEnter` với timeout trên cả hai khóa, thu nhận theo THỨ TỰ NHẤT "
            "QUAN (theo account id) nên không bao giờ deadlock — nhả khóa sạch trên mọi nhánh. Hiện "
            "thực `static void UnsafeTransfer(...)` cách ngây thơ (lock a rồi lock b, theo thứ tự đối "
            "số) để minh họa ABBA deadlock mà bài học lập bảng. SafeTransfer trả 1 khi thành công, 0 "
            "khi hết giờ."
        ),
        "hints": {
            "safe-transfer": "Xếp theo Id: first = a.Id < b.Id ? a : b; TryEnter(first, 1000); TryEnter(second, 1000); "
                             "finally nhả cả hai.",
            "funds-guarded": "Kiểm tra a.Balance < amount BÊN TRONG cặp khóa và thoát với 0 trước mọi Debit.",
            "reverse-direction-safe": "Cùng thứ tự khóa bất kể thứ tự đối số — đó là toàn bộ bản sửa.",
        },
    },
    "csa-checkpoint-m11-task": {
        "title": "Checkpoint parallel",
        "prompt": (
            "Hiện thực `static long SumSquaresParallel(int[] data, int threshold)` tính tổng bình "
            "phương — tuần tự khi data.Length <= threshold, song song khi ngược lại, bằng Parallel.For "
            "với tổng theo luồng (combine cuối bằng Interlocked). Rồi hiện thực `static int[] "
            "SquaresParallel(int[] data)` trả về bình phương THEO THỨ TỰ GỐC qua PLINQ (AsOrdered). "
            "Test so cả hai với kết quả tuần tự và khẳng định bản song song của mảng 10 triệu phần tử "
            "nhanh hơn baseline tuần tự bị cố ý làm chậm (chi phí giả mỗi phần tử)."
        ),
        "hints": {
            "sum-correct": "Parallel.For với localInit: () => 0L, body: (i, state, local) => local + "
                           "(long)data[i]*data[i], localFinally: local => Interlocked.Add(ref total, local).",
            "plinq-ordered": "data.AsParallel().AsOrdered().Select(x => x * x).ToArray() — thiếu AsOrdered, PLINQ gộp lệch thứ tự.",
        },
    },
        "csa-p11-parallel-cancel": {
        "title": "Quét song song có hủy",
        "prompt": (
            "Hiện thực `static int FirstMatch(int[] data, Func<int, bool> predicate, int workers)` tìm chỉ "
            "số đầu tiên (i thấp nhất) mà predicate(data[i]) đúng, chạy quét theo chunk song song — dùng "
            "Parallel.For với 'chỉ số tìm thấy' dùng chung được bảo vệ bởi Interlocked.CompareExchange nên "
            "chỉ chỉ số THẤP HƠN mới thắng, và dừng các vòng lặp còn lại khi đã tìm thấy (loopState.Stop()). "
            "Trả về -1 nếu vắng mặt. Test đếm số lần gọi predicate: không có Stop() thì cả 10 triệu "
            "lần đều chạy cho match ở chỉ số 5 — test yêu cầu dưới 1 triệu lần gọi."
        ),
        "hints": {
            "first-match": "Interlocked.CompareExchange(ref best, i, int.MaxValue) chỉ thắng khi best vẫn là MaxValue HOẶC i thấp "
                           "hơn — vòng CAS giữ giá trị nhỏ nhất.",
            "absent": "Cùng vòng lặp; không CAS nào thành công.",
            "early-exit": "Sau khi CAS thắng, gọi loopState.Stop() để Parallel.For ngừng điều phối các iteration tiếp theo — test đếm số lần gọi predicate và quét hết là 10.000.000 lần.",
        },
    },
    "csa-p11-amdahl": {
        "title": "Định luật Amdahl, đo được",
        "prompt": (
            "Một pipeline có phần song song hóa P và tỉ lệ tuần tự S (S + P = 1). Hiện thực `static "
            "double Speedup(double serialFraction, int cores)` trả về speedup Amdahl S(n) = 1 / (S + "
            "P/n) — và `static int BreakEvenCores(double serialFraction, double minSpeedup)` trả về "
            "số core nhỏ nhất mà speedup đạt minSpeedup (trả -1 nếu không số core hữu hạn nào đạt "
            "được). Test kiểm tra trần cứng: với 10% công việc tuần tự, không bao nhiêu core cũng "
            "không vượt 10x."
        ),
        "hints": {
            "amdahl-values": "Speedup = 1/(S + (1-S)/n). BreakEven: giải 1/(S + (1-S)/n) >= target theo n, làm tròn lên — trừ khi "
                             "S*target >= 1, khi đó không thể đạt (-1).",
        },
    },
    "csa-checkpoint-m12-task": {
        "title": "Checkpoint Channels",
        "prompt": (
            "Hiện thực `static async Task<int> PumpAsync(ChannelReader<int> source, "
            "ChannelWriter<int> sink, int factor, CancellationToken ct)` đọc mọi phần tử từ source, "
            "ghi item*factor vào sink, và hoàn thành sink khi xong — lan truyền hủy. Rồi hiện thực "
            "`static async Task<List<int>> RunBounded(int count)`: tạo bounded channel (sức chứa 8), "
            "một producer ghi 0..count-1 rồi hoàn thành, và một consumer duy nhất gom qua "
            "ReadAllAsync. Test xác minh dòng chảy end-to-end và output của consumer là đầy đủ."
        ),
        "hints": {
            "pump": "await foreach (var item in source.ReadAllAsync(ct)) await sink.WriteAsync(item * factor, ct); "
                    "finally sink.Complete().",
            "bounded-drain": "Bounded(capacity: 8); producer: for-loop WriteAsync rồi TryComplete; consumer: await foreach "
                             "ReadAllAsync vào list.",
        },
    },
    "csa-p12-fanout": {
        "title": "Fan-out worker",
        "prompt": (
            "Hiện thực `static async Task<int[]> FanOut(int itemCount, int workers)` nơi itemCount "
            "công việc (giá trị = chỉ số) chảy qua một channel và `workers` task tiêu thụ đồng thời "
            "mỗi cái kéo phần tử và tính index * 2, ghi kết quả vào list an-toàn-luồng dùng chung. "
            "Mọi phần tử phải được xử lý đúng một lần (consumer cạnh tranh trên một channel), và "
            "phương thức trả về kết quả đã sắp. Test chạy workers=4 trên 1000 phần tử và khẳng định "
            "tính đầy đủ lẫn duy nhất."
        ),
        "hints": {
            "exactly-once": "Một channel, N consumer mỗi cái `await foreach (var i in reader.ReadAllAsync())` — channel bảo đảm "
                            "mỗi phần tử đến đúng một reader.",
        },
    },
    "csa-p12-drain": {
        "title": "Xả dữ liệu khi tắt lịch sự",
        "prompt": (
            "Worker phải NGỪNG NHẬN công việc mới ngay khi tắt, nhưng làm nốt những gì đã nhận. "
            "Hiện thực `static async Task<List<int>> ShutdownDrain(int feedCount, int shutdownAfter)`: "
            "producer ghi các số nguyên 0..feedCount-1; sau khi `shutdownAfter` phần tử đã được GHI, "
            "producer gọi TryComplete (không nhận thêm) — nhưng mọi phần tử đã ghi trước khi hoàn "
            "thành vẫn phải được tiêu thụ bởi reader nền gom qua ReadAllAsync. Trả về danh sách đã "
            "gom. Test khẳng định đúng shutdownAfter phần tử đến, không hơn."
        ),
        "hints": {
            "drain-exact": "Trong vòng producer: nếu (i == shutdownAfter - 1) thì sau khi WriteAsync(i) gọi TryComplete. Các phần "
                           "tử đã vào buffer vẫn được ReadAllAsync giao sau khi hoàn thành.",
        },
    },
    "csa-checkpoint-m13-task": {
        "title": "Checkpoint GC",
        "prompt": (
            "Hiện thực `static long MeasureAlloc<T>(Func<T> factory, int iterations)` trả về chênh "
            "lệch GC.GetAllocatedBytesForCurrentThread() qua `iterations` lần gọi factory — đầu dò "
            "cấp phát vi mô chuẩn. Rồi hiện thực `static int Gen0Collections()` trả về "
            "GC.CollectionCount(0), và `static WeakReference MakeWeak()` trả về WeakReference tới một "
            "object() mới cấp phát. Test: 1000 lần `new byte[64]` phải cấp phát NHIỀU HƠN 1000*64 "
            "byte; Target của weak reference phải thành null sau GC.Collect + WaitForPendingFinalizers "
            "+ GC.Collect (mẫu helper-method về liveness mà bài học dạy)."
        ),
        "hints": {
            "allocation-probe": "GC.GetAllocatedBytesForCurrentThread() chính xác cho luồng hiện tại — chụp trước/sau, không có "
                                "cấp phát nào xen giữa.",
            "weak-ref-death": "MakeWeak phải trả WeakReference mà KHÔNG giữ local còn sống: `var o = new object(); var wr = new "
                              "WeakReference(o); return wr;` — object không được nằm trong thanh ghi khi caller thu gom "
                              "(mẫu helper method + return).",
            "gc-counts-exposed": "return GC.CollectionCount(0) — đơn điệu tăng theo định nghĩa; vòng lặp chỉ tạo áp lực.",
        },
    },
    "csa-p13-event-leak": {
        "title": "Chẩn đoán rò rỉ event",
        "prompt": (
            "Đăng ký event neo giữ subscriber của nó: publisher sống lâu giữ các subscriber ngắn hạn "
            "là rò rỉ kinh điển của .NET. Hiện thực `static int AliveAfterUnsubscribe()`: tạo một "
            "Publisher, tạo 100 Subscriber mỗi cái đăng ký Publisher.Tick, trả về 100; rồi hiện thực "
            "`static void UnsubscribeAll(Publisher p, List<Subscriber> subs)` gọi Dispose trên từng cái "
            "(subscriber hiện thực IDisposable và hủy đăng ký trong Dispose). Test xác minh sau Dispose "
            "+ GC.Collect x2, WeakReference tới subscriber đã chết — chứng minh hủy đăng ký cắt gốc."
        ),
        "hints": {
            "unsubscribe-breaks-root": "Subscriber.Dispose phải làm p.Tick -= OnTick; chính phép -= cắt gốc publisher→subscriber.",
        },
    },
    "csa-p13-arraypool": {
        "title": "Kỷ luật ArrayPool",
        "prompt": (
            "Hiện thực `static long PooledSum(int[] values)` sao chép `values` qua buffer thuê từ "
            "ArrayPool (thuê byte[] ít nhất 4*values.Length, cộng các int đầu tiên theo nhóm 4 byte "
            "little-endian, trả về tổng, TRẢ mảng về pool trong finally). Rồi hiện thực `static long "
            "DirectSum(int[] values)` chỉ cộng trực tiếp. Cả hai phải trả kết quả giống nhau; bản "
            "pooled không được cấp phát mảng mới mỗi lần gọi (test gọi 100 lần và kiểm tra chênh lệch "
            "GC rất nhỏ)."
        ),
        "hints": {
            "sums-match": "Buffer.BlockCopy(vals, 0, rented, 0, vals.Length * 4); rồi cộng các int theo bước 4 byte qua "
                          "BitConverter hoặc view int[].",
            "pooled-no-alloc": "ArrayPool<byte>.Shared.Rent/Return trong try/finally — thuê bucket TỐI THIỂU, trả về mà không "
                               "clear trừ khi pool yêu cầu.",
        },
    },
}
