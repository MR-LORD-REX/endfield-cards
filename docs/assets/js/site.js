import { sections, pages } from "./navigation.js";

const baseURL = new URL("../../", import.meta.url);
const elements = Object.fromEntries([
  "navigation", "article", "breadcrumb", "reading-time", "page-pagination", "source-link",
  "table-of-contents", "menu-toggle", "sidebar-backdrop", "theme-toggle", "search-trigger",
  "search-dialog", "search-close", "search-input", "search-status", "search-results", "toast",
].map((id) => [id, document.getElementById(id)]));
const main = document.getElementById("main-content");
const documents = new Map();
const pageById = new Map(pages.map((page) => [page.id, page]));
const pageByURL = new Map(pages.map((page) => [new URL(page.path, baseURL).href, page]));
let currentPage = null;
let renderGeneration = 0;
let headingObserver;
let searchGeneration = 0;
let searchTimer;
let selectedResult = -1;
let searchNavigated = false;
let toastTimer;

function routeURL(page, section = "") {
  return `#/${page.id}${section ? `?section=${encodeURIComponent(section)}` : ""}`;
}

function readRoute() {
  if (!location.hash || location.hash === "#" || location.hash === "#/") return { id: "overview", section: "" };
  if (!location.hash.startsWith("#/")) return { id: currentPage?.id || "overview", section: location.hash.slice(1) };
  const [id, query = ""] = location.hash.slice(2).split("?", 2);
  return { id, section: new URLSearchParams(query).get("section") || "" };
}

function buildNavigation() {
  for (const section of sections) {
    const group = document.createElement("div");
    group.className = "nav-section";
    const label = document.createElement("p");
    label.className = "nav-group-title";
    label.textContent = section.title;
    group.append(label);
    for (const page of section.pages) {
      const link = document.createElement("a");
      link.className = "nav-page";
      link.href = routeURL(page);
      link.dataset.page = page.id;
      link.textContent = page.title;
      group.append(link);
    }
    elements.navigation.append(group);
  }
}

async function loadDocument(page) {
  if (!documents.has(page.id)) {
    const pending = fetch(new URL(page.path, baseURL)).then(async (response) => {
      if (!response.ok) throw new Error(`Unable to load ${page.title} (${response.status}).`);
      return response.text();
    }).catch((error) => {
      documents.delete(page.id);
      throw error;
    });
    documents.set(page.id, pending);
  }
  return documents.get(page.id);
}

function plainText(markdown) {
  return markdown.replace(/!?\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/[#*>`~|]/g, "").replace(/\s+/g, " ").trim();
}

function headingId(text) {
  return text.toLowerCase().normalize("NFKC").trim().replace(/[^\p{L}\p{N}\s_-]/gu, "")
    .replace(/\s+/g, "-").replace(/^-+|-+$/g, "") || "section";
}

function enhanceHeadings(page) {
  elements["table-of-contents"].replaceChildren();
  headingObserver?.disconnect();
  const used = new Map();
  const outline = [];
  const headings = [...elements.article.querySelectorAll("h1, h2, h3, h4")];
  const pageTitle = headings[0]?.textContent || page.title;
  for (const heading of headings) {
    const title = heading.textContent;
    const slug = headingId(title);
    const duplicate = used.get(slug) || 0;
    used.set(slug, duplicate + 1);
    heading.id = duplicate ? `${slug}-${duplicate}` : slug;
    if (!heading.matches("h2, h3")) continue;
    const anchor = document.createElement("a");
    anchor.className = "heading-anchor";
    anchor.href = routeURL(page, heading.id);
    anchor.textContent = "#";
    anchor.setAttribute("aria-label", `Link to ${title}`);
    heading.append(anchor);
    const link = document.createElement("a");
    link.className = `toc-link${heading.matches("h3") ? " subheading" : ""}`;
    link.href = routeURL(page, heading.id);
    link.textContent = title;
    link.dataset.heading = heading.id;
    elements["table-of-contents"].append(link);
    outline.push(heading);
  }
  if (typeof IntersectionObserver === "function") {
    headingObserver = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting)
        .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (!visible.length) return;
      for (const link of elements["table-of-contents"].querySelectorAll("a")) {
        link.classList.toggle("active", link.dataset.heading === visible[0].target.id);
      }
    }, { rootMargin: "-90px 0px -65% 0px" });
    outline.forEach((heading) => headingObserver.observe(heading));
  }
  return pageTitle;
}

