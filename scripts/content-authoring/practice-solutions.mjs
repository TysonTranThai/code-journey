/**
 * Practice-challenge solutions (Course 1 revision). Appended by the
 * content-authoring scripts; imported by verify-challenges.mjs.
 */
export const R = {};
export const W = {};
R["practice-basic-selectors"] =
  "<style>\np {\n  color: dimgray;\n}\n\n.note {\n  background-color: lightyellow;\n}\n\n#tagline {\n  font-style: italic;\n}\n</style>";
W["practice-basic-selectors"] = "p { color: dimgray; }";
R["practice-descendant-selector"] =
  "<style>\nnav a {\n  color: teal;\n  text-decoration: none;\n}\n</style>";
W["practice-descendant-selector"] = "a { color: teal; text-decoration: none; }";
R["practice-override-one-heading"] =
  '<style>\nh2 {\n  color: seagreen;\n}\n\n#featured {\n  color: crimson;\n}\n</style>\n\n<h2>Fresh bread</h2>\n<h2 id="featured">Sourdough of the week</h2>\n<h2>Croissants</h2>';
W["practice-override-one-heading"] = "h2 { color: seagreen; }\nh2 { color: crimson; }";
R["practice-card-spacing"] =
  '<style>\n.card {\n  padding: 1.5rem;\n  border: 1px solid silver;\n  margin: 1rem 0;\n  border-radius: 8px;\n}\n</style>\n\n<div class="card">A cozy little card</div>';
W["practice-card-spacing"] = ".card { padding: 10px; }";
R["practice-border-box-reset"] =
  '<style>\n*, *::before, *::after {\n  box-sizing: border-box;\n}\n\n.box {\n  width: 200px;\n  padding: 20px;\n  border: 4px solid dimgray;\n}\n</style>\n\n<div class="box">200 means 200</div>';
W["practice-border-box-reset"] = ".box { box-sizing: border-box; }";
R["practice-margin-cleanup"] =
  '<style>\n.card {\n  width: 200px;\n  background: lavender;\n}\n\n.card + .card {\n  margin-left: 1rem;\n}\n</style>\n\n<div class="card">One</div>\n<div class="card">Two</div>';
W["practice-margin-cleanup"] = ".card { margin-right: 2rem; }";
R["practice-flex-center-card"] =
  "<style>\n.stage {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  min-height: 100vh;\n}\n</style>";
W["practice-flex-center-card"] = ".stage { display: block; }";
R["practice-flex-navbar"] =
  "<style>\n.nav {\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n}\n\n.nav ul {\n  display: flex;\n  gap: 1rem;\n  list-style: none;\n}\n</style>";
W["practice-flex-navbar"] = ".nav { display: flex; }\n.nav ul { list-style: none; }";
R["practice-flex-card-row"] =
  "<style>\n.row {\n  display: flex;\n  flex-wrap: wrap;\n  gap: 1rem;\n}\n\n.card {\n  flex: 1;\n  min-width: 200px;\n}\n</style>";
W["practice-flex-card-row"] = ".row { display: flex; }\n.card { width: 200px; }";
R["practice-grid-gallery"] =
  "<style>\n.gallery {\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  gap: 1rem;\n}\n</style>";
W["practice-grid-gallery"] = ".gallery { display: flex; gap: 1rem; }";
R["practice-grid-feature"] =
  "<style>\n.gallery {\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  gap: 1rem;\n}\n\n.featured {\n  grid-column: 1 / -1;\n}\n</style>";
W["practice-grid-feature"] =
  ".gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }\n.featured { grid-column: 1 / 2; }";
R["practice-grid-auto-fit"] =
  "<style>\n.gallery {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));\n  gap: 1rem;\n}\n</style>";
W["practice-grid-auto-fit"] =
  ".gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }";
R["practice-responsive-columns"] =
  "<style>\n.cards {\n  display: grid;\n  grid-template-columns: 1fr;\n  gap: 1rem;\n}\n\n@media (min-width: 640px) {\n  .cards {\n    grid-template-columns: repeat(2, 1fr);\n  }\n}\n\n@media (min-width: 1024px) {\n  .cards {\n    grid-template-columns: repeat(3, 1fr);\n  }\n}\n</style>";
W["practice-responsive-columns"] =
  "@media (max-width: 640px) { .cards { grid-template-columns: repeat(2, 1fr); } }";
