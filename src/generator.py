import json
from typing import Any
from prompts import SYSTEM_PROMPT, build_generation_prompt, build_modifier_prompt


def _parse_json(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1:
            return json.loads(raw[start:end + 1])
        raise ValueError("Invalid JSON from model")


def _call_groq(client: Any, prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )

    return response.choices[0].message.content


def generate_post(topic: str, tone: str, client: Any) -> dict:
    prompt = build_generation_prompt(topic, tone)
    raw = _call_groq(client, prompt)
    return _parse_json(raw)


def modify_post(post: dict, mode: str, client: Any) -> dict:
    prompt = build_modifier_prompt(post, mode)
    raw = _call_groq(client, prompt)
    return _parse_json(raw)