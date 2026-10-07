"use strict";
const $ = (s) => document.querySelector(s);
const el = (tag, attrs = {}, ...kids) => {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === undefined || v === null || v === false) continue;
    if (k === "class") n.className = v; else if (k === "text") n.textContent = v; else n.setAttribute(k, v);
  }
  kids.flat().forEach((k) => { if (k !== null && k !== undefined && k !== false) n.append(k instanceof Node ? k : document.createTextNode(k)); });
  return n;
};
const fmt = (x) => (typeof x === "number" ? x.toLocaleString("fr-FR", { maximumFractionDigits: 2 }) : String(x));
const plural = (n, one, many) => `${fmt(n)} ${n > 1 ? many : one}`;

let CONFIG = null;
let FILES = [];
let currentRun = null;
const results = $("#results");

async function api(path, opts) {
  const r = await fetch(path, opts);
  if (!r.ok) {
    let msg = r.statusText;
    try { msg = (await r.json()).detail || msg; } catch (_) {}
    throw new Error(msg);
  }
  return r.json();
}

// ------------------------------------------------------------------ configuration
async function loadConfig() {
  CONFIG = await api("/api/config");
  $("#allowed").textContent = CONFIG.allowed_extensions.join(", ");
  const badge = $("#llm-badge");
  badge.textContent = CONFIG.groq_key_configured ? "LLM prêt" : "Clé Groq à saisir";
  badge.className = "badge " + (CONFIG.groq_key_configured ? "b-ok" : "b-warn");
  $("#key-field").hidden = CONFIG.groq_key_configured;
  const sel = $("#model");
  CONFIG.models.forEach((m) => sel.append(el("option", { value: m, text: m })));
  sel.value = CONFIG.default_model;
}

// ------------------------------------------------------------------ fichiers
function addFiles(list) {
  const errors = [];
  for (const f of list) {
    const ext = "." + f.name.split(".").pop().toLowerCase();
    if (!CONFIG.allowed_extensions.includes(ext)) { errors.push(`${f.name} : format non accepté`); continue; }
    if (f.size > CONFIG.max_file_mb * 1024 * 1024) { errors.push(`${f.name} : plus de ${CONFIG.max_file_mb} Mo`); continue; }
    if (FILES.some((x) => x.name === f.name)) continue;
    if (FILES.length >= CONFIG.max_files) { errors.push(`maximum ${CONFIG.max_files} fichiers`); break; }
    FILES.push(f);
  }
  $("#file-error").hidden = !errors.length;
  $("#file-error").textContent = errors.join(" · ");
  renderFiles();
}

function renderFiles() {
  $("#file-list").replaceChildren(...FILES.map((f, i) => {
    const rm = el("button", { title: "Retirer", "aria-label": "Retirer " + f.name }, "×");
    rm.onclick = () => { FILES.splice(i, 1); renderFiles(); };
    const size = f.size < 1024 ? "< 1 Ko" : `${Math.round(f.size / 1024)} Ko`;
    return el("li", {}, el("span", { title: f.name }, f.name), el("small", { class: "muted" }, size), rm);
  }));
  $("#run-btn").disabled = !FILES.length;
}

const dz = $("#dropzone");
["dragenter", "dragover"].forEach((e) => dz.addEventListener(e, (ev) => { ev.preventDefault(); dz.classList.add("over"); }));
["dragleave", "drop"].forEach((e) => dz.addEventListener(e, (ev) => { ev.preventDefault(); dz.classList.remove("over"); }));
dz.addEventListener("drop", (ev) => addFiles(ev.dataTransfer.files));
$("#file-input").addEventListener("change", (ev) => { addFiles(ev.target.files); ev.target.value = ""; });
document.querySelectorAll("input[name=planner]").forEach((r) =>
  r.addEventListener("change", () => { $("#llm-options").hidden = document.querySelector("input[name=planner]:checked").value !== "llm"; }));

// ------------------------------------------------------------------ états du panneau de droite
function showBusy(text) {
  results.replaceChildren(el("div", { class: "busy" }, el("span", { class: "spinner" }), el("span", { id: "stage" }, text)));
}

function showError(msg) {
  results.replaceChildren(el("p", { class: "error" }, "Le nettoyage a échoué : " + msg));
}

// ------------------------------------------------------------------ lancement et suivi
$("#run-btn").addEventListener("click", async () => {
  const planner = document.querySelector("input[name=planner]:checked").value;
  const fd = new FormData();
  FILES.forEach((f) => fd.append("files", f));
  fd.append("planner", planner);
  fd.append("impute", $("#impute").checked);
  fd.append("model", planner === "llm" ? $("#model").value : "");
  fd.append("groq_api_key", planner === "llm" ? $("#groq-key").value : "");
  $("#run-btn").disabled = true;
  showBusy("Envoi des fichiers…");
  try {
    const { job_id } = await api("/api/jobs", { method: "POST", body: fd });
    await follow(job_id);
  } catch (e) {
    showError(e.message);
  } finally {
    $("#run-btn").disabled = !FILES.length;
  }
});

