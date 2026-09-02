# Invalid-content fixtures

Each subdirectory is a deliberately broken curriculum tree used by
`tests/unit/curriculum-loaders.test.ts` to prove that invalid content throws
at load time (and therefore fails the build — CURR-04).

Structure: each case contains a `tracks/` directory (the loader's expected
root) with a named track dir inside, so every case is independently loadable
via `getTracks(<case>/tracks)`.

| Case                      | What is wrong                                          |
| ------------------------- | ------------------------------------------------------ |
| `missing-required-field/` | lesson JSON lacks the required `minutes` field         |
| `duplicate-lesson-id/`    | the same lesson id is used twice across the curriculum |
| `broken-content-path/`    | a lesson's `contentPath` points at a nonexistent file  |
| `empty-lessons-array/`    | a module has an empty `lessons` array                  |

Each tree is minimal but structurally complete apart from the injected fault
(track → course → module → lessons), so the ONLY failure is the fault itself.
