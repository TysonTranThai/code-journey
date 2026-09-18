"""Module 19 — Advanced networking (csa-m19)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-networking",
        "Advanced Networking",
        "Sockets on loopback: framing, protocols, connection lifecycle, and the failure modes of distributed I/O — verified in the sandbox.",
    )

    csa.register_lesson(
        MID, "csa-m19-sockets", "Sockets and the loopback world",
        "TcpClient/TcpListener, NetworkStream, and why localhost is the honest lab for protocol code.",
        15, "advanced", _m19_sockets, _m19_sockets_vi,
    )
    csa.register_lesson(
        MID, "csa-m19-framing", "Framing: the first protocol bug",
        "TCP is a byte stream, not a message stream: length-prefix framing and why 'one write = one read' is a lie.",
        16, "advanced", _m19_framing, _m19_framing_vi,
    )
    csa.register_lesson(
        MID, "csa-m19-protocols", "Protocol design: requests, responses, timeouts",
        "Correlation IDs, deadlines, and the client/server contract that survives slow consumers.",
        15, "advanced", _m19_protocols, _m19_protocols_vi,
    )
    csa.register_lesson(
        MID, "csa-m19-failures", "Network failure modes on localhost",
        "Partial reads, slowloris, connection exhaustion, and backpressure — every distributed failure, miniaturized.",
        15, "advanced", _m19_failures, _m19_failures_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m19", "Checkpoint: networking",
        "Synthesis: implement length-prefix framing and a working echo protocol client/server.",
        12, "advanced", _m19_checkpoint, _m19_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m19-task", MID,
        title="Networking checkpoint",
        prompt=(
            "Implement length-prefix framing on in-memory buffers (loopback-independent, deterministic): "
            "`static byte[] EncodeFrame(string payload)` — 4-byte little-endian length prefix followed by UTF-8 "
            "bytes; `static string DecodeFrame(ReadOnlySpan<byte> data)` — reads the prefix, validates that "
            "data.Length >= 4 + length (throw ArgumentException otherwise), decodes exactly `length` bytes. Then "
            "implement `static async Task<string> EchoProtocol(string message)`: start a TcpListener on an "
            "ephemeral loopback port, accept one client, read one frame, echo the payload back framed, and return "
            "what the client received. The sandbox's loopback TCP is verified working."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "frame-roundtrip",
                "code": (
                    "var frame = Solution.EncodeFrame(\"hello\");\n"
                    'Cj.Eq(frame.Length, 4 + 5, "prefix + payload");\n'
                    'Cj.Eq(frame[0], 5, "LE length low byte");\n'
                    'Cj.Eq(Solution.DecodeFrame(frame), "hello", "decodes exactly");'
                ),
                "hint": "BinaryPrimitives.WriteInt32LittleEndian(prefix, Encoding.UTF8.GetByteCount(payload)); then write bytes.",
            },
            {
                "name": "truncated-frame-rejected",
                "code": (
                    "var frame = Solution.EncodeFrame(\"truncate me please\");\n"
                    "var bad = frame[..^3];   // cut the last 3 payload bytes\n"
                    "var ex = await Cj.ThrowsAsync<ArgumentException>(() => Task.Run(() => Solution.DecodeFrame(bad)));\n"
                    'Cj.True(ex is not null, "truncated frame must throw, not decode garbage");'
                ),
                "hint": "If data.Length < 4 + length, throw ArgumentException — partial frames are the #1 TCP bug.",
            },
            {
                "name": "loopback-echo",
                "code": (
                    "var echoed = await Solution.EchoProtocol(\"ping-42\");\n"
                    'Cj.Eq(echoed, "ping-42", "full client/server roundtrip on loopback");'
                ),
                "hint": "TcpListener(IPAddress.Loopback, 0) picks an ephemeral port; read frame, write same payload framed back; client reads and decodes.",
            },
        ],
        reference=(
            "using System.Buffers.Binary;\nusing System.Net;\nusing System.Net.Sockets;\nusing System.Text;\n\n"
            "public class Solution\n{\n"
            "    public static byte[] EncodeFrame(string payload)\n"
            "    {\n"
            "        var body = Encoding.UTF8.GetBytes(payload);\n"
            "        var frame = new byte[4 + body.Length];\n"
            "        BinaryPrimitives.WriteInt32LittleEndian(frame, body.Length);\n"
            "        body.CopyTo(frame, 4);\n"
            "        return frame;\n"
            "    }\n\n"
            "    public static string DecodeFrame(ReadOnlySpan<byte> data)\n"
            "    {\n"
            "        if (data.Length < 4) throw new ArgumentException(\"frame too short for prefix\");\n"
            "        int len = BinaryPrimitives.ReadInt32LittleEndian(data);\n"
            "        if (len < 0 || data.Length < 4 + len) throw new ArgumentException($\"truncated frame: need {4 + len}, have {data.Length}\");\n"
            "        return Encoding.UTF8.GetString(data.Slice(4, len));\n"
            "    }\n\n"
            "    public static async Task<string> EchoProtocol(string message)\n"
            "    {\n"
            "        var listener = new TcpListener(IPAddress.Loopback, 0);\n"
            "        listener.Start();\n"
            "        int port = ((IPEndPoint)listener.LocalEndpoint).Port;\n"
            "        var server = listener.AcceptTcpClientAsync();\n"
            "        using var client = new TcpClient();\n"
            "        await client.ConnectAsync(IPAddress.Loopback, port);\n"
            "        var accepted = await server;\n"
            "        using (accepted)\n"
            "        {\n"
            "            var clientNet = client.GetStream();\n"
            "            await clientNet.WriteAsync(EncodeFrame(message));\n"
            "            // server side: read one frame, echo it back (this IS the protocol)\n"
            "            var snet = accepted.GetStream();\n"
            "            var hdr = new byte[4];\n"
            "            int got = 0;\n"
            "            while (got < 4)\n"
            "            {\n"
            "                int n = await snet.ReadAsync(hdr.AsMemory(got));\n"
            "                if (n == 0) throw new IOException(\"closed before prefix\");\n"
            "                got += n;\n"
            "            }\n"
            "            int len = BinaryPrimitives.ReadInt32LittleEndian(hdr);\n"
            "            var body = new byte[len];\n"
            "            int bread = 0;\n"
            "            while (bread < len)\n"
            "            {\n"
            "                int n = await snet.ReadAsync(body.AsMemory(bread));\n"
            "                if (n == 0) throw new IOException(\"closed before body\");\n"
            "                bread += n;\n"
            "            }\n"
            "            var echo = EncodeFrame(Encoding.UTF8.GetString(body));\n"
            "            await snet.WriteAsync(echo);\n"
            "            // client side: read the echo\n"
            "            var buf = new byte[1024];\n"
            "            int read = await clientNet.ReadAsync(buf);\n"
            "            return DecodeFrame(buf.AsSpan(0, read));\n"
            "        }\n"
            "    }\n}"
        ),
        wrong=(
            "using System.Buffers.Binary;\nusing System.Text;\n\n"
            "public class Solution\n{\n"
            "    public static byte[] EncodeFrame(string payload)\n"
            "    {\n"
            "        var body = Encoding.UTF8.GetBytes(payload);\n"
            "        var frame = new byte[4 + body.Length];\n"
            "        BinaryPrimitives.WriteInt32LittleEndian(frame, body.Length);\n"
            "        body.CopyTo(frame, 4);\n"
            "        return frame;\n"
            "    }\n\n"
            "    public static string DecodeFrame(ReadOnlySpan<byte> data)\n"
            "    {\n"
            "        int len = BinaryPrimitives.ReadInt32LittleEndian(data);   // WRONG: no length check — reads garbage on truncation\n"
            "        return Encoding.UTF8.GetString(data.Slice(4, len));\n"
            "    }\n\n"
            "    public static async Task<string> EchoProtocol(string message)\n"
            "    {\n"
            "        var listener = new TcpListener(IPAddress.Loopback, 0);\n"
            "        listener.Start();\n"
            "        int port = ((IPEndPoint)listener.LocalEndpoint).Port;\n"
            "        var server = listener.AcceptTcpClientAsync();\n"
            "        using var client = new TcpClient();\n"
            "        await client.ConnectAsync(IPAddress.Loopback, port);\n"
            "        var accepted = await server;\n"
            "        using (accepted)\n"
            "        {\n"
            "            var net = accepted.GetStream();\n"
            "            await net.WriteAsync(EncodeFrame(message));\n"
            "            var buf = new byte[4];   // WRONG: reads only the prefix, never the body\n"
            "            int read = await net.ReadAsync(buf);\n"
            "            return read >= 4 ? Encoding.UTF8.GetString(buf.AsSpan(0, 0)) : \"\";   // always \"\"\n"
            "        }\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p19-net", "Networking drills",
        "Buffer management, protocol state machines, timeout enforcement, and partial-write handling.",
        45, "advanced", "csa-m19-protocols",
        ["csa-p19-frame-stream", "csa-p19-timeout-enforce"],
    )
    csa.register_challenge(
        "csa-p19-frame-stream", MID,
        title="Frame a continuous stream",
        prompt=(
            "Real TCP delivers frames glued together and split apart. Implement `static List<string> "
            "DecodeStream(byte[] streamBytes)` that decodes ALL frames concatenated in one buffer (the common "
            "localhost reality: two writes arrive in one read), throwing ArgumentException if the stream ends "
            "mid-frame. The test concatenates three encoded frames into one buffer plus a truncated fourth, and "
            "expects two clean decodes then a throw... implement `static List<string> DecodeStreamSafe(byte[] "
            "streamBytes)` that returns all COMPLETE frames and ignores a trailing partial frame (the tolerant "
            "reader every real protocol needs)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "glued-frames",
                "code": (
                    "var buf = Solution.EncodeFrame(\"a\").Concat(Solution.EncodeFrame(\"bb\")).Concat(Solution.EncodeFrame(\"ccc\")).ToArray();\n"
                    "var r = Solution.DecodeStream(buf);\n"
                    'Cj.Eq(string.Join("|", r), "a|bb|ccc", "three glued frames decode");'
                ),
                "hint": "Loop: read prefix, validate remaining, slice payload, advance offset.",
            },
            {
                "name": "trailing-partial-tolerated",
                "code": (
                    "var buf = Solution.EncodeFrame(\"x\").Concat(Solution.EncodeFrame(\"yy\")).ToArray();\n"
                    "var partial = buf.Concat(new byte[] { 0, 0, 0 }).ToArray();   // truncated third frame\n"
                    "var r = Solution.DecodeStreamSafe(partial);\n"
                    'Cj.Eq(string.Join("|", r), "x|yy", "complete frames only; partial ignored");'
                ),
                "hint": "Same loop, but if 4 + len > remaining: stop (return what you have) instead of throwing.",
            },
        ],
        reference=(
            "using System.Buffers.Binary;\nusing System.Text;\n\n"
            "public class Solution\n{\n"
            "    public static byte[] EncodeFrame(string payload)\n"
            "    {\n"
            "        var body = Encoding.UTF8.GetBytes(payload);\n"
            "        var frame = new byte[4 + body.Length];\n"
            "        BinaryPrimitives.WriteInt32LittleEndian(frame, body.Length);\n"
            "        body.CopyTo(frame, 4);\n"
            "        return frame;\n"
            "    }\n\n"            "    public static List<string> DecodeStream(byte[] streamBytes)\n"
            "    {\n"
            "        var frames = new List<string>();\n"
            "        int offset = 0;\n"
            "        while (offset < streamBytes.Length)\n"
            "        {\n"
            "            if (streamBytes.Length - offset < 4) throw new ArgumentException(\"truncated prefix\");\n"
            "            int len = BinaryPrimitives.ReadInt32LittleEndian(streamBytes.AsSpan(offset));\n"
            "            if (len < 0 || streamBytes.Length - offset - 4 < len)\n"
            "                throw new ArgumentException(\"truncated frame\");\n"
            "            frames.Add(Encoding.UTF8.GetString(streamBytes, offset + 4, len));\n"
            "            offset += 4 + len;\n"
            "        }\n"
            "        return frames;\n"
            "    }\n\n"
            "    public static List<string> DecodeStreamSafe(byte[] streamBytes)\n"
            "    {\n"
            "        var frames = new List<string>();\n"
            "        int offset = 0;\n"
            "        while (offset + 4 <= streamBytes.Length)\n"
            "        {\n"
            "            int len = BinaryPrimitives.ReadInt32LittleEndian(streamBytes.AsSpan(offset));\n"
            "            if (len < 0 || offset + 4 + len > streamBytes.Length) break;   // trailing partial: stop\n"
            "            frames.Add(Encoding.UTF8.GetString(streamBytes, offset + 4, len));\n"
            "            offset += 4 + len;\n"
            "        }\n"
            "        return frames;\n"
            "    }\n}"
        ),
        wrong=(
            "using System.Buffers.Binary;\nusing System.Text;\n\n"
            "public class Solution\n{\n"
            "    public static byte[] EncodeFrame(string payload)\n"
            "    {\n"
            "        var body = Encoding.UTF8.GetBytes(payload);\n"
            "        var frame = new byte[4 + body.Length];\n"
            "        BinaryPrimitives.WriteInt32LittleEndian(frame, body.Length);\n"
            "        body.CopyTo(frame, 4);\n"
            "        return frame;\n"
            "    }\n\n"            "    public static List<string> DecodeStream(byte[] streamBytes)\n"
            "    {\n"
            "        var frames = new List<string>();\n"
            "        int offset = 0;\n"
            "        while (offset < streamBytes.Length)\n"
            "        {\n"
            "            int len = BinaryPrimitives.ReadInt32LittleEndian(streamBytes.AsSpan(offset));   // WRONG: no bounds check before prefix read\n"
            "            frames.Add(Encoding.UTF8.GetString(streamBytes, offset + 4, len));   // WRONG: no frame-length check\n"
            "            offset += 4 + len;\n"
            "        }\n"
            "        return frames;\n"
            "    }\n\n"
            "    public static List<string> DecodeStreamSafe(byte[] streamBytes) => DecodeStream(streamBytes);   // WRONG: not tolerant\n"
            "}"
        ),
        level="real-world",
    )
    csa.register_challenge(
        "csa-p19-timeout-enforce", MID,
        title="Deadline enforcement",
        prompt=(
            "Implement `static async Task<string> ReadWithDeadline(Func<Task<string>> read, TimeSpan deadline)`: "
            "await the read; if it exceeds the deadline, throw TimeoutException and STOP WAITING (the read task "
            "continues but the caller does not). Use Task.WhenAny(read, Task.Delay(deadline)) — the classic "
            "abandon-the-wait pattern. The test uses a read that sleeps 500ms with a 50ms deadline and expects a "
            "throw in well under 500ms."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "fast-read-passes",
                "code": (
                    "var r = await Solution.ReadWithDeadline(() => Task.FromResult(\"ok\"), TimeSpan.FromMilliseconds(500));\n"
                    'Cj.Eq(r, "ok", "fast read completes");'
                ),
                "hint": "WhenAny returns the first completed task; if it is the read, return its result.",
            },
            {
                "name": "slow-read-times-out",
                "code": (
                    "var sw = Stopwatch.StartNew();\n"
                    "var ex = await Cj.ThrowsAsync<TimeoutException>(() => Solution.ReadWithDeadline(\n"
                    "    async () => { await Task.Delay(500); return \"late\"; },\n"
                    "    TimeSpan.FromMilliseconds(50)));\n"
                    "sw.Stop();\n"
                    'Cj.True(ex is not null, "deadline throws");\n'
                    'Cj.True(sw.ElapsedMilliseconds < 400, $"abandoned the wait quickly (took {sw.ElapsedMilliseconds}ms)");'
                ),
                "hint": "var completed = await Task.WhenAny(readTask, Task.Delay(deadline)); if (completed != readTask) throw new TimeoutException();",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static async Task<string> ReadWithDeadline(Func<Task<string>> read, TimeSpan deadline)\n"
            "    {\n"
            "        var readTask = read();\n"
            "        var completed = await Task.WhenAny(readTask, Task.Delay(deadline)).ConfigureAwait(false);\n"
            "        if (completed != readTask)\n"
            "            throw new TimeoutException($\"read exceeded {deadline}\");\n"
            "        return await readTask.ConfigureAwait(false);\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static async Task<string> ReadWithDeadline(Func<Task<string>> read, TimeSpan deadline)\n"
            "    {\n"
            "        var readTask = read();\n"
            "        var delay = Task.Delay(deadline);\n"
            "        await Task.WhenAll(readTask, delay);   // WRONG: waits for BOTH — the deadline adds delay, never abandons\n"
            "        return await readTask;\n"
            "    }\n}"
        ),
        level="real-world",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m19_sockets = r"""## Sockets and the loopback world

