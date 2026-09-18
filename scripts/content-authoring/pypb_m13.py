#!/usr/bin/env python3
"""Module 13: problem-solving-fundamentals — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "problem-solving-fundamentals"

# ── Lessons ──────────────────────────────────────────────────────────────────
L1 = """
Programming is problem-solving with extra steps. The steps are the job:

1. **Inputs** — what do I actually have? (types, shapes, edge cases)
2. **Outputs** — what exactly must come out? (format, units, order)
3. **Processing** — the transformation between them, in words FIRST.

## Inputs -> Processing -> Outputs, on paper

"Find the best student": inputs = list of (name, score); output = one name;
processing = scan, track the max, remember who holds it. Written out, the code
is almost typing itself:

```python
best_name, best_score = None, -1
for name, score in students:
    if score > best_score:
        best_name, best_score = name, score
print(best_name)
```

Beginners who skip the paper step debug for an hour; professionals who do it
write the loop once.
"""

L1_VI = """
Lập trình là giải quyết vấn đề với vài bước phụ. Các bước ấy chính là công việc:

1. **Đầu vào** — tôi thực sự có gì? (kiểu, hình dạng, biên)
2. **Đầu ra** — chính xác cái gì phải ra? (định dạng, đơn vị, thứ tự)
3. **Xử lý** — phép biến đổi giữa chúng, viết bằng lời TRƯỚC.

## Đầu vào -> Xử lý -> Đầu ra, trên giấy

"Tìm học sinh giỏi nhất": đầu vào = danh sách (tên, điểm); đầu ra = một tên;
xử lý = quét, theo dõi điểm cao nhất, nhớ ai đang giữ nó. Viết ra rồi, mã gần
như là gõ lại:

```python
best_name, best_score = None, -1
for name, score in students:
    if score > best_score:
        best_name, best_score = name, score
print(best_name)
```

Người mới bỏ bước giấy gỡ lỗi cả giờ; chuyên gia làm bước giấy và viết vòng lặp
một lần.
"""

L2 = """
## Pseudocode: the program in plain language

```
total = 0
for each price in prices:
    if price > 100:
        total = total + price * 0.9
    else:
        total = total + price
print total
```

No syntax to trip on; just the logic. Translate to Python afterwards, one line
at a time. If you cannot write the pseudocode, you do not understand the
problem yet — no amount of Python will fix that.

## The classic sub-skills

- **Counting**: a variable that goes up by one when something happens.
- **Searching**: loop until found, remember WHERE, stop looking (or don't —
  count all matches instead).
- **Aggregating**: total, average, best, worst — the accumulator family.
- **Transforming**: build a NEW list from an old one, item by item.

Every challenge below is one of these wearing a costume.
"""

L2_VI = """
## Pseudocode: chương trình bằng ngôn ngữ thường

```
total = 0
for each price in prices:
    if price > 100:
        total = total + price * 0.9
    else:
        total = total + price
print total
```

Không cú pháp để vấp; chỉ có logic. Dịch sang Python sau, từng dòng một. Nếu
bạn không viết nổi pseudocode, nghĩa là bạn chưa hiểu bài toán — Python không
thể sửa điều đó.

## Các kỹ năng con kinh điển

- **Đếm**: một biến tăng lên một mỗi khi có việc gì xảy ra.
- **Tìm kiếm**: lặp cho đến khi thấy, nhớ Ở ĐÂU, dừng lại (hoặc không — đếm hết
  các lần xuất hiện).
- **Tổng hợp**: tổng, trung bình, tốt nhất, tệ nhất — gia đình accumulator.
- **Biến đổi**: xây danh sách MỚI từ danh sách cũ, từng phần tử.

Mọi thử thách dưới đây đều là một trong những kỹ năng đó đội áo choàng.
"""

L3 = """
## Complexity intuition (no math required)

```python
# One pass over the data — fine for 10 or 10,000,000 items.
for item in items: ...

# One pass per item — 1,000 items = 1,000,000 comparisons. Feel the heat.
for a in items:
    for b in items: ...
```

You will formalize this in Intermediate (it is called Big-O). For now, carry
the intuition: **nested loops over the same data are the first suspect when a
program is slow.** Often there is a one-pass alternative — and the standard
library usually has it.

