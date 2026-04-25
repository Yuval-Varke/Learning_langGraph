from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_message
from langgraph.graph import StateGraph

class State(TypedDict):
    messages: Annotated[list, add_message]


graph_builder = StateGraph(State)