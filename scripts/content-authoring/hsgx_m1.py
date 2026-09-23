#!/usr/bin/env python3
"""HSG Intensive — Module 1: hsgx-recognition (Problem Recognition).

Reading the problem before the algorithm: the three-pass reading pass,
recognition signals (constraint ranges, structure words, query shapes), and
the two core reference materials (Algorithm Selection Guide + Complexity
Cheat Sheet). Every drill hides the topic — the student must name the tool.

Conventions (same as hsga_*): zero literal backslashes. Test input AND want
use real newlines via T(); C++ bodies via cpp() turning {{NL}} into \n escapes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgx import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, contest_test, recognition_drill,
)

Q = chr(92)
NL = chr(10)


def cpp(s):
    return s.replace("{{NL}}", Q + "n")


def T(*lines):
    return "".join(l + NL for l in lines)


# NOTE: solutions use explicit includes (hsga pattern) — solution.cpp is
# compiled INTO the QA harness TU (which pre-includes the std headers), and
# the local QA toolchain (Apple clang) lacks bits/stdc++.h.
CPP_STD = cpp("""#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <utility>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL


def letter(l):
    # bare letter, no newline — contest_test builds want via T() (no trailing NL)
    return CPP_STD + cpp('    out << "' + l + '";') + END


M = "hsgx-recognition"
write_module(
    M,
    "Problem Recognition",
    "Read a problem before knowing its topic: the three-pass reading method, the constraint-to-algorithm reflex, and the recognition signals that reveal which tool the setter had in mind.",
    "Nhận diện bài toán",
    "Đọc đề trước khi biết chủ đề: phương pháp đọc ba lượt, phản xạ chuyển giới hạn thành thuật toán, và các tín hiệu nhận diện cho biết đề muốn gì.",
    ["hsgx-m1-reading", "hsgx-m1-signals", "hsgx-cp-m1"],
    ["hsgx-p1-drills"],
)

