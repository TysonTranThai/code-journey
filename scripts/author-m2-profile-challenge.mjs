import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";

const dir =
  "src/content/tracks/web-development/courses/web-development-beginner/modules/html-foundations/lessons/personal-profile-project/challenges";
mkdirSync(dir, { recursive: true });

const challenge = {
  id: "personal-profile-page",
  title: "Build Your Profile Page",
  prompt:
    "Build your personal profile page from the project brief: complete document, header with one <h1> (your name), nav with fragment links, main with About / Hobbies / Gallery / Contact sections, labeled email form, and a footer. Content is yours — structure is graded.",
  difficulty: "beginner",
  boilerplate: "<!-- Your profile page -->\n\n",
  tests: [
    {
      name: "complete document skeleton",
      code: `if (!/<!DOCTYPE\\s+html>/i.test(code)) {
  throw new Error("Start with <!DOCTYPE html>.");
}
if (!/<html[^>]*\\slang\\s*=/i.test(code)) {
  throw new Error("<html> needs a lang attribute.");
}
if (!/<meta[^>]*charset/i.test(code)) {
  throw new Error('The head needs <meta charset="UTF-8">.');
}
const t = code.match(/<title>([\\s\\S]*?)<\\/title>/i);
if (!t || !t[1].trim()) {
  throw new Error("Add a non-empty <title>.");
}`,
      hint: "Same skeleton as your first page: doctype, html lang, head (charset + title), body.",
    },
    {
      name: "header with exactly one h1",
      code: `const h1s = (code.match(/<h1[\\s>]/gi) || []).length;
if (h1s !== 1) {
  throw new Error("Exactly one <h1> — your name (found " + h1s + ").");
}
const header = code.match(/<header[\\s>][\\s\\S]*?<\\/header>/i);
if (!header || !/<h1/i.test(header[0])) {
  throw new Error("Put your name's <h1> inside a <header>.");
}`,
      hint: "<header> opens the page; your name is the one <h1>.",
    },
    {
      name: "nav with fragment links",
      code: `const nav = code.match(/<nav[\\s>][\\s\\S]*?<\\/nav>/i);
if (!nav) {
  throw new Error("Add a <nav>.");
}
const fragLinks = nav[0].match(/href\\s*=\\s*["']#[^"']+["']/gi) || [];
if (fragLinks.length < 2) {
  throw new Error('The nav needs at least two fragment links (href="#about" style).');
}
const ids = [...code.matchAll(/id\\s*=\\s*["']([^"']+)["']/gi)].map((m) => m[1]);
for (const href of fragLinks) {
  const target = href.replace(/href\\s*=\\s*["']#/, "").replace(/["']/g, "");
  if (!ids.includes(target)) {
    throw new Error("Nav link #" + target + " has no element with that id.");
  }
}`,
      hint: 'Each nav link points at an id on the page: <a href="#about"> needs id="about" somewhere.',
    },
    {
      name: "main with About, Hobbies, Gallery sections",
      code: `const main = code.match(/<main[\\s>][\\s\\S]*?<\\/main>/i);
if (!main) {
  throw new Error("Wrap the content sections in a <main>.");
}
const lower = main[0].toLowerCase();
if (!/<section[\\s>][\\s\\S]*?<h2[\\s\\S]*?<\\/section>/i.test(main[0])) {
  throw new Error("Sections must each carry an <h2> heading.");
}
if (!lower.includes("about")) throw new Error("Add an About section (an id or heading containing 'about').");
if (!lower.includes("hobb")) throw new Error("Add a Hobbies section (an id or heading containing 'hobbies').");
if (!lower.includes("galler")) throw new Error("Add a Gallery section (an id or heading containing 'gallery').");`,
      hint: "Three sections with h2 headings and ids: about, hobbies, gallery.",
    },
    {
      name: "image with meaningful alt",
      code: `const main = code.match(/<main[\\s>][\\s\\S]*?<\\/main>/i) ?? code;
const imgs = main.match(/<img[^>]*>/gi) || [];
if (imgs.length === 0) {
  throw new Error("The gallery needs at least one <img>.");
}
for (const img of imgs) {
  const alt = (img.match(/alt\\s*=\\s*["']([^"']*)["']/i) || [])[1];
  if (alt === undefined || alt.trim().length < 4) {
    throw new Error("Every image needs meaningful alt text (4+ characters describing the picture).");
  }
}`,
      hint: "alt describes the picture's content — what would a visitor miss if it did not load?",
    },
    {
      name: "contact form with labeled email",
      code: `const form = code.match(/<form[\\s>][\\s\\S]*?<\\/form>/i);
if (!form) {
  throw new Error("Add a <form> in the contact section.");
}
if (!/<input[^>]*type\\s*=\\s*["']email["']/i.test(form[0])) {
  throw new Error("The form needs an email input.");
}
const input =
  form[0].match(/<input[^>]*type\\s*=\\s*["']email["'][^>]*id\\s*=\\s*["']([^"']+)["'][^>]*>/i) ??
  form[0].match(/<input[^>]*id\\s*=\\s*["']([^"']+)["'][^>]*type\\s*=\\s*["']email["'][^>]*>/i);
if (!input) {
  throw new Error("Give the email input an id.");
}
const labelRe = new RegExp("<label[^>]*for\\\\s*=\\\\s*[\\"']" + input[1] + "[\\"']", "i");
if (!labelRe.test(code)) {
  throw new Error('Label the email input with <label for="' + input[1] + '">.');
}
if (!/<button[^>]*type\\s*=\\s*["']submit["'][^>]*>[^<]*\\S/i.test(form[0])) {
  throw new Error("Add a submit button with visible text.");
}`,
      hint: "From the forms lesson: input type=email + id, <label for>, button type=submit.",
    },
    {
      name: "footer and clean heading levels",
      code: `if (!/<footer[\\s>][\\s\\S]*?<\\/footer>/i.test(code)) {
  throw new Error("Add a <footer> with a copyright line.");
}
const levels = [...code.matchAll(/<h([1-6])[\\s>]/gi)].map((m) => Number(m[1]));
let prev = 0;
for (const level of levels) {
  if (level > prev + 1) {
    throw new Error("Heading levels must not skip (h" + prev + " followed by h" + level + ").");
  }
  prev = level;
}`,
      hint: "The outline rule: each heading steps down at most one level from the one before.",
    },
  ],
};

writeFileSync(path.join(dir, "personal-profile-page.json"), JSON.stringify(challenge, null, 2) + "\n");
console.log("wrote personal-profile-page.json");
