/**
 * Author Module 5 (Developer Tools, Git & GitHub) — 6 lessons, 6 challenges.
 *
 * Terminal + Git challenges grade terminal/git workflow KNOWLEDGE via
 * multiple-choice-style value comparisons and command-sequence checks that do
 * not require git to be installed in the sandbox.
 *
 * Escaping-safe convention: NO raw backticks and NO raw "${" in content.
 * Run: node scripts/content-authoring/m5.mjs
 */
import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";

const T = String.fromCharCode(96);

const DIR =
  "src/content/tracks/web-development/courses/web-development-beginner/modules/developer-tools-git-and-github/lessons";

function writeLesson(id, title, description, minutes, difficulty, challenges, mdx) {
  const lessonDir = path.join(DIR, id);
  mkdirSync(lessonDir, { recursive: true });
  writeFileSync(
    path.join(DIR, `${id}.json`),
    JSON.stringify(
      { id, title, description, minutes, difficulty, contentPath: `./${id}.mdx`, challenges },
      null,
      2,
    ) + "\n",
  );
  writeFileSync(path.join(DIR, `${id}.mdx`), mdx.trimStart() + "\n");
  console.log("lesson:", id);
}

function writeChallenge(lessonId, challenge) {
  const dir = path.join(DIR, lessonId, "challenges");
  mkdirSync(dir, { recursive: true });
  writeFileSync(path.join(dir, `${challenge.id}.json`), JSON.stringify(challenge, null, 2) + "\n");
  console.log("  challenge:", challenge.id);
}

/* ── 5.1 The terminal ───────────────────────────────────────────────── */

writeLesson(
  "terminal-basics",
  "The Terminal: Talking to Your Computer Directly",
  "The command line is how developers drive tools like Git. Learn the handful of commands that cover everyday work.",
  12,
  "beginner",
  ["terminal-commands"],
  `
Graphical file managers show folders as icons. The **terminal** shows the same
filesystem as text — and lets you act on it with short commands. It looks
intimidating and is actually the most predictable tool you will ever use.

## The prompt and the working directory

Every terminal has a **working directory** — the folder you are currently "in".
${T}pwd${T} (print working directory) shows where you are:

~~~text
$ pwd
/Users/ada/projects
~~~

## The five commands that matter

~~~text
pwd               # where am I?
ls                # list files here
cd my-project     # change directory — into my-project
cd ..             # back up one level
mkdir new-site    # make a new folder
~~~

Windows' CMD/PowerShell uses ${T}dir${T} instead of ${T}ls${T}; everything else
here works the same.

## Paths: absolute vs relative

- **Relative** (${T}cd projects${T}) — from where you are now
- **Absolute** (${T}cd /Users/ada/projects${T}) — from the root of the disk

${T}.${T} means "this folder" and ${T}..${T} means "the parent" —
${T}cd ..${T} climbs one level, ${T}./index.html${T} points at a file here.

## Creating files and running programs

~~~text
touch notes.txt       # create an empty file
node script.js        # run a program with an argument
git status            # another program: Git (next lesson)
~~~

The pattern is always: program name, then arguments. You already know this shape
from ${T}console.log${T} — the terminal is just a bigger version.

## What you learned

- The terminal is a text view of the same filesystem
- ${T}pwd${T}, ${T}ls${T}, ${T}cd${T}, ${T}mkdir${T}, ${T}touch${T}
- Relative vs absolute paths; ${T}.${T} and ${T}..${T}
- Every command is a program plus arguments

**Next:** version control — why every line of code deserves an undo button.
`,
);

