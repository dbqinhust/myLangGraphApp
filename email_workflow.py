from typing import Any, Dict

from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph

from email_state import EmailState
from gemini_client import create_gemini_model, response_text


def create_initial_state(email: Dict[str, Any]) -> EmailState:
    return {
        "email": email,
        "is_spam": None,
        "spam_reason": None,
        "email_category": None,
        "email_draft": None,
        "messages": [],
    }


def read_email(state: EmailState) -> dict:
    email = state["email"]
    print(
        f"Alfred is processing an email from {email['sender']} "
        f"with subject: {email['subject']}"
    )
    return {}


def classify_email(state: EmailState) -> dict:
    email = state["email"]
    model = create_gemini_model()
    prompt = f"""
    As Alfred the butler, analyze this email and determine if it is spam or legitimate.

    Email:
    From: {email['sender']}
    Subject: {email['subject']}
    Body: {email['body']}

    First, determine if this email is spam. If it is spam, explain why.
    If it is legitimate, categorize it (inquiry, complaint, thank you, etc.).
    """

    response = model.invoke([HumanMessage(content=prompt)])
    text = response_text(response)
    normalized_text = text.lower()
    is_spam = "spam" in normalized_text and "not spam" not in normalized_text

    spam_reason = None
    if is_spam and "reason:" in normalized_text:
        spam_reason = text.split("reason:", 1)[1].strip()

    email_category = None
    if not is_spam:
        categories = ["inquiry", "complaint", "thank you", "request", "information"]
        email_category = next(
            (category for category in categories if category in normalized_text),
            None,
        )

    return {
        "is_spam": is_spam,
        "spam_reason": spam_reason,
        "email_category": email_category,
        "messages": state.get("messages", [])
        + [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": text},
        ],
    }


def handle_spam(state: EmailState) -> dict:
    print(f"Alfred has marked the email as spam. Reason: {state['spam_reason']}")
    print("The email has been moved to the spam folder.")
    return {}


def draft_response(state: EmailState) -> dict:
    email = state["email"]
    category = state["email_category"] or "general"
    model = create_gemini_model()
    prompt = f"""
    As Alfred the butler, draft a polite preliminary response to this email.

    Email:
    From: {email['sender']}
    Subject: {email['subject']}
    Body: {email['body']}

    This email has been categorized as: {category}

    Draft a brief, professional response that Mr. Hugg can review and personalize before sending.
    """

    response = model.invoke([HumanMessage(content=prompt)])
    text = response_text(response)

    return {
        "email_draft": text,
        "messages": state.get("messages", [])
        + [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": text},
        ],
    }


def notify_mr_hugg(state: EmailState) -> dict:
    email = state["email"]

    print("\n" + "=" * 50)
    print(f"Sir, you've received an email from {email['sender']}.")
    print(f"Subject: {email['subject']}")
    print(f"Category: {state['email_category']}")
    print("\nI've prepared a draft response for your review:")
    print("-" * 50)
    print(state["email_draft"])
    print("=" * 50 + "\n")
    return {}


def route_email(state: EmailState) -> str:
    if state["is_spam"]:
        return "spam"

    return "legitimate"


def create_workflow():
    email_graph = StateGraph(EmailState)

    email_graph.add_node("read_email", read_email)
    email_graph.add_node("classify_email", classify_email)
    email_graph.add_node("handle_spam", handle_spam)
    email_graph.add_node("draft_response", draft_response)
    email_graph.add_node("notify_mr_hugg", notify_mr_hugg)

    email_graph.add_edge(START, "read_email")
    email_graph.add_edge("read_email", "classify_email")
    email_graph.add_conditional_edges(
        "classify_email",
        route_email,
        {
            "spam": "handle_spam",
            "legitimate": "draft_response",
        },
    )
    email_graph.add_edge("handle_spam", END)
    email_graph.add_edge("draft_response", "notify_mr_hugg")
    email_graph.add_edge("notify_mr_hugg", END)

    return email_graph.compile()
