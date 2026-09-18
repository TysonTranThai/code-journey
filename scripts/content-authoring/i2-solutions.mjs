/**
 * Intermediate-course challenge solutions. Appended by the i2-*.mjs
 * authoring scripts; imported by verify-challenges.mjs.
 */
export const R = {};
export const W = {};
R["i2-make-counter"] =
  "function makeCounter() {\n  let count = 0;\n  return {\n    increment() { return ++count; },\n    value() { return count; },\n  };\n}";
W["i2-make-counter"] =
  "function makeCounter() {\n  return { increment() { return 1; }, value() { return 0; } };\n}";
R["i2-rate-limiter"] =
  "function createLimiter(maxCalls) {\n  let left = maxCalls;\n  return function () {\n    if (left > 0) { left--; return true; }\n    return false;\n  };\n}";
W["i2-rate-limiter"] = "function createLimiter(maxCalls) { return function () { return true; }; }";
R["i2-memoize"] =
  "function memoize(fn) {\n  const cache = new Map();\n  return function (arg) {\n    if (cache.has(arg)) return cache.get(arg);\n    const v = fn(arg);\n    cache.set(arg, v);\n    return v;\n  };\n}";
W["i2-memoize"] = "function memoize(fn) { return fn; }";
R["i2-make-counter"] =
  "function makeCounter() {\n  let count = 0;\n  return {\n    increment() { return ++count; },\n    value() { return count; },\n  };\n}";
W["i2-make-counter"] =
  "function makeCounter() {\n  return { increment() { return 1; }, value() { return 0; } };\n}";
R["i2-rate-limiter"] =
  "function createLimiter(maxCalls) {\n  let left = maxCalls;\n  return function () {\n    if (left > 0) { left--; return true; }\n    return false;\n  };\n}";
W["i2-rate-limiter"] = "function createLimiter(maxCalls) { return function () { return true; }; }";
R["i2-memoize"] =
  "function memoize(fn) {\n  const cache = new Map();\n  return function (arg) {\n    if (cache.has(arg)) return cache.get(arg);\n    const v = fn(arg);\n    cache.set(arg, v);\n    return v;\n  };\n}";
W["i2-memoize"] = "function memoize(fn) { return fn; }";
R["i2-sum-by-user"] =
  'const orders = [\n  { user: "ada", total: 120 },\n  { user: "linh", total: 35 },\n  { user: "ada", total: 80 },\n];\n\nfunction sumByUser(orders) {\n  return orders.reduce((acc, o) => {\n    acc[o.user] = (acc[o.user] ?? 0) + o.total;\n    return acc;\n  }, {});\n}';
W["i2-sum-by-user"] = "function sumByUser(orders) { return {}; }";
R["i2-pipeline"] =
  "const orders = [];\nfunction topSpenders(orders, min) {\n  const seen = new Set();\n  return orders.filter((o) => o.total >= min).map((o) => o.user).filter((u) => { if (seen.has(u)) return false; seen.add(u); return true; });\n}\nfunction countBy(orders, keyFn) {\n  return orders.reduce((acc, o) => { const k = keyFn(o); acc[k] = (acc[k] ?? 0) + 1; return acc; }, {});\n}";
W["i2-pipeline"] =
  "function topSpenders(orders, min) { return orders.map((o) => o.user); }\nfunction countBy(orders, keyFn) { return {}; }";
R["i2-make-counter"] =
  "function makeCounter() {\n  let count = 0;\n  return {\n    increment() { return ++count; },\n    value() { return count; },\n  };\n}";
W["i2-make-counter"] =
  "function makeCounter() {\n  return { increment() { return 1; }, value() { return 0; } };\n}";
R["i2-rate-limiter"] =
  "function createLimiter(maxCalls) {\n  let left = maxCalls;\n  return function () {\n    if (left > 0) { left--; return true; }\n    return false;\n  };\n}";
W["i2-rate-limiter"] = "function createLimiter(maxCalls) { return function () { return true; }; }";
R["i2-memoize"] =
  "function memoize(fn) {\n  const cache = new Map();\n  return function (arg) {\n    if (cache.has(arg)) return cache.get(arg);\n    const v = fn(arg);\n    cache.set(arg, v);\n    return v;\n  };\n}";
W["i2-memoize"] = "function memoize(fn) { return fn; }";
R["i2-sum-by-user"] =
  'const orders = [\n  { user: "ada", total: 120 },\n  { user: "linh", total: 35 },\n  { user: "ada", total: 80 },\n];\n\nfunction sumByUser(orders) {\n  return orders.reduce((acc, o) => {\n    acc[o.user] = (acc[o.user] ?? 0) + o.total;\n    return acc;\n  }, {});\n}';
W["i2-sum-by-user"] = "function sumByUser(orders) { return {}; }";
R["i2-pipeline"] =
  "const orders = [];\nfunction topSpenders(orders, min) {\n  const seen = new Set();\n  return orders.filter((o) => o.total >= min).map((o) => o.user).filter((u) => { if (seen.has(u)) return false; seen.add(u); return true; });\n}\nfunction countBy(orders, keyFn) {\n  return orders.reduce((acc, o) => { const k = keyFn(o); acc[k] = (acc[k] ?? 0) + 1; return acc; }, {});\n}";
W["i2-pipeline"] =
  "function topSpenders(orders, min) { return orders.map((o) => o.user); }\nfunction countBy(orders, keyFn) { return {}; }";
R["i2-design-module-api"] =
  "function createCart() {\n  let items = [];\n  return {\n    add(item) { items.push(item); return items.length; },\n    total() { return items.reduce((s, i) => s + i.price, 0); },\n    clear() { items = []; },\n  };\n}";
W["i2-design-module-api"] =
  "function createCart() { return { items: [], add() { return 0; }, total() { return 0; }, clear() {} }; }";
R["i2-break-cycle"] =
  "function findCycle(graph) {\n  const visited = new Set();\n  const onPath = new Set();\n  function visit(node) {\n    if (onPath.has(node)) return true;\n    if (visited.has(node)) return false;\n    visited.add(node); onPath.add(node);\n    for (const next of graph[node] ?? []) if (visit(next)) return true;\n    onPath.delete(node);\n    return false;\n  }\n  for (const node of Object.keys(graph)) if (visit(node)) return true;\n  return false;\n}";
W["i2-break-cycle"] = "function findCycle(graph) { return false; }";
R["i2-make-counter"] =
  "function makeCounter() {\n  let count = 0;\n  return {\n    increment() { return ++count; },\n    value() { return count; },\n  };\n}";
W["i2-make-counter"] =
  "function makeCounter() {\n  return { increment() { return 1; }, value() { return 0; } };\n}";
R["i2-rate-limiter"] =
  "function createLimiter(maxCalls) {\n  let left = maxCalls;\n  return function () {\n    if (left > 0) { left--; return true; }\n    return false;\n  };\n}";
W["i2-rate-limiter"] = "function createLimiter(maxCalls) { return function () { return true; }; }";
R["i2-memoize"] =
  "function memoize(fn) {\n  const cache = new Map();\n  return function (arg) {\n    if (cache.has(arg)) return cache.get(arg);\n    const v = fn(arg);\n    cache.set(arg, v);\n    return v;\n  };\n}";
W["i2-memoize"] = "function memoize(fn) { return fn; }";
R["i2-sum-by-user"] =
  'const orders = [\n  { user: "ada", total: 120 },\n  { user: "linh", total: 35 },\n  { user: "ada", total: 80 },\n];\n\nfunction sumByUser(orders) {\n  return orders.reduce((acc, o) => {\n    acc[o.user] = (acc[o.user] ?? 0) + o.total;\n    return acc;\n  }, {});\n}';
W["i2-sum-by-user"] = "function sumByUser(orders) { return {}; }";
R["i2-pipeline"] =
  "const orders = [];\nfunction topSpenders(orders, min) {\n  const seen = new Set();\n  return orders.filter((o) => o.total >= min).map((o) => o.user).filter((u) => { if (seen.has(u)) return false; seen.add(u); return true; });\n}\nfunction countBy(orders, keyFn) {\n  return orders.reduce((acc, o) => { const k = keyFn(o); acc[k] = (acc[k] ?? 0) + 1; return acc; }, {});\n}";
W["i2-pipeline"] =
  "function topSpenders(orders, min) { return orders.map((o) => o.user); }\nfunction countBy(orders, keyFn) { return {}; }";
R["i2-design-module-api"] =
  "function createCart() {\n  let items = [];\n  return {\n    add(item) { items.push(item); return items.length; },\n    total() { return items.reduce((s, i) => s + i.price, 0); },\n    clear() { items = []; },\n  };\n}";
W["i2-design-module-api"] =
  "function createCart() { return { items: [], add() { return 0; }, total() { return 0; }, clear() {} }; }";
R["i2-break-cycle"] =
  "function findCycle(graph) {\n  const visited = new Set();\n  const onPath = new Set();\n  function visit(node) {\n    if (onPath.has(node)) return true;\n    if (visited.has(node)) return false;\n    visited.add(node); onPath.add(node);\n    for (const next of graph[node] ?? []) if (visit(next)) return true;\n    onPath.delete(node);\n    return false;\n  }\n  for (const node of Object.keys(graph)) if (visit(node)) return true;\n  return false;\n}";
W["i2-break-cycle"] = "function findCycle(graph) { return false; }";
R["i2-dedupe-set"] =
  "function dedupeTags(tags) {\n  const seen = new Set();\n  const out = [];\n  for (const t of tags) {\n    const k = t.toLowerCase();\n    if (!seen.has(k)) { seen.add(k); out.push(t); }\n  }\n  return out;\n}\nfunction hasAll(tags, needed) {\n  const s = new Set(tags.map((t) => t.toLowerCase()));\n  return needed.every((t) => s.has(t.toLowerCase()));\n}";
W["i2-dedupe-set"] =
  "function dedupeTags(tags) { return tags; }\nfunction hasAll(tags, needed) { return false; }";
R["i2-index-map"] =
  "function indexById(users) { return new Map(users.map((u) => [u.id, u])); }\nfunction lookup(index, id) { return index.get(id) ?? null; }\nfunction groupByRole(users) {\n  const m = new Map();\n  for (const u of users) {\n    const bucket = m.get(u.role) ?? [];\n    bucket.push(u);\n    m.set(u.role, bucket);\n  }\n  return m;\n}";
W["i2-index-map"] =
  "function indexById(users) { return new Map(); }\nfunction lookup(index, id) { return undefined; }\nfunction groupByRole(users) { return new Map(); }";
R["i2-pick-fields"] =
  "function pick(obj, keys) {\n  const out = {};\n  for (const k of keys) {\n    if (k in obj) out[k] = obj[k];\n  }\n  return out;\n}";
W["i2-pick-fields"] = "function pick(obj, keys) { return obj; }";
R["i2-merge-settings"] =
  "function mergeSettings(defaults, overrides) {\n  return { ...defaults, ...overrides };\n}";
W["i2-merge-settings"] =
  "function mergeSettings(defaults, overrides) {\n  Object.assign(defaults, overrides);\n  return defaults;\n}";
R["i2-stats"] =
  "function stats(...numbers) {\n  if (numbers.length === 0) return { min: 0, max: 0, avg: 0 };\n  let min = numbers[0], max = numbers[0], sum = 0;\n  for (const n of numbers) {\n    if (n < min) min = n;\n    if (n > max) max = n;\n    sum += n;\n  }\n  return { min, max, avg: sum / numbers.length };\n}";
W["i2-stats"] =
  "function stats(...numbers) { return { min: numbers[0], max: numbers[0], avg: numbers[0] }; }";
R["i2-safe-parse"] =
  "function safeParse(json, fallback) {\n  try {\n    return JSON.parse(json);\n  } catch {\n    return fallback;\n  }\n}";
W["i2-safe-parse"] = "function safeParse(json, fallback) { return JSON.parse(json); }";
R["i2-validation-error"] =
  'class ValidationError extends Error {\n  constructor(message) {\n    super(message);\n    this.name = "ValidationError";\n  }\n}\nfunction validateAge(age) {\n  if (typeof age !== "number" || Number.isNaN(age)) {\n    throw new ValidationError("age must be a number");\n  }\n  if (age < 0) {\n    throw new ValidationError("age must be non-negative");\n  }\n}\nfunction tryValidateAge(age) {\n  try {\n    validateAge(age);\n    return { ok: true, value: age };\n  } catch (err) {\n    if (err instanceof ValidationError) {\n      return { ok: false, error: err };\n    }\n    throw err;\n  }\n}';
W["i2-validation-error"] =
  'class ValidationError extends Error {\n  constructor(message) {\n    super(message);\n    this.name = "ValidationError";\n  }\n}\nfunction validateAge(age) {\n  if (age < 0) {\n    return "age must be non-negative";\n  }\n}\nfunction tryValidateAge(age) {\n  return { ok: true, value: age };\n}';
R["i2-retry-once"] =
  "function withRetry(task, retries) {\n  let last;\n  for (let attempt = 0; attempt <= retries; attempt++) {\n    try {\n      return task();\n    } catch (err) {\n      last = err;\n    }\n  }\n  throw last;\n}";
W["i2-retry-once"] = "function withRetry(task, retries) { return task(); }";
R["i2-explorer-index"] =
  "function createExplorer(records) {\n  const index = new Map(records.map((r) => [r.id, r]));\n  return {\n    byId(id) {\n      return index.get(id) ?? null;\n    },\n    count() {\n      return records.length;\n    },\n    top(n) {\n      return records\n        .map((r, i) => ({ r, i }))\n        .sort((a, b) => b.r.score - a.r.score || a.i - b.i)\n        .slice(0, n)\n        .map((e) => e.r);\n    },\n  };\n}";
W["i2-explorer-index"] =
  "function createExplorer(records) {\n  return {\n    byId(id) { return undefined; },\n    count() { return records.length; },\n    top(n) { return records; },\n  };\n}";
R["i2-explorer-query"] =
  'function createQuery(records) {\n  return function query(opts = {}) {\n    const { minScore, maxScore, sortBy = "score", order = "asc", page = 1, perPage = 2 } = opts;\n    let rows = records.filter(\n      (r) =>\n        (minScore === undefined || r.score >= minScore) &&\n        (maxScore === undefined || r.score <= maxScore),\n    );\n    rows = rows\n      .map((r, i) => ({ r, i }))\n      .sort((a, b) => {\n        const av = a.r[sortBy];\n        const bv = b.r[sortBy];\n        const cmp = av < bv ? -1 : av > bv ? 1 : 0;\n        const dir = order === "desc" ? -1 : 1;\n        return cmp * dir || a.i - b.i;\n      })\n      .map((e) => e.r);\n    const total = rows.length;\n    const pages = total === 0 ? 0 : Math.ceil(total / perPage);\n    const start = (page - 1) * perPage;\n    const items = rows.slice(start, start + perPage);\n    return { items, total, page, pages };\n  };\n}';
W["i2-explorer-query"] =
  "function createQuery(records) {\n  return function query(opts = {}) {\n    return { items: records, total: records.length, page: 1, pages: 1 };\n  };\n}";
R["i2-explorer-export"] =
  'function toCsv(records, columns) {\n  const lines = [columns.join(",")];\n  for (const r of records) {\n    lines.push(\n      columns\n        .map((c) => (r[c] === undefined || r[c] === null ? "" : String(r[c])))\n        .join(","),\n    );\n  }\n  return lines.join("\\n");\n}';
W["i2-explorer-export"] = 'function toCsv(records, columns) {\n  return columns.join(",");\n}';

R["i2-data-explorer-checkpoint"] =
  "function groupBy(records, keyFn) {\n  const out = {};\n  for (const r of records) {\n    const k = keyFn(r);\n    (out[k] ??= []).push(r);\n  }\n  return out;\n}\nfunction uniqueBy(records, keyFn) {\n  const seen = new Set();\n  const out = [];\n  for (const r of records) {\n    const k = keyFn(r);\n    if (!seen.has(k)) { seen.add(k); out.push(r); }\n  }\n  return out;\n}\nfunction summarize(records) {\n  if (records.length === 0) return { count: 0, avgScore: 0, top: null };\n  let sum = 0;\n  let top = records[0];\n  for (const r of records) {\n    sum += r.score;\n    if (r.score > top.score) top = r;\n  }\n  return { count: records.length, avgScore: sum / records.length, top };\n}\nfunction safeGet(records, index) {\n  if (!Number.isInteger(index) || index < 0 || index >= records.length) return null;\n  return records[index];\n}";
W["i2-data-explorer-checkpoint"] =
  "function groupBy() { return {}; }\nfunction uniqueBy() { return []; }\nfunction summarize() { return { count: 0, avgScore: 0, top: null }; }\nfunction safeGet() { return null; }";
R["i2-delegate-resolve"] =
  'function resolveAction(event, root) {\n  for (let el = event.target; el && el !== root; el = el.parent) {\n    if (el.matches("[data-action]")) return el;\n  }\n  return null;\n}';
W["i2-delegate-resolve"] = "function resolveAction(event, root) { return null; }";
R["i2-action-router"] =
  'function handleClick(event, root, actions) {\n  for (let el = event.target; el && el !== root; el = el.parent) {\n    if (el.matches("[data-action]")) {\n      const name = el.dataset.action;\n      if (typeof actions[name] === "function") {\n        actions[name](el);\n        return name;\n      }\n      return "missing";\n    }\n  }\n  return null;\n}';
W["i2-action-router"] = "function handleClick(event, root, actions) { return null; }";
R["i2-once-handler"] =
  "function once(fn) {\n  let done = false;\n  let result;\n  return (...args) => {\n    if (done) return result;\n    done = true;\n    result = fn(...args);\n    return result;\n  };\n}";
W["i2-once-handler"] = "function once(fn) {\n  return (...args) => fn(...args);\n}";
R["i2-modal-lifecycle"] =
  'function createModal() {\n  let open = false;\n  let opener = null;\n  let panel = null;\n  return {\n    open(trigger, root) {\n      if (open) return "already-open";\n      open = true;\n      opener = trigger;\n      panel = root;\n      return "opened";\n    },\n    close() {\n      if (!open) return "already-closed";\n      open = false;\n      panel = null;\n      return "closed";\n    },\n    opener() {\n      return opener;\n    },\n    isOpen() {\n      return open;\n    },\n  };\n}';
W["i2-modal-lifecycle"] =
  'function createModal() {\n  return { open() { return "opened"; }, close() { return "closed"; }, isOpen() { return true; } };\n}';
R["i2-accordion"] =
  "function createAccordion(count) {\n  let open = -1;\n  return {\n    toggle(i) {\n      if (i < 0 || i >= count) return;\n      open = open === i ? -1 : i;\n    },\n    isOpen(i) {\n      return open === i;\n    },\n    openCount() {\n      return open === -1 ? 0 : 1;\n    },\n  };\n}";
W["i2-accordion"] =
  "function createAccordion(count) {\n  const states = Array(count).fill(false);\n  return {\n    toggle(i) { states[i] = !states[i]; },\n    isOpen(i) { return states[i]; },\n    openCount() { return states.filter(Boolean).length; },\n  };\n}";
R["i2-validate-field"] =
  'function validateField(name, value) {\n  if (name === "name") {\n    const v = String(value).trim();\n    if (v.length < 2 || v.length > 40) return "name must be 2-40 characters";\n    return null;\n  }\n  if (name === "email") {\n    const s = String(value);\n    const at = s.indexOf("@");\n    if (at <= 0 || at === s.length - 1 || s.indexOf("@", at + 1) !== -1) {\n      return "email must be local@domain";\n    }\n    return null;\n  }\n  if (name === "age") {\n    const n = Number(value);\n    if (!Number.isFinite(n) || n < 16 || n > 120) return "age must be 16-120";\n    return null;\n  }\n  return null;\n}';
W["i2-validate-field"] = "function validateField(name, value) { return null; }";
R["i2-validate-form"] =
  'function validateField(name, value) {\n  if (name === "name") {\n    const v = String(value).trim();\n    if (v.length < 2 || v.length > 40) return "name must be 2-40 characters";\n    return null;\n  }\n  if (name === "email") {\n    const s = String(value);\n    const at = s.indexOf("@");\n    if (at <= 0 || at === s.length - 1 || s.indexOf("@", at + 1) !== -1) {\n      return "email must be local@domain";\n    }\n    return null;\n  }\n  if (name === "age") {\n    const n = Number(value);\n    if (!Number.isFinite(n) || n < 16 || n > 120) return "age must be 16-120";\n    return null;\n  }\n  return null;\n}\nfunction validateForm(values) {\n  const errors = {};\n  for (const [field, value] of Object.entries(values)) {\n    const msg = validateField(field, value);\n    if (msg) errors[field] = msg;\n  }\n  if (\n    "password" in values &&\n    "confirm" in values &&\n    values.password !== values.confirm\n  ) {\n    errors.confirm = "confirm must match password";\n  }\n  return { valid: Object.keys(errors).length === 0, errors };\n}';
W["i2-validate-form"] = "function validateForm(values) {\n  return { valid: true, errors: {} };\n}";
R["i2-row-manager"] =
  "function createRowManager() {\n  let nextId = 1;\n  let rows = [];\n  return {\n    add(label) {\n      const id = nextId++;\n      rows.push({ id, label });\n      return id;\n    },\n    remove(id) {\n      const i = rows.findIndex((r) => r.id === id);\n      if (i === -1) return false;\n      rows.splice(i, 1);\n      return true;\n    },\n    list() {\n      return rows;\n    },\n    move(id, toIndex) {\n      const from = rows.findIndex((r) => r.id === id);\n      if (from === -1) return false;\n      if (toIndex < 0 || toIndex >= rows.length) return false;\n      const [row] = rows.splice(from, 1);\n      rows.splice(toIndex, 0, row);\n      return true;\n    },\n  };\n}";
W["i2-row-manager"] =
  "function createRowManager() {\n  let rows = [];\n  let nextId = 1;\n  return {\n    add(label) { rows.push({ id: 0, label }); return 0; },\n    remove() { return false; },\n    list() { return rows; },\n    move() { return false; },\n  };\n}";
R["i2-dashboard-checkpoint"] =
  'function findActionable(target, selector) {\n  for (let el = target; el; el = el.parent) {\n    if (el.matches(selector)) return el;\n  }\n  return null;\n}\nfunction reduceTabs(state, action) {\n  if (action.type === "select") {\n    const active = Math.min(Math.max(action.index, 0), state.count - 1);\n    return { ...state, active };\n  }\n  if (action.type === "next") {\n    return { ...state, active: (state.active + 1) % state.count };\n  }\n  if (action.type === "prev") {\n    return { ...state, active: (state.active - 1 + state.count) % state.count };\n  }\n  return state;\n}\nfunction debounce(fn, ms) {\n  let t;\n  return (...args) => {\n    clearTimeout(t);\n    t = setTimeout(() => fn(...args), ms);\n  };\n}';
