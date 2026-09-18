#!/usr/bin/env python3
"""Repair pass for Python Intermediate challenge QA failures (root-caused).

Fixes, in order:
  A. tests using inspect.getsource -> use the platform `code` variable
     (solutions are graded via exec(SOLUTION_SOURCE); getsource can never work)
  B. sqlite tests: set conn.row_factory = sqlite3.Row; commit seeded rows
  C. strengthen weak tests (class-attr probe, concurrency timing, injection probe)
  D. add EN+VI tests where streaming-vs-slurp needs a behavioral check
  E. boilerplate for pi5-exc-order defines the exception family
  F. append corrected R/W overrides to pi-solutions.mjs (last key wins,
     matching both JS semantics and the harness parser)
VI overlays are touched only where test counts change (EN==VI test counts).
"""
import glob
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, "src/content/tracks/python/courses/python-intermediate")
LEDGER = os.path.join(ROOT, "scripts/content-authoring/pi-solutions.mjs")

changed = []


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def find_ch(cid):
    for p in glob.glob(
        os.path.join(COURSE, "modules/*/practices/*/challenges", cid + ".json")
    ) + glob.glob(
        os.path.join(COURSE, "modules/*/lessons/*/challenges", cid + ".json")
    ):
        return p
    raise SystemExit("challenge not found: " + cid)


def find_vi(cid):
    base = find_ch(cid)
    vi = base[:-5] + ".vi.json"
    return vi if os.path.exists(vi) else None


def edit(cid, fn):
    p = find_ch(cid)
    ch = load(p)
    fn(ch)
    save(p, ch)
    changed.append(cid)


# ---------------------------------------------------------------- A. getsource
def fix_sec_shell(ch):
    for t in ch["tests"]:
        if t["name"] == "no shell, no f-string":
            t["code"] = (
                "assert 'shell=True' not in code, 'never delegate quoting to a shell'\n"
                "assert \"f'\" not in code and 'f\"' not in code, 'build argv, not strings'\n"
                "assert 'subprocess.run' in code"
            )


def fix_sec_deser(ch):
    for t in ch["tests"]:
        if t["name"] == "pickle is not used":
            t["code"] = "assert 'pickle' not in code, 'pickle.loads executes embedded code'"


def fix_mock_api(ch):
    for t in ch["tests"]:
        if t["name"] == "test uses mocking and passes":
            t["code"] = (
                "import unittest, io\n"
                "assert 'mock' in code.lower(), 'use unittest.mock in the test suite'\n"
                "result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)"
                ".run(unittest.TestLoader().loadTestsFromTestCase(SUITE_TEST))\n"
                "assert result.wasSuccessful(), 'fetch tests failed'"
            )


def fix_mock_clock(ch):
    for t in ch["tests"]:
        if t["name"] == "all three bands tested":
            t["code"] = (
                "import unittest, io\n"
                "assert code.count('Good') >= 3, 'test all three bands'\n"
                "result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)"
                ".run(unittest.TestLoader().loadTestsFromTestCase(SUITE_TEST))\n"
                "assert result.wasSuccessful(), 'greeting tests failed'"
            )


def fix_ut_setup(ch):
    for t in ch["tests"]:
        if t["name"] == "setUp runs per test":
            t["code"] = (
                "import unittest, io\n"
                "assert 'def setUp' in code, 'give the suite a setUp'\n"
                "assert code.count('def test_') >= 2, 'at least two test methods'\n"
                "result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)"
                ".run(unittest.TestLoader().loadTestsFromTestCase(SUITE_TEST))\n"
                "assert result.wasSuccessful(), 'cart tests failed'"
            )


def fix_sub_matrix(ch):
    for t in ch["tests"]:
        if t["name"] == "subTest structure":
            t["code"] = (
                "import unittest, io\n"
                "assert 'subTest' in code, 'use self.subTest in the suite'\n"
                "result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)"
                ".run(unittest.TestLoader().loadTestsFromTestCase(SUITE_TEST))\n"
                "assert result.wasSuccessful(), 'leap tests failed'"
            )