function contentURL(href, sourceURL) {
  // Repository Markdown points outside docs; Pages includes previews at its root.
  const preview = href.match(/^(?:\.{1,2}\/)*examples\/output\/(.+)$/);
  return preview ? new URL(`examples/output/${preview[1]}`, baseURL) : new URL(href, sourceURL);
}

function rewriteLinks(page) {
  const sourceURL = new URL(page.path, baseURL);
  for (const link of elements.article.querySelectorAll("a[href]")) {
    const href = link.getAttribute("href");
    if (!href || href.startsWith("#/")) continue;
    try {
      if (href.startsWith("#")) {
        link.href = routeURL(page, decodeURIComponent(href.slice(1)));
        continue;
      }
      const target = contentURL(href, sourceURL);
      const section = target.hash.slice(1);
      target.hash = "";
      const internal = pageByURL.get(target.href);
      if (internal) link.href = routeURL(internal, decodeURIComponent(section));
      else {
        link.href = contentURL(href, sourceURL).href;
        if (target.origin !== location.origin && ["http:", "https:"].includes(target.protocol)) {
          link.target = "_blank";
          link.rel = "noopener noreferrer";
        }
      }
    } catch { /* Leave malformed links as sanitized Markdown text. */ }
  }
  for (const image of elements.article.querySelectorAll("img[src]")) {
    try { image.src = contentURL(image.getAttribute("src"), sourceURL).href; } catch { image.removeAttribute("src"); }
    image.loading = "lazy";
  }
}

async function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }
  const previous = document.activeElement;
  const field = document.createElement("textarea");
  field.value = text;
  field.style.cssText = "position:fixed;left:-9999px;top:0";
  document.body.append(field);
  field.select();
  const copied = document.execCommand("copy");
  field.remove();
  previous?.focus({ preventScroll: true });
  if (!copied) throw new Error("Copy unavailable");
}

function enhancePreviews(page) {
  const previewPath = new URL("examples/output/", baseURL).pathname;
  for (const image of elements.article.querySelectorAll("img[src]")) {
    if (!new URL(image.src).pathname.startsWith(previewPath)) continue;
    let link = image.closest("a");
    if (!link) {
      link = document.createElement("a");
      image.replaceWith(link);
      link.append(image);
    }
    link.href = image.src;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.setAttribute("aria-label", `Open ${image.alt || "card preview"} at full size in a new tab`);
    link.classList.add("preview-link");
  }
  if (page.id !== "gallery") return;
  for (const heading of elements.article.querySelectorAll("h2")) {
    const grid = document.createElement("div");
    grid.className = "gallery-grid";
    let content = heading.nextElementSibling;
    while (content && !content.matches("h1, h2")) {
      const next = content.nextElementSibling;
      for (const link of content.querySelectorAll("a.preview-link")) {
        const image = link.querySelector("img");
        const figure = document.createElement("figure");
        figure.className = "gallery-card";
        const caption = document.createElement("figcaption");
        caption.textContent = image.alt || "Card preview";
        figure.append(link, caption);
        grid.append(figure);
      }
      if (content.matches("p") && !content.textContent.trim() && !content.children.length) content.remove();
      content = next;
    }
    if (grid.children.length) heading.insertAdjacentElement("afterend", grid);
  }
}

function showToast(message) {
  clearTimeout(toastTimer);
  elements.toast.textContent = message;
  elements.toast.hidden = false;
  toastTimer = setTimeout(() => { elements.toast.hidden = true; }, 2200);
}

