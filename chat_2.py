from dotenv import load_dotenv
from groq import Groq
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Optional,Literal
from google import genai
import os

load_dotenv()


gemini_client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional [bool]


def chatbot_gemini(state:State):
    print("\n\nInside the Gemini Node.",state)
    res = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=state.get("user_query")
    )
    state['llm_output'] = res.text
    return state

def evaluate_response(state:State) -> Literal["chatbot_groq", "endnode"]: 
    print("\n\nEvaluating the response from Gemini.",state)
    if False:
        return "endnode"
    return "chatbot_groq"

def chatbot_groq(state:State):
    print("\n\nInside the Groq Node.",state)
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": state.get("user_query")
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    state['llm_output'] = chat_completion.choices[0].message.content
    return state

def endnode(state:State):
    print("\n\nInside the End Node.",state)
    print("\n\nFinal LLM Output:", state.get("llm_output"))
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("chatbot_groq", chatbot_groq)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot_gemini")
graph_builder.add_conditional_edges("chatbot_gemini",evaluate_response)

graph_builder.add_edge("chatbot_groq", "endnode")
graph_builder.add_edge("endnode", END) 


graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "What is 2 times the cube of 2 ?"}))
print("\n\nUpdated Graph State:", updated_state)