## AI as an assistant, not an oracle

When you ask AI for help:

1. **Ask for explanations and hints first**, code second: "Why does my loop
   skip the last item?" beats "write this for me".
2. **Never trust, always verify**: run the code, read every line, test the
   edges yourself. AI confidently invents functions that do not exist.
3. **Interrogate the answer**: "What happens with an empty list?" — make the AI
   defend its code, like a code reviewer would.

The course lets AI explain and hint, never hand you graded answers — the same
discipline you should carry into your own tools.
"""

L3_VI = """
## Trực giác độ phức tạp (không cần toán)

```python
# Một lượt qua dữ liệu — ổn với 10 hay 10.000.000 phần tử.
for item in items: ...

# Một lượt cho mỗi phần tử — 1.000 phần tử = 1.000.000 phép so sánh. Cảm nhận
# độ nóng.
for a in items:
    for b in items: ...
```

Bạn sẽ chính thức hóa điều này trong Intermediate (nó gọi là Big-O). Hiện tại,
hãy mang theo trực giác: **vòng lặp lồng nhau trên cùng một dữ liệu là nghi phạm
số một khi chương trình chậm.** Thường có phương án một lượt — và thư viện chuẩn
thường đã có sẵn nó.

## AI là trợ lý, không phải đền xử

Khi nhờ AI giúp:

1. **Hỏi giải thích và gợi ý trước**, mã sau: "Vì sao vòng lặp của tôi bỏ qua phần
   tử cuối?" hơn hẳn "viết giúp tôi".
2. **Không bao giờ tin mù quáng, luôn kiểm chứng**: chạy mã, đọc từng dòng, tự
   kiểm tra biên. AI rất tự tin phát minh ra các hàm không tồn tại.
3. **Hỏi ngược câu trả lời**: "Chuyện gì xảy ra với danh sách rỗng?" — buộc AI
   bảo vệ mã của nó, như một reviewer sẽ làm.

