SYSTEM_PROMPT = """You are a viral LinkedIn content strategist with 10+ years of experience crafting posts that drive real engagement.

Your writing is human, story-driven, and avoids all corporate buzzwords and cringe language.

You MUST return ONLY valid JSON — no markdown, no backticks, no explanation. Just raw JSON.

Return this exact structure:
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
- hook: Max 1-2 punchy lines. Must stop the scroll. No fluff.
- post: Structured in short paragraphs (2-3 sentences each). Human, storytelling-based.
- cta: Clear, specific, non-generic call to action. NOT "Let me know your thoughts."
- hashtags: 3-6 relevant hashtags (without the # symbol in the array values, add # in values)
- alternate_versions: Three full rewrites of the post body only (not hook/cta):
    - formal: polished, executive-level, authoritative
    - casual: conversational, friendly, like texting a colleague
    - viral: high-energy, bold, controversial or surprising angle
- NEVER use: "synergy", "leverage", "game-changer", "thrilled to announce", "excited to share", "humbled"
- DO use: specific details, numbers, real stories, tension, vulnerability where appropriate
"""

MAKE_VIRAL_PROMPT = """Take this LinkedIn post and make it significantly more viral.

Techniques to apply:
- Add a bold, controversial or counterintuitive opening claim
- Use pattern interrupts (unexpected line breaks, one-word sentences)
- Add specificity (real numbers, timeframes, names if appropriate)
- Create tension or stakes early
- End with a question or statement that demands engagement

Return ONLY valid JSON in this exact structure:
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
"""

SHORTEN_PROMPT = """Shorten this LinkedIn post to make it more punchy and scannable.

Rules:
- Keep the core message and hook
- Cut filler words, redundant sentences, any fluff
- Target 30-40% shorter
- Each paragraph max 2 sentences
- Keep the emotional core intact

Return ONLY valid JSON in this exact structure:
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
"""

ADD_EMOJIS_PROMPT = """Add strategic emojis to this LinkedIn post to increase engagement and scannability.

Rules:
- Use emojis at the start of key paragraphs as visual bullets
- Add 1-2 emojis to the hook for impact
- Add relevant emojis to hashtags
- Don't overdo it — max 8-10 emojis total
- Choose emojis that match the tone and topic
- Keep the text itself unchanged except for emoji additions

Return ONLY valid JSON in this exact structure:
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
"""
=======

Rules:
- hook: Max 1-2 punchy lines. Must stop the scroll. No fluff.
- post: Structured in short paragraphs (2-3 sentences each). Human, storytelling-based.
- cta: Clear, specific, non-generic call to action. NOT "Let me know your thoughts."
- hashtags: 3-6 relevant hashtags (without the # symbol in the array values, add # in values)
- alternate_versions: Three full rewrites of the post body only (not hook/cta):
    - formal: polished, executive-level, authoritative
    - casual: conversational, friendly, like texting a colleague
    - viral: high-energy, bold, controversial or surprising angle
- NEVER use: "synergy", "leverage", "game-changer", "thrilled to announce", "excited to share", "humbled"
- DO use: specific details, numbers, real stories, tension, vulnerability where appropriate
"""

MAKE_VIRAL_PROMPT = """Take this LinkedIn post and make it significantly more viral.

Techniques to apply:
- Add a bold, controversial or counterintuitive opening claim
- Use pattern interrupts (unexpected line breaks, one-word sentences)
- Add specificity (real numbers, timeframes, names if appropriate)
- Create tension or stakes early
- End with a question or statement that demands engagement

Return ONLY valid JSON in this exact structure:
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
"""

SHORTEN_PROMPT = """Shorten this LinkedIn post to make it more punchy and scannable.

Rules:
- Keep the core message and hook
- Cut filler words, redundant sentences, any fluff
- Target 30-40% shorter
- Each paragraph max 2 sentences
- Keep the emotional core intact

Return ONLY valid JSON in this exact structure:
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
"""

ADD_EMOJIS_PROMPT = """Add strategic emojis to this LinkedIn post to increase engagement and scannability.

Rules:
- Use emojis at the start of key paragraphs as visual bullets
- Add 1-2 emojis to the hook for impact
- Add relevant emojis to hashtags
- Don't overdo it — max 8-10 emojis total
- Choose emojis that match the tone and topic
- Keep the text itself unchanged except for emoji additions

Return ONLY valid JSON in this exact structure:
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
"""


def build_generation_prompt(topic: str, tone: str) -> str:
    tone_instructions = {
        "professional": "Tone: Professional and credible. Thought-leadership style. Confident but not arrogant. Story-driven with business insight.",
        "casual": "Tone: Casual and conversational. Like you're talking to a friend who happens to be in your industry. Use contractions, short sentences, everyday language.",
        "viral": "Tone: High-energy and bold. Make a strong, slightly controversial claim. Use pattern interrupts. Designed to get comments and shares."
    }

    tone_instruction = tone_instructions.get(tone, tone_instructions["professional"])

    return f"""Create a LinkedIn post about the following topic:

Topic: {topic}

{tone_instruction}

Remember: Return ONLY valid JSON. No markdown, no backticks, no explanation."""


def build_modifier_prompt(current_post: dict, modifier: str, add_emojis: bool = False) -> str:
    import json

    post_json = json.dumps(current_post, indent=2)

    prompt_map = {
        "viral": MAKE_VIRAL_PROMPT,
        "shorten": SHORTEN_PROMPT,
        "emojis": ADD_EMOJIS_PROMPT,
    }

    base_prompt = prompt_map.get(modifier, MAKE_VIRAL_PROMPT)

    return f"""{base_prompt}

Here is the current post to transform:

{post_json}

Return ONLY valid JSON. No markdown, no backticks, no explanation."""
>>>>>>> b7af538 (Switch to Grok (X.AI) via openai client; add XAI_API_KEY placeholder)
