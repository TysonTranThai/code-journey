#!/usr/bin/env python3
"""Java — Advanced — Module 11: javaa-sockets-wire.

Real loopback TCP in the sandbox: sockets as byte streams, framing (the
newline protocol), read timeouts as the anti-hang device, half-close
semantics, and the checkpoint — a KV protocol server with a test client.
Loopback is verified-sandbox-safe; no egress anywhere. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "javaa-sockets-wire"

L_STREAM_EN = """
A TCP socket is *a byte stream with no message boundaries*. Write three
JSON objects to a socket and the reader may receive three chunks, one chunk,
or one-and-a-half — the network owes you neither your send boundaries nor
your read sizes. Everything message-shaped is YOUR protocol's job: framing.

```java
Socket s = new Socket("localhost", port);        // loopback: safe, instant
s.setSoTimeout(500);                             // read() throws after 500ms idle
BufferedReader in = new BufferedReader(
    new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8));
in.readLine();                                   // frame = "until newline"
```

The newline protocol is the classic first frame: sender appends `\\n`, reader
splits on it. It is text-only and it forbids embedded newlines — binary
protocols graduate to length prefixes (`[4-byte length][payload]`), which is
what HTTP/2 and every serious wire format do. Either way, the framing rule
belongs to the protocol, not the stream.

**Timeouts are survival**: a read against a silent peer blocks forever by
default. `setSoTimeout` bounds every read; production servers also bound
*idle* connections and *total request* time. A socket without a timeout is a
thread-leak with a delay.
"""
L_STREAM_VI = """
Socket TCP là *luồng byte không có ranh giới thông điệp*. Ghi ba đối tượng
JSON vào socket, người đọc có thể nhận ba khúc, một khúc, hoặc một-rưỡi —
mạng không nợ bạn ranh giới gửi lẫn kích thước đọc. Mọi thứ hình thông điệp
là việc của PROTOCOL của bạn: đóng khung.

```java
Socket s = new Socket("localhost", port);        // loopback: an toàn, tức thì
s.setSoTimeout(500);                             // read() ném sau 500ms im lặng
BufferedReader in = new BufferedReader(
    new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8));
in.readLine();                                   // khung = "cho tới newline"
```

Giao thức newline là khung kinh điển đầu tiên: người gửi thêm `\\n`, người đọc
tách theo nó. Nó chỉ dành cho văn bản và cấm newline lồng bên trong — giao
thức nhị phân tốt nghiệp sang length prefix (`[4 byte độ dài][payload]`),
đó là điều HTTP/2 và mọi wire format nghiêm túc làm. Dù cách nào, quy tắc
đóng khung thuộc về protocol, không thuộc về stream.

**Timeout là sự sống còn**: read vào một peer im lặng sẽ block vĩnh viễn theo
mặc định. `setSoTimeout` chặn trên mọi lần đọc; server production còn chặn
*kết nối rảnh* và *tổng thời gian xử lý yêu cầu*. Socket không có timeout là
một thread-leak có đặt hẹn giờ.
"""

L_LIFECYCLE_EN = """
Sockets have a *half-close*: `socket.shutdownOutput()` sends EOF to the peer
while your read direction stays open. It is the precise way to say "my
request is complete" — a one-shot command client writes its payload,
half-closes, reads the entire response until EOF. `close()` closes BOTH
directions and releases the descriptor.

The server side is `ServerSocket.accept()` — each accepted connection gets
its own `Socket`, and the classic model is a thread (or virtual thread) per
connection. With virtual threads (Module 5), thread-per-connection returns
to respectability: 10k concurrent connections with blocking-style code.

Accept/close hygiene: close the SERVER socket in finally (stops new
connections), close each client socket in finally (frees descriptors), and
never share one `Socket` object across threads without synchronization —
the streams are not thread-safe.
"""
L_LIFECYCLE_VI = """
Socket có *half-close*: `socket.shutdownOutput()` gửi EOF tới peer trong khi
chiều đọc của bạn vẫn mở. Đó là cách chính xác để nói "yêu cầu của tôi xong"
— một command client một-lần ghi payload, half-close, đọc toàn bộ phản hồi
cho tới EOF. `close()` đóng CẢ HAI chiều và trả descriptor.

Phía server là `ServerSocket.accept()` — mỗi kết nối được nhận cho ra một
`Socket` riêng, và mô hình kinh điển là một thread (hoặc virtual thread) mỗi
kết nối. Với virtual thread (Module 5), thread-per-kết nối trở lại đúng mực:
10k kết nối đồng thời với code kiểu blocking.

