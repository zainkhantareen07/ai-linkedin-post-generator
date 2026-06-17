import streamlit as st
import json
# Remove the dot before generator and prompts
from generator import generate_post, refine_post, client
from utils import compile_post_to_text
from prompts import SYSTEM_PROMPT


def display_json_data(data: dict) -> None:
    st.subheader("Raw JSON Output")
    st.json(data)


def render_post(data: dict) -> None:
    st.markdown(f"### {data.get('hook', '')}")
    st.write(data.get("post", ""))
    st.markdown(f"**CTA:** {data.get('cta', '')}")
    hashtags = data.get("hashtags", [])
    if hashtags:
        st.markdown(f"**Hashtags:** {format_hashtags(hashtags)}")
    alternate = data.get("alternate_versions", {})
    if alternate:
        with st.expander("Alternate Versions"):
            st.write("**Formal**")
            st.write(alternate.get("formal", ""))
            st.write("**Casual**")
            st.write(alternate.get("casual", ""))
            st.write("**Viral**")
            st.write(alternate.get("viral", ""))


def app() -> None:
    st.title("AI LinkedIn Post Generator")
    st.write("Generate a strong LinkedIn post with hook, CTA, hashtags, and alternate versions.")

    topic = st.text_input("Topic")
    tone = st.selectbox("Tone", ["professional", "casual", "viral"])
    teach_mode = st.checkbox("Teach mode")
    add_emoji = st.checkbox("Add emojis")
    linkedin_token = st.text_input(
        "LinkedIn Access Token",
        type="password",
        help="Paste a valid LinkedIn OAuth access token to publish directly.",
    )

    if "current_post" not in st.session_state:
        st.session_state.current_post = None
        st.session_state.tone = ""

    if st.button("Generate Post"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating post..."):
                st.session_state.current_post = generate_post(topic, tone)
                st.session_state.tone = tone
                st.success("Generated successfully.")

    if st.session_state.current_post:
        result = st.session_state.current_post
        render_post(result)

        if teach_mode:
            st.markdown("### Teach Mode")
            st.code(SYSTEM_PROMPT, language="text")
            display_json_data(result)
            st.markdown(f"**Tone used:** {st.session_state.tone}")

        action_cols = st.columns(3)
        if action_cols[0].button("Make it more viral"):
            with st.spinner("Making the post more viral..."):
                st.session_state.current_post = make_more_viral(result)
                st.success("Post updated for more viral reach.")
                result = st.session_state.current_post
                render_post(result)

        if action_cols[1].button("Shorten post"):
            with st.spinner("Shortening the post..."):
                st.session_state.current_post = shorten_post(result)
                st.success("Post shortened successfully.")
                result = st.session_state.current_post
                render_post(result)

        if action_cols[2].button("Apply emojis"):
            if add_emoji:
                with st.spinner("Adding emojis..."):
                    st.session_state.current_post = add_emojis(result)
                    st.success("Emojis applied successfully.")
                    result = st.session_state.current_post
                    render_post(result)
            else:
                st.warning("Enable 'Add emojis' to use this button.")

        if st.download_button(
            "Download post as .txt",
            data=compile_post_to_text(result),
            file_name="linkedin_post.txt",
        ):
            st.success("Download ready.")

        st.markdown("---")
        st.subheader("📲 Direct Share")
        if st.button("🚀 Share Directly to LinkedIn Feed"):
            if not linkedin_token:
                st.error("Please provide a valid LinkedIn Access Token first.")
            else:
                with st.spinner("Connecting to LinkedIn..."):
                    full_text = compile_post_to_text(result)
                    publish_result = publish_to_linkedin(linkedin_token, full_text)
                    if publish_result.get("success"):
                        st.success(publish_result["success"])
                    else:
                        st.error(publish_result.get("error", "Failed to publish to LinkedIn."))
