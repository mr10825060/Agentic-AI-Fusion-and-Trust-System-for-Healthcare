from langgraph.graph import StateGraph

from agents.ingestion import ingestion_agent
from agents.cleaning import cleaning_agent
from agents.analysis import analysis_agent
from agents.fusion import fusion_agent
from agents.trust import trust_agent


def build_graph():
    graph = StateGraph(dict)

    # INGESTION NODE
    def ingest(state):
        state["data"] = ingestion_agent()
        return state

    # CLEANING NODE
    def clean(state):
        state["clean_data"] = cleaning_agent(state["data"])
        return state

    # ANALYSIS NODE
    def analyze(state):
        state["insights"] = analysis_agent(state["clean_data"])
        return state

    # FUSION NODE
    def fuse(state):
        state["fused"] = fusion_agent(state["clean_data"])
        return state

    # TRUST NODE
    def trust(state):
        scores, overall = trust_agent(state["clean_data"])
        state["trust_scores"] = scores
        state["overall_trust"] = overall
        return state

    # Add nodes
    graph.add_node("ingestion", ingest)
    graph.add_node("cleaning", clean)
    graph.add_node("analysis", analyze)
    graph.add_node("fusion", fuse)
    graph.add_node("trust", trust)

    # Flow setup
    graph.set_entry_point("ingestion")

    graph.add_edge("ingestion", "cleaning")
    graph.add_edge("cleaning", "analysis")
    graph.add_edge("analysis", "fusion")
    graph.add_edge("fusion", "trust")

    return graph.compile()