# ------------------------------------------------------------------ lessons
write_lesson(
    M, "hsgx-m1-reading",
    "Three-Pass Reading",
    "How contest solvers actually read a problem: story, constraints, examples — three passes with three different questions.",
    20,
    """
# Three-Pass Reading

Fast solvers do not read a problem once. They read it **three times**, asking
a different question each pass.

## Pass 1 — What is the shape?

Skip the story. Find: what is given (n, m, arrays, graph), what is asked
(count? construct? maximize? minimum possible x?), and the constraint table.
Write down the *shape* in one line: `n ≤ 2·10^5, q ≤ 2·10^5, range add,
range sum` is a shape; "orcs attack villages" is not.

## Pass 2 — What do the examples say?

Recompute every sample **by hand**. Two reasons: it verifies you understood
the operation, and samples hide edge cases (a sample where the answer is 0 is
telling you 0 is possible). If your mental model cannot reproduce the
samples, you are not ready to think about algorithms.

## Pass 3 — What fits the budget?

Convert constraints to a complexity budget (next lesson covers the table).
Then ask: which family has that complexity *and* matches the shape? If
n ≤ 20, almost anything works — the setter is testing correct brute force.
If n ≤ 2·10^5 with queries interleaved, only O((n+q) log n)-ish survives.

## The Algorithm Selection Guide (keep this)

| If you see | Consider (in order) |
|---|---|
| n ≤ 20 | brute force / bitmask enumeration |
| n ≤ 500, pairs | O(n^2) DP or Floyd-Warshall |
| n ≤ 5000, sequences | O(n^2) DP, divide and conquer |
| n ≤ 2·10^5, offline | sorting + two pointers, sweep line |
| range add / range sum | Fenwick (BIT) or lazy segment tree |
| static range min | sparse table |
| connectivity, edges only added | DSU |
| shortest path, non-negative weights | Dijkstra |
| shortest path, unit weights | BFS |
| unweighted, 0/1 weights | 0-1 BFS |
| all-pairs small n | Floyd-Warshall |
| spanning tree weight | Kruskal / Prim |
| strongly connected components | Kosaraju / Tarjan |
| k-th element online | balanced BST / Fenwick descent / merge sort tree |
| count pairs i<j with condition | sort + Fenwick (inversion-style) |
| pattern occurrences in text | KMP / Z-function |
| count numbers ≤ N with digit property | digit DP |
| assignment / pairing | bipartite matching, flow |
| game, piles, last move wins | Nim / Grundy (XOR) |
| geometry, minimize distance | sweep + closest pair, binary search |
| answer is monotone in x | binary search on answer |

The table is a *shortlist generator*, not an answer key. Drills in this
module train the reflex; later modules train the verification (does the
family actually fit the operation semantics?).
""",
    "Đọc đề ba lượt",
    "Solver thi đấu thực sự đọc bài ba lần, mỗi lượt một câu hỏi khác nhau.",
    """
# Đọc đề ba lượt

Solver nhanh không đọc đề một lần. Họ đọc **ba lượt**, mỗi lượt một câu hỏi.

## Lượt 1 — Bài có dạng gì?

Bỏ qua cốt truyện. Tìm: dữ liệu cho trước (n, m, mảng, đồ thị), cái được hỏi
(đếm? dựng? tối đa? giá trị x nhỏ nhất?), và bảng giới hạn. Viết *dạng* bài
trong một dòng: `n ≤ 2·10^5, q ≤ 2·10^5, cập nhật đoạn, tổng đoạn` là một
dạng; "orcs tấn công làng" thì không.

## Lượt 2 — Ví dụ nói gì?

Tính lại **từng ví dụ bằng tay**. Hai lý do: xác nhận bạn hiểu đúng phép
toán, và ví dụ giấu test biên (một ví dụ có đáp án 0 đang nói với bạn rằng 0
là khả thi). Nếu mô hình trong đầu không tái tạo được ví dụ, bạn chưa sẵn
sàng nghĩ về thuật toán.

## Lượt 3 — Cái gì vừa với ngân sách?

Chuyển giới hạn thành ngân sách độ phức tạp (bảng ở bài sau). Sau đó hỏi:
họ thuật toán nào vừa ngân sách *và* khớp dạng bài? Nếu n ≤ 20, gần như
thuật nào cũng chạy — người ra đề đang kiểm tra brute force đúng. Nếu
n ≤ 2·10^5 với truy vấn xen kẽ, chỉ O((n+q) log n)-ish là sống sót.

## Bảng chọn thuật toán (hãy giữ lại)

| Nếu bạn thấy | Cân nhắc (theo thứ tự) |
|---|---|
| n ≤ 20 | brute force / liệt kê bitmask |
| n ≤ 500, xét từng cặp | DP O(n^2) hoặc Floyd-Warshall |
| n ≤ 5000, dãy | DP O(n^2), chia để trị |
| n ≤ 2·10^5, offline | sắp xếp + two pointers, quét đường thẳng |
| cập nhật đoạn / tổng đoạn | Fenwick (BIT) hoặc segment tree lazy |
| min đoạn tĩnh | sparse table |
| liên thông, chỉ thêm cạnh | DSU |
| đường đi ngắn nhất, trọng số không âm | Dijkstra |
| đường đi ngắn nhất, trọng số 1 | BFS |
| trọng số 0/1 | 0-1 BFS |
| mọi cặp đỉnh, n nhỏ | Floyd-Warshall |
| cây khung nhỏ nhất | Kruskal / Prim |
| thành phần liên thông mạnh | Kosaraju / Tarjan |
| phần tử thứ k trực tuyến | BST cân bằng / Fenwick descent / merge sort tree |
| đếm cặp i<j theo điều kiện | sort + Fenwick (kiểu nghịch thế) |
| số lần xuất hiện của mẫu trong xâu | KMP / Z-function |
| đếm số ≤ N theo tính chất chữ số | digit DP |
| ghép cặp / phân công | ghép đôi hai phía, flow |
| trò chơi, đống đá, người cuối thắng | Nim / Grundy (XOR) |
| hình học, khoảng cách nhỏ nhất | quét + cặp điểm gần nhất, tìm kiếm nhị phân |
| đáp án đơn điệu theo x | tìm kiếm nhị phân trên đáp án |

Bảng chỉ là *bộ sinh ứng cử viên*, không phải đáp án. Drill trong module này
luyện phản xạ; các module sau luyện kiểm chứng (họ thuật toán có thật sự vừa
với ngữ nghĩa phép toán không?).
""",
)