W["i2-dashboard-checkpoint"] =
  "function findActionable() { return null; }\nfunction reduceTabs(state) { return state; }\nfunction debounce(fn) { return fn; }";
R["i2-ordering-probe"] =
  'function runProbe(log) {\n  log("sync");\n  Promise.resolve().then(() => log("micro"));\n  setTimeout(() => log("macro"), 0);\n  return "scheduled";\n}';
W["i2-ordering-probe"] =
  'function runProbe(log) {\n  log("sync");\n  log("micro");\n  log("macro");\n  return "scheduled";\n}';
R["i2-yield-loop"] =
  "async function processChunks(items, handler, chunkSize) {\n  const results = [];\n  for (let i = 0; i < items.length; i += chunkSize) {\n    const batch = items.slice(i, i + chunkSize);\n    results.push(await handler(batch));\n    await new Promise((r) => setTimeout(r, 0));\n  }\n  return results;\n}";
W["i2-yield-loop"] =
  "async function processChunks(items, handler, chunkSize) {\n  const results = [];\n  for (let i = 0; i < items.length; i += chunkSize) {\n    results.push(handler(items.slice(i, i + chunkSize)));\n  }\n  return results;\n}";
R["i2-chain-transform"] =
  "async function pipeline(value, steps) {\n  try {\n    for (const step of steps) {\n      value = await step(value);\n    }\n    return { ok: true, value };\n  } catch (err) {\n    return { ok: false, error: err.message };\n  }\n}";
W["i2-chain-transform"] =
  "async function pipeline(value, steps) {\n  for (const step of steps) {\n    value = await step(value);\n  }\n  return { ok: true, value };\n}";
R["i2-seq-chain"] =
  'async function fetchProfile(db) {\n  try {\n    const user = await db.getUser(7);\n    const [settings, friends] = await Promise.all([\n      db.getSettings(user.id),\n      db.getFriends(user.id),\n    ]);\n    return { user, settings, friends };\n  } catch {\n    return { error: "user-not-found" };\n  }\n}';
W["i2-seq-chain"] =
  "async function fetchProfile(db) {\n  const user = await db.getUser(7);\n  const settings = await db.getSettings(7);\n  const friends = await db.getFriends(7);\n  return { user, settings, friends };\n}";
R["i2-finally-cleanup"] =
  "async function withLock(lock, job) {\n  await lock.acquire();\n  try {\n    return await job();\n  } finally {\n    await lock.release();\n  }\n}";
W["i2-finally-cleanup"] =
  "async function withLock(lock, job) {\n  await lock.acquire();\n  return await job();\n}";
R["i2-settled-report"] =
  'async function gatherReport(fetchers) {\n  const results = await Promise.allSettled(fetchers.map((f) => f.run()));\n  const ok = {};\n  const broken = [];\n  results.forEach((r, i) => {\n    if (r.status === "fulfilled") ok[fetchers[i].name] = r.value;\n    else broken.push(fetchers[i].name);\n  });\n  return { ok, broken };\n}';
W["i2-settled-report"] =
  "async function gatherReport(fetchers) {\n  const values = await Promise.all(fetchers.map((f) => f.run()));\n  return { ok: values, broken: [] };\n}";
R["i2-first-mirror"] =
  "async function fastestMirror(urls, fetchFn) {\n  return Promise.any(urls.map((u) => fetchFn(u)));\n}";
W["i2-first-mirror"] =
  "async function fastestMirror(urls, fetchFn) {\n  return Promise.race(urls.map((u) => fetchFn(u)));\n}";
R["i2-race-timeout"] =
  "async function withDeadline(task, ms, onTimeout) {\n  const timer = new Promise((res) => setTimeout(() => res(onTimeout()), ms));\n  return Promise.race([task, timer]);\n}";
W["i2-race-timeout"] = "async function withDeadline(task, ms, onTimeout) {\n  return task;\n}";

R["i2-async-checkpoint"] =
  'function createLoader(fetchFn) {\n  const cache = new Map();\n  return {\n    load(key) {\n      if (!cache.has(key)) {\n        cache.set(key, fetchFn(key));\n      }\n      return cache.get(key);\n    },\n    reset() {\n      cache.clear();\n    },\n  };\n}\nasync function loadDashboard(sources) {\n  const settled = await Promise.allSettled(sources.map((s) => s()));\n  const loaded = [];\n  const failed = [];\n  for (const r of settled) {\n    if (r.status === "fulfilled") loaded.push(r.value);\n    else failed.push(r.reason);\n  }\n  return { loaded, failed };\n}\nasync function withTimeout(promise, ms, fallback) {\n  const timer = new Promise((res) => setTimeout(() => res(fallback), ms));\n  return Promise.race([promise, timer]);\n}';
W["i2-async-checkpoint"] =
  "function createLoader(fetchFn) {\n  return { load: (key) => fetchFn(key), reset() {} };\n}\nasync function loadDashboard(sources) {\n  const loaded = await Promise.all(sources.map((s) => s()));\n  return { loaded, failed: [] };\n}\nasync function withTimeout(promise, ms, fallback) {\n  return promise;\n}";
R["i2-fetch-guard"] =
  'async function fetchJSON(url, fetchImpl, opts = {}) {\n  const realFetch = fetchImpl ?? fetch;\n  const requestOpts = { ...opts };\n  if (requestOpts.body !== undefined) {\n    requestOpts.body = JSON.stringify(requestOpts.body);\n    requestOpts.headers = { "Content-Type": "application/json", ...(requestOpts.headers ?? {}) };\n  }\n  const res = await realFetch(url, requestOpts);\n  if (!res.ok) {\n    throw new Error("HTTP " + res.status);\n  }\n  return res.json();\n}';
W["i2-fetch-guard"] =
  "async function fetchJSON(url, fetchImpl, opts = {}) {\n  const res = await fetchImpl(url, opts);\n  return res.json();\n}";
R["i2-paginate"] =
  "async function fetchAllPages(fetchPage, maxPages) {\n  const items = [];\n  let page = 1;\n  let result;\n  do {\n    result = await fetchPage(page);\n    items.push(...result.items);\n    page++;\n  } while (result.hasMore && page <= maxPages);\n  return items;\n}";
W["i2-paginate"] =
  "async function fetchAllPages(fetchPage, maxPages) {\n  const first = await fetchPage(1);\n  return first.items;\n}";
R["i2-query-builder"] =
  'function buildQuery(base, params = {}) {\n  const entries = Object.entries(params).filter(([, v]) => v !== undefined && v !== null);\n  if (entries.length === 0) return base;\n  const qs = new URLSearchParams(entries);\n  return base + "?" + qs.toString();\n}';
W["i2-query-builder"] =
  'function buildQuery(base, params = {}) {\n  return base + "?" + JSON.stringify(params);\n}';
R["i2-abort-classify"] =
  'function classifyError(err) {\n  if (err && typeof err === "object" && err.name === "AbortError") return "aborted";\n  if (err && typeof err === "object" && typeof err.message === "string") {\n    const m = err.message.toLowerCase();\n    if (m.includes("fetch") || m.includes("network")) return "network";\n  }\n  return "other";\n}';
W["i2-abort-classify"] = 'function classifyError(err) {\n  return "other";\n}';
R["i2-abortable-delay"] =
  'function abortableDelay(ms, signal) {\n  return new Promise((resolve, reject) => {\n    if (signal && signal.aborted) {\n      const e = new Error("aborted");\n      e.name = "AbortError";\n      reject(e);\n      return;\n    }\n    const onAbort = () => {\n      clearTimeout(t);\n      const e = new Error("aborted");\n      e.name = "AbortError";\n      reject(e);\n    };\n    const t = setTimeout(() => {\n      signal && signal.removeEventListener("abort", onAbort);\n      resolve("done");\n    }, ms);\n    signal && signal.addEventListener("abort", onAbort, { once: true });\n  });\n}';
W["i2-abortable-delay"] =
  'function abortableDelay(ms, signal) {\n  return new Promise((resolve) => setTimeout(() => resolve("done"), ms));\n}';
R["i2-latest-wins"] =
  "function createSearcher(runQuery) {\n  let currentId = 0;\n  let currentPromise = null;\n  return {\n    search(term) {\n      const id = ++currentId;\n      currentPromise = runQuery(term).then((value) => {\n        if (id === currentId) return value;\n        return currentPromise;\n      });\n      return id;\n    },\n    result() {\n      return currentPromise;\n    },\n  };\n}";
W["i2-latest-wins"] =
  "function createSearcher(runQuery) {\n  const results = [];\n  return {\n    async search(term) {\n      results.push(await runQuery(term));\n    },\n    result() {\n      return Promise.resolve(results[results.length - 1]);\n    },\n  };\n}";
R["i2-state-machine"] =
  'function createViewState() {\n  let state = { status: "idle" };\n  let currentId = 0;\n  return {\n    get() {\n      return { ...state };\n    },\n    load(fetchFn) {\n      const id = ++currentId;\n      state = { status: "loading" };\n      return fetchFn().then(\n        (data) => {\n          if (id === currentId) state = { status: "success", data };\n        },\n        (err) => {\n          if (id === currentId) state = { status: "error", message: err.message };\n        },\n      );\n    },\n  };\n}';
W["i2-state-machine"] =
  'function createViewState() {\n  let state = { status: "idle" };\n  return {\n    get() { return { ...state }; },\n    async load(fetchFn) {\n      state = { status: "loading" };\n      state = { status: "success", data: await fetchFn() };\n    },\n  };\n}';
R["i2-cached-client"] =
  'function createClient(fetchImpl) {\n  const cache = new Map();\n  async function request(url, opts) {\n    const res = await fetchImpl(url, opts);\n    if (!res.ok) throw new Error("HTTP " + res.status);\n    return res.json();\n  }\n  return {\n    get(url) {\n      if (!cache.has(url)) cache.set(url, request(url));\n      return cache.get(url);\n    },\n    invalidate(url) {\n      cache.delete(url);\n    },\n    invalidateAll() {\n      cache.clear();\n    },\n    post(url, body) {\n      return request(url, {\n        method: "POST",\n        body: JSON.stringify(body),\n        headers: { "Content-Type": "application/json" },\n      });\n    },\n  };\n}';
W["i2-cached-client"] =
  'function createClient(fetchImpl) {\n  return {\n    async get(url) {\n      const res = await fetchImpl(url);\n      return res.json();\n    },\n    invalidate() {},\n    invalidateAll() {},\n    async post(url, body) {\n      const res = await fetchImpl(url, { method: "POST", body });\n      return res.json();\n    },\n  };\n}';
R["i2-token-theme"] =
  ':root {\n  --color-bg: #ffffff;\n  --color-fg: #111827;\n  --color-accent: #2563eb;\n}\n[data-theme="dark"] {\n  --color-bg: #0b1120;\n  --color-fg: #e2e8f0;\n}\n.card {\n  background: var(--color-bg);\n  color: var(--color-fg);\n  border: 1px solid var(--color-accent);\n}';
W["i2-token-theme"] =
  ":root {\n  --color-bg: #ffffff;\n  --color-fg: #111827;\n}\n.card {\n  background: #ffffff;\n  color: #111827;\n}";
R["i2-auto-gallery"] =
  ".gallery {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));\n  gap: 1rem;\n}";
W["i2-auto-gallery"] = ".gallery { display: grid; grid-template-columns: 200px; }";
R["i2-app-shell"] =
  '.shell {\n  display: grid;\n  grid-template-areas:\n    "head head"\n    "side main"\n    "side foot";\n  grid-template-columns: 220px 1fr;\n}';
W["i2-app-shell"] = ".shell { display: grid; }";
R["i2-container-card"] =
  ".slot { container-type: inline-size; }\n@container (min-width: 420px) {\n  .card {\n    display: grid;\n    grid-template-columns: 120px 1fr;\n  }\n}";
W["i2-container-card"] = ".slot {}\n.card { display: grid; grid-template-columns: 120px 1fr; }";
R["i2-disclosure"] =
  'function createDisclosure() {\n  let open = false;\n  return {\n    toggle() {\n      open = !open;\n      return open ? "expanded" : "collapsed";\n    },\n    isOpen() {\n      return open;\n    },\n    state() {\n      return {\n        open,\n        ariaExpanded: open ? "true" : "false",\n        hidden: !open,\n      };\n    },\n  };\n}';
W["i2-disclosure"] =
  'function createDisclosure() {\n  let open = true;\n  return {\n    toggle() { open = !open; return "expanded"; },\n    isOpen() { return open; },\n    state() { return { open, ariaExpanded: "true", hidden: false }; },\n  };\n}';
R["i2-sort-reducer"] =
  'function sortRows(rows, key, dir) {\n  return [...rows].sort((a, b) => {\n    const av = a[key];\n    const bv = b[key];\n    let cmp;\n    if (typeof av === "number" && typeof bv === "number") {\n      cmp = av - bv;\n    } else {\n      cmp = String(av).localeCompare(String(bv));\n    }\n    return dir === "asc" ? cmp : -cmp;\n  });\n}\nfunction nextSortDir(current) {\n  return current === "asc" ? "desc" : "asc";\n}';
W["i2-sort-reducer"] =
  'function sortRows(rows, key, dir) {\n  rows.sort((a, b) => (a[key] > b[key] ? 1 : -1));\n  return rows;\n}\nfunction nextSortDir(current) {\n  return "asc";\n}';
R["i2-focus-plan"] =
  "function focusPlan({ focusables, currentIndex, forward, restoreIndex }) {\n  const n = focusables;\n  const next = (currentIndex + (forward ? 1 : -1) + n) % n;\n  return { next, restoreTo: restoreIndex };\n}";
W["i2-focus-plan"] =
  "function focusPlan({ focusables, currentIndex, forward, restoreIndex }) {\n  return { next: forward ? currentIndex + 1 : currentIndex - 1, restoreTo: restoreIndex };\n}";
R["i2-motion-reduced"] =
  ".panel {\n  transition: transform 0.25s ease;\n}\n.panel.is-closed {\n  transform: translateX(-100%);\n}\n@media (prefers-reduced-motion: reduce) {\n  *, *::before, *::after {\n    animation-duration: 0.01ms !important;\n    transition-duration: 0.01ms !important;\n  }\n}";
W["i2-motion-reduced"] =
  ".panel {\n  transition: width 0.25s;\n}\n.panel.is-closed {\n  width: 0;\n}";
R["i2-dash-tokens"] =
  'function buildTheme(base, overrides) {\n  const out = { ...base };\n  for (const k of Object.keys(overrides)) {\n    const b = base[k];\n    const o = overrides[k];\n    out[k] = b && o && typeof b === "object" && typeof o === "object"\n      ? buildTheme(b, o)\n      : o;\n  }\n  return out;\n}\nfunction tokenValue(tokens, path, fallback) {\n  const v = path.split(".").reduce((o, k) => (o == null ? undefined : o[k]), tokens);\n  return v === undefined ? fallback : v;\n}';
W["i2-dash-tokens"] =
  "function buildTheme(base, overrides) {\n  return { ...base, ...overrides };\n}\nfunction tokenValue(tokens, path, fallback) {\n  return fallback;\n}";
R["i2-widget-planner"] =
  "function planLayout(widgets, cols) {\n  const buckets = Array.from({ length: cols }, () => []);\n  widgets.forEach((w, i) => buckets[i % cols].push(w));\n  return buckets;\n}\nfunction place(widgets, cols, index) {\n  return { row: Math.floor(index / cols), col: index % cols };\n}";
W["i2-widget-planner"] =
  "function planLayout(widgets, cols) {\n  return [widgets];\n}\nfunction place(widgets, cols, index) {\n  return { row: 0, col: index };\n}";
R["i2-token-theme"] =
  ':root {\n  --color-bg: #ffffff;\n  --color-fg: #111827;\n  --color-accent: #2563eb;\n}\n[data-theme="dark"] {\n  --color-bg: #0b1120;\n  --color-fg: #e2e8f0;\n}\n.card {\n  background: var(--color-bg);\n  color: var(--color-fg);\n  border: 1px solid var(--color-accent);\n}';
W["i2-token-theme"] =
  ":root {\n  --color-bg: #ffffff;\n  --color-fg: #111827;\n}\n.card {\n  background: #ffffff;\n  color: #111827;\n}";
R["i2-auto-gallery"] =
  ".gallery {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));\n  gap: 1rem;\n}";
W["i2-auto-gallery"] = ".gallery { display: grid; grid-template-columns: 200px; }";
R["i2-app-shell"] =
  '.shell {\n  display: grid;\n  grid-template-areas:\n    "head head"\n    "side main"\n    "side foot";\n  grid-template-columns: 220px 1fr;\n}';
W["i2-app-shell"] = ".shell { display: grid; }";
R["i2-container-card"] =
  ".slot { container-type: inline-size; }\n@container (min-width: 420px) {\n  .card {\n    display: grid;\n    grid-template-columns: 120px 1fr;\n  }\n}";
W["i2-container-card"] = ".slot {}\n.card { display: grid; grid-template-columns: 120px 1fr; }";
R["i2-disclosure"] =
  'function createDisclosure() {\n  let open = false;\n  return {\n    toggle() {\n      open = !open;\n      return open ? "expanded" : "collapsed";\n    },\n    isOpen() {\n      return open;\n    },\n    state() {\n      return {\n        open,\n        ariaExpanded: open ? "true" : "false",\n        hidden: !open,\n      };\n    },\n  };\n}';
W["i2-disclosure"] =
  'function createDisclosure() {\n  let open = true;\n  return {\n    toggle() { open = !open; return "expanded"; },\n    isOpen() { return open; },\n    state() { return { open, ariaExpanded: "true", hidden: false }; },\n  };\n}';
R["i2-sort-reducer"] =
  'function sortRows(rows, key, dir) {\n  return [...rows].sort((a, b) => {\n    const av = a[key];\n    const bv = b[key];\n    let cmp;\n    if (typeof av === "number" && typeof bv === "number") {\n      cmp = av - bv;\n    } else {\n      cmp = String(av).localeCompare(String(bv));\n    }\n    return dir === "asc" ? cmp : -cmp;\n  });\n}\nfunction nextSortDir(current) {\n  return current === "asc" ? "desc" : "asc";\n}';
W["i2-sort-reducer"] =
  'function sortRows(rows, key, dir) {\n  rows.sort((a, b) => (a[key] > b[key] ? 1 : -1));\n  return rows;\n}\nfunction nextSortDir(current) {\n  return "asc";\n}';
R["i2-focus-plan"] =
  "function focusPlan({ focusables, currentIndex, forward, restoreIndex }) {\n  const n = focusables;\n  const next = (currentIndex + (forward ? 1 : -1) + n) % n;\n  return { next, restoreTo: restoreIndex };\n}";
W["i2-focus-plan"] =
  "function focusPlan({ focusables, currentIndex, forward, restoreIndex }) {\n  return { next: forward ? currentIndex + 1 : currentIndex - 1, restoreTo: restoreIndex };\n}";
R["i2-motion-reduced"] =
  ".panel {\n  transition: transform 0.25s ease;\n}\n.panel.is-closed {\n  transform: translateX(-100%);\n}\n@media (prefers-reduced-motion: reduce) {\n  *, *::before, *::after {\n    animation-duration: 0.01ms !important;\n    transition-duration: 0.01ms !important;\n  }\n}";
W["i2-motion-reduced"] =
  ".panel {\n  transition: width 0.25s;\n}\n.panel.is-closed {\n  width: 0;\n}";
R["i2-dash-tokens"] =
  'function buildTheme(base, overrides) {\n  const out = { ...base };\n  for (const k of Object.keys(overrides)) {\n    const b = base[k];\n    const o = overrides[k];\n    out[k] = b && o && typeof b === "object" && typeof o === "object"\n      ? buildTheme(b, o)\n      : o;\n  }\n  return out;\n}\nfunction tokenValue(tokens, path, fallback) {\n  const v = path.split(".").reduce((o, k) => (o == null ? undefined : o[k]), tokens);\n  return v === undefined ? fallback : v;\n}';
W["i2-dash-tokens"] =
  "function buildTheme(base, overrides) {\n  return { ...base, ...overrides };\n}\nfunction tokenValue(tokens, path, fallback) {\n  return fallback;\n}";
R["i2-widget-planner"] =
  "function planLayout(widgets, cols) {\n  const buckets = Array.from({ length: cols }, () => []);\n  widgets.forEach((w, i) => buckets[i % cols].push(w));\n  return buckets;\n}\nfunction place(widgets, cols, index) {\n  return { row: Math.floor(index / cols), col: index % cols };\n}";
W["i2-widget-planner"] =
  "function planLayout(widgets, cols) {\n  return [widgets];\n}\nfunction place(widgets, cols, index) {\n  return { row: 0, col: index };\n}";

R["i2-ui-checkpoint"] =
  'function resolveTokens(scopes) {\n  return scopes.reduce((acc, scope) => ({ ...acc, ...scope }), {});\n}\nfunction applyTheme(state, action) {\n  if (action.type === "set") {\n    return { ...state, mode: action.mode, explicit: true };\n  }\n  if (action.type === "reset") {\n    return { mode: "system", explicit: false };\n  }\n  return state;\n}\nfunction motionPolicy(prefersReducedMotion, userSetting) {\n  if (userSetting === "reduced") return "reduced";\n  if (userSetting === "full") return "full";\n  return prefersReducedMotion ? "reduced" : "full";\n}';
W["i2-ui-checkpoint"] =
  'function resolveTokens(scopes) { return {}; }\nfunction applyTheme(state, action) { return state; }\nfunction motionPolicy() { return "full"; }';
R["i2-token-theme"] =
  ':root {\n  --color-bg: #ffffff;\n  --color-fg: #111827;\n  --color-accent: #2563eb;\n}\n[data-theme="dark"] {\n  --color-bg: #0b1120;\n  --color-fg: #e2e8f0;\n}\n.card {\n  background: var(--color-bg);\n  color: var(--color-fg);\n  border: 1px solid var(--color-accent);\n}';
W["i2-token-theme"] =
  ":root {\n  --color-bg: #ffffff;\n  --color-fg: #111827;\n}\n.card {\n  background: #ffffff;\n  color: #111827;\n}";
R["i2-auto-gallery"] =
  ".gallery {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));\n  gap: 1rem;\n}";
W["i2-auto-gallery"] = ".gallery { display: grid; grid-template-columns: 200px; }";
R["i2-app-shell"] =
  '.shell {\n  display: grid;\n  grid-template-areas:\n    "head head"\n    "side main"\n    "side foot";\n  grid-template-columns: 220px 1fr;\n}';
W["i2-app-shell"] = ".shell { display: grid; }";
R["i2-container-card"] =
  ".slot { container-type: inline-size; }\n@container (min-width: 420px) {\n  .card {\n    display: grid;\n    grid-template-columns: 120px 1fr;\n  }\n}";