A socket is a file handle to a network endpoint. The managed API surface:

```csharp
var listener = new TcpListener(IPAddress.Loopback, 0);   // port 0 = ephemeral
listener.Start();
var client = await listener.AcceptTcpClientAsync();      // one per connection
var stream = client.GetStream();                          // NetworkStream: duplex, unbuffered-ish

var outbound = new TcpClient();
await outbound.ConnectAsync(IPAddress.Loopback, port);
```

Code Journey's sandbox permits **loopback TCP and UDP with no external
network** — which is precisely the honest lab for protocol engineering:
all the hard parts (framing, buffering, lifecycle, timeouts, partial
transfers) happen on localhost, while the uncontrollable variables
(packet loss, routing, firewalls) are absent. Protocol bugs found here
are the same bugs that eat production services.

The facts that surprise newcomers:

- **NetworkStream has no message concept.** `WriteAsync(frame)` does not
  produce `ReadAsync(buf) == frame`. It produces *bytes available sometime,
  possibly glued with other writes, possibly split*.
- **Read returns 0 only on clean close.** A half-open connection (peer
  died, cable pulled) surfaces as an INFINITE read or a timeout — never as
  a zero. That is why deadlines (next lesson) are not optional.
- **Accept is not authentication.** Anyone who can reach the port can
  connect; protocol-level auth (or none, if loopback-only) is your design.