Vệ sinh accept/close: đóng socket SERVER trong finally (ngừng nhận kết nối
mới), đóng từng socket client trong finally (giải phóng descriptor), và không
bao giờ dùng chung một đối tượng `Socket` giữa các thread không có đồng bộ —
các stream không thread-safe.
"""

L_KV_EN = """
The checkpoint protocol — a KV store over TCP:

```text
client: PUT key value\n     server: OK\n
client: GET key\n           server: VALUE value\n   (or)  MISSING\n
client: QUIT\n              server: BYE\n  (then both close)
```

Design decisions worth noticing: the frame is a line (text protocol, easy to
debug with telnet); responses are SINGLE lines (the client never has to count
bytes); `QUIT` ends the session explicitly instead of relying on EOF races;
unknown commands answer `ERR` rather than hanging or crashing. A server loop:
accept → per-connection handler → read-line/write-line until QUIT/EOF. The
test client proves the whole loop over real loopback bytes.
"""
L_KV_VI = """
Giao thức của checkpoint — một KV store trên TCP:

```text
client: PUT key value\n     server: OK\n
client: GET key\n           server: VALUE value\n   (hoặc)  MISSING\n
client: QUIT\n              server: BYE\n  (rồi cả hai đóng)
```

Những quyết định thiết kế đáng chú ý: khung là một dòng (giao thức văn bản,
dễ debug bằng telnet); phản hồi là MỘT dòng (client không phải đếm byte);
`QUIT` kết thúc phiên tường minh thay vì dựa vào race EOF; lệnh lạ trả `ERR`
thay vì treo hoặc crash. Vòng lặp server: accept → handler mỗi kết nối →
read-line/write-line cho tới QUIT/EOF. Client kiểm thử chứng minh toàn bộ
vòng lặp trên byte loopback thật.
"""

write_module(
    M, "Sockets & the Wire",
    "Loopback TCP: streams without boundaries, framing, timeouts, half-close, and a KV protocol.",
    "Socket & Giao thức dây",
    "TCP loopback: luồng không ranh giới, đóng khung, timeout, half-close, và giao thức KV.",
    ["javaa-socket-streams", "javaa-socket-lifecycle", "javaa-kv-protocol"],
    ["javaa-p11-sockets"],
)

write_lesson(M, "javaa-socket-streams",
    "Streams without boundaries",
    "Why the network owes you no framing, newline vs length-prefix protocols, and read timeouts.",
    16, L_STREAM_EN,
    "Luồng không ranh giới",
    "Vì sao mạng không nợ bạn đóng khung, newline vs length-prefix, và read timeout.",
    L_STREAM_VI)

write_lesson(M, "javaa-socket-lifecycle",
    "Lifecycle and half-close",
    "shutdownOutput vs close, the accept loop, and descriptor hygiene.",
    14, L_LIFECYCLE_EN,
    "Vòng đời và half-close",
    "shutdownOutput vs close, vòng lặp accept, và vệ sinh descriptor.",
    L_LIFECYCLE_VI)

write_lesson(M, "javaa-kv-protocol",
    "Designing a line protocol",
    "A KV exchange where every decision — frames, single-line responses, QUIT, ERR — is visible.",
    16, L_KV_EN,
    "Thiết kế giao thức dòng",
    "Trao đổi KV mà mọi quyết định — khung, phản hồi một dòng, QUIT, ERR — đều hiện rõ.",
    L_KV_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_ECHO = challenge(
    "javaa-p11-echo",
    "A framed echo server",
    "1. `static String frame(String message)` — return the wire form: message + \"\\n\".\n"
    "2. `static java.util.List<String> deframe(String received)` — split a received chunk\n"
    "into complete frames: split on \"\\n\" and DROP a trailing fragment that lacks its\n"
    "terminator (an incomplete frame is not a frame). Empty input → empty list.\n"
    "3. `static byte[] lengthFrame(String payload)` — binary framing: 4-byte big-endian\n"
    "length prefix followed by UTF-8 payload bytes.\n"
    "4. `static int prefixLength(byte[] framed)` — read the 4-byte big-endian prefix back.",
    P_BOILER,
    [
        ("newline framing round-trips", r"""
checkEq(Solution.frame("hi"), "hi\n", "newline appended");
checkEq(Solution.deframe("a\nb\nc"), java.util.List.of("a", "b"), "torn tail dropped");
checkEq(Solution.deframe(""), java.util.List.of(), "empty in, empty out");
""", "Frames are terminated or absent."),
        ("length-prefix framing", r"""