W["i2-container-card"] = ".slot {}\n.card { display: grid; grid-template-columns: 120px 1fr; }";
R["i2-disclosure"] =
  'function createDisclosure() {\n  let open = false;\n  return {\n    toggle() {\n      open = !open;\n      return open ? "expanded" : "collapsed";\n    },\n    isOpen() {\n      return open;\n    },\n    state() {\n      return {\n        open,\n        ariaExpanded: open ? "true" : "false",\n        hidden: !open,\n      };\n    },\n  };\n}';
W["i2-disclosure"] =
  'function createDisclosure() {\n  let open = true;\n  return {\n    toggle() { open = !open; return "expanded"; },\n    isOpen() { return open; },\n    state() { return { open, ariaExpanded: "true", hidden: false }; },\n  };\n}';
R["i2-sort-reducer"] =
  'function sortRows(rows, key, dir) {\n  return [...rows].sort((a, b) => {\n    const av = a[key];\n    const bv = b[key];\n    let cmp;\n    if (typeof av === "number" && typeof bv === "number") {\n      cmp = av - bv;\n    } else {\n      cmp = String(av).localeCompare(String(bv));\n    }\n    return dir === "asc" ? cmp : -cmp;\n  });\n}\nfunction nextSortDir(current) {\n  return current === "asc" ? "desc" : "asc";\n}';
W["i2-sort-reducer"] =
  'function sortRows(rows, key, dir) {\n  rows.sort((a, b) => (a[key] > b[key] ? 1 : -1));\n  return rows;\n}\nfunction nextSortDir(current) {\n  return "asc";\n}';
R["i2-focus-plan"] =
  "function focusPlan({ focusables, currentIndex, forward, restoreIndex }) {\n  const n = focusables;\n  const next = (currentIndex + (forward ? 1 : -1) + n) % n;\n  return { next, restoreTo: restoreIndex };\n}";
W["i2-focus-plan"] =
  "function focusPlan({ focusables, currentIndex, forward, restoreIndex }) {\n  return { next: forward ? currentIndex + 1 : currentIndex - 1, restoreTo: restoreIndex };\n}";
R["i2-motion-reduced"] =
  ".panel {\n  transition: transform 0.25s ease;\n}\n.panel.is-closed {\n  transform: translateX(-100%);\n}\n@media (prefers-reduced-motion: reduce) {\n  *, *::before, *::after {\n    animation-duration: 0.01ms !important;\n    transition-duration: 0.01ms !important;\n  }\n}";
W["i2-motion-reduced"] =
  ".panel {\n  transition: width 0.25s;\n}\n.panel.is-closed {\n  width: 0;\n}";
R["i2-dash-tokens"] =
  'function buildTheme(base, overrides) {\n  const out = { ...base };\n  for (const k of Object.keys(overrides)) {\n    const b = base[k];\n    const o = overrides[k];\n    out[k] = b && o && typeof b === "object" && typeof o === "object"\n      ? buildTheme(b, o)\n      : o;\n  }\n  return out;\n}\nfunction tokenValue(tokens, path, fallback) {\n  const v = path.split(".").reduce((o, k) => (o == null ? undefined : o[k]), tokens);\n  return v === undefined ? fallback : v;\n}';
W["i2-dash-tokens"] =
  "function buildTheme(base, overrides) {\n  return { ...base, ...overrides };\n}\nfunction tokenValue(tokens, path, fallback) {\n  return fallback;\n}";
R["i2-widget-planner"] =
  "function planLayout(widgets, cols) {\n  const buckets = Array.from({ length: cols }, () => []);\n  widgets.forEach((w, i) => buckets[i % cols].push(w));\n  return buckets;\n}\nfunction place(widgets, cols, index) {\n  return { row: Math.floor(index / cols), col: index % cols };\n}";
W["i2-widget-planner"] =
  "function planLayout(widgets, cols) {\n  return [widgets];\n}\nfunction place(widgets, cols, index) {\n  return { row: 0, col: index };\n}";
R["i2-shape-guard"] =
  'function hasShape(obj, spec) {\n  if (typeof obj !== "object" || obj === null) return false;\n  return Object.entries(spec).every(([k, t]) => typeof obj[k] === t);\n}';
W["i2-shape-guard"] = "function hasShape(obj, spec) { return true; }";
R["i2-normalize"] =
  'function normalizeUsers(raw) {\n  const out = [];\n  for (const r of raw) {\n    if (r && typeof r === "object" && typeof r.name === "string") {\n      const age = Number(r.age);\n      if (Number.isFinite(age)) {\n        out.push({ name: r.name.trim(), age });\n      }\n    }\n  }\n  return out;\n}';
W["i2-normalize"] =
  "function normalizeUsers(raw) {\n  return raw.map((r) => ({ name: r.name, age: Number(r.age) }));\n}";
R["i2-omit-pick"] =
  "function pick(obj, keys) {\n  const out = {};\n  for (const k of keys) {\n    if (k in obj) out[k] = obj[k];\n  }\n  return out;\n}\nfunction omit(obj, keys) {\n  const out = { ...obj };\n  for (const k of keys) {\n    delete out[k];\n  }\n  return out;\n}";
W["i2-omit-pick"] =
  "function pick(obj, keys) {\n  for (const k of keys) delete obj[k];\n  return obj;\n}\nfunction omit(obj, keys) {\n  for (const k of keys) delete obj[k];\n  return obj;\n}";
R["i2-narrow-format"] =
  'function format(value) {\n  if (value === null || value === undefined) return "\u2014";\n  if (typeof value === "string") return value.trim();\n  if (typeof value === "number") return value.toFixed(2);\n  if (typeof value === "boolean") return value ? "yes" : "no";\n  throw new Error("unreachable");\n}';
W["i2-narrow-format"] =
  'function format(value) {\n  if (!value) return "\u2014";\n  return String(value);\n}';
R["i2-union-reducer"] =
  'function reduceRequest(state, action) {\n  switch (action.type) {\n    case "start": return { kind: "loading" };\n    case "resolve": return { kind: "success", data: action.data };\n    case "reject": return { kind: "error", message: action.message };\n    case "reset": return { kind: "idle" };\n    default: return state;\n  }\n}';
W["i2-union-reducer"] =
  "function reduceRequest(state, action) {\n  state.kind = action.type;\n  return state;\n}";
R["i2-exhaustive"] =
  'function describeShape(v) {\n  if (v === null) return "nothing";\n  if (typeof v === "string") return "text";\n  if (typeof v === "number") return "number";\n  if (typeof v === "boolean") return "flag";\n  if (Array.isArray(v)) return "list of " + v.length;\n  throw new Error("Unhandled shape");\n}';
W["i2-exhaustive"] = "function describeShape(v) {\n  return String(v);\n}";
R["i2-first-or"] =
  "function firstOr(items, fallback) {\n  return items.length > 0 ? items[0] : fallback;\n}";
W["i2-first-or"] =
  "function firstOr(items, fallback) {\n  return items[items.length] ?? fallback;\n}";
R["i2-group-by"] =
  "function groupBy(items, keyFn) {\n  const out = {};\n  for (const item of items) {\n    const k = keyFn(item);\n    (out[k] ??= []).push(item);\n  }\n  return out;\n}\nfunction keyCount(groups) {\n  return Object.keys(groups).length;\n}";
W["i2-group-by"] =
  "function groupBy(items, keyFn) {\n  return {};\n}\nfunction keyCount(groups) {\n  return 0;\n}";
R["i2-result-wrap"] =
  "function attempt(fn) {\n  try {\n    return { ok: true, value: fn() };\n  } catch (err) {\n    return { ok: false, error: err.message };\n  }\n}";
W["i2-result-wrap"] = "function attempt(fn) {\n  return { ok: true, value: fn() };\n}";
R["i2-unknown-handler"] =
  'function handleUnknown(payload) {\n  if (Array.isArray(payload) && payload.every((x) => typeof x === "string")) {\n    return { kind: "tags", tags: payload.map((s) => s.trim()) };\n  }\n  if (typeof payload === "number" && Number.isFinite(payload)) {\n    return { kind: "count", count: payload };\n  }\n  if (payload && typeof payload === "object" && typeof payload.id === "string") {\n    return { kind: "entity", id: payload.id };\n  }\n  return { kind: "reject" };\n}';
W["i2-unknown-handler"] =
  'function handleUnknown(payload) {\n  return { kind: "tags", tags: payload };\n}';
R["i2-storage-guard"] =
  "function loadSetting(storage, key, isShape, fallback) {\n  let parsed;\n  try {\n    const raw = storage.getItem(key);\n    if (raw === null) return { ok: false, fallback };\n    parsed = JSON.parse(raw);\n  } catch {\n    return { ok: false, fallback };\n  }\n  if (!isShape(parsed)) return { ok: false, fallback };\n  return { ok: true, value: parsed };\n}\nfunction saveSetting(storage, key, value) {\n  storage.setItem(key, JSON.stringify(value));\n}";
W["i2-storage-guard"] =
  "function loadSetting(storage, key, isShape, fallback) {\n  return { ok: true, value: JSON.parse(storage.getItem(key)) };\n}\nfunction saveSetting(storage, key, value) {\n  storage.setItem(key, value);\n}";
R["i2-safe-json"] =
  "function parseOr(raw, fallback) {\n  try {\n    return JSON.parse(raw);\n  } catch {\n    return fallback;\n  }\n}\nfunction serialize(value, fallback) {\n  try {\n    return JSON.stringify(value);\n  } catch {\n    return fallback;\n  }\n}";
W["i2-safe-json"] =
  "function parseOr(raw, fallback) {\n  return JSON.parse(raw);\n}\nfunction serialize(value, fallback) {\n  return JSON.stringify(value);\n}";
R["i2-dto-validators"] =
  'function isTaskDTO(v) {\n  if (!v || typeof v !== "object" || Array.isArray(v)) return false;\n  if (typeof v.id !== "string") return false;\n  if (typeof v.title !== "string" || v.title.trim().length === 0) return false;\n  if (typeof v.done !== "boolean") return false;\n  if (v.due !== undefined && typeof v.due !== "string") return false;\n  return true;\n}\nfunction isTaskListDTO(v) {\n  return Array.isArray(v) && v.every(isTaskDTO);\n}';
W["i2-dto-validators"] =
  "function isTaskDTO(v) { return !!v; }\nfunction isTaskListDTO(v) { return Array.isArray(v); }";
R["i2-api-result"] =
  "async function toApiResult(promise) {\n  try {\n    const data = await promise;\n    return { ok: true, data };\n  } catch (err) {\n    return { ok: false, status: 0, message: err.message };\n  }\n}\nfunction unwrap(result) {\n  if (result.ok) return result.data;\n  throw new Error(result.message);\n}";
W["i2-api-result"] =
  "async function toApiResult(promise) {\n  const data = await promise;\n  return { ok: true, data };\n}\nfunction unwrap(result) {\n  return result.data;\n}";
R["i2-typed-client"] =
  'function createTypedClient(fetchImpl) {\n  async function getJSON(url) {\n    const res = await fetchImpl(url);\n    return { res, body: await res.json() };\n  }\n  return {\n    async getTask(id) {\n      const { res, body } = await getJSON("/tasks/" + id);\n      if (!res.ok) return { ok: false, reason: "not-found" };\n      if (!isTaskDTO(body)) return { ok: false, reason: "invalid" };\n      return { ok: true, task: body };\n    },\n    async listTasks() {\n      const { res, body } = await getJSON("/tasks");\n      if (!res.ok || !isTaskListDTO(body)) return { ok: false, reason: "invalid" };\n      return { ok: true, tasks: body };\n    },\n  };\n}\nfunction isTaskDTO(v) {\n  if (!v || typeof v !== "object" || Array.isArray(v)) return false;\n  return typeof v.id === "string" && typeof v.title === "string" && v.title.length > 0 && typeof v.done === "boolean";\n}\nfunction isTaskListDTO(v) {\n  return Array.isArray(v) && v.every(isTaskDTO);\n}';
W["i2-typed-client"] =
  'function createTypedClient(fetchImpl) {\n  return {\n    async getTask(id) {\n      const res = await fetchImpl("/tasks/" + id);\n      return { ok: true, task: await res.json() };\n    },\n    async listTasks() {\n      const res = await fetchImpl("/tasks");\n      return { ok: true, tasks: await res.json() };\n    },\n  };\n}';
R["i2-shape-guard"] =
  'function hasShape(obj, spec) {\n  if (typeof obj !== "object" || obj === null) return false;\n  return Object.entries(spec).every(([k, t]) => typeof obj[k] === t);\n}';
W["i2-shape-guard"] = "function hasShape(obj, spec) { return true; }";
R["i2-normalize"] =
  'function normalizeUsers(raw) {\n  const out = [];\n  for (const r of raw) {\n    if (r && typeof r === "object" && typeof r.name === "string") {\n      const age = Number(r.age);\n      if (Number.isFinite(age)) {\n        out.push({ name: r.name.trim(), age });\n      }\n    }\n  }\n  return out;\n}';
W["i2-normalize"] =
  "function normalizeUsers(raw) {\n  return raw.map((r) => ({ name: r.name, age: Number(r.age) }));\n}";
R["i2-omit-pick"] =
  "function pick(obj, keys) {\n  const out = {};\n  for (const k of keys) {\n    if (k in obj) out[k] = obj[k];\n  }\n  return out;\n}\nfunction omit(obj, keys) {\n  const out = { ...obj };\n  for (const k of keys) {\n    delete out[k];\n  }\n  return out;\n}";
W["i2-omit-pick"] =
  "function pick(obj, keys) {\n  for (const k of keys) delete obj[k];\n  return obj;\n}\nfunction omit(obj, keys) {\n  for (const k of keys) delete obj[k];\n  return obj;\n}";
R["i2-narrow-format"] =
  'function format(value) {\n  if (value === null || value === undefined) return "\u2014";\n  if (typeof value === "string") return value.trim();\n  if (typeof value === "number") return value.toFixed(2);\n  if (typeof value === "boolean") return value ? "yes" : "no";\n  throw new Error("unreachable");\n}';
W["i2-narrow-format"] =
  'function format(value) {\n  if (!value) return "\u2014";\n  return String(value);\n}';
R["i2-union-reducer"] =
  'function reduceRequest(state, action) {\n  switch (action.type) {\n    case "start": return { kind: "loading" };\n    case "resolve": return { kind: "success", data: action.data };\n    case "reject": return { kind: "error", message: action.message };\n    case "reset": return { kind: "idle" };\n    default: return state;\n  }\n}';
W["i2-union-reducer"] =
  "function reduceRequest(state, action) {\n  state.kind = action.type;\n  return state;\n}";
R["i2-exhaustive"] =
  'function describeShape(v) {\n  if (v === null) return "nothing";\n  if (typeof v === "string") return "text";\n  if (typeof v === "number") return "number";\n  if (typeof v === "boolean") return "flag";\n  if (Array.isArray(v)) return "list of " + v.length;\n  throw new Error("Unhandled shape");\n}';
W["i2-exhaustive"] = "function describeShape(v) {\n  return String(v);\n}";
R["i2-first-or"] =
  "function firstOr(items, fallback) {\n  return items.length > 0 ? items[0] : fallback;\n}";
W["i2-first-or"] =
  "function firstOr(items, fallback) {\n  return items[items.length] ?? fallback;\n}";
R["i2-group-by"] =
  "function groupBy(items, keyFn) {\n  const out = {};\n  for (const item of items) {\n    const k = keyFn(item);\n    (out[k] ??= []).push(item);\n  }\n  return out;\n}\nfunction keyCount(groups) {\n  return Object.keys(groups).length;\n}";
W["i2-group-by"] =
  "function groupBy(items, keyFn) {\n  return {};\n}\nfunction keyCount(groups) {\n  return 0;\n}";
R["i2-result-wrap"] =
  "function attempt(fn) {\n  try {\n    return { ok: true, value: fn() };\n  } catch (err) {\n    return { ok: false, error: err.message };\n  }\n}";
W["i2-result-wrap"] = "function attempt(fn) {\n  return { ok: true, value: fn() };\n}";
R["i2-unknown-handler"] =
  'function handleUnknown(payload) {\n  if (Array.isArray(payload) && payload.every((x) => typeof x === "string")) {\n    return { kind: "tags", tags: payload.map((s) => s.trim()) };\n  }\n  if (typeof payload === "number" && Number.isFinite(payload)) {\n    return { kind: "count", count: payload };\n  }\n  if (payload && typeof payload === "object" && typeof payload.id === "string") {\n    return { kind: "entity", id: payload.id };\n  }\n  return { kind: "reject" };\n}';
W["i2-unknown-handler"] =
  'function handleUnknown(payload) {\n  return { kind: "tags", tags: payload };\n}';
R["i2-storage-guard"] =
  "function loadSetting(storage, key, isShape, fallback) {\n  let parsed;\n  try {\n    const raw = storage.getItem(key);\n    if (raw === null) return { ok: false, fallback };\n    parsed = JSON.parse(raw);\n  } catch {\n    return { ok: false, fallback };\n  }\n  if (!isShape(parsed)) return { ok: false, fallback };\n  return { ok: true, value: parsed };\n}\nfunction saveSetting(storage, key, value) {\n  storage.setItem(key, JSON.stringify(value));\n}";
W["i2-storage-guard"] =
  "function loadSetting(storage, key, isShape, fallback) {\n  return { ok: true, value: JSON.parse(storage.getItem(key)) };\n}\nfunction saveSetting(storage, key, value) {\n  storage.setItem(key, value);\n}";
R["i2-safe-json"] =
  "function parseOr(raw, fallback) {\n  try {\n    return JSON.parse(raw);\n  } catch {\n    return fallback;\n  }\n}\nfunction serialize(value, fallback) {\n  try {\n    return JSON.stringify(value);\n  } catch {\n    return fallback;\n  }\n}";
W["i2-safe-json"] =
  "function parseOr(raw, fallback) {\n  return JSON.parse(raw);\n}\nfunction serialize(value, fallback) {\n  return JSON.stringify(value);\n}";
R["i2-dto-validators"] =
  'function isTaskDTO(v) {\n  if (!v || typeof v !== "object" || Array.isArray(v)) return false;\n  if (typeof v.id !== "string") return false;\n  if (typeof v.title !== "string" || v.title.trim().length === 0) return false;\n  if (typeof v.done !== "boolean") return false;\n  if (v.due !== undefined && typeof v.due !== "string") return false;\n  return true;\n}\nfunction isTaskListDTO(v) {\n  return Array.isArray(v) && v.every(isTaskDTO);\n}';
W["i2-dto-validators"] =
  "function isTaskDTO(v) { return !!v; }\nfunction isTaskListDTO(v) { return Array.isArray(v); }";
R["i2-api-result"] =
  "async function toApiResult(promise) {\n  try {\n    const data = await promise;\n    return { ok: true, data };\n  } catch (err) {\n    return { ok: false, status: 0, message: err.message };\n  }\n}\nfunction unwrap(result) {\n  if (result.ok) return result.data;\n  throw new Error(result.message);\n}";
W["i2-api-result"] =
  "async function toApiResult(promise) {\n  const data = await promise;\n  return { ok: true, data };\n}\nfunction unwrap(result) {\n  return result.data;\n}";
R["i2-typed-client"] =
  'function createTypedClient(fetchImpl) {\n  async function getJSON(url) {\n    const res = await fetchImpl(url);\n    return { res, body: await res.json() };\n  }\n  return {\n    async getTask(id) {\n      const { res, body } = await getJSON("/tasks/" + id);\n      if (!res.ok) return { ok: false, reason: "not-found" };\n      if (!isTaskDTO(body)) return { ok: false, reason: "invalid" };\n      return { ok: true, task: body };\n    },\n    async listTasks() {\n      const { res, body } = await getJSON("/tasks");\n      if (!res.ok || !isTaskListDTO(body)) return { ok: false, reason: "invalid" };\n      return { ok: true, tasks: body };\n    },\n  };\n}\nfunction isTaskDTO(v) {\n  if (!v || typeof v !== "object" || Array.isArray(v)) return false;\n  return typeof v.id === "string" && typeof v.title === "string" && v.title.length > 0 && typeof v.done === "boolean";\n}\nfunction isTaskListDTO(v) {\n  return Array.isArray(v) && v.every(isTaskDTO);\n}';
W["i2-typed-client"] =
  'function createTypedClient(fetchImpl) {\n  return {\n    async getTask(id) {\n      const res = await fetchImpl("/tasks/" + id);\n      return { ok: true, task: await res.json() };\n    },\n    async listTasks() {\n      const res = await fetchImpl("/tasks");\n      return { ok: true, tasks: await res.json() };\n    },\n  };\n}';
R["i2-shape-guard"] =
  'function hasShape(obj, spec) {\n  if (typeof obj !== "object" || obj === null) return false;\n  return Object.entries(spec).every(([k, t]) => typeof obj[k] === t);\n}';
W["i2-shape-guard"] = "function hasShape(obj, spec) { return true; }";
R["i2-normalize"] =
  'function normalizeUsers(raw) {\n  const out = [];\n  for (const r of raw) {\n    if (r && typeof r === "object" && typeof r.name === "string") {\n      const age = Number(r.age);\n      if (Number.isFinite(age)) {\n        out.push({ name: r.name.trim(), age });\n      }\n    }\n  }\n  return out;\n}';
W["i2-normalize"] =
  "function normalizeUsers(raw) {\n  return raw.map((r) => ({ name: r.name, age: Number(r.age) }));\n}";
R["i2-omit-pick"] =
  "function pick(obj, keys) {\n  const out = {};\n  for (const k of keys) {\n    if (k in obj) out[k] = obj[k];\n  }\n  return out;\n}\nfunction omit(obj, keys) {\n  const out = { ...obj };\n  for (const k of keys) {\n    delete out[k];\n  }\n  return out;\n}";
W["i2-omit-pick"] =
  "function pick(obj, keys) {\n  for (const k of keys) delete obj[k];\n  return obj;\n}\nfunction omit(obj, keys) {\n  for (const k of keys) delete obj[k];\n  return obj;\n}";
R["i2-narrow-format"] =
  'function format(value) {\n  if (value === null || value === undefined) return "\u2014";\n  if (typeof value === "string") return value.trim();\n  if (typeof value === "number") return value.toFixed(2);\n  if (typeof value === "boolean") return value ? "yes" : "no";\n  throw new Error("unreachable");\n}';
W["i2-narrow-format"] =
  'function format(value) {\n  if (!value) return "\u2014";\n  return String(value);\n}';
R["i2-union-reducer"] =
  'function reduceRequest(state, action) {\n  switch (action.type) {\n    case "start": return { kind: "loading" };\n    case "resolve": return { kind: "success", data: action.data };\n    case "reject": return { kind: "error", message: action.message };\n    case "reset": return { kind: "idle" };\n    default: return state;\n  }\n}';
W["i2-union-reducer"] =
  "function reduceRequest(state, action) {\n  state.kind = action.type;\n  return state;\n}";
