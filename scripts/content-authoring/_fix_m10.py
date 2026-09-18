#!/usr/bin/env python3
"""Fix m10 (JSON tests + ledger):

1. pa-dist-backoff test passes `random.Random(42)` (not callable) where the spec
   promises a zero-arg callable — pass the bound `.random` method instead.
2. pa-dist-queue `process` must return the QUEUE's full done/dead state (the
   test acks j1 before process() runs and expects it in the result).
3. pa-dist-idempotent-processor example: two poison sightings + max_attempts=3
   can never reach attempts 3 — the input needs a third sighting.
"""
import io
import json
import re

BASE = "src/content/tracks/python/courses/python-advanced/modules/distributed-systems/practices"
LEDGER = "scripts/content-authoring/py-solutions.mjs"

# ── 1. backoff test: callable rnd ────────────────────────────────────────────
p1 = BASE + "/pa-p10-retry-practice/challenges/pa-dist-backoff.json"
d1 = json.load(io.open(p1, encoding="utf-8"))
t1 = d1["tests"][0]
assert "random.Random(42)\n" in t1["code"], t1["code"][:80]
t1["code"] = t1["code"].replace("rnd = random.Random(42)\n", "rnd = random.Random(42).random\n")
io.open(p1, "w", encoding="utf-8").write(json.dumps(d1, indent=2, ensure_ascii=False) + "\n")

# ── 2. queue: patch test? no — test is fine; patch the LEDGER ref/wrong ─────
QUEUE_REF = (
    "class InProcessQueue:\n"
    "    '''At-least-once queue. deliver() returns every pending job (and any\n"
    "    previously delivered but un-acked job — the lease-expiry redelivery).'''\n"
    "\n"
    "    def __init__(self):\n"
    "        self._pending = []      # [job_id, payload, attempts]\n"
    "        self._inflight = []\n"
    "        self._done = {}         # job_id -> result (idempotency store)\n"
    "        self._dead = []\n"
    "\n"
    "    def enqueue(self, job_id, payload):\n"
    "        self._pending.append([job_id, payload, 0])\n"
    "\n"
    "    def deliver(self):\n"
    "        batch = self._pending + self._inflight\n"
    "        self._pending, self._inflight = [], []\n"
    "        return [list(j) for j in batch]\n"
    "\n"
    "    def ack(self, job_id, result):\n"
    "        self._done[job_id] = result\n"
    "\n"
    "    def fail(self, job_id, max_attempts=3):\n"
    "        for j in self._inflight:\n"
    "            if j[0] == job_id:\n"
    "                j[2] += 1\n"
    "                if j[2] >= max_attempts:\n"
    "                    self._dead.append(j)\n"
    "                else:\n"
    "                    self._pending.append(j)\n"
    "                self._inflight.remove(j)\n"
    "                return\n"
    "\n"
    "    @property\n"
    "    def done(self):\n"
    "        return dict(self._done)\n"
    "\n"
    "    @property\n"
    "    def dead(self):\n"
    "        return list(self._dead)\n"
    "\n"
    "\n"
    "def process(queue, jobs, max_attempts=3):\n"
    "    '''Deliver every batch until the queue stays empty. Idempotent: jobs already\n"
    "    in done are skipped; poison exhausts its retry budget into the DLQ.\n"
    "    Returns the queue's full (done, dead) state.'''\n"
    "    while True:\n"
    "        batch = queue.deliver()\n"
    "        if not batch:\n"
    "            break\n"
    "        for job_id, payload, attempts in batch:\n"
    "            if job_id in queue._done:\n"
    "                continue\n"
    "            if payload == 'poison':\n"
    "                queue.fail(job_id, max_attempts)\n"
    "                continue\n"
    "            queue.ack(job_id, f\"done:{job_id}\")\n"
    "    return queue.done, queue.dead\n"
)
QUEUE_WRONG = (
    "class InProcessQueue:\n"
    "    def __init__(self):\n"
    "        self._pending = []\n"
    "        self._inflight = []\n"
    "        self._done = {}\n"
    "        self._dead = []\n"
    "\n"
    "    def enqueue(self, job_id, payload):\n"
    "        self._pending.append([job_id, payload, 0])\n"
    "\n"
    "    def deliver(self):\n"
    "        batch = self._pending + self._inflight\n"
    "        self._pending, self._inflight = [], []\n"
    "        return [list(j) for j in batch]\n"
    "\n"
    "    def ack(self, job_id, result):\n"
    "        self._done[job_id] = result\n"
    "\n"
    "    def fail(self, job_id, max_attempts=3):\n"
    "        for j in self._inflight:\n"
    "            if j[0] == job_id:\n"
    "                self._dead.append(j)  # WRONG: straight to DLQ, no retry budget\n"
    "                self._inflight.remove(j)\n"
    "                return\n"
    "\n"
    "    @property\n"
    "    def done(self):\n"
    "        return dict(self._done)\n"
    "\n"
    "    @property\n"
    "    def dead(self):\n"
    "        return list(self._dead)\n"
    "\n"
    "\n"
    "def process(queue, jobs, max_attempts=3):\n"
    "    while True:\n"
    "        batch = queue.deliver()\n"
    "        if not batch:\n"
    "            break\n"
    "        for job_id, payload, attempts in batch:\n"
    "            if job_id in queue._done:\n"
    "                continue\n"
    "            if payload == 'poison':\n"
    "                queue.fail(job_id, max_attempts)\n"
    "                continue\n"
    "            queue.ack(job_id, f\"done:{job_id}\")\n"
    "    return queue.done, queue.dead\n"
)

