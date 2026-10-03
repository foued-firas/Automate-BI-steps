"""Graphe global du pipeline BI : chaque agent est un sous-graphe branché ici.

Pour ajouter l'Agent 2 (cleaning) :
    graph.add_node("cleaning", build_cleaning_graph())
    graph.add_edge("profiling", "cleaning")
    graph.add_edge("cleaning", END)
"""

from langgraph.graph import END, START, StateGraph

from src.agents.profiling import build_profiling_graph
from src.state import BIState


def build_pipeline():
    graph = StateGraph(BIState)
    graph.add_node("profiling", build_profiling_graph())
    graph.add_edge(START, "profiling")
    graph.add_edge("profiling", END)
    return graph.compile()