writeChallenge("terminal-basics", {
  id: "terminal-commands",
  title: "Command the Terminal",
  prompt:
    'Match each task to its command — write your answers as a single object assigned to `answers`:\n\nanswers = { where: "?", list: "?", enter: "?", up: "?", makeFolder: "?" }\n\n- where: show the current directory\n- list: list the files here\n- enter: move into a folder called my-project\n- up: move back up one level\n- makeFolder: create a folder called notes',
  difficulty: "beginner",
  boilerplate:
    'const answers = {\n  where: "",\n  list: "",\n  enter: "",\n  up: "",\n  makeFolder: "",\n};\n',
  tests: [
    {
      name: "the five core commands",
      code: `const fn = new Function(code + "\\nreturn { answers };");
const { answers } = fn();
if (answers.where !== "pwd") throw new Error('where: "pwd" prints the working directory.');
if (answers.list !== "ls") throw new Error('list: "ls" lists files (dir on Windows CMD).');
if (answers.enter !== "cd my-project") throw new Error('enter: "cd my-project" moves into the folder.');
if (answers.up !== "cd ..") throw new Error('up: "cd .." climbs one level.');
if (answers.makeFolder !== "mkdir notes") throw new Error('makeFolder: "mkdir notes" creates the folder.');`,
      hint: "pwd · ls · cd my-project · cd .. · mkdir notes",
    },
  ],
});

/* ── 5.2 Git: what and why ──────────────────────────────────────────── */

writeLesson(
  "git-version-control",
  "Git: A Time Machine for Your Code",
  "Version control explained from zero: repositories, commits, and the everyday add/commit/status rhythm.",
  16,
  "beginner",
  ["git-init-and-commit"],
  `
**Git** records snapshots of your project so you can look back, undo, and
collaborate. Without it, developers emailed folders named
${T}final-v3-REAL.zip${T}. With it, every state of your project is one command away.

## The repository

A **repository** ("repo") is a folder Git watches. Turn any project into a repo:

~~~text
git init
~~~

This creates a hidden ${T}.git${T} folder — the time machine itself. Your files do
not change; Git just starts paying attention.

## The three places your code lives

1. **Working directory** — the files you edit
2. **Staging area** — changes chosen for the next snapshot
3. **Repository history** — the permanent snapshots ("commits")

~~~text
git status          # what has changed? what is staged?
git add index.html  # stage one file
git add .           # stage everything changed
git commit -m "Add navigation bar"    # snapshot the staged changes
~~~

## Commits are checkpoints, not backups

A **commit** is a named snapshot with a message explaining *why*. Good messages
complete the sentence "This commit will…":

~~~text
git commit -m "Fix broken link in the footer"     ✓
git commit -m "stuff"                              ✗ future-you will hate this
~~~

Small, frequent commits turn big changes into a readable story — and give you
dozens of restore points.

## Looking back

~~~text
git log --oneline   # the history, one line per commit
~~~

Made a mess before committing? ${T}git status${T} tells you the state; the history
keeps everything safe that you did commit. This course's own repo has dozens of
commits — run ${T}git log --oneline${T} on any real project and read it like a diary.

## What you learned

- ${T}git init${T} starts the time machine
- edit → ${T}git status${T} → ${T}git add${T} → ${T}git commit -m${T}
- Commit messages explain *why*, in present tense
- ${T}git log${T} reads the history

**Next:** branches — experiment without breaking the main line.
`,
);

writeChallenge("git-git-version-control", {
  id: "git-init-and-commit",
  title: "The Everyday Git Rhythm",
  prompt:
    'Write a function `commitSequence()` that RETURNS an array of git commands — in order — for this situation: you just created a new project folder, and you have finished your first page and want to record it.\n\nInclude exactly: initializing the repo, checking the state, staging everything, and committing with the message "First page".',
  difficulty: "beginner",
  boilerplate: "// commitSequence() returns the 4 git commands in order\n",
  tests: [
    {
      name: "the four commands in order",
      code: `const fn = new Function(code + "\\nreturn { commitSequence };");
const { commitSequence } = fn();
const seq = commitSequence();
if (!Array.isArray(seq) || seq.length !== 4) {
  throw new Error("Return an array of exactly 4 commands.");
}
const j = seq.map((s) => String(s).trim());
if (j[0] !== "git init") throw new Error("Step 1 is git init.");
if (j[1] !== "git status") throw new Error("Step 2 is git status — look before you leap.");
if (j[2] !== "git add .") throw new Error("Step 3 is git add . to stage everything.");
if (!/^git commit -m ['\\"]First page['\\"]$/.test(j[3])) {
  throw new Error('Step 4 is git commit -m "First page" — messages go in quotes.');
}`,
      hint: '["git init", "git status", "git add .", "git commit -m \\"First page\\""]',
    },
  ],
});