R["practice-fluid-images"] = "<style>\nimg {\n  max-width: 100%;\n  height: auto;\n}\n</style>";
W["practice-fluid-images"] = "img { width: 100%; }";
R["practice-readable-body"] =
  '<style>\nbody {\n  font-family: Georgia, "Times New Roman", serif;\n  line-height: 1.6;\n}\n\nmain {\n  max-width: 60ch;\n  margin-inline: auto;\n}\n</style>';
W["practice-readable-body"] = "body { font-family: Arial; }";
R["practice-type-scale"] =
  "<style>\nh1 {\n  font-size: 2.5rem;\n}\n\nh2 {\n  font-size: 1.5rem;\n}\n\n.small {\n  font-size: 0.875rem;\n}\n</style>";
W["practice-type-scale"] = "h1 { font-size: 12px; }";
R["practice-const-vs-let"] =
  'const firstName = "Ada";\nlet score = 0;\nscore = 42;\nconsole.log(`${firstName}: ${score}`);';
W["practice-const-vs-let"] = 'var firstName = "Ada";\nvar score = 0;';
R["practice-shopping-total"] =
  "const price = 4.5;\nconst quantity = 3;\nconst total = price * quantity;\nconsole.log(`${quantity} items cost ${total}`);\nconsole.log(total > 10);";
W["practice-shopping-total"] = "const total = 13.5;";
R["practice-grade-gates"] =
  'function grade(score) {\n  if (score >= 90) return "A";\n  else if (score >= 80) return "B";\n  else return "Keep practicing";\n}\nconsole.log(grade(92));\nconsole.log(grade(55));';
W["practice-grade-gates"] = 'function grade(score) { return "A"; }';
R["practice-refactor-branches"] =
  'function temp(score) {\n  if (score >= 80) {\n    return "hot";\n  } else if (score >= 60) {\n    return "warm";\n  } else {\n    return "cold";\n  }\n}\nconsole.log(temp(85));';
W["practice-refactor-branches"] =
  'function temp(score) { if (score >= 60) { return "warm"; } else if (score >= 80) { return "hot"; } else { return "cold"; } }';
R["practice-countdown-loop"] =
  "function sumUpTo(n) {\n  let total = 0;\n  for (let i = 1; i <= n; i++) {\n    total += i;\n  }\n  return total;\n}\nconsole.log(sumUpTo(10));\nconsole.log(sumUpTo(100));";
W["practice-countdown-loop"] = "function sumUpTo(n) { return 55; }";
R["practice-loop-string-builder"] =
  'function stars(rows) {\n  let out = "";\n  for (let i = 1; i <= rows; i++) {\n    out += "*".repeat(i) + "\\n";\n  }\n  return out;\n}\nconsole.log(JSON.stringify(stars(3)));';
W["practice-loop-string-builder"] = 'function stars(rows) { return "*\\n"; }';
R["practice-converter-function"] =
  "function celsiusToFahrenheit(c) {\n  return (c * 9) / 5 + 32;\n}\nconsole.log(celsiusToFahrenheit(0));\nconsole.log(celsiusToFahrenheit(100));\nconsole.log(celsiusToFahrenheit(37));";
W["practice-converter-function"] = "function celsiusToFahrenheit(c) { return c + 32; }";
R["practice-default-parameter"] =
  'function greet(name, greeting = "Hello") {\n  return `${greeting}, ${name}!`;\n}\nconsole.log(greet("Ada"));\nconsole.log(greet("Ada", "Bonjour"));';
W["practice-default-parameter"] =
  'function greet(name, greeting) { if (greeting === undefined) { greeting = "Hi"; } return greeting + ", " + name + "!"; }';
R["practice-filter-scores"] =
  "const scores = [45, 92, 67, 88, 30];\nconst passing = scores.filter((s) => s >= 60);\nconsole.log(passing.length);";
W["practice-filter-scores"] = "const passing = scores;";
R["practice-map-transform"] =
  "const prices = [10, 20, 30];\nconst withTax = prices.map((p) => Math.round(p * 1.2));\nconsole.log(withTax);";
W["practice-map-transform"] = "const withTax = prices.push(36);";
R["practice-find-one"] =
  'const users = [{ name: "Ada", admin: false }, { name: "Grace", admin: true }, { name: "Linus", admin: false }];\nconsole.log(users.find((u) => u.admin).name);';