The lifecycle rules: dispose clients (finally / using), shut down
gracefully (`Shutdown(Both)` then dispose), and bound every listener with
an accept loop that cannot die from one bad connection.
"""

_m19_sockets_vi = r"""## Socket và thế giới loopback

Socket là file handle tới một điểm cuối mạng. Bề mặt API managed:

```csharp
var listener = new TcpListener(IPAddress.Loopback, 0);   // cổng 0 = ephemeral
listener.Start();
var client = await listener.AcceptTcpClientAsync();      // một cái cho mỗi kết nối
var stream = client.GetStream();                          // NetworkStream: duplex, gần như không buffer

var outbound = new TcpClient();
await outbound.ConnectAsync(IPAddress.Loopback, port);
```

Sandbox của Code Journey cho phép **TCP và UDP loopback, không mạng bên
ngoài** — và đó chính là phòng thí nghiệm trung thực cho kỹ nghệ giao thức:
mọi phần khó (framing, buffer, vòng đời, timeout, truyền một phần) đều xảy
ra trên localhost, trong khi các biến không kiểm soát được (mất gói, định
tuyến, firewall) vắng mặt. Bug giao thức tìm thấy ở đây chính là những bug
ăn mòn service production.

Những sự thật khiến người mới bất ngờ:

- **NetworkStream không có khái niệm tin nhắn.** `WriteAsync(frame)` không
  sinh ra `ReadAsync(buf) == frame`. Nó sinh ra *các byte có sẵn lúc nào
  đó, có thể dính với các write khác, có thể bị tách*.
