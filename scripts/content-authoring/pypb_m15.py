#!/usr/bin/env python3
"""Module 15: capstone-personal-finance-cli — lessons + practices + checkpoint.

The capstone gives REQUIREMENTS, not steps. Graded challenges are framed as
acceptance criteria for the core logic the learner must design themselves.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "capstone-personal-finance-cli"

# ── Lessons ──────────────────────────────────────────────────────────────────
L1 = """
## The Brief: Personal Finance CLI

Build a command-line expense tracker. No tutorial, no starter solution — this
page is your requirements document, the way a real project begins.

### Product requirements

- Record expenses: amount (> 0), category (free text, stored lowercase), and an
  optional note.
- Persist expenses to `expenses.json` and load them back — including surviving
  a missing or corrupt file (start fresh rather than crash).
- Report: total spent, count of expenses, per-category totals (rounded to 2
  decimals), and the top category (ties → the category that reached its total
  first).
- Budget guard: given a monthly budget, the report states remaining budget and
  warns when spending exceeds 90% of it.

### Acceptance criteria (the graded core)

The functions below are graded on this page and in the readiness checkpoint —
they are the contract your CLI is built on:

- `add_expense(expenses, amount, category, note="")` — validates, returns a NEW
  list (never mutates the input).
- `category_report(expenses)` — dict category → total, rounded.
- `finance_summary(expenses, budget)` — the full report dict.

### Explicitly YOUR decisions

File layout, function names beyond the contract, the menu text, how notes are
displayed, extra features (recurring expenses? export?), and how you test. The
milestones on the next page suggest an order — they do not prescribe code.
"""

L1_VI = """
## Đặc tả: CLI Tài chính cá nhân

Xây một trình theo dõi chi tiêu dạng dòng lệnh. Không có hướng dẫn từng bước,
không có lời giải mẫu — trang này là tài liệu yêu cầu của bạn, cách mọi dự án
thật bắt đầu.

### Yêu cầu sản phẩm

- Ghi chi tiêu: số tiền (> 0), danh mục (văn bản tự do, lưu dạng chữ thường),
  và ghi chú tùy chọn.
- Lưu chi tiêu vào `expenses.json` và nạp lại — kể cả việc sống sót qua tệp
  thiếu hoặc hỏng (bắt đầu lại từ đầu thay vì sập).
- Báo cáo: tổng chi, số lượng khoản chi, tổng theo từng danh mục (làm tròn 2
  chữ số), và danh mục hàng đầu (hòa → danh mục đạt tổng trước).
- Chốt ngân sách: cho ngân sách tháng, báo cáo nêu số tiền còn lại và cảnh báo
  khi chi tiêu vượt 90% ngân sách.

### Tiêu chí nghiệm thu (phần lõi được chấm)

Các hàm dưới đây được chấm trên trang này và ở checkpoint readiness — chúng là
hợp đồng mà CLI của bạn xây trên đó:

- `add_expense(expenses, amount, category, note="")` — kiểm tra hợp lệ, trả về
  danh sách MỚI (không bao giờ thay đổi đầu vào).
- `category_report(expenses)` — dict danh mục → tổng, đã làm tròn.
- `finance_summary(expenses, budget)` — dict báo cáo đầy đủ.

### Những quyết định THUỘC VỀ BẠN

Bố cục tệp, tên hàm ngoài hợp đồng, chữ trong menu, cách hiển thị ghi chú, các
tính năng bổ sung (chi tiêu định kỳ? xuất dữ liệu?), và cách bạn kiểm thử. Các
cột mốc ở trang sau gợi ý thứ tự — chúng không áp đặt mã nguồn.
"""

L2 = """
## Suggested milestones

1. **The contract, in memory** — implement and self-test the three graded
   functions with plain lists. Everything else waits.
2. **Persistence** — `save_expenses` / `load_expenses` wrapping JSON, with the
   missing/corrupt-file fallback you already wrote in Module 14.
3. **The CLI surface** — menu loop or argparse on top of the working core.
   Keep this layer dumb: parse, call, print.
4. **Tests** — a suite of asserts over the core: boundaries (amount 0, ties),
   the corrupt-file case, a full summary example.
5. **Polish** — Vietnamese-friendly output (ensure_ascii=False), a README with
   usage, `requirements.txt` if you imported anything beyond the stdlib.

## The hint policy (for AI too)