function enhanceCode() {
  for (const pre of elements.article.querySelectorAll("pre")) {
    const code = pre.querySelector("code");
    if (!code) continue;
    const original = code.textContent;
    const language = [...code.classList].find((name) => name.startsWith("language-"))?.slice(9) || "text";
    const aliases = { py: "python", sh: "bash", shell: "bash", console: "plaintext", text: "plaintext" };
    const highlighting = aliases[language] || language;
    if (window.hljs?.getLanguage(highlighting)) {
      code.innerHTML = window.hljs.highlight(original, { language: highlighting }).value;
      code.classList.add("hljs");
    }
    const wrapper = document.createElement("div");
    wrapper.className = "code-block";
    const toolbar = document.createElement("div");
    toolbar.className = "code-toolbar";
    const label = document.createElement("span");
    label.textContent = { py: "Python", python: "Python", sh: "Shell", bash: "Shell", console: "Terminal", text: "Text" }[language] || language;
    const button = document.createElement("button");
    button.className = "copy-button";
    button.textContent = "Copy";
    button.setAttribute("aria-label", `Copy ${label.textContent} example`);
    button.addEventListener("click", async () => {
      try { await copyText(original); button.textContent = "Copied"; showToast("Example copied to clipboard"); }
      catch { showToast("Select the example to copy it manually"); }
      setTimeout(() => { button.textContent = "Copy"; }, 2000);
    });
    toolbar.append(label, button);
    pre.replaceWith(wrapper);
    wrapper.append(toolbar, pre);
  }
  for (const table of elements.article.querySelectorAll("table")) {
    const wrapper = document.createElement("div");
    wrapper.className = "table-wrapper";
    table.replaceWith(wrapper);
    wrapper.append(table);
  }
}

function buildPagination(page) {
  elements["page-pagination"].replaceChildren();
  const index = pages.findIndex((candidate) => candidate.id === page.id);
  for (const [offset, label, direction] of [[-1, "← Previous", "previous"], [1, "Next →", "next"]]) {
    const target = pages[index + offset];
    if (!target) continue;
    const link = document.createElement("a");
    link.className = `pagination-link ${direction}`;
    link.href = routeURL(target);
    const caption = document.createElement("small");
    caption.textContent = label;
    const title = document.createElement("span");
    title.textContent = target.title;
    link.append(caption, title);
    elements["page-pagination"].append(link);
  }
}

function scrollToSection(section, focus = false) {
  const target = section && section !== "main-content"
    ? [...elements.article.querySelectorAll("[id]")].find((element) => element.id === section) : main;
  if (section && target) target.scrollIntoView({ block: "start" });
  else if (!section || section === "main-content") window.scrollTo({ top: 0 });
  if (focus && target) {
    if (!target.hasAttribute("tabindex")) target.setAttribute("tabindex", "-1");
    target.focus({ preventScroll: true });
  }
}

function renderError(title, message, retry = false) {
  headingObserver?.disconnect();
  elements.article.replaceChildren();
  const heading = document.createElement("h1");
  heading.textContent = title;
  const panel = document.createElement("div");
  panel.className = "error-state";
  const paragraph = document.createElement("p");
  paragraph.textContent = message;
  panel.append(paragraph);
  if (retry) {
    const button = document.createElement("button");
    button.textContent = "Try again";
    button.addEventListener("click", () => renderRoute(true, true));
    panel.append(button);
  } else {
    const link = document.createElement("a");
    link.href = "#/overview";
    link.textContent = "Return to the overview →";
    panel.append(link);
  }
  elements.article.append(heading, panel);
  elements.article.setAttribute("aria-busy", "false");
  elements["table-of-contents"].replaceChildren();
  elements["page-pagination"].replaceChildren();
}

function renderLoading() {
  headingObserver?.disconnect();
  const wrapper = document.createElement("div");
  wrapper.className = "loading-state";
  const bar = document.createElement("span");
  bar.className = "loading-bar";
  const label = document.createElement("p");
  label.textContent = "Loading documentation…";
  wrapper.append(bar, label);
  elements.article.replaceChildren(wrapper);
  elements.article.setAttribute("aria-busy", "true");
  elements["table-of-contents"].replaceChildren();
  elements["page-pagination"].replaceChildren();
  elements["reading-time"].textContent = "";
}