Khóa học cho AI giải thích và gợi ý, không bao giờ trao đáp án được chấm — cùng
kỷ luật mà bạn nên mang vào công cụ của chính mình.
"""

# ── Practices ────────────────────────────────────────────────────────────────
write_practice(
    MOD, "m13-counting-search-practice",
    "Counting & Searching Drills",
    "Accumulators, membership, and first-match logic.",
    "Bài tập đếm & tìm kiếm",
    "Accumulator, membership, và logic khớp đầu tiên.",
    "searching-counting", 30, "beginner",
    [
        challenge(
            "py-ps-count-words",
            "Word Count",
            "Write count_words(text) returning the number of words (whitespace-separated).",
            "",
            [("counts words", 'assert count_words("to be or not to be") == 6\nassert count_words("") == 0, "empty text has no words"\nassert count_words("   ") == 0, "whitespace only is zero"',
              "text.split() already handles all whitespace and returns [] for empty.")],
            level="imitation",
        ),
        challenge(
            "py-ps-find-first",
            "Find the First Match",
            "Write first_long(words, n) returning the FIRST word longer than n characters, or None if there is none.",
            "",
            [("first match or None", 'assert first_long(["a", "bb", "cccc", "dd"], 2) == "cccc", "first over 2 chars"\nassert first_long(["a", "b"], 99) is None, "no match -> None"\nassert first_long([], 1) is None, "empty list -> None"',
              "loop; return early on the first hit; after the loop, return None.")],
            level="guided",
        ),
        challenge(
            "py-ps-count-vowel-words",
            "Combine the Skills",
            "Write count_special(words) counting words that start with a vowel (a, e, i, o, u — case-insensitive) AND are at least 3 characters long.",
            "",
            [("combined predicate", 'ws = ["Apple", "ant", "egg", "elephant", "bee", "Owl", "ig"]\nassert count_special(ws) == 5, f"Apple/ant/egg/elephant/Owl qualify, got {count_special(ws)}"\nassert count_special(["bee", "ig"]) == 0, "bee is not a vowel word; ig is too short"\nassert count_special([]) == 0',
              "w[0].lower() in 'aeiou' and len(w) >= 3 — both conditions, one counter.")],
            level="independent",
        ),
        challenge(
            "py-ps-two-sum-lite",
            "Pair Finder",
            "Write has_pair(numbers, target) returning True when ANY two DIFFERENT positions in numbers sum to target.",
            "",
            [("pair detection", 'assert has_pair([1, 2, 4, 7], 9) is True, "2 + 7"\nassert has_pair([1, 2, 4], 8) is False, "no pair makes 8"\nassert has_pair([5], 10) is False, "cannot use the same position twice"',
              "nested loop is fine at this level — j starts at i + 1 to avoid reusing a position.")],
            level="independent",
        ),
    ],
    {
        "py-ps-count-words": vi_challenge("Đếm từ", "Viết count_words(text) trả về số từ (tách bởi khoảng trắng).",
                                        [("đếm đúng số từ", "text.split() đã xử lý mọi khoảng trắng và trả về [] cho chuỗi rỗng.")]),
        "py-ps-find-first": vi_challenge("Tìm khớp đầu tiên", "Viết first_long(words, n) trả về từ ĐẦU TIÊN dài hơn n ký tự, hoặc None nếu không có.",
                                        [("khớp đầu hoặc None", "lặp; return sớm ở lần trúng đầu tiên; sau vòng lặp, return None.")]),
        "py-ps-count-vowel-words": vi_challenge("Kết hợp các kỹ năng", "Viết count_special(words) đếm các từ bắt đầu bằng nguyên âm (a, e, i, o, u — không phân biệt hoa thường) VÀ dài ít nhất 3 ký tự.",
                                        [("vị từ kết hợp", "w[0].lower() in 'aeiou' và len(w) >= 3 — cả hai điều kiện, một bộ đếm.")]),
        "py-ps-two-sum-lite": vi_challenge("Tìm cặp", "Viết has_pair(numbers, target) trả về True khi có HAI vị trí KHÁC NHAU bất kỳ trong numbers có tổng bằng target.",
                                        [("phát hiện cặp", "vòng lặp lồng ổn ở mức này — j bắt đầu từ i + 1 để tránh dùng lại một vị trí.")]),
    },
    solutions=[
        ("py-ps-count-words", 'def count_words(text):\n    return len(text.split())',
         'def count_words(text):\n    if text == "":\n        return 0\n    return text.count(" ") + 1'),
        ("py-ps-find-first", 'def first_long(words, n):\n    for w in words:\n        if len(w) > n:\n            return w\n    return None',
         'def first_long(words, n):\n    for w in words:\n        if len(w) >= n:\n            return w\n    return None'),
        ("py-ps-count-vowel-words", 'def count_special(words):\n    count = 0\n    for w in words:\n        if w and w[0].lower() in "aeiou" and len(w) >= 3:\n            count += 1\n    return count',
         'def count_special(words):\n    count = 0\n    for w in words:\n        if w and w[0].lower() in "aeiou" or len(w) >= 3:\n            count += 1\n    return count'),
        ("py-ps-two-sum-lite", 'def has_pair(numbers, target):\n    for i in range(len(numbers)):\n        for j in range(i + 1, len(numbers)):\n            if numbers[i] + numbers[j] == target:\n                return True\n    return False',
         'def has_pair(numbers, target):\n    for i in range(len(numbers)):\n        for j in range(i, len(numbers)):\n            if i != j or numbers[i] * 2 == target:\n                return False\n    return False'),
    ],
)

write_practice(
    MOD, "m13-transform-ai-practice",
    "Transformation & AI Critique",
    "Build new data from old — and audit what an AI would hand you.",
    "Biến đổi & Phê bình AI",
    "Xây dữ liệu mới từ dữ liệu cũ — và kiểm toán những gì AI đưa cho bạn.",
    "aggregation-transformation", 35, "beginner",
    [
        challenge(
            "py-ps-transform-orders",
            "Transform: Orders to Report",
            "orders = [(\"coffee\", 2, 3.5), (\"tea\", 1, 2.0), (\"coffee\", 3, 3.5)] (item, qty, unit_price). Write revenue_by_item(orders) returning a dict item -> total revenue, rounded to 2 decimals per item.",
            "",
            [("aggregation dict", 'orders = [("coffee", 2, 3.5), ("tea", 1, 2.0), ("coffee", 3, 3.5)]\nr = revenue_by_item(orders)\nassert r == {"coffee": 17.5, "tea": 2.0}, f"got {r}"\nassert revenue_by_item([]) == {}, "empty orders -> empty report"',
              'acc[item] = acc.get(item, 0) + qty * price; round(x, 2) at the end.')],
            level="independent",
        ),
        challenge(
            "py-ps-transform-records",
            "Transform: Records to Labels",
            "students = [{\"name\": \"Minh\", \"score\": 8}, {\"name\": \"Lan\", \"score\": 5}] (0-10 scale). Write to_labels(students) returning a NEW list of strings \"name: pass\" when score >= 6 else \"name: retake\".",
            "",
            [("new list built", 'students = [{"name": "Minh", "score": 8}, {"name": "Lan", "score": 5}]\nassert to_labels(students) == ["Minh: pass", "Lan: retake"], f"got {to_labels(students)}"\nassert to_labels([{ "name": "B", "score": 6}]) == ["B: pass"], "6 is a pass (>= 6)"\nassert to_labels([]) == [], "empty students -> empty labels"',
              "build a result list with append inside the loop — never mutate the input dicts.")],
            level="guided",
        ),
        challenge(
            "py-ps-ai-critique",
            "Critique the AI's Code",
            'An AI produced second_max(nums) which claims to return the second-largest value (duplicates count: [3, 3, 1] -> 3). The shipped version is buggy: it returns min(max(nums), min(nums)). Write audit_second_max() returning a string of EXACTLY one line documenting a concrete failing input, in the form: input=[3, 3, 1] result=1 expected=3 — where result is what the buggy code returns and expected is the true second-largest.',
            "",
            [("documented counterexample", 'import re\n_r = audit_second_max()\nassert isinstance(_r, str) and _r.count("input=") == 1 and "result=" in _r and "expected=" in _r, f"one line, three fields, got {_r!r}"\n_m = re.search(r"input=\\[([^\\]]*)\\] result=(-?[\\d.]+) expected=(-?[\\d.]+)", _r)\nassert _m, f"format: input=[..] result=.. expected=.., got {_r!r}"\n_nums = [float(x) for x in _m.group(1).split(",") if x.strip()]\n_res, _exp = float(_m.group(2)), float(_m.group(3))\nassert len(_nums) >= 2, "need at least two values"\n_buggy = min(max(_nums), min(_nums))\nassert _res == _buggy, f"result must equal what the buggy code returns for your input: {_buggy}"\nassert _exp == sorted(_nums)[-2], f"expected must be the true second-largest of your input (duplicates count)"\nassert _res != _exp, "result must differ from expected — that is the failure"',
              "Duplicates break it: [3, 3, 1] -> true second-largest is 3, but the buggy min(max, min) reports 1.")],
            level="real-world",
        ),
        challenge(
            "py-ps-max-gap",
            "Capstone Warmup: Max Gap",
            "Write max_gap(numbers) returning the largest difference between adjacent values in the list (None for lists with fewer than 2 items).",
            "",
            [("adjacent differences", 'assert max_gap([4, 9, 10, 20]) == 10, "20 - 10"\nassert max_gap([5, 5, 5]) == 0, "all equal -> 0"\nassert max_gap([7]) is None and max_gap([]) is None, "too short -> None"',
              "loop from index 1; track the max of numbers[i] - numbers[i-1].")],
            level="independent",
        ),
    ],
    {
        "py-ps-transform-orders": vi_challenge("Biến đổi: Đơn hàng thành báo cáo", 'orders = [("coffee", 2, 3.5), ("tea", 1, 2.0), ("coffee", 3, 3.5)] (món, số lượng, giá đơn vị). Viết revenue_by_item(orders) trả về dict món -> tổng doanh thu, làm tròn 2 chữ số cho từng món.',
                                        [("dict tổng hợp", 'acc[item] = acc.get(item, 0) + qty * price; round(x, 2) ở cuối.')]),
        "py-ps-transform-records": vi_challenge("Biến đổi: Bản ghi thành nhãn", 'students = [{"name": "Minh", "score": 8}, {"name": "Lan", "score": 5}] (thang 0-10). Viết to_labels(students) trả về danh sách chuỗi MỚI "name: pass" khi score >= 6 còn không thì "name: retake".',
                                        [("danh sách mới được xây", "xây danh sách kết quả bằng append trong vòng lặp — không bao giờ thay đổi dict đầu vào.")]),
        "py-ps-ai-critique": vi_challenge("Phê bình mã của AI", 'Một AI viết second_max(nums) tuyên bố trả về giá trị lớn thứ hai (trùng lặp vẫn tính: [3, 3, 1] -> 3). Bản phát hành bị lỗi: nó trả về min(max(nums), min(nums)). Viết audit_second_max() trả về chuỗi ĐÚNG MỘT dòng ghi nhận một đầu vào lỗi cụ thể, dạng: input=[3, 3, 1] result=1 expected=3 — result là thứ mã lỗi trả về, expected là giá trị lớn thứ hai thật.',
                                        [("phản ví dụ được ghi nhận", "Trùng lặp phá hỏng nó: [3, 3, 1] -> lớn thứ hai thật là 3, nhưng min(max, min) lỗi báo 1.")]),
        "py-ps-max-gap": vi_challenge("Khởi động capstone: Khoảng cách lớn nhất", "Viết max_gap(numbers) trả về hiệu lớn nhất giữa các giá trị kề nhau trong danh sách (None cho danh sách ít hơn 2 phần tử).",
                                        [("hiệu các phần tử kề", "lặp từ chỉ số 1; theo dõi max của numbers[i] - numbers[i-1].")]),
    },
    solutions=[
        ("py-ps-transform-orders", 'def revenue_by_item(orders):\n    totals = {}\n    for item, qty, price in orders:\n        totals[item] = totals.get(item, 0) + qty * price\n    return {item: round(t, 2) for item, t in totals.items()}',
         'def revenue_by_item(orders):\n    totals = {}\n    for item, qty, price in orders:\n        totals[qty] = totals.get(qty, 0) + qty * price\n    return {item: round(t, 2) for item, t in totals.items()}'),
        ("py-ps-transform-records", 'def to_labels(students):\n    labels = []\n    for s in students:\n        status = "pass" if s["score"] >= 6 else "retake"\n        labels.append(f"{s[\'name\']}: {status}")\n    return labels',
         'def to_labels(students):\n    labels = []\n    for s in students:\n        status = "pass" if s["score"] > 6 else "retake"\n        labels.append(f"{s[\'name\']}: {status}")\n    return labels\n\nto_labels([{ "name": "X", "score": 6}])'),
        ("py-ps-ai-critique", 'def audit_second_max():\n    return "input=[3, 3, 1] result=1 expected=3"',
         'def audit_second_max():\n    return "input=[3, 3, 1] result=3 expected=1"'),
        ("py-ps-max-gap", 'def max_gap(numbers):\n    if len(numbers) < 2:\n        return None\n    best = numbers[1] - numbers[0]\n    for i in range(1, len(numbers)):\n        gap = numbers[i] - numbers[i - 1]\n        if gap > best:\n            best = gap\n    return best',
         'def max_gap(numbers):\n    if len(numbers) < 2:\n        return None\n    return max(numbers) - min(numbers)'),
    ],
)

# ── Checkpoint: problem solving ──────────────────────────────────────────────
CP = """
## Checkpoint: Problem Solving

