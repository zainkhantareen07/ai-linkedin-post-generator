SYSTEM_PROMPT = """You are a viral LinkedIn content strategist.

Return ONLY valid JSON.

Structure:
{
  "hook": "",
  "post": "",
  "cta": "",
  "hashtags": [],
  "alternate_versions": {
    "formal": "",
    "casual": "",
    "viral": ""
  }
}

Rules:
- No markdown
- No explanations
- No extra text
- Human storytelling style
- No corporate buzzwords
"""

def build_generation_prompt(topic: str, tone: str) -> str:
    return f"""
Create a LinkedIn post.

Topic: {topic}
Tone: {tone}

Return ONLY JSON.
"""


def build_modifier_prompt(post: dict, mode: str) -> str:
    return f"""
Modify this LinkedIn post.

Mode: {mode}

Post:
{post}

Return ONLY JSON.
"""