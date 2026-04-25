from dotenv import load_dotenv
load_dotenv()  
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver  

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

class State(TypedDict):
    messages: Annotated[list, add_messages]


#Creating Nodes
def chatbot(state:State):
    res = llm.invoke(state.get("messages"))
    return {"messages": [res]}


graph_builder = StateGraph(State)


graph_builder.add_node("chatbot",chatbot)

#Creating Edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# (START) --> chatbot --> (END)


graph = graph_builder.compile()

def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

DB_URI = "mongodb://admin:admin@localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpoints = graph_builder.compile(checkpointer=checkpointer)
    config = {
        "configurable": {
            "thread_id": "elon_thread_1" 
        }
    }

    updated_state = graph_with_checkpoints.invoke(
        State({"messages": ["Hi, What is my name and what have I built ?"]}),
        config
    )
    print("\n\nUpdated Graph State:", updated_state)