- **Read trả 0 chỉ khi đóng sạch.** Kết nối nửa mở (peer chết, cáp bị rút)
  lộ diện dưới dạng một lệnh đọc VÔ HẠN hoặc timeout — không bao giờ là số
  không. Vì vậy deadline (bài kế tiếp) không phải tùy chọn.
- **Accept không phải xác thực.** Ai tới được cổng đều kết nối được; xác
  thực mức giao thức (hoặc không, nếu chỉ loopback) là thiết kế của bạn.

Luật vòng đời: dispose client (finally / using), đóng duyên dáng
(`Shutdown(Both)` rồi dispose), và giới hạn mọi listener bằng một vòng
accept không thể chết vì một kết nối xấu.
"""

_m19_framing = r"""## Framing: the first protocol bug

TCP gives you a **byte stream**. Every protocol you build on it must
re-introduce messages. The bug that ends junior protocols: assuming
one write = one read.

```csharp
// Writer sends two frames:
await stream.WriteAsync(EncodeFrame("first"));
await stream.WriteAsync(EncodeFrame("second"));

// Reader gets ONE read containing BOTH frames glued — or three reads
// splitting the second frame across boundaries. TCP owes you nothing.
```

**Length-prefix framing** is the standard fix: every message is
`[4-byte length][payload]`. The reader maintains a buffer and a state
machine:

