#!/usr/bin/env python3
"""Restore the 6 original VI hints clobbered by the round-1 sync_vi bug."""
import io
import json

ROOT = "/Users/tysontran/Documents/Code Journey"
COURSE = ROOT + "/src/content/tracks/python/courses/python-intermediate"

RESTORE = {
    # keyed by position: [original 2 tests in authoring order, then the probe]
    "pi6-stream-pipeline": [
        ("Đếm trên nhiều tệp", "Lặp từng tệp theo dòng; split và tích lũy."),
        ("Tệp rỗng đóng góp 0", "Không token trong stream rỗng."),
        ("Xử lý theo dòng thay vì đọc cả tệp", "read_text() nạp toàn bộ tệp vào bộ nhớ — hãy lặp qua tệp theo từng dòng."),
    ],
    "pi6-stream-longest": [
        ("Tìm dòng dài nhất", "Theo dõi max trong khi lặp trực tiếp đối tượng tệp."),
        ("Tệp rỗng", "Không có dòng → trả ''."),
        ("Xử lý theo dòng thay vì đọc cả tệp", "read_text() nạp toàn bộ tệp vào bộ nhớ — hãy lặp qua tệp theo từng dòng."),
    ],
    "pi6-stream-chunks": [
        ("Digest của nội dung đã biết", "h.update(chunk) trong vòng lặp, rồi h.hexdigest()."),
        ("Tệp rỗng vẫn có digest", "Không chunk nào vẫn cho digest hợp lệ."),
        ("Đọc theo khối thay vì đọc cả tệp", "f.read() không đối số là đọc nguyên tệp — hãy đọc từng khối cố định."),
    ],
}


def main():
    fixed = 0
    for cid, tests in RESTORE.items():
        import glob
        hits = glob.glob(
            COURSE + "/modules/*/practices/*/challenges/" + cid + ".vi.json"
        ) + glob.glob(
            COURSE + "/modules/*/lessons/*/challenges/" + cid + ".vi.json"
        )
        assert hits, cid
        path = hits[0]
        ch = json.load(open(path, encoding="utf-8"))
        assert len(ch["tests"]) == len(RESTORE[cid]), (cid, len(ch["tests"]))
        for t, (name, hint) in zip(ch["tests"], RESTORE[cid]):
            t["name"], t["hint"] = name, hint
        with io.open(path, "w", encoding="utf-8") as f:
            json.dump(ch, f, ensure_ascii=False, indent=2)
            f.write("\n")
        fixed += 1
        print("restored", cid)
    print("done:", fixed, "files")


if __name__ == "__main__":
    main()
