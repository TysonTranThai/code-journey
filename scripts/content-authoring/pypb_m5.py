#!/usr/bin/env python3
"""Module 5: lists-and-collections — lessons + practices. Boundary-biased grading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge

MOD = "lists-and-collections"

L1 = """
A **list** holds many values in order:

```python
todo = ["email boss", "buy milk", "walk dog"]
```

Lists are mutable — you can change them in place:

```python
todo[0] = "email boss FIRST"
todo.append("sleep")        # add to the end
todo.insert(1, "coffee")    # insert at position 1
todo.remove("buy milk")     # remove by value
last = todo.pop()           # remove + return the last item
```

Everyday list tools:

```python
len(todo)          # how many
"buy milk" in todo # membership: True/False
todo.sort()        # order in place
todo.reverse()     # flip in place
sorted(todo)       # NEW sorted list, original untouched
```

`sort()` mutates and returns `None`; `sorted()` returns a new list. Mixing
these two up is a classic beginner bug:

```python
names = sorted(names)   # right
names = names.sort()    # BUG: names becomes None
```

## Slicing works on lists too

Everything from strings — `[start:stop]`, negatives, steps — applies to lists.
"""

L1_VI = """
Một **danh sách (list)** chứa nhiều giá trị theo thứ tự:

```python
todo = ["email boss", "buy milk", "walk dog"]
```

List có thể thay đổi (mutable) — bạn sửa được tại chỗ:

```python
todo[0] = "email boss FIRST"
todo.append("sleep")        # thêm vào cuối
todo.insert(1, "coffee")    # chèn vào vị trí 1
todo.remove("buy milk")     # xóa theo giá trị
last = todo.pop()           # xóa + trả về phần tử cuối
```

Công cụ list hằng ngày:

```python
len(todo)          # bao nhiêu phần tử
"buy milk" in todo # kiểm tra thành viên: True/False
todo.sort()        # sắp xếp tại chỗ
todo.reverse()     # đảo ngược tại chỗ
sorted(todo)       # danh sách MỚI đã sắp, bản gốc giữ nguyên
```

`sort()` sửalist gốc và trả về `None`; `sorted()` trả về list mới. Nhầm hai cái
này là bug kinh điển của người mới:

```python
names = sorted(names)   # đúng
names = names.sort()    # LỖI: names thành None
```

## Slicing cũng chạy trên list

Mọi thứ từ chuỗi — `[start:stop]`, số âm, bước nhảy — đều áp dụng được cho list.
"""

L2 = """
Tuples and sets complete the container toolbox.

## Tuple — a list that never changes

```python
point = (3, 4)
point[0]          # 3
point[0] = 9      # TypeError!
```

Use tuples for fixed groups: coordinates, RGB colors, (day, month, year).
They signal intent: "this shape does not change". One element needs a comma:
`(42,)`.

## Set — uniqueness, fast membership

```python
tags = {"python", "coding", "python"}
len(tags)          # 2 — duplicates vanish
"python" in tags   # very fast, even for huge sets
tags.add("learning")
```

Sets have no order and no duplicates — perfect for "have I seen this?" checks
and deduplication: `set(my_list)` removes duplicates.

## Choosing the container

| Need | Use |
| --- | --- |
| Ordered items, will change | list |
| Fixed shape, never changes | tuple |
| Uniqueness + fast lookup | set |
| Key → value lookups | dict (next lesson) |
"""

L2_VI = """
Tuple và set hoàn thiện bộ dụng cụ chứa dữ liệu.

## Tuple — một list không bao giờ đổi

```python
point = (3, 4)
point[0]          # 3
point[0] = 9      # TypeError!
```

Dùng tuple cho các nhóm cố định: tọa độ, màu RGB, (ngày, tháng, năm). Tuple thể
hiện ý đồ: "hình dạng này không đổi". Một phần tử cũng cần dấu phẩy: `(42,)`.

## Set — duy nhất và tra cứu nhanh

```python
tags = {"python", "coding", "python"}
len(tags)          # 2 — phần tử trùng biến mất
"python" in tags   # rất nhanh, kể cả với set khổng lồ
tags.add("learning")
```

Set không có thứ tự và không trùng lặp — hoàn hảo cho dạng "đã gặp cái này
chưa?" và khử trùng lặp: `set(my_list)` xóa phần tử trùng.

## Chọn container

