import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";

const dir =
  "src/content/tracks/web-development/courses/web-development-beginner/modules/html-foundations/lessons/html-forms/challenges";
mkdirSync(dir, { recursive: true });

const labelForRe = (idExpr) =>
  `const labelRe = new RegExp("<label[^>]*for\\\\s*=\\\\s*[\\"']" + ${idExpr} + "[\\"'][^>]*>[\\\\s\\\\S]*?<\\\\/label>", "i");`;

const challenge = {
  id: "build-a-contact-form",
  title: "Real-World: Contact Form for a Small Business",
  prompt:
    'A local business needs a contact form. Build it accessibly.\n\nRequirements:\n- A `<form>` containing the controls.\n- A labeled email input (`type="email"`, with a `<label for>` wired to its `id`, and `required`).\n- A labeled `<select>` with at least two `<option>`s.\n- A labeled `<textarea>` for the message.\n- A `<button type="submit">` with visible text.',
  difficulty: "beginner",
  boilerplate: "<!-- Contact form below -->\n\n",
  tests: [
    {
      name: "has a form",
      code: `if (!/<form[\\s>][\\s\\S]*?<\\/form>/i.test(code)) {
  throw new Error("Wrap the controls in a <form> element.");
}`,
      hint: "Everything a visitor fills in lives inside <form>…</form>.",
    },
    {
      name: "email input has type email and a name",
      code: `const email = code.match(/<input[^>]*type\\s*=\\s*["']email["'][^>]*>/i);
if (!email) {
  throw new Error('Add <input type="email">.');
}
if (!/name\\s*=/i.test(email[0])) {
  throw new Error("The email input needs a name attribute — no name, no data.");
}`,
      hint: '<input type="email" name="email"> — the type gives mobile keyboards the @ key.',
    },
    {
      name: "email input is labeled correctly",
      code: `const email = code.match(/<input[^>]*type\\s*=\\s*["']email["'][^>]*>/i);
if (!email) {
  throw new Error("Add the email input first.");
}
const id = (email[0].match(/id\\s*=\\s*["']([^"']+)["']/i) || [])[1];
if (!id) {
  throw new Error("Give the email input an id so a label can point at it.");
}
${labelForRe('id.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&")')}
if (!labelRe.test(code)) {
  throw new Error("Add <label for=\\"" + id + "\\">Email</label> — every input needs a label.");
}`,
      hint: 'Pair <label for="email"> with the input\'s id="email" — that link is what screen readers announce.',
    },
    {
      name: "email input is required",
      code: `const email = code.match(/<input[^>]*type\\s*=\\s*["']email["'][^>]*>/i);
if (!email || !/required/i.test(email[0])) {
  throw new Error("Make the email input required.");
}`,
      hint: "Add the required attribute to the email input — the browser blocks empty submission.",
    },
    {
      name: "select with options",
      code: `const sel = code.match(/<select[^>]*>[\\s\\S]*?<\\/select>/i);
if (!sel) {
  throw new Error("Add a <select> with a few <option>s.");
}
const opts = (sel[0].match(/<option[\\s>]/gi) || []).length;
if (opts < 2) {
  throw new Error("The <select> needs at least two <option>s.");
}`,
      hint: "<select> wraps <option> elements — one per choice.",
    },
    {
      name: "select has a label",
      code: `const sel = code.match(/<select[^>]*id\\s*=\\s*["']([^"']+)["'][^>]*>/i);
if (!sel) {
  throw new Error("Give the select an id first.");
}
${labelForRe("sel[1]")}
if (!labelRe.test(code)) {
  throw new Error("The select needs a <label for=\\"" + sel[1] + "\\"> too.");
}`,
      hint: 'Selects need labels exactly like inputs: <label for="topic">.',
    },
    {
      name: "textarea with a label",
      code: `const ta = code.match(/<textarea[^>]*id\\s*=\\s*["']([^"']+)["'][^>]*>/i);
if (!ta) {
  throw new Error("Add a <textarea> for the message.");
}
${labelForRe("ta[1]")}
if (!labelRe.test(code)) {
  throw new Error('Label the textarea with <label for="' + ta[1] + '">.');
}`,
      hint: "Multi-line messages belong in <textarea>; give it an id and a matching label.",
    },
    {
      name: "submit button with text",
      code: `const btn = code.match(/<button[^>]*type\\s*=\\s*["']submit["'][^>]*>[\\s\\S]*?<\\/button>/i);
if (!btn) {
  throw new Error('Add <button type="submit">…</button>.');
}
const text = btn[0].replace(/<[^>]+>/g, "").trim();
if (!text) {
  throw new Error("The button needs visible text — screen readers announce it.");
}`,
      hint: '<button type="submit">Send message</button> — real text, not an icon alone.',
    },
  ],
};

writeFileSync(
  path.join(dir, "build-a-contact-form.json"),
  JSON.stringify(challenge, null, 2) + "\n",
);
console.log("wrote build-a-contact-form.json");
