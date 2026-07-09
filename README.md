# Email Workflow with LangGraph and Gemini

This project is a small LangGraph demo that processes incoming emails with Gemini.
It acts like a simple assistant named Alfred:

1. Reads an incoming email.
2. Uses Gemini to classify it as spam or legitimate.
3. Routes spam emails to a spam handler.
4. Drafts a polite response for legitimate emails.
5. Prints the draft for review.

## Project Structure

- `email_assistant_demo/` - the complete email workflow demo package.
- `email_assistant_demo/app.py` - local entrypoint that runs the sample emails through the workflow.
- `email_assistant_demo/email_workflow.py` - LangGraph nodes, routing, and graph creation.
- `email_assistant_demo/email_state.py` - shared workflow state definition.
- `email_assistant_demo/gemini_client.py` - Gemini model setup and response text handling.
- `email_assistant_demo/sample_emails.py` - sample legitimate and spam emails used by the demo.
- `email_assistant_demo/langfuse_tracing_example.py` - optional Langfuse tracing example.
- `requirements.txt` - Python dependencies.

## Requirements

- Python 3.10+
- A Gemini API key from Google AI Studio

The app uses `langchain-google-genai`, which checks `GOOGLE_API_KEY` first and
then `GEMINI_API_KEY`.

## Local Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your Gemini API key in `.env`:

```env
GOOGLE_API_KEY=your-api-key
GEMINI_MODEL=gemini-2.5-flash
```

The `.env` file is ignored by Git so your key stays local.

## Run the Demo

From the project root:

```bash
python -m email_assistant_demo.app
```

The script processes one legitimate sample email and one spam sample email. You
will see Alfred's classification and response draft printed in the terminal.

## Verify Without Calling Gemini

You can check that the code imports and the graph builds without making a live
model request:

```bash
python -m py_compile email_assistant_demo/*.py
python -c "from email_assistant_demo.email_workflow import create_workflow; create_workflow(); print('workflow ok')"
```

## Run With Langfuse Tracing

Add your Langfuse credentials to `.env`:

```env
LANGFUSE_PUBLIC_KEY=your-public-key
LANGFUSE_SECRET_KEY=your-secret-key
LANGFUSE_HOST=https://cloud.langfuse.com
```

Then run:

```bash
python -m email_assistant_demo.langfuse_tracing_example
```