def fix_sub_edges(ch):
    for t in ch["tests"]:
        if t["name"] == "boundary sweep present":
            t["code"] = (
                "import unittest, io\n"
                "assert 'subTest' in code, 'use self.subTest in the suite'\n"
                "result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)"
                ".run(unittest.TestLoader().loadTestsFromTestCase(SUITE_TEST))\n"
                "assert result.wasSuccessful(), 'clamp tests failed'"
            )


def fix_log_record(ch):
    for t in ch["tests"]:
        if t["name"] == "uses lazy formatting (no f-string in the call)":
            t["code"] = (
                "assert \"f'\" not in code and 'f\"' not in code, "
                "'pass values as logging args, not interpolated strings'\n"
                "assert 'log.warning(' in code"
            )


# ------------------------------------------------------------------ B. sqlite
def add_row_factory(ch):
    for t in ch["tests"]:
        t["code"] = t["code"].replace(
            "conn = sqlite3.connect(':memory:')\n",
            "conn = sqlite3.connect(':memory:')\nconn.row_factory = sqlite3.Row\n",
        )


def fix_transfer_commit(ch):
    for t in ch["tests"]:
        t["code"] = t["code"].replace(
            "conn.executemany('INSERT INTO accounts VALUES (?, ?)', [(1, 100), (2, 0)])\n",
            "conn.executemany('INSERT INTO accounts VALUES (?, ?)', [(1, 100), (2, 0)])\n"
            "conn.commit()\n",
        ).replace(
            "conn.executemany('INSERT INTO accounts VALUES (?, ?)', [(1, 10), (2, 0)])\n",
            "conn.executemany('INSERT INTO accounts VALUES (?, ?)', [(1, 10), (2, 0)])\n"
            "conn.commit()\n",
        )


# ------------------------------------------------------------------ C. weak spots
def fix_counter(ch):
    for t in ch["tests"]:
        if t["name"] == "independent counters":
            t["code"] = (
                "a, b = Counter(), Counter()\n"
                "a.tick(); a.tick()\n"
                "assert b.tick() == 1\n"
                "import sqlite3\n"
                "conn = sqlite3.connect(':memory:')\n"
                "conn.execute('CREATE TABLE t (v TEXT)')\n"
                "conn.commit()\n"
                "def add_row(title):\n"
                "    conn.execute(\"INSERT INTO t (v) VALUES ('\" + title + \"')\")\n"
                "    conn.commit()\n"
                "add_row(\"it's fine\")\n"
                "n = conn.execute(\"SELECT COUNT(*) FROM t WHERE v LIKE '%fine%'\").fetchone()[0]\n"
                "assert n == 1, 'a quoted value must be stored verbatim, not executed as SQL'\n"
            )


def fix_tk_pairs(ch):
    for t in ch["tests"]:
        if t["name"] == "keys stay paired regardless of finish order":
            t["code"] = (
                "import time\n"
                "start = time.monotonic()\n"
                "out = run_collect([('x', 3), ('y', 1), ('z', 2)])\n"
                "assert out == {'x': 'user-3', 'y': 'user-1', 'z': 'user-2'}\n"
                "elapsed = time.monotonic() - start\n"
                "assert elapsed < 0.12, 'fetches ran sequentially (%.3fs) - schedule them together' % elapsed\n"
            )


def fix_repo_tasks(ch):
    for t in ch["tests"]:
        if t["name"] == "add and get round-trip":
            t["code"] = t["code"].rstrip() + (
                "\ntid2 = repo.add(\"it's a trap\")\n"
                "assert repo.get(tid2)['title'] == \"it's a trap\", "
                "'a quote in the title must be stored, not break the SQL'\n"
            )


def fix_client_fast_fail(ch):
    for t in ch["tests"]:
        if t["name"] == "client error fails immediately":
            t["code"] = (
                "calls = []\n"
                "class R:\n"
                "    status = 404\n"
                "    def read(self):\n"
                "        return b'{}'\n"
                "def transport(u):\n"
                "    calls.append(u)\n"
                "    return R()\n"
                "c = MiniClient('http://api', transport=transport)\n"
                "try:\n"
                "    c.get('/missing')\n"
                "    failed = False\n"
                "except ApiError:\n"
                "    failed = True\n"
                "assert failed\n"
                "assert len(calls) == 1, 'client errors (4xx) must not be retried'\n"
            )


