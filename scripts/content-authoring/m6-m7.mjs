/**
 * Author Module 6 (How Modern Websites Work) — 4 lessons, 2 challenges —
 * and Module 7 (Final Project) — 2 lessons, 1 capstone challenge.
 *
 * Escaping-safe convention: NO raw backticks and NO raw "${" in content.
 * Run: node scripts/content-authoring/m6-m7.mjs
 */
import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";

const T = String.fromCharCode(96);
const D = String.fromCharCode(36);

const BASE =
  "src/content/tracks/web-development/courses/web-development-beginner/modules";

function writer(modDir) {
  return {
    writeLesson(id, title, description, minutes, difficulty, challenges, mdx) {
      const lessonDir = path.join(modDir, "lessons", id);
      mkdirSync(lessonDir, { recursive: true });
      writeFileSync(
        path.join(modDir, "lessons", `${id}.json`),
        JSON.stringify(
          { id, title, description, minutes, difficulty, contentPath: `./${id}.mdx`, challenges },
          null,
          2,
        ) + "\n",
      );
      writeFileSync(path.join(modDir, "lessons", `${id}.mdx`), mdx.trimStart() + "\n");
      console.log("lesson:", id);
    },
    writeChallenge(lessonId, challenge) {
      const dir = path.join(modDir, "lessons", lessonId, "challenges");
      mkdirSync(dir, { recursive: true });
      writeFileSync(
        path.join(dir, `${challenge.id}.json`),
        JSON.stringify(challenge, null, 2) + "\n",
      );
      console.log("  challenge:", challenge.id);
    },
  };
}

/* ═════════════════════ MODULE 6 ══════════════════════════════════════ */

const M6 = writer(path.join(BASE, "how-modern-websites-work"));

/* ── 6.1 Frontend, backend, and the request cycle ───────────────────── */

M6.writeLesson(
  "frontend-backend",
  "Frontend, Backend, and the Full Request Cycle",
  "Follow one click through the whole machine: browser, network, server, database — and see where everything you built actually runs.",
  15,
  "intermediate",
  [],
  `
You have built the **frontend** — the code that runs in the browser. Now meet the
rest of the machine.

## The two halves of every site

- **Frontend (client-side):** HTML, CSS, JavaScript — downloaded to *the user's
  browser* and executed there. Everything from Modules 1–4 lives here.
- **Backend (server-side):** code on a server that responds to requests, applies
  rules, and owns the data. Users never see this code.

## One click, end to end

When you press "Buy":

1. The browser sends an **HTTP request** — "POST /checkout" with your cart.
2. The **server** receives it. Backend code runs: check the session, validate the
   cart, compute tax.
3. The server asks the **database** — "save this order" — and waits.
4. The server sends back an HTTP **response** — status, and usually JSON.
5. The browser's JavaScript renders the confirmation.

All of that in a few hundred milliseconds, thousands of times per second, all over
the world.

## Where Code Journey itself fits

When you press **Run** on a challenge: your browser (frontend) posts your code to a
Code Journey server (backend), which stores the job and hands it to a locked-down
execution machine, then returns a verdict your browser displays. You have been
using a full-stack application this whole time — now you can name its parts.

## Why the split matters

The frontend can be *modified* by anyone (open DevTools — every value in it is
yours to inspect). So trust lives on the server: passwords, prices, permissions.
Any site that trusts the browser on important decisions gets broken within minutes.
This single idea explains most security decisions you will ever encounter.

## What you learned

- Frontend runs in the browser; backend runs on the server
- The request cycle: request → server → database → response → render
- Code Journey is itself a full-stack app you have been using
- The browser is untrusted territory — real checks happen server-side

**Next:** the protocol that carries it all — HTTP.
`,
);

/* ── 6.2 HTTP, JSON, and the language of APIs ───────────────────────── */