R["i2-exhaustive"] =
  'function describeShape(v) {\n  if (v === null) return "nothing";\n  if (typeof v === "string") return "text";\n  if (typeof v === "number") return "number";\n  if (typeof v === "boolean") return "flag";\n  if (Array.isArray(v)) return "list of " + v.length;\n  throw new Error("Unhandled shape");\n}';
W["i2-exhaustive"] = "function describeShape(v) {\n  return String(v);\n}";
R["i2-first-or"] =
  "function firstOr(items, fallback) {\n  return items.length > 0 ? items[0] : fallback;\n}";
W["i2-first-or"] =
  "function firstOr(items, fallback) {\n  return items[items.length] ?? fallback;\n}";
R["i2-group-by"] =
  "function groupBy(items, keyFn) {\n  const out = {};\n  for (const item of items) {\n    const k = keyFn(item);\n    (out[k] ??= []).push(item);\n  }\n  return out;\n}\nfunction keyCount(groups) {\n  return Object.keys(groups).length;\n}";
W["i2-group-by"] =
  "function groupBy(items, keyFn) {\n  return {};\n}\nfunction keyCount(groups) {\n  return 0;\n}";
R["i2-result-wrap"] =
  "function attempt(fn) {\n  try {\n    return { ok: true, value: fn() };\n  } catch (err) {\n    return { ok: false, error: err.message };\n  }\n}";
W["i2-result-wrap"] = "function attempt(fn) {\n  return { ok: true, value: fn() };\n}";
R["i2-unknown-handler"] =
  'function handleUnknown(payload) {\n  if (Array.isArray(payload) && payload.every((x) => typeof x === "string")) {\n    return { kind: "tags", tags: payload.map((s) => s.trim()) };\n  }\n  if (typeof payload === "number" && Number.isFinite(payload)) {\n    return { kind: "count", count: payload };\n  }\n  if (payload && typeof payload === "object" && typeof payload.id === "string") {\n    return { kind: "entity", id: payload.id };\n  }\n  return { kind: "reject" };\n}';
W["i2-unknown-handler"] =
  'function handleUnknown(payload) {\n  return { kind: "tags", tags: payload };\n}';
R["i2-storage-guard"] =
  "function loadSetting(storage, key, isShape, fallback) {\n  let parsed;\n  try {\n    const raw = storage.getItem(key);\n    if (raw === null) return { ok: false, fallback };\n    parsed = JSON.parse(raw);\n  } catch {\n    return { ok: false, fallback };\n  }\n  if (!isShape(parsed)) return { ok: false, fallback };\n  return { ok: true, value: parsed };\n}\nfunction saveSetting(storage, key, value) {\n  storage.setItem(key, JSON.stringify(value));\n}";
W["i2-storage-guard"] =
  "function loadSetting(storage, key, isShape, fallback) {\n  return { ok: true, value: JSON.parse(storage.getItem(key)) };\n}\nfunction saveSetting(storage, key, value) {\n  storage.setItem(key, value);\n}";
R["i2-safe-json"] =
  "function parseOr(raw, fallback) {\n  try {\n    return JSON.parse(raw);\n  } catch {\n    return fallback;\n  }\n}\nfunction serialize(value, fallback) {\n  try {\n    return JSON.stringify(value);\n  } catch {\n    return fallback;\n  }\n}";
W["i2-safe-json"] =
  "function parseOr(raw, fallback) {\n  return JSON.parse(raw);\n}\nfunction serialize(value, fallback) {\n  return JSON.stringify(value);\n}";
R["i2-dto-validators"] =
  'function isTaskDTO(v) {\n  if (!v || typeof v !== "object" || Array.isArray(v)) return false;\n  if (typeof v.id !== "string") return false;\n  if (typeof v.title !== "string" || v.title.trim().length === 0) return false;\n  if (typeof v.done !== "boolean") return false;\n  if (v.due !== undefined && typeof v.due !== "string") return false;\n  return true;\n}\nfunction isTaskListDTO(v) {\n  return Array.isArray(v) && v.every(isTaskDTO);\n}';
W["i2-dto-validators"] =
  "function isTaskDTO(v) { return !!v; }\nfunction isTaskListDTO(v) { return Array.isArray(v); }";
R["i2-api-result"] =
  "async function toApiResult(promise) {\n  try {\n    const data = await promise;\n    return { ok: true, data };\n  } catch (err) {\n    return { ok: false, status: 0, message: err.message };\n  }\n}\nfunction unwrap(result) {\n  if (result.ok) return result.data;\n  throw new Error(result.message);\n}";
W["i2-api-result"] =
  "async function toApiResult(promise) {\n  const data = await promise;\n  return { ok: true, data };\n}\nfunction unwrap(result) {\n  return result.data;\n}";
R["i2-typed-client"] =
  'function createTypedClient(fetchImpl) {\n  async function getJSON(url) {\n    const res = await fetchImpl(url);\n    return { res, body: await res.json() };\n  }\n  return {\n    async getTask(id) {\n      const { res, body } = await getJSON("/tasks/" + id);\n      if (!res.ok) return { ok: false, reason: "not-found" };\n      if (!isTaskDTO(body)) return { ok: false, reason: "invalid" };\n      return { ok: true, task: body };\n    },\n    async listTasks() {\n      const { res, body } = await getJSON("/tasks");\n      if (!res.ok || !isTaskListDTO(body)) return { ok: false, reason: "invalid" };\n      return { ok: true, tasks: body };\n    },\n  };\n}\nfunction isTaskDTO(v) {\n  if (!v || typeof v !== "object" || Array.isArray(v)) return false;\n  return typeof v.id === "string" && typeof v.title === "string" && v.title.length > 0 && typeof v.done === "boolean";\n}\nfunction isTaskListDTO(v) {\n  return Array.isArray(v) && v.every(isTaskDTO);\n}';
W["i2-typed-client"] =
  'function createTypedClient(fetchImpl) {\n  return {\n    async getTask(id) {\n      const res = await fetchImpl("/tasks/" + id);\n      return { ok: true, task: await res.json() };\n    },\n    async listTasks() {\n      const res = await fetchImpl("/tasks");\n      return { ok: true, tasks: await res.json() };\n    },\n  };\n}';

// ── Module 5 checkpoint ──
R["i2-ts-checkpoint"] = `function isUser(v) {
  if (typeof v !== "object" || v === null || Array.isArray(v)) return false;
  if (typeof v.id !== "string") return false;
  if (typeof v.email !== "string" || !v.email.includes("@")) return false;
  if (v.name !== undefined && typeof v.name !== "string") return false;
  return true;
}
function parseWith(v, validator, fallback) {
  return validator(v) ? { ok: true, value: v } : { ok: false, fallback };
}
function handleApi(result) {
  return result.ok ? result.data : "HTTP " + result.status;
}`;
R["i2-shape-guard"] =
  'function hasShape(obj, spec) {\n  if (typeof obj !== "object" || obj === null) return false;\n  return Object.entries(spec).every(([k, t]) => typeof obj[k] === t);\n}';
W["i2-shape-guard"] = "function hasShape(obj, spec) { return true; }";
R["i2-normalize"] =
  'function normalizeUsers(raw) {\n  const out = [];\n  for (const r of raw) {\n    if (r && typeof r === "object" && typeof r.name === "string") {\n      const age = Number(r.age);\n      if (Number.isFinite(age)) {\n        out.push({ name: r.name.trim(), age });\n      }\n    }\n  }\n  return out;\n}';
W["i2-normalize"] =
  "function normalizeUsers(raw) {\n  return raw.map((r) => ({ name: r.name, age: Number(r.age) }));\n}";
R["i2-omit-pick"] =
  "function pick(obj, keys) {\n  const out = {};\n  for (const k of keys) {\n    if (k in obj) out[k] = obj[k];\n  }\n  return out;\n}\nfunction omit(obj, keys) {\n  const out = { ...obj };\n  for (const k of keys) {\n    delete out[k];\n  }\n  return out;\n}";
W["i2-omit-pick"] =
  "function pick(obj, keys) {\n  for (const k of keys) delete obj[k];\n  return obj;\n}\nfunction omit(obj, keys) {\n  for (const k of keys) delete obj[k];\n  return obj;\n}";
R["i2-narrow-format"] =
  'function format(value) {\n  if (value === null || value === undefined) return "\u2014";\n  if (typeof value === "string") return value.trim();\n  if (typeof value === "number") return value.toFixed(2);\n  if (typeof value === "boolean") return value ? "yes" : "no";\n  throw new Error("unreachable");\n}';
W["i2-narrow-format"] =
  'function format(value) {\n  if (!value) return "\u2014";\n  return String(value);\n}';
R["i2-union-reducer"] =
  'function reduceRequest(state, action) {\n  switch (action.type) {\n    case "start": return { kind: "loading" };\n    case "resolve": return { kind: "success", data: action.data };\n    case "reject": return { kind: "error", message: action.message };\n    case "reset": return { kind: "idle" };\n    default: return state;\n  }\n}';
W["i2-union-reducer"] =
  "function reduceRequest(state, action) {\n  state.kind = action.type;\n  return state;\n}";
R["i2-exhaustive"] =
  'function describeShape(v) {\n  if (v === null) return "nothing";\n  if (typeof v === "string") return "text";\n  if (typeof v === "number") return "number";\n  if (typeof v === "boolean") return "flag";\n  if (Array.isArray(v)) return "list of " + v.length;\n  throw new Error("Unhandled shape");\n}';
W["i2-exhaustive"] = "function describeShape(v) {\n  return String(v);\n}";
R["i2-first-or"] =
  "function firstOr(items, fallback) {\n  return items.length > 0 ? items[0] : fallback;\n}";
W["i2-first-or"] =
  "function firstOr(items, fallback) {\n  return items[items.length] ?? fallback;\n}";
R["i2-group-by"] =
  "function groupBy(items, keyFn) {\n  const out = {};\n  for (const item of items) {\n    const k = keyFn(item);\n    (out[k] ??= []).push(item);\n  }\n  return out;\n}\nfunction keyCount(groups) {\n  return Object.keys(groups).length;\n}";
W["i2-group-by"] =
  "function groupBy(items, keyFn) {\n  return {};\n}\nfunction keyCount(groups) {\n  return 0;\n}";
R["i2-result-wrap"] =
  "function attempt(fn) {\n  try {\n    return { ok: true, value: fn() };\n  } catch (err) {\n    return { ok: false, error: err.message };\n  }\n}";
W["i2-result-wrap"] = "function attempt(fn) {\n  return { ok: true, value: fn() };\n}";
R["i2-unknown-handler"] =
  'function handleUnknown(payload) {\n  if (Array.isArray(payload) && payload.every((x) => typeof x === "string")) {\n    return { kind: "tags", tags: payload.map((s) => s.trim()) };\n  }\n  if (typeof payload === "number" && Number.isFinite(payload)) {\n    return { kind: "count", count: payload };\n  }\n  if (payload && typeof payload === "object" && typeof payload.id === "string") {\n    return { kind: "entity", id: payload.id };\n  }\n  return { kind: "reject" };\n}';
W["i2-unknown-handler"] =
  'function handleUnknown(payload) {\n  return { kind: "tags", tags: payload };\n}';
R["i2-storage-guard"] =
  "function loadSetting(storage, key, isShape, fallback) {\n  let parsed;\n  try {\n    const raw = storage.getItem(key);\n    if (raw === null) return { ok: false, fallback };\n    parsed = JSON.parse(raw);\n  } catch {\n    return { ok: false, fallback };\n  }\n  if (!isShape(parsed)) return { ok: false, fallback };\n  return { ok: true, value: parsed };\n}\nfunction saveSetting(storage, key, value) {\n  storage.setItem(key, JSON.stringify(value));\n}";
W["i2-storage-guard"] =
  "function loadSetting(storage, key, isShape, fallback) {\n  return { ok: true, value: JSON.parse(storage.getItem(key)) };\n}\nfunction saveSetting(storage, key, value) {\n  storage.setItem(key, value);\n}";
R["i2-safe-json"] =
  "function parseOr(raw, fallback) {\n  try {\n    return JSON.parse(raw);\n  } catch {\n    return fallback;\n  }\n}\nfunction serialize(value, fallback) {\n  try {\n    return JSON.stringify(value);\n  } catch {\n    return fallback;\n  }\n}";
W["i2-safe-json"] =
  "function parseOr(raw, fallback) {\n  return JSON.parse(raw);\n}\nfunction serialize(value, fallback) {\n  return JSON.stringify(value);\n}";
R["i2-dto-validators"] =
  'function isTaskDTO(v) {\n  if (!v || typeof v !== "object" || Array.isArray(v)) return false;\n  if (typeof v.id !== "string") return false;\n  if (typeof v.title !== "string" || v.title.trim().length === 0) return false;\n  if (typeof v.done !== "boolean") return false;\n  if (v.due !== undefined && typeof v.due !== "string") return false;\n  return true;\n}\nfunction isTaskListDTO(v) {\n  return Array.isArray(v) && v.every(isTaskDTO);\n}';
W["i2-dto-validators"] =
  "function isTaskDTO(v) { return !!v; }\nfunction isTaskListDTO(v) { return Array.isArray(v); }";
R["i2-api-result"] =
  "async function toApiResult(promise) {\n  try {\n    const data = await promise;\n    return { ok: true, data };\n  } catch (err) {\n    return { ok: false, status: 0, message: err.message };\n  }\n}\nfunction unwrap(result) {\n  if (result.ok) return result.data;\n  throw new Error(result.message);\n}";
W["i2-api-result"] =
  "async function toApiResult(promise) {\n  const data = await promise;\n  return { ok: true, data };\n}\nfunction unwrap(result) {\n  return result.data;\n}";
R["i2-typed-client"] =
  'function createTypedClient(fetchImpl) {\n  async function getJSON(url) {\n    const res = await fetchImpl(url);\n    return { res, body: await res.json() };\n  }\n  return {\n    async getTask(id) {\n      const { res, body } = await getJSON("/tasks/" + id);\n      if (!res.ok) return { ok: false, reason: "not-found" };\n      if (!isTaskDTO(body)) return { ok: false, reason: "invalid" };\n      return { ok: true, task: body };\n    },\n    async listTasks() {\n      const { res, body } = await getJSON("/tasks");\n      if (!res.ok || !isTaskListDTO(body)) return { ok: false, reason: "invalid" };\n      return { ok: true, tasks: body };\n    },\n  };\n}\nfunction isTaskDTO(v) {\n  if (!v || typeof v !== "object" || Array.isArray(v)) return false;\n  return typeof v.id === "string" && typeof v.title === "string" && v.title.length > 0 && typeof v.done === "boolean";\n}\nfunction isTaskListDTO(v) {\n  return Array.isArray(v) && v.every(isTaskDTO);\n}';
W["i2-typed-client"] =
  'function createTypedClient(fetchImpl) {\n  return {\n    async getTask(id) {\n      const res = await fetchImpl("/tasks/" + id);\n      return { ok: true, task: await res.json() };\n    },\n    async listTasks() {\n      const res = await fetchImpl("/tasks");\n      return { ok: true, tasks: await res.json() };\n    },\n  };\n}';
R["i2-commit-reach"] =
  "function reachable(commits, target) {\n  const chain = [];\n  let cur = target;\n  while (cur && commits[cur] !== undefined) {\n    chain.push(cur);\n    cur = commits[cur];\n  }\n  return chain.reverse();\n}";
W["i2-commit-reach"] = "function reachable(commits, target) {\n  return Object.keys(commits);\n}";
R["i2-diverged"] =
  "function diverged(commits, a, b) {\n  const anc = (t) => {\n    const s = new Set();\n    let cur = t;\n    while (cur && commits[cur] !== undefined) { s.add(cur); cur = commits[cur]; }\n    return s;\n  };\n  const sa = anc(a), sb = anc(b);\n  return !sa.has(b) && !sb.has(a);\n}";
W["i2-diverged"] = "function diverged(commits, a, b) {\n  return a !== b;\n}";
R["i2-bisect"] =
  "function bisect(commits, isBad) {\n  let lo = 0, hi = commits.length - 1;\n  while (lo < hi) {\n    const mid = Math.floor((lo + hi) / 2);\n    if (isBad(commits[mid])) hi = mid; else lo = mid + 1;\n  }\n  return commits[lo];\n}";
W["i2-bisect"] = "function bisect(commits, isBad) {\n  return commits.find(isBad);\n}";
R["i2-branch-classify"] =
  'function classifyBranch(name) {\n  const types = ["feat", "fix", "chore", "docs", "refactor", "test"];\n  const i = name.indexOf("/");\n  if (i === -1) return null;\n  const type = name.slice(0, i), desc = name.slice(i + 1);\n  if (!types.includes(type)) return null;\n  if (!desc || !/^[a-z0-9-]+$/.test(desc)) return null;\n  return type === "feat" || type === "fix" ? "feature" : "maintenance";\n}';
W["i2-branch-classify"] =
  'function classifyBranch(name) {\n  return name.includes("/") ? "feature" : null;\n}';
R["i2-flow-validate"] =
  'function validateFlow(events) {\n  let branched = false, commits = 0, pushed = false, prs = 0, merged = false;\n  for (const e of events) {\n    if (merged) return false;\n    if (e === "branch") { if (branched) return false; branched = true; }\n    else if (e === "commit") { if (!branched) return false; commits++; }\n    else if (e === "push") { if (commits === 0) return false; pushed = true; }\n    else if (e === "pr") { if (!pushed) return false; prs++; if (prs > 1) return false; }\n    else if (e === "merge") { if (prs !== 1) return false; merged = true; }\n    else return false;\n  }\n  return branched && commits > 0 && pushed && prs === 1;\n}';
W["i2-flow-validate"] =
  'function validateFlow(events) {\n  return events[0] === "branch" && events.includes("pr");\n}';
R["i2-stale-branches"] =
  "function staleReport(branches) {\n  return branches\n    .filter((b) => b.ageDays > 14 && b.ahead > 5)\n    .map((b) => b.name)\n    .sort();\n}";
W["i2-stale-branches"] =
  "function staleReport(branches) {\n  return branches.filter((b) => b.ageDays > 14).map((b) => b.name);\n}";
R["i2-conflict-parse"] =
  'function parseConflict(text) {\n  const lines = text.split("\\n");\n  let side = null, mine = [], theirs = [];\n  for (const l of lines) {\n    if (l.startsWith("<<<<<<<")) { side = "mine"; continue; }\n    if (l === "=======") { side = "theirs"; continue; }\n    if (l.startsWith(">>>>>>>")) { side = null; continue; }\n    if (side === "mine") mine.push(l);\n    else if (side === "theirs") theirs.push(l);\n  }\n  return { mine: mine.join("\\n"), theirs: theirs.join("\\n") };\n}';
W["i2-conflict-parse"] =
  "function parseConflict(text) {\n  return { mine: text, theirs: text };\n}";
R["i2-conflict-resolve"] =
  'function resolveConflictFile(text, chosen) {\n  const lines = text.split("\\n");\n  let side = null;\n  const out = [];\n  for (const l of lines) {\n    if (l.startsWith("<<<<<<<")) { side = "mine"; continue; }\n    if (l === "=======") { side = "theirs"; continue; }\n    if (l.startsWith(">>>>>>>")) { side = null; continue; }\n    if (side === null) out.push(l);\n    else if (side === chosen) out.push(l);\n  }\n  return out.join("\\n");\n}';
W["i2-conflict-resolve"] =
  'function resolveConflictFile(text, chosen) {\n  return text.replace(/<<<<<<<[\\s\\S]*?>>>>>>>[^\\n]*\\n?/, "");\n}';
R["i2-conflict-verify"] =
  'function hasUnresolved(text) {\n  return text.split("\\n").some((l) =>\n    l.startsWith("<<<<<<< ") || l === "=======" || l.startsWith(">>>>>>> ")\n  );\n}';
W["i2-conflict-verify"] = 'function hasUnresolved(text) {\n  return text.includes("======");\n}';
R["i2-recovery-choice"] =
  'function advise(o) {\n  if (o.pushed && o.othersHaveIt) return "revert";\n  if (!o.pushed && o.hasUncommittedWork) return "stash-then-reset";\n  if (!o.pushed) return "reset-soft";\n  if (o.hasUncommittedWork) return "stash-then-reset";\n  return "recreate";\n}';
W["i2-recovery-choice"] = 'function advise(o) {\n  return o.pushed ? "revert" : "reset-soft";\n}';
R["i2-reset-modes"] =
  'function applyReset(state, mode, n) {\n  const base = { commit: state.commit - n, staged: [...state.staged], worktree: [...state.worktree] };\n  if (mode === "mixed") base.staged = [];\n  if (mode === "hard") { base.staged = []; base.worktree = []; }\n  return base;\n}';
W["i2-reset-modes"] =
  "function applyReset(state, mode, n) {\n  return { commit: state.commit - n, staged: [], worktree: [] };\n}";
R["i2-reflog-walk"] =
  'function lastGood(reflog) {\n  const c = reflog.find((e) => e.action === "commit");\n  return c ? c.head : null;\n}';
W["i2-reflog-walk"] =
  "function lastGood(reflog) {\n  return reflog[reflog.length - 1]?.head ?? null;\n}";
R["i2-commit-parse"] =
  'function parseCommit(msg) {\n  const types = ["feat", "fix", "refactor", "perf", "test", "docs", "chore", "ci"];\n  const header = msg.split("\\n")[0];\n  const m = header.match(/^(\\w+)(\\(([^)]*)\\))?(!)?:\\s(.+)$/);\n  if (!m || !types.includes(m[1]) || !m[5]) return null;\n  return {\n    type: m[1],\n    scope: m[3] || null,\n    breaking: m[4] === "!" || msg.includes("BREAKING CHANGE"),\n    desc: m[5],\n  };\n}';
W["i2-commit-parse"] =
  'function parseCommit(msg) {\n  return { type: "feat", scope: null, breaking: false, desc: msg };\n}';
W["i2-commit-parse"] =
  'function parseCommit(msg) {\n  return { type: "feat", scope: null, breaking: false, desc: msg };\n}';
R["i2-semver-impact"] =
  'function releaseBump(commits) {\n  if (commits.some((c) => c.breaking)) return "major";\n  if (commits.some((c) => c.type === "feat")) return "minor";\n  if (commits.some((c) => c.type === "fix")) return "patch";\n  return null;\n}';
W["i2-semver-impact"] =
  'function releaseBump(commits) {\n  return commits.length ? "minor" : null;\n}';
R["i2-pr-size"] =
  'function prVerdict(files) {\n  const lines = files.reduce((n, f) => n + f.additions + f.deletions, 0);\n  if (lines > 400) return "split";\n  if (files.length > 10) return "too-many-files";\n  return "ok";\n}';
W["i2-pr-size"] =
  'function prVerdict(files) {\n  return files.length > 10 ? "too-many-files" : "ok";\n}';