# ------------------------------------------------------- D. streaming behavior
NO_SLURP_LINES = (
    "from pathlib import Path\n"
    "import tempfile\n"
    "p = Path(tempfile.mkdtemp()) / 'big.txt'\n"
    "p.write_text('a b c' + chr(10) + 'd e', encoding='utf-8')\n"
    "def _no_slurp(self, *a, **k):\n"
    "    raise AssertionError('read_text() slurps the whole file - stream line by line instead')\n"
    "Path.read_text = _no_slurp\n"
    "assert count_words([p]) == 5\n"
)


def add_stream_pipeline_test(ch):
    ch["tests"].append(
        {
            "name": "streams instead of slurping",
            "code": NO_SLURP_LINES,
            "hint": "read_text() loads the entire file into memory; iterate the file object line by line.",
        }
    )


NO_SLURP_LONGEST = (
    "from pathlib import Path\n"
    "import tempfile\n"
    "p = Path(tempfile.mkdtemp()) / 'big.txt'\n"
    "p.write_text(chr(10).join(['l' * i for i in range(1, 2000)]), encoding='utf-8')\n"
    "def _no_slurp(self, *a, **k):\n"
    "    raise AssertionError('read_text() slurps the whole file - stream line by line instead')\n"
    "Path.read_text = _no_slurp\n"
    "assert longest_line(p) == 'l' * 1999\n"
)


def add_stream_longest_test(ch):
    ch["tests"].append(
        {
            "name": "streams instead of slurping",
            "code": NO_SLURP_LONGEST,
            "hint": "Track the longest line as you read; never load the whole file at once.",
        }
    )


def add_stream_chunks_test(ch):
    ch["tests"].append(
        {
            "name": "reads in blocks, not all at once",
            "code": (
                "import hashlib\n"
                "assert 'read()' not in code, 'f.read() with no size slurps the whole file - read fixed-size blocks'\n"
                "assert 'sha256' in code\n"
            ),
            "hint": "f.read() with no argument reads everything; pass a block size.",
        }
    )


VI_NEW_TESTS = {
    "streams instead of slurping": {
        "name": "Xử lý theo dòng thay vì đọc cả tệp",
        "hint": "read_text() nạp toàn bộ tệp vào bộ nhớ — hãy lặp qua tệp theo từng dòng.",
    },
    "reads in blocks, not all at once": {
        "name": "Đọc theo khối thay vì đọc cả tệp",
        "hint": "f.read() không đối số là đọc nguyên tệp — hãy đọc từng khối cố định.",
    },
}


def sync_vi(cid):
    p = find_ch(cid)
    vi_path = p[:-5] + ".vi.json"
    en = load(p)
    vi = load(vi_path)
    vi["tests"] = [
        {"name": VI_NEW_TESTS.get(t["name"], {}).get("name", t["name"]), "hint":
         VI_NEW_TESTS.get(t["name"], {}).get("hint", "")}
        for t in en["tests"]
    ]
    # preserve the original VI name/hint for untouched tests
    orig = {t["name"]: t.get("hint", "") for t in load(vi_path)["tests"]}
    for t in vi["tests"]:
        if t["name"] in orig and not t["hint"]:
            t["hint"] = orig[t["name"]]
        elif t["name"] in orig:
            pass  # new mapping already applied
    save(vi_path, vi)
    changed.append(cid + " (vi)")


# ------------------------------------------------------------- E. boilerplate
EXC_BOILERPLATE = (
    "class AppError(Exception):\n"
    "    pass\n"
    "\n"
    "class ValidationError(AppError):\n"
    "    pass\n"
    "\n"
    "class NotFoundError(AppError):\n"
    "    pass\n"
    "\n"
    "\n"
    "def classify(fn):\n"
    "    pass\n"
)


def fix_exc_order(ch):
    ch["boilerplate"] = EXC_BOILERPLATE


