# Curriculum Research — AP Computer Science A (Beginner / Foundations)

> Researched 2026-09-20 from authoritative sources (College Board AP Central).
> No College Board questions or copyrighted material are reproduced; original
> exercises only, aligned to the public framework structure.

## Sources consulted

| Source | What it established |
| --- | --- |
| [AP CSA course page — AP Central](https://apcentral.collegeboard.org/courses/ap-computer-science-a) | Current unit structure, exam weightings, computational-thinking practices (verified 2026-09-20) |
| [AP CSA exam page — AP Central](https://apcentral.collegeboard.org/courses/ap-computer-science-a/exam) | Digital exam format, MCQ/FRQ counts, the four FRQ question types, Java Quick Reference (verified 2026-09-20) |
| [AP CSA Course and Exam Description (CED), Effective Fall 2025](https://apcentral.collegeboard.org/media/pdf/ap-computer-science-a-course-and-exam-description.pdf) | Referenced for scope; the four-unit structure quoted from the course page reflects this edition |
| AP CSA 2025 revision coverage (AP Central pages + public teacher commentary) | The Fall 2025 revision reorganized the course from 10 units to 4 and reduced the role of inheritance to a smaller, integrated topic |

## Current AP CSA framework (verified on AP Central, 2026-09-20)

### Units and multiple-choice weighting

| Unit | MCQ weight |
| --- | --- |
| 1. Using Objects and Methods | 15–25% |
| 2. Selection and Iteration | 25–35% |
| 3. Class Creation | 10–18% |
| 4. Data Collections | 30–40% |

Data Collections (arrays, ArrayList, 2D arrays) is the largest unit — the
foundations course must build especially strong fluency there.

### Computational Thinking Practices (MCQ weight)

| Practice | Weight |
| --- | --- |
| 1. Design Code | 2–10% |
| 2. Develop Code | 22–38% |
| 3. Analyze Code | 37–53% |
| 4. Document Code and Computing Systems | 10–15% |
| 5. Use Computers Responsibly | 2–10% |

**Analyze Code is the single largest assessed skill** (determine output /
result, explain why code misbehaves). The course therefore weights code
tracing, output prediction, and debugging at least as heavily as writing.

### Exam format (digital, Bluebook)

- Section I: 42 multiple-choice questions, 90 minutes, 55% of score.
- Section II: 4 free-response questions, 90 minutes, 45% of score. All FRQs
  assess Practice 2 (Develop Code) with these foci:
  1. Methods and Control Structures (2 methods, or 1 constructor + 1 method)
  2. Class Design (class header, instance variables, constructor, methods)
  3. Data Analysis with ArrayList (1 method of a provided class)
  4. 2D Array (1 method of a provided class)
- A **Java Quick Reference** sheet lists the library methods accessible on the
  exam — foundations students should learn exactly those String/ArrayList/
  Math methods, not the wider API.

### Key revision implications (Fall 2025 CED)

- **Inheritance is de-emphasized**: no longer a standalone unit; assessed at a
  smaller scale. The foundations course teaches extends/overriding/super as a
  short, careful introduction (one module + integrated practice), not a deep
  treatment — deeper polymorphism belongs to the future exam-prep course.
- **Object creation comes first**: Unit 1 has students *using* objects and
  methods before *writing* classes (Unit 3). The course mirrors that: use
  String/Math/Scanner-style objects early, design classes later.
- 2D arrays and ArrayList remain core FRQ territory (Q3/Q4).

## What the future track looks like

    ap-csa-beginner   (this course: Java foundations, AP-flavored)
          ↓
    ap-csa-core       (full framework coverage, FRQ practice per type)
          ↓
    ap-csa-advanced   (mock exams, timed FRQ sets, score-5 polish)

This course deliberately stops before exam-specific technique; it builds the
Java fluency every later stage assumes.

## Curriculum decisions (framework → course)

1. **Ordering follows AP CSA's own sequence**, not a generic Java course:
   objects/methods usage early → selection/iteration → class creation →
   data collections (the biggest block) → light inheritance → recursion/2D →
   AP-style integration and readiness checkpoint.
2. **Analyze-first pedagogy**: every module mixes "write it" challenges with
   "what is printed / what is the state / which method runs" trace challenges,
   because Practice 3 dominates the MCQ section.
3. **String methods limited to the Java Quick Reference set**: length,
   substring (1- and 2-arg), charAt, indexOf, equals, compareTo, == vs
   equals pitfall. No regex, no streams.
4. **ArrayList limited to exam methods**: add, get, set, remove, size (plus
   contains/iteration for fluency), Integer autoboxing, the
   length-vs-size() distinction, and the classic remove-while-iterating bug.
5. **Inheritance compressed** into one module + integrated problems, matching
   the de-emphasis; polymorphic tracing kept at intro level.
6. **Recursion at AP depth only**: base case, recursive case, call-stack
   tracing of 1–2 argument recursions, simple array/string recursions.
7. **2D arrays get a full module + FRQ-style problems** (row/column
   traversals, aggregation, grid reasoning) — it is a dedicated FRQ type.
8. **FRQ-style foundations woven in early and explicitly**: reading a spec,
   preconditions/postconditions, writing one method of a provided class, and
   a final module of mixed AP-style problems across all four FRQ shapes.
9. **Intentionally excluded** (general-Java or later-course material):
   multithreading, JVM internals, reflection/annotations, advanced generics,
   streams/functional style, exceptions beyond awareness, file IO, packages/
   imports beyond java.util, interfaces, enums, switch, do-while (not on the
   AP subset — noted once for completeness), networking, databases, Spring.
10. **Language**: English primary, full Vietnamese synchronization with
    Vietnamese high-school terminology; code, tests, and expected outputs are
    identical across locales.

## Execution environment (verified in-repo, 2026-09-20)

| Item | Verified value |
| --- | --- |
| Runtime | OpenJDK **21** (`docker/Dockerfile.sandbox`: `openjdk21-jdk=21.0.11_p10-r0`) |
| Compiler | `javac --release 21` (forced by `JAVA_RELEASE_FLAG` in `src/workers/java-runtime.ts`) |
| Test harness | Generated `Test_*` classes with `CjTestBase` helpers (checkEq/checkTrue/checkContains/checkLines/checkNear/checkThrows/capture) |
| CPU | `--cpus 0.5` |
| Memory | per-challenge `memoryMb` with `--memory-swap` equal (no swap) |
| Wall clock | 30 s hard cap (`MAX_TIMEOUT_MS`) |
| Network | `--network none` |
| Rootfs | read-only, tmpfs `/tmp` (exec) and `/job` (data) |
| Process limit | `--pids-limit 64` |

AP CSA uses only a Java subset; everything in the course compiles under
`--release 21` with no external libraries.