byte[] f = Solution.lengthFrame("héllo");
checkEq(Solution.prefixLength(f), f.length - 4, "prefix counts payload bytes");
checkTrue(new String(f, 4, f.length - 4, java.nio.charset.StandardCharsets.UTF_8).equals("héllo"),
    "payload intact");
""", "The prefix is arithmetic, not guesswork."),
    ],
    level="guided",
)
CH_ECHO_VI = vi_challenge(
    "Echo server có đóng khung",
    "frame/deframe/lengthFrame/prefixLength: khung là có kết thúc hoặc không tồn tại; prefix là phép tính, không phải phỏng đoán.",
    [("Khung newline khép kín", "Đuôi rách bị bỏ; rỗng vào rỗng ra."),
     ("Đóng khung length-prefix", "Prefix đếm byte payload.")],
)

CH_TIMEOUT = challenge(
    "javaa-p11-timeout",
    "Timeouts are survival",
    "1. `static int readWithBudget(java.io.Reader r, int budgetChars)` — read up to\n"
    "budgetChars characters into a String, then return the string LENGTH (simulates a\n"
    "bounded read; use the reader's real read(char[]) loop).\n"
    "2. `static long elapsedOf(java.util.function.Supplier<?> work)` — nanoTime around\n"
    "work.get(), return elapsed nanos (the shape of every timeout guard).\n"
    "3. `static String statusFor(long elapsedNanos, long deadlineNanos)` — return\n"
    "\"ok\" if elapsed <= deadline else \"timeout\".",
    P_BOILER,
    [
        ("bounded reads and deadline checks", r"""
java.io.Reader r = new java.io.StringReader("abcdef");
checkEq(Solution.readWithBudget(r, 4), 4, "budget bounds the read");
checkTrue(Solution.elapsedOf(() -> 42) >= 0, "elapsed measured");
checkEq(Solution.statusFor(50, 100), "ok", "within deadline");
checkEq(Solution.statusFor(150, 100), "timeout", "past deadline");
""", "Every read has a budget; every op has a deadline."),
    ],
    level="independent",
)
CH_TIMEOUT_VI = vi_challenge(
    "Timeout là sự sống còn",
    "readWithBudget/elapsedOf/statusFor: mọi lần đọc có ngân sách, mọi phép toán có hạn chót.",
    [("Đọc có chặn trên", "Ngân sách chặn lần đọc."),
     ("Kiểm hạn chót", "Quá hạn là timeout, trong hạn là ok.")],
)

write_practice(M, "javaa-p11-sockets",
    "Socket drills",
    "Framing, budgets, and deadlines — the discipline before real sockets.",
    "Bài tập socket",
    "Đóng khung, ngân sách, và hạn chót — kỷ luật trước khi tới socket thật.",
    "javaa-kv-protocol", 50, "advanced",
    [CH_ECHO, CH_TIMEOUT],
    {"javaa-p11-echo": CH_ECHO_VI, "javaa-p11-timeout": CH_TIMEOUT_VI},
    solutions=[
        ("javaa-p11-echo", r"""
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class Solution {
    public static String frame(String message) {
        return message + "\n";
    }

    public static List<String> deframe(String received) {
        if (received.isEmpty()) return List.of();
        boolean torn = !received.endsWith("\n");
        String[] parts = received.split("\n", -1);
        List<String> frames = new ArrayList<>();
        int limit = torn ? parts.length - 1 : (parts[parts.length - 1].isEmpty() ? parts.length - 1 : parts.length);
        for (int i = 0; i < limit; i++) {
            if (!parts[i].isEmpty()) frames.add(parts[i]);
        }
        return frames;
    }

    public static byte[] lengthFrame(String payload) {
        byte[] body = payload.getBytes(StandardCharsets.UTF_8);
        byte[] framed = new byte[4 + body.length];
        framed[0] = (byte) ((body.length >>> 24) & 0xFF);
        framed[1] = (byte) ((body.length >>> 16) & 0xFF);
        framed[2] = (byte) ((body.length >>> 8) & 0xFF);
        framed[3] = (byte) (body.length & 0xFF);
        System.arraycopy(body, 0, framed, 4, body.length);
        return framed;
    }

    public static int prefixLength(byte[] framed) {
        return ((framed[0] & 0xFF) << 24) | ((framed[1] & 0xFF) << 16)
             | ((framed[2] & 0xFF) << 8)  | (framed[3] & 0xFF);
    }
}
""", r"""
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class Solution {
    public static String frame(String message) {
        return message;   // WRONG: no terminator — the reader can never frame it
    }

    public static List<String> deframe(String received) {
        if (received.isEmpty()) return List.of();
        return new ArrayList<>(List.of(received.split("\n")));   // WRONG: torn tail becomes a frame
    }

    public static byte[] lengthFrame(String payload) {
        byte[] body = payload.getBytes(StandardCharsets.UTF_8);
        byte[] framed = new byte[4 + body.length];
        framed[0] = (byte) (body.length % 256);   // WRONG: only the low byte — truncates above 255
        System.arraycopy(body, 0, framed, 4, body.length);
        return framed;
    }

    public static int prefixLength(byte[] framed) {
        return framed[0] & 0xFF;   // WRONG: reads one byte, not four
    }
}
"""),
        ("javaa-p11-timeout", r"""