1. Have 4+ bytes? Read the prefix → this frame's length.
2. Have 4+len bytes? Extract the payload, advance, repeat.
3. Not enough? Wait for more bytes (append incoming data to the buffer).

This is exactly what the checkpoint implements on a buffer — and what
`DecodeStreamSafe` extends to the tolerant-reader form real protocols
need: complete frames process, trailing partials wait.

Design decisions in every framing scheme:

- **Prefix size**: 4 bytes caps frames at 2GB — and demands a MAX-FRAME
  check (a malicious/corrupt prefix of 0x7FFFFFFF should not allocate 2GB;
  the reader rejects frames over a policy cap).
- **Endianness**: little-endian (BinaryPrimitives) or big-endian (network
  order) — either is fine, but it must be WRITTEN DOWN and never changed.
- **In-band vs out-of-band**: control messages inside the stream (like
  HTTP headers) vs a second channel. In-band is simpler; out-of-band
  avoids head-of-line blocking for mixed traffic.

When you cannot trust framing to carry semantics, upgrade to a real
wire protocol (HTTP, gRPC, MessagePack) — they solved framing, versions,
and types; your job is the payload.
"""

_m19_framing_vi = r"""## Framing: bug giao thức đầu tiên

TCP đưa cho bạn một **dòng byte**. Mọi giao thức bạn xây trên đó phải tự
tái giới thiệu khái niệm tin nhắn. Bug kết liễu các giao thức nghiệp dư:
giả định một lần ghi = một lần đọc.

