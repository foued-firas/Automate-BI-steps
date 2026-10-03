"""State global partagé par tous les agents du pipeline BI.

Chaque agent possède sa propre section et n'écrit que dans celle-ci :
    input      -> entrées communes (orchestrateur / utilisateur)
    profiling  -> Agent 1 : profilage & diagnostic qualité
    cleaning   -> Agent 2 : data quality & cleaning
    kpi, modeling, dashboard -> agents suivants

Règle : aucune DataFrame dans le state, uniquement des chemins et des
résultats sérialisables en JSON.
"""

import operator
from typing import Annotated, Any, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


def merge_section(left: dict | None, right: dict | None) -> dict:
    """Fusion superficielle : un nœud ne renvoie que les clés qu'il met à jour."""
    return {**(left or {}), **(right or {})}


class InputSection(TypedDict, total=False):
    source_dir: str  # dossier contenant les CSV
    files: list[str]  # optionnel : restreindre à certains fichiers
    business_context: str  # optionnel : contexte métier pour le LLM


class ProfilingSection(TypedDict, total=False):
    """Sortie de l'Agent 1 (voir docs/spec_agent1_profiling.md)."""

    metadata: dict[str, Any]
    tables: list[dict[str, Any]]
    relationships: list[dict[str, Any]]
    issues: list[dict[str, Any]]
    summary: dict[str, Any]
    artifacts: dict[str, str]  # chemins des rapports exportés (JSON, Markdown)


class BIState(TypedDict, total=False):
    input: InputSection
    profiling: Annotated[ProfilingSection, merge_section]
    cleaning: Annotated[dict[str, Any], merge_section]
    kpi: Annotated[dict[str, Any], merge_section]
    modeling: Annotated[dict[str, Any], merge_section]
    dashboard: Annotated[dict[str, Any], merge_section]
    errors: Annotated[list[dict[str, Any]], operator.add]
    # Optionnel : historique pour les agents conversationnels / ReAct.
    messages: Annotated[list[AnyMessage], add_messages]