W["practice-find-one"] = 'console.log("Grace");';
R["practice-dom-text-and-class"] =
  'const heading = document.getElementById("heading");\nconst intro = document.getElementById("intro");\nheading.textContent = "Pipeline running";\nintro.classList.add("is-active");';
W["practice-dom-text-and-class"] = 'heading.innerText = "Wrong";';
R["practice-dom-create-items"] =
  'const todos = ["learn the DOM", "build a list", "render from data"];\nconst list = document.querySelector("#todo-list");\nfor (const todo of todos) {\n  const li = document.createElement("li");\n  li.textContent = todo;\n  list.appendChild(li);\n}';
W["practice-dom-create-items"] = "const list = document.querySelector('#todo-list');";
R["practice-dom-counter"] =
  'let count = 0;\nfunction bump() {\n  count = count + 1;\n  display.textContent = count;\n}\nbutton.addEventListener("click", bump);\nbump();\nbump();\nconsole.log(display.textContent);';
W["practice-dom-counter"] = "let count = 0;\nbutton.addEventListener('click', () => {});";
R["practice-storage-roundtrip"] =
  'function saveSettings(settings) {\n  storage.setItem("settings", JSON.stringify(settings));\n}\nfunction loadSettings() {\n  const raw = storage.getItem("settings");\n  if (raw === null) return { theme: "light" };\n  try { return JSON.parse(raw); } catch { return { theme: "light" }; }\n}\nsaveSettings({ theme: "dark", fontSize: 16 });\nconsole.log(loadSettings().theme);';
W["practice-storage-roundtrip"] = 'function saveSettings(s) { storage.setItem("settings", s); }';
R["practice-storage-corrupt-guard"] =
  'function loadSettings() {\n  const raw = storage.getItem("settings");\n  try {\n    return JSON.parse(raw);\n  } catch {\n    return { theme: "light" };\n  }\n}\nstorage.setItem("settings", "not-json{{");\nconsole.log(loadSettings());';
W["practice-storage-corrupt-guard"] =
  "function loadSettings() { return JSON.parse(storage.getItem('settings')); }";
R["practice-ordered-await"] =
  "async function run() {\n  const user = await api.loadUser();\n  const greeting = await api.loadGreeting(user.name);\n  console.log(greeting);\n}\nrun();";
W["practice-ordered-await"] =
  "async function run() { console.log(api.loadGreeting(api.loadUser().name)); }";
R["practice-fetch-guard"] =
  'async function loadUser() {\n  const response = await fetch("https://api.example.com/me");\n  if (!response.ok) {\n    throw new Error("HTTP " + response.status);\n  }\n  return await response.json();\n}\nloadUser().then((user) => console.log(user.name)).catch((err) => console.error(err.message));';
W["practice-fetch-guard"] =
  "async function loadUser() { const r = await fetch('https://api.example.com/me'); return r; }";
R["practice-save-point"] =
  'const workflow = {\n  check: "git status",\n  stage: "git add .",\n  commit: \'git commit -m "Add navigation"\',\n};';
W["practice-save-point"] = 'const workflow = { check: "", stage: "", commit: "" };';
R["practice-undo-commit"] = 'const undo = {\n  inspect: "git log",\n  redo: "git revert HEAD",\n};';
W["practice-undo-commit"] = 'const undo = { inspect: "git log", redo: "git reset --hard" };';
R["practice-classify-features"] =
  'const answers = {\n  cartAnimation: "frontend",\n  chargeCard: "backend",\n  stockCheck: "backend",\n  darkMode: "frontend",\n};';
W["practice-classify-features"] =
  'const answers = { cartAnimation: "backend", chargeCard: "frontend", stockCheck: "frontend", darkMode: "backend" };';
R["practice-request-trace"] =
  'const trace = [\n  "browser requests page",\n  "server checks session",\n  "no session found",\n  "redirect to login",\n];';
W["practice-request-trace"] =
  'const trace = ["no session found", "redirect to login", "browser requests page", "server checks session"];';

// ── Restored solutions (Course 1 revision, phase 2 re-verification) ─────────