R["i2-secret-detect"] =
  'function findSecrets(line) {\n  const pats = [\n    /AKIA[A-Z0-9]{16}/g,\n    /ghp_[\\w]{36,}/g,\n    /sk-[\\w-]{20,}/g,\n    /(?:key|token|secret|password)\\s*=\\s*"([^"]{8,})"/gi,\n  ];\n  const out = [];\n  for (const re of pats) {\n    let m;\n    while ((m = re.exec(line)) !== null) out.push(m[0]);\n  }\n  return out;\n}';
W["i2-secret-detect"] =
  'function findSecrets(line) {\n  return line.includes("key") ? [line] : [];\n}';
R["i2-diff-scan"] =
  'function scanDiff(diff) {\n  const out = [];\n  for (const line of diff) {\n    if (line.startsWith("+") && !line.startsWith("+++")) {\n      const secrets = findSecrets(line.slice(1));\n      if (secrets.length) out.push({ line, secrets });\n    }\n  }\n  return out;\n}\n\nfunction findSecrets(line) {\n  const pats = [\n    /AKIA[A-Z0-9]{16}/g,\n    /ghp_[\\w]{36,}/g,\n    /sk-[\\w-]{20,}/g,\n    /(?:key|token|secret|password)\\s*=\\s*"([^"]{8,})"/gi,\n  ];\n  const out = [];\n  for (const re of pats) {\n    let m;\n    while ((m = re.exec(line)) !== null) out.push(m[0]);\n  }\n  return out;\n}';
W["i2-diff-scan"] =
  'function scanDiff(diff) {\n  return diff.filter((l) => l.startsWith("+")).map((line) => ({ line, secrets: [line] }));\n}';
R["i2-gitignore-check"] =
  'function ignoreCovers(lines, filePath) {\n  for (const raw of lines) {\n    const p = raw.trim();\n    if (!p || p.startsWith("#")) continue;\n    if (p.endsWith("/")) {\n      if (filePath.includes("/" + p) || filePath.startsWith(p)) return true;\n    } else if (p.startsWith("*")) {\n      if (filePath.endsWith(p.slice(1))) return true;\n    } else if (p.includes("*")) {\n      if (filePath.startsWith(p.replace("*", ""))) return true;\n    } else if (p === filePath) return true;\n  }\n  return false;\n}';
W["i2-gitignore-check"] =
  "function ignoreCovers(lines, filePath) {\n  return lines.some((p) => filePath.includes(p));\n}";

R["i2-workflow-checkpoint"] =
  'function resolveConflict(mine, theirs, strategy) {\n  if (strategy === "mine") return mine;\n  if (strategy === "theirs") return theirs;\n  return mine + "\\n" + theirs;\n}\nfunction chooseRecovery(pushed, othersPulled, wantHistory) {\n  if (pushed && othersPulled) return "revert";\n  if (!pushed) return "reset";\n  return wantHistory ? "merge" : "reset";\n}\nfunction bumpVersion(version, type) {\n  const parts = version.split(".").map(Number);\n  if (type === "fix") return parts[0] + "." + parts[1] + "." + (parts[2] + 1);\n  if (type === "feat") return parts[0] + "." + (parts[1] + 1) + ".0";\n  return (parts[0] + 1) + ".0.0";\n}';
W["i2-workflow-checkpoint"] =
  'function resolveConflict(mine, theirs, strategy) { return mine; }\nfunction chooseRecovery(pushed, othersPulled, wantHistory) { return "reset"; }\nfunction bumpVersion(version, type) {\n  const parts = version.split(".").map(Number);\n  return parts[0] + "." + parts[1] + "." + (parts[2] + 1);\n}';
R["i2-deep-equal"] =
  'function deepEqual(a, b) {\n  if (Object.is(a, b)) return true;\n  if (typeof a !== "object" || typeof b !== "object" || a === null || b === null) return false;\n  if (Array.isArray(a) !== Array.isArray(b)) return false;\n  const ka = Object.keys(a), kb = Object.keys(b);\n  if (ka.length !== kb.length) return false;\n  return ka.every((k) => k in b && deepEqual(a[k], b[k]));\n}';
W["i2-deep-equal"] =
  "function deepEqual(a, b) {\n  return JSON.stringify(a) === JSON.stringify(b);\n}";
R["i2-assert-throws"] =
  'function assertThrows(fn, errClass, msgPart) {\n  try {\n    fn();\n    return "no-throw";\n  } catch (e) {\n    if (errClass && !(e instanceof errClass)) return "wrong-type";\n    if (msgPart && !(e.message || "").includes(msgPart)) return "wrong-message";\n    return "ok";\n  }\n}';
W["i2-assert-throws"] =
  'function assertThrows(fn) {\n  try { fn(); return "no-throw"; } catch { return "ok"; }\n}';
R["i2-diff-msg"] =
  'function fmt(v) {\n  if (typeof v === "string") return \'"\' + v + \'"\';\n  if (v === null) return "null";\n  if (v === undefined) return "undefined";\n  if (typeof v === "function") return "function";\n  if (Array.isArray(v)) return "[" + v.map(fmt).join(", ") + "]";\n  if (typeof v === "object") return "{" + Object.entries(v).map(([k, x]) => k + ": " + fmt(x)).join(", ") + "}";\n  return String(v);\n}';
W["i2-diff-msg"] = "function fmt(v) {\n  return String(v);\n}";
R["i2-case-enumerate"] =
  'function edgeCases(value) {\n  const out = [];\n  const empty = Array.isArray(value) ? value.length === 0\n    : typeof value === "string" ? value === ""\n    : typeof value === "object" && value !== null ? Object.keys(value).length === 0 : false;\n  if (empty) out.push("empty");\n  if (value === 0 || Object.is(value, -0) || value === Number.MAX_SAFE_INTEGER) out.push("boundary");\n  if (value === null || value === undefined || Number.isNaN(value)) out.push("wrong-type");\n  if (typeof value === "string" && value !== "") out.push("wrong-type");\n  if (Array.isArray(value) && new Set(value).size !== value.length) out.push("duplicate");\n  return out;\n}';
W["i2-case-enumerate"] =
  'function edgeCases(value) {\n  return ["empty", "boundary", "wrong-type", "duplicate"];\n}';
R["i2-test-naming"] =
  'function testName(fn, behavior) {\n  if (!behavior) throw new Error("behavior required");\n  return fn + " " + behavior[0].toUpperCase() + behavior.slice(1);\n}';
W["i2-test-naming"] = 'function testName(fn, behavior) {\n  return fn + " " + behavior;\n}';
R["i2-pyramid-pick"] =
  'function testLevel(spec) {\n  const s = spec.toLowerCase();\n  if (s.includes("user") || s.includes("click") || s.includes("browser")) return "e2e";\n  if (s.includes("with real") || s.includes("together")) return "integration";\n  return "unit";\n}';
W["i2-pyramid-pick"] = 'function testLevel(spec) {\n  return "unit";\n}';
R["i2-make-spy"] =
  "function makeSpy(impl) {\n  const calls = [];\n  const results = [];\n  const spy = (...args) => {\n    calls.push(args);\n    const r = impl ? impl(...args) : undefined;\n    results.push(r);\n    return r;\n  };\n  spy.calls = calls;\n  spy.results = results;\n  spy.reset = () => { calls.length = 0; results.length = 0; };\n  return spy;\n}";
W["i2-make-spy"] =
  "function makeSpy(impl) {\n  const spy = (...args) => impl && impl(...args);\n  spy.calls = [];\n  return spy;\n}";
R["i2-stub-fetch"] =
  "function makeFetchStub(routes) {\n  const requests = [];\n  const stub = async (url) => {\n    requests.push(url);\n    if (url in routes) {\n      return { ok: true, status: 200, json: async () => routes[url] };\n    }\n    return { ok: false, status: 404, json: async () => null };\n  };\n  stub.requests = requests;\n  return stub;\n}";
W["i2-stub-fetch"] =
  "function makeFetchStub(routes) {\n  return async () => ({ ok: true, status: 200, json: async () => ({}) });\n}";
R["i2-inject-seam"] =
  'function makeGreeter(clock) {\n  return (name) => {\n    const h = clock();\n    if (h < 12) return "Good morning, " + name;\n    if (h < 18) return "Good afternoon, " + name;\n    return "Good evening, " + name;\n  };\n}';
W["i2-inject-seam"] = 'function makeGreeter(clock) {\n  return (name) => "Hello, " + name;\n}';
R["i2-pipeline-bisect"] =
  "function firstBadStage(stages, inspect) {\n  let lo = 0, hi = stages.length - 1;\n  if (!inspect(stages[hi])) return null;\n  while (lo < hi) {\n    const mid = Math.floor((lo + hi) / 2);\n    if (inspect(stages[mid])) hi = mid; else lo = mid + 1;\n  }\n  return stages[lo];\n}";
W["i2-pipeline-bisect"] =
  "function firstBadStage(stages, inspect) {\n  return stages.find(inspect) ?? null;\n}";
R["i2-stack-read"] =
  'function firstOwnFrame(frames) {\n  return frames.find((f) => f.file.startsWith("app/")) ?? null;\n}\nfunction errorKind(message) {\n  if (message.includes("is not a function")) return "type";\n  if (message.includes("Cannot read prop")) return "shape";\n  return "other";\n}';
W["i2-stack-read"] =
  'function firstOwnFrame(frames) {\n  return frames[0] ?? null;\n}\nfunction errorKind(message) {\n  return "other";\n}';
R["i2-repro-minimize"] =
  "function minimalInput(inputs, isBroken) {\n  return inputs.find(isBroken) ?? null;\n}";
W["i2-repro-minimize"] = "function minimalInput(inputs, isBroken) {\n  return null;\n}";
R["i2-mini-runner"] =
  "function runSuite(tests) {\n  let passed = 0, failed = 0;\n  const failures = [];\n  for (const t of tests) {\n    try {\n      t.fn();\n      passed++;\n    } catch {\n      failed++;\n      failures.push(t.name);\n    }\n  }\n  return { passed, failed, failures };\n}";
W["i2-mini-runner"] =
  "function runSuite(tests) {\n  return { passed: tests.length, failed: 0, failures: [] };\n}";
R["i2-flaky-quarantine"] =
  "function quarantine(history) {\n  const stats = new Map();\n  for (const r of history) {\n    const s = stats.get(r.name) ?? { p: 0, f: 0 };\n    if (r.passed) s.p++; else s.f++;\n    stats.set(r.name, s);\n  }\n  const out = [];\n  for (const [name, s] of stats) if (s.p > 0 && s.f > 0) out.push(name);\n  return out.sort();\n}";
W["i2-flaky-quarantine"] =
  "function quarantine(history) {\n  return [...new Set(history.filter((r) => !r.passed).map((r) => r.name))].sort();\n}";
R["i2-regression-first"] =
  "function addRegression(ledger, bugId, fixCommit, coversAll) {\n  if (!coversAll || ledger.some((e) => e.bugId === bugId)) return ledger;\n  return [...ledger, { bugId, fixCommit }];\n}";
W["i2-regression-first"] =
  "function addRegression(ledger, bugId, fixCommit, coversAll) {\n  ledger.push({ bugId, fixCommit });\n  return ledger;\n}";

R["i2-repair-checkpoint"] =
  'function diagnose(testName) {\n  const t = testName.toLowerCase();\n  if (t.includes("empty")) return "edge-case";\n  if (t.includes("slow")) return "performance";\n  if (t.includes("null") || t.includes("undefined")) return "type-error";\n  return "logic";\n}\nfunction analyzeSpy(spy, expectedCount, expectedFirstArg) {\n  if (spy.calls.length !== expectedCount) return false;\n  if (spy.calls.length === 0) return expectedFirstArg === undefined;\n  return spy.calls[0][0] === expectedFirstArg;\n}\nfunction fixAndProve(isFixed, testPasses) {\n  if (isFixed && testPasses) return "fixed";\n  if (isFixed) return "untested";\n  return "broken";\n}';
W["i2-repair-checkpoint"] =
  'function diagnose(testName) { return "logic"; }\nfunction analyzeSpy(spy, expectedCount, expectedFirstArg) { return true; }\nfunction fixAndProve(isFixed, testPasses) { return "fixed"; }';
R["i2-deep-equal"] =
  'function deepEqual(a, b) {\n  if (Object.is(a, b)) return true;\n  if (typeof a !== "object" || typeof b !== "object" || a === null || b === null) return false;\n  if (Array.isArray(a) !== Array.isArray(b)) return false;\n  const ka = Object.keys(a), kb = Object.keys(b);\n  if (ka.length !== kb.length) return false;\n  return ka.every((k) => k in b && deepEqual(a[k], b[k]));\n}';
W["i2-deep-equal"] =
  "function deepEqual(a, b) {\n  return JSON.stringify(a) === JSON.stringify(b);\n}";
R["i2-assert-throws"] =
  'function assertThrows(fn, errClass, msgPart) {\n  try {\n    fn();\n    return "no-throw";\n  } catch (e) {\n    if (errClass && !(e instanceof errClass)) return "wrong-type";\n    if (msgPart && !(e.message || "").includes(msgPart)) return "wrong-message";\n    return "ok";\n  }\n}';
W["i2-assert-throws"] =
  'function assertThrows(fn) {\n  try { fn(); return "no-throw"; } catch { return "ok"; }\n}';
R["i2-diff-msg"] =
  'function fmt(v) {\n  if (typeof v === "string") return \'"\' + v + \'"\';\n  if (v === null) return "null";\n  if (v === undefined) return "undefined";\n  if (typeof v === "function") return "function";\n  if (Array.isArray(v)) return "[" + v.map(fmt).join(", ") + "]";\n  if (typeof v === "object") return "{" + Object.entries(v).map(([k, x]) => k + ": " + fmt(x)).join(", ") + "}";\n  return String(v);\n}';
W["i2-diff-msg"] = "function fmt(v) {\n  return String(v);\n}";
R["i2-case-enumerate"] =
  'function edgeCases(value) {\n  const out = [];\n  const empty = Array.isArray(value) ? value.length === 0\n    : typeof value === "string" ? value === ""\n    : typeof value === "object" && value !== null ? Object.keys(value).length === 0 : false;\n  if (empty) out.push("empty");\n  if (value === 0 || Object.is(value, -0) || value === Number.MAX_SAFE_INTEGER) out.push("boundary");\n  if (value === null || value === undefined || Number.isNaN(value)) out.push("wrong-type");\n  if (typeof value === "string" && value !== "") out.push("wrong-type");\n  if (Array.isArray(value) && new Set(value).size !== value.length) out.push("duplicate");\n  return out;\n}';
W["i2-case-enumerate"] =
  'function edgeCases(value) {\n  return ["empty", "boundary", "wrong-type", "duplicate"];\n}';
R["i2-test-naming"] =
  'function testName(fn, behavior) {\n  if (!behavior) throw new Error("behavior required");\n  return fn + " " + behavior;\n}';
W["i2-test-naming"] = 'function testName(fn, behavior) {\n  return fn + " " + behavior;\n}';
R["i2-pyramid-pick"] =
  'function testLevel(spec) {\n  const s = spec.toLowerCase();\n  if (s.includes("user") || s.includes("click") || s.includes("browser")) return "e2e";\n  if (s.includes("with real") || s.includes("together")) return "integration";\n  return "unit";\n}';
W["i2-pyramid-pick"] = 'function testLevel(spec) {\n  return "unit";\n}';
R["i2-make-spy"] =
  "function makeSpy(impl) {\n  const calls = [];\n  const results = [];\n  const spy = (...args) => {\n    calls.push(args);\n    const r = impl ? impl(...args) : undefined;\n    results.push(r);\n    return r;\n  };\n  spy.calls = calls;\n  spy.results = results;\n  spy.reset = () => { calls.length = 0; results.length = 0; };\n  return spy;\n}";
W["i2-make-spy"] =
  "function makeSpy(impl) {\n  const spy = (...args) => impl && impl(...args);\n  spy.calls = [];\n  return spy;\n}";
R["i2-stub-fetch"] =
  "function makeFetchStub(routes) {\n  const requests = [];\n  const stub = async (url) => {\n    requests.push(url);\n    if (url in routes) {\n      return { ok: true, status: 200, json: async () => routes[url] };\n    }\n    return { ok: false, status: 404, json: async () => null };\n  };\n  stub.requests = requests;\n  return stub;\n}";
W["i2-stub-fetch"] =
  "function makeFetchStub(routes) {\n  return async () => ({ ok: true, status: 200, json: async () => ({}) });\n}";
R["i2-inject-seam"] =
  'function makeGreeter(clock) {\n  return (name) => {\n    const h = clock();\n    if (h < 12) return "Good morning, " + name;\n    if (h < 18) return "Good afternoon, " + name;\n    return "Good evening, " + name;\n  };\n}';
W["i2-inject-seam"] = 'function makeGreeter(clock) {\n  return (name) => "Hello, " + name;\n}';
R["i2-pipeline-bisect"] =
  "function firstBadStage(stages, inspect) {\n  let lo = 0, hi = stages.length - 1;\n  if (!inspect(stages[hi])) return null;\n  while (lo < hi) {\n    const mid = Math.floor((lo + hi) / 2);\n    if (inspect(stages[mid])) hi = mid; else lo = mid + 1;\n  }\n  return stages[lo];\n}";
W["i2-pipeline-bisect"] =
  "function firstBadStage(stages, inspect) {\n  return stages.find(inspect) ?? null;\n}";
R["i2-stack-read"] =
  'function firstOwnFrame(frames) {\n  return frames.find((f) => f.file.startsWith("app/")) ?? null;\n}\nfunction errorKind(message) {\n  if (message.includes("is not a function")) return "type";\n  if (message.includes("Cannot read prop")) return "shape";\n  return "other";\n}';
W["i2-stack-read"] =
  'function firstOwnFrame(frames) {\n  return frames[0] ?? null;\n}\nfunction errorKind(message) {\n  return "other";\n}';
R["i2-repro-minimize"] =
  "function minimalInput(inputs, isBroken) {\n  return inputs.find(isBroken) ?? null;\n}";
W["i2-repro-minimize"] = "function minimalInput(inputs, isBroken) {\n  return null;\n}";
R["i2-mini-runner"] =
  "function runSuite(tests) {\n  let passed = 0, failed = 0;\n  const failures = [];\n  for (const t of tests) {\n    try {\n      t.fn();\n      passed++;\n    } catch {\n      failed++;\n      failures.push(t.name);\n    }\n  }\n  return { passed, failed, failures };\n}";
W["i2-mini-runner"] =
  "function runSuite(tests) {\n  return { passed: tests.length, failed: 0, failures: [] };\n}";
R["i2-flaky-quarantine"] =
  "function quarantine(history) {\n  const stats = new Map();\n  for (const r of history) {\n    const s = stats.get(r.name) ?? { p: 0, f: 0 };\n    if (r.passed) s.p++; else s.f++;\n    stats.set(r.name, s);\n  }\n  const out = [];\n  for (const [name, s] of stats) if (s.p > 0 && s.f > 0) out.push(name);\n  return out.sort();\n}";
W["i2-flaky-quarantine"] =
  "function quarantine(history) {\n  return [...new Set(history.filter((r) => !r.passed).map((r) => r.name))].sort();\n}";
R["i2-regression-first"] =
  "function addRegression(ledger, bugId, fixCommit, coversAll) {\n  if (!coversAll || ledger.some((e) => e.bugId === bugId)) return ledger;\n  return [...ledger, { bugId, fixCommit }];\n}";
W["i2-regression-first"] =
  "function addRegression(ledger, bugId, fixCommit, coversAll) {\n  ledger.push({ bugId, fixCommit });\n  return ledger;\n}";
R["i2-phase-classify"] =
  'function phase(prop) {\n  const layout = ["width", "height", "top", "left", "margin", "font-size"];\n  const paint = ["color", "background", "box-shadow", "visibility"];\n  const composite = ["transform", "opacity"];\n  if (layout.includes(prop)) return "layout";\n  if (paint.includes(prop)) return "paint";\n  if (composite.includes(prop)) return "composite";\n  return "unknown";\n}';
W["i2-phase-classify"] = 'function phase(prop) {\n  return "layout";\n}';
R["i2-batch-rw"] =
  'function simulate(ops, onLayout) {\n  const mark = () => { if (onLayout) onLayout(); };\n  mark(); // initial layout\n  const reads = ops.filter((o) => o.op === "read");\n  const writes = ops.filter((o) => o.op === "write");\n  const heights = reads.map((o) => HEIGHTS[o.el]);\n  for (const w of writes) HEIGHTS[w.el] = w.value;\n  mark();\n  return heights;\n}\nconst HEIGHTS = { a: 10, b: 20, c: 30 };';
W["i2-batch-rw"] =
  'const HEIGHTS = { a: 10, b: 20, c: 30 };\nfunction simulate(ops, onLayout) {\n  const out = [];\n  for (const o of ops) {\n    if (o.op === "read") { if (onLayout) onLayout(); out.push(HEIGHTS[o.el]); }\n    else { HEIGHTS[o.el] = o.value; if (onLayout) onLayout(); }\n  }\n  return out;\n}';
R["i2-frame-budget"] =
  'function frameVerdict(tasks) {\n  const total = tasks.reduce((a, b) => a + b, 0);\n  if (total > 16.7) return "jank";\n  if (total > 12) return "tight";\n  return "smooth";\n}\nfunction longTaskCount(tasks) {\n  return tasks.filter((t) => t > 50).length;\n}';
W["i2-frame-budget"] =
  'function frameVerdict(tasks) {\n  return tasks[0] > 16.7 ? "jank" : "smooth";\n}\nfunction longTaskCount(tasks) {\n  return 0;\n}';
R["i2-script-attrs"] =
  'function scriptBehavior(attrs) {\n  if (!attrs.includes("src=")) return "inline";\n  if (attrs.includes("async")) return "async";\n  if (attrs.includes("defer")) return "defer";\n  return "blocking";\n}';
W["i2-script-attrs"] = 'function scriptBehavior(attrs) {\n  return "blocking";\n}';
R["i2-critical-chain"] =
  "function chainLength(requests, id) {\n  const byId = new Map(requests.map((r) => [r.id, r]));\n  let n = 0, cur = id;\n  while (cur && byId.has(cur)) {\n    n++;\n    cur = byId.get(cur).after;\n  }\n  return n;\n}";
W["i2-critical-chain"] = "function chainLength(requests, id) {\n  return 1;\n}";
R["i2-blocking-audit"] =
  "function firstPaintBlockers(resources) {\n  return resources.filter((r) => r.blocking).length;\n}\nfunction byKind(resources) {\n  const out = {};\n  for (const r of resources) out[r.type] = (out[r.type] ?? 0) + 1;\n  return out;\n}";
W["i2-blocking-audit"] =
  "function firstPaintBlockers(resources) {\n  return resources.length;\n}\nfunction byKind(resources) {\n  return {};\n}";
