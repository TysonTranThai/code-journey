"""VI overlays for C# Advanced challenges — modules 14–24 (m14…m24).

Keys are challenge ids; values: {"title", "prompt", "hints": {test_name: hint}}.
Code identifiers, signatures, and error messages stay in English per the
localization contract (same as Beginner/Intermediate).
"""

VI: dict[str, dict] = {
    "csa-checkpoint-m14-task": {
        "title": "Checkpoint hiệu năng",
        "prompt": (
            "Hai hiện thực được cung cấp trong harness: SlowPath nối chuỗi trong vòng lặp; FastPath "
            "dùng string.Create. Hiện thực `static string RepeatChar(char c, int n)` dựng một chuỗi "
            "n ký tự `c` bằng string.Create (không cấp phát trung gian), và `static long "
            "Measure(Func<int> work, int iterations)` trả về tổng byte cấp phát qua `iterations` lần "
            "gọi với MỘT lần warmup trước (warmup được chấm điểm: thiếu nó, cấp phát lần gọi đầu của "
            "JIT làm hỏng kết quả)."
        ),
        "hints": {
            "repeat-correct": "string.Create(n, c, static (span, state) => span.Fill(state));",
            "zero-intermediates": "string.Create chỉ cấp phát buffer CUỐI. Nối bằng += hoặc StringBuilder tạo nhiều tầng trung gian.",
            "measure-warms-up": "Gọi work() một lần trước khi chụp baseline cấp phát.",
        },
    },
    "csa-p14-boxing-hunt": {
        "title": "Săn boxing ẩn",
        "prompt": (
            "Hiện thực `static long SumInterface(IEnumerable<int> values)` (cộng qua foreach trên "
            "interface — cấp phát enumerator + boxing nếu đi qua IEnumerable) và `static long "
            "SumSpan(int[] values)` (cộng qua Span<int> — không cấp phát). Test chứng minh khoảng "
            "cách cấp phát: SumSpan phải cấp phát 0 qua 100 lần chạy; chi phí của SumInterface được "
            "in ra để so sánh. Hiện thực cả hai cho đúng, và chính con số dạy bài học."
        ),
        "hints": {
            "values-match": "foreach trên mảng qua IEnumerable box một IEnumerator<int>; foreach trên span dùng ref iteration.",
            "span-zero-alloc": "foreach (var v in values.AsSpan()) — chẳng có đối tượng enumerator nào tồn tại.",
        },
    },
    "csa-p14-linq-vs-loop": {
        "title": "LINQ vs vòng lặp: phán quyết đo được",
        "prompt": (
            "Hiện thực `static int CountEvenLinq(int[] values)` (values.Count(x => x % 2 == 0)) và "
            "`static int CountEvenLoop(int[] values)` (vòng for thuần). Cả hai phải trả cùng một số "
            "đếm. Rồi hiện thực `static long AllocDelta(Func<int[]> work, int iterations)` — warmup + "
            "chênh lệch cấp phát theo luồng — và dùng nó trong test để so sánh cấp phát của CẢ HAI bộ "
            "đếm. Insight được chấm điểm: với workload này vòng lặp cấp phát 0; ghi chú chi phí LINQ "
            "trong comment hiện thực."
        ),
        "hints": {
            "same-count": "Cả hai đếm x % 2 == 0; bản vòng lặp dùng for và một biến đếm.",
            "loop-zero-alloc": "for theo chỉ số; không enumerator, không closure.",
        },
    },
    "csa-checkpoint-m15-task": {
        "title": "Checkpoint CLR internals",
        "prompt": (
            "Hiện thực `static (string ilName, bool isSealed, int methodCount) Inspect<T>()` bằng "
            "reflection: trả về tên đầy đủ của kiểu, có sealed không, và số phương thức instance "
            "khai báo. Rồi hiện thực `static string DispatchDescription(Type t)` trả về đúng "
            "\\\"virtual\\\" nếu t có phương thức virtual (khai báo, instance), \\\"interface\\\" nếu nó hiện "
            "thực interface nào, ngược lại \\\"direct\\\". Insight được chấm điểm: typeof(List<int>) báo "
            "cùng lúc sealed, virtual, và interface."
        ),
        "hints": {
            "inspect-sealed": "typeof(T).FullName, .IsSealed, .GetMethods(BindingFlags.Public | BindingFlags.Instance | "
                              "BindingFlags.DeclaredOnly).Length.",
            "dispatch-desc": "GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | "
                             "BindingFlags.DeclaredOnly).Any(m => m.IsVirtual); GetInterfaces().Length > 0.",
        },
    },
    "csa-p15-exception-cost": {
        "title": "Chi phí exception, đo được",
        "prompt": (
            "Hiện thực `static long ThrowCatchCost(int iterations)`: chụp Stopwatch ticks cho "
            "`iterations` chu kỳ throw+catch của một thể hiện exception tạo sẵn (throw ex; bên trong "
            "try, catch { }) và trả về số mili giây trôi qua. Rồi hiện thực `static long "
            "ErrorCodeCost(int iterations)` làm cùng công việc nhưng trả về -1 thay vì ném (luồng "
            "kiểm tra, cùng hình dạng vòng lặp). Hiện thực `static int Divide(int a, int b)` ném "
            "DivideByZeroException khi b==0 — test dùng một lần để xác minh nhánh exception hoạt động."
        ),
        "hints": {
            "divide-throws": "if (b == 0) throw new DivideByZeroException(); return a / b.",
            "costs-measured": "Tạo exception MỘT LẦN (new Exception() ngoài vòng lặp); Stopwatch.StartNew() → vòng lặp → "
                              ".ElapsedMilliseconds.",
        },
    },
    "csa-p15-generic-runtime": {
        "title": "Chuyên biệt hóa generic lúc chạy",
        "prompt": (
            "Generic trên value type được chuyên biệt hóa theo từng kiểu; trên reference type dùng "
            "chung một instantiation. Chứng minh phần quan sát được: hiện thực `static int "
            "OpenGenericCount()` trả về số open generic type definition tiếp cận được qua "
            "typeof(Dictionary<,>) (0 nếu đã constructed, 1 nếu open) — hiện thực là: "
            "`typeof(Dictionary<,>).IsGenericTypeDefinition ? 1 : 0`. Rồi hiện thực `static bool "
            "SameRuntimeType<A, B>() => typeof(A) == typeof(B)` và test kiểm tra "
            "SameRuntimeType<List<int>, List<int>>() là true còn SameRuntimeType<List<int>, "
            "List<string>>() là false."
        ),
        "hints": {
            "open-generic": "IsGenericTypeDefinition trên typeof(Dictionary<,>) chưa gắn; typeof(A) == typeof(B) là so sánh "
                            "tham chiếu trên runtime type.",
        },
    },
    "csa-m16-checkpoint-lesson-task": {
        "title": "Checkpoint chẩn đoán",
        "prompt": (
            "Hiện thực `static string Describe(Exception ex)` sinh một dòng chẩn đoán: \\\"<TypeName>: "
            "<Message> | caused by: <TypeName>: <Message> | ...\\\" đi theo chuỗi InnerException tới gốc, "
            "nối bằng \\\" | caused by: \\\". Rồi hiện thực `static (int depth, string rootType) "
            "Analyze(Exception ex)` trả về độ sâu chuỗi inner-exception (0 khi không có inner) và tên "
            "kiểu của exception gốc. Kỹ năng được chấm điểm: không bao giờ làm mất nguyên nhân gốc "
            "chôn trong chuỗi AggregateException/InnerException."
        ),
        "hints": {
            "describe-chain": "Đi ex → ex.InnerException → null, nối mỗi \\\"type: message\\\" bằng \\\" | caused by: \\\".",
            "analyze-depth": "Đếm bước tới khi InnerException == null; ghi GetType().Name của exception cuối.",
        },
    },
    "csa-p16-circuit-breaker": {
        "title": "Máy trạng thái circuit breaker",
        "prompt": (
            "Hiện thực lớp `CircuitBreaker(int failureThreshold, TimeSpan openDuration)` với phương "
            "thức `bool TryExecute(Action action)`: CLOSED thì thực thi và đếm lỗi liên tiếp (reset "
            "khi thành công); chạm ngưỡng thì mở trong openDuration (TryExecute trả false ngay lập "
            "tức khi đang mở); hết thời gian thì chuyển HALF-OPEN, cho một lần thử — thành công thì "
            "đóng lại, thất bại thì mở lại. Hiện thực `string State` trả về \\\"closed\\\", \\\"open\\\", hoặc "
            "\\\"half-open\\\"."
        ),
        "hints": {
            "opens-and-resets": "Theo dõi _state, _consecutiveFailures, _openedAt. Trong TryExecute: nếu open và now < "
                                "openedAt+duration → false; nếu open và đã hết hạn → state=half-open, cho một lần thử.",
            "half-open-fails-reopens": "Lần dò half-open thất bại: reset _openedAt, state=open.",
        },
    },
    "csa-p16-retry-backoff": {
        "title": "Retry với exponential backoff",
        "prompt": (
            "Hiện thực `static async Task<int> RetryAsync(Func<int> attempt, int maxAttempts, int "
            "baseDelayMs)` gọi attempt() tối đa maxAttempts lần: thành công thì trả giá trị; thất bại "
            "thì await Task.Delay(baseDelayMs * 2^attemptIndex) trước lần thử kế (attemptIndex bắt đầu "
            "từ 0). Hết lượt thì ném InvalidOperationException. Test đếm số lần thử và xác minh delay "
            "tăng dần: chạy maxAttempts=3 với hàm luôn thất bại — tổng thời gian phải ít nhất "
            "baseDelayMs + 2*baseDelayMs."
        ),
        "hints": {
            "succeeds-eventually": "for (int i = 0; i < maxAttempts; i++) { try { return attempt(); } catch when (i < maxAttempts - "
                                   "1) { await Task.Delay(baseDelayMs << i); } } — rồi ném.",
            "backoff-timing": "Delay trước lần thử 2 và 3: 30 * 2^0 = 30, rồi 30 * 2^1 = 60. Tổng chờ 90ms.",
        },
    },
    "csa-checkpoint-m17-task": {
        "title": "Checkpoint unsafe",
        "prompt": (
            "Hiện thực `static int UnsafeSum(ReadOnlySpan<int> values)` cộng một span int bằng con trỏ "
            "unsafe: `fixed (int* p = values)` (hoặc trong unsafe method trên span qua "
            "GetPinnableReference), đi bằng p[i], cộng dồn. Test xác minh đúng đắn VÀ việc nó chỉ "
            "biên dịch nhờ harness thêm -unsafe (cùng cờ mà dự án thật cấu hình). Rồi hiện thực "
            "`static byte[] Reinterpret(long value)` diễn giải lại byte của một long thành mảng ushort "
            "4 phần tử (bản sao) bằng Unsafe/MemoryMarshal — minh họa reinterpretation không cần con trỏ."
        ),
        "hints": {
            "unsafe-sum": "unsafe { fixed (int* p = values) { for (int i = 0; i < values.Length; i++) sum += p[i]; } }",
            "reinterpret": "var src = MemoryMarshal.CreateReadOnlySpan(ref value, 1); var dst = MemoryMarshal.AsBytes(src); "
                           "rồi đọc hai ushort — hoặc gọn hơn: MemoryMarshal.Cast<long, ushort>(new Span<long>(ref value, "
                           "1)).ToArray()",
        },
    },
    "csa-p17-pointer-copy": {
        "title": "Sao chép bằng con trỏ với pinning có giới hạn",
        "prompt": (
            "Hiện thực `static void CopyBytes(byte[] src, int srcOffset, byte[] dst, int dstOffset, "
            "int count)` bằng con trỏ unsafe với `fixed` — pin CẢ HAI mảng cho lần sao chép. Test "
            "đúng đắn thực hiện các bản sao không chồng lấn tại các offset; bài học: pin hẹp (chỉ "
            "trong khối fixed), không bao giờ lưu con trỏ, không bao giờ để chúng thoát ra ngoài."
        ),
        "hints": {
            "copy-correct": "fixed (byte* ps = src) fixed (byte* pd = dst) { for (int i = 0; i < count; i++) "
                            "pd[dstOffset + i] = ps[srcOffset + i]; }",
            "empty-count": "Điều kiện vòng for tự xử lý; fixed trên đoạn rỗng là hợp lệ.",
        },
    },
    "csa-p17-marshal-cast": {
        "title": "Diễn giải lại struct",
        "prompt": (
            "Hiện thực struct `Packet { public uint Header; public uint Payload; }` và `static uint[] "
            "ReadPacketBytes(byte[] bytes)` diễn giải lại một đoạn 8 byte thành Packet qua "
            "MemoryMarshal.Read<Packet> — trả về [Header, Payload] dưới dạng mảng uint. Test nạp byte "
            "little-endian và xác minh giá trị trường; bài học: reinterpretation phụ thuộc layout và "
            "chẳng bao giờ thay thế được một parser thật."
        ),
        "hints": {
            "packet-fields": "MemoryMarshal.Read<Packet>(bytes.AsSpan(0, 8)) rồi return [p.Header, p.Payload].",
        },
    },
    "csa-checkpoint-m18-task": {
        "title": "Checkpoint triển khai/AOT",
        "prompt": (
            "Hiện thực `static string DeploymentDescription(bool selfContained, bool trimmed, bool "
            "aot)`: trả về \\\"framework-dependent\\\" khi selfContained=false; \\\"self-contained\\\" khi "
            "selfContained && !trimmed && !aot; \\\"trimmed\\\" khi selfContained && trimmed && !aot; "
            "\\\"aot\\\" khi aot (bất kể trimmed — AOT hàm ý nó). Rồi hiện thực `static bool "
            "IsTrimCompatible(string reflectionPattern)` trả về false với các mẫu linker không chứng "
            "minh được: \\\"assembly scanning\\\", \\\"activator by name\\\", \\\"json by string type name\\\"; true "
            "với \\\"source generated serializer\\\", \\\"generic constraint\\\", \\\"explicit registration\\\"."
        ),
        "hints": {
            "deployment-desc": "Kiểm tra aot trước, rồi selfContained, rồi trimmed.",
            "trim-compat": "Một tập mẫu an toàn vs các mẫu động đã biết; mọi thứ động đều thua.",
        },
    },
    "csa-p18-reflection-audit": {
        "title": "Kiểm toán reflection",
        "prompt": (
            "Cho một kiểu, liệt kê các thao tác reflection nào sẽ gãy dưới trimming mạnh: hiện thực "
            "`static List<string> Audit(Type t)` trả về mô tả cho mỗi thao tác sống sót qua trimming "
            "một cách tĩnh: gồm \\\"gettype-of-t\\\" nếu t là kiểu thấy được lúc biên dịch (luôn đúng ở "
            "đây), \\\"declared-fields\\\" nếu nó có trường (GetFields luôn chạy trên kiểu được giữ), "
            "\\\"attribute-read\\\" nếu nó có attribute, \\\"constructor-invoke\\\" nếu có constructor không tham "
            "số — nhưng KHÔNG BAO GIỜ gồm \\\"scan-all-types\\\" (không bao giờ sống sót). Test xác minh cả "
            "phần gồm lẫn phần vắng mặt."
        ),
        "hints": {
            "audit-kept-type": "typeof(Sample) là tham chiếu trực tiếp → kiểu (và thành viên) được giữ; quét toàn cục chẳng bao "
                               "giờ chứng minh được.",
        },
    },
    "csa-p18-size-math": {
        "title": "Phép toán khởi động và kích thước",
        "prompt": (
            "Hiện thực `static (long bytes, double startupMs) DeployCost(string model, int appBytes, "
            "double jitMs)` mô tả chi phí triển khai mang tính khái niệm: \\\"framework-dependent\\\" → "
            "runtime KHÔNG được đóng gói (trả appBytes, jitMs + 120 cho JIT lần gọi đầu); "
            "\\\"self-contained\\\" → bytes = appBytes + 65_000_000, startupMs = jitMs + 120; \\\"trimmed\\\" → "
            "bytes = appBytes + 25_000_000, startupMs = jitMs + 120; \\\"aot\\\" → bytes = appBytes + "
            "18_000_000, startupMs = 2.0 (không JIT). Điểm được chấm: AOT không trả thuế JIT; các mô "
            "hình khác đều mang nó."
        ),
        "hints": {
            "cost-table": "Switch theo model; trả tuple theo bảng. AOT bỏ qua jitMs hoàn toàn.",
        },
    },
    "csa-checkpoint-m19-task": {
        "title": "Checkpoint networking",
        "prompt": (
            "Hiện thực length-prefix framing trên buffer trong bộ nhớ (không phụ thuộc loopback, tất "
            "định): `static byte[] EncodeFrame(string payload)` — tiền tố độ dài 4 byte little-endian "
            "rồi byte UTF-8; `static string DecodeFrame(ReadOnlySpan<byte> data)` — đọc tiền tố, xác "
            "thực data.Length >= 4 + length (ném ArgumentException nếu không), giải mã đúng `length` "
            "byte. Rồi hiện thực `static async Task<string> EchoProtocol(string message)`: mở "
            "TcpListener trên port loopback ephemeral, nhận một client, đọc một frame, echo payload "
            "trả về theo khung, và trả về thứ client nhận được. Loopback TCP của sandbox đã được xác "
            "minh hoạt động."
        ),
        "hints": {
            "frame-roundtrip": "BinaryPrimitives.WriteInt32LittleEndian(prefix, Encoding.UTF8.GetByteCount(payload)); rồi ghi byte.",
            "truncated-frame-rejected": "Nếu data.Length < 4 + length, ném ArgumentException — frame dở dang là bug TCP số một.",
            "loopback-echo": "TcpListener(IPAddress.Loopback, 0) chọn port ephemeral; đọc frame, ghi cùng payload đóng khung trả về; "
                             "client đọc và giải mã.",
        },
    },
    "csa-p19-frame-stream": {
        "title": "Đóng khung luồng liên tục",
        "prompt": (
            "TCP thật giao các frame dính nhau và bị xẻ. Hiện thực `static List<string> "
            "DecodeStream(byte[] streamBytes)` giải mã TẤT CẢ frame nối trong một buffer (thực tế "
            "localhost: hai lần ghi đến trong một lần đọc), ném ArgumentException nếu stream kết thúc "
            "giữa frame. Test nối ba frame vào một buffer cộng thêm frame thứ tư bị cắt, mong hai lần "
            "giải mã sạch rồi một lần ném... hãy hiện thực `static List<string> "
            "DecodeStreamSafe(byte[] streamBytes)` trả về mọi frame HOÀN CHỈNH và bỏ qua frame cuối "
            "bị cắt (mẫu reader khoan dung mà mọi giao thức thật cần)."
        ),
        "hints": {
            "glued-frames": "Vòng lặp: đọc tiền tố, xác thực phần còn lại, cắt payload, tăng offset.",
            "trailing-partial-tolerated": "Cùng vòng lặp, nhưng nếu 4 + len > phần còn lại: dừng (trả những gì có) thay vì ném.",
        },
    },
    "csa-p19-timeout-enforce": {
        "title": "Thi hành deadline",
        "prompt": (
            "Hiện thực `static async Task<string> ReadWithDeadline(Func<Task<string>> read, TimeSpan "
            "deadline)`: await phép đọc; nếu quá deadline, ném TimeoutException và NGỪNG CHỜ (task đọc "
            "vẫn chạy nhưng caller thì không). Dùng Task.WhenAny(read, Task.Delay(deadline)) — mẫu "
            "abandon-the-wait kinh điển. Test dùng phép đọc ngủ 500ms với deadline 50ms và mong có "
            "lỗi ném trong khoảng thấp hơn xa 500ms."
        ),
        "hints": {
            "fast-read-passes": "WhenAny trả về task hoàn thành đầu tiên; nếu là task đọc, trả kết quả của nó.",
            "slow-read-times-out": "var completed = await Task.WhenAny(readTask, Task.Delay(deadline)); if (completed != readTask) "
                                   "throw new TimeoutException();",
        },
    },
    "csa-checkpoint-m20-task": {
        "title": "Checkpoint hệ phân tán",
        "prompt": (
            "Message bus mô phỏng, tất định: hiện thực lớp `IdempotentProcessor` với `int "
            "Process(string messageId, Func<int> work)` — xử lý work đúng một lần cho mỗi messageId, "
            "cache kết quả, trả lại khi lặp lại mà KHÔNG chạy lại work (work có bộ đếm tác dụng phụ "
            "mà test theo dõi). Rồi hiện thực `static int[] DeliverAll(List<string> messageIds, "
            "Func<string, int> handler, int duplicates)` giao mỗi tin nhắn `duplicates` lần (lộn xộn, "
            "xáo trộn tất định theo chỉ số) và trả về chênh lệch bộ đếm work — phải đúng bằng "
            "messageIds.Count vì các bản trùng bị hấp thụ nhờ idempotency."
        ),
        "hints": {
            "process-once": "Dictionary<string,int> cache: TryGetValue → trả; ngược lại tính, lưu, trả.",
            "duplicates-absorbed": "DeliverAll: một IdempotentProcessor dùng chung; giao mỗi id `duplicates` lần; đếm số lần chạy "
                                   "trước/sau.",
        },
    },
    "csa-p20-retry-budget": {
        "title": "Ngân sách thất bại",
        "prompt": (
            "Retry nhân tải đúng lúc hệ thống ít chịu đựng được nhất. Hiện thực `static int "
            "AmplifiedLoad(int clients, int baseAttempts, int retryMultiplier)` trả về tổng request: "
            "clients × baseAttempts × (1 + retryMultiplier). Rồi hiện thực `static bool "
            "WithinBudget(int total, int budget)` và `static string Verdict(int clients, int "
            "baseAttempts, int retryMultiplier, int budget)` trả \\\"ok\\\" nếu nằm trong, \\\"overload\\\" nếu "
            "ngược lại. Insight được chấm: 1000 client × 1 lời gọi × 5 retry = 6000 request — retry "
            "storm là phép toán, không phải xui xẻo."
        ),
        "hints": {
            "amplification": "AmplifiedLoad = clients * baseAttempts * (1 + retryMultiplier); Verdict so với budget.",
        },
    },
    "csa-p20-eventual-read": {
        "title": "Đọc-sau-ghi dưới tính nhất quán cuối cùng",
        "prompt": (
            "Hiện thực lớp `EventualStore(int replicationDelayMs)` với `void Write(string key, int "
            "value)` (primary ngay tức thì; replica sau khoảng trễ qua Task.Run) và `int? "
            "ReadStale(string key)` (đọc replica, có thể trượt các ghi mới) cộng `int? "
            "ReadPrimary(string key)` (luôn cập nhật). Hiện thực `static async Task<bool> "
            "ReadAfterWriteHolds(EventualStore store, string key)` ghi 42, đọc replica NGAY LẬP TỨC — "
            "và trả về việc lần đọc có thấy bản ghi hay không (với trễ thật thì KHÔNG được thấy; test "
            "sau đó chờ quá khoảng trễ và đòi replica hội tụ)."
        ),
        "hints": {
            "stale-then-converged": "Write: dict[key]=v trên primary; Task.Run(async { await Task.Delay(replicationDelayMs); "
                                    "replica[key]=v; }). ReadAfterWriteHolds: Write, rồi ReadStale != null.",
        },
    },
    "csa-checkpoint-m21-task": {
        "title": "Checkpoint bảo mật",
        "prompt": (
            "Hiện thực `static byte[] RandomSalt(int bytes)` dùng RandomNumberGenerator, và `static "
            "string HashPassword(string password, byte[] salt)` trả về Base64 của "
            "Rfc2898DeriveBytes(Pbkdf2) với 100_000 vòng lặp, SHA256, đầu ra 32 byte. Rồi hiện thực "
            "`static bool VerifyPassword(string password, byte[] salt, string expectedBase64)` tính "
            "lại và so bằng CryptographicOperations.FixedTimeEquals (so sánh an toàn thời gian mà bài "
            "học bắt buộc). Nghiệm sai dùng string == — test chứng minh hai hành vi khác biệt về ngữ "
            "nghĩa."
        ),
        "hints": {
            "hash-verify": "Rfc2898DeriveBytes.Pbkdf2(password, salt, 100_000, HashAlgorithmName.SHA256, 32); "
                           "Convert.ToBase64String kết quả.",
            "salt-unique": "RandomNumberGenerator.GetBytes(16) — không bao giờ new Random() cho bí mật.",
        },
    },
    "csa-p21-path-traversal": {
        "title": "Chặn path traversal",
        "prompt": (
            "Hiện thực `static string SafeJoin(string baseDir, string userInput)` nối tên tệp tương "
            "đối do người dùng cung cấp vào thư mục gốc nhưng TỪ CHỐI traversal: chuẩn hóa đường dẫn "
            "kết hợp (Path.GetFullPath) và ném UnauthorizedAccessException nếu kết quả không bắt đầu "
            "bằng base đã chuẩn hóa (cho phép base kết thúc bằng dấu phân tách). \\\"report.pdf\\\" đi qua; "
            "\\\"..\\\\..\\\\etc\\\\passwd\\\" và đường dẫn tuyệt đối bị chặn."
        ),
        "hints": {
            "clean-name-passes": "var full = Path.GetFullPath(Path.Combine(baseDir, userInput)); var baseFull = "
                                 "Path.GetFullPath(baseDir); if (!full.StartsWith(baseFull)) throw new UnauthorizedAccessException();",
            "traversal-rejected": "Path.Combine + GetFullPath chuẩn hóa ..; kiểm tra tiền tố bắt cả traversal tương đối lẫn thoát "
                                  "tuyệt đối.",
        },
    },
    "csa-p21-parameterized-query": {
        "title": "Parameterize hoặc gãy",
        "prompt": (
            "SQL injection là chuỗi nối gặp input người dùng. Hiện thực `static string "
            "BuildQuery(string tableName, string userInput)` trả về văn bản SQL kiểu-tham-số hóa AN "
            "TOÀN: \\\"SELECT * FROM \\\" + table đã xác thực + \\\" WHERE name = @name\\\" — xác thực table với "
            "danh sách trắng {\\\"orders\\\", \\\"customers\\\"} (ném ArgumentException nếu khác) và KHÔNG BAO "
            "GIỜ nhúng userInput vào chuỗi (@name giữ là placeholder). Hiện thực `static bool "
            "IsSafeQuery(string sql)` trả về false nếu sql chứa ký tự nháy đơn (bằng chứng dữ liệu "
            "người dùng đã bị nội suy)."
        ),
        "hints": {
            "placeholder-not-interpolated": "Xác thực table với danh sách trắng; trả $\\\"SELECT * FROM {table} WHERE name = @name\\\" — "
                                            "input người dùng không bao giờ vào chuỗi.",
            "table-allowlist": "Tên bảng không thể là tham số — hãy cho vào danh sách trắng.",
        },
    },
    "csa-checkpoint-m22-task": {
        "title": "Checkpoint truy cập dữ liệu",
        "prompt": (
            "Dựng `class OptimisticStore<T> where T : notnull` với `void Put(string key, T value, int "
            "expectedVersion)` và `(bool ok, T? value) TryGet(string key)` cộng `int VersionOf(string "
            "key)`. Put chỉ lưu khi expectedVersion khớp phiên bản hiện tại (key vắng mặt = phiên bản "
            "0), tăng phiên bản, và ném `InvalidOperationException` với thông báo bắt đầu bằng \\\"version "
            "conflict\\\" nếu không. Rồi hiện thực `static int SaveAll(OptimisticStore<string> store, "
            "List<(string Key, string Value, int Expected)> writes, int maxRounds)` áp các ghi theo "
            "vòng — mỗi vòng thử mọi ghi chưa lưu với phiên bản hiện tại, đếm xung đột — và trả về số "
            "vòng cần thiết (ném InvalidOperationException nếu chưa xong trong maxRounds)."
        ),
        "hints": {
            "conflict-detected": "Theo dõi Dictionary<string,(T value,int version)>; trong Put so expected với phiên bản hiện tại "
                                 "trước khi ghi.",
            "conflict-retry-converges": "Giữ danh sách chờ; mỗi vòng thử lại mục nào expectedVersion mới khớp; đếm số vòng.",
        },
    },
    "csa-p22-pool-budget": {
        "title": "Ngân sách connection pool",
        "prompt": (
            "Một pool cỡ P phục vụ các request đồng thời: mỗi request giữ kết nối trong `holdMs` "
            "mili giây. Hiện thực `static int MaxConcurrentWithin(int poolSize, int requests, int "
            "holdMs, int windowMs)` = bao nhiêu trong `requests` có thể in-flight đồng thời với "
            "poolSize kết nối (min(poolSize, requests)), và `static double Utilization(int poolSize, "
            "int requests, int holdMs, int windowMs)` = MaxConcurrentWithin × holdMs / windowMs × 100, "
            "làm tròn 2 số thập phân. Rồi `static bool WillStarve(int poolSize, int requests, int "
            "holdMs, int windowMs)` = true khi requests > poolSize."
        ),
        "hints": {
            "pool-limits-concurrency": "Phép toán thuần: cap = min(poolSize, requests); starve = requests > poolSize.",
            "utilization-formula": "cap × holdMs ÷ windowMs × 100, Math.Round tới 2 số thập phân.",
        },
    },
    "csa-p22-nplus-one-count": {
        "title": "Bộ đếm truy vấn N+1",
        "prompt": (
            "Cho `orders` (List<string> id) mỗi đơn cần một truy vấn lấy dòng hàng: vòng lặp ngây thơ "
            "gửi 1 + N truy vấn. Hiện thực `static int NaiveQueries(int orderCount)` = orderCount + 1, "
            "và `static int BatchedQueries(int orderCount, int batchSize)` = "
            "ceil(orderCount / batchSize) + 1 (truy vấn IN theo lô). Rồi hiện thực `static (int naive, "
            "int batched, double saved) Compare(int orderCount, int batchSize)` trả cả ba với saved = "
            "round((naive − batched) / naive × 100, 2)."
        ),
        "hints": {
            "query-math": "(int)Math.Ceiling(orderCount / (double)batchSize); saved qua Math.Round tới 2 số thập phân.",
        },
    },
    "csa-checkpoint-m24-task": {
        "title": "Checkpoint capstone",
        "prompt": (
            "Lắp ráp lõi nền tảng thành `class JobPlatform`. Constructor: `JobPlatform(int capacity)`. "
            "Phương thức: `(bool accepted) Submit(string jobId, Func<int> work)` — chỉ nhận khi jobId "
            "chưa từng thấy VÀ số in-flight < capacity (idempotency + backpressure; bản trùng và vượt "
            "sức chứa trả false và tính là bị từ chối); `int RunAll()` — thực thi mọi công việc đã "
            "nhận đúng một lần (theo thứ tự thời gian), trả về chênh lệch bộ đếm work (bằng số đã "
            "nhận — chứng minh mỗi job chạy đúng một lần); thuộc tính `int Pending`. Rồi `static (int "
            "accepted, int rejected, int executed) SubmitSchedule(JobPlatform p, List<string> jobIds, "
            "int duplicatesPerJob)` — nộp mỗi id (1 + duplicatesPerJob) lần, trả về số accepted/rejected "
            "và executed = RunAll()."
        ),
        "hints": {
            "idempotent-and-bounded": "HashSet<string> seen + danh sách chờ; nhận khi !seen.Contains && pending.Count < capacity.",
            "schedule-runs-once": "SubmitSchedule: giao mỗi id (1+duplicates) lần; executed = p.RunAll(); bộ đếm work dùng chung.",
        },
    },
    "csa-p24-slo-budget": {
        "title": "Ngân sách lỗi SLO",
        "prompt": (
            "SLO 99.9% khả dụng trên cửa sổ 30 ngày (2,592,000 s) cấp một ngân sách lỗi "
            "`budgetSeconds = window × (1 − slo)`. Hiện thực `static double BudgetSeconds(double "
            "windowSeconds, double slo)` và `static (double remaining, bool within) Spend(double "
            "windowSeconds, double slo, double downtimeSeconds)` trả về ngân sách còn lại và thời "
            "gương chết nguồn có còn nằm trong ngân sách (within = downtime ≤ budget)."
        ),
        "hints": {
            "budget-math": "budget = window × (1 − slo); remaining = budget − downtime; within = downtime ≤ budget.",
        },
    },
    "csa-p24-dlq-promotion": {
        "title": "Luật thăng cấp DLQ",
        "prompt": (
            "Một công việc rơi vào dead-letter queue khi số thất bại đạt ngưỡng. Hiện thực `static "
            "(bool dead, int failures) OnFailure(int currentFailures, int threshold, int maxAttempts)` "
            "— tăng số thất bại; dead = failures ≥ threshold HOẶC lượt thử cạn (maxAttempts), và số "
            "thất bại bão hòa ở threshold (không tăng vượt sau khi dead)."
        ),
        "hints": {
            "promotion-rules": "failures = min(current+1, threshold); dead = failures ≥ threshold || maxAttempts ≤ current+1... "
                               "hãy quyết định ngữ nghĩa cạn lượt chính xác và khớp với test.",
        },
    },
}