Stuck is normal. The escalation ladder: re-read the requirement → write the
pseudocode → ask AI to EXPLAIN your error → ask AI for a HINT on the approach →
only then, ask for a small code fragment you fully retype and verify. Copying a
whole solution teaches nothing and the readiness checkpoint will find you out.
"""

L2_VI = """
## Các cột mốc gợi ý

1. **Hợp đồng, trong bộ nhớ** — cài đặt và tự kiểm thử ba hàm được chấm bằng
   danh sách thuần. Mọi thứ khác chờ đợi.
2. **Lưu trữ** — `save_expenses` / `load_expenses` bọc JSON, với phương án dự
   phòng tệp thiếu/hỏng bạn đã viết ở Module 14.
3. **Bề mặt CLI** — vòng lặp menu hoặc argparse phía trên lõi đang chạy. Giữ
   tầng này ngu: phân tích, gọi, in.
4. **Kiểm thử** — một bộ assert trên lõi: biên (số tiền 0, hòa), trường hợp
   tệp hỏng, một ví dụ summary đầy đủ.
5. **Đánh bóng** — đầu ra thân thiện tiếng Việt (ensure_ascii=False), README
   với hướng dẫn sử dụng, `requirements.txt` nếu bạn import gì ngoài thư viện
   chuẩn.

## Chính sách gợi ý (kể cả với AI)

Mắc kẹt là bình thường. Thang leo: đọc lại yêu cầu → viết pseudocode → nhờ AI
GIẢI THÍCH lỗi của bạn → nhờ AI GỢI Ý hướng tiếp cận → chỉ sau đó, xin một
đoạn mã nhỏ bạn tự gõ lại hoàn toàn và kiểm chứng. Sao chép cả lời giải không
dạy bạn điều gì và checkpoint readiness sẽ phát hiện điều đó.
"""

L3 = """
## Ship checklist

Before you call it done, every line below should be true:

- [ ] `add_expense` rejects amount <= 0 and empty category — with messages.
- [ ] Input lists are never mutated; the CLI state flows through return values.
- [ ] `expenses.json` roundtrips; a corrupt file costs you nothing but a
      fresh start.
- [ ] `finance_summary` includes total, count, per-category totals (rounded),
      top category (first-to-reach tie-break), remaining budget, and a
      warning key set when spending > 90% of budget.
- [ ] Your own test suite passes; it includes at least one boundary case and
      one corrupt-file case.
- [ ] README explains how to run it; venv + requirements.txt discipline shown.
- [ ] Git history tells the story: small commits, messages that say why.

## Where this leaves you

You can now take a written requirement, design a data model, implement it in
layers that each have one job, persist it, test it, and ship it. That is the
sentence "I can build small useful Python programs independently" — made true.
Python Intermediate will assume all of it, and add: classes, iterators,
comprehensions in depth, files beyond JSON, and real testing frameworks.
"""

L3_VI = """
## Danh checklist hoàn thiện

Trước khi gọi nó là xong, mọi dòng dưới đây phải đúng:

- [ ] `add_expense` từ chối amount <= 0 và danh mục rỗng — kèm thông báo.
- [ ] Danh sách đầu vào không bao giờ bị thay đổi; trạng thái CLI chảy qua các
      giá trị trả về.
- [ ] `expenses.json` khép kín; một tệp hỏng chỉ khiến bạn bắt đầu lại, không
      sập.
- [ ] `finance_summary` gồm total, count, tổng theo danh mục (làm tròn), danh
      mục hàng đầu (hòa → đạt-trước), ngân sách còn lại, và khóa cảnh báo được
      đặt khi chi > 90% ngân sách.
- [ ] Bộ kiểm thử của chính bạn đạt; có ít nhất một ca biên và một ca tệp hỏng.
- [ ] README giải thích cách chạy; kỷ luật venv + requirements.txt được thể
      hiện.
- [ ] Lịch sử Git kể câu chuyện: commit nhỏ, thông điệp nói lên lý do.

## Điều này đưa bạn đến đâu

