/**
 * Reference + wrong solutions for the ADVANCED (Course 3, Advanced HTML) harness.
 * Reference solutions must pass every test; wrong solutions must fail at least one.
 * Wrong solutions deliberately miss exactly one core requirement where meaningful.
 */

const SKEL = (title, body) =>
  `<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${title}</title></head>
<body>
${body}
</body>
</html>
`;

const HEAD_FULL = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kite CLI — Getting started</title>
  <meta name="description" content="Install and configure Kite CLI in ten minutes.">
  <link rel="canonical" href="https://docs.example.com/kite/getting-started">
  <meta property="og:title" content="Kite CLI — Getting started">
  <meta property="og:description" content="Install and configure Kite CLI in ten minutes.">
  <meta property="og:image" content="https://docs.example.com/kite-card.png">
  <link rel="alternate" hreflang="en" href="https://docs.example.com/kite/getting-started">
  <link rel="alternate" hreflang="vi" href="https://docs.example.com/kite/vi/getting-started">
  <link rel="alternate" hreflang="x-default" href="https://docs.example.com/kite/getting-started">
</head>
<body></body>
</html>
`;

export const REFERENCE_SOLUTIONS = {
  "i3-arch-rebuild": SKEL(
    "Field Notes",
    `<hgroup>
  <h1>Field Notes from the Semantics Wars</h1>
  <p>Dispatches from a working developer</p>
</hgroup>
<article>
  <h2>Why structure survives refactors</h2>
  <p>Markup outlives frameworks.</p>
  <article aria-labelledby="c1-h">
    <h3 id="c1-h">Preaching to the choir</h3>
    <p>Said every a11y engineer ever.</p>
  </article>
</article>
<section aria-labelledby="comments-h">
  <h2 id="comments-h">Comments</h2>
  <p>Readers respond below.</p>
</section>`,
  ),
  "i3-arch-outline": SKEL(
    "Field Guide",
    `<h1>Field Guide to Web Semantics</h1>
<h2>Habitats</h2>
<h3>Grasslands</h3>
<h3>Wetlands</h3>
<h2>Migrations</h2>
<h3>Autumn routes</h3>
<h3>Spring returns</h3>
<h2>Field Techniques</h2>
<h3>Observation</h3>
<h3>Note taking</h3>
<h4>Abbreviations</h4>
<footer>Field Guide</footer>`,
  ),
  "i3-arch-debug": SKEL(
    "City Guide",
    `<h1>City Guide</h1>
<h2>Old Town</h2>
<h2>Districts</h2>
<section aria-labelledby="districts-h">
  <h2 id="districts-h">Districts</h2>
  <p>Cobbled streets and cafes.</p>
</section>
<h2>Food Scene</h2>
<section aria-labelledby="markets-h">
  <h2 id="markets-h">Markets</h2>
  <article>
    <h3>Night market</h3>
    <p>Open Fridays.</p>
    <section aria-labelledby="getting-h">
      <h4 id="getting-h">Getting there</h4>
      <p>Bus 12.</p>
    </section>
  </article>
</section>`,
  ),
  "i3-name-icon-button": SKEL(
    "Toolbar",
    `<button aria-labelledby="close-l"><svg aria-hidden="true"><path d="M1 1"/></svg></button>
<span id="close-l" hidden>Close panel</span>
<button aria-labelledby="search-l"><svg aria-hidden="true"><path d="M2 2"/></svg></button>
<span id="search-l" hidden>Search documents</span>
<button aria-labelledby="settings-l"><svg aria-hidden="true"><path d="M3 3"/></svg></button>
<span id="settings-l" hidden>Open settings</span>
<button>Save</button>`,
  ),
  "i3-name-regions": SKEL(
    "Two navs",
    `<nav aria-label="Primary"><a href="/docs">Docs</a></nav>
<main>
  <h1>Platform hub</h1>
  <section aria-labelledby="guides-h">
    <h2 id="guides-h">Guides</h2>
  </section>
  <section aria-labelledby="ref-h">
    <h2 id="ref-h">Reference</h2>
  </section>
</main>
<nav aria-label="Footer"><a href="/privacy">Privacy</a></nav>`,
  ),
  "i3-name-debug": SKEL(
    "Checkout",
    `<h1>Checkout</h1>
<img src="cards.png" alt="Accepted payment cards: Visa, Mastercard, Amex">
<form>
  <label for="email">Email address</label>
  <input id="email" type="email">
  <label for="promocode">Promo code</label>
  <input id="promocode" type="text">
  <button>Pay now</button>
  <button>Buy now</button>
