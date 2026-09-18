#!/usr/bin/env python3
"""Emit missing lessons for modules 8-15.

The pypb_m8..m15 scripts define lesson content (L1..L4 / *_VI) but their
write_lesson calls were never present, so only practices were written. This
script execs each module script with write_lesson/_checkpoint wired to real
emitters and write_practice neutralized (practices already exist on disk and
are the verified state), so ONLY the missing lessons are emitted.
"""
import io
import sys

HERE = "scripts/content-authoring"
sys.path.insert(0, HERE)
import pypb

LESSON_META = {
    "errors-and-debugging": "pypb_m8.py", "files-paths-and-data": "pypb_m9.py",
    "modules-and-standard-library": "pypb_m10.py", "environments-and-packages": "pypb_m11.py",
    "testing-and-code-quality": "pypb_m12.py", "problem-solving-fundamentals": "pypb_m13.py",
    "command-line-applications": "pypb_m14.py", "capstone-personal-finance-cli": "pypb_m15.py",
}

# (mod, lid, title, desc, minutes, Lconst, vi_title, vi_desc, VIconst)
PLAN = {
    "pypb_m8.py": [
        ("errors-and-debugging", "tracebacks-try-except", "Tracebacks & try/except",
         "The three error families, reading a traceback bottom-up, and catching exceptions narrowly.", 12,
         "L1", "Traceback & try/except",
         "Ba họ lỗi, đọc traceback từ dưới lên, và bắt ngoại lệ một cách hẹp.", "L1_VI"),
        ("errors-and-debugging", "else-finally-raise", "else, finally & raise",
         "Success paths in else, cleanup in finally, and failing loudly with your own exceptions.", 12,
         "L2", "else, finally & raise",
         "Đường thành công trong else, dọn dẹp trong finally, và fail ầm ĩ bằng ngoại lệ của riêng bạn.", "L2_VI"),
        ("errors-and-debugging", "defensive-programming", "Defensive Programming",
         "Validate at the boundary, raise on broken invariants, and turn silent bugs into loud ones.", 10,
         "L3", "Lập trình phòng thủ",
         "Kiểm tra ở biên giới, raise khi bất biến bị vi phạm, biến bug câm lặng thành bug ồn ào.", "L3_VI"),
        ("errors-and-debugging", "debugging-method", "The Debugging Method",
         "Reproduce, read, locate, understand, fix, verify — a discipline, not luck.", 12,
         "L4", "Phương pháp gỡ lỗi",
         "Tái hiện, đọc, định vị, hiểu, sửa, kiểm chứng — một kỷ luật, không phải vận may.", "L4_VI"),
    ],
    "pypb_m9.py": [
        ("files-paths-and-data", "reading-files", "Reading Files",
         "open + with, read and readlines, line-by-line iteration, and FileNotFoundError.", 12,
         "L1", "Đọc tệp",
         "open + with, read và readlines, duyệt từng dòng, và FileNotFoundError.", "L1_VI"),
        ("files-paths-and-data", "writing-files-with", "Writing Files & pathlib",
         "Write and append modes, newline discipline, and paths as objects with pathlib.", 12,
         "L2", "Ghi tệp & pathlib",
         "Chế độ ghi và nối, kỷ luật xuống dòng, và đường dẫn dạng đối tượng với pathlib.", "L2_VI"),
        ("files-paths-and-data", "csv-basics", "CSV Basics",
         "Split, join, headers, and the string-typed nature of spreadsheet data.", 12,
         "L3", "CSV cơ bản",
         "Split, join, dòng tiêu đề, và bản chất chuỗi của dữ liệu bảng tính.", "L3_VI"),
        ("files-paths-and-data", "json-persistence", "JSON Persistence",
         "dumps/loads, save/load patterns, and keeping Vietnamese readable in files.", 12,
         "L4", "Lưu trữ JSON",
         "dumps/loads, mẫu save/load, và giữ tiếng Việt dễ đọc trong tệp.", "L4_VI"),
    ],
    "pypb_m10.py": [
        ("modules-and-standard-library", "imports-modules", "Imports & Your Own Modules",
         "import vs from-import, prefix discipline, and any .py file is a module.", 12,
         "L1", "Import & module của riêng bạn",
         "import so với from-import, kỷ luật tiền tố, và mọi tệp .py đều là module.", "L1_VI"),
        ("modules-and-standard-library", "creating-modules-name", "__name__ & Module Patterns",
         "Script or import? The __main__ guard and reusable module design.", 12,
         "L2", "__name__ & mẫu module",
         "Script hay import? Lớp bảo vệ __main__ và thiết kế module dùng lại được.", "L2_VI"),
        ("modules-and-standard-library", "stdlib-tour", "Standard Library Tour",
         "random, datetime, statistics — borrowed power with reproducible results.", 12,
         "L3", "Tham quan thư viện chuẩn",
         "random, datetime, statistics — sức mạnh mượn được với kết quả tái lập được.", "L3_VI"),
        ("modules-and-standard-library", "stdlib-tour-2", "Standard Library Tour II",
         "pathlib, json, and Counter — the tools that replace manual loops.", 12,
         "L4", "Tham quan thư viện chuẩn II",
         "pathlib, json, và Counter — những công cụ thay thế vòng lặp thủ công.", "L4_VI"),
    ],
    "pypb_m11.py": [
        ("environments-and-packages", "why-dependencies", "Why Dependencies Need Isolation",
         "Version conflicts, and the venv pattern that fixes them.", 10,
         "L1", "Vì sao phụ thuộc cần cô lập",
         "Xung đột phiên bản, và mẫu venv khắc phục chúng.", "L1_VI"),
        ("environments-and-packages", "venv", "venv & pip",
         "Create, activate, install — and pin versions with requirements.txt.", 10,
         "L2", "venv & pip",
         "Tạo, kích hoạt, cài đặt — và ghim phiên bản với requirements.txt.", "L2_VI"),
        ("environments-and-packages", "pip-requirements", "Dependency Judgment",
         "Questions before importing, and keeping the tree clean.", 10,
         "L3", "Phán đoán phụ thuộc",
         "Câu hỏi trước khi import, và giữ cây thư mục gọn gàng.", "L3_VI"),
    ],
    "pypb_m12.py": [
        ("testing-and-code-quality", "why-testing-assertions", "Why Testing: Assertions",
         "assert states what must be true; tests are asserts anyone can re-run.", 10,
         "L1", "Vì sao kiểm thử: Assertions",
         "assert phát biểu điều gì phải đúng; bài kiểm thử là assert mà ai cũng chạy lại được.", "L1_VI"),
        ("testing-and-code-quality", "basic-automated-tests", "Boundaries & Trustworthy Tests",
         "Test the edges, and make sure failing tests fail for the right reason.", 12,
         "L2", "Biên & bài kiểm thử đáng tin",
         "Kiểm tra biên, và đảm bảo bài kiểm thử lỗi vì đúng lý do.", "L2_VI"),
        ("testing-and-code-quality", "readable-code", "Readable Code",
         "Names, small functions, no magic numbers, and comments that explain why.", 12,
         "L3", "Mã dễ đọc",
         "Tên gọi, hàm nhỏ, không con số thần thánh, và chú thích giải thích vì sao.", "L3_VI"),
    ],
    "pypb_m13.py": [
        ("problem-solving-fundamentals", "decompose-inputs-outputs", "Inputs, Outputs & Processing",
         "Write the transformation in words first; the code is typing itself.", 12,
         "L1", "Đầu vào, đầu ra & xử lý",
         "Viết phép biến đổi bằng lời trước; mã chỉ là việc gõ lại.", "L1_VI"),
        ("problem-solving-fundamentals", "pseudocode-skills", "Pseudocode & Sub-skills",
         "Plain-language programs, plus counting, searching, aggregating, transforming.", 12,
         "L2", "Pseudocode & kỹ năng con",
         "Chương trình bằng ngôn ngữ thường, cùng đếm, tìm kiếm, tổng hợp, biến đổi.", "L2_VI"),
        ("problem-solving-fundamentals", "complexity-ai", "Complexity Intuition & AI as Assistant",
         "Nested loops are the first suspect; interrogate AI answers like a reviewer.", 12,
         "L3", "Trực giác độ phức tạp & AI trợ lý",
         "Vòng lặp lồng là nghi phạm đầu tiên; thẩm vấn câu trả lời của AI như một reviewer.", "L3_VI"),
    ],
    "pypb_m14.py": [
        ("command-line-applications", "cli-input-menus", "CLI Menus & Testable Cores",
         "The menu loop, input() limits in graders, and separating deciding from doing.", 12,
         "L1", "Menu CLI & lõi kiểm thử được",
         "Vòng lặp menu, giới hạn của input() với bộ chấm, và tách quyết định khỏi hành động.", "L1_VI"),
        ("command-line-applications", "argparse-lite", "Arguments with argparse",
         "Speak-first CLIs: actions, optional extras, and free professional error handling.", 12,
         "L2", "Tham số với argparse",
         "CLI nói trước: hành động, phần bổ sung tùy chọn, và xử lý lỗi chuyên nghiệp miễn phí.", "L2_VI"),
        ("command-line-applications", "organizing-cli-apps", "Organizing a CLI App",
         "Layers: controller, storage, models — and rules that keep them sane.", 12,
         "L3", "Tổ chức ứng dụng CLI",
         "Các tầng: điều khiển, lưu trữ, mô hình — và các quy tắc giữ cho chúng tỉnh táo.", "L3_VI"),
    ],
    "pypb_m15.py": [
        ("capstone-personal-finance-cli", "capstone-brief", "The Brief: Personal Finance CLI",
         "Your requirements document: product requirements, the graded contract, and your decisions.", 15,
         "L1", "Đặc tả: CLI Tài chính cá nhân",
         "Tài liệu yêu cầu của bạn: yêu cầu sản phẩm, hợp đồng được chấm, và các quyết định của bạn.", "L1_VI"),
        ("capstone-personal-finance-cli", "capstone-milestones", "Milestones & the Hint Policy",
         "A build order that works, and the escalation ladder for getting unstuck (with AI too).", 12,
         "L2", "Cột mốc & chính sách gợi ý",
         "Trình tự xây hiệu quả, và thang leo để thoát khỏi bế tắc (kể cả với AI).", "L2_VI"),
        ("capstone-personal-finance-cli", "capstone-ship", "Ship Checklist & Where This Leaves You",
         "Every line true before you call it done — and the sentence it makes true about you.", 12,
         "L3", "Checklist hoàn thiện & bạn ở đâu",
         "Mọi dòng phải đúng trước khi gọi là xong — và câu nói mà nó khiến trở thành sự thật.", "L3_VI"),
    ],
}


