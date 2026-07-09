from langchain_core.messages import HumanMessage

from .workflow import create_react_workflow


def main() -> None:
    workflow = create_react_workflow()
    result = workflow.invoke(
        {
            "messages": [HumanMessage(content="Divide 6790 by 5")],
            "input_file": None,
        }
    )

    for message in result["messages"]:
        message.pretty_print()


if __name__ == "__main__":
    main()