/* ── 5.3 Branches & merging ─────────────────────────────────────────── */

writeLesson(
  "git-branches",
  "Branches: Experiment Without Breaking Things",
  "Branches let you try ideas in a parallel sandbox and merge them back when they work — how teams (and careful solo developers) work.",
  16,
  "beginner",
  ["branch-workflow"],
  `
A **branch** is a parallel line of history. The default branch — usually
${T}main${T} — is the stable version. A new branch is a safe sandbox: experiment
freely; ${T}main${T} never notices until you merge.

## The workflow

~~~text
git branch about-page        # create a branch named about-page
git switch about-page        # move onto it (git switch -c about-page = both steps)
...edit files, add, commit...
git switch main              # back to the stable line
git merge about-page         # bring the branch's work into main
~~~

While on ${T}about-page${T}, commits land on that branch. ${T}main${T} stays
untouched — that is the entire point.

## Resolving a basic conflict

A **conflict** happens when two branches change the same lines. Git marks the
collision in the file itself:

~~~text
<<<<<<< HEAD
Welcome to my site
=======
Welcome — come on in
>>>>>>> about-page
~~~

You resolve it by editing the file to the version you want (or a blend), removing
the ${T}<<<<<<<${T} markers, then ${T}git add${T} + ${T}git commit${T}. Conflicts
are not errors — they are Git asking you to make a decision it refuses to guess.

## Real habits

- One branch per idea or feature; short-lived branches merge cleanly
- Never commit straight to main in a team repo — branch, even alone, for practice
- ${T}git branch${T} lists branches; ${T}git log --oneline --all${T} shows every line

## What you learned

- ${T}git branch${T}/${T}git switch${T} create and enter sandboxes
- Merge brings completed work back into main
- Conflicts are decisions, not failures — edit, add, commit

**Next:** taking your repositories online — GitHub.
`,
);

writeChallenge("git-branches", {
  id: "branch-workflow",
  title: "Feature Branch Workflow",
  prompt:
    'Write `branchWorkflow()` returning an object describing this flow: create a branch named "feature/faq", switch to it, then — after finishing work — bring it into main.\n\nShape: { create: "?", switch: "?", merge: "?" } (run from main, merge into main).',
  difficulty: "beginner",
  boilerplate: 'const branchWorkflow = () => ({\n  create: "",\n  switch: "",\n  merge: "",\n});\n',
  tests: [
    {
      name: "create, switch, merge — with the right branch name",
      code: `const fn = new Function(code + "\\nreturn { branchWorkflow };");
const { branchWorkflow } = fn();
const w = branchWorkflow();
if (w.create !== "git branch feature/faq") throw new Error("create: git branch feature/faq");
if (w.switch !== "git switch feature/faq") throw new Error("switch: git switch feature/faq");
if (w.merge !== "git merge feature/faq") throw new Error("merge (from main): git merge feature/faq");`,
      hint: "git branch feature/faq · git switch feature/faq · git merge feature/faq",
    },
  ],
});

/* ── 5.4 GitHub ─────────────────────────────────────────────────────── */