import java.io.*;
import java.util.function.Supplier;

public class Solution {
    public static int readWithBudget(Reader r, int budgetChars) throws Exception {
        char[] buf = new char[budgetChars];
        StringBuilder out = new StringBuilder();
        int n;
        while (out.length() < budgetChars && (n = r.read(buf, 0, budgetChars - out.length())) != -1) {
            out.append(buf, 0, n);
        }
        return out.length();
    }

    public static long elapsedOf(Supplier<?> work) {
        long t0 = System.nanoTime();
        work.get();
        return System.nanoTime() - t0;
    }

    public static String statusFor(long elapsedNanos, long deadlineNanos) {
        return elapsedNanos <= deadlineNanos ? "ok" : "timeout";
    }
}
""", r"""
import java.io.*;
import java.util.function.Supplier;

public class Solution {
    public static int readWithBudget(Reader r, int budgetChars) throws Exception {
        int total = 0;
        while (r.read() != -1) {   // WRONG: unbounded — ignores the budget entirely
            total++;
        }
        return total;
    }

    public static long elapsedOf(Supplier<?> work) {
        work.get();
        return 0;   // WRONG: no measurement — the guard is decorative
    }

    public static String statusFor(long elapsedNanos, long deadlineNanos) {
        return "ok";   // WRONG: deadlines never fire
    }
}
"""),
    ],
)

CP_MD = """
## Checkpoint: the KV protocol over real loopback

A real `ServerSocket`, real clients, real bytes — the full accept/frame/
respond loop with a strict line protocol, exercised in-sandbox.
"""

CP_CH = challenge(
    "javaa-checkpoint-m11-task",
    "Checkpoint: KV over TCP",
    "Inside Solution, implement the protocol engine and prove it over loopback:\n"
    "1. `static String handle(String line, java.util.Map<String, String> store)` — one\n"
    "protocol turn: parse the command, mutate/query the store, return the response LINE\n"
    "(no newline included). Rules: `PUT k v` → \"OK\"; `GET k` → \"VALUE v\" or \"MISSING\";\n"
    "`QUIT` → \"BYE\"; anything else (including empty and unknown commands) → \"ERR\".\n"
    "PUT with a value containing spaces: store everything after the second token.\n"
    "2. `static int serveOnce(int port)` — full loop: open ServerSocket on the port,\n"
    "accept ONE client, serve handle() per received line (store persists across lines\n"
    "within the session), write each response with \"\\n\" framing, stop after BYE, close\n"
    "everything in finally, return the number of protocol turns served. Use a 5s\n"
    "soTimeout so a wedged client cannot hang the run. Runs in the calling thread —\n"
    "the TEST connects from the same JVM via loopback.",
    P_BOILER,
    [
        ("the protocol engine", r"""
java.util.Map<String, String> store = new java.util.HashMap<>();
checkEq(Solution.handle("PUT a 1", store), "OK", "put accepted");
checkEq(Solution.handle("GET a", store), "VALUE 1", "get returns stored");
checkEq(Solution.handle("GET zz", store), "MISSING", "absent key");
checkEq(Solution.handle("NONSENSE", store), "ERR", "unknown command");
checkEq(Solution.handle("QUIT", store), "BYE", "session ends");
""", "Every command has exactly one answer."),
        ("over real loopback bytes", r"""