```csharp
// Writer gửi hai khung:
await stream.WriteAsync(EncodeFrame("first"));
await stream.WriteAsync(EncodeFrame("second"));

// Reader nhận MỘT lần đọc chứa CẢ HAI khung dính nhau — hoặc ba lần đọc
// tách khung thứ hai ra giữa chừng. TCP không nợ bạn gì cả.
```

**Framing tiền tố độ dài** là cách sửa chuẩn: mọi tin nhắn là
`[4 byte độ dài][payload]`. Reader duy trì một buffer và một máy trạng thái:

1. Có 4+ byte? Đọc tiền tố → độ dài khung này.
2. Có 4+len byte? Trích payload, tăng offset, lặp lại.
3. Chưa đủ? Chờ thêm byte (nối dữ liệu đến vào buffer).

Đây chính xác là những gì checkpoint cài trên một buffer — và những gì
`DecodeStreamSafe` mở rộng thành dạng tolerant-reader mà giao thức thật
cần: khung hoàn chỉnh được xử lý, phần thừa dở dang được chờ.

Các quyết định thiết kế trong mọi lược đồ framing:

- **Kích thước tiền tố**: 4 byte cho phép khung tới 2GB — và đòi hỏi một
  kiểm tra MAX-FRAME (tiền tố độc/hỏng 0x7FFFFFFF không được phép cấp phát
  2GB; reader từ chối khung vượt trần chính sách).
