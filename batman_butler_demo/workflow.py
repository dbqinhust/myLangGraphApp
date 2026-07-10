from langchain_core.messages import SystemMessage
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from .gemini_client import create_gemini_model
from .state import AgentState
from .tools import TOOLS


TOOL_DESCRIPTION = """
extract_text(img_path: str) -> str:
    Extract text from a local image file using Gemini vision.

divide(a: int, b: int) -> float:
    Divide a and b.
"""


def assistant(state: AgentState) -> dict:
    model = create_gemini_model()
    model_with_tools = model.bind_tools(TOOLS)
    image = state["input_file"]
    system_message = SystemMessage(
        content=(
            "You are a helpful butler named Alfred who serves Mr. Wayne and "
            "Batman. You can analyze documents and run computations with these "
            f"tools:\n{TOOL_DESCRIPTION}\n"
            f"Currently loaded image: {image}"
        )
    )

    return {
        "messages": [model_with_tools.invoke([system_message] + state["messages"])],
        "input_file": image,
    }


def create_react_workflow():
    builder = StateGraph(AgentState)

    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(TOOLS))

    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")

    return builder.compile()
