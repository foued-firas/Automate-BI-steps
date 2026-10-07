"""Orchestrateur BI Flow (partie données) : Quality & Cleaning -> ETL.

Utilise LangGraph s'il est installé, sinon enchaîne les nœuds dans l'ordre (même contrat d'état).
  python run_pipeline.py                              # data/raw, règles
  python run_pipeline.py fichiers.xlsx a.csv --planner llm
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / "cleaning_agent"), str(ROOT / "etl_agent")]
from agent import cleaning_node  # noqa: E402
from etl_agent import etl_node  # noqa: E402


def stop_if_ko(state: dict) -> str:
    return "end" if state.get("cleaning_status") == "KO" else "etl"


def build_graph():
    from typing import TypedDict

    from langgraph.graph import END, StateGraph

    class State(TypedDict, total=False):
        input_paths: list
        planner: str
        clean_data_dir: str
        model_dir: str
        cleaning_status: str
        cleaning_run_id: str
        cleaning_trace: str
        cleaning_report: str
        cleaning_error: str
        needs_human_validation: list
        etl_status: str
        etl_error: str
        etl_contract: dict

    g = StateGraph(State)
    g.add_node("cleaning", cleaning_node)
    g.add_node("etl", etl_node)
    g.set_entry_point("cleaning")
    g.add_conditional_edges("cleaning", stop_if_ko, {"etl": "etl", "end": END})
    g.add_edge("etl", END)
    return g.compile()


def run(state: dict) -> dict:
    try:
        return build_graph().invoke(state)
    except ImportError:
        state.update(cleaning_node(state))
        if stop_if_ko(state) == "etl":
            state.update(etl_node(state))
        return state


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Pipeline BI Flow : nettoyage puis modèle en étoile")
    p.add_argument("inputs", nargs="*", default=[str(ROOT / "data" / "raw")])
    p.add_argument("--planner", choices=["rules", "llm"], default="rules")
    a = p.parse_args()
    s = run({"input_paths": a.inputs, "planner": a.planner,
             "clean_data_dir": str(ROOT / "data" / "clean"), "model_dir": str(ROOT / "data" / "gold")})
    print(f"Nettoyage : {s.get('cleaning_status')} (run {s.get('cleaning_run_id')})")
    print(f"  rapport : {s.get('cleaning_report')}")
    for item in s.get("needs_human_validation", []):
        print(f"  à valider : {item}")
    print(f"ETL : {s.get('etl_status')} {s.get('etl_error', '')}")
