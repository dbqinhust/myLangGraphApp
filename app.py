from email_workflow import create_initial_state, create_workflow
from sample_emails import LEGITIMATE_EMAIL, SPAM_EMAIL


def process_email(label: str, email: dict) -> None:
    print(f"\nProcessing {label} email...")
    workflow = create_workflow()
    workflow.invoke(create_initial_state(email))


if __name__ == "__main__":
    process_email("legitimate", LEGITIMATE_EMAIL)
    process_email("spam", SPAM_EMAIL)
