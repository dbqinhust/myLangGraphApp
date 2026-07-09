from dotenv import load_dotenv
from langfuse.langchain import CallbackHandler

from email_workflow import create_initial_state, create_workflow
from sample_emails import LEGITIMATE_EMAIL


load_dotenv()


def main() -> None:
    workflow = create_workflow()
    langfuse_handler = CallbackHandler()

    legitimate_result = workflow.invoke(
        input=create_initial_state(LEGITIMATE_EMAIL),
        config={"callbacks": [langfuse_handler]},
    )

    print("Langfuse-traced workflow completed.")
    print(f"Spam: {legitimate_result['is_spam']}")
    print(f"Category: {legitimate_result['email_category']}")
    print(f"Draft response:\n{legitimate_result['email_draft']}")


if __name__ == "__main__":
    main()