async function follow(jobId) {
  for (;;) {
    const job = await api(`/api/jobs/${jobId}`);
    if (job.status === "waiting") { renderQuestions(jobId, job); return; }
    if (job.status === "done") { renderResult(job.result); loadHistory(); return; }
    if (job.status === "error") throw new Error(job.error);
    const stage = $("#stage");
    if (stage) stage.textContent = job.stage + "…"; else showBusy(job.stage + "…");
    await new Promise((r) => setTimeout(r, 800));
  }
}

// ------------------------------------------------------------------ question : valeurs extrêmes
function renderQuestions(jobId, job) {
  const choices = {};
  const rows = job.questions.map((q) => {
    choices[q.id] = q.llm_advice || "keep";
    const name = `q-${q.id}`;
    const radio = (value, label) => el("label", {},
      el("input", { type: "radio", name, value, checked: choices[q.id] === value ? "" : null }),
      el("span", {}, label));
    const seg = el("div", { class: "segmented", role: "radiogroup", "aria-label": `${q.table} ${q.column}` },
      radio("cap", "Corriger"), radio("keep", "Garder"));
    seg.addEventListener("change", (ev) => { choices[q.id] = ev.target.value; });
    const found = [];
    if (q.n_high) found.push(`${plural(q.n_high, "valeur", "valeurs")} au-dessus de ${fmt(q.high)}`);
    if (q.n_low) found.push(`${plural(q.n_low, "valeur", "valeurs")} en dessous de ${fmt(q.low)}`);
    const ex = q.examples.length ? ` (par exemple ${q.examples.map(fmt).join(" ; ")})` : "";
    return el("div", { class: "question" },
      el("div", {},
        el("div", { class: "q-title" }, `${q.table} · ${q.column}`),
        el("div", { class: "q-text" }, (found.join(" et ") || q.summary) + ex),
        el("div", { class: "muted" }, `Plage habituelle : ${fmt(q.low)} à ${fmt(q.high)}`),
        q.llm_advice ? el("div", { class: "advice" }, el("b", {}, `Le LLM conseille de ${q.llm_advice === "cap" ? "corriger" : "garder"}`), " : ", q.llm_reason) : null),
      seg);
  });
  const setAll = (v) => {
    job.questions.forEach((q) => { choices[q.id] = v; });
    results.querySelectorAll(`.question input[value=${v}]`).forEach((i) => { i.checked = true; });
  };
  const go = el("button", { class: "primary" }, "Valider et voir le résultat");
  go.onclick = async () => {
    go.disabled = true;
    try {
      await api(`/api/jobs/${jobId}/answers`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ answers: choices }) });
      showBusy("Application de vos choix…");
      await follow(jobId);
    } catch (e) { showError(e.message); }
  };
  const allCap = el("button", { class: "link" }, "Tout corriger");
  allCap.onclick = () => setAll("cap");
  const allKeep = el("button", { class: "link" }, "Tout garder");
  allKeep.onclick = () => setAll("keep");

  results.replaceChildren(
    el("h2", {}, "Des valeurs extrêmes ont été trouvées"),
    el("p", { class: "ask-intro muted" },
      "Ces valeurs sont très éloignées des autres : ce sont peut-être des erreurs de saisie, ou de vraies valeurs. ",
      "« Corriger » les ramène à la limite de la plage habituelle. « Garder » ne les modifie pas."),
    ...rows,
    el("div", { class: "ask-actions" }, el("div", { class: "actions" }, allCap, allKeep), go));
}

// ------------------------------------------------------------------ résultat
function kpi(value, label) {
  return el("div", { class: "kpi" }, el("b", {}, value), el("span", {}, label));
}

function renderResult(v) {
  currentRun = v.run_id;
  const t = v.totals;
  const pl = v.planner || {};
  const head = el("div", { class: "res-head" },
    el("div", {}, el("h2", {}, "Nettoyage terminé"), el("div", { class: "muted" }, v.files.join(", "))),
    el("div", { class: "actions" },
      el("a", { class: "primary", href: `/api/runs/${v.run_id}/download` }, "Télécharger les tables nettoyées"),
      el("a", { class: "ghost", href: `/api/runs/${v.run_id}/report`, target: "_blank", rel: "noopener" }, "Rapport imprimable")));

  const parts = [head,
    el("div", { class: "kpis" },
      kpi(`${t.tables_to_process} / ${t.tables}`, "tables à traiter"),
      kpi(fmt(t.corrections), "corrections"),
      kpi(fmt(t.rows_removed), "lignes supprimées"))];

  if (pl.warning) parts.push(el("p", { class: "note warn" }, pl.warning));
  else if (pl.model) parts.push(el("p", { class: "note" }, `Analyse faite par ${pl.model}.`));
  if (v.clean_tables.length) parts.push(el("p", { class: "note" }, `Déjà propres, rien à faire : ${v.clean_tables.join(", ")}.`));

  if (!v.tables.length) {
    parts.push(el("p", { class: "empty muted" }, "Aucune correction nécessaire : toutes les tables sont propres."));
    results.replaceChildren(...parts);
    markHistory();
    return;
  }

  const tabs = el("div", { class: "tabs", role: "tablist" });
  const pane = el("div", { role: "tabpanel" });
  v.tables.forEach((tb, i) => {
    const n = tb.actions.reduce((s, a) => s + a.count, 0);
    const b = el("button", { role: "tab", "aria-selected": i === 0 ? "true" : "false" }, tb.name, el("span", { class: "count" }, fmt(n)));
    b.onclick = () => {
      tabs.querySelectorAll("button").forEach((x) => x.setAttribute("aria-selected", "false"));
      b.setAttribute("aria-selected", "true");
      pane.replaceChildren(...tableView(tb));
    };
    tabs.append(b);
  });
  pane.replaceChildren(...tableView(v.tables[0]));
  parts.push(tabs, pane);
  results.replaceChildren(...parts);
  markHistory();
}