write_lesson(
    M, "hsgx-m1-signals",
    "Recognition Signals",
    "The recurring fingerprints: constraint ranges, update/query patterns, and structure words — and how distractors are built.",
    20,
    """
# Recognition Signals

Setters hide the topic, but fingerprints survive the disguise.

## Signal 1 — The constraint range

- **n ≤ 20**: exponential intended. 2^n with small constant is fine.
- **n ≤ 500**: O(n^3) intended (Floyd, assignment DP).
- **n ≤ 5000**: O(n^2) intended.
- **n ≤ 10^5 – 2·10^5**: O(n log n) intended — data structures, sorting,
  Dijkstra with heap.
- **n ≤ 10^6+**: linear — two pointers, sieve, KMP, prefix sums.
- **value ≤ 10^9 but n small**: the *values* are not the state; maybe the
  answer is binary-searchable, or compress coordinates.
- **N ≤ 10^18**: log-scale — digit DP, binary search, matrix power.

## Signal 2 — The update/query pattern

- **interleaved updates + range queries**: segment tree family.
- **only prefix queries after building**: prefix sums, no tree needed.
- **edge additions, connectivity queries, no deletions**: DSU. (Deletions?
  DSU breaks — think offline reverse-time or link-cut trees.)
- **(l, r, k) style queries**: offline + Fenwick over values, or merge sort
  tree / wavelet tree if forced online.
- **min over all pairs / nearest**: sort + sweep, or binary search on answer.

## Signal 3 — Structure words and their translations

- "minimum time so that all ..." → binary search on the answer, then a
  feasibility check (greedy or graph search).
- "count the number of ways" → DP almost surely; find the *order* that makes
  subproblems independent.
- "choose a subset such that ..." with n ≤ 30 → meet in the middle.
- "for each i, the nearest j > i with ..." → monotonic stack or set descent.
- "game, two players, optimal play" → game theory: symmetric positions, XOR
  of Grundy numbers.
- "guaranteed the graph is a DAG" → topological DP.
- "tree, queries on paths" → LCA; path *updates* → HLD.

## How distractors work (and why drills use them)

Multiple-choice drills here are not a quiz format — they train *elimination*.
The tempting wrong option is always the one that matches the story but not
the constraint: prefix sums when updates are interleaved; BFS when weights
exist; greedy when the exchange argument fails. In the exam the distractors
are your own first ideas — eliminating them fast is the skill.

## Exercise before the drill set

Take any problem you solved last month. Write its shape in one line, the
constraint budget, and the family you used. Then write the *second* family
you considered and why it lost. Recognition is exactly this comparison,
executed in seconds.
""",
    "Tín hiệu nhận diện",
    "Các dấu vân tay lặp lại: dải giới hạn, mẫu cập nhật/truy vấn, và từ khóa cấu trúc — cùng cách xây phương án gây nhiễu.",
    """
# Tín hiệu nhận diện

Người ra đề giấu chủ đề, nhưng dấu vân tay vẫn còn.

## Tín hiệu 1 — Dải giới hạn

- **n ≤ 20**: chủ đích là mũ. 2^n với hằng số nhỏ là đủ.
- **n ≤ 500**: chủ đích O(n^3) (Floyd, DP phân công).
- **n ≤ 5000**: chủ đích O(n^2).
- **n ≤ 10^5 – 2·10^5**: chủ đích O(n log n) — cấu trúc dữ liệu, sắp xếp,
  Dijkstra với heap.
- **n ≤ 10^6+**: tuyến tính — two pointers, sàng, KMP, tổng tiền tố.
- **giá trị ≤ 10^9 nhưng n nhỏ**: *giá trị* không phải trạng thái; có thể
  đáp án đơn điệu để tìm kiếm nhị phân, hoặc nén tọa độ.
- **N ≤ 10^18**: thang log — digit DP, tìm kiếm nhị phân, lũy thừa ma trận.

## Tín hiệu 2 — Mẫu cập nhật/truy vấn

- **cập nhật + truy vấn đoạn xen kẽ**: họ segment tree.
- **chỉ truy vấn tiền tố sau khi dựng**: tổng tiền tố, không cần cây.
- **thêm cạnh + truy vấn liên thông, không xóa**: DSU. (Có xóa? DSU gãy —
  nghĩ offline đảo thời gian hoặc link-cut tree.)
- **truy vấn dạng (l, r, k)**: offline + Fenwick trên giá trị, hoặc merge
  sort tree / wavelet tree nếu bắt buộc trực tuyến.
- **min trên mọi cặp / gần nhất**: sort + quét, hoặc tìm kiếm nhị phân đáp án.

## Tín hiệu 3 — Từ khóa cấu trúc và bản dịch

- "thời gian nhỏ nhất để tất cả ..." → tìm kiếm nhị phân đáp án, rồi kiểm tra
  khả thi (greedy hoặc duyệt đồ thị).
- "đếm số cách" → gần như chắc chắn DP; tìm *thứ tự* khiến bài con độc lập.
- "chọn tập con sao cho ..." với n ≤ 30 → meet in the middle.
- "với mỗi i, j gần nhất > i sao cho ..." → stack đơn điệu hoặc set descent.
- "trò chơi, hai người, chơi tối ưu" → lý thuyết trò chơi: vị trí đối xứng,
  XOR các số Grundy.
- "đảm bảo đồ thị là DAG" → DP trên thứ tự tô-pô.
- "cây, truy vấn trên đường đi" → LCA; *cập nhật* đường đi → HLD.

## Phương án gây nhiễu hoạt động thế nào (vì sao drill dùng nó)

Drill trắc nghiệm ở đây không phải dạng kiểm tra — nó luyện *loại trừ*.
Phương án sai gây nhiễu luôn là cái khớp cốt truyện nhưng không khớp giới
hạn: tổng tiền tố khi cập nhật xen kẽ; BFS khi có trọng số; greedy khi lập
luận đổi chỗ thất bại. Trong phòng thi, phương án nhiễu chính là ý đầu tiên
của bạn — loại nhanh chúng là kỹ năng cần luyện.

## Bài tập trước bộ drill

Lấy một bài bạn đã giải tháng trước. Viết dạng bài trong một dòng, ngân sách
giới hạn, và họ thuật toán bạn dùng. Sau đó viết *họ thứ hai* bạn từng cân
nhắc và vì sao nó thua. Nhận diện chính là phép so sánh này, thực hiện trong
vài giây.
""",
)