</form>`,
  ),
  "i3-dialog-faq": SKEL(
    "FAQ",
    `<details name="faq">
  <summary>Can I change plan later?</summary>
  <p>Yes, prorated to the day.</p>
</details>
<details name="faq">
  <summary>Do you offer invoices?</summary>
  <p>Every account, automatically.</p>
</details>
<details name="faq">
  <summary>Is there a free tier?</summary>
  <p>Forever, for one project.</p>
</details>`,
  ),
  "i3-dialog-confirm": SKEL(
    "Delete file",
    `<button data-open>Delete…</button>
<dialog id="confirm-delete" aria-labelledby="confirm-h">
  <h2 id="confirm-h">Delete this file?</h2>
  <p>This cannot be undone.</p>
  <form method="dialog">
    <button autofocus>Cancel</button>
    <button value="delete">Delete</button>
  </form>
</dialog>
<style>dialog::backdrop { background: rgba(0,0,0,.5); }</style>`,
  ),
  "i3-dialog-debug": SKEL(
    "Settings",
    `<h1>Workspace settings</h1>
<button commandfor="danger" command="show-modal">Delete workspace…</button>
<dialog id="danger">
  <h2>Delete workspace?</h2>
  <form method="dialog"><button autofocus>Cancel</button></form>
</dialog>
<details name="faq">
  <summary>Can I undo?</summary>
  <p>No.</p>
</details>
<details name="faq">
  <summary>What is exported?</summary>
  <p>Issues and labels.</p>
</details>`,
  ),
  "i3-popover-menu": SKEL(
    "Row actions",
    `<button popovertarget="row-menu">Actions</button>
<div id="row-menu" popover>
  <button>Rename</button>
  <button>Duplicate</button>
  <button popovertarget="row-menu" popovertargetaction="hide">Close</button>
</div>`,
  ),
  "i3-popover-toast": SKEL(
    "Toast + filters",
    `<button popovertarget="toast" popovertargetaction="show">Save</button>
<div id="toast" popover="manual">
  <p>Saved.</p>
  <button popovertarget="toast" popovertargetaction="hide">Close</button>
</div>
<button popovertarget="filters">Filters</button>
<div id="filters" popover>
  <label><input type="checkbox"> Active</label>
</div>`,
  ),
  "i3-popover-debug": SKEL(
    "Danger zone",
    `<h1>Danger zone</h1>
<button commandfor="delete-confirm" command="show-modal">Delete project…</button>
<dialog id="delete-confirm">
  <h2>Delete this project?</h2>
  <p>All issues and labels go with it.</p>
  <button commandfor="delete-confirm" command="close">Cancel</button>
  <button onclick="deleteProject()">Delete forever</button>
</dialog>
<script>
  function deleteProject(){ /* real action only */ }
</script>`,
  ),
  "i3-media-hero": SKEL(
    "Hero",
    `<picture>
  <source type="image/avif" srcset="hero.avif">
  <source type="image/webp" srcset="hero.webp">
  <img src="hero.jpg" alt="Launch event crowd under confetti" width="1600" height="800" fetchpriority="high">
</picture>`,
  ),
  "i3-media-srcset": SKEL(
    "Product card",
    `<img src="product-600w.jpg"
  srcset="product-300w.jpg 300w, product-600w.jpg 600w, product-900w.jpg 900w"
  sizes="(max-width: 600px) 100vw, 30vw"
  width="900" height="600"
  decoding="async"
  alt="Aluminium water bottle in three colors">
<img src="sketch.jpg" loading="lazy" width="600" height="400" alt="Early design sketch of the bottle">`,
  ),
  "i3-media-debug": SKEL(
    "Gallery",
    `<picture>
  <source type="image/avif" srcset="hero.avif">
  <img src="hero.jpg" alt="Confetti falling over the launch stage" width="1600" height="800" fetchpriority="high">
</picture>
<div class="card">
  <img src="team.jpg" sizes="300px" alt="The founding team on stage" width="600" height="400">
</div>
<picture>
  <source type="image/webp" srcset="chart.webp">
  <img src="chart.jpg" alt="Downloads per week, rising" width="900" height="500">
</picture>`,
  ),
  "i3-embed-sandbox": SKEL(
    "Two embeds",
    `<iframe src="https://chat.example.com/widget" sandbox="allow-scripts allow-forms" title="Support chat" loading="lazy" width="320" height="480"></iframe>