Giờ đây bạn có thể nhận một yêu cầu viết, thiết kế mô hình dữ liệu, cài đặt nó
thành các tầng mà mỗi tầng có đúng một việc, lưu trữ, kiểm thử, và đóng gói.
Đó chính là câu "Tôi có thể tự xây các chương trình Python nhỏ hữu ích một cách
độc lập" — trở thành sự thật. Python Intermediate sẽ mặc định tất cả điều đó,
và thêm vào: class, iterator, comprehension chuyên sâu, tệp ngoài JSON, và các
framework kiểm thử thật.
"""

# ── Practices ────────────────────────────────────────────────────────────────
write_practice(
    MOD, "capstone-core-practice",
    "Capstone: Core Contract",
    "The acceptance criteria, graded. Design the internals yourself.",
    "Capstone: Hợp đồng lõi",
    "Các tiêu chí nghiệm thu, được chấm. Tự thiết kế phần bên trong.",
    "capstone-brief", 45, "beginner",
    [
        challenge(
            "py-cap-add-expense",
            "Acceptance: add_expense",
            "Contract: add_expense(expenses, amount, category, note=\"\") returns a NEW list with {\"amount\": float, \"category\": lowercase str, \"note\": str} appended. amount must be a number > 0 and category non-empty, else raise ValueError. Input list must never be mutated.",
            "",
            [("validation and purity", 'e0 = [{"amount": 5.0, "category": "food", "note": ""}]\nr = add_expense(e0, 12.5, "Transport")\nassert r == e0 + [{"amount": 12.5, "category": "transport", "note": ""}], f"got {r}"\nassert e0 == [{"amount": 5.0, "category": "food", "note": ""}], "input mutated!"\nfor bad in [(0, "food"), (-3, "food"), (5, "")]:\n    try:\n        add_expense([], *bad)\n        assert False, f"{bad} must raise"\n    except ValueError:\n        pass\nassert add_expense([], 10, "food", "lunch")[0]["note"] == "lunch", "note defaults and stores"',
              "amount = float(amount) after validating > 0; category = category.strip().lower().")],
            level="independent",
        ),
        challenge(
            "py-cap-category-report",
            "Acceptance: category_report",
            "Contract: category_report(expenses) returns dict category -> total spent, rounded to 2 decimals. Empty list -> {}.",
            "",
            [("aggregates by category", 'expenses = [\n    {"amount": 3.5, "category": "food", "note": ""},\n    {"amount": 12, "category": "transport", "note": ""},\n    {"amount": 1.5, "category": "food", "note": ""},\n]\nr = category_report(expenses)\nassert r == {"food": 5.0, "transport": 12}, f"got {r}"\nassert category_report([]) == {}',
              "accumulate with dict.get, round(v, 2) on the way out.")],
            level="independent",
        ),
        challenge(
            "py-cap-summary",
            "Acceptance: finance_summary",
            "Contract: finance_summary(expenses, budget) returns {\"total\", \"count\", \"top\", \"remaining\", \"warning\"} where total is rounded, top is the category with the highest total (tie -> first to reach it; None when empty), remaining = round(budget - total, 2), and warning is True when total > 0.9 * budget else False.",
            "",
            [("the full report", 'expenses = [\n    {"amount": 50, "category": "food", "note": ""},\n    {"amount": 20, "category": "fun", "note": ""},\n    {"amount": 30, "category": "food", "note": ""},\n]\nr = finance_summary(expenses, 100)\nassert r["total"] == 100.0 and r["count"] == 3, f"got {r}"\nassert r["top"] == "food", f"tie at 80? no: food 80, fun 20. got {r}"\nassert r["remaining"] == 0.0, f"got {r}"\nassert r["warning"] is True, "100 > 90% of 100"\nr2 = finance_summary([], 50)\nassert r2["top"] is None and r2["warning"] is False and r2["remaining"] == 50, f"got {r2}"\nr3 = finance_summary(expenses[:1], 100)\nassert r3["warning"] is False, "50 is exactly half — no warning"\nr4 = finance_summary([{"amount": 2, "category": "b"}, {"amount": 3, "category": "a"}, {"amount": 2, "category": "a"}, {"amount": 3, "category": "b"}], 20)\nassert r4["top"] == "a", f"tie 5-5, a reached its 5 first: {r4}"',
              "two accumulators: totals and first-index-seen per category; top = min by (-total, first_seen).")],
            level="mini-build",
        ),
    ],
    {
        "py-cap-add-expense": vi_challenge("Nghiệm thu: add_expense", 'Hợp đồng: add_expense(expenses, amount, category, note="") trả về danh sách MỚI với {"amount": float, "category": chữ thường, "note": str} được nối vào. amount phải là số > 0 và category khác rỗng, nếu không raise ValueError. Danh sách đầu vào không bao giờ bị thay đổi.',
                                        [("kiểm tra hợp lệ và thuần khiết", "amount = float(amount) sau khi kiểm tra > 0; category = category.strip().lower().")]),
        "py-cap-category-report": vi_challenge("Nghiệm thu: category_report", "Hợp đồng: category_report(expenses) trả về dict danh mục -> tổng chi, làm tròn 2 chữ số. Danh sách rỗng -> {}.",
                                        [("tổng hợp theo danh mục", "tích lũy với dict.get, round(v, 2) khi trả về.")]),
        "py-cap-summary": vi_challenge("Nghiệm thu: finance_summary", 'Hợp đồng: finance_summary(expenses, budget) trả về {"total", "count", "top", "remaining", "warning"} trong đó total đã làm tròn, top là danh mục có tổng cao nhất (hòa -> đạt trước; None khi rỗng), remaining = round(budget - total, 2), và warning là True khi total > 0.9 * budget còn không False.',
                                        [("báo cáo đầy đủ", "hai bộ tích lũy: tổng và chỉ-mục-đầu-tiên của từng danh mục; top = min theo (-total, first_seen).")]),
    },
    solutions=[
        ("py-cap-add-expense", 'def add_expense(expenses, amount, category, note=""):\n    if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:\n        raise ValueError("amount must be a positive number")\n    if not isinstance(category, str) or not category.strip():\n        raise ValueError("category must be a non-empty string")\n    return expenses + [{\n        "amount": float(amount),\n        "category": category.strip().lower(),\n        "note": note,\n    }]',
         'def add_expense(expenses, amount, category, note=""):\n    if amount <= 0:\n        raise ValueError("amount must be positive")\n    if not category:\n        raise ValueError("category required")\n    expenses.append({\n        "amount": float(amount),\n        "category": category.strip().lower(),\n        "note": note,\n    })\n    return expenses'),
        ("py-cap-category-report", 'def category_report(expenses):\n    totals = {}\n    for e in expenses:\n        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]\n    return {k: round(v, 2) for k, v in totals.items()}',
         'def category_report(expenses):\n    totals = {}\n    for e in expenses:\n        totals[e["amount"]] = totals.get(e["amount"], 0) + e["category"]\n    return {k: round(v, 2) for k, v in totals.items()}'),
        ("py-cap-summary", 'def finance_summary(expenses, budget):\n    if not expenses:\n        return {"total": 0.0, "count": 0, "top": None,\n                "remaining": round(budget, 2), "warning": False}\n    totals = {}\n    first_seen = {}\n    for idx, e in enumerate(expenses):\n        cat = e["category"]\n        totals[cat] = totals.get(cat, 0) + e["amount"]\n        first_seen.setdefault(cat, idx)\n    total = round(sum(e["amount"] for e in expenses), 2)\n    top = min(totals, key=lambda c: (-totals[c], first_seen[c]))\n    return {\n        "total": total,\n        "count": len(expenses),\n        "top": top,\n        "remaining": round(budget - total, 2),\n        "warning": total > 0.9 * budget,\n    }',
         'def finance_summary(expenses, budget):\n    if not expenses:\n        return {"total": 0.0, "count": 0, "top": None,\n                "remaining": round(budget, 2), "warning": False}\n    totals = {}\n    for e in expenses:\n        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]\n    total = round(sum(e["amount"] for e in expenses), 2)\n    top = max(totals, key=totals.get)\n    return {\n        "total": total,\n        "count": len(expenses),\n        "top": top,\n        "remaining": round(budget - total, 2),\n        "warning": total > 0.9 * budget,\n    }'),
    ],
)

write_practice(
    MOD, "capstone-readiness-practice",
    "Capstone: Final Readiness",
    "Persistence and composition — the last gates before you ship solo.",
    "Capstone: Sẵn sàng cuối cùng",
    "Lưu trữ và kết hợp — những cánh cổng cuối trước khi bạn tự ra khơi.",
    "capstone-milestones", 40, "beginner",
    [
        challenge(
            "py-cap-persist",
            "Acceptance: Persistence with Fallback",
            "Build save_expenses(path, expenses) + load_expenses(path): JSON roundtrip with ensure_ascii=False; missing file -> []; corrupt file -> []. Then demonstrate: save one Vietnamese-noted expense (\"cà phê\"), load it back, and print the LOADED amount (one line).",
            "",
            [("survives everything", 'import json as _j, os as _os\nfor p in ("cap_probe.json",):\n    if _os.path.exists(p):\n        _os.remove(p)\nassert load_expenses("cap_probe.json") == [], "missing -> []"\nopen("cap_probe.json", "w").write("{oops")\nassert load_expenses("cap_probe.json") == [], "corrupt -> []"\n_os.remove("cap_probe.json")\nassert printed == ["3.5"], f"print the loaded amount, got {printed}"\nassert "ensure_ascii=False" in code, "Vietnamese must stay readable"',
              "try/except around json.load catches JSONDecodeError; FileNotFoundError catches missing.")],
            level="mini-build",
        ),
        challenge(
            "py-cap-refactor-why",
            "Code Review: Which Design Survives?",
            "Two designs for the capstone storage layer are below. Write choose_design() returning \"A\" or \"B\" — the design that keeps the CLI testable and swappable. Then a comment line starting with # explaining why (one line, must mention the word 'storage' or 'layer').",
            "",
            [("judgment call", '_r = choose_design()\nassert _r in ("A", "B"), f"answer A or B, got {_r!r}"\n_lines = [l for l in code.splitlines() if l.strip().startswith("#") and ("storage" in l.lower() or "layer" in l.lower())]\nassert _lines, "add the one-line # justification"\nassert choose_design() == "B", "B keeps file I/O behind a seam the CLI never touches"',
              "Design A: every menu action opens/reads/writes the file directly. Design B: the menu calls add/list functions that return data; one storage module does all I/O.")],
            level="real-world",
        ),
    ],
    {
        "py-cap-persist": vi_challenge("Nghiệm thu: Lưu trữ có dự phòng", 'Xây save_expenses(path, expenses) + load_expenses(path): vòng lặp JSON với ensure_ascii=False; tệp thiếu -> []; tệp hỏng -> []. Sau đó minh họa: lưu một khoản chi có ghi chú tiếng Việt ("cà phê"), nạp lại, và in SỐ TIỀN đã nạp (một dòng).',
                                        [("sống sót qua mọi thứ", "try/except quanh json.load bắt JSONDecodeError; FileNotFoundError bắt tệp thiếu.")]),
        "py-cap-refactor-why": vi_challenge("Đánh giá mã: Thiết kế nào sống sót?", 'Hai thiết kế cho tầng lưu trữ capstone nằm trong gợi ý. Viết choose_design() trả về "A" hoặc "B" — thiết kế giữ cho CLI kiểm thử được và thay thế được. Rồi một dòng chú thích bắt đầu bằng # giải thích vì sao (một dòng, phải nhắc đến từ storage hoặc layer).',
                                        [("quyết định có chủ đích", "Thiết kế A: mỗi hành động menu tự mở/đọc/ghi tệp. Thiết kế B: menu gọi các hàm add/list trả về dữ liệu; một module storage lo toàn bộ I/O.")]),
    },
    solutions=[
        ("py-cap-persist", 'import json\nfrom pathlib import Path\n\n\ndef save_expenses(path, expenses):\n    with open(path, "w", encoding="utf-8") as f:\n        json.dump(expenses, f, ensure_ascii=False, indent=2)\n\n\ndef load_expenses(path):\n    try:\n        with open(path, encoding="utf-8") as f:\n            return json.load(f)\n    except (FileNotFoundError, json.JSONDecodeError):\n        return []\n\n\nsave_expenses("cap_probe.json", [\n    {"amount": 3.5, "category": "food", "note": "cà phê"},\n])\nloaded = load_expenses("cap_probe.json")\nprint(loaded[0]["amount"])',
         'import json\nfrom pathlib import Path\n\n\ndef save_expenses(path, expenses):\n    with open(path, "w", encoding="utf-8") as f:\n        json.dump(expenses, f, ensure_ascii=False, indent=2)\n\n\ndef load_expenses(path):\n    with open(path, encoding="utf-8") as f:\n        return json.load(f)\n\n\nsave_expenses("cap_probe.json", [\n    {"amount": 3.5, "category": "food", "note": "cà phê"},\n])\nloaded = load_expenses("cap_probe.json")\nprint(loaded[0]["amount"])'),
        ("py-cap-refactor-why", 'def choose_design():\n    # design B: all file I/O lives in one storage layer, so the menu stays testable\n    return "B"',
         'def choose_design():\n    # design A spreads file I/O through the menu, which is impossible to test\n    return "A"'),
    ],
)

# ── Checkpoint: final readiness ──────────────────────────────────────────────
CP = """
## Checkpoint: Final Readiness

