from dotenv import load_dotenv
load_dotenv()  
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

class State(TypedDict):
    messages: Annotated[list, add_messages]


#Creating Nodes
def chatbot(state:State):
    res = llm.invoke(state.get("messages"))
    return {"messages": [res]}

def samplenode(state:State):
    print("\n\nInside the sample node.",state)
    return {"messages": ["This is a sample node."]}

graph_builder = StateGraph(State)


graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("samplenode",samplenode)

#Creating Edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

# (START) --> chatbot --> samplenode --> (END)


graph = graph_builder.compile()


updated_state = graph.invoke(State({"messages": ["Hi, I am Yuval"]}))
print("\n\nUpdated Graph State:", updated_state)