- **Endianness**: little-endian (BinaryPrimitives) hay big-endian (thứ tự
  mạng) — cái nào cũng được, nhưng phải được GHI RA và không bao giờ đổi.
- **In-band vs out-of-band**: tin nhắn điều khiển bên trong dòng (như
  header HTTP) vs một kênh thứ hai. In-band đơn giản hơn; out-of-band tránh
  head-of-line blocking cho traffic lẫn lộn.

Khi không thể tin framing mang ngữ nghĩa, hãy nâng cấp lên giao thức dây
thật (HTTP, gRPC, MessagePack) — chúng đã giải quyết framing, phiên bản,
và kiểu; việc của bạn là payload.
"""

_m19_protocols = r"""## Protocol design: requests, responses, timeouts

A request/response protocol on raw sockets needs four properties to
survive contact with reality:

**1. Correlation.** Requests and responses must be pairable — a
request ID echoed in the response. Without it, a client with two
in-flight requests cannot tell which response is which (and pipelining
becomes impossible).

**2. Deadlines.** Every read gets a timeout, enforced with
`Task.WhenAny(read, delay)` or a CancellationToken from
`CancellationTokenSource(TimeSpan)` — abandon the wait, then fail the
connection. A protocol without read deadlines accumulates half-open
connections until the file-descriptor table fills.

**3. Bounded buffers.** A reader that accepts unbounded data before
framing validates it is a DoS primitive (slowloris: send one byte every
59 seconds forever). Policy: cap the frame size, cap the buffer, and
close connections that exceed either.

**4. Clean states.** The protocol state machine — connected, awaiting
request, awaiting response, closed — must be explicit, and every
transition must be reachable by the tests. The failure modes (mid-frame
disconnect, timeout, oversized frame, bad magic) each map to a transition
to `closed` with a diagnostic reason.

The client-side contract mirrors it: connect with timeout, write framed
requests, read with deadline, correlate, dispose deterministically. The
checkpoint's `EchoProtocol` is the smallest honest version of all four
properties; the practice drills add the stream-gluing reality.
"""

_m19_protocols_vi = r"""## Thiết kế giao thức: request, response, timeout

Một giao thức request/response trên socket thô cần bốn tính chất để sống
sót khi va chạm với thực tế:

**1. Tương quan.** Request và response phải ghép cặp được — một request ID
được echo trong response. Không có nó, client có hai request đang bay
không thể biết response nào của request nào (và pipelining trở nên bất khả
thi).

**2. Deadline.** Mọi lệnh đọc có timeout, thi hành bằng
`Task.WhenAny(read, delay)` hoặc CancellationToken từ
`CancellationTokenSource(TimeSpan)` — từ bỏ cuộc chờ, rồi hủy kết nối.
Một giao thức không có deadline khi đọc sẽ tích lũy các kết nối nửa mở cho
đến khi bảng file-descriptor đầy.

**3. Buffer giới hạn.** Reader chấp nhận dữ liệu vô hạn trước khi framing
kịp xác thực là một công cụ DoS (slowloris: gửi một byte mỗi 59 giây mãi
mãi). Chính sách: trần kích thước khung, trần buffer, và đóng mọi kết nối
vượt một trong hai.

**4. Trạng thái sạch.** Máy trạng thái của giao thức — connected, awaiting
request, awaiting response, closed — phải tường minh, và mọi chuyển tiếp
phải với tới được bằng test. Các chế độ lỗi (ngắt giữa khung, timeout,
khung quá lớn, magic sai) mỗi cái ánh xạ tới một chuyển tiếp về `closed`
kèm lý do chẩn đoán.

Hợp đồng phía client phản chiếu: kết nối có timeout, ghi request có
framing, đọc có deadline, tương quan, dispose tất định. `EchoProtocol`
trong checkpoint là phiên bản nhỏ nhất trung thực của cả bốn tính chất;
các drill practice bổ sung thực tế dính khung của stream.
"""

_m19_failures = r"""## Network failure modes on localhost

Every distributed-systems failure has a miniature you can reproduce on
loopback — which is why this module works:

