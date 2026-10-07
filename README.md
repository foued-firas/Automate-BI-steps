# BI Flow : agents données (Quality & Cleaning, traçage, ETL)

Partie « données » du projet BI Flow (ESPRIT 5DS 2026/2027, voir `docs/BI_Flow_Report.pdf`) :
automatiser les étapes Power Query et modélisation de Power BI avec des agents traçables.

```
Interface web ─► CSV / Excel ─► Agent Quality & Cleaning ─► data/clean ─► Agent ETL ─► data/gold (schéma en étoile) ─► Power BI
                 │   ▲ outil LLM Groq (optionnel)             │
                 ▼                                             ▼
             history/ (agent de traçage)            etl_contract.json, etl_lineage.json
```

## Démarrage

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows  (Mac / Linux : source .venv/bin/activate)
pip install -r requirements.txt
cp .env.example .env              # puis renseigner GROQ_API_KEY (Windows : copy .env.example .env)
```

### Application web (recommandé)

```bash
uvicorn web.app:app --reload
```
Ouvrir http://127.0.0.1:8000, déposer des fichiers **CSV ou Excel (.csv, .xlsx, .xlsm)**, choisir « LLM Groq » et lancer.
L'interface affiche l'analyse du LLM par table, les corrections appliquées ou refusées, les points à valider,
le statut de l'ETL, le rapport avant / après et un ZIP téléchargeable du run.
L'ETL (schéma en étoile) se lance automatiquement si les 7 tables du modèle sont déposées
(categories, customers, employees, order_details, orders, products, shippers).
Si la clé n'est pas dans `.env`, on peut la saisir dans l'interface : elle sert au run et n'est pas enregistrée.

### En ligne de commande

```bash
python run_pipeline.py                          # nettoie data/raw puis construit data/gold
python run_pipeline.py a.csv b.xlsx --planner llm
```

### Tests

```bash
python -m pytest cleaning_agent/tests web/tests
```

## Contenu

| Dossier | Contenu |
|---|---|
| `cleaning_agent/` | agent de nettoyage (15 outils), outil LLM Groq, agent de traçage, comparaison avant / après, tests, jeu de démonstration sale. Voir son README. |
| `etl_agent/` | agent ETL : schéma en étoile (`fact_sales`, `fact_orders`, 5 dimensions), contrôles, contrat JSON, lineage, requêtes Power Query M. Voir son README. |
| `data/raw/` | dataset source (7 CSV Northwind) |
| `data/clean/` | tables nettoyées |
| `data/gold/` | modèle en étoile prêt pour Power BI |
| `history/` | historique de tous les runs de nettoyage (journal, versions avant / après, traces, rapports HTML) |
| `web/` | application web : backend FastAPI (`app.py`), frontend (`static/`), tests |
| `run_pipeline.py` | orchestrateur Cleaning -> ETL (LangGraph si installé, sinon séquentiel) |
| `docs/` | rapport d'architecture BI Flow |
