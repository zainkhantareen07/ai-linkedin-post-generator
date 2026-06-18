import json
from datetime import datetime


def format_full_linkedin_post(post: dict) -> str:
    return "\n\n".join([
        post.get("hook", ""),
        post.get("post", ""),
        post.get("cta", ""),
        " ".join(post.get("hashtags", []))
    ])


def format_post_for_export(post: dict, topic: str, tone: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""
AI LinkedIn Post Generator

Generated: {now}
Topic: {topic}
Tone: {tone}

HOOK:
{post.get("hook", "")}

POST:
{post.get("post", "")}

CTA:
{post.get("cta", "")}

HASHTAGS:
{" ".join(post.get("hashtags", []))}
"""


def count_words(text: str) -> int:
    return len(text.split()) if text else 0


def validate_inputs(topic: str):
    if not topic or len(topic.strip()) < 5:
        return False, "Topic too short"
    if len(topic) > 500:
        return False, "Topic too long"
    return True, ""