writeLesson(
  "github-remote",
  "GitHub: Your Code, Online",
  "Push your repository to GitHub so it is backed up, shareable, and open for collaboration — the remote in every developer's workflow.",
  16,
  "beginner",
  ["push-to-github"],
  `
Git is local; **GitHub** hosts Git repositories online. The online copy is called a
**remote**. Publishing your repo gives you backup, a portfolio, and collaboration —
every job application you will ever make starts with a link to your GitHub.

## Connect and push

After creating an empty repo on github.com (the site shows you these exact
commands):

~~~text
git remote add origin https://github.com/ada/my-site.git
git push -u origin main
~~~

- ${T}origin${T} is the conventional nickname for your remote
- ${T}push${T} uploads commits; ${T}-u${T} remembers the pairing so future pushes
  are just ${T}git push${T}

## The daily cycle with a remote

~~~text
git pull            # fetch + merge anything new from the remote
...work, add, commit...
git push            # share your commits
~~~

${T}clone${T} is the reverse of remote-add: it downloads an existing repo with its
full history — ${T}git clone <url>${T} is how you join any project.

## README, issues, pull requests

- **README.md** — the repo's front page: what it is, how to run it
- **Issues** — a to-do list of bugs and ideas
- **Pull request (PR)** — "please merge my branch": the review-and-discussion step
  every team uses. On your own repos, open PRs to yourself for practice; reading
  diffs is a skill worth building early.

## What you learned

- A remote is your repo hosted online; ${T}origin${T} by convention
- ${T}push${T} uploads, ${T}pull${T} downloads, ${T}clone${T} starts fresh
- README, issues, and PRs are how real projects communicate

**Next:** putting a real site on the internet — GitHub Pages.
`,
);

writeChallenge("github-remote", {
  id: "push-to-github",
  title: "Publish to a Remote",
  prompt:
    "Your local repo is ready. Write `publishCommands()` returning an array with, in order: the command that connects a remote at https://github.com/ada/my-site.git, the command that uploads main and remembers the pairing, and the command your teammate uses to download the whole repo fresh.",
  difficulty: "beginner",
  boilerplate: "// publishCommands() returns the 3 commands in order\n",
  tests: [
    {
      name: "remote add, push -u, clone",
      code: `const fn = new Function(code + "\\nreturn { publishCommands };");
const { publishCommands } = fn();
const cmds = publishCommands().map((s) => String(s).trim());
if (cmds.length !== 3) throw new Error("Return exactly 3 commands.");
if (!cmds[0].startsWith("git remote add origin https://github.com/ada/my-site.git")) {
  throw new Error("First: git remote add origin <url>.");
}
if (!cmds[1].startsWith("git push -u origin main")) {
  throw new Error("Second: git push -u origin main.");
}
if (!cmds[2].startsWith("git clone https://github.com/ada/my-site.git")) {
  throw new Error("Third: your teammate clones the same URL with git clone.");
}`,
      hint: "git remote add origin <url> · git push -u origin main · git clone <url>",
    },
  ],
});

/* ── 5.5 Deploying with GitHub Pages ────────────────────────────────── */

writeLesson(
  "deploy-github-pages",
  "Deploy: Put Your Site on the Internet",
  "Turn a GitHub repository into a live, shareable URL with GitHub Pages — your first real deployment.",
  14,
  "intermediate",
  ["deploy-checklist"],
  `
A website on your laptop is a rehearsal. **Deployment** copies it to a server so
the world can visit. GitHub Pages deploys straight from a repository — free, and
perfect for the static sites you build in this course.

## Deploying a repo with Pages

1. Push your project to GitHub (previous lesson)
2. Repo → Settings → Pages
3. Source: "Deploy from a branch" → branch ${T}main${T}, folder ${T}/ (root)
4. Save — within minutes your site is live at
   ${T}https://your-name.github.io/my-site/${T}

Every push to main redeploys automatically. Deployment becomes a side effect of
committing — that habit scales all the way to professional teams.

## What works on Pages — and what does not

Works: HTML, CSS, and client-side JavaScript (everything from Modules 1–4).

Does not: server-side code. Pages serves files; it cannot run a database or a
Node server. That is what full hosting platforms are for — a natural next step
after this course, not a mystery.

## Deploy checklist (catch the classic breakages)

- **Paths are case-sensitive** on the server: ${T}Logo.PNG${T} ≠ ${T}logo.png${T}
- Use **relative paths** (${T}./styles.css${T}) — absolute paths like
  ${T}/Users/ada/...${T} only exist on your machine
- Test in a private/incognito window — caches lie

## What you learned

- Deployment = copying your site to a server the world can reach
- GitHub Pages deploys from a branch and redeploys on every push
- Static hosting serves files; servers and databases need full hosting
- Relative paths + exact case = the two classic deploy bugs

**Next:** wrap up the module with a checkpoint and a real publication.
`,
);

