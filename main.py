"""Point d'entrée : lance le pipeline BI (pour l'instant, l'Agent 1 de profilage).

    python main.py
    python main.py --data "Datasets/Import&Export/data" --context "Ventes import/export"
"""

import argparse
import sys

from src.config import DEFAULT_DATA_DIR
from src.graph import build_pipeline


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Pipeline BI — Agent 1 : profilage")
    parser.add_argument("--data", default=str(DEFAULT_DATA_DIR), help="Dossier des CSV")
    parser.add_argument("--context", default=None, help="Contexte métier pour le LLM")
    args = parser.parse_args()

    state = build_pipeline().invoke(
        {"input": {"source_dir": args.data, "business_context": args.context}}
    )

    prof = state["profiling"]
    summary = prof["summary"]
    print(f"\nTables : {summary['tables_count']} | Lignes : {summary['total_rows']} "
          f"| Problèmes : {summary['issues_count']} {summary['issues_by_severity']}")
    print(f"Score global de qualité : {summary['global_quality_score']}/100")
    print(f"LLM : {prof['metadata']['llm']['status']}")
    for err in state.get("errors", []):
        print(f"  ! [{err['node']}] {err['table'] or ''} {err['error']}")
    print(f"\nRapport JSON     : {prof['artifacts']['json_report']}")
    print(f"Rapport Markdown : {prof['artifacts']['markdown_report']}")


if __name__ == "__main__":
    main()
