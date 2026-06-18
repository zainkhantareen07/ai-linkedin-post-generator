import json
from datetime import datetime
import requests


def format_post_for_export(post: dict, topic: str, tone: str) -> str:
    """Format post data as a clean .txt file content."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    hashtags = " ".join(post.get("hashtags", []))

    lines = [
        "=" * 60,
        "  AI LinkedIn Post Generator — Export",
        f"  Generated: {now}",
        f"  Topic: {topic}",
        f"  Tone: {tone.capitalize()}",
        "=" * 60,
        "",
        "── HOOK ──────────────────────────────────────────────────",
        post.get("hook", ""),
        "",
        "── FULL POST ─────────────────────────────────────────────",
        post.get("post", ""),
        "",
        "── CALL TO ACTION ───────────────────────────────────────-",
        post.get("cta", ""),
        "",
        "── HASHTAGS ─────────────────────────────────────────────-",
        hashtags,
        "",
        "── ALTERNATE VERSIONS ───────────────────────────────────-",
        "",
        "[ FORMAL ]",
        post.get("alternate_versions", {}).get("formal", ""),
        "",
        "[ CASUAL ]",
        post.get("alternate_versions", {}).get("casual", ""),
        "",
        "[ VIRAL ]",
        post.get("alternate_versions", {}).get("viral", ""),
        "",
        "=" * 60,
        "  Generated with AI LinkedIn Post Generator",
        "=" * 60,
    ]

    return "\n".join(lines)


def format_full_linkedin_post(post: dict) -> str:
    """Combine hook + post + cta + hashtags into a ready-to-copy LinkedIn post."""
    parts = []

    hook = post.get("hook", "").strip()
    body = post.get("post", "").strip()
    cta = post.get("cta", "").strip()
    hashtags = " ".join(post.get("hashtags", []))

    if hook:
        parts.append(hook)
    if body:
        parts.append(body)
    if cta:
        parts.append(cta)
    if hashtags:
        parts.append(hashtags)

    return "\n\n".join(parts)


def get_raw_debug_info(post: dict, topic: str, tone: str, system_prompt: str) -> str:
    """Return debug info for teach mode."""
    return json.dumps({
        "system_prompt_preview": system_prompt[:300] + "...",
        "topic": topic,
        "tone": tone,
        "raw_output": post
    }, indent=2)


def count_words(text: str) -> int:
    """Count words in a string."""
    return len(text.split()) if text.strip() else 0


def validate_inputs(topic: str) -> tuple[bool, str]:
    """Validate user inputs before making API call."""
    if not topic or not topic.strip():
        return False, "Please enter a topic before generating."
    if len(topic.strip()) < 5:
        return False, "Topic is too short. Please be more descriptive."
    if len(topic) > 500:
        return False, "Topic is too long. Please keep it under 500 characters."
    return True, ""


def parse_openai_response(response_text: str) -> dict:
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Fallback: attempt to extract JSON substring
        start = response_text.find("{")
        end = response_text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(response_text[start:end + 1])
            except json.JSONDecodeError:
                pass
        raise ValueError("Unable to parse OpenAI response as valid JSON")


def format_hashtags(hashtags: list[str]) -> str:
    return " ".join(f"#{tag.strip().lstrip('#')}" for tag in hashtags if tag)


def compile_post_to_text(post_data: dict) -> str:
    parts = [
        post_data.get("hook", "").strip(),
        post_data.get("post", "").strip(),
        post_data.get("cta", "").strip(),
        format_hashtags(post_data.get("hashtags", [])),
    ]
    return "\n\n".join(part for part in parts if part)


def publish_to_linkedin(token: str, post_text: str) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    profile_response = requests.get("https://api.linkedin.com/v2/me", headers=headers)
    if profile_response.status_code != 200:
        return {
            "error": f"Failed to authenticate with LinkedIn: {profile_response.status_code} {profile_response.text}"
        }

    profile_data = profile_response.json()
    member_id = profile_data.get("id")
    if not member_id:
        return {"error": "LinkedIn profile ID not found from token."}

    author_urn = f"urn:li:person:{member_id}"
    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    api_url = "https://api.linkedin.com/v2/ugcPosts"
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code in (201, 202):
        return {"success": "Post published successfully to LinkedIn!"}
    return {"error": f"Failed to publish: {response.status_code} {response.text}"}