M6.writeLesson(
  "http-json-apis",
  "HTTP and JSON: The Language Servers Speak",
  "Requests, responses, status codes, headers, and JSON — the vocabulary behind every fetch call you have written.",
  15,
  "intermediate",
  [],
  `
## The request, dissected

~~~text
GET /courses/web-development-beginner HTTP/1.1
Host: codejourney.example
Accept: application/json
~~~

- **Method** — the verb: ${T}GET${T} (read), ${T}POST${T} (create/submit),
  ${T}PUT/PATCH${T} (update), ${T}DELETE${T} (remove)
- **Path** — which resource
- **Headers** — metadata (what formats are accepted, who is calling)

## The response, dissected

~~~text
HTTP/1.1 200 OK
Content-Type: application/json

{"id": "web-development-beginner", "lessons": 62}
~~~

A **status code**, headers, and a body. The families:

- **1xx** informational · **2xx** success · **3xx** redirect
- **4xx** the client's mistake (${T}404${T} not found, ${T}401${T} unauthenticated,
  ${T}403${T} forbidden, ${T}429${T} too many requests)
- **5xx** the server's mistake

You have met several already: Code Journey's run API answers ${T}401${T} when you
are signed out and ${T}429${T} when you exceed the rate limit — now you can read
those like a professional.

## JSON: the data format of the web

**JSON** (JavaScript Object Notation) is text shaped like JavaScript objects —
objects, arrays, strings, numbers, booleans, null. Every language reads it, which
is why APIs everywhere speak it:

~~~js
const text = '{"user":{"name":"Ada","roles":["learner"]}}';
const data = JSON.parse(text);       // string → object
data.user.roles[0];                  // "learner" — navigate like any object

JSON.stringify(data);                // object → string (for sending)
~~~

## Stateless — and why cookies exist

HTTP is **stateless**: every request arrives alone, remembering nothing. So how do
sites keep you logged in? **Cookies** — small pieces of data the browser attaches to
every request to that site. The server reads the cookie, recognizes your
**session**, and treats the request as yours. That single mechanism is how
"stay signed in" works everywhere.

## What you learned

- Requests: method + path + headers; responses: status + headers + body
- Status families; the everyday ones (${T}401${T}, ${T}403${T}, ${T}404${T}, ${T}429${T})
- JSON is the web's data format; ${T}JSON.parse${T}/${T}stringify${T} convert
- Statelessness → cookies → sessions

**Next:** where the data lives — databases.
`,
);

/* ── 6.3 Databases & authentication concepts ────────────────────────── */

M6.writeLesson(
  "databases-and-auth",
  "Databases and Authentication: Where Data Lives",
  "Tables, rows, and queries; hashing, sessions, and why servers — never browsers — guard identity.",
  15,
  "intermediate",
  [],
  `
## The database — the memory

A server can restart any moment; its memory is wiped. Durable data lives in a
**database**. The dominant kind is **relational** — data in **tables** of rows and
columns, linked by ids:

~~~text
users
id | email           | password_hash
1  | ada@example.com | $2b$12$KIX...

submissions
id | user_id | challenge_id | verdict
7  | 1       | render-a-list | passed
~~~

That ${T}user_id${T} column is the link: one user, many submissions. You query with
**SQL**: ${T}SELECT * FROM submissions WHERE user_id = 1;${T}. When Code Journey
shows your submission history, a query exactly like that ran.

## Authentication vs authorization

Two different questions:

- **Authentication** — *who are you?* (login)
- **Authorization** — *what may this account do?* (permissions)

## How login actually works

1. You submit email + password.
2. The server looks up the user and **hashes** the submitted password — a one-way
   mathematical transformation.
3. Hashes match → you are authenticated. The server issues a **session** (often a
   cookie with a random, unguessable id).

**Passwords are never stored** — only their hashes. A one-way hash cannot be
reversed; if the database leaks, attackers get hashes, not passwords. When a site
emails you your actual password in plain text, run.

## Authorization you have already experienced

Code Journey checks authorization on every submission read: user A requesting user
B's result gets ${T}404${T}, even with the right id. The server asked not *does
this submission exist* but *does this submission belong to the requester* — and it
checks on the server, where the answer cannot be forged.

## What you learned

- Relational databases: tables, rows, id links, SQL queries
- Authentication (who) vs authorization (what may they do)
- Passwords are hashed, never stored; sessions keep you logged in
- Ownership checks happen server-side — you lived this with the 404s

**Next:** how sites reach the world — DNS, HTTPS, and deployment.
`,
);

/* ── 6.4 DNS, HTTPS, and the life of a URL ──────────────────────────── */

M6.writeLesson(
  "deployment-dns-https",
  "Deployment, DNS, and HTTPS: The Life of a URL",
  "Type an address, get a page — what actually happens between the enter key and the pixels, and why the little padlock matters.",
  15,
  "intermediate",
  [],
  `
## What happens when you press Enter

1. **DNS lookup.** The browser asks the internet's phonebook: *what is the IP
   address for ${T}example.com${T}?* DNS translates names → numbers, worldwide,
   cached at many layers for speed.
2. **TCP + TLS handshake.** The browser connects to that address and agrees on
   encryption keys with the server.
3. **HTTP request/response.** ${T}GET /${T} comes back as HTML.
4. **The page loads.** The browser parses the HTML, discovers the CSS and
   JavaScript, fetches those, renders — your code from Module 1, in full circle.

## HTTPS — the padlock is non-negotiable

**HTTPS** is HTTP inside TLS encryption. Anything sent over plain HTTP can be read
or modified by anyone between you and the server — passwords, cookies, everything.

HTTPS gives three guarantees: **encryption** (nobody reads the traffic),
**integrity** (nobody modifies it in transit), and **identity** (the certificate
proves the server is who it claims). Certificates are free and automatic in 2026
(Let's Encrypt and every major host) — a site without HTTPS today is a red flag,
full stop.

## How code gets deployed

- **Static sites** (your Modules 1–5 projects): files copied to a CDN-backed host.
  Fast, cheap, ideal when the browser does all the work.
- **Full-stack apps** (like Code Journey): a running server process plus a
  database, deployed to a platform that manages machines, restarts, and scaling.

Either way the rhythm is identical: push code → pipeline deploys it → users get the
new version. You have done the static version already with GitHub Pages.

## The whole picture — and your place in it

DNS turns a name into a machine. HTTP carries a request to it. The server's backend
queries its database and answers in JSON. The browser's frontend renders it. You
have now written the frontend, consumed APIs as a client, and understand the
machinery behind every remaining piece.

**Next:** put all of it together — the final project.
`,
);

