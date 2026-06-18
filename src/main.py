import json


def generate_post(client, topic, tone):
    prompt = f"""
Create a high-quality LinkedIn post.

Topic:
{topic}

Tone:
{tone}

Return ONLY valid JSON.

Format:

{{
    "hook":"...",
    "post":"...",
    "cta":"...",
    "hashtags":[
        "#AI",
        "#Technology",
        "#Innovation"
    ]
}}

Do not include markdown.
Do not include explanations.
Return JSON only.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception:
        return {
            "hook": "",
            "post": content,
            "cta": "",
            "hashtags": []
        }