# ------------------------------------------------------------- F. ledger fixes
LEDGER_OVERRIDES = [
    # pi11-sec-shell: reference must genuinely call subprocess.run (no comment crutch)
    ("pi11-sec-shell", "R",
     "import subprocess\n"
     "\n"
     "def build_ffmpeg_cmd(filename):\n"
     "    return ['ffmpeg', '-i', filename, filename + '.mp4']\n"
     "\n"
     "def run_demo(filename):\n"
     "    cmd = build_ffmpeg_cmd(filename)\n"
     "    subprocess.run(cmd)\n"
     "    return cmd\n"),
    # pi10-tk-pairs: 0.05s sleeps make sequential-vs-concurrent measurable
    ("pi10-tk-pairs", "R",
     "import asyncio\n"
     "\n"
     "async def fetch_name(user_id):\n"
     "    await asyncio.sleep(0.05)\n"
     "    return f'user-{user_id}'\n"
     "\n"
     "async def collect(pairs):\n"
     "    tasks = {key: asyncio.create_task(fetch_name(uid)) for key, uid in pairs}\n"
     "    return {key: await task for key, task in tasks.items()}\n"
     "\n"
     "def run_collect(pairs):\n"
     "    return asyncio.run(collect(pairs))\n"),
    ("pi10-tk-pairs", "W",
     "import asyncio\n"
     "\n"
     "async def fetch_name(user_id):\n"
     "    await asyncio.sleep(0.05)\n"
     "    return f'user-{user_id}'\n"
     "\n"
     "async def collect(pairs):\n"
     "    out = {}\n"
     "    for key, uid in pairs:\n"
     "        out[key] = await fetch_name(uid)\n"
     "    return out\n"
     "\n"
     "def run_collect(pairs):\n"
     "    return asyncio.run(collect(pairs))\n"),
    # pi8-repo-tasks: wrong = f-string SQL in add (quote probe catches it)
    ("pi8-repo-tasks", "W",
     "import sqlite3\n"
     "\n"
     "class TaskRepository:\n"
     "    def __init__(self, conn):\n"
     "        self._conn = conn\n"
     "\n"
     "    def add(self, title):\n"
     "        cur = self._conn.execute(f'INSERT INTO tasks (title) VALUES (\\'{title}\\')')\n"
     "        self._conn.commit()\n"
     "        return cur.lastrowid\n"
     "\n"
     "    def get(self, task_id):\n"
     "        row = self._conn.execute(\n"
     "            'SELECT id, title, done FROM tasks WHERE id = ?', (task_id,)\n"
     "        ).fetchone()\n"
     "        return dict(row) if row else None\n"
     "\n"
     "    def complete(self, task_id):\n"
     "        cur = self._conn.execute(\n"
     "            'UPDATE tasks SET done = 1 WHERE id = ? AND done = 0', (task_id,)\n"
     "        )\n"
     "        self._conn.commit()\n"
     "        return cur.rowcount == 1\n"
     "\n"
     "    def all(self):\n"
     "        return [\n"
     "            dict(r)\n"
     "            for r in self._conn.execute('SELECT id, title, done FROM tasks ORDER BY id')\n"
     "        ]\n"),
    # pi8-ckpt-notes: wrong = f-string LIKE (injection probe catches it)
    ("pi8-ckpt-notes", "W",
     "import sqlite3\n"
     "\n"
     "def init_notes(conn):\n"
     "    conn.execute('''CREATE TABLE notes (\n"
     "        id INTEGER PRIMARY KEY,\n"
     "        title TEXT NOT NULL,\n"
     "        body TEXT NOT NULL\n"
     "    )''')\n"
     "    conn.commit()\n"
     "\n"
     "class NotesRepository:\n"
     "    def __init__(self, conn):\n"
     "        self._conn = conn\n"
     "\n"
     "    def add(self, title, body):\n"
     "        try:\n"
     "            cur = self._conn.execute(\n"
     "                'INSERT INTO notes (title, body) VALUES (?, ?)', (title, body)\n"
     "            )\n"
     "            self._conn.commit()\n"
     "            return cur.lastrowid\n"
     "        except sqlite3.IntegrityError as exc:\n"
     "            raise ValueError('duplicate title') from exc\n"
     "\n"
     "    def search(self, term):\n"
     "        rows = self._conn.execute(\n"
     "            f\"SELECT id, title, body FROM notes WHERE title LIKE '%{term}%'\",\n"
     "        ).fetchall()\n"
     "        return [dict(r) for r in rows]\n"
     "\n"
     "    def delete(self, note_id):\n"
     "        cur = self._conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))\n"
     "        self._conn.commit()\n"
     "        return cur.rowcount == 1\n"),
    # pi3-ctx-tracker: wrong = swallows exceptions (return True)
    ("pi3-ctx-tracker", "W",
     "EVENTS = []\n"
     "\n"
     "class Session:\n"
     "    def __enter__(self):\n"
     "        EVENTS.append('open')\n"
     "        return 'open'\n"
     "\n"
     "    def __exit__(self, exc_type, exc, tb):\n"
     "        EVENTS.append('closed')\n"
     "        return True\n"),
    # pi3-gen-parse: wrong = eager list (not a generator)
    ("pi3-gen-parse", "W",
     "def parse_scores(lines):\n"
     "    out = []\n"
     "    for line in lines:\n"
     "        cleaned = line.strip()\n"
     "        if cleaned.isdigit():\n"
     "            out.append(int(cleaned))\n"
     "    return out\n"),
    # pi1-sort-records: wrong = ties broken by name (not stable order)
    ("pi1-sort-records", "W",
     "def cheapest_first(products):\n"
     "    return sorted(products, key=lambda p: (p['price'], p['name']))\n"),
    # pi6-path-organize: wrong = no lowercase, no sort
    ("pi6-path-organize", "W",
     "from pathlib import Path\n"
     "\n"
     "def by_suffix(paths):\n"
     "    groups = {}\n"
     "    for p in paths:\n"
     "        groups.setdefault(p.suffix, []).append(p.name)\n"
     "    return groups\n"),
    # pi6-csv-rows: wrong = writer omits the header
    ("pi6-csv-rows", "W",
     "import csv, io\n"
     "\n"
     "def parse_csv(text):\n"
     "    return list(csv.DictReader(io.StringIO(text)))\n"
     "\n"
     "def to_csv_text(rows, fieldnames):\n"
     "    buf = io.StringIO()\n"
     "    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator='\\n')\n"
     "    writer.writerows(rows)\n"
     "    return buf.getvalue()\n"),
]