M6.writeChallenge("frontend-backend", {
  id: "architecture-sort",
  title: "Sort the Architecture",
  prompt:
    "For each concern, name where it belongs — \"frontend\" or \"backend\":\n\nanswers = { passwordCheck: \"?\", buttonText: \"?\", priceCalculation: \"?\", themeToggle: \"?\", databaseQuery: \"?\" }",
  difficulty: "intermediate",
  boilerplate:
    'const answers = {\n  passwordCheck: "",\n  buttonText: "",\n  priceCalculation: "",\n  themeToggle: "",\n  databaseQuery: "",\n};\n',
  tests: [
    {
      name: "trust lives on the server; presentation in the browser",
      code: `const fn = new Function(code + "\\nreturn { answers };");
const { answers } = fn();
if (answers.passwordCheck !== "backend") throw new Error('passwordCheck: "backend" — the browser can be modified by anyone.');
if (answers.buttonText !== "frontend") throw new Error('buttonText: "frontend" — pure presentation.');
if (answers.priceCalculation !== "backend") throw new Error('priceCalculation: "backend" — never trust prices computed in the browser.');
if (answers.themeToggle !== "frontend") throw new Error('themeToggle: "frontend" — a pure UI concern.');
if (answers.databaseQuery !== "backend") throw new Error('databaseQuery: "backend" — the database is never reachable from the browser.');`,
      hint: "If it involves trust, money, identity, or data — backend. If it is what the user sees and clicks — frontend.",
    },
  ],
});

M6.writeChallenge("http-json-apis", {
  id: "http-status-code-check",
  title: "Read the Status Codes",
  prompt:
    'Match each situation to its HTTP status code:\n\nanswers = { anonymousRun: "?", missingPage: "?", tooManyRequests: "?", allGood: "?" }\n\n- anonymousRun: an anonymous user tries to execute code (the server refuses; not signed in)\n- missingPage: the requested page does not exist\n- tooManyRequests: the client exceeded the rate limit\n- allGood: the request succeeded',
  difficulty: "intermediate",
  boilerplate:
    'const answers = {\n  anonymousRun: 0,\n  missingPage: 0,\n  tooManyRequests: 0,\n  allGood: 0,\n};\n',
  tests: [
    {
      name: "the four everyday codes",
      code: `const fn = new Function(code + "\\nreturn { answers };");
const { answers } = fn();
if (answers.anonymousRun !== 401) throw new Error("anonymousRun: 401 Unauthorized — authentication required.");
if (answers.missingPage !== 404) throw new Error("missingPage: 404 Not Found.");
if (answers.tooManyRequests !== 429) throw new Error("tooManyRequests: 429 Too Many Requests.");
if (answers.allGood !== 200) throw new Error("allGood: 200 OK.");`,
      hint: "401 · 404 · 429 · 200 — you have met every one of these on Code Journey itself.",
    },
  ],
});

/* ═════════════════════ MODULE 7 ══════════════════════════════════════ */

const M7 = writer(path.join(BASE, "final-project"));

/* ── 7.1 Plan the build ─────────────────────────────────────────────── */