<iframe src="report.html" sandbox="allow-scripts allow-same-origin" title="Quarterly report" width="640" height="360"></iframe>`,
  ),
  "i3-meta-head": HEAD_FULL,
  "i3-meta-debug": `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Release notes — Widget</title>
  <meta name="robots" content="index, follow">
</head>
<body>
  <h1>Release notes</h1>
  <iframe src="https://comments.example.com/thread/42" sandbox="allow-scripts allow-forms" title="Comments thread" width="600" height="400"></iframe>
</body>
</html>
`,
  "i3-project-doc-layer": `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kite CLI — Getting started</title>
  <meta name="description" content="Install and fly with Kite CLI.">
  <link rel="canonical" href="https://docs.example.com/kite/getting-started">
  <meta property="og:title" content="Kite CLI — Getting started">
  <meta property="og:image" content="https://docs.example.com/kite-card.png">
</head>
<body>
  <header>Kite CLI</header>
  <nav><a href="#install-h">Install</a><a href="#usage-h">Usage</a></nav>
  <main>
    <article aria-labelledby="kite-h">
      <h1 id="kite-h">Getting started with Kite CLI</h1>
      <p>Updated <time datetime="2026-09-12">September 12, 2026</time>.</p>
      <section aria-labelledby="install-h">
        <h2 id="install-h">Install</h2>
        <p>One command.</p>
      </section>
      <section aria-labelledby="usage-h">
        <h2 id="usage-h">Usage</h2>
        <p>Fly.</p>
      </section>
    </article>
  </main>
  <footer>
    <address><a href="mailto:team@kite.dev">team@kite.dev</a></address>
  </footer>
</body>
</html>
`,
  "i3-project-media-layer": `<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Kite docs</title></head>
<body>
  <details name="faq"><summary>Is it fast?</summary><p>Yes.</p></details>
  <details name="faq"><summary>Is it free?</summary><p>Yes.</p></details>
  <details name="faq"><summary>Is it done?</summary><p>Almost.</p></details>
  <dialog aria-labelledby="del-h">
    <h2 id="del-h">Delete local config?</h2>
    <form method="dialog"><button autofocus>Cancel</button><button>Delete</button></form>
  </dialog>
  <picture>
    <source type="image/avif" srcset="hero.avif">
    <source type="image/webp" srcset="hero.webp">
    <img src="hero.jpg" alt="Kite flying over a laptop" width="1600" height="800">
  </picture>
  <iframe src="https://demo.kite.dev/embed" sandbox="allow-scripts" title="Kite demo" loading="lazy" width="640" height="360"></iframe>
</body>
</html>
`,
  "i3-project-enhance-layer": `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kite CLI — Getting started</title>
  <meta name="robots" content="index, follow">
  <link rel="alternate" hreflang="en" href="https://docs.example.com/en/getting-started">
  <link rel="alternate" hreflang="vi" href="https://docs.example.com/vi/getting-started">
</head>
<body>
  <details>
    <summary>Install command</summary>
    <code>npx kite init</code>
    <button aria-label="Copy install command">Copy</button>
  </details>
</body>
</html>
`,
};

export const WRONG_SOLUTIONS = {
  // Architecture: headings present but outline skips (h1→h3) and second h1 sneaks in.
  "i3-arch-rebuild": SKEL(
    "Field Notes",
    `<h1>Field Notes</h1>
<h3>Why structure survives refactors</h3>
<article><p>Markup outlives frameworks.</p></article>
<section><h4>Comments</h4></section>`,
  ),
  // Outline: correct h1/h2/h3 but the h4 is missing.
  "i3-arch-outline": SKEL(
    "Field Guide",
    `<h1>Field Guide</h1>
<h2>Habitats</h2><h3>Grasslands</h3><h3>Wetlands</h3>
<h2>Migrations</h2><h3>Autumn routes</h3><h3>Spring returns</h3>
<h2>Field Techniques</h2><h3>Observation</h3><h3>Note taking</h3>
<footer>Field Guide</footer>`,
  ),
  // Debug: fixed h1s but left the role="heading" hack in place.
  "i3-arch-debug": SKEL(
    "City Guide",
    `<h1>City Guide</h1>