def main():
    emitted = 0
    for script, plan in PLAN.items():
        src = io.open(f"{HERE}/{script}", encoding="utf-8").read()
        env = {"__name__": "__emit__", "__file__": f"{HERE}/{script}"}
        # neutral emitters for everything except lessons
        env.update({
            "write_module": lambda *a, **k: None,
            "write_practice": lambda *a, **k: print("  (skipped practice — already on disk)"),
            "challenge": pypb.challenge,
            "vi_challenge": pypb.vi_challenge,
            "write_checkpoint": lambda *a, **k: None,  # checkpoint lessons already on disk
        })

        def real_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, difficulty="beginner"):
            pypb.write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, difficulty)
            nonlocal emitted
            emitted += 1

        env["write_lesson"] = real_lesson
        exec(compile(src, script, "exec"), env)
        # then emit the planned lessons (which reference the module's own L* constants)
        for entry in plan:
            (mod, lid, title, desc, minutes, lkey, vt, vd, vlkey) = entry
            if lkey not in env:
                print(f"  !! {script} missing {lkey}")
                continue
            pypb.write_lesson(mod, lid, title, desc, minutes, env[lkey], vt, vd, env[vlkey])
            emitted += 1
    print("emitted lessons (incl. duplicates from exec'd calls):", emitted)


main()