M7.writeLesson(
  "capstone-planning",
  "Final Project: Plan Your Website",
  "Choose a real site to build, scope it deliberately, and plan sections, pages, and milestones — the decisions come first.",
  15,
  "intermediate",
  [],
  `
You have built every skill this capstone needs. Now you choose the project — that
choice, and the plan, are the first deliverable.

## Pick your site

Choose something you would actually publish:

- **Personal portfolio** — about you, your work, a contact form
- **Small business site** — a local café, studio, or service: services, gallery,
  contact
- **Community page** — a club, team, or event with schedules and sign-up form

Pick the one you can describe in three sentences. If you cannot, it is too big.

## Scope it deliberately

Every capstone needs, at minimum:

- **3+ sections or pages** (home, about/work, contact)
- **Responsive layout** using Flexbox and/or Grid
- **Accessible forms** (labels, error feedback) with JavaScript validation
- **Real interactivity** — at least: mobile navigation toggle, one stateful feature
  (filter, theme, or list) that persists with localStorage
- **Semantic HTML throughout** — one ${T}h1${T}, landmarks, alt text, contrast

Write these as a checklist *before* coding. This is your acceptance test: the
project is done when the checklist is green, not when you are tired.

## Milestones, not marathons

1. Content and structure — semantic HTML for every section (no styling yet)
2. Layout — responsive with Flexbox/Grid, mobile-first
3. Polish — typography, color system, focus states, transitions
4. Behavior — validation, navigation toggle, your stateful feature
5. Ship — Git history with meaningful commits, deployed, README written

Each milestone ends with something that works. Build in that order — content
before styling before behavior — and you will never stare at a blank page.

**Next:** build it, ship it, and pass the capstone checks.
`,
);

/* ── 7.2 Build, ship, and the capstone check ────────────────────────── */

M7.writeLesson(
  "capstone-build-and-ship",
  "Final Project: Build, Ship, and Verify",
  "The build checklist, the shipping ritual, and the graded capstone verification that crowns the course.",
  20,
  "advanced",
  ["capstone-verification"],
  `
Build milestone by milestone. When the checklist is green, ship:

## The shipping ritual

1. **Git as you go** — a history of meaningful commits tells the story of the
   build; it is also your undo button.
2. **README.md** — what the site is, what it uses, how to view it.
3. **Deploy** — GitHub Pages, as in Module 5. Share the link; a deployed project
   beats a perfect local one every time.

## The pre-flight audit (do this yourself, then the grader checks it too)

- Resize from 375px to desktop — nothing breaks, nothing overflows
- Tab through the whole site — every interactive element reachable, focus visible
- Submit the empty form — clear, text (not color-only) error messages
- Check contrast on every text/background pair
- Run your one stateful feature, reload the page — the state survives

## The capstone verification

The final challenge verifies the *decisions* a real build requires: layout
approach, accessibility behavior, and workflow. It complements — never replaces —
the site itself; the code below encodes the verification so your progress records
the capstone honestly.

Passing it, with a deployed site behind you, you are done: a complete website,
built by you, from nothing.

**Where next:** CSS deep-dives, TypeScript, React, backend with Node — every road
starts from the foundations you now own.
`,
);

M7.writeChallenge("capstone-build-and-ship", {
  id: "capstone-verification",
  title: "Capstone Verification",
  prompt:
    "Verify the decisions your final project encodes. Write one object `capstone` with:\n\n- layout: which CSS layout system(s) your site uses — \"flexbox\", \"grid\", or \"both\"\n- nav: how your navigation adapts on small screens — \"hamburger\", \"stacked\", or \"horizontal\"\n- storageKey: the localStorage key your stateful feature persists under (a string)\n- contrastChecked and keyboardNavigable and formLabeled: booleans confirming you audited each",
  difficulty: "advanced",
  boilerplate:
    'const capstone = {\n  layout: "",\n  nav: "",\n  storageKey: "",\n  contrastChecked: false,\n  keyboardNavigable: false,\n  formLabeled: false,\n};\n',
  tests: [
    {
      name: "a deliberate layout and responsive nav decision",
      code: `const fn = new Function(code + "\\nreturn { capstone };");
const { capstone } = fn();
if (!["flexbox", "grid", "both"].includes(capstone.layout)) {
  throw new Error('layout must be "flexbox", "grid", or "both" — your site must use one of them.');
}
if (!["hamburger", "stacked", "horizontal"].includes(capstone.nav)) {
  throw new Error('nav must be "hamburger", "stacked", or "horizontal" — name your real approach.');
}`,
      hint: "Layout: what did you actually build with? Nav: what actually happens under 768px?",
    },
    {
      name: "stateful feature persists under a named key",
      code: `const fn = new Function(code + "\\nreturn { capstone };");
const { capstone } = fn();
if (typeof capstone.storageKey !== "string" || capstone.storageKey.length < 3) {
  throw new Error("storageKey must be the real localStorage key your feature uses (at least 3 characters).");
}`,
      hint: "Whatever you call JSON.stringify(localStorage.getItem(...)) with — e.g. \"tasks\" or \"theme\".",
    },
    {
      name: "the accessibility audit was real",
      code: `const fn = new Function(code + "\\nreturn { capstone };");
const { capstone } = fn();
for (const key of ["contrastChecked", "keyboardNavigable", "formLabeled"]) {
  if (capstone[key] !== true) {
    throw new Error(key + " must be true — do the audit first: contrast pairs, keyboard-only pass, labels on every control.");
  }
}`,
      hint: "Tab through the site, submit the empty form, check contrast — then set all three to true.",
    },
  ],
});
