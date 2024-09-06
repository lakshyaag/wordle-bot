from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from .nodes import check_attempt, get_guess, next_guess
from .state import AgentState

workflow = StateGraph(AgentState)

workflow.add_node("get_guess", get_guess)
workflow.add_node("check_attempt", check_attempt)
workflow.set_entry_point("get_guess")
workflow.add_edge("get_guess", "check_attempt")
workflow.add_conditional_edges(
    "check_attempt", next_guess, {"continue": "get_guess", "end": END}
)


graph = workflow.compile(checkpointer=MemorySaver())
