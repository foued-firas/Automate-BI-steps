"""Application web BI Flow : backend FastAPI + frontend (web/static).

Lancement (depuis la racine du projet) :
    uvicorn web.app:app --reload        puis ouvrir http://127.0.0.1:8000

Parcours :
  1. l'utilisateur dépose des fichiers CSV / Excel ;
  2. l'agent de nettoyage (avec l'outil LLM Groq si choisi) traite chaque table ;
  3. si des valeurs extrêmes sont trouvées, l'interface demande à l'utilisateur de valider avant de les corriger ;
  4. l'interface affiche, pour les seules tables à traiter, ce qui a été corrigé et les lignes avant / après.
"""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import sys
import threading
import traceback
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from fastapi import Body, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "cleaning_agent"))
import agent as cleaning  # noqa: E402
import llm_planner  # noqa: E402

HISTORY = ROOT / "history"
WORKSPACE = ROOT / "web" / "workspace"
STATIC = ROOT / "web" / "static"
ALLOWED = {".csv", ".xlsx", ".xlsm"}          # formats acceptés, et seulement ceux-là
MAX_FILE_MB = 25
MAX_FILES = 20
RUN_ID = re.compile(r"^clean_\d{8}T\d{6,12}Z$")

app = FastAPI(title="BI Flow - Agent Quality & Cleaning", version="2.0")
JOBS: dict[str, dict] = {}
SESSIONS: dict[str, cleaning.CleaningSession] = {}   # runs en attente de la réponse de l'utilisateur
LOCK = threading.Lock()


# --------------------------------------------------------------------------- utilitaires
def safe_name(name: str) -> str:
    base = Path(name or "fichier").name
    return re.sub(r"[^0-9A-Za-z._-]+", "_", base)[:120] or "fichier"


def run_dir(run_id: str) -> Path:
    if not RUN_ID.match(run_id):
        raise HTTPException(404, "Run inconnu")
    d = HISTORY / "runs" / run_id
    if not (d / "view.json").is_file():
        raise HTTPException(404, "Run inconnu")
    return d


def set_job(job_id: str, **kw):
    with LOCK:
        JOBS[job_id].update(kw)


# --------------------------------------------------------------------------- exécution d'un job
def start(job_id: str, files: list[Path], planner: str, impute: bool, model: str | None, api_key: str | None):
    try:
        set_job(job_id, status="running", stage="Analyse des tables" + (" par le LLM" if planner == "llm" else "") + " et nettoyage")
        session = cleaning.CleaningSession(files, WORKSPACE / job_id / "clean", HISTORY, impute=impute,
                                           planner_mode=planner, model=model, api_key=api_key)
        if session.questions:
            with LOCK:
                SESSIONS[job_id] = session
            set_job(job_id, status="waiting", stage="Votre accord est nécessaire", questions=session.questions,
                    planner=session.tracer.planner)
        else:
            finish(job_id, session, {})
    except Exception as exc:
        traceback.print_exc()
        set_job(job_id, status="error", stage="Erreur", error=str(exc))
    finally:
        shutil.rmtree(WORKSPACE / job_id / "uploads", ignore_errors=True)


def finish(job_id: str, session: cleaning.CleaningSession, answers: dict[str, str]):
    try:
        set_job(job_id, status="running", stage="Application de vos choix et préparation de la comparaison")
        summary = session.finish(answers)
        set_job(job_id, status="done", stage="Terminé", result=summary["view"], questions=None)
    except Exception as exc:
        traceback.print_exc()
        set_job(job_id, status="error", stage="Erreur", error=str(exc))
    finally:
        shutil.rmtree(WORKSPACE / job_id, ignore_errors=True)


# --------------------------------------------------------------------------- API
@app.get("/api/config")
def config():
    llm_planner.load_env()
    return {"allowed_extensions": sorted(ALLOWED), "max_file_mb": MAX_FILE_MB, "max_files": MAX_FILES,
            "groq_key_configured": bool(os.environ.get("GROQ_API_KEY")),
            "default_model": os.environ.get("GROQ_MODEL") or llm_planner.PREFERRED_MODELS[0],
            "models": llm_planner.PREFERRED_MODELS}


