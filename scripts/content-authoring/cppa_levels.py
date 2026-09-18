#!/usr/bin/env python3
"""Stamp deliberate-practice `level` on cpp-advanced practice challenges.

Idempotent: safe to re-run. Asserts the LEVELS map covers exactly the set of
practice challenges on disk before writing, so new challenges can't be missed.
VI sidecars carry no `level` (structural fields are EN-only per loader docs).
"""
import glob
import json
import os

BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "src/content/tracks/cpp/courses/cpp-advanced/modules",
)

LEVELS = {
    # module 1 — object model: category/lifetime drills, then derivation
    "cppa1-const-rvalue-rejects-move": "imitation",
    "cppa1-predict-category": "imitation",
    "cppa1-explicit-conversions": "imitation",
    "cppa1-destruction-order": "guided",
    "cppa1-init-narrowing": "guided",
    "cppa1-lifetime-extension": "guided",
    "cppa1-named-rvalue-is-lvalue": "guided",
    "cppa1-static-outlives-view": "guided",
    # module 2 — move/forwarding
    "cppa2-forward-wrapper": "independent",
    "cppa2-greedy-forwarding": "guided",
    "cppa2-guaranteed-elision": "combination",
    "cppa2-noexcept-vector": "combination",
    "cppa2-rule-of-zero": "combination",
    # module 3 — templates deep
    "cppa3-ctad-array": "imitation",
    "cppa3-fold-sum": "imitation",
    "cppa3-count-zeros": "guided",
    "cppa3-ctad-guide": "guided",
    "cppa3-uniform-print": "guided",
    "cppa3-variadic-min": "guided",
    "cppa3-array-bound-nttp": "independent",
    "cppa3-nttp-buffer": "independent",
    "cppa3-specialize-traits": "independent",
    "cppa3-specialize-vector3": "independent",
    # module 4 — concepts
    "cppa4-concept-write": "guided",
    "cppa4-adhoc-requires": "guided",
    "cppa4-overload-subsumption": "combination",
    # module 5 — compile time
    "cppa5-conditional-type": "guided",
    "cppa5-constexpr-parse": "guided",
    "cppa5-consteval-gate": "independent",
    "cppa5-traits-dispatch": "independent",
    # module 6 — ranges/views
    "cppa6-pipeline-basics": "imitation",
    "cppa6-projections": "independent",
    "cppa6-stride-view": "mini-build",
    "cppa6-dangling-fix": "debugging",
    # module 7 — coroutines
    "cppa7-generator-counter": "combination",
    "cppa7-generator-fib": "combination",
    "cppa7-generator-take": "combination",
    "cppa7-generator-capture-fix": "debugging",
    # module 8 — memory model
    "cppa8-atomic-hammer": "independent",
    "cppa8-release-acquire": "independent",
    "cppa8-ordering-choice": "combination",
    # module 9 — concurrency
    "cppa9-future-roundtrip": "independent",
    "cppa9-cv-handoff": "combination",
    "cppa9-parallel-sum": "combination",
    # module 10 — allocators
    "cppa10-pool-acquire": "combination",
    "cppa10-pool-release": "combination",
    "cppa10-pmr-arena": "real-world",
    # module 11 — performance
    "cppa11-alg-win": "real-world",
    "cppa11-reserve-then-build": "real-world",
    # module 12 — UB/defensive
    "cppa12-add-checked": "real-world",
    "cppa12-incident-repair": "debugging",
    # module 13 — debugging
    "cppa13-crash-forensics": "debugging",
    "cppa13-minimal-repro": "combination",
    # module 14 — testing
    "cppa14-property-roundtrip": "combination",
    "cppa14-kill-the-mutants": "combination",
    # module 15 — build systems
    "cppa15-config-guards": "combination",
    # module 16 — ABI/linking
    "cppa16-pimpl-discipline": "combination",
    "cppa16-opaque-factory": "real-world",
    # module 17 — networking
    "cppa17-frame-decoder": "combination",
    "cppa17-bounded-queue": "combination",
    # module 18 — security
    "cppa18-checked-math": "combination",
    "cppa18-path-sandbox": "real-world",
    "cppa18-shell-quote": "real-world",
    # module 19 — architecture/production
    "cppa19-event-bus": "real-world",
    "cppa19-config-ladder": "real-world",
    "cppa19-token-bucket": "real-world",
    # module 21 — capstone
    "cppa21-capstone-core": "real-world",
    "cppa21-capstone-report": "real-world",
}

VALID = {"imitation", "guided", "independent", "combination", "real-world", "debugging", "mini-build"}


def main() -> None:
    files = sorted(p for p in glob.glob(os.path.join(BASE, "*", "practices", "*", "challenges", "*.json")) if ".vi." not in p)
    on_disk = {os.path.basename(p)[:-5] for p in files}
    mapped = set(LEVELS)
    assert on_disk == mapped, (
        f"coverage mismatch: missing={sorted(on_disk - mapped)} extra={sorted(mapped - on_disk)}"
    )
    assert all(v in VALID for v in LEVELS.values()), "invalid level value"

    stamped = 0
    for p in files:
        cid = os.path.basename(p)[:-5]
        with open(p) as f:
            data = json.load(f)
        if data.get("level") == LEVELS[cid]:
            continue
        # key order: level goes after difficulty, matching sibling courses
        out = {}
        for k, v in data.items():
            out[k] = v
            if k == "difficulty" and "level" not in data:
                out["level"] = LEVELS[cid]
        if "level" not in out:
            out["level"] = LEVELS[cid]
        assert out["level"] == LEVELS[cid]
        with open(p, "w") as f:
            f.write(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
        stamped += 1
    print(f"practice challenges: {len(files)}, level stamped now: {stamped}")


if __name__ == "__main__":
    main()