R["practice-minimal-document"] = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
</head>
<body>
<p>Hello, web.</p>
</body>
</html>`;
W["practice-minimal-document"] = `<p>Hello, web.</p>`;

R["practice-titled-page"] = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>About Me</title>
</head>
<body>
<p>All about me and what I am learning.</p>
</body>
</html>`;
W["practice-titled-page"] = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Wrong Title</title>
</head>
<body>
<p>All about me and what I am learning.</p>
</body>
</html>`;

R["practice-personal-heading"] = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>My page</title>
</head>
<body>
<h1>Ada Lovelace</h1>
<p>I am learning to build the web.</p>
</body>
</html>`;
W["practice-personal-heading"] = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>My page</title>
</head>
<body>
<p>I am learning to build the web.</p>
</body>
</html>`;

R["practice-about-me-page"] = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>About Me</title>
</head>
<body>
<h1>Ada Lovelace</h1>
<p>I am learning web development at Code Journey.</p>
<p>My goal is to build things people love to use.</p>
<ul>
<li>Build a portfolio</li>
<li>Learn JavaScript</li>
<li>Ship a real project</li>
</ul>
</body>
</html>`;
W["practice-about-me-page"] = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>About Me</title>
</head>
<body>
<h1>Ada Lovelace</h1>
<p>Just one paragraph.</p>
</body>
</html>`;

R["practice-heading-hierarchy"] = `<h1>A Week of Learning</h1>
<p>Here is how my first week went.</p>
<h2>The plan</h2>
<p>I set out a simple study plan.</p>
<h3>Monday</h3>
<p>Started with HTML.</p>
<h2>What surprised me</h2>
<p>How much I enjoyed it.</p>`;
W["practice-heading-hierarchy"] = `<h1>A Week of Learning</h1>
<p>Intro line.</p>
<h3>Monday</h3>
<p>Started with HTML.</p>
<h2>What surprised me</h2>
<p>How much I enjoyed it.</p>`;

R["practice-article-structure"] = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>My Weekend Project</title>
</head>
<body>
<h1>My Weekend Project</h1>
<p>On Saturday I built my first web page.</p>
<p>On Sunday I styled it with CSS.</p>
<h2>What I learned</h2>
<p>Small steps add up fast.</p>
</body>
</html>`;
W["practice-article-structure"] = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>My Weekend Project</title>
</head>
<body>
<h1>My Weekend Project</h1>
<p>Only one paragraph.</p>
<h2>What I learned</h2>
</body>
</html>`;

R["practice-fix-the-link"] =
  `<p>When you get stuck, the <a href="https://developer.mozilla.org">MDN Web Docs</a> has the answers.</p>
`;
W["practice-fix-the-link"] =
  `<p>When you get stuck, the <a href="developer.mozilla.org">MDN Web Docs</a> has the answers.</p>
`;

R["practice-nav-menu"] = `<nav>
<ul>
<li><a href="#about">About</a></li>
<li><a href="#projects">Projects</a></li>
<li><a href="#contact">Contact</a></li>
</ul>
</nav>
`;
W["practice-nav-menu"] = `<nav>
<a href="#about">About</a>
<a href="#projects">Projects</a>
</nav>
`;

R["practice-relative-link"] = `<h1>Welcome</h1>
<p><a href="about.html">About this site</a></p>
<p><a href="projects.html">See my projects</a></p>
`;
W["practice-relative-link"] = `<h1>Welcome</h1>
<p><a href="https://example.com/about.html">About this site</a></p>
<p><a href="projects.html">See my projects</a></p>
`;

R["practice-accessible-image"] = `<h1>Morning pages</h1>
<p>Every walk starts before the sun does.</p>
<img src="/images/sunrise.jpg" alt="Sunrise over a mountain lake">
`;
W["practice-accessible-image"] = `<h1>Morning pages</h1>
<p>Every walk starts before the sun does.</p>
<img src="/images/sunrise.jpg">
`;

R["practice-figure-caption"] = `<h2>Where the week begins</h2>
<figure>
<img src="/images/market.jpg" alt="A crowded farmers market on a Saturday morning">
<figcaption>Saturday, 7 a.m.</figcaption>
</figure>
`;
W["practice-figure-caption"] = `<h2>Where the week begins</h2>
<figure>
<img src="/images/market.jpg" alt="wrong alt">
<figcaption>Saturday, 7 a.m.</figcaption>
</figure>
`;

R["practice-fix-the-image"] = `<h2>The team</h2>
<img src="team-photo.jpg" alt="The five founders at a whiteboard">
`;
W["practice-fix-the-image"] = `<h2>The team</h2>
<img src="images/teamphoto.JPG" alt="image">
`;

R["practice-semantic-rescue"] = `<header>
<p class="site-name">PetitFour</p>
</header>
<nav>
<a href="#menu">Menu</a>
<a href="#order">Order</a>
</nav>
<main>
<h1>Small cakes, big joy</h1>
<p>Baked fresh every morning.</p>
</main>
<footer>
<p>12 Rue des Lilas, Paris</p>
</footer>`;
W["practice-semantic-rescue"] = `<div>
<p class="site-name">PetitFour</p>
</div>
<div>
<a href="#menu">Menu</a>
<a href="#order">Order</a>
</div>
<div>
<h1>Small cakes, big joy</h1>
<p>Baked fresh every morning.</p>
</div>
<div>
<p>12 Rue des Lilas, Paris</p>
</div>`;

R["practice-label-input-pair"] = `<form>
<label for="email">Email address</label>
<input type="email" id="email" name="email">
</form>
`;
W["practice-label-input-pair"] = `<form>
<label>Email address</label>
<input type="email">
</form>
`;

R["practice-input-types"] = `<form>
<label for="pw">Password</label>
<input id="pw" type="password">

<label for="mail">Email</label>
<input id="mail" type="email">

<label for="dob">Date of birth</label>
<input id="dob" type="date">
</form>
`;
W["practice-input-types"] = `<form>
<label for="pw">Password</label>
<input id="pw" type="text">

<label for="mail">Email</label>
<input id="mail" type="text">

<label for="dob">Date of birth</label>
<input id="dob" type="text">
</form>
`;

R["practice-choice-controls"] = `<fieldset>
<legend>Choose a size</legend>
<label for="size-s">Small</label>
<input type="radio" id="size-s" name="size" value="s">
<label for="size-m">Medium</label>
<input type="radio" id="size-m" name="size" value="m">
<label for="size-l">Large</label>
<input type="radio" id="size-l" name="size" value="l">
</fieldset>

<p>
<label for="gift">This is a gift</label>
<input type="checkbox" id="gift" name="gift" value="yes">
</p>`;
W["practice-choice-controls"] = `<fieldset>
<legend>Choose a size</legend>
<label for="size-s">Small</label>
<input type="radio" id="size-s" name="size" value="s">
<label for="size-m">Medium</label>
<input type="radio" id="size-m" name="size" value="m">
<label for="size-l">Large</label>
<input type="radio" id="size-l" name="size" value="l">
</fieldset>

<p>
<label for="gift">This is a gift</label>
<input type="checkbox" id="gift" name="gift" value="no">
</p>`;

R["practice-dom-counter"] = `let count = 0;
function handleClick() {
  count = count + 1;
  display.textContent = count;
}
button.addEventListener("click", handleClick);
handleClick();
handleClick();`;
W["practice-dom-counter"] = `let count = 0;
function handleClick() {
  display.textContent = "clicked";
}
button.addEventListener("click", handleClick);
handleClick();
handleClick();`;

R["practice-storage-roundtrip"] = `function saveSettings(settings) {
  storage.setItem("settings", JSON.stringify(settings));
}
function loadSettings() {
  const raw = storage.getItem("settings");
  if (raw === null) return { theme: "light" };
  return JSON.parse(raw);
}
saveSettings({ theme: "dark", fontSize: 16 });`;
W["practice-storage-roundtrip"] = `function saveSettings(settings) {
  storage.setItem("settings", settings);
}
function loadSettings() {
  const raw = storage.getItem("settings");
  if (raw === null) return { theme: "light" };
  return JSON.parse(raw);
}
saveSettings({ theme: "dark", fontSize: 16 });`;

R["practice-storage-corrupt-guard"] = `function loadSettings() {
  const raw = storage.getItem("settings");
  try {
    return JSON.parse(raw);
  } catch {
    return { theme: "light" };
  }
}
storage.setItem("settings", "not-json{{");`;
W["practice-storage-corrupt-guard"] = `function loadSettings() {
  const raw = storage.getItem("settings");
  return JSON.parse(raw);
}
storage.setItem("settings", "not-json{{");`;