| Nhu cầu | Dùng |
| --- | --- |
| Các mục có thứ tự, sẽ thay đổi | list |
| Hình dạng cố định, không đổi | tuple |
| Duy nhất + tra cứu nhanh | set |
| Tra cứu khóa → giá trị | dict (bài sau) |
"""

L3 = """
A **dictionary** maps keys to values — like a real dictionary maps words to
definitions:

```python
student = {"name": "Minh", "age": 21, "gpa": 3.6}
student["name"]           # 'Minh'
student["age"] = 22       # update
student["major"] = "CS"   # add a new key
del student["gpa"]        # remove
```

## Safe lookups

Reading a missing key crashes:

```python
student["phone"]          # KeyError!
student.get("phone")           # None
student.get("phone", "n/a")    # default value
"phone" in student             # membership check on keys
```

## Iterating (preview)

```python
for key in student:
    print(key, student[key])

for key, value in student.items():
    print(key, value)
```

`.items()` yields key–value pairs — the elegant way to walk a dict. Dicts are
the natural shape for records: one student, one product, one setting — keys as
field names.
"""

L3_VI = """
Một **từ điển (dictionary)** ánh xạ khóa đến giá trị — giống như từ điển thật
ánh xạ từ ngữ sang định nghĩa:

```python
student = {"name": "Minh", "age": 21, "gpa": 3.6}
student["name"]           # 'Minh'
student["age"] = 22       # cập nhật
student["major"] = "CS"   # thêm khóa mới
del student["gpa"]        # xóa
```

## Tra cứu an toàn

Đọc một khóa không tồn tại sẽ làm chương trình đổ vỡ:

```python
student["phone"]          # KeyError!
student.get("phone")           # None
student.get("phone", "n/a")    # giá trị mặc định
"phone" in student             # kiểm tra thành viên trên khóa
```

## Duyệt (xem trước)

```python
for key in student:
    print(key, student[key])

for key, value in student.items():
    print(key, value)
```

`.items()` trả về các cặp khóa–giá trị — cách thanh lịch để đi qua một dict. Dict
là hình dạng tự nhiên của bản ghi: một học sinh, một sản phẩm, một cấu hình —
khóa làm tên trường.
"""

L4 = """
Containers nest — lists inside dicts, dicts in lists — and that combination is
how real data looks:

```python
students = [
    {"name": "Minh", "grades": [8, 9, 7]},
    {"name": "Lan", "grades": [10, 9]},
]

students[0]["name"]           # 'Minh'
students[1]["grades"][-1]     # 9
students[0]["grades"].append(6)
```

Read nested access inside-out, one bracket at a time. When it gets confusing,
print the intermediate value:

```python
first = students[0]
print(first)       # see the whole dict before digging deeper
```

Nested containers are the bridge to everything ahead: files (Module 9 saves
them as JSON), modules (Module 10 groups functions), and every real dataset
you will ever process.
"""

L4_VI = """
Container lồng nhau — list trong dict, dict trong list — và sự kết hợp đó là
hình dạng dữ liệu thật:

```python
students = [
    {"name": "Minh", "grades": [8, 9, 7]},
    {"name": "Lan", "grades": [10, 9]},
]

students[0]["name"]           # 'Minh'
students[1]["grades"][-1]     # 9
students[0]["grades"].append(6)
```

Hãy đọc truy cập lồng nhau từ trong ra ngoài, từng cặp ngoặc một. Khi nó rối,
hãy in giá trị trung gian:

```python
first = students[0]
print(first)       # xem cả dict trước khi đào sâu hơn
```