<h2>Old Town</h2>
<div role="heading" aria-level="2">Districts</div>
<section aria-labelledby="d-h"><h2 id="d-h">Districts</h2></section>
<h2>Food Scene</h2>`,
  ),
  // Icon buttons: labels referenced but one svg is not aria-hidden.
  "i3-name-icon-button": SKEL(
    "Toolbar",
    `<button aria-labelledby="close-l"><svg aria-hidden="true"><path d="M1 1"/></svg></button>
<span id="close-l" hidden>Close panel</span>
<button aria-labelledby="search-l"><svg><path d="M2 2"/></svg></button>
<span id="search-l" hidden>Search documents</span>
<button>Save</button>`,
  ),
  // Regions: two navs but with identical names.
  "i3-name-regions": SKEL(
    "Two navs",
    `<nav aria-label="Primary"><a href="/docs">Docs</a></nav>
<main>
  <h1>Platform hub</h1>
  <section aria-labelledby="guides-h"><h2 id="guides-h">Guides</h2></section>
</main>
<nav aria-label="Primary"><a href="/privacy">Privacy</a></nav>`,
  ),
  // Debug: fixed the image + buttons but left the unassociated email label.
  "i3-name-debug": SKEL(
    "Checkout",
    `<h1>Checkout</h1>
<img src="cards.png" alt="Accepted payment cards: Visa, Mastercard, Amex">
<form>
  <label>Email address</label>
  <input id="email" type="email">
  <button>Pay now</button>
  <button>Buy now</button>
</form>`,
  ),
  // FAQ: three details but no shared name (no exclusive accordion).
  "i3-dialog-faq": SKEL(
    "FAQ",
    `<details><summary>Can I change plan later?</summary><p>Yes.</p></details>
<details><summary>Do you offer invoices?</summary><p>Yes.</p></details>
<details><summary>Is there a free tier?</summary><p>Yes.</p></details>`,
  ),
  // Dialog: real dialog + form, but autofocus is on the destructive button.
  "i3-dialog-confirm": SKEL(
    "Delete file",
    `<dialog id="confirm-delete" aria-labelledby="confirm-h">
  <h2 id="confirm-h">Delete this file?</h2>
  <form method="dialog">
    <button value="delete" autofocus>Delete</button>
    <button>Cancel</button>
  </form>
</dialog>
<style>dialog::backdrop { background: rgba(0,0,0,.5); }</style>`,
  ),
  // Debug: dialog converted but accordions keep mismatched names.
  "i3-dialog-debug": SKEL(
    "Settings",
    `<h1>Workspace settings</h1>
<button commandfor="danger" command="show-modal">Delete workspace…</button>
<dialog id="danger"><h2>Delete workspace?</h2></dialog>
<details name="faq"><summary>Can I undo?</summary><p>No.</p></details>
<details name="faq2"><summary>What is exported?</summary><p>Issues.</p></details>`,
  ),
  // Popover menu: popover exists but no close button with action=hide.
  "i3-popover-menu": SKEL(
    "Row actions",
    `<button popovertarget="row-menu">Actions</button>
<div id="row-menu" popover>
  <button>Rename</button>
  <button>Duplicate</button>
</div>`,
  ),
  // Toast: uses manual flavor but forgets its own close button.
  "i3-popover-toast": SKEL(
    "Toast + filters",
    `<div id="toast" popover="manual"><p>Saved.</p></div>
<button popovertarget="filters">Filters</button>
<div id="filters" popover><label><input type="checkbox"> Active</label></div>`,
  ),
  // Debug: open button converted, close button still onclick.
  "i3-popover-debug": SKEL(
    "Danger zone",
    `<h1>Danger zone</h1>
<button commandfor="delete-confirm" command="show-modal">Delete project…</button>
<dialog id="delete-confirm">
  <h2>Delete this project?</h2>
  <button onclick="closeDelete()">Cancel</button>
</dialog>
<script>
  function closeDelete(){ document.getElementById('delete-confirm').close(); }
</script>`,
  ),
  // Hero: sources correct but fetchpriority missing.
  "i3-media-hero": SKEL(
    "Hero",
    `<picture>
  <source type="image/avif" srcset="hero.avif">
  <source type="image/webp" srcset="hero.webp">
  <img src="hero.jpg" alt="Launch event crowd under confetti" width="1600" height="800">
</picture>`,
  ),
  // srcset: candidates fine but sizes uses a lying 100vw.
  "i3-media-srcset": SKEL(
    "Product card",
    `<img src="product-600w.jpg"
  srcset="product-300w.jpg 300w, product-600w.jpg 600w, product-900w.jpg 900w"
  sizes="100vw"
  width="900" height="600"
  decoding="async"
  alt="Aluminium water bottle in three colors">
