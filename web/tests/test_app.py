"""Tests de l'API web (sans appel Groq réel) : python -m pytest web/tests"""
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from fastapi.testclient import TestClient  # noqa: E402

import web.app as webapp  # noqa: E402

_TMP = Path(tempfile.mkdtemp())
webapp.HISTORY, webapp.WORKSPACE = _TMP / "history", _TMP / "workspace"  # ne pas polluer l'historique réel
client = TestClient(webapp.app)
SAMPLES = ROOT / "cleaning_agent" / "samples"


def wait(job_id, until=("done", "error", "waiting")):
    for _ in range(120):
        job = client.get(f"/api/jobs/{job_id}").json()
        if job["status"] in until:
            return job
        time.sleep(0.5)
    raise TimeoutError


def upload(paths, planner="rules"):
    files = [("files", (p.name, p.read_bytes(), "application/octet-stream")) for p in paths]
    return client.post("/api/jobs", files=files, data={"planner": planner})


def test_config_et_page():
    c = client.get("/api/config").json()
    assert c["allowed_extensions"] == [".csv", ".xlsm", ".xlsx"]
    assert "openai/gpt-oss-120b" in c["models"]
    assert "Glissez vos fichiers" in client.get("/").text


def test_format_refuse():
    r = client.post("/api/jobs", files=[("files", ("notes.txt", b"a,b\n1,2", "text/plain"))], data={"planner": "rules"})
    assert r.status_code == 400 and "Format refusé" in r.json()["detail"]
    r = client.post("/api/jobs", files=[("files", ("vide.csv", b"  ", "text/csv"))], data={"planner": "rules"})
    assert r.status_code == 400


def test_accord_utilisateur_sur_les_valeurs_extremes():
    job_id = upload([SAMPLES / "clients_sale.csv", SAMPLES / "ventes_sale.xlsx"]).json()["job_id"]
    job = wait(job_id)
    assert job["status"] == "waiting", job
    q = next(q for q in job["questions"] if q["table"] == "ventes_sale_produits")
    assert 9999 in q["examples"]
    assert client.post(f"/api/jobs/{job_id}/answers", json={"answers": {q["id"]: "oui"}}).status_code == 400
    answers = {x["id"]: "keep" for x in job["questions"]} | {q["id"]: "cap"}
    assert client.post(f"/api/jobs/{job_id}/answers", json={"answers": answers}).status_code == 200
    assert client.post(f"/api/jobs/{job_id}/answers", json={"answers": answers}).status_code == 409
    job = wait(job_id, until=("done", "error"))
    assert job["status"] == "done", job
    v = job["result"]
    assert "etl" not in v and "needs_human_validation" not in v
    prod = next(t for t in v["tables"] if t["name"] == "ventes_sale_produits")
    assert any(a["tool"] == "cap_outliers" for a in prod["actions"])
    assert client.get(f"/api/runs/{v['run_id']}").json()["run_id"] == v["run_id"]
    assert "Nettoyage : avant / après" in client.get(f"/api/runs/{v['run_id']}/report").text
    z = client.get(f"/api/runs/{v['run_id']}/download")
    assert z.status_code == 200 and z.content[:2] == b"PK"
    assert any(x["run_id"] == v["run_id"] for x in client.get("/api/runs").json())


def test_tables_propres_non_affichees():
    raw = ROOT / "data" / "raw"
    job_id = upload([raw / "categories.csv", raw / "shippers.csv", raw / "customers.csv"], planner="llm").json()["job_id"]
    job = wait(job_id)
    if job["status"] == "waiting":
        client.post(f"/api/jobs/{job_id}/answers", json={"answers": {}})
        job = wait(job_id, until=("done", "error"))
    v = job["result"]
    assert set(v["clean_tables"]) == {"categories", "shippers"}
    assert [t["name"] for t in v["tables"]] == ["customers"]      # seule table à traiter : 1 double espace
    assert v["planner"]["mode"] in {"llm", "rules"}               # sans clé : repli règles, signalé


def test_run_inconnu():
    assert client.get("/api/runs/../../etc").status_code == 404
    assert client.get("/api/runs/clean_20990101T000000Z").status_code == 404