Container lồng nhau là cây cầu đến mọi thứ phía trước: tệp (Module 9 lưu chúng
thành JSON), module (Module 10 gom các hàm), và mọi tập dữ liệu thật bạn sẽ
xử lý.
"""

write_lesson(MOD, "lists", "Lists",
             "Ordered, mutable collections: append, insert, remove, sort.", 12,
             L1, "Danh sách (List)", "Collections có thứ tự, có thể thay đổi: append, insert, remove, sort.", L1_VI)

write_lesson(MOD, "tuples-sets", "Tuples & Sets",
             "Fixed-shape tuples and uniqueness-driven sets — when each wins.", 10,
             L2, "Tuple & Set", "Tuple hình dạng cố định và set dựa trên tính duy nhất — khi nào cái nào thắng.", L2_VI)

write_lesson(MOD, "dictionaries", "Dictionaries",
             "Key→value lookups, safe .get(), and iterating pairs.", 12,
             L3, "Từ điển (Dictionary)", "Tra cứu khóa→giá trị, .get() an toàn, và duyệt các cặp.", L3_VI)

write_lesson(MOD, "nested-collections", "Nested Collections",
             "Lists of dicts, dicts with lists — the shape of real data.", 10,
             L4, "Collection lồng nhau", "List của dict, dict chứa list — hình dạng của dữ liệu thật.", L4_VI)

# ── Practices ───────────────────────────────────────────────────────────────
write_practice(
    MOD, "m5-lists-practice",
    "List Drills",
    "Build, mutate, and query lists.",
    "Bài tập list",
    "Xây dựng, sửa đổi, và truy vấn list.",
    "lists", 30, "beginner",
    [
        challenge(
            "py-list-append",
            "Grow the List",
            "colors starts with red. Append blue, then insert green at the front, then print the list.",
            'colors = ["red"]\n',
            [("prints mutated list", 'assert len(printed) == 1 and "green" in printed[0] and "red" in printed[0] and "blue" in printed[0], f"expected [green, red, blue], got {printed}"\nassert printed[0].find("green") < printed[0].find("red") < printed[0].find("blue"), f"order must be green, red, blue, got {printed[0]}"',
              "append adds at the end; insert(0, x) puts at the front.")],
            level="imitation",
        ),
        challenge(
            "py-list-remove",
            "Remove the Outcast",
            'guests = ["ana", "bo", "cy", "bo"] is given. Remove BOTH occurrences of "bo" and print the remaining list.',
            'guests = ["ana", "bo", "cy", "bo"]\n',
            [("both removed", 'assert printed and "bo" not in printed[0] and "ana" in printed[0] and "cy" in printed[0], f"got {printed}"\nassert "remove(" in code or "bo" in code, "remove every occurrence of bo"',
              "One remove() call only drops the first match — loop or count.")],
            level="guided",
        ),
        challenge(
            "py-list-sorted-vs-sort",
            "sorted() vs sort()",
            'scores = [7, 10, 8] is given. Print the sorted version WITHOUT changing scores, then print scores unchanged on the second line.',
            'scores = [7, 10, 8]\n',
            [("original untouched", 'assert len(printed) == 2, f"expected two lines, got {printed}"\nassert "10" in printed[0] and "7" in printed[0], f"first line should be sorted, got {printed[0]}"\nassert printed[1].strip().startswith("[7, 10"), f"second line must be the original order, got {printed[1]}"',
              "print(sorted(scores)) then print(scores) — sorted() leaves the original alone.")],
            level="guided",
        ),
        challenge(
            "py-list-second-largest",
            "Second Largest",
            "nums is given. Print the second largest value. Do not sort the list itself in place — use sorted() or a smart max.",
            "nums = [4, 9, 1, 7]\n",
            [("prints 7", 'assert printed == ["7"], f"got {printed}"\nassert "nums.sort()" not in code, "do not sort in place — the original order matters"',
              "sorted(nums)[-2] — the second item from the top.")],
            level="independent",
        ),
    ],
    {
        "py-list-append": vi_challenge("Làm giàu list", 'colors bắt đầu với red. Thêm blue vào cuối, chèn green lên đầu, rồi in list.',
                                         [("in list đã sửa", "append thêm vào cuối; insert(0, x) đặt lên đầu.")]),
        "py-list-remove": vi_challenge("Xóa khách không mời", 'guests = ["ana", "bo", "cy", "bo"] đã cho. Xóa CẢ HAI lần xuất hiện của "bo" và in list còn lại.',
                                         [("đã xóa cả hai", "Một lần remove() chỉ bỏ khớp đầu tiên — hãy lặp hoặc đếm.")]),
        "py-list-sorted-vs-sort": vi_challenge("sorted() vs sort()", 'scores = [7, 10, 8] đã cho. In bản đã sắp xếp mà KHÔNG đổi scores, rồi in scores nguyên vẹn ở dòng hai.',
                                                 [("bản gốc không đổi", "print(sorted(scores)) rồi print(scores) — sorted() không đụng vào bản gốc.")]),
        "py-list-second-largest": vi_challenge("Lớn nhì", "nums đã cho. In giá trị lớn thứ hai. Đừng sắp xếp list tại chỗ — dùng sorted() hoặc max thông minh.",
                                                 [("in 7", "sorted(nums)[-2] — phần tử thứ hai từ trên xuống.")]),
    },
    solutions=[
        ("py-list-append", 'colors = ["red"]\ncolors.append("blue")\ncolors.insert(0, "green")\nprint(colors)',
         'colors = ["red"]\ncolors.append("blue")\ncolors.insert(0, "green")\nprint(colors[0])'),
        ("py-list-remove", 'guests = ["ana", "bo", "cy", "bo"]\nwhile "bo" in guests:\n    guests.remove("bo")\nprint(guests)',
         'guests = ["ana", "bo", "cy", "bo"]\nguests.remove("bo")\nprint(guests)'),
        ("py-list-sorted-vs-sort", 'scores = [7, 10, 8]\nprint(sorted(scores))\nprint(scores)',
         'scores = [7, 10, 8]\nprint(scores.sort())\nprint(scores)'),
        ("py-list-second-largest", "nums = [4, 9, 1, 7]\nprint(sorted(nums)[-2])",
         "nums = [4, 9, 1, 7]\nprint(max(nums))"),
    ],
)

write_practice(
    MOD, "m5-tuple-set-practice",
    "Tuples & Sets",
    "Pick the right container and use its superpower.",
    "Tuple & Set",
    "Chọn đúng container và dùng siêu năng lực của nó.",
    "tuples-sets", 25, "beginner",
    [
        challenge(
            "py-set-dedupe",
            "Deduplicate Tags",
            'tags = ["py", "web", "py", "data", "web"] is given. Print how many UNIQUE tags there are.',
            'tags = ["py", "web", "py", "data", "web"]\n',
            [("prints 3", 'assert printed == ["3"], f"got {printed}"',
              "len(set(tags)) — sets collapse duplicates.")],
            level="guided",
        ),
        challenge(
            "py-set-seen",
            "Seen Before?",
            'ids = [101, 202, 101, 303] is given. seen = set() starts empty. For practice, print True if 101 appears more than once in ids, False otherwise (a set makes this one line).',
            'ids = [101, 202, 101, 303]\nseen = set()\n',
            [("prints duplicate status", 'assert printed == ["True"], f"got {printed}"',
              "len(ids) != len(set(ids)) — sizes differ only when duplicates exist.")],
            level="independent",
        ),
        challenge(
            "py-tuple-swap-trick",
            "Tuple Swap Trick",
            "a = 1 and b = 2 are given. Swap them WITHOUT a temp variable — Python's tuple assignment: a, b = b, a. Print a then b.",
            "a = 1\nb = 2\n",
            [("swapped", 'assert printed == ["2", "1"], f"got {printed}"\nassert "a, b = b, a" in code, "use tuple assignment"',
              "a, b = b, a — the Pythonic swap.")],
            level="guided",
        ),
    ],
    {
        "py-set-dedupe": vi_challenge("Khử trùng lặp thẻ", 'tags = ["py", "web", "py", "data", "web"] đã cho. In số thẻ DUY NHẤT.',
                                        [("in 3", "len(set(tags)) — set dập tắt phần tử trùng.")]),
        "py-set-seen": vi_challenge("Đã gặp chưa?", 'ids = [101, 202, 101, 303] đã cho. seen = set() khởi đầu rỗng. Để thực hành, in True nếu 101 xuất hiện nhiều hơn một lần trong ids, False nếu ngược lại (set giúp gọn một dòng).',
                                      [("in trạng thái trùng", "len(ids) != len(set(ids)) — kích thước chỉ khác khi có trùng lặp.")]),
        "py-tuple-swap-trick": vi_challenge("Mẹo hoán đổi bằng tuple", "a = 1 và b = 2 đã cho. Hoán đổi KHÔNG dùng biến tạm — phép gán tuple của Python: a, b = b, a. In a rồi b.",
                                              [("đã hoán đổi", "a, b = b, a — cách hoán đổi chuẩn Python.")]),
    },
    solutions=[
        ("py-set-dedupe", 'tags = ["py", "web", "py", "data", "web"]\nprint(len(set(tags)))',
         'tags = ["py", "web", "py", "data", "web"]\nprint(len(tags))'),
        ("py-set-seen", "ids = [101, 202, 101, 303]\nseen = set()\nprint(len(ids) != len(set(ids)))",
         "ids = [101, 202, 101, 303]\nseen = set()\nprint(len(ids) == len(set(ids)))"),
        ("py-tuple-swap-trick", "a = 1\nb = 2\na, b = b, a\nprint(a)\nprint(b)",
         "a = 1\nb = 2\na, b = a, b\nprint(a)\nprint(b)"),
    ],
)

write_practice(
    MOD, "m5-dict-practice",
    "Dictionary Drills",
    "Key-value lookups done safely.",
    "Bài tập dictionary",
    "Tra cứu khóa–giá trị một cách an toàn.",
    "dictionaries", 30, "beginner",
    [
        challenge(
            "py-dict-get",
            "Safe Lookup",
            'stock = {"apple": 5, "pear": 0} is given. Print the count for "banana" without crashing — use .get() with a default of 0.',
            'stock = {"apple": 5, "pear": 0}\n',
            [("prints 0", 'assert printed == ["0"], f"got {printed}"\nassert ".get(" in code, "use .get() with a default"',
              'stock.get("banana", 0) — no KeyError, sane default.')],
            level="guided",
        ),
        challenge(
            "py-dict-update",
            "Update the Record",
            'book = {"title": "Dune", "year": 1965} is given. Update year to 2020 for the anniversary edition and add "pages": 412. Print the dict.',
            'book = {"title": "Dune", "year": 1965}\n',
            [("record updated", 'assert printed and "2020" in printed[0] and "412" in printed[0], f"got {printed}"',
              "book[\"year\"] = 2020 and book[\"pages\"] = 412, then print(book).")],
            level="imitation",
        ),
        challenge(
            "py-dict-inventory-value",
            "Total Inventory Value",
            'prices = {"pen": 2, "book": 10, "bag": 30} is given. Print the sum of all values.',
            'prices = {"pen": 2, "book": 10, "bag": 30}\n',
            [("prints 42", 'assert printed == ["42"], f"got {printed}"',
              "sum(prices.values()) — or add them one by one for now.")],
            level="guided",
        ),
    ],
    {
        "py-dict-get": vi_challenge("Tra cứu an toàn", 'stock = {"apple": 5, "pear": 0} đã cho. In số lượng của "banana" mà không làm chương trình đổ — dùng .get() với mặc định 0.',
                                      [("in 0", 'stock.get("banana", 0) — không KeyError, mặc định hợp lý.')]),
        "py-dict-update": vi_challenge("Cập nhật bản ghi", 'book = {"title": "Dune", "year": 1965} đã cho. Cập nhật year thành 2020 cho bản kỷ niệm và thêm "pages": 412. In dict.',
                                         [("bản ghi đã cập nhật", "book[\"year\"] = 2020 và book[\"pages\"] = 412, rồi print(book).")]),
        "py-dict-inventory-value": vi_challenge("Tổng giá trị kho", 'prices = {"pen": 2, "book": 10, "bag": 30} đã cho. In tổng tất cả giá trị.',
                                                  [("in 42", "sum(prices.values()) — hoặc tạm thời cộng từng cái.")]),
    },
    solutions=[
        ("py-dict-get", 'stock = {"apple": 5, "pear": 0}\nprint(stock.get("banana", 0))',
         'stock = {"apple": 5, "pear": 0}\nprint(stock["banana"])'),
        ("py-dict-update", 'book = {"title": "Dune", "year": 1965}\nbook["year"] = 2020\nbook["pages"] = 412\nprint(book)',
         'book = {"title": "Dune", "year": 1965}\nbook["year"] = 1965\nbook["pages"] = 412\nprint(book)'),
        ("py-dict-inventory-value", 'prices = {"pen": 2, "book": 10, "bag": 30}\nprint(sum(prices.values()))',
         'prices = {"pen": 2, "book": 10, "bag": 30}\nprint(sum(prices.keys()))'),
    ],
)

write_practice(
    MOD, "m5-nested-practice",
    "Mini Build: Nested Data",
    "Read and mutate records the way real apps do.",
    "Mini build: Dữ liệu lồng nhau",
    "Đọc và sửa bản ghi như ứng dụng thật vẫn làm.",
    "nested-collections", 35, "beginner",
    [
        challenge(
            "py-nested-read",
            "Read the Record",
            "students (a list of dicts) is given in the starter. Print the name of the SECOND student, then their first grade — two lines.",
            'students = [\n    {"name": "Minh", "grades": [8, 9, 7]},\n    {"name": "Lan", "grades": [10, 9]},\n]\n',
            [("reads nested fields", 'assert len(printed) == 2, f"expected two lines, got {printed}"\nassert "Lan" in printed[0], f"second student name, got {printed}"\nassert "10" in printed[1], f"first grade of Lan, got {printed}"',
              "students[1][\"name\"] and students[1][\"grades\"][0].")],
            level="guided",
        ),
        challenge(
            "py-nested-append",
            "Add a Grade",
            "students is given. Append the grade 8 to Minh's grades, then print Minh's full record.",
            'students = [\n    {"name": "Minh", "grades": [8, 9, 7]},\n    {"name": "Lan", "grades": [10, 9]},\n]\n',
            [("grade appended", 'assert printed and "8" in printed[0] and "Minh" in printed[0], f"got {printed}"\nassert printed[0].count("8") == 2, f"Minh should now have two 8s, got {printed[0]}"',
              "students[0][\"grades\"].append(8), then print(students[0]).")],
            level="guided",
        ),
        challenge(
            "py-nested-average",
            "Average Grade",
            "students is given. Print each student's name and the average of their grades as name: avg (rounded to 1 decimal) — two lines, f-strings shine here.",
            'students = [\n    {"name": "Minh", "grades": [8, 9, 7]},\n    {"name": "Lan", "grades": [10, 9]},\n]\n',
            [("prints averages", 'assert len(printed) == 2, f"expected two lines, got {printed}"\nassert "8.0" in printed[0], f"Minh avg 8.0, got {printed[0]}"\nassert "9.5" in printed[1], f"Lan avg 9.5, got {printed[1]}"\nassert "Minh" in printed[0] and "Lan" in printed[1], f"names must appear, got {printed}"',
              "sum(g)/len(g) per student; f\"{name}: {avg:.1f}\"")],
            level="mini-build",
        ),
    ],
    {
        "py-nested-read": vi_challenge("Đọc bản ghi", "students (một list của dict) đã cho trong phần khởi đầu. In tên của học sinh THỨ HAI, rồi điểm đầu tiên của họ — hai dòng.",
                                         [("đọc trường lồng nhau", "students[1][\"name\"] và students[1][\"grades\"][0].")]),
        "py-nested-append": vi_challenge("Thêm điểm", "students đã cho. Thêm điểm 8 vào grades của Minh, rồi in toàn bộ bản ghi của Minh.",
                                            [("đã thêm điểm", "students[0][\"grades\"].append(8), rồi print(students[0]).")]),
        "py-nested-average": vi_challenge("Điểm trung bình", "students đã cho. In tên và điểm trung bình của từng học sinh dạng name: avg (làm tròn 1 chữ số) — hai dòng, f-string tỏa sáng ở đây.",
                                            [("in điểm trung bình", "sum(g)/len(g) cho từng học sinh; f\"{name}: {avg:.1f}\"")]),
    },
    solutions=[
        ("py-nested-read", 'students = [\n    {"name": "Minh", "grades": [8, 9, 7]},\n    {"name": "Lan", "grades": [10, 9]},\n]\nprint(students[1]["name"])\nprint(students[1]["grades"][0])',
         'students = [\n    {"name": "Minh", "grades": [8, 9, 7]},\n    {"name": "Lan", "grades": [10, 9]},\n]\nprint(students[0]["name"])\nprint(students[1]["grades"][0])'),
        ("py-nested-append", 'students = [\n    {"name": "Minh", "grades": [8, 9, 7]},\n    {"name": "Lan", "grades": [10, 9]},\n]\nstudents[0]["grades"].append(8)\nprint(students[0])',
         'students = [\n    {"name": "Minh", "grades": [8, 9, 7]},\n    {"name": "Lan", "grades": [10, 9]},\n]\nstudents[1]["grades"].append(8)\nprint(students[0])'),
        ("py-nested-average", 'students = [\n    {"name": "Minh", "grades": [8, 9, 7]},\n    {"name": "Lan", "grades": [10, 9]},\n]\nfor s in students:\n    avg = sum(s["grades"]) / len(s["grades"])\n    print(f"{s[\'name\']}: {avg:.1f}")',
         'students = [\n    {"name": "Minh", "grades": [8, 9, 7]},\n    {"name": "Lan", "grades": [10, 9]},\n]\nfor s in students:\n    avg = sum(s["grades"]) * len(s["grades"])\n    print(f"{s[\'name\']}: {avg:.1f}")'),
    ],
)

print("module 5 content written")