function tableView(tb) {
  const out = [el("p", { class: "note" }, `${tb.source} · ${plural(tb.rows_before, "ligne", "lignes")} avant, ${plural(tb.rows_after, "ligne", "lignes")} après`)];

  if (tb.llm && tb.llm.analysis) {
    out.push(el("div", { class: "llm-box" }, el("b", {}, "Analyse du LLM"), el("p", {}, tb.llm.analysis)));
  }

  out.push(el("h3", {}, "Ce qui a été corrigé"),
    el("ul", { class: "done" }, tb.actions.map((a) =>
      el("li", {}, el("div", { class: "act" }, el("span", {}, a.text), ...a.columns.map((c) => el("span", { class: "col" }, c)))))));
  tb.outliers.filter((o) => o.status === "kept").forEach((o) =>
    out.push(el("p", { class: "note" }, `Valeurs extrêmes gardées telles quelles (${o.column}) : ${o.text}.`)));
  tb.llm_refused.forEach((r) =>
    out.push(el("p", { class: "note" }, `Non appliqué sur conseil du LLM : ${r.label.toLowerCase()} (${r.column || "table"}). `
      + (r.reason ? r.reason.charAt(0).toUpperCase() + r.reason.slice(1) : ""))));

  const g = tb.grid;
  if (g.rows.length) {
    out.push(el("h3", {}, "Avant → après"),
      el("div", { class: "legend" },
        el("span", {}, el("i"), "valeur corrigée"),
        el("span", {}, "barré : ancienne valeur"),
        el("span", {}, "· : espace en trop")));
    const thead = el("tr", {}, el("th", {}, "Ligne"), g.columns.map((c) => el("th", {}, c)));
    const body = g.rows.map((r) => el("tr", {}, el("td", { class: "row-id" }, String(r.row)),
      r.cells.map((c) => c.changed
        ? el("td", { class: "ch" }, el("span", { class: "old" }, c.before), el("span", { class: "new" }, c.after))
        : el("td", {}, c.after))));
    out.push(el("div", { class: "scroll" }, el("table", {}, el("thead", {}, thead), el("tbody", {}, body))));
    if (g.more) out.push(el("p", { class: "note" }, `… et ${plural(g.more, "autre ligne modifiée", "autres lignes modifiées")} (toutes sont dans les tables téléchargées).`));
  }

  const rm = tb.removed;
  if (rm.rows.length) {
    out.push(el("h3", {}, "Lignes supprimées"));
    const thead = el("tr", {}, el("th", {}, "Ligne"), el("th", {}, "Raison"), rm.columns.map((c) => el("th", {}, c)));
    const body = rm.rows.map((r) => el("tr", {}, el("td", { class: "row-id" }, String(r.row)),
      el("td", {}, el("span", { class: "chip" }, r.reason)), r.values.map((x) => el("td", {}, x))));
    out.push(el("div", { class: "scroll" }, el("table", {}, el("thead", {}, thead), el("tbody", {}, body))));
    if (rm.more) out.push(el("p", { class: "note" }, `… et ${plural(rm.more, "autre ligne supprimée", "autres lignes supprimées")}.`));
  }
  return out;
}

// ------------------------------------------------------------------ historique
function markHistory() {
  document.querySelectorAll("#history li").forEach((li) => li.classList.toggle("active", li.dataset.id === currentRun));
}

async function loadHistory() {
  const runs = await api("/api/runs");
  const ul = $("#history");
  if (!runs.length) { ul.replaceChildren(el("li", { class: "muted" }, "Aucun nettoyage pour l'instant")); return; }
  ul.replaceChildren(...runs.map((r) => {
    const files = r.files.slice(0, 2).join(", ") + (r.files.length > 2 ? "…" : "");
    const li = el("li", { "data-id": r.run_id }, el("div", {}, files),
      el("small", {}, `${new Date(r.finished_at).toLocaleString("fr-FR")} · ${r.tables_to_process}/${r.tables} tables traitées · ${plural(r.corrections, "correction", "corrections")}`));
    li.onclick = async () => renderResult(await api(`/api/runs/${r.run_id}`));
    return li;
  }));
  markHistory();
}

loadConfig().then(loadHistory).catch((e) => showError(e.message));
