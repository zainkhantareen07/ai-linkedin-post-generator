import json
import re
from typing import Any
import os
from prompts import SYSTEM_PROMPT, build_generation_prompt, build_modifier_prompt


# Note: We expect a configured `openai` module instance to be passed in as `client`.


def _parse_json_response(raw: str) -> dict:
    """Safely parse JSON from Gemini response, stripping markdown fences if present."""
    # Strip markdown code fences
    cleaned = re.sub(r"```json(.*?)```", r"\1", raw, flags=re.DOTALL)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse JSON from response: {cleaned}")


def _call_chat(client: Any, user_prompt: str, model: str = "grok-2-1218", temperature: float = 0.6, max_tokens: int = 800) -> str:
    """Call OpenAI-compatible ChatCompletion (Grok) and return the assistant content."""
    # Build messages: system prompt + user prompt
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    resp = client.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # OpenAI-style response: choices[0].message.content
    try:
        return resp["choices"][0]["message"]["content"]
    except Exception as e:
        # Some clients may return slightly different shapes; try attribute access
        try:
            return resp.choices[0].message.content  # type: ignore
        except Exception:
            raise RuntimeError(f"Unexpected response shape from model: {e}")


def generate_post(topic: str, tone: str, client: Any) -> dict:
    """Generate a new LinkedIn post JSON using the configured client."""
    prompt = build_generation_prompt(topic, tone)
    raw = _call_chat(client, prompt)
    return _parse_json_response(raw)


def modify_post(current_post: dict, modifier: str, client: Any) -> dict:
    """Modify an existing post (viral/shorten/emojis) and return the new JSON."""
    prompt = build_modifier_prompt(current_post, modifier)
    raw = _call_chat(client, prompt)
    return _parse_json_response(raw)