int port = 45321 + (int) (System.nanoTime() % 1000);
Thread server = Thread.ofVirtual().start(() -> {
    try { Solution.serveOnce(port); } catch (Exception ignored) { }
});
Thread.sleep(300);   // let the server bind
try (java.net.Socket s = new java.net.Socket("localhost", port)) {
    s.setSoTimeout(5000);
    var out = new java.io.PrintWriter(s.getOutputStream(), true, java.nio.charset.StandardCharsets.UTF_8);
    var in = new java.io.BufferedReader(new java.io.InputStreamReader(s.getInputStream(), java.nio.charset.StandardCharsets.UTF_8));
    out.println("PUT name buffy");
    checkEq(in.readLine(), "OK", "server answered OK");
    out.println("GET name");
    checkEq(in.readLine(), "VALUE buffy", "value over the wire");
    out.println("QUIT");
    checkEq(in.readLine(), "BYE", "clean goodbye");
}
server.join(5000);
checkTrue(true, "session complete");
""", "The full stack: sockets, framing, protocol, state."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: KV trên TCP",
    "handle: mỗi lệnh đúng một câu trả lời; serveOnce: vòng accept/frame/respond thật qua loopback với soTimeout.",
    [("Bộ máy giao thức", "Mỗi lệnh có đúng một câu trả lời."),
     ("Qua byte loopback thật", "Cả ngăn xếp: socket, khung, giao thức, trạng thái.")],
)

write_checkpoint(M, "javaa-checkpoint-m11",
    "Checkpoint: KV Over TCP",
    "A line protocol served over real loopback sockets, end to end.",
    30, CP_MD,
    "Checkpoint: KV trên TCP",
    "Giao thức dòng phục vụ qua socket loopback thật, từ đầu đến cuối.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class Solution {
    public static String handle(String line, Map<String, String> store) {
        if (line == null) return "ERR";
        String trimmed = line.trim();
        if (trimmed.isEmpty()) return "ERR";
        if (trimmed.equals("QUIT")) return "BYE";
        String[] parts = trimmed.split(" ", 3);
        String cmd = parts[0];
        if (cmd.equals("PUT") && parts.length == 3) {
            store.put(parts[1], parts[2]);
            return "OK";
        }
        if (cmd.equals("GET") && parts.length == 2) {
            String v = store.get(parts[1]);
            return v == null ? "MISSING" : "VALUE " + v;
        }
        return "ERR";
    }

    public static int serveOnce(int port) throws Exception {
        int turns = 0;
        try (ServerSocket server = new ServerSocket(port)) {
            server.setSoTimeout(10_000);
            try (Socket client = server.accept()) {
                client.setSoTimeout(5_000);
                BufferedReader in = new BufferedReader(
                    new InputStreamReader(client.getInputStream(), StandardCharsets.UTF_8));
                PrintWriter out = new PrintWriter(
                    new OutputStreamWriter(client.getOutputStream(), StandardCharsets.UTF_8), true);
                Map<String, String> store = new HashMap<>();
                String line;
                boolean done = false;
                while (!done && (line = in.readLine()) != null) {
                    String response = handle(line, store);
                    turns++;
                    out.println(response);
                    if (response.equals("BYE")) done = true;
                }
            }
        }
        return turns;
    }
}
""", wrong=r"""
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class Solution {
    public static String handle(String line, Map<String, String> store) {
        if (line == null) return "ERR";
        String trimmed = line.trim();
        if (trimmed.isEmpty()) return "ERR";
        if (trimmed.equals("QUIT")) return "BYE";
        String[] parts = trimmed.split(" ", 2);   // WRONG: splits into 2 — PUT loses multi-word values
        String cmd = parts[0];
        if (cmd.equals("PUT") && parts.length == 2) {
            String[] kv = parts[1].split(" ", 2);
            store.put(kv[0], kv.length > 1 ? kv[1] : "");
            return "OK";
        }
        if (cmd.equals("GET")) {
            String key = trimmed.substring(3).trim();
            String v = store.get(key);
            return v == null ? "MISSING" : "VALUE " + v;
        }
        return "OK";   // WRONG: unknown commands answer OK instead of ERR
    }

    public static int serveOnce(int port) throws Exception {
        int turns = 0;
        try (ServerSocket server = new ServerSocket(port)) {
            try (Socket client = server.accept()) {
                // WRONG: no soTimeout — a wedged client hangs the run forever
                BufferedReader in = new BufferedReader(
                    new InputStreamReader(client.getInputStream(), StandardCharsets.UTF_8));
                PrintWriter out = new PrintWriter(
                    new OutputStreamWriter(client.getOutputStream(), StandardCharsets.UTF_8), true);
                Map<String, String> store = new HashMap<>();
                String line;
                while ((line = in.readLine()) != null) {   // WRONG: never stops at BYE
                    turns++;
                    out.println(handle(line, store));
                }
            }
        }
        return turns;
    }
}
""")

print("module 11 authored")