**Partial transfer.** Reader gets half a frame. Cause: stream semantics
(framing, above). Fix: buffering state machine. This is 90% of "random
protocol bug" reports.

**Slowloris / resource exhaustion.** Client opens many connections and
sends bytes slowly; server threads/buffers pile up. Fix: read deadlines +
connection caps + accept-loop isolation (one bad client cannot kill the
listener).

**Connection storms.** Client retries failing connections in a tight
loop; listener accept queue overflows; client sees connection-refused
storms. Fix: retry with backoff (Module 16) and treat refusal as a signal,
not a provocation.

**Head-of-line blocking.** One slow response delays every subsequent one
on the same connection. Fix: multiplexing (correlation IDs + concurrent
requests) or a connection pool. This tradeoff — one connection, ordered,
simple vs many connections, concurrent, complex — is the HTTP/1.1 →
HTTP/2 story, reproducible at 20 lines on loopback.

**The half-open problem.** Peer dies mid-request. Your read blocks
forever — TCP will not tell you for minutes. Fix: deadlines, period. The
`ReadWithDeadline` practice task is the muscle memory.

The habit these drills build: when a distributed failure appears in
production, reduce it to its loopback miniature, fix the miniature with a
test, then re-verify the real system. The failure catalog transfers; only
the timescales differ.
"""

_m19_failures_vi = r"""## Các chế độ lỗi mạng trên localhost

Mọi thất bại của hệ phân tán đều có một bản thu nhỏ tái hiện được trên
loopback — vì sao module này tồn tại:

**Truyền một phần.** Reader nhận nửa khung. Nguyên nhân: ngữ nghĩa stream
(framing, phía trên). Cách sửa: máy trạng thái buffer. Đây là 90% báo cáo
"bug giao thức ngẫu nhiên".

**Slowloris / cạn kiệt tài nguyên.** Client mở nhiều kết nối và gửi byte
rất chậm; thread/buffer của server dồn lại. Cách sửa: deadline khi đọc +
trần kết nối + cách ly vòng accept (một client xấu không thể giết
listener).

**Cơn bão kết nối.** Client retry các kết nối hỏng trong vòng kín; accept
queue của listener tràn; client thấy bão connection-refused. Cách sửa:
retry có backoff (Module 16) và coi refusal là tín hiệu, không phải lời
khiêu khích.

**Head-of-line blocking.** Một response chậm trì hoãn mọi response sau đó
trên cùng kết nối. Cách sửa: multiplexing (correlation ID + request đồng
thời) hoặc connection pool. Đánh đổi này — một kết nối, có thứ tự, đơn
giản vs nhiều kết nối, đồng thời, phức tạp — là câu chuyện HTTP/1.1 →
HTTP/2, tái hiện được trong 20 dòng trên loopback.

**Vấn đề nửa mở.** Peer chết giữa request. Lệnh đọc của bạn chặn vĩnh viễn
— TCP sẽ không báo bạn trong vài phút. Cách sửa: deadline, chấm hết.
Practice `ReadWithDeadline` chính là trí nhớ cơ bắp đó.

Thói quen mà các drill này xây nên: khi một lỗi phân tán xuất hiện trong
production, hãy thu nó về bản thu nhỏ trên loopback, sửa bản thu nhỏ kèm
test, rồi xác minh lại hệ thống thật. Danh mục lỗi chuyển giao được; chỉ
thang thời gian là khác nhau.
"""

_m19_checkpoint = r"""## Checkpoint: networking

The graded task builds the framing primitives (strict and tolerant
readers) plus a loopback echo protocol — the smallest complete
client/server with deadlines. Practice adds stream-gluing reality and
deadline enforcement as separate skills.
"""

_m19_checkpoint_vi = r"""## Checkpoint: networking

Bài được chấm xây các primitive framing (reader nghiêm ngặt và khoan dung)
cộng một giao thức echo trên loopback — client/server hoàn chỉnh nhỏ nhất
có deadline. Practice bổ sung thực tế dính khung và thi hành deadline
như hai kỹ năng riêng."""