R["i2-cls-score"] =
  "function cls(shifts) {\n  let best = 0, cur = 0;\n  for (const s of shifts) {\n    if (s.sincePrev !== null && s.sincePrev > 500) {\n      best = Math.max(best, cur);\n      cur = 0;\n    }\n    cur += s.fraction * s.distance;\n  }\n  return Math.max(best, cur);\n}";
W["i2-cls-score"] =
  "function cls(shifts) {\n  return shifts.reduce((a, s) => a + s.fraction * s.distance, 0);\n}";
R["i2-vitals-grade"] =
  'function grade(vitals) {\n  let misses = 0;\n  if (vitals.lcp > 2.5) misses++;\n  if (vitals.inp > 200) misses++;\n  if (vitals.cls > 0.1) misses++;\n  if (misses === 0) return "good";\n  if (misses === 3) return "poor";\n  return "needs-improvement";\n}';
W["i2-vitals-grade"] = 'function grade(vitals) {\n  return vitals.lcp > 2.5 ? "poor" : "good";\n}';
R["i2-budget-enforce"] =
  "function audit(assets, budgets) {\n  const over = [];\n  for (const k of Object.keys(budgets)) {\n    if (assets[k] > budgets[k]) over.push(k);\n  }\n  over.sort();\n  return { pass: over.length === 0, over };\n}";
W["i2-budget-enforce"] = "function audit(assets, budgets) {\n  return { pass: true, over: [] };\n}";
R["i2-page-diagnose"] =
  'function diagnose(page) {\n  if (page.ttfbMs > 800) return "slow-server";\n  if (page.heroLazy) return "lazy-hero";\n  if (page.renderBlocking.includes("css")) return "blocking-css";\n  if (page.imageKB > 2000) return "oversized-images";\n  if (page.jsKB > 500) return "heavy-js";\n  return "healthy";\n}';
W["i2-page-diagnose"] = 'function diagnose(page) {\n  return "healthy";\n}';
R["i2-fix-and-remeasure"] =
  'function applyFix(page, fix) {\n  const p = { ...page, renderBlocking: [...page.renderBlocking] };\n  if (fix === "server") p.ttfbMs = p.ttfbMs / 2;\n  if (fix === "hero") p.heroLazy = false;\n  if (fix === "css") p.renderBlocking = [];\n  if (fix === "images") p.imageKB = p.imageKB / 4;\n  if (fix === "js") p.jsKB = p.jsKB / 2;\n  return p;\n}\nfunction improved(page, fix) {\n  const after = applyFix(page, fix);\n  return { before: page, after, better: diagnose(after) === "healthy" };\n}';
W["i2-fix-and-remeasure"] =
  "function applyFix(page, fix) {\n  page.ttfbMs = 0;\n  return page;\n}\nfunction improved(page, fix) {\n  return { before: page, after: page, better: false };\n}";
R["i2-lcp-chain"] =
  "function lcpEstimate(page) {\n  const cssBlockMs = page.renderBlocking.length * 50;\n  const imageMs = page.imageKB / 100;\n  return page.ttfbMs + cssBlockMs + imageMs;\n}\nfunction withinLcp(page) {\n  return lcpEstimate(page) <= 2500;\n}";
W["i2-lcp-chain"] =
  "function lcpEstimate(page) {\n  return 0;\n}\nfunction withinLcp(page) {\n  return true;\n}";

R["i2-perf-checkpoint"] =
  'function phaseOf(prop) {\n  const composite = ["transform", "opacity"];\n  const paint = ["color", "background", "box-shadow"];\n  const layout = ["width", "height", "top", "left", "font-size"];\n  if (composite.includes(prop)) return "composite";\n  if (paint.includes(prop)) return "paint";\n  if (layout.includes(prop)) return "layout";\n  return "style";\n}\nfunction budgetVerdict(actual, limit) {\n  if (actual <= limit) return "ok";\n  if (actual <= limit * 1.1) return "over";\n  return "fail";\n}\nfunction pickFix(symptom) {\n  const map = {\n    "slow-ttfb": "server",\n    "huge-image": "image-optimization",\n    "long-task": "chunking",\n    "layout-shift": "dimensions",\n    "render-blocking-css": "critical-css",\n  };\n  return map[symptom] ?? "profile-first";\n}';
W["i2-perf-checkpoint"] =
  'function phaseOf(prop) { return "layout"; }\nfunction budgetVerdict(actual, limit) { return "fail"; }\nfunction pickFix(symptom) { return "server"; }';
R["i2-phase-classify"] =
  'function phase(prop) {\n  const layout = ["width", "height", "top", "left", "margin", "font-size"];\n  const paint = ["color", "background", "box-shadow", "visibility"];\n  const composite = ["transform", "opacity"];\n  if (layout.includes(prop)) return "layout";\n  if (paint.includes(prop)) return "paint";\n  if (composite.includes(prop)) return "composite";\n  return "unknown";\n}';
W["i2-phase-classify"] = 'function phase(prop) {\n  return "layout";\n}';
R["i2-batch-rw"] =
  'function simulate(ops, onLayout) {\n  const mark = () => { if (onLayout) onLayout(); };\n  mark(); // initial layout\n  const reads = ops.filter((o) => o.op === "read");\n  const writes = ops.filter((o) => o.op === "write");\n  const heights = reads.map((o) => HEIGHTS[o.el]);\n  for (const w of writes) HEIGHTS[w.el] = w.value;\n  mark();\n  return heights;\n}\nconst HEIGHTS = { a: 10, b: 20, c: 30 };';
W["i2-batch-rw"] =
  'const HEIGHTS = { a: 10, b: 20, c: 30 };\nfunction simulate(ops, onLayout) {\n  const out = [];\n  for (const o of ops) {\n    if (o.op === "read") { if (onLayout) onLayout(); out.push(HEIGHTS[o.el]); }\n    else { HEIGHTS[o.el] = o.value; if (onLayout) onLayout(); }\n  }\n  return out;\n}';
R["i2-frame-budget"] =
  'function frameVerdict(tasks) {\n  const total = tasks.reduce((a, b) => a + b, 0);\n  if (total > 16.7) return "jank";\n  if (total > 12) return "tight";\n  return "smooth";\n}\nfunction longTaskCount(tasks) {\n  return tasks.filter((t) => t > 50).length;\n}';
W["i2-frame-budget"] =
  'function frameVerdict(tasks) {\n  return tasks[0] > 16.7 ? "jank" : "smooth";\n}\nfunction longTaskCount(tasks) {\n  return 0;\n}';
R["i2-script-attrs"] =
  'function scriptBehavior(attrs) {\n  if (!attrs.includes("src=")) return "inline";\n  if (attrs.includes("async")) return "async";\n  if (attrs.includes("defer")) return "defer";\n  return "blocking";\n}';
W["i2-script-attrs"] = 'function scriptBehavior(attrs) {\n  return "blocking";\n}';
R["i2-critical-chain"] =
  "function chainLength(requests, id) {\n  const byId = new Map(requests.map((r) => [r.id, r]));\n  let n = 0, cur = id;\n  while (cur && byId.has(cur)) {\n    n++;\n    cur = byId.get(cur).after;\n  }\n  return n;\n}";
W["i2-critical-chain"] = "function chainLength(requests, id) {\n  return 1;\n}";
R["i2-blocking-audit"] =
  "function firstPaintBlockers(resources) {\n  return resources.filter((r) => r.blocking).length;\n}\nfunction byKind(resources) {\n  const out = {};\n  for (const r of resources) out[r.type] = (out[r.type] ?? 0) + 1;\n  return out;\n}";
W["i2-blocking-audit"] =
  "function firstPaintBlockers(resources) {\n  return resources.length;\n}\nfunction byKind(resources) {\n  return {};\n}";
R["i2-cls-score"] =
  "function cls(shifts) {\n  let best = 0, cur = 0;\n  for (const s of shifts) {\n    if (s.sincePrev !== null && s.sincePrev > 500) {\n      best = Math.max(best, cur);\n      cur = 0;\n    }\n    cur += s.fraction * s.distance;\n  }\n  return Math.max(best, cur);\n}";
W["i2-cls-score"] =
  "function cls(shifts) {\n  return shifts.reduce((a, s) => a + s.fraction * s.distance, 0);\n}";
R["i2-vitals-grade"] =
  'function grade(vitals) {\n  let misses = 0;\n  if (vitals.lcp > 2.5) misses++;\n  if (vitals.inp > 200) misses++;\n  if (vitals.cls > 0.1) misses++;\n  if (misses === 0) return "good";\n  if (misses === 3) return "poor";\n  return "needs-improvement";\n}';
W["i2-vitals-grade"] = 'function grade(vitals) {\n  return vitals.lcp > 2.5 ? "poor" : "good";\n}';
R["i2-budget-enforce"] =
  "function audit(assets, budgets) {\n  const over = [];\n  for (const k of Object.keys(budgets)) {\n    if (assets[k] > budgets[k]) over.push(k);\n  }\n  over.sort();\n  return { pass: over.length === 0, over };\n}";
W["i2-budget-enforce"] = "function audit(assets, budgets) {\n  return { pass: true, over: [] };\n}";
R["i2-page-diagnose"] =
  'function diagnose(page) {\n  if (page.ttfbMs > 800) return "slow-server";\n  if (page.heroLazy) return "lazy-hero";\n  if (page.renderBlocking.includes("css")) return "blocking-css";\n  if (page.imageKB > 2000) return "oversized-images";\n  if (page.jsKB > 500) return "heavy-js";\n  return "healthy";\n}';
W["i2-page-diagnose"] = 'function diagnose(page) {\n  return "healthy";\n}';
R["i2-fix-and-remeasure"] =
  'function applyFix(page, fix) {\n  const p = { ...page, renderBlocking: [...page.renderBlocking] };\n  if (fix === "server") p.ttfbMs = p.ttfbMs / 2;\n  if (fix === "hero") p.heroLazy = false;\n  if (fix === "css") p.renderBlocking = [];\n  if (fix === "images") p.imageKB = p.imageKB / 4;\n  if (fix === "js") p.jsKB = p.jsKB / 2;\n  return p;\n}\nfunction improved(page, fix) {\n  const after = applyFix(page, fix);\n  return { before: page, after, better: JSON.stringify(after) !== JSON.stringify(page) };\n}';
W["i2-fix-and-remeasure"] =
  "function applyFix(page, fix) {\n  page.ttfbMs = 0;\n  return page;\n}\nfunction improved(page, fix) {\n  return { before: page, after: page, better: false };\n}";
R["i2-lcp-chain"] =
  "function lcpEstimate(page) {\n  const cssBlockMs = page.renderBlocking.length * 50;\n  const imageMs = page.imageKB / 100;\n  return page.ttfbMs + cssBlockMs + imageMs;\n}\nfunction withinLcp(page) {\n  return lcpEstimate(page) <= 2500;\n}";
W["i2-lcp-chain"] =
  "function lcpEstimate(page) {\n  return 0;\n}\nfunction withinLcp(page) {\n  return true;\n}";
R["i2-xss-sink"] =
  'function isDangerousSink(line) {\n  const sinks = ["innerHTML =", "innerHTML +=", "outerHTML =", "document.write(", "eval("];\n  return sinks.some((s) => line.includes(s));\n}';
W["i2-xss-sink"] = 'function isDangerousSink(line) {\n  return line.includes("innerHTML");\n}';
R["i2-html-encode"] =
  'function encodeHTML(s) {\n  return s\n    .replaceAll("&", "&amp;")\n    .replaceAll("<", "&lt;")\n    .replaceAll(">", "&gt;")\n    .replaceAll(\'"\', "&quot;")\n    .replaceAll("\'", "&#39;");\n}\nfunction rendersAsText(html) {\n  return html.includes("&lt;") && !html.includes("<");\n}';
W["i2-html-encode"] =
  "function encodeHTML(s) {\n  return s;\n}\nfunction rendersAsText(html) {\n  return true;\n}";
R["i2-url-encode"] =
  'function buildSearchUrl(base, params) {\n  const entries = Object.entries(params);\n  if (entries.length === 0) return base;\n  const qs = entries\n    .map(([k, v]) => encodeURIComponent(k) + "=" + encodeURIComponent(v))\n    .join("&");\n  return base + "?" + qs;\n}';
W["i2-url-encode"] =
  'function buildSearchUrl(base, params) {\n  return base + "?" + JSON.stringify(params);\n}';
R["i2-ownership-guard"] =
  'function canRead(record, user) {\n  if (!record || !user) return false;\n  return (\n    record.visibility === "public" ||\n    record.ownerId === user.id ||\n    user.role === "admin"\n  );\n}';
W["i2-ownership-guard"] =
  'function canRead(record, user) {\n  return record.visibility === "public";\n}';
R["i2-role-gate"] =
  'const TABLE = {\n  admin: ["read", "write", "delete"],\n  editor: ["read", "write"],\n  viewer: ["read"],\n};\nfunction authorize(user, action, resource) {\n  const allowed = user && TABLE[user.role];\n  return allowed && allowed.includes(action) ? "allow" : "deny";\n}';
W["i2-role-gate"] =
  'function authorize(user, action, resource) {\n  return user.role === "admin" ? "allow" : "deny";\n}';
R["i2-idor-scan"] =
  'function findIdor(routes) {\n  return routes\n    .filter((r) => r.path.includes(":id") && !r.hasOwnershipCheck)\n    .map((r) => r.path)\n    .sort();\n}';
W["i2-idor-scan"] =
  "function findIdor(routes) {\n  return routes.filter((r) => !r.hasOwnershipCheck).map((r) => r.path);\n}";
R["i2-header-audit"] =
  'function auditHeaders(headers) {\n  const out = [];\n  if (!headers["Content-Security-Policy"]) out.push("missing-csp");\n  if (!headers["Strict-Transport-Security"]) out.push("missing-hsts");\n  if (!headers["X-Content-Type-Options"]) out.push("missing-nosniff");\n  if (headers["X-Frame-Options"] !== "DENY") out.push("clickjackable");\n  return out;\n}';
W["i2-header-audit"] = "function auditHeaders(headers) {\n  return [];\n}";
R["i2-csp-parse"] =
  'function cspAllows(policy, kind) {\n  if (!policy) return false;\n  const dirs = {};\n  for (const part of policy.split(";")) {\n    const [name, ...srcs] = part.trim().split(/\\s+/);\n    if (name) dirs[name] = srcs;\n  }\n  const specific = kind === "img" ? "img-src" : "script-src";\n  const srcs = dirs[specific] ?? dirs["default-src"];\n  if (!srcs) return false;\n  return srcs.includes("\'self\'") || srcs.includes("data:");\n}';
W["i2-csp-parse"] = "function cspAllows(policy, kind) {\n  return policy.includes(\"'self'\");\n}";
R["i2-cors-decide"] =
  'function corsDecision(origin, allowedOrigins, credentials) {\n  const wildcard = allowedOrigins.includes("*");\n  const known = wildcard || allowedOrigins.includes(origin);\n  if (!known) return "deny";\n  if (wildcard && credentials) return "deny";\n  return credentials ? "allow-with-credentials" : "allow";\n}';
W["i2-cors-decide"] =
  'function corsDecision(origin, allowedOrigins, credentials) {\n  return "allow";\n}';
R["i2-secret-audit"] =
  'function auditConfig(config) {\n  const hasSecrets = Boolean(config.dbUrl || config.apiKey || config.sessionSecret);\n  if (hasSecrets && !config.gitignoredEnv) return "secrets-in-repo";\n  if (config.hardcoded.length > 0) return "hardcoded-credentials";\n  if (config.nodeEnv === "development") return "dev-config-in-prod";\n  return "clean";\n}';
W["i2-secret-audit"] = 'function auditConfig(config) {\n  return "clean";\n}';
R["i2-endpoint-audit"] =
  'function auditEndpoints(routes) {\n  let critical = 0, warnings = 0;\n  for (const r of routes) {\n    const unguardedWrite = !r.authRequired && r.method !== "GET";\n    const noRateOnAuth = !r.rateLimited && /login|register|reset/.test(r.path);\n    if (unguardedWrite || noRateOnAuth) critical++;\n    else if (!r.validatesInput) warnings++;\n  }\n  return { critical, warnings };\n}';
W["i2-endpoint-audit"] =
  "function auditEndpoints(routes) {\n  return { critical: 0, warnings: 0 };\n}";
R["i2-findings-report"] =
  "const RANK = { critical: 0, high: 1, medium: 2, low: 3 };\nfunction prioritize(findings) {\n  return findings\n    .map((f, i) => ({ ...f, i }))\n    .sort((a, b) => RANK[a.severity] - RANK[b.severity] || a.i - b.i)\n    .map((f) => f.id);\n}\nfunction summary(findings) {\n  const out = { critical: 0, high: 0, medium: 0, low: 0 };\n  for (const f of findings) out[f.severity]++;\n  return out;\n}";
W["i2-findings-report"] =
  "function prioritize(findings) {\n  return findings.map((f) => f.id);\n}\nfunction summary(findings) {\n  return { critical: 0, high: 0, medium: 0, low: 0 };\n}";

R["i2-security-checkpoint"] =
  'function classify(snippet) {\n  if (snippet.includes("innerHTML") || snippet.includes("document.write")) return "xss";\n  if (/(SELECT|query)\\s*\\(/.test(snippet) && snippet.includes("+")) return "sql-injection";\n  if (snippet.includes("exec(")) return "command-injection";\n  if (snippet.includes("/api/") && snippet.includes(":id") && snippet.includes("no owner check")) return "idor";\n  return "none";\n}\nfunction defenseFor(threat) {\n  const map = {\n    "xss": "output-encoding",\n    "sql-injection": "parameterized-queries",\n    "command-injection": "execfile-allowlist",\n    "idor": "ownership-check",\n    "csrf": "samesite-token",\n  };\n  return map[threat] ?? "defense-in-depth";\n}\nfunction corsVerdict(allowOrigin, credentials) {\n  if (allowOrigin === "*" && credentials) return "invalid";\n  if (allowOrigin !== "*") return "ok";\n  return "risky";\n}';
W["i2-security-checkpoint"] =
  'function classify(snippet) { return "none"; }\nfunction defenseFor(threat) { return "output-encoding"; }\nfunction corsVerdict(allowOrigin, credentials) { return "ok"; }';
R["i2-xss-sink"] =
  'function isDangerousSink(line) {\n  const sinks = ["innerHTML =", "innerHTML +=", "outerHTML =", "document.write(", "eval("];\n  return sinks.some((s) => line.includes(s));\n}';
W["i2-xss-sink"] = 'function isDangerousSink(line) {\n  return line.includes("innerHTML");\n}';
R["i2-html-encode"] =
  'function encodeHTML(s) {\n  return s\n    .replaceAll("&", "&amp;")\n    .replaceAll("<", "&lt;")\n    .replaceAll(">", "&gt;")\n    .replaceAll(\'"\', "&quot;")\n    .replaceAll("\'", "&#39;");\n}\nfunction rendersAsText(html) {\n  return html.includes("&lt;") && !html.includes("<");\n}';
W["i2-html-encode"] =
  "function encodeHTML(s) {\n  return s;\n}\nfunction rendersAsText(html) {\n  return true;\n}";
R["i2-url-encode"] =
  'function buildSearchUrl(base, params) {\n  const entries = Object.entries(params);\n  if (entries.length === 0) return base;\n  const qs = entries\n    .map(([k, v]) => encodeURIComponent(k) + "=" + encodeURIComponent(v))\n    .join("&");\n  return base + "?" + qs;\n}';
W["i2-url-encode"] =
  'function buildSearchUrl(base, params) {\n  return base + "?" + JSON.stringify(params);\n}';
R["i2-ownership-guard"] =
  'function canRead(record, user) {\n  if (!record || !user) return false;\n  return (\n    record.visibility === "public" ||\n    record.ownerId === user.id ||\n    user.role === "admin"\n  );\n}';
W["i2-ownership-guard"] =
  'function canRead(record, user) {\n  return record.visibility === "public";\n}';
R["i2-role-gate"] =
  'const TABLE = {\n  admin: ["read", "write", "delete"],\n  editor: ["read", "write"],\n  viewer: ["read"],\n};\nfunction authorize(user, action, resource) {\n  const allowed = user && TABLE[user.role];\n  return allowed && allowed.includes(action) ? "allow" : "deny";\n}';
W["i2-role-gate"] =
  'function authorize(user, action, resource) {\n  return user.role === "admin" ? "allow" : "deny";\n}';
R["i2-idor-scan"] =
  'function findIdor(routes) {\n  return routes\n    .filter((r) => r.path.includes(":id") && !r.hasOwnershipCheck)\n    .map((r) => r.path)\n    .sort();\n}';
W["i2-idor-scan"] =
  "function findIdor(routes) {\n  return routes.filter((r) => !r.hasOwnershipCheck).map((r) => r.path);\n}";
R["i2-header-audit"] =
  'function auditHeaders(headers) {\n  const out = [];\n  if (!headers["Content-Security-Policy"]) out.push("missing-csp");\n  if (!headers["Strict-Transport-Security"]) out.push("missing-hsts");\n  if (!headers["X-Content-Type-Options"]) out.push("missing-nosniff");\n  if (headers["X-Frame-Options"] !== "DENY") out.push("clickjackable");\n  return out;\n}';
W["i2-header-audit"] = "function auditHeaders(headers) {\n  return [];\n}";
R["i2-csp-parse"] =
  'function cspAllows(policy, kind) {\n  if (!policy) return false;\n  const dirs = {};\n  for (const part of policy.split(";")) {\n    const [name, ...srcs] = part.trim().split(/\\s+/);\n    if (name) dirs[name] = srcs;\n  }\n  const specific = kind === "img" ? "img-src" : "script-src";\n  const srcs = dirs[specific] ?? dirs["default-src"];\n  if (!srcs) return false;\n  return srcs.includes("\'self\'") || srcs.includes("data:");\n}';
W["i2-csp-parse"] = "function cspAllows(policy, kind) {\n  return policy.includes(\"'self'\");\n}";
R["i2-cors-decide"] =
  'function corsDecision(origin, allowedOrigins, credentials) {\n  const wildcard = allowedOrigins.includes("*");\n  const known = wildcard || allowedOrigins.includes(origin);\n  if (!known) return "deny";\n  if (wildcard && credentials) return "deny";\n  return credentials ? "allow-with-credentials" : "allow";\n}';
W["i2-cors-decide"] =
  'function corsDecision(origin, allowedOrigins, credentials) {\n  return "allow";\n}';
R["i2-secret-audit"] =
  'function auditConfig(config) {\n  const hasSecrets = Boolean(config.dbUrl || config.apiKey || config.sessionSecret);\n  if (hasSecrets && !config.gitignoredEnv) return "secrets-in-repo";\n  if (config.hardcoded.length > 0) return "hardcoded-credentials";\n  if (config.nodeEnv === "development") return "dev-config-in-prod";\n  return "clean";\n}';