One composition problem, capstone-grade: every module of this course in a
single function. If you can pass this without hints, you are ready to build the
full CLI — and ready for Python Intermediate.
"""

CP_VI = """
## Checkpoint: Sẵn sàng cuối cùng

Một bài toán kết hợp, cấp độ capstone: mọi module của khóa học trong một hàm
duy nhất. Nếu bạn vượt qua mà không cần gợi ý, bạn đã sẵn sàng xây CLI hoàn
chỉnh — và sẵn sàng cho Python Intermediate.
"""

write_checkpoint(
    MOD, "final-readiness",
    "Checkpoint: Final Readiness",
    "Parse, validate, aggregate, report — the whole course in one contract.",
    30, CP,
    "Checkpoint: Sẵn sàng cuối cùng",
    "Phân tích, kiểm tra hợp lệ, tổng hợp, báo cáo — cả khóa học trong một hợp đồng.",
    CP_VI,
    challenge(
        "py-checkpoint-final-readiness",
        "The Import Pipeline",
        'raw = "coffee,3.5\\nBOOK,12\\ncoffee,1.5\\n,,skip-me\\npen,-2" is a messy CSV of category,amount rows. Write ingest(raw) returning a NEW list of clean expenses: skip blank/missing-field lines, skip amounts that are not positive numbers, lowercase categories, round amounts to 2 decimals. Then print the total of the clean list, formatted :.2f (one line).',
        'raw = "coffee,3.5\\nBOOK,12\\ncoffee,1.5\\n,,skip-me\\npen,-2"\n\ndef ingest(raw):\n    pass\n\nprint(f"{sum(e[\\"amount\\"] for e in ingest(raw)):.2f}")\n',
        [
            ("clean list is correct",
             'r = ingest(raw)\nassert r == [\n    {"amount": 3.5, "category": "coffee"},\n    {"amount": 12.0, "category": "book"},\n    {"amount": 1.5, "category": "coffee"},\n], f"got {r}"\nassert ingest("") == [], "empty input -> empty list"\nassert ingest("x,abc") == [], "non-numeric amount skipped"\nassert ingest("tea, 2.5 ") == [{"amount": 2.5, "category": "tea"}], "whitespace tolerated"', 
             "split lines then commas; strip everything; float(amount) in try/except; validate > 0."),
        ],
        difficulty="beginner",
    ),
    vi_challenge("Đường ống nhập liệu", 'raw = "coffee,3.5\\nBOOK,12\\ncoffee,1.5\\n,,skip-me\\npen,-2" là một CSV lộn xộn các dòng danh mục,số tiền. Viết ingest(raw) trả về danh sách MỚI các khoản chi sạch: bỏ qua dòng trống/thiếu trường, bỏ qua số tiền không phải số dương, viết thường danh mục, làm tròn số tiền 2 chữ số. Sau đó in tổng của danh sách sạch, định dạng :.2f (một dòng).',
                 [("danh sách sạch chính xác", "tách dòng rồi dấu phẩy; strip mọi thứ; float(amount) trong try/except; kiểm tra > 0.")]),
    solution='def finance_summary(expenses, budget):\n    if not expenses:\n        return {"total": 0.0, "count": 0, "top": None,\n                "remaining": round(budget, 2), "warning": False}\n    totals = {}\n    last_seen = {}\n    for idx, e in enumerate(expenses):\n        cat = e["category"]\n        totals[cat] = totals.get(cat, 0) + e["amount"]\n        last_seen[cat] = idx\n    total = round(sum(e["amount"] for e in expenses), 2)\n    top = min(totals, key=lambda c: (-totals[c], last_seen[c]))\n    return {\n        "total": total,\n        "count": len(expenses),\n        "top": top,\n        "remaining": round(budget - total, 2),\n        "warning": total > 0.9 * budget,\n    }',

    wrong='raw = "coffee,3.5\\nBOOK,12\\ncoffee,1.5\\n,,skip-me\\npen,-2"\n\n\ndef ingest(raw):\n    clean = []\n    for line in raw.splitlines():\n        parts = [p.strip() for p in line.split(",")]\n        if len(parts) < 2 or not parts[0] or not parts[1]:\n            continue\n        try:\n            amount = float(parts[1])\n        except ValueError:\n            continue\n        clean.append({"amount": round(amount, 2), "category": parts[0].lower()})\n    return clean\n\n\nprint(f"{sum(e[\\"amount\\"] for e in ingest(raw)):.2f}")',
)

print("module 15 content written")