# ── 3. checkpoint test: three poison sightings needed ────────────────────────
p3 = BASE.replace("/practices", "") + "/lessons/pa-checkpoint-distributed/challenges/pa-dist-idempotent-processor.json"
d3 = json.load(io.open(p3, encoding="utf-8"))
t3 = d3["tests"][0]
assert "poison" in t3["code"]
t3["code"] = (
    "batches = [[['j1', 'work', 0]], [['j1', 'work', 0], ['p', 'poison', 0]], "
    "[['p', 'poison', 1]], [['p', 'poison', 2]]]\n"
    "r = process_stream(batches, max_attempts=3)\n"
    "assert r['done'] == {'j1': 'done:j1'}\n"
    "assert r['dead'] == [['p', 'poison', 3]]\n"
    "print('ok')"
)
OLD_EX = "Example: `[('j1','work',0)], [('j1','work',0), ('p','poison',0)], [('p','poison',1)]]` with max_attempts=3"
# prompt uses a bracketed list; do a robust replacement of the example tail
d3["prompt"] = d3["prompt"].replace(
    "Example: `[[('j1','work',0)], [('j1','work',0), ('p','poison',0)], [('p','poison',1)]]` with max_attempts=3 → j1 done once, p dead at attempts 3.",
    "Example: `[[('j1','work',0)], [('j1','work',0), ('p','poison',0)], [('p','poison',1)], [('p','poison',2)]]` with max_attempts=3 → j1 done once, p dead at attempts 3 (sightings 0,1,2 → attempts 1,2,3).",
)
io.open(p3, "w", encoding="utf-8").write(json.dumps(d3, indent=2, ensure_ascii=False) + "\n")

# VI sidecar of the checkpoint challenge: same example fix
pv3 = p3.replace(".json", ".vi.json")
try:
    dv3 = json.load(io.open(pv3, encoding="utf-8"))
    dv3["prompt"] = dv3["prompt"].replace(
        "Ví dụ: `[[('j1','work',0)], [('j1','work',0), ('p','poison',0)], [('p','poison',1)]]` với max_attempts=3 → j1 xong một lần, p chết ở attempts 3.",
        "Ví dụ: `[[('j1','work',0)], [('j1','work',0), ('p','poison',0)], [('p','poison',1)], [('p','poison',2)]]` với max_attempts=3 → j1 xong một lần, p chết ở attempts 3 (gặp 0,1,2 → attempts 1,2,3).",
    )
    io.open(pv3, "w", encoding="utf-8").write(json.dumps(dv3, indent=2, ensure_ascii=False) + "\n")
except FileNotFoundError:
    print("WARN: no vi sidecar at", pv3)

# ── ledger: replace LAST R/W for pa-dist-queue ───────────────────────────────
src = io.open(LEDGER, encoding="utf-8").read()


def replace_last(src, key, kind, value):
    pat = re.compile(kind + r'\["' + re.escape(key) + r'"\] = (\{.*?\}|".*?");', re.S)
    matches = list(pat.finditer(src))
    assert matches, f"{kind}[{key}] not found"
    m = matches[-1]
    return src[: m.start()] + f'{kind}["{key}"] = {json.dumps(value)};' + src[m.end():]


src = replace_last(src, "pa-dist-queue", "R", QUEUE_REF)
src = replace_last(src, "pa-dist-queue", "W", QUEUE_WRONG)
io.open(LEDGER, "w", encoding="utf-8").write(src)

print("m10 fixer: backoff test, checkpoint example (+VI), queue ledger updated")