# ----------------------------------------------------------------- practice
D1, D1VI = recognition_drill(
    "hsgx-p1-d1", "Range Add, Range Sum",
    "An array of n ≤ 200000 integers. q ≤ 200000 operations, interleaved: `1 l r x` adds x to every a[l..r]; `2 l r` prints the sum of a[l..r].",
    ["Static prefix sums, rebuilt after each update",
     "Fenwick tree (two-BIT range trick) or lazy segment tree",
     "Dijkstra from node l",
     "Sort the array and use two pointers"],
    "B",
    "Interleaved range update + range query kills static prefix sums — you need a structure with O(log n) update and query.",
    vi_title="Cập nhật đoạn, tổng đoạn",
    vi_scenario="Mảng n ≤ 200000 phần tử. q ≤ 200000 thao tác xen kẽ: `1 l r x` cộng x vào mọi a[l..r]; `2 l r` in tổng a[l..r].",
    vi_options=["Tổng tiền tố tĩnh, dựng lại sau mỗi cập nhật",
                "Cây Fenwick (mẹo hai BIT cho đoạn) hoặc segment tree lazy",
                "Dijkstra từ đỉnh l",
                "Sắp xếp mảng rồi two pointers"],
    vi_hint="Cập nhật đoạn + truy vấn đoạn xen kẽ hạ tổng tiền tố tĩnh — cần cấu trúc có cập nhật và truy vấn O(log n).",
)
D2, D2VI = recognition_drill(
    "hsgx-p1-d2", "Weighted Shortest Path",
    "A directed graph with n ≤ 100000 vertices, m ≤ 200000 edges, positive integer weights. For one source s, print the shortest distance to every vertex.",
    ["BFS from s",
     "Kruskal minimum spanning tree",
     "Dijkstra with a priority queue",
     "DSU with path compression"],
    "C",
    "Weights are positive and arbitrary — BFS only works on unit weights; Dijkstra with a heap is the fit.",
    vi_title="Đường đi ngắn nhất có trọng số",
    vi_scenario="Đồ thị có hướng n ≤ 100000 đỉnh, m ≤ 200000 cạnh, trọng số nguyên dương. Từ một đỉnh s, in khoảng cách ngắn nhất tới mọi đỉnh.",
    vi_options=["BFS từ s",
                "Cây khung nhỏ nhất Kruskal",
                "Dijkstra với hàng đợi ưu tiên",
                "DSU với nén đường"],
    vi_hint="Trọng số dương tùy ý — BFS chỉ đúng với trọng số 1; Dijkstra với heap là lựa chọn phù hợp.",
)
D3, D3VI = recognition_drill(
    "hsgx-p1-d3", "Count Pattern Occurrences",
    "Text s with |s| ≤ 1000000 and pattern p with |p| ≤ 100000, both over lowercase letters. Count how many times p occurs in s.",
    ["Check every starting position (|s|·|p| comparisons)",
     "KMP prefix function over p + '#' + s",
     "Digit DP over the string",
     "Kruskal on the characters"],
    "B",
    "|s| up to 10^6 demands linear time — the KMP prefix function reports every occurrence in O(|s| + |p|).",
    vi_title="Đếm số lần xuất hiện của mẫu",
    vi_scenario="Xâu s với |s| ≤ 1000000 và mẫu p với |p| ≤ 100000, đều gồm chữ cái thường. Đếm số lần p xuất hiện trong s.",
    vi_options=["Thử mọi vị trí xuất phát (|s|·|p| phép so)",
                "Hàm tiền tố KMP trên p + '#' + s",
                "Digit DP trên xâu",
                "Kruskal trên các ký tự"],
    vi_hint="|s| tới 10^6 đòi hỏi tuyến tính — hàm tiền tố KMP báo mọi lần xuất hiện trong O(|s| + |p|).",
)
D4, D4VI = recognition_drill(
    "hsgx-p1-d4", "Count Target Pairs",
    "Given n ≤ 200000 integers a[i] and a target x, count the pairs i < j with a[i] + a[j] = x.",
    ["Nested loops over all pairs",
     "Sort, then two pointers from both ends",
     "Segment tree with lazy propagation",
     "Binary search on the answer"],
    "B",
    "n^2 pairs is 4·10^10 — too slow. After sorting, the two-pointer sweep counts pairs in O(n log n).",
    vi_title="Đếm cặp có tổng đúng",
    vi_scenario="Cho n ≤ 200000 số nguyên a[i] và đích x, đếm các cặp i < j với a[i] + a[j] = x.",
    vi_options=["Vòng lặp lồng trên mọi cặp",
                "Sắp xếp, rồi two pointers từ hai đầu",
                "Segment tree với lazy propagation",
                "Tìm kiếm nhị phân trên đáp án"],
    vi_hint="n^2 cặp là 4·10^10 — quá chậm. Sau khi sắp xếp, quét two pointers đếm cặp trong O(n log n).",
)
D5, D5VI = recognition_drill(
    "hsgx-p1-d5", "Assign Workers to Jobs",
    "n ≤ 500 workers, n ≤ 500 jobs; worker i can do job j iff edge (i, j) exists. Maximize the number of filled jobs.",
    ["Greedy: everyone takes their first available job",
     "Kruskal spanning tree on workers",
     "Bipartite matching with augmenting paths (Kuhn / Hopcroft-Karp)",
     "Prefix sums over workers"],
    "C",
    "Bipartite structure + maximize assignments = matching. Greedy fails the classic two-way conflict; augmenting paths fix it.",
    vi_title="Phân công công nhân việc",
    vi_scenario="n ≤ 500 công nhân, n ≤ 500 việc; công nhân i làm được việc j khi và chỉ khi có cạnh (i, j). Tối đa hóa số việc được nhận.",
    vi_options=["Greedy: mỗi người lấy việc trống đầu tiên",
                "Cây khung Kruskal trên công nhân",
                "Ghép đôi hai phía bằng đường tăngiana (Kuhn / Hopcroft-Karp)",
                "Tổng tiền tố trên công nhân"],
    vi_hint="Cấu trúc hai phía + tối đa phân công = ghép đôi. Greedy gãy ở xung đột hai chiều kinh điển; đường tăngiana xử lý được.",
)
D6, D6VI = recognition_drill(
    "hsgx-p1-d6", "The Stone Game",
    "n ≤ 100000 piles of stones; two players alternate removing any positive number of stones from one pile; the player taking the last stone wins. Both play optimally. Who wins?",
    ["Simulate the game with BFS over pile states",
     "XOR of all pile sizes: first player wins iff nonzero",
     "Sort piles and greedy the largest",
     "Dijkstra on the state graph"],
    "B",
    "This is exactly Nim: a position is losing iff the XOR of pile sizes is 0. Simulation of the full state space is exponential.",
    vi_title="Trò chơi đá",
    vi_scenario="n ≤ 100000 đống đá; hai người luân phiên lấy số đá dương tùy ý từ một đống; người lấy viên cuối thắng. Cả hai chơi tối ưu. Ai thắng?",
    vi_options=["Mô phỏng trò chơi bằng BFS trên trạng thái các đống",
                "XOR của mọi kích thước đống: người đi trước thắng khi và chỉ khi khác 0",
                "Sắp xếp các đống và greedy lấy lớn nhất",
                "Dijkstra trên đồ thị trạng thái"],
    vi_hint="Đây chính là Nim: vị trí thua khi và chỉ khi XOR các đống bằng 0. Mô phỏng toàn bộ không gian trạng thái là mũ.",
)
D7, D7VI = recognition_drill(
    "hsgx-p1-d7", "Count Numbers With Property",
    "Given N ≤ 10^18, count the integers in [1, N] whose decimal digits are non-decreasing (e.g. 1259 yes, 129 no).",
    ["Sieve up to N (impossible memory)",
     "Iterate and check each number up to N",
     "Digit DP over the decimal representation of N",
     "Two pointers over digits"],
    "C",
    "N has up to 19 digits; the count itself is over digit *positions* — the classic digit DP shape: state = position + last digit + tight flag.",
    vi_title="Đếm số theo tính chất chữ số",
    vi_scenario="Cho N ≤ 10^18, đếm các số trong [1, N] có chữ số không giảm (ví dụ 1259 đúng, 129 sai).",
    vi_options=["Sàng tới N (bộ nhớ không thể)",
                "Duyệt và kiểm từng số tới N",
                "Digit DP trên biểu diễn thập phân của N",
                "Two pointers trên các chữ số"],
    vi_hint="N có tới 19 chữ số; đếm diễn ra trên *vị trí chữ số* — dạng digit DP kinh điển: trạng thái = vị trí + chữ số trước + cờ tight.",
)
D8, D8VI = recognition_drill(
    "hsgx-p1-d8", "Growing Network",
    "n ≤ 200000 computers, m ≤ 300000 link events in chronological order, each adding one connection. After each event, report the number of connected components.",
    ["Run BFS after every event",
     "DSU with union-by-size; components = n minus successful unions",
     "Kruskal, then binary search each query",
     "Sparse table over events"],
    "B",
    "Edges are only added and the question is connectivity — DSU amortizes all m unions in near-linear time; components decrease by one per merge.",
    vi_title="Mạng lớn dần",
    vi_scenario="n ≤ 200000 máy tính, m ≤ 300000 sự kiện nối theo thứ tự thời gian, mỗi sự kiện thêm một kết nối. Sau mỗi sự kiện, in số thành phần liên thông.",
    vi_options=["Chạy BFS lại sau mỗi sự kiện",
                "DSU với union-by-size; thành phần = n trừ số lần hợp nhất thành công",
                "Kruskal, rồi tìm kiếm nhị phân từng truy vấn",
                "Sparse table trên các sự kiện"],
    vi_hint="Chỉ thêm cạnh và hỏi liên thông — DSU xử lý toàn bộ m lần hợp trong gần tuyến tính; số thành phần giảm một mỗi lần gộp.",
)

