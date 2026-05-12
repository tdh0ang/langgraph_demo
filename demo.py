from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# -------------------------
# Shared state
# -------------------------
class DemoState(TypedDict):
    user_input: str
    intent: str
    response: str


# -------------------------
# Nodes
# -------------------------

def classify_intent(state: DemoState):
    text = state["user_input"].lower()

    if any(word in text for word in ["add", "multiply", "math"]):
        intent = "math"
    else:
        intent = "general"

    print(f"[classifier] detected intent: {intent}")

    return {"intent": intent}


def handle_math(state: DemoState):
    print("[math node] running fake math logic")

    return {
        "response": "Pretend I solved a math problem here."
    }


def handle_general(state: DemoState):
    print("[general node] running fake chatbot logic")

    return {
        "response": "Pretend this came from an LLM."
    }


# -------------------------
# Router
# -------------------------

def route_intent(state: DemoState):
    return state["intent"]


# -------------------------
# Build graph
# -------------------------

graph = StateGraph(DemoState)

graph.add_node("classifier", classify_intent)
graph.add_node("math_handler", handle_math)
graph.add_node("general_handler", handle_general)

graph.add_edge(START, "classifier")

graph.add_conditional_edges(
    "classifier",
    route_intent,
    {
        "math": "math_handler",
        "general": "general_handler",
    },
)

graph.add_edge("math_handler", END)
graph.add_edge("general_handler", END)

app = graph.compile()


# -------------------------
# Run it
# -------------------------

result = app.invoke({
    "user_input": "can you add numbers?" # Or "Hello World"
})

print("\nFINAL STATE:")
print(result)

# =====================================================
# Export Mermaid Diagram
# =====================================================

mermaid_diagram = app.get_graph().draw_mermaid()

with open("workflow.mmd", "w") as f:
    f.write(mermaid_diagram)

print("\nMermaid diagram exported:")
print(" - workflow.mmd")


# =====================================================
# Export PNG Diagram
# =====================================================

try:
    png_data = app.get_graph().draw_mermaid_png()

    with open("workflow.png", "wb") as f:
        f.write(png_data)

    print(" - workflow.png")

except Exception as e:
    print("\nPNG generation failed.")
    print("You may need Graphviz installed.")
    print(f"Error: {e}")