<img src="sketch.jpg" loading="lazy" width="600" height="400" alt="Early design sketch">`,
  ),
  // Debug: hero priority fixed but card sizes still 100vw.
  "i3-media-debug": SKEL(
    "Gallery",
    `<picture>
  <source type="image/avif" srcset="hero.avif">
  <img src="hero.jpg" alt="Confetti falling over the launch stage" width="1600" height="800" fetchpriority="high">
</picture>
<div class="card">
  <img src="team.jpg" sizes="100vw" alt="The founding team on stage" width="600" height="400">
</div>`,
  ),
  // Embeds: widget sandboxed but grants the escalation pair.
  "i3-embed-sandbox": SKEL(
    "Two embeds",
    `<iframe src="https://chat.example.com/widget" sandbox="allow-scripts allow-forms allow-same-origin" title="Support chat" loading="lazy" width="320" height="480"></iframe>
<iframe src="report.html" sandbox="allow-scripts allow-same-origin" title="Quarterly report" width="640" height="360"></iframe>`,
  ),
  // Head: canonical points at the site root instead of the page.
  "i3-meta-head": HEAD_FULL.replace(
    'href="https://docs.example.com/kite/getting-started"',
    'href="https://docs.example.com"',
  ),
  // Debug: sandbox added (with same-origin — escalation) and robots fixed.
  "i3-meta-debug": `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Release notes — Widget</title>
  <meta name="robots" content="index, follow">
</head>
<body>
  <h1>Release notes</h1>
  <iframe src="https://comments.example.com/thread/42" sandbox="allow-scripts allow-same-origin" title="Comments thread" width="600" height="400"></iframe>
</body>
</html>
`,
  // Project doc layer: head fine, but no <time datetime> and article lacks aria-labelledby.
  "i3-project-doc-layer": `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kite CLI — Getting started</title>
  <meta name="description" content="Install and fly with Kite CLI.">
  <link rel="canonical" href="https://docs.example.com/kite/getting-started">
  <meta property="og:title" content="Kite CLI — Getting started">
  <meta property="og:image" content="https://docs.example.com/kite-card.png">
</head>
<body>
  <header>Kite CLI</header>
  <nav><a href="#install-h">Install</a><a href="#usage-h">Usage</a></nav>
  <main>
    <article>
      <h1>Getting started with Kite CLI</h1>
      <p>Updated September 12, 2026.</p>
      <section aria-labelledby="install-h"><h2 id="install-h">Install</h2></section>
      <section aria-labelledby="usage-h"><h2 id="usage-h">Usage</h2></section>
    </article>
  </main>
  <footer><address><a href="mailto:team@kite.dev">team@kite.dev</a></address></footer>
</body>
</html>
`,
  // Project media layer: FAQ + dialog fine, but iframe carries allow-same-origin.
  "i3-project-media-layer": `<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Kite docs</title></head>
<body>
  <details name="faq"><summary>Is it fast?</summary><p>Yes.</p></details>
  <details name="faq"><summary>Is it free?</summary><p>Yes.</p></details>
  <details name="faq"><summary>Is it done?</summary><p>Almost.</p></details>
  <dialog aria-labelledby="del-h">
    <h2 id="del-h">Delete local config?</h2>
    <form method="dialog"><button autofocus>Cancel</button><button>Delete</button></form>
  </dialog>
  <picture>
    <source type="image/avif" srcset="hero.avif">
    <source type="image/webp" srcset="hero.webp">
    <img src="hero.jpg" alt="Kite flying over a laptop" width="1600" height="800">
  </picture>
  <iframe src="https://demo.kite.dev/embed" sandbox="allow-scripts allow-same-origin" title="Kite demo" loading="lazy" width="640" height="360"></iframe>
</body>
</html>
`,
  // Project enhance layer: hreflang ok but robots says noindex.
  "i3-project-enhance-layer": `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kite CLI — Getting started</title>
  <meta name="robots" content="noindex, follow">
  <link rel="alternate" hreflang="en" href="https://docs.example.com/en/getting-started">
  <link rel="alternate" hreflang="vi" href="https://docs.example.com/vi/getting-started">
</head>
<body>
  <details>
    <summary>Install command</summary>
    <code>npx kite init</code>
    <button aria-label="Copy install command">Copy</button>
  </details>
</body>
</html>
`,
};