writeChallenge("deploy-github-pages", {
  id: "deploy-checklist",
  title: "Ship It — Deploy Decisions",
  prompt:
    'A learner pushed their site but visitors see a broken layout with no styles. The site is at github.io/my-site/ and the HTML contains <link rel="stylesheet" href="/Users/ada/site/styles.css">.\n\nWrite `fix()` returning an object: { problem: "paths" | "case" | "server", fix: "<the corrected link tag>" }.',
  difficulty: "intermediate",
  boilerplate: 'const fix = () => ({\n  problem: "",\n  fix: "",\n});\n',
  tests: [
    {
      name: "diagnosis and the corrected tag",
      code: `const fn = new Function(code + "\\nreturn { fix };");
const { fix } = fn();
const out = fix();
if (out.problem !== "paths") {
  throw new Error('The absolute path only exists on the learner\\'s machine — problem is "paths".');
}
if (!/<link[^>]*href\\s*=\\s*['\\"]\\.\\/styles\\.css['\\"]/.test(out.fix) && !/<link[^>]*href\\s*=\\s*['\\"]styles\\.css['\\"]/.test(out.fix)) {
  throw new Error("The fix should use a relative path, e.g. <link rel=\\"stylesheet\\" href=\\"./styles.css\\">.");
}`,
      hint: 'problem: "paths", fix: <link rel="stylesheet" href="./styles.css">',
    },
  ],
});

/* ── 5.6 Checkpoint ─────────────────────────────────────────────────── */

writeLesson(
  "git-checkpoint",
  "Checkpoint: Developer Workflow",
  "Prove the developer-tooling fundamentals: terminal, commits, branches, remotes, and deployment.",
  12,
  "intermediate",
  ["workflow-checkpoint"],
  `
The **Git checkpoint** — five questions spanning the whole module. Concept checks,
a command sequence, and one debugging scenario. This is exactly the workflow you
will use on your final project, so get it fluent now.

**After passing:** how modern websites actually work — the architecture tour.
`,
);

writeChallenge("git-checkpoint", {
  id: "workflow-checkpoint",
  title: "Developer Workflow Check",
  prompt:
    'Answer three scenario questions in one object `answers`:\n\n1. undoTarget: You committed a bug and want to return the project to the previous commit\'s state. Which command family restores a past commit? Answer "checkout", "revert", or "log".\n2. safeShare: You want to propose a change to a teammate\'s repo through review. Answer "push", "pull request", or "issue".\n3. stage: Which command moves your edits into the staging area (one word, no arguments)?',
  difficulty: "intermediate",
  boilerplate: 'const answers = {\n  undoTarget: "",\n  safeShare: "",\n  stage: "",\n};\n',
  tests: [
    {
      name: "concept answers",
      code: `const fn = new Function(code + "\\nreturn { answers };");
const { answers } = fn();
if (answers.undoTarget !== "revert") throw new Error('undoTarget: "revert" creates a commit that undoes a past one — the safe history-respecting choice.');
if (answers.safeShare !== "pull request") throw new Error('safeShare: a "pull request" opens your branch for review and merge.');
if (answers.stage !== "add") throw new Error('stage: "git add" moves edits into the staging area.');`,
      hint: "revert · pull request · add",
    },
  ],
});
