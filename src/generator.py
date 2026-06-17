import os

import openai

from prompts import (
    BASE_USER_TEMPLATE,
    EMOJI_PROMPT,
    SHORTEN_PROMPT,
    SYSTEM_PROMPT,
    VIRAL_PROMPT,
)
from utils import parse_openai_response


def _get_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not set in environment")
    return api_key


def _call_openai(prompt: str, temperature: float = 0.8) -> dict:
    openai.api_key = _get_api_key()
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=700,
    )
    text = completion.choices[0].message.content.strip()
    return parse_openai_response(text)


def generate_post(topic: str, tone: str) -> dict:
    prompt = BASE_USER_TEMPLATE.format(topic=topic, tone=tone)
    return _call_openai(prompt)


def make_more_viral(current: dict) -> dict:
    prompt = f"{VIRAL_PROMPT}\nCurrent JSON:\n{current}"
    return _call_openai(prompt)


def shorten_post(current: dict) -> dict:
    prompt = f"{SHORTEN_PROMPT}\nCurrent JSON:\n{current}"
    return _call_openai(prompt)


def add_emojis(current: dict) -> dict:
    prompt = f"{EMOJI_PROMPT}\nCurrent JSON:\n{current}"
    return _call_openai(prompt)