W["i2-secret-audit"] = 'function auditConfig(config) {\n  return "clean";\n}';
R["i2-endpoint-audit"] =
  'function auditEndpoints(routes) {\n  let critical = 0, warnings = 0;\n  for (const r of routes) {\n    const unguardedWrite = !r.authRequired && r.method !== "GET";\n    const noRateOnAuth = !r.rateLimited && /login|register|reset/.test(r.path);\n    if (unguardedWrite || noRateOnAuth) critical++;\n    else if (!r.validatesInput) warnings++;\n  }\n  return { critical, warnings };\n}';
W["i2-endpoint-audit"] =
  "function auditEndpoints(routes) {\n  return { critical: 0, warnings: 0 };\n}";
R["i2-findings-report"] =
  "const RANK = { critical: 0, high: 1, medium: 2, low: 3 };\nfunction prioritize(findings) {\n  return findings\n    .map((f, i) => ({ ...f, i }))\n    .sort((a, b) => RANK[a.severity] - RANK[b.severity] || a.i - b.i)\n    .map((f) => f.id);\n}\nfunction summary(findings) {\n  const out = { critical: 0, high: 0, medium: 0, low: 0 };\n  for (const f of findings) out[f.severity]++;\n  return out;\n}";
W["i2-findings-report"] =
  "function prioritize(findings) {\n  return findings.map((f) => f.id);\n}\nfunction summary(findings) {\n  return { critical: 0, high: 0, medium: 0, low: 0 };\n}";
R["i2-url-parse"] =
  'function parseRequest(url) {\n  const [path, qs] = url.split("?");\n  const query = {};\n  if (qs) {\n    for (const pair of qs.split("&")) {\n      const [k, v = ""] = pair.split("=");\n      query[decodeURIComponent(k)] = decodeURIComponent(v);\n    }\n  }\n  const segs = path.split("/").filter(Boolean);\n  const params = {};\n  if (segs.length >= 2 && /^\\d+$/.test(segs[segs.length - 1])) {\n    params.id = segs[segs.length - 1];\n  }\n  return { path, params, query };\n}';
W["i2-url-parse"] =
  "function parseRequest(url) {\n  return { path: url, params: {}, query: {} };\n}";
R["i2-body-stream"] =
  'function assembleBody(chunks) {\n  if (chunks.length === 0) return { ok: false, error: "invalid-json" };\n  try {\n    return { ok: true, data: JSON.parse(chunks.join("")) };\n  } catch {\n    return { ok: false, error: "invalid-json" };\n  }\n}';
W["i2-body-stream"] =
  'function assembleBody(chunks) {\n  return { ok: true, data: JSON.parse(chunks.join("")) };\n}';
R["i2-status-classify"] =
  'function respond(handler) {\n  const table = {\n    "create-ok": { status: 201, body: { ok: true } },\n    "create-duplicate": { status: 409, body: { error: "duplicate" } },\n    "get-ok": { status: 200, body: { ok: true } },\n    "get-missing": { status: 404, body: { error: "not-found" } },\n    "update-invalid": { status: 400, body: { error: "validation" } },\n    "delete-ok": { status: 204, body: null },\n    "boom": { status: 500, body: { error: "internal" } },\n  };\n  return table[handler];\n}';
W["i2-status-classify"] =
  "function respond(handler) {\n  return { status: 200, body: { ok: true } };\n}";
R["i2-route-review"] =
  'const VERBS = ["get", "list", "create", "delete", "update", "fetch", "save"];\nfunction reviewRoute(method, path) {\n  const lower = path.toLowerCase();\n  if (VERBS.some((v) => lower.includes(v))) return "verb";\n  const segs = lower.split("/").filter(Boolean);\n  const needsId = ["PUT", "PATCH", "DELETE"].includes(method);\n  if (needsId && segs.length < 3) return "missing-id";\n  return "good";\n}';
W["i2-route-review"] = 'function reviewRoute(method, path) {\n  return "good";\n}';
W["i2-route-review"] = 'function reviewRoute(method, path) {\n  return "good";\n}';
R["i2-pagination"] =
  "function paginate(items, query) {\n  const limit = Math.min(Math.max(Math.trunc(query.limit ?? 10), 1), 100);\n  const offset = Math.max(Math.trunc(query.offset ?? 0), 0);\n  const results = items.slice(offset, offset + limit);\n  const next = offset + limit < items.length ? offset + limit : null;\n  return { results, total: items.length, next };\n}";
W["i2-pagination"] =
  "function paginate(items, query) {\n  return { results: items, total: items.length, next: null };\n}";
R["i2-error-shape"] =
  "function apiError(status, message, field) {\n  const error = { message };\n  if (field !== undefined) error.field = field;\n  return { status, body: { error } };\n}\nfunction fromZod(issues) {\n  return issues.map((i) => ({ field: i.path, message: i.message }));\n}";
W["i2-error-shape"] =
  "function apiError(status, message, field) {\n  return { status, body: { error: { message, field } } };\n}\nfunction fromZod(issues) {\n  return issues;\n}";
R["i2-pipeline-run"] =
  "function runPipeline(middlewares, handler) {\n  const req = {};\n  let i = 0;\n  const next = () => {\n    const mw = middlewares[i++];\n    if (mw) mw(req, next);\n    else handler(req);\n  };\n  next();\n  return req;\n}";
W["i2-pipeline-run"] =
  "function runPipeline(middlewares, handler) {\n  const req = {};\n  handler(req);\n  return req;\n}";
R["i2-auth-guard-order"] =
  'function securePipeline(config) {\n  return ["logger", "bodyParser", "rateLimiter", "auth", "router"];\n}';
W["i2-auth-guard-order"] = 'function securePipeline(config) {\n  return ["auth", "router"];\n}';
R["i2-error-boundary"] =
  'function withErrorBoundary(handler) {\n  return (input) => {\n    try {\n      return { status: 200, body: handler(input) };\n    } catch (err) {\n      if (err && typeof err.status === "number") {\n        return { status: err.status, body: { error: err.message } };\n      }\n      return { status: 500, body: { error: "internal error" } };\n    }\n  };\n}';
W["i2-error-boundary"] =
  "function withErrorBoundary(handler) {\n  return (input) => ({ status: 200, body: handler(input) });\n}";
R["i2-store-create"] =
  'function makeStore() {\n  let n = 0;\n  const tasks = new Map();\n  return {\n    create(body, userId) {\n      const errors = [];\n      const title = typeof body.title === "string" ? body.title.trim() : "";\n      if (!title || title.length > 200) errors.push({ field: "title", message: "1-200 chars" });\n      if (body.due !== undefined && body.due !== null && !Number.isInteger(Date.parse(body.due))) {\n        errors.push({ field: "due", message: "ISO date" });\n      }\n      if (errors.length) return { ok: false, errors };\n      const id = "t" + ++n;\n      const task = { id, title, due: body.due ?? null, ownerId: userId, done: false };\n      tasks.set(id, task);\n      return { ok: true, task };\n    },\n  };\n}';
W["i2-store-create"] =
  'function makeStore() {\n  return {\n    create(body, userId) {\n      return { ok: true, task: { id: "t1", title: body.title, ownerId: userId, done: false } };\n    },\n  };\n}';
R["i2-store-authz"] =
  'function makeStore() {\n  let n = 0;\n  const tasks = new Map();\n  return {\n    create(body, userId) {\n      const id = "t" + ++n;\n      const task = { id, title: body.title, due: body.due ?? null, ownerId: userId, done: false };\n      tasks.set(id, task);\n      return { ok: true, task };\n    },\n    update(id, patch, userId) {\n      const task = tasks.get(id);\n      if (!task) return { ok: false, status: 404 };\n      if (task.ownerId !== userId) return { ok: false, status: 403 };\n      if (typeof patch.title === "string") task.title = patch.title;\n      if (typeof patch.done === "boolean") task.done = patch.done;\n      return { ok: true, task };\n    },\n    remove(id, userId) {\n      const task = tasks.get(id);\n      if (!task) return { ok: false, status: 404 };\n      if (task.ownerId !== userId) return { ok: false, status: 403 };\n      tasks.delete(id);\n      return { ok: true };\n    },\n    list(query, userId) {\n      return [...tasks.values()].filter((t) => t.ownerId === userId);\n    },\n  };\n}';
W["i2-store-authz"] =
  "function makeStore() {\n  const tasks = new Map();\n  return {\n    update(id, patch, userId) {\n      const task = tasks.get(id);\n      if (task.ownerId !== userId) return { ok: false, status: 403 };\n      task.title = patch.title;\n      return { ok: true, task };\n    },\n    remove(id, userId) {\n      tasks.delete(id);\n      return { ok: true };\n    },\n  };\n}";
R["i2-store-query"] =
  'function makeStore() {\n  let n = 0;\n  const tasks = new Map();\n  return {\n    create(body, userId) {\n      const id = "t" + ++n;\n      const task = { id, title: body.title, ownerId: userId, done: false };\n      tasks.set(id, task);\n      return { ok: true, task };\n    },\n    update(id, patch, userId) {\n      const task = tasks.get(id);\n      if (task.ownerId !== userId) return { ok: false, status: 403 };\n      if (typeof patch.done === "boolean") task.done = patch.done;\n      return { ok: true, task };\n    },\n    list(query = {}, userId) {\n      let out = [...tasks.values()].filter((t) => t.ownerId === userId);\n      if (typeof query.done === "boolean") out = out.filter((t) => t.done === query.done);\n      if (query.title) out = out.filter((t) => t.title.toLowerCase().includes(query.title.toLowerCase()));\n      return out.sort((a, b) => a.id.localeCompare(b.id));\n    },\n  };\n}';
W["i2-store-query"] =
  "function makeStore() {\n  const tasks = new Map();\n  return {\n    list(query, userId) {\n      return [...tasks.values()];\n    },\n  };\n}";

R["i2-backend-checkpoint"] =
  'function matchRoute(pattern, method, path, method2) {\n  if (method !== method2) return null;\n  const pp = pattern.split("/").filter(Boolean);\n  const sp = path.split("/").filter(Boolean);\n  if (pp.length !== sp.length) return null;\n  const params = {};\n  for (let i = 0; i < pp.length; i++) {\n    if (pp[i].startsWith(":")) {\n      if (!sp[i]) return null;\n      params[pp[i].slice(1)] = sp[i];\n    } else if (pp[i] !== sp[i]) {\n      return null;\n    }\n  }\n  return params;\n}\nfunction orderMiddleware(names) {\n  return ["logger", "bodyParser", "auth", "errorBoundary"].filter((n) => names.includes(n));\n}\nfunction statusFor(situation) {\n  const map = {\n    "created": 201,\n    "validation-failed": 400,\n    "not-logged-in": 401,\n    "not-allowed": 403,\n    "missing": 404,\n    "duplicate": 409,\n    "crashed": 500,\n  };\n  return map[situation];\n}';
W["i2-backend-checkpoint"] =
  "function matchRoute(pattern, method, path, method2) { return null; }\nfunction orderMiddleware(names) { return names; }\nfunction statusFor(situation) { return 200; }";
R["i2-select-filter"] =
  'function selectRows(rows, spec) {\n  let out = rows;\n  if (spec.where) {\n    out = out.filter((r) =>\n      Object.entries(spec.where).every(([col, val]) => (val === null ? r[col] === null : r[col] === val))\n    );\n  }\n  if (spec.orderBy) {\n    const [col, dir] = spec.orderBy;\n    const cmp = (a, b) => {\n      const av = a[col], bv = b[col];\n      if (av === null && bv === null) return 0;\n      if (av === null) return 1;\n      if (bv === null) return -1;\n      return av < bv ? -1 : av > bv ? 1 : 0;\n    };\n    out = [...out].sort(cmp);\n    if (dir === "desc") out.reverse();\n  }\n  const offset = spec.offset ?? 0;\n  const limit = spec.limit ?? out.length;\n  return out.slice(offset, offset + limit);\n}';
W["i2-select-filter"] = "function selectRows(rows, spec) {\n  return rows;\n}";
W["i2-select-filter"] = "function selectRows(rows, spec) {\n  return rows;\n}";
R["i2-aggregate"] =
  "function groupByCount(rows, key) {\n  const counts = new Map();\n  for (const r of rows) counts.set(r[key], (counts.get(r[key]) ?? 0) + 1);\n  return [...counts.entries()]\n    .map(([k, c]) => ({ key: k, count: c }))\n    .sort((a, b) => b.count - a.count || String(a.key).localeCompare(String(b.key)));\n}\nfunction having(rows, key, min) {\n  return groupByCount(rows, key).filter((g) => g.count >= min);\n}";
W["i2-aggregate"] =
  "function groupByCount(rows, key) {\n  return rows.map((r) => ({ key: r[key], count: 1 }));\n}\nfunction having(rows, key, min) {\n  return groupByCount(rows, key);\n}";
R["i2-sql-audit"] =
  'function auditStatement(sql) {\n  const upd = /^(UPDATE|DELETE)\\b/.test(sql);\n  if (upd && !/\\bWHERE\\b/i.test(sql)) return "unsafe";\n  if (sql.includes(\'" + \') || sql.includes("${") || sql.includes("= NULL")) return "unsafe";\n  if (/\\$1|\\?/.test(sql) && /\\bWHERE\\b/i.test(sql)) return "parameterized";\n  return "ok";\n}';
W["i2-sql-audit"] = 'function auditStatement(sql) {\n  return "ok";\n}';
R["i2-fk-enforce"] =
  'function insertWithFK(tables, table, row) {\n  if (table === "tasks") {\n    if (!tables.users.has(row.authorId)) {\n      return { ok: false, error: "fk-violation" };\n    }\n    const id = "t" + (tables.tasks.length + 1);\n    tables.tasks.push({ ...row, id });\n    return { ok: true, id };\n  }\n  return { ok: false, error: "unknown-table" };\n}';
W["i2-fk-enforce"] =
  'function insertWithFK(tables, table, row) {\n  const id = "t" + (tables.tasks.length + 1);\n  tables.tasks.push({ ...row, id });\n  return { ok: true, id };\n}';
R["i2-junction-check"] =
  'function link(tables, taskId, tagId) {\n  const hasTask = tables.tasks.some((t) => t.id === taskId);\n  const hasTag = tables.tags.some((t) => t.id === tagId);\n  if (!hasTask || !hasTag) return { ok: false, error: "fk-violation" };\n  const pair = { taskId, tagId };\n  if (tables.taskTags.some((p) => p.taskId === taskId && p.tagId === tagId)) {\n    return { ok: false, error: "duplicate" };\n  }\n  tables.taskTags.push(pair);\n  return { ok: true, pair };\n}';
W["i2-junction-check"] =
  "function link(tables, taskId, tagId) {\n  tables.taskTags.push({ taskId, tagId });\n  return { ok: true };\n}";
R["i2-normalize-check"] =
  'function isNormalized(rows) {\n  return !rows.some((r) => "authorName" in r && "authorId" in r);\n}\nfunction normalize(rows) {\n  return rows.map(({ authorName, ...rest }) => rest);\n}';
W["i2-normalize-check"] =
  "function isNormalized(rows) {\n  return true;\n}\nfunction normalize(rows) {\n  return rows;\n}";
R["i2-repository"] =
  'function makeRepo(db) {\n  return {\n    create(data) {\n      const row = { ...data, id: "r" + db.nextId++ };\n      db.rows.push(row);\n      return row;\n    },\n    findById(id) {\n      return db.rows.find((r) => r.id === id) ?? null;\n    },\n    update(id, patch) {\n      const row = db.rows.find((r) => r.id === id);\n      if (!row) return { ok: false, error: "not-found" };\n      Object.assign(row, patch);\n      return { ok: true, row };\n    },\n    remove(id) {\n      const i = db.rows.findIndex((r) => r.id === id);\n      if (i === -1) return { ok: false, error: "not-found" };\n      db.rows.splice(i, 1);\n      return { ok: true };\n    },\n  };\n}';
W["i2-repository"] =
  "function makeRepo(db) {\n  return {\n    create(data) { db.rows.push(data); return data; },\n    findById(id) { return db.rows[0] ?? null; },\n    update(id, patch) { return { ok: true, row: db.rows[0] }; },\n    remove(id) { return { ok: true }; },\n  };\n}";
R["i2-transfer-tx"] =
  'function transfer(accounts, fromId, toId, amount) {\n  const from = accounts.get(fromId);\n  const to = accounts.get(toId);\n  if (!from || !to) return { ok: false, error: "not-found" };\n  if (from.balance < amount) return { ok: false, error: "insufficient" };\n  from.balance -= amount;\n  to.balance += amount;\n  return { ok: true };\n}';
W["i2-transfer-tx"] =
  "function transfer(accounts, fromId, toId, amount) {\n  accounts.get(fromId).balance -= amount;\n  accounts.get(toId).balance += amount;\n  return { ok: true };\n}";
R["i2-n1-refactor"] =
  'function countFetches(taskCount, strategy) {\n  if (strategy === "naive") return 1 + taskCount;\n  if (strategy === "join") return 1;\n  return 2;\n}\nfunction refactorReport(taskCount, savedMs) {\n  const naive = countFetches(taskCount, "naive");\n  const join = countFetches(taskCount, "join");\n  return { naive, join, msSaved: (naive - join) * savedMs };\n}';
W["i2-n1-refactor"] =
  "function countFetches(taskCount, strategy) {\n  return taskCount;\n}\nfunction refactorReport(taskCount, savedMs) {\n  return { naive: 0, join: 0, msSaved: 0 };\n}";
R["i2-request-flow"] =
  'const TRANSITIONS = {\n  "idle|fetch": "loading",\n  "loading|resolve-with-data": "success",\n  "loading|resolve-empty": "empty",\n  "loading|reject": "error",\n  "success|fetch": "loading",\n  "error|fetch": "loading",\n  "empty|fetch": "loading",\n  "idle|reset": "idle",\n  "success|reset": "idle",\n  "error|reset": "idle",\n  "empty|reset": "idle",\n  "loading|reset": "idle",\n};\nfunction uiStateFor(event) {\n  return TRANSITIONS[event.from + "|" + event.on] ?? "idle-state-invalid";\n}';
W["i2-request-flow"] = 'function uiStateFor(event) {\n  return "loading";\n}';
R["i2-shared-schema"] =
  'function makeContract() {\n  return {\n    validateTask(body) {\n      const issues = [];\n      if (typeof body.title !== "string" || !body.title.trim() || body.title.length > 200) {\n        issues.push({ field: "title", message: "required, 1-200 chars" });\n      }\n      if (body.done !== undefined && typeof body.done !== "boolean") {\n        issues.push({ field: "done", message: "must be boolean" });\n      }\n      if (issues.length) return { ok: false, issues };\n      return { ok: true, value: { title: body.title, done: body.done ?? false } };\n    },\n    toApiShape(task) {\n      const { ownerId, ...rest } = task;\n      return { ...rest, author: ownerId };\n    },\n  };\n}';
W["i2-shared-schema"] =
  "function makeContract() {\n  return {\n    validateTask(body) {\n      return { ok: true, value: body };\n    },\n    toApiShape(task) {\n      return { ...task, author: task.ownerId };\n    },\n  };\n}";
R["i2-optimistic-ui"] =
  'function optimisticApply(state, action) {\n  if (action.type === "add") {\n    return {\n      items: [...state.items, action.item],\n      pending: [...state.pending, action.item.id],\n    };\n  }\n  if (action.type === "confirm") {\n    return { ...state, pending: state.pending.filter((id) => id !== action.id) };\n  }\n  if (action.type === "rollback") {\n    return {\n      items: state.items.filter((i) => i.id !== action.id),\n      pending: state.pending.filter((id) => id !== action.id),\n    };\n  }\n  return state;\n}';
W["i2-optimistic-ui"] =
  "function optimisticApply(state, action) {\n  state.items.push(action.item);\n  return state;\n}";

R["i2-db-checkpoint"] =
  'function joinPlan(query) {\n  if (query.includes("skip users with none")) return "inner";\n  if (query.includes("zero included")) return "left";\n  if (query.includes("tag names")) return "inner-two";\n  return "none";\n}\nfunction txDecision(steps, hasFailureRisk) {\n  if (steps === 0) return "readonly";\n  if (steps >= 2 || hasFailureRisk) return "transaction";\n  return "single";\n}\nfunction countQueries(taskCount, pattern) {\n  if (pattern === "n+1") return taskCount + 1;\n  if (pattern === "join") return 1;\n  return 2;\n}';
W["i2-db-checkpoint"] =
  'function joinPlan(query) { return "inner"; }\nfunction txDecision(steps, hasFailureRisk) { return "single"; }\nfunction countQueries(taskCount, pattern) { return 0; }';
R["i2-read-env"] =
  'function readEnv(env, required) {\n  const missing = required.filter((k) => env[k] === undefined || env[k] === "");\n  if (missing.length > 0) {\n    throw new Error("Missing required env vars: " + missing.join(", "));\n  }\n  return env;\n}';
W["i2-read-env"] =
  'function readEnv(env, required) {\n  for (const k of required) {\n    if (!(k in env)) throw new Error("Missing " + k);\n  }\n  return env;\n}';
R["i2-config-loader"] =
  'function loadConfig(env) {\n  let port = 3000;\n  if (env.PORT !== undefined) {\n    port = Number(env.PORT);\n    if (Number.isNaN(port)) throw new Error("PORT must be a number, got: " + env.PORT);\n  }\n  return {\n    port,\n    databaseUrl: env.DATABASE_URL || "",\n    debug: env.DEBUG === "true",\n    features: env.FEATURES ? env.FEATURES.split(",") : [],\n  };\n}';
W["i2-config-loader"] =
  'function loadConfig(env) {\n  return {\n    port: Number(env.PORT),\n    databaseUrl: env.DATABASE_URL,\n    debug: Boolean(env.DEBUG),\n    features: env.FEATURES.split(","),\n  };\n}';
R["i2-release-gate"] =
  'function canRelease(checks) {\n  if (!checks.ci) return "ci";\n  if (!checks.migrations) return "migrations";\n  if (!checks.smoke) return "smoke";\n  if (checks.reviewers < 1) return "review";\n  return "yes";\n}';
W["i2-release-gate"] =
  'function canRelease(checks) {\n  if (checks.ci && checks.migrations && checks.smoke && checks.reviewers >= 1) return "yes";\n  return "blocked";\n}';
R["i2-rollback-or-fix"] =
  'function respond(incident) {\n  if (incident.dataLoss) return "rollback";\n  if (incident.mitigationWorks && incident.fixReady) return "fix-forward";\n  if (incident.mitigationWorks) return "feature-off";\n  return "rollback";\n}';
W["i2-rollback-or-fix"] =
  'function respond(incident) {\n  if (incident.fixReady) return "fix-forward";\n  if (incident.mitigationWorks) return "feature-off";\n  return "rollback";\n}';