async function renderRoute(force = false, focus = false) {
  const route = readRoute();
  const page = pageById.get(route.id);
  const generation = ++renderGeneration;
  closeMenu(false);
  for (const link of elements.navigation.querySelectorAll("a")) {
    if (link.dataset.page === page?.id) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  }
  if (!page) {
    currentPage = null;
    document.title = "Page not found · endfield-cards";
    elements.breadcrumb.textContent = "Documentation";
    elements["reading-time"].textContent = "";
    elements["source-link"].hidden = true;
    renderError("Page not found", "This documentation page is unavailable. Choose a page from the navigation.");
    scrollToSection("", focus);
    return;
  }
  if (currentPage?.id === page.id && !force) { scrollToSection(route.section, focus); return; }
  currentPage = null;
  renderLoading();
  elements.breadcrumb.textContent = `${page.section} / ${page.title}`;
  elements["source-link"].href = new URL(page.path, baseURL).href;
  elements["source-link"].hidden = false;
  try {
    const markdown = await loadDocument(page);
    if (generation !== renderGeneration) return;
    if (!window.marked || !window.DOMPurify) throw new Error("The Markdown renderer could not load. Refresh the page to try again.");
    elements.article.innerHTML = window.DOMPurify.sanitize(window.marked.parse(markdown, { gfm: true }));
    const title = enhanceHeadings(page);
    rewriteLinks(page);
    enhancePreviews(page);
    enhanceCode();
    buildPagination(page);
    elements["reading-time"].textContent = `${Math.max(1, Math.ceil(plainText(markdown).split(/\s+/).length / 200))} min read`;
    document.title = `${title} · endfield-cards`;
    document.querySelector('meta[name="description"]').content = page.description;
    currentPage = page;
    elements.article.setAttribute("aria-busy", "false");
    requestAnimationFrame(() => { if (generation === renderGeneration) scrollToSection(route.section, focus); });
  } catch (error) {
    if (generation !== renderGeneration) return;
    renderError("Couldn't load this page", location.protocol === "file:"
      ? "Preview through a local HTTP server: python -m http.server 8000 --directory docs. Then open http://localhost:8000."
      : error.message, true);
  }
}

function openMenu() {
  document.body.classList.add("menu-open");
  elements["sidebar-backdrop"].hidden = false;
  elements["menu-toggle"].setAttribute("aria-expanded", "true");
  elements["menu-toggle"].setAttribute("aria-label", "Close navigation");
  (elements.navigation.querySelector('[aria-current="page"]') || elements.navigation.querySelector("a"))?.focus();
}

function closeMenu(restoreFocus = true) {
  const open = document.body.classList.contains("menu-open");
  document.body.classList.remove("menu-open");
  elements["sidebar-backdrop"].hidden = true;
  elements["menu-toggle"].setAttribute("aria-expanded", "false");
  elements["menu-toggle"].setAttribute("aria-label", "Open navigation");
  if (open && restoreFocus) elements["menu-toggle"].focus();
}

function updateThemeButton() {
  const dark = document.documentElement.dataset.theme === "dark";
  elements["theme-toggle"].setAttribute("aria-label", `Switch to ${dark ? "light" : "dark"} theme`);
  document.querySelector('meta[name="theme-color"]').content = dark ? "#151a21" : "#f5f5f0";
}