def append_ledger():
    with io.open(LEDGER, "a", encoding="utf-8") as f:
        f.write("\n/* --- QA repair overrides (last key wins) --- */\n")
        for cid, kind, val in LEDGER_OVERRIDES:
            f.write(kind + "[" + json.dumps(cid) + "] = " + json.dumps(val) + ";\n")
    changed.append("ledger+%d" % len(LEDGER_OVERRIDES))


if __name__ == "__main__":
    edit("pi11-sec-shell", fix_sec_shell)
    edit("pi11-sec-deser", fix_sec_deser)
    edit("pi7-mock-api", fix_mock_api)
    edit("pi7-mock-clock", fix_mock_clock)
    edit("pi7-ut-setup", fix_ut_setup)
    edit("pi7-sub-matrix", fix_sub_matrix)
    edit("pi7-sub-edges", fix_sub_edges)
    edit("pi5-log-record", fix_log_record)
    edit("pi8-repo-tasks", add_row_factory)
    edit("pi8-repo-tasks", fix_repo_tasks)
    edit("pi8-ckpt-notes", add_row_factory)
    edit("pi-cap-1-repo", add_row_factory)
    edit("pi8-tx-transfer", fix_transfer_commit)
    edit("pi2-cls-counter", fix_counter)
    edit("pi10-tk-pairs", fix_tk_pairs)
    edit("pi9-ckpt-client", fix_client_fast_fail)
    edit("pi6-stream-pipeline", add_stream_pipeline_test)
    edit("pi6-stream-longest", add_stream_longest_test)
    edit("pi6-stream-chunks", add_stream_chunks_test)
    for cid in ("pi6-stream-pipeline", "pi6-stream-longest", "pi6-stream-chunks"):
        sync_vi(cid)
    edit("pi5-exc-order", fix_exc_order)
    append_ledger()
    print("patched:", len(changed), "targets")
    for c in changed:
        print("  -", c)