write_practice(
    M, "hsgx-p1-drills", "Recognition Drill Set 1",
    "Eight scenarios, no topic names. Output the letter of the algorithm family that fits constraints and semantics — the letter is the whole program.",
    "Bộ nhận diện 1",
    "Tám tình huống, không tên chủ đề. In ra chữ cái của họ thuật toán vừa giới hạn và ngữ nghĩa — chữ cái là toàn bộ chương trình.",
    "hsgx-m1-signals",
    40,
    "advanced",
    [D1, D2, D3, D4, D5, D6, D7, D8],
    {
        "hsgx-p1-d1": D1VI,
        "hsgx-p1-d2": D2VI,
        "hsgx-p1-d3": D3VI,
        "hsgx-p1-d4": D4VI,
        "hsgx-p1-d5": D5VI,
        "hsgx-p1-d6": D6VI,
        "hsgx-p1-d7": D7VI,
        "hsgx-p1-d8": D8VI,
    },
    solutions=[
        ("hsgx-p1-d1", letter("B"), letter("A")),
        ("hsgx-p1-d2", letter("C"), letter("A")),
        ("hsgx-p1-d3", letter("B"), letter("A")),
        ("hsgx-p1-d4", letter("B"), letter("A")),
        ("hsgx-p1-d5", letter("C"), letter("A")),
        ("hsgx-p1-d6", letter("B"), letter("A")),
        ("hsgx-p1-d7", letter("C"), letter("A")),
        ("hsgx-p1-d8", letter("B"), letter("A")),
    ],
)

