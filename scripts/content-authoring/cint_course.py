#!/usr/bin/env python3
"""
C — Intermediate: course skeleton (c track, course 2).

Idempotent, surgical shared-file handling:
  - Creates src/content/tracks/c/track.json + track.vi.json IF ABSENT
    (as of 2026-09-14 the c track has no manifest — Beginner's course is
    still being authored). References ONLY c-intermediate: loadTrack
    re-throws for referenced courses whose course.json is absent, so
    referencing c-beginner before that agent wires their manifest would
    break whole-curriculum discovery. Beginner appends their reference
    when they wire theirs (read-modify-write, never overwrite).
  - Creates the c-intermediate course.json shell (empty modules — the
    loader's documented authoring-shell escape) so the track loads.
  - Appends ONE line to validate-content.ts's COURSE_TRACKS if absent.
"""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACK_DIR = os.path.join(ROOT, "src/content/tracks/c")
BASE = os.path.join(TRACK_DIR, "courses/c-intermediate")
VALIDATOR = os.path.join(ROOT, "scripts/content-authoring/validate-content.ts")


def _w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _j(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def main():
    # 1. track.json (create if absent; if present, ensure c-intermediate is
    #    referenced — read-modify-write, preserving every other entry).
    tp = os.path.join(TRACK_DIR, "track.json")
    if os.path.exists(tp):
        with io.open(tp, "r", encoding="utf-8") as f:
            t = json.load(f)
        refs = [c.get("reference") for c in t.get("courses", [])]
        if "c-intermediate" not in refs:
            t["courses"].append({"reference": "c-intermediate"})
            _w(tp, _j(t))
            print("track.json: appended c-intermediate")
        else:
            print("track.json: c-intermediate already referenced")
    else:
        _w(
            tp,
            _j(
                {
                    "id": "c",
                    "title": "C",
                    "description": "Learn C the way it actually works: from your first compiled program to "
                    "memory-owning, well-tested C. A practice-first path — pointers and ownership are "
                    "practiced until they are instincts, every data structure is built from scratch, "
                    "and every challenge is verified against a real gcc in a locked-down sandbox.",
                    "courses": [{"reference": "c-intermediate"}],
                }
            ),
        )
        print("track.json: created (c track manifest, referencing c-intermediate)")

    tvp = os.path.join(TRACK_DIR, "track.vi.json")
    if not os.path.exists(tvp):
        _w(
            tvp,
            _j(
                {
                    "title": "C",
                    "description": "Học C theo đúng cách nó vận hành: từ chương trình được biên dịch đầu tiên "
                    "đến code C có quản lý bộ nhớ và có kiểm thử. Lộ trình tập trung thực hành — con trỏ "
                    "và quyền sở hữu bộ nhớ được luyện đến khi thành phản xạ, mọi cấu trúc dữ liệu đều "
                    "tự tay xây, và mọi thử thách đều được đối chiếu với gcc thật trong sandbox cách ly.",
                }
            ),
        )
        print("track.vi.json: created")

    # 2. course shell (empty modules — loader skips authoring shells).
    cp = os.path.join(BASE, "course.json")
    if os.path.exists(cp):
        print("course.json: exists, leaving untouched")
    else:
        _w(
            cp,
            _j(
                {
                    "id": "c-intermediate",
                    "title": "C — Intermediate",
                    "description": "Placeholder while the course is authored.",
                    "audience": [],
                    "outcomes": [],
                    "prerequisites": [],
                    "modules": [],
                }
            ),
        )
        print("course.json: created (authoring shell)")
    cvp = os.path.join(BASE, "course.vi.json")
    if not os.path.exists(cvp):
        _w(
            cvp,
            _j(
                {
                    "title": "C — Trung cấp",
                    "description": "Khung tạm thời trong khi khóa học đang được biên soạn.",
                }
            ),
        )
        print("course.vi.json: created (shell)")

    # 3. validator registry append (one line, idempotent).
    with io.open(VALIDATOR, "r", encoding="utf-8") as f:
        src = f.read()
    if '{ track: "c", course: "c-intermediate" }' in src:
        print("validator: entry already present")
    else:
        anchor = '{ track: "java", course: "java-advanced" },'
        if anchor not in src:
            raise SystemExit("validator: anchor line not found — inspect manually")
        src = src.replace(anchor, anchor + '\n  { track: "c", course: "c-intermediate" },', 1)
        with io.open(VALIDATOR, "w", encoding="utf-8") as f:
            f.write(src)
        print("validator: appended c-intermediate entry")


if __name__ == "__main__":
    main()