@app.post("/api/jobs")
async def create_job(files: list[UploadFile] = File(...), planner: str = Form("llm"), impute: bool = Form(False),
                     model: str = Form(""), groq_api_key: str = Form("")):
    if planner not in {"llm", "rules"}:
        raise HTTPException(400, "planner doit valoir 'llm' ou 'rules'")
    if not files or len(files) > MAX_FILES:
        raise HTTPException(400, f"Déposez entre 1 et {MAX_FILES} fichiers")
    if model and model not in llm_planner.PREFERRED_MODELS:
        raise HTTPException(400, f"Modèle non proposé : {model}")
    job_id = uuid.uuid4().hex[:12]
    up = WORKSPACE / job_id / "uploads"
    up.mkdir(parents=True)
    saved = []
    for f in files:
        name = safe_name(f.filename)
        data = await f.read()
        error = None
        if Path(name).suffix.lower() not in ALLOWED:
            error = f"Format refusé pour {name} : seuls {', '.join(sorted(ALLOWED))} sont acceptés"
        elif len(data) > MAX_FILE_MB * 1024 * 1024:
            error = f"{name} dépasse {MAX_FILE_MB} Mo"
        elif not data.strip():
            error = f"{name} est vide"
        if error:
            shutil.rmtree(WORKSPACE / job_id, ignore_errors=True)
            raise HTTPException(400, error)
        path = up / name
        path.write_bytes(data)
        saved.append(path)
    with LOCK:
        JOBS[job_id] = {"job_id": job_id, "status": "queued", "stage": "En attente",
                        "files": [p.name for p in saved], "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    # la clé saisie dans l'interface n'est ni stockée ni tracée : elle ne sert qu'à ce job
    threading.Thread(target=start, args=(job_id, saved, planner, impute, model or None, groq_api_key.strip() or None),
                     daemon=True).start()
    return {"job_id": job_id}


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    with LOCK:
        job = JOBS.get(job_id)
        if not job:
            raise HTTPException(404, "Job inconnu")
        return dict(job)


@app.post("/api/jobs/{job_id}/answers")
def answer_job(job_id: str, payload: dict = Body(...)):
    """Réponses de l'utilisateur aux questions (valeurs extrêmes) : {"answers": {"q1": "cap" | "keep", ...}}."""
    answers = payload.get("answers") or {}
    if not isinstance(answers, dict) or any(v not in {"cap", "keep"} for v in answers.values()):
        raise HTTPException(400, "Chaque réponse doit valoir 'cap' ou 'keep'")
    with LOCK:
        session = SESSIONS.pop(job_id, None)
    if session is None:
        raise HTTPException(409, "Ce run n'attend pas de réponse")
    threading.Thread(target=finish, args=(job_id, session, answers), daemon=True).start()
    return {"ok": True}


@app.get("/api/runs")
def list_runs():
    runs = []
    for d in sorted((HISTORY / "runs").glob("clean_*"), reverse=True)[:50]:
        view_file = d / "view.json"
        if not view_file.is_file():
            continue  # ancien run sans vue simplifiée
        v = json.loads(view_file.read_text(encoding="utf-8"))
        runs.append({"run_id": v["run_id"], "finished_at": v["finished_at"], "files": v["files"],
                     "tables": v["totals"]["tables"], "tables_to_process": v["totals"]["tables_to_process"],
                     "corrections": v["totals"]["corrections"]})
    return runs


@app.get("/api/runs/{run_id}")
def get_run(run_id: str):
    return json.loads((run_dir(run_id) / "view.json").read_text(encoding="utf-8"))


@app.get("/api/runs/{run_id}/report", response_class=HTMLResponse)
def get_report(run_id: str):
    return HTMLResponse((run_dir(run_id) / "comparaison.html").read_text(encoding="utf-8"))


@app.get("/api/runs/{run_id}/download")
def download(run_id: str):
    """ZIP simple : les tables nettoyées, le rapport avant / après et la trace."""
    d = run_dir(run_id)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted((d / "after").glob("*.csv")):
            z.write(p, f"tables_nettoyees/{p.name}")
        for name in ("comparaison.html", "trace.md"):
            if (d / name).is_file():
                z.write(d / name, name)
    buf.seek(0)
    return StreamingResponse(buf, media_type="application/zip",
                             headers={"Content-Disposition": f'attachment; filename="nettoyage_{run_id}.zip"'})


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


app.mount("/static", StaticFiles(directory=STATIC), name="static")