# --------------------------------------------------------------- checkpoint
# Real task (not a letter drill): the constraint→complexity reflex, executed.
CP_M1_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1, 0);
    for (int i = 1; i <= n; ++i) { in >> a[i]; a[i] += a[i - 1]; }
    long long X = 0, S = 0;
    for (int t = 0; t < q; ++t) {
        int l, r; in >> l >> r;
        if (l > r) swap(l, r);
        long long s = a[r] - a[l - 1];
        out << s << "{{NL}}";
        if (q == 200000) {           // checksum protocol: only the full-scale
            X ^= s;                  // test reports the folded pair "X S"
            S = (S + s % 1000000007 + 1000000007) % 1000000007;
        }
    }
    if (q == 200000) out << X << " " << S << "{{NL}}";
""") + END

CP_M1_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    // WRONG: recomputes each query in O(r-l+1). With n,q = 200000 and ranges
    // ~n/3 wide on average, that is ~10^10+ operations — far beyond the
    // limit. The constraints name the tool: prefix sums, O(n + q).
    for (int t = 0; t < q; ++t) {
        int l, r; in >> l >> r;
        if (l > r) swap(l, r);
        long long s = 0;
        for (int i = l; i <= r; ++i) s += a[i];
        out << s << "{{NL}}";
        if (q == 200000) {
            long long X = 0, S = 0;
            X ^= s;
            S = (S + s % 1000000007 + 1000000007) % 1000000007;
        }
    }
""") + END

