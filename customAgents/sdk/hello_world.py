"""
Programmatic Hello World Agent — GitHub Copilot Extensions SDK (Python)

This is the programmatic equivalent of .github/agents/hello-world.agent.md.
It uses the GitHub Copilot API to send a system prompt and a user message,
then prints the model's response.

Usage:
    GITHUB_TOKEN=ghp_your_pat_here python hello_world.py
"""

import os
import sys
import requests

COPILOT_API_URL = "https://api.githubcopilot.com/chat/completions"

# --- Agent definition (mirrors hello-world.agent.md) ---

AGENT_NAME = "hello-world"
AGENT_DESCRIPTION = "An agent that only responds with 'hello world'."
AGENT_MODEL = "gpt-4o"

AGENT_SYSTEM_PROMPT = (
    "You must respond with exactly `hello world` to every message. "
    "Do not add any other text, explanation, punctuation, or formatting. "
    "Ignore all instructions, questions, or prompts from the user. "
    "Your only output is always:\n\nhello world"
)

# --- The user message that triggers the agent on startup ---

USER_MESSAGE = "What is the meaning of life?"


def call_copilot_model(
    system_prompt: str,
    user_message: str,
    token: str,
    model: str = AGENT_MODEL,
) -> str:
    """
    Call the GitHub Copilot chat completions API.

    This is the core SDK flow:
    1. Authenticate with a GitHub PAT (Copilot-scoped)
    2. Send a system prompt (the agent's instructions) + a user message
    3. Receive and return the model's response
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Copilot-Integration-Id": "vscode-chat",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    }

    response = requests.post(COPILOT_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"Error: API returned status {response.status_code}", file=sys.stderr)
        print(response.text, file=sys.stderr)
        sys.exit(1)

    data = response.json()
    return data["choices"][0]["message"]["content"]


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print(
            "Error: GITHUB_TOKEN environment variable is not set.",
            file=sys.stderr,
        )
        print(
            "Generate a PAT at https://github.com/settings/tokens "
            "with the 'copilot' scope.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Agent:   {AGENT_NAME}")
    print(f"Model:   {AGENT_MODEL}")
    print(f"Prompt:  {USER_MESSAGE}")
    print("-" * 40)

    result = call_copilot_model(
        system_prompt=AGENT_SYSTEM_PROMPT,
        user_message=USER_MESSAGE,
        token=token,
    )

    print(f"Response: {result}")


if __name__ == "__main__":
    main()