function highlightMatches(container, text, query) {
  const terms = query.split(/\s+/).filter(Boolean);
  if (!terms.length) { container.textContent = text; return; }
  const escaped = terms.map((term) => term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  const expression = new RegExp(`(${escaped.join("|")})`, "gi");
  let last = 0;
  for (const match of text.matchAll(expression)) {
    container.append(document.createTextNode(text.slice(last, match.index)));
    const mark = document.createElement("mark");
    mark.textContent = match[0];
    container.append(mark);
    last = match.index + match[0].length;
  }
  container.append(document.createTextNode(text.slice(last)));
}

async function searchDocuments() {
  const generation = ++searchGeneration;
  const query = elements["search-input"].value.trim().slice(0, 180);
  elements["search-results"].replaceChildren();
  selectedResult = -1;
  if (!query) { elements["search-status"].textContent = "Type to search all documentation."; return; }
  elements["search-status"].textContent = "Searching…";
  const results = await Promise.allSettled(pages.map(async (page) => ({ page, markdown: await loadDocument(page) })));
  if (generation !== searchGeneration || !elements["search-dialog"].open) return;
  const terms = query.toLowerCase().split(/\s+/);
  const matches = [];
  let unavailable = 0;
  for (const result of results) {
    if (result.status !== "fulfilled") { unavailable++; continue; }
    const { page, markdown } = result.value;
    const text = plainText(markdown);
    const haystack = `${page.title} ${page.description} ${text}`.toLowerCase();
    if (!terms.every((term) => haystack.includes(term))) continue;
    const score = terms.filter((term) => page.title.toLowerCase().includes(term)).length;
    const position = Math.max(0, text.toLowerCase().indexOf(terms[0]));
    const start = Math.max(0, position - 50);
    matches.push({ page, score, snippet: `${start ? "…" : ""}${text.slice(start, start + 170)}${text.length > start + 170 ? "…" : ""}` });
  }
  matches.sort((a, b) => b.score - a.score);
  for (const { page, snippet } of matches) {
    const link = document.createElement("a");
    link.className = "search-result";
    link.href = routeURL(page);
    const section = document.createElement("small");
    section.textContent = page.section;
    const title = document.createElement("strong");
    highlightMatches(title, page.title, query);
    const preview = document.createElement("p");
    highlightMatches(preview, snippet, query);
    link.append(section, title, preview);
    link.addEventListener("click", () => {
      searchNavigated = true;
      elements["search-dialog"].close();
      if (location.hash === routeURL(page)) scrollToSection("", true);
    });
    elements["search-results"].append(link);
  }
  elements["search-status"].textContent = matches.length
    ? `${matches.length} ${matches.length === 1 ? "page" : "pages"} found${unavailable ? ` · ${unavailable} pages could not be loaded` : ""}`
    : unavailable ? "Some pages could not be loaded. Check your connection and try again." : "No pages found. Try a method name or a shorter search.";
}

function openSearch() {
  closeMenu(false);
  searchNavigated = false;
  if (!elements["search-dialog"].open) elements["search-dialog"].showModal();
  elements["search-input"].focus();
  searchDocuments();
}

elements["menu-toggle"].addEventListener("click", () => document.body.classList.contains("menu-open") ? closeMenu() : openMenu());
elements["sidebar-backdrop"].addEventListener("click", () => closeMenu());
elements.navigation.addEventListener("click", (event) => {
  const link = event.target.closest("a");
  if (!link) return;
  closeMenu(false);
  if (link.hash === location.hash) scrollToSection("", true);
});
for (const link of document.querySelectorAll('.skip-link, .back-to-top')) {
  link.addEventListener("click", (event) => { event.preventDefault(); scrollToSection("main-content", true); });
}
elements["theme-toggle"].addEventListener("click", () => {
  const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = next;
  try { localStorage.setItem("endfield-cards-docs-theme", next); } catch { /* Theme works even if storage is disabled. */ }
  updateThemeButton();
});
elements["search-trigger"].addEventListener("click", openSearch);
elements["search-close"].addEventListener("click", () => elements["search-dialog"].close());
elements["search-dialog"].addEventListener("click", (event) => {
  const bounds = elements["search-dialog"].getBoundingClientRect();
  if (event.target === elements["search-dialog"] && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) elements["search-dialog"].close();
});
elements["search-input"].addEventListener("input", () => {
  ++searchGeneration;
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => { if (elements["search-dialog"].open) searchDocuments(); }, 140);
});
elements["search-dialog"].addEventListener("close", () => {
  ++searchGeneration;
  clearTimeout(searchTimer);
  if (!searchNavigated) elements["search-trigger"].focus();
  searchNavigated = false;
});
elements["search-input"].addEventListener("keydown", (event) => {
  const results = [...elements["search-results"].querySelectorAll("a")];
  if (["ArrowDown", "ArrowUp"].includes(event.key) && results.length) {
    event.preventDefault();
    selectedResult = selectedResult < 0 ? (event.key === "ArrowDown" ? 0 : results.length - 1)
      : (selectedResult + (event.key === "ArrowDown" ? 1 : -1) + results.length) % results.length;
    results.forEach((result, index) => result.classList.toggle("selected", index === selectedResult));
    results[selectedResult].scrollIntoView({ block: "nearest" });
  } else if (event.key === "Enter" && results.length) {
    event.preventDefault();
    results[Math.max(0, selectedResult)].click();
  }
});
document.addEventListener("click", (event) => {
  const link = event.target.closest("a[href]");
  if (!link || event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
  if (link.hash.startsWith("#/") && link.hash === location.hash) {
    event.preventDefault();
    renderRoute(false, true);
  }
});
document.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    elements["search-dialog"].open ? elements["search-dialog"].close() : openSearch();
  }
  if (event.key === "Escape") closeMenu();
  if (event.key === "Tab" && document.body.classList.contains("menu-open")) {
    const controls = [elements["menu-toggle"], ...document.getElementById("sidebar").querySelectorAll("a[href], button")];
    const first = controls[0];
    const last = controls.at(-1);
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  }
});
window.addEventListener("hashchange", () => renderRoute(false, true));
matchMedia("(min-width: 861px)").addEventListener("change", (event) => { if (event.matches) closeMenu(false); });
buildNavigation();
updateThemeButton();
renderRoute();