# Deterministic full-scale test: n = q = 200000. Expected output computed
# in Python (prefix sums), then folded to a 64-bit checksum so the want
# literal stays small and byte-exact.
_vals = [(i * 7919) % 1000000 - 500000 for i in range(1, 200001)]
_pref = [0]
for v in _vals:
    _pref.append(_pref[-1] + v)
_qls = [(i * 13) % 200000 + 1 for i in range(1, 200001)]
_qrs = [(i * 31) % 200000 + 1 for i in range(1, 200001)]
_xor = 0
_lsum = 0
_sums = []
for l, r in zip(_qls, _qrs):
    if l > r:
        l, r = r, l
    _s = _pref[r] - _pref[l - 1]
    _sums.append(_s)
    _xor ^= _s
    _lsum = (_lsum + _s) % 1000000007
CP_M1_IN = T("200000 200000", " ".join(map(str, _vals)),
             " ".join(str(l) + " " + str(r) for l, r in zip(_qls, _qrs)))
# want = 200000 sum lines + the checksum line "X S"
CP_M1_WANT = T(*[str(s) for s in _sums] + [str(_xor) + " " + str(_lsum)])

write_checkpoint(
    M, "hsgx-cp-m1", "Checkpoint — Read, Then Decide",
    "The first real task: static range sums at full scale. The correct complexity is decided by the constraints, not by the story.",
    20,
    """
**Điểm kiểm tra — Đọc, rồi quyết định.** Given n ≤ 200000 integers and
q ≤ 200000 queries (l, r): compute each range sum, then report XOR of the
sums and their total modulo 1e9+7. The array never changes. A per-query
loop will not survive the largest test — the constraint table from this
module names the tool.
""",
    "Điểm kiểm tra — Đọc, rồi quyết định",
    "Nhiệm vụ thật đầu tiên: tổng đoạn tĩnh ở đúng giới hạn. Độ phức tạp đúng do giới hạn quyết định, không do cốt truyện.",
    """
**Điểm kiểm tra — Đọc, rồi quyết định.** Cho n ≤ 200000 số nguyên và
q ≤ 200000 truy vấn (l, r): tính từng tổng đoạn, rồi báo XOR của các tổng và
tổng tất cả modulo 1e9+7. Mảng không đổi. Vòng lặp từng truy vấn sẽ không
sống sót test lớn nhất — bảng giới hạn của module này gọi tên công cụ.
""",
    challenge(
        "hsgx-cp-m1-rangesum",
        "Static Range Sums",
        """**Bài toán.** Given n integers and q queries. Each query gives l and r
(1 ≤ l ≤ r ≤ n); consider the sum s = a[l..r] for each query.

**Output:** two numbers — the XOR of all q sums, and the sum of all q sums
modulo 1 000 000 007.

**Constraints:** 1 ≤ n, q ≤ 200000; |a[i]| ≤ 10^6. The array is static.
Ranges may be given with l > r; treat them as [r, l].

**Warning:** a per-query loop is O(n·q) total — the largest test will not
finish. Choose the complexity the constraints allow.
""",
        [
            contest_test("single query", T("3 1", "1 2 3", "1 3"), T("6"),
                "Whole-array sum is 6."),
            contest_test("negative values", T("4 2", "-1 5 -2 8", "1 2", "2 4"), T("4", "11"),
                "Per-query sums 4 and 11. Prefix sums handle negatives naturally."),
            contest_test("l equals r", T("5 1", "9 1 4 1 5", "3 3"), T("4"),
                "Single-element range is the element."),
            contest_test("full scale", CP_M1_IN, T(*[str(s) for s in _sums] + [str(_xor) + " " + str(_lsum)]),
                "n = q = 200000: O(n·q) is ~10^10+ ops — times out; prefix sums finish instantly. Ground truth computed independently in Python."),
        ],
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Tổng đoạn tĩnh",
        """**Bài toán.** Cho n số nguyên và q truy vấn. Mỗi truy vấn cho l và r
(1 ≤ l ≤ r ≤ n); in tổng a[l..r].

**Ràng buộc:** 1 ≤ n, q ≤ 200000; |a[i]| ≤ 10^6. Mảng tĩnh.

**Cảnh báo:** vòng lặp từng truy vấn tổng là O(n·q) — test lớn nhất sẽ
không kịp. Hãy chọn độ phức tạp mà giới hạn cho phép.
""",
        [("một truy vấn", "Tổng cả mảng là 6."),
         ("giá trị âm", "Tổng tiền tố xử lý số âm tự nhiên."),
         ("l bằng r", "Đoạn một phần tử là chính nó."),
         ("đúng giới hạn", "O(n·q) ~ 10^10+ phép — quá thời gian; tổng tiền tố xong ngay lập tức.")],
    ),
    CP_M1_R,
    CP_M1_W,
)

print("module m1 complete")
