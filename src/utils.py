import json

import requests


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