R["i2-canary-cohort"] =
  "function canaryFor(user, rollout) {\n  if (user.betaOptIn) return true;\n  if (user.internal && rollout.excludeInternals) return false;\n  return hash(user.id) % 100 < rollout.percent;\n}";
W["i2-canary-cohort"] =
  "function canaryFor(user, rollout) {\n  return hash(user.id) % 100 < rollout.percent;\n}";
R["i2-structured-log"] =
  'function logLine(level, event, fields) {\n  if (!["debug", "info", "warn", "error"].includes(level)) {\n    throw new Error("Invalid level: " + level);\n  }\n  return JSON.stringify({ ts: fixedTimestamp, level, event, ...fields, level, event });\n}';
W["i2-structured-log"] =
  "function logLine(level, event, fields) {\n  return JSON.stringify({ ...fields, ts: fixedTimestamp, level, event });\n}";
R["i2-health-checks"] =
  "function healthZ(state) {\n  return state.crashed ? 503 : 200;\n}\n\nfunction readyZ(state) {\n  return state.dbUp && state.cacheUp ? 200 : 503;\n}";
W["i2-health-checks"] =
  "function healthZ(state) {\n  return state.dbUp && state.cacheUp ? 200 : 503;\n}\n\nfunction readyZ(state) {\n  return state.crashed ? 503 : 200;\n}";
R["i2-alert-triage"] =
  'function triage(alert) {\n  if (!alert.actionable) return "dashboard";\n  return alert.urgent ? "page" : "ticket";\n}';
W["i2-alert-triage"] =
  'function triage(alert) {\n  if (alert.urgent) return "page";\n  if (alert.actionable) return "dashboard";\n  return "ticket";\n}';
R["i2-structured-log"] =
  'const fixedTimestamp = 1700000000000;\nfunction logLine(level, event, fields) {\n  if (!["debug", "info", "warn", "error"].includes(level)) {\n    throw new Error("Invalid level: " + level);\n  }\n  return JSON.stringify({ ts: fixedTimestamp, level, event, ...fields, level, event });\n}';
W["i2-structured-log"] =
  "function logLine(level, event, fields) {\n  return JSON.stringify({ ...fields, ts: 0, level, event });\n}";
R["i2-canary-cohort"] =
  "function hash(s) {\n  let h = 0;\n  for (let i = 0; i < s.length; i++) {\n    h = (h * 31 + s.charCodeAt(i)) >>> 0;\n  }\n  return h;\n}\nfunction canaryFor(user, rollout) {\n  if (user.betaOptIn) return true;\n  if (user.internal && rollout.excludeInternals) return false;\n  return hash(user.id) % 100 < rollout.percent;\n}";
W["i2-canary-cohort"] =
  "function hash(s) { return 0; }\nfunction canaryFor(user, rollout) {\n  return hash(user.id) % 100 < rollout.percent;\n}";
R["i2-prod-checkpoint"] =
  'function envVerdict(config) {\n  if (!config.secretsInEnv) return "unsafe-secrets";\n  if (!config.validated) return "invalid-config";\n  if (config.devBuild) return "dev-build";\n  return "ready";\n}\nfunction releaseStrategy(risk, users) {\n  if (risk === "low") return "rolling";\n  if (users > 10000) return "canary";\n  return "blue-green";\n}\nfunction triage(alert) {\n  if (!alert.actionable) return "dashboard";\n  return alert.urgent ? "page" : "ticket";\n}';
W["i2-prod-checkpoint"] =
  'function envVerdict(config) { return "ready"; }\nfunction releaseStrategy(risk, users) {\n  if (risk === "high") return "canary";\n  return "blue-green";\n}\nfunction triage(alert) {\n  return alert.urgent ? "page" : "ticket";\n}';
R["i2-capstone-model"] =
  'const model = {\n  table: "tickets",\n  columns: ["id", "author_id", "title", "description", "priority", "status", "created_at", "closed_at"],\n  priorities: ["low", "medium", "high"],\n  closedByDefault: "open",\n};';
W["i2-capstone-model"] =
  'const model = {\n  table: "t",\n  columns: ["id", "title"],\n  priorities: ["low", "high"],\n  closedByDefault: "",\n};';
R["i2-capstone-contract"] =
  'const createEndpoint = {\n  method: "POST",\n  path: "/api/tickets",\n  successStatus: 201,\n  bodyFields: ["title", "description", "priority"],\n};\n\nconst listEndpoint = {\n  method: "GET",\n  path: "/api/tickets",\n  queryParam: "priority",\n};';
W["i2-capstone-contract"] =
  'const createEndpoint = {\n  method: "GET",\n  path: "tickets",\n  successStatus: 302,\n  bodyFields: ["title"],\n};\n\nconst listEndpoint = {\n  method: "POST",\n  path: "tickets",\n  queryParam: 7,\n};';
R["i2-capstone-authz"] =
  'const authz = {\n  authorOnlyEdit: true,\n  serverChecks: true,\n  idSource: "session",\n};';
W["i2-capstone-authz"] =
  'const authz = {\n  authorOnlyEdit: false,\n  serverChecks: false,\n  idSource: "request-body",\n};';
R["i2-capstone-errors"] =
  "const errors = {\n  invalidTicket: 400,\n  notAuthor: 403,\n  notSignedIn: 401,\n  clientValidates: true,\n};";
W["i2-capstone-errors"] =
  "const errors = {\n  invalidTicket: 500,\n  notAuthor: 200,\n  notSignedIn: 400,\n  clientValidates: false,\n};";
R["i2-capstone-states"] =
  "const states = {\n  loading: true,\n  errorState: true,\n  emptyState: true,\n  optimisticWrite: true,\n};";
W["i2-capstone-states"] =
  "const states = {\n  loading: false,\n  errorState: false,\n  emptyState: false,\n  optimisticWrite: false,\n};";
R["i2-capstone-deploy"] =
  'const deploy = {\n  envSecrets: true,\n  migrations: "versioned-scripts",\n  healthEndpoint: "/healthz",\n  buildIsReproducible: true,\n};';
W["i2-capstone-deploy"] =
  'const deploy = {\n  envSecrets: false,\n  migrations: "manual-sql",\n  healthEndpoint: "health",\n  buildIsReproducible: false,\n};';
R["i2-capstone-verification"] =
  "const capstone = {\n  dataModel: true,\n  apiValidates: true,\n  apiAuthorizes: true,\n  asyncStates: true,\n  accessibilityPass: true,\n  testsWritten: true,\n  readme: true,\n};";
W["i2-capstone-verification"] =
  "const capstone = {\n  dataModel: true,\n  apiValidates: false,\n  apiAuthorizes: true,\n  asyncStates: false,\n  accessibilityPass: true,\n  testsWritten: false,\n  readme: true,\n};";
R["i2-capstone-model"] =
  'const model = {\n  table: "tickets",\n  columns: ["id", "author_id", "title", "description", "priority", "status", "created_at", "closed_at"],\n  priorities: ["low", "medium", "high"],\n  closedByDefault: "open",\n};';
W["i2-capstone-model"] =
  'const model = {\n  table: "t",\n  columns: ["id", "title"],\n  priorities: ["low", "high"],\n  closedByDefault: "",\n};';
R["i2-capstone-contract"] =
  'const createEndpoint = {\n  method: "POST",\n  path: "/api/tickets",\n  successStatus: 201,\n  bodyFields: ["title", "description", "priority"],\n};\n\nconst listEndpoint = {\n  method: "GET",\n  path: "/api/tickets",\n  queryParam: "priority",\n};';
W["i2-capstone-contract"] =
  'const createEndpoint = {\n  method: "GET",\n  path: "tickets",\n  successStatus: 302,\n  bodyFields: ["title"],\n};\n\nconst listEndpoint = {\n  method: "POST",\n  path: "tickets",\n  queryParam: 7,\n};';
R["i2-capstone-authz"] =
  'const authz = {\n  authorOnlyEdit: true,\n  serverChecks: true,\n  idSource: "session",\n};';
W["i2-capstone-authz"] =
  'const authz = {\n  authorOnlyEdit: false,\n  serverChecks: false,\n  idSource: "request-body",\n};';
R["i2-capstone-errors"] =
  "const errors = {\n  invalidTicket: 400,\n  notAuthor: 403,\n  notSignedIn: 401,\n  clientValidates: true,\n};";
W["i2-capstone-errors"] =
  "const errors = {\n  invalidTicket: 500,\n  notAuthor: 200,\n  notSignedIn: 400,\n  clientValidates: false,\n};";
R["i2-capstone-states"] =
  "const states = {\n  loading: true,\n  errorState: true,\n  emptyState: true,\n  optimisticWrite: true,\n};";
W["i2-capstone-states"] =
  "const states = {\n  loading: false,\n  errorState: false,\n  emptyState: false,\n  optimisticWrite: false,\n};";
R["i2-capstone-deploy"] =
  'const deploy = {\n  envSecrets: true,\n  migrations: "versioned-scripts",\n  healthEndpoint: "/healthz",\n  buildIsReproducible: true,\n};';
W["i2-capstone-deploy"] =
  'const deploy = {\n  envSecrets: false,\n  migrations: "manual-sql",\n  healthEndpoint: "health",\n  buildIsReproducible: false,\n};';
R["i2-capstone-verification"] =
  "const capstone = {\n  dataModel: true,\n  apiValidates: true,\n  apiAuthorizes: true,\n  asyncStates: true,\n  accessibilityPass: true,\n  testsWritten: true,\n  readme: true,\n};";
W["i2-capstone-verification"] =
  "const capstone = {\n  dataModel: true,\n  apiValidates: false,\n  apiAuthorizes: true,\n  asyncStates: false,\n  accessibilityPass: true,\n  testsWritten: false,\n  readme: true,\n};";
R["i2-delegate-resolve"] =
  'function resolveAction(event, root) {\n  for (let el = event.target; el && el !== root; el = el.parent) {\n    if (el.matches("[data-action]")) return el;\n  }\n  return null;\n}';
W["i2-delegate-resolve"] = "function resolveAction(event, root) { return null; }";
R["i2-action-router"] =
  'function handleClick(event, root, actions) {\n  for (let el = event.target; el && el !== root; el = el.parent) {\n    if (el.matches("[data-action]")) {\n      const name = el.dataset.action;\n      if (typeof actions[name] === "function") {\n        actions[name](el);\n        return name;\n      }\n      return "missing";\n    }\n  }\n  return null;\n}';
W["i2-action-router"] = "function handleClick(event, root, actions) { return null; }";
R["i2-once-handler"] =
  "function once(fn) {\n  let done = false;\n  let result;\n  return (...args) => {\n    if (done) return result;\n    done = true;\n    result = fn(...args);\n    return result;\n  };\n}";
W["i2-once-handler"] = "function once(fn) {\n  return (...args) => fn(...args);\n}";
R["i2-modal-lifecycle"] =
  'function createModal() {\n  let open = false;\n  let previousFocus = null;\n  let root = null;\n  return {\n    open(trigger, panel) {\n      if (open) return "already-open";\n      open = true;\n      previousFocus = trigger;\n      root = panel;\n      return "opened";\n    },\n    close() {\n      if (!open) return "already-closed";\n      open = false;\n      root = null;\n      return previousFocus;\n    },\n    isOpen() {\n      return open;\n    },\n  };\n}';
W["i2-modal-lifecycle"] =
  'function createModal() {\n  return { open() { return "opened"; }, close() { return "closed"; }, isOpen() { return true; } };\n}';
R["i2-accordion"] =
  "function createAccordion(count) {\n  let open = -1;\n  return {\n    toggle(i) {\n      if (i < 0 || i >= count) return;\n      open = open === i ? -1 : i;\n    },\n    isOpen(i) {\n      return open === i;\n    },\n    openCount() {\n      return open === -1 ? 0 : 1;\n    },\n  };\n}";
W["i2-accordion"] =
  "function createAccordion(count) {\n  const states = Array(count).fill(false);\n  return {\n    toggle(i) { states[i] = !states[i]; },\n    isOpen(i) { return states[i]; },\n    openCount() { return states.filter(Boolean).length; },\n  };\n}";
R["i2-validate-field"] =
  'function validateField(name, value) {\n  if (name === "name") {\n    const v = String(value).trim();\n    if (v.length < 2 || v.length > 40) return "name must be 2-40 characters";\n    return null;\n  }\n  if (name === "email") {\n    const s = String(value);\n    const at = s.indexOf("@");\n    if (at <= 0 || at === s.length - 1 || s.indexOf("@", at + 1) !== -1) {\n      return "email must be local@domain";\n    }\n    return null;\n  }\n  if (name === "age") {\n    const n = Number(value);\n    if (!Number.isFinite(n) || n < 16 || n > 120) return "age must be 16-120";\n    return null;\n  }\n  return null;\n}';
W["i2-validate-field"] = "function validateField(name, value) { return null; }";
R["i2-validate-form"] =
  'function validateField(name, value) {\n  if (name === "name") {\n    const v = String(value).trim();\n    if (v.length < 2 || v.length > 40) return "name must be 2-40 characters";\n    return null;\n  }\n  if (name === "email") {\n    const s = String(value);\n    const at = s.indexOf("@");\n    if (at <= 0 || at === s.length - 1 || s.indexOf("@", at + 1) !== -1) {\n      return "email must be local@domain";\n    }\n    return null;\n  }\n  if (name === "age") {\n    const n = Number(value);\n    if (!Number.isFinite(n) || n < 16 || n > 120) return "age must be 16-120";\n    return null;\n  }\n  return null;\n}\nfunction validateForm(values) {\n  const errors = {};\n  for (const [field, value] of Object.entries(values)) {\n    const msg = validateField(field, value);\n    if (msg) errors[field] = msg;\n  }\n  if (\n    "password" in values &&\n    "confirm" in values &&\n    values.password !== values.confirm\n  ) {\n    errors.confirm = "confirm must match password";\n  }\n  return { valid: Object.keys(errors).length === 0, errors };\n}';
W["i2-validate-form"] = "function validateForm(values) {\n  return { valid: true, errors: {} };\n}";
R["i2-row-manager"] =
  "function createRowManager() {\n  let nextId = 1;\n  let rows = [];\n  return {\n    add(label) {\n      const id = nextId++;\n      rows.push({ id, label });\n      return id;\n    },\n    remove(id) {\n      const i = rows.findIndex((r) => r.id === id);\n      if (i === -1) return false;\n      rows.splice(i, 1);\n      return true;\n    },\n    list() {\n      return rows;\n    },\n    move(id, toIndex) {\n      const from = rows.findIndex((r) => r.id === id);\n      if (from === -1) return false;\n      if (toIndex < 0 || toIndex >= rows.length) return false;\n      const [row] = rows.splice(from, 1);\n      rows.splice(toIndex, 0, row);\n      return true;\n    },\n  };\n}";
W["i2-row-manager"] =
  "function createRowManager() {\n  let rows = [];\n  let nextId = 1;\n  return {\n    add(label) { rows.push({ id: 0, label }); return 0; },\n    remove() { return false; },\n    list() { return rows; },\n    move() { return false; },\n  };\n}";
R["i2-url-parse-view"] =
  'function viewFromUrl(url) {\n  const u = new URL(url);\n  const segs = u.pathname.replace(/^\\//, "").split("/").filter(Boolean);\n  const last = segs[segs.length - 1] || "";\n  const id = /^\\d+$/.test(last) ? last : null;\n  const query = {};\n  for (const [k, v] of u.searchParams) query[k] = v;\n  return { route: u.pathname.replace(/^\\//, ""), id, query };\n}';
W["i2-url-parse-view"] =
  'function viewFromUrl(url) {\n  const u = new URL(url);\n  return { route: u.pathname, id: u.pathname.split("/")[1], query: u.search };\n}';
R["i2-history-nav"] =
  "function createHistory() {\n  const stack = [];\n  let idx = -1;\n  return {\n    push(u) { stack.splice(idx + 1); stack.push(u); idx = stack.length - 1; },\n    replace(u) { if (idx >= 0) stack[idx] = u; else stack.push(u); idx = Math.max(idx, 0); },\n    back() { if (idx > 0) { idx--; return stack[idx + 1]; } return null; },\n    canBack() { return idx > 0; },\n    current() { return idx >= 0 ? stack[idx] : null; },\n  };\n}";
W["i2-history-nav"] =
  "function createHistory() {\n  const stack = [];\n  return {\n    push(u) { stack.push(u); },\n    replace(u) { stack.push(u); },\n    back() { return stack.pop() ?? null; },\n    canBack() { return stack.length > 0; },\n    current() { return stack[stack.length - 1] ?? null; },\n  };\n}";
R["i2-debounce-vs-throttle"] =
  "function debounce(fn, wait, clock) {\n  let lastAttempt = -Infinity;\n  return function () {\n    if (clock.now() - lastAttempt >= wait) {\n      lastAttempt = clock.now();\n      fn();\n    } else {\n      lastAttempt = clock.now();\n    }\n  };\n}\n\nfunction throttle(fn, wait, clock) {\n  let lastRun = -Infinity;\n  return function () {\n    if (clock.now() - lastRun >= wait) {\n      lastRun = clock.now();\n      fn();\n    }\n  };\n}";
W["i2-debounce-vs-throttle"] =
  "function debounce(fn, wait, clock) {\n  return function () { fn(); };\n}\n\nfunction throttle(fn, wait, clock) {\n  return function () { fn(); };\n}";
R["i2-lazy-visibility"] =
  "function createLazyLoader() {\n  const seen = new WeakSet();\n  const handlers = new WeakMap();\n  return {\n    observe(el, onLoad) { handlers.set(el, onLoad); },\n    intersect(el) {\n      if (!handlers.has(el) || seen.has(el)) return false;\n      seen.add(el);\n      handlers.get(el)(el);\n      return true;\n    },\n  };\n}";
W["i2-lazy-visibility"] =
  "function createLazyLoader() {\n  const handlers = new WeakMap();\n  return {\n    observe(el, onLoad) { handlers.set(el, onLoad); },\n    intersect(el) {\n      if (handlers.has(el)) { handlers.get(el)(el); return true; }\n      return false;\n    },\n  };\n}";
R["i2-dashboard-render"] =
  'function renderTasks(state) {\n  const weight = { high: 3, medium: 2, low: 1 };\n  const sorted = [...state.tasks].sort((a, b) => {\n    if (a.done !== b.done) return a.done ? 1 : -1;\n    return (weight[b.priority] || 0) - (weight[a.priority] || 0);\n  });\n  return sorted\n    .map((t) => \'<li data-id="\' + t.id + \'"\' + (t.done ? \' class="done"\' : "") + ">" + t.title + "</li>")\n    .join("");\n}\n\nfunction nextId(state) {\n  const max = state.tasks.reduce((m, t) => Math.max(m, Number(t.id)), 0);\n  return String(max + 1);\n}';
W["i2-dashboard-render"] =
  'function renderTasks(state) {\n  return state.tasks\n    .map((t) => \'<li data-id="\' + t.id + \'">" + t.title + "</li>")\n    .join("");\n}\n\nfunction nextId(state) {\n  return String(state.tasks.length + 1);\n}';
R["i2-dashboard-delegate"] =
  "function createDelegator(onToggle) {\n  const items = new Map();\n  return {\n    wire(el, id) { items.set(el, { id, done: false }); },\n    click(target) {\n      const item = items.get(target);\n      if (!item) return false;\n      onToggle(item.id, item.done);\n      item.done = !item.done;\n      return true;\n    },\n  };\n}";
W["i2-dashboard-delegate"] =
  "function createDelegator(onToggle) {\n  const items = new Map();\n  return {\n    wire(el, id) { items.set(el, id); },\n    click(target) {\n      onToggle(items.get(target));\n      return true;\n    },\n  };\n}";
R["i2-modal-lifecycle"] =
  'function createModal() {\n  let open = false;\n  let previousFocus = null;\n  return {\n    open(trigger, panel) {\n      if (open) return "already-open";\n      open = true;\n      previousFocus = trigger;\n      return "opened";\n    },\n    close() {\n      if (!open) return "already-closed";\n      open = false;\n      previousFocus = null;\n      return "closed";\n    },\n    isOpen() { return open; },\n  };\n}';
W["i2-modal-lifecycle"] =
  'function createModal() {\n  let open = false;\n  return {\n    open() { open = true; return "opened"; },\n    close() { open = false; return "closed"; },\n    isOpen() { return open; },\n  };\n}';
R["i2-debounce-vs-throttle"] =
  "function debounce(fn, wait, clock) {\n  let lastAttempt = null;\n  return function () {\n    const now = clock.now();\n    if (lastAttempt !== null && now - lastAttempt >= wait) {\n      fn();\n    }\n    lastAttempt = now;\n  };\n}\n\nfunction throttle(fn, wait, clock) {\n  let lastRun = -Infinity;\n  return function () {\n    const now = clock.now();\n    if (now - lastRun >= wait) {\n      lastRun = now;\n      fn();\n    }\n  };\n}";
W["i2-debounce-vs-throttle"] =
  "function debounce(fn, wait, clock) {\n  return function () { fn(); };\n}\n\nfunction throttle(fn, wait, clock) {\n  return function () { fn(); };\n}";
R["i2-history-nav"] =
  "function createHistory() {\n  const stack = [];\n  let idx = -1;\n  return {\n    push(u) { stack.splice(idx + 1); stack.push(u); idx = stack.length - 1; },\n    replace(u) { if (idx >= 0) stack[idx] = u; else { stack.push(u); idx = stack.length - 1; } },\n    back() { if (idx > 0) { idx--; return stack[idx]; } return null; },\n    canBack() { return idx > 0; },\n    current() { return idx >= 0 ? stack[idx] : null; },\n  };\n}";
W["i2-history-nav"] =
  "function createHistory() {\n  const stack = [];\n  return {\n    push(u) { stack.push(u); },\n    replace(u) { stack.push(u); },\n    back() { return stack.pop() ?? null; },\n    canBack() { return stack.length > 0; },\n    current() { return stack[stack.length - 1] ?? null; },\n  };\n}";
R["i2-modal-lifecycle"] =
  'function createModal() {\n  let open = false;\n  let previousFocus = undefined;\n  return {\n    open(trigger, panel) {\n      if (open) return "already-open";\n      open = true;\n      previousFocus = trigger;\n      return "opened";\n    },\n    close() {\n      if (!open) return "already-closed";\n      open = false;\n      return "closed";\n    },\n    restoreFocus() {\n      const t = previousFocus;\n      previousFocus = undefined;\n      return t;\n    },\n    isOpen() { return open; },\n  };\n}';
W["i2-modal-lifecycle"] =
  'function createModal() {\n  let open = false;\n  return {\n    open() { open = true; return "opened"; },\n    close() { open = false; return "closed"; },\n    isOpen() { return open; },\n  };\n}';
