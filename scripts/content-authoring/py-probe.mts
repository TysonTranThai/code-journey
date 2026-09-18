/** Debug probe: dump the generated test file for manual inspection. */
import { writeFileSync } from "node:fs";
import { buildPyJobScript } from "../../src/workers/python-runtime";

const script = buildPyJobScript(
  {
    code: "x = 1",
    testFiles: [{ name: "probe", code: "print(sorted(_GLOBALS.keys()))" }],
  },
  "CJ_EOF_TEST",
);
const m = script.match(/cat > "test-probe.py" << 'CJ_EOF_TEST'\n([\s\S]*?)\nCJ_EOF_TEST/);
if (!m) throw new Error("test file section not found");
writeFileSync("/tmp/pytest-probe.py", m[1]);
console.log(m[1]);