Everything so far, disguised as one business question. No new syntax — this is
the exam for how you think, not what you memorize.
"""

CP_VI = """
## Checkpoint: Giải quyết vấn đề

Mọi thứ từ trước đến nay, hóa trang thành một câu hỏi kinh doanh. Không cú pháp
mới — đây là bài thi về cách bạn nghĩ, không phải những gì bạn thuộc lòng.
"""

write_checkpoint(
    MOD, "checkpoint-problem-solving",
    "Checkpoint: Problem Solving",
    "One business question, answered with the accumulator toolbox.",
    25, CP,
    "Checkpoint: Giải quyết vấn đề",
    "Một câu hỏi kinh doanh, trả lời bằng hộp công cụ accumulator.",
    CP_VI,
    challenge(
        "py-checkpoint-problem-solving",
        "The Best Seller Report",
        'sales = [("mon", "pen", 4), ("mon", "book", 2), ("tue", "pen", 3), ("wed", "bag", 5), ("wed", "book", 7)] — tuples of (day, item, qty). Write report(sales) returning a dict with keys: "total" (all units sold), "best_item" (item with the highest total units; ties -> the one that REACHED its total first), and "busiest_day" (day with the most units; ties -> alphabetically first).',
        'sales = [("mon", "pen", 4), ("mon", "book", 2), ("tue", "pen", 3), ("wed", "bag", 5), ("wed", "book", 7)]\n\ndef report(sales):\n    pass\n\nprint(report(sales))\n',
        [
            ("report is correct",
             'r = report(sales)\nassert r["total"] == 21, f"total: {r}"\nassert r["best_item"] == "book", f"best_item: {r}"\nassert r["busiest_day"] == "wed", f"busiest_day: {r}"\nr2 = report([("mon", "a", 1), ("tue", "b", 1)])\nassert r2["best_item"] == "a", f"tie -> a\'s last sale (mon) precedes b\'s (tue): {r2}"\nassert r2["busiest_day"] == "mon", f"day tie -> alphabetical: {r2}"\nr5 = report([("tue", "a", 1), ("mon", "b", 1)])\nassert r5["busiest_day"] == "mon", f"day tie -> alphabetical, not arrival: {r5}"\nr6 = report([("mon", "a", 1), ("tue", "b", 2), ("wed", "a", 1)])\nassert r6["best_item"] == "b", f"totals tie at 2; b\'s last sale (tue) precedes a\'s (wed): {r6}"',
             "track units AND the index of each item\'s LAST sale; on equal totals prefer the item whose last sale came EARLIER (min by (-units, last_idx)). Days: sort by (-units, name)."),
        ],
        difficulty="beginner",
    ),
    vi_challenge("Báo cáo mặt hàng chạy nhất", 'sales = [("mon", "pen", 4), ("mon", "book", 2), ("tue", "pen", 3), ("wed", "bag", 5), ("wed", "book", 7)] — các bộ (ngày, món, số lượng). Viết report(sales) trả về dict với khóa: "total" (tổng số bán), "best_item" (món có tổng số cao nhất; hòa -> món ĐẠT tổng trước), và "busiest_day" (ngày có nhiều đơn nhất; hòa -> theo bảng chữ cái đầu tiên).',
                 [("báo cáo chính xác", "hai dict accumulator (theo món, theo ngày) trong MỘT lượt; xử lý hòa ngay khi duyệt.")]),
    solution='sales = [("mon", "pen", 4), ("mon", "book", 2), ("tue", "pen", 3), ("wed", "bag", 5), ("wed", "book", 7)]\n\n\ndef report(sales):\n    per_item = {}\n    item_last = {}\n    per_day = {}\n    total = 0\n    for idx, (day, item, qty) in enumerate(sales):\n        per_item[item] = per_item.get(item, 0) + qty\n        item_last[item] = idx\n        per_day[day] = per_day.get(day, 0) + qty\n        total += qty\n    best_item = min(per_item, key=lambda it: (-per_item[it], item_last[it]))\n    best_day = sorted(per_day, key=lambda d: (-per_day[d], d))[0]\n    return {"total": total, "best_item": best_item, "busiest_day": best_day}\n\n\nprint(report(sales))',
    wrong='sales = [("mon", "pen", 4), ("mon", "book", 2), ("tue", "pen", 3), ("wed", "bag", 5), ("wed", "book", 7)]\n\n\ndef report(sales):\n    per_item = {}\n    per_day = {}\n    total = 0\n    for day, item, qty in sales:\n        per_item[item] = per_item.get(item, 0) + qty\n        per_day[day] = per_day.get(day, 0) + qty\n        total += qty\n    best_item = max(per_item, key=per_item.get)\n    best_day = max(per_day, key=per_day.get)\n    return {"total": total, "best_item": best_item, "busiest_day": best_day}\n\n\nprint(report(sales))',
)

print("module 13 content written")
