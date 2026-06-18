import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from main import get_openai_client
from generator import generate_post, modify_post
from utils import (
    format_post_for_export,
    format_full_linkedin_post,
    count_words,
    validate_inputs,
)
from prompts import SYSTEM_PROMPT

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI LinkedIn Post Generator",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Main header */
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #0A66C2;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
    }

    /* Section headers */
    .section-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #0A66C2;
        margin-bottom: 0.4rem;
    }

    /* Hook box */
    .hook-box {
        background: linear-gradient(135deg, #0A66C2 0%, #004182 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        font-size: 1.15rem;
        font-weight: 600;
        line-height: 1.5;
        margin-bottom: 1rem;
    }

    /* Post content box */
    .post-box {
        background: #f8f9fa;
        border-left: 4px solid #0A66C2;
        padding: 1.2rem 1.5rem;
        border-radius: 0 10px 10px 0;
        font-size: 0.95rem;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    /* CTA box */
    .cta-box {
        background: #e8f3ff;
        border: 1px solid #0A66C2;
        padding: 1rem 1.4rem;
        border-radius: 10px;
        font-size: 0.95rem;
        font-weight: 500;
        color: #004182;
    }

    /* Hashtag chips */
    .hashtag-chip {
        display: inline-block;
        background: #e8f3ff;
        color: #0A66C2;
        padding: 0.3rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }

    /* Word count badge */
    .word-count {
        font-size: 0.78rem;
        color: #888;
        margin-top: 0.4rem;
    }

    /* Debug box */
    .debug-box {
        background: #1e1e2e;
        color: #cdd6f4;
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
        white-space: pre-wrap;
        overflow-x: auto;
    }

    /* Divider */
    .custom-divider {
        border: none;
        border-top: 2px solid #e8f3ff;
        margin: 1.5rem 0;
    }

    /* Button row */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Session state init ───────────────────────────────────────────────────────

if "post" not in st.session_state:
    st.session_state.post = None
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "tone" not in st.session_state:
    st.session_state.tone = "professional"
if "history" not in st.session_state:
    st.session_state.history = []

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown('<div class="main-title">💼 AI LinkedIn Post Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Turn any topic into a scroll-stopping LinkedIn post in seconds.</div>', unsafe_allow_html=True)

# ── Sidebar: Teach Mode ───────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🎓 Teach Mode")
    teach_mode = st.checkbox("Show debug info", value=False)
    if teach_mode:
        st.info("When a post is generated, you'll see the system prompt, raw JSON output, and selected tone.")

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown(
        "Powered by GPT-4o. Enter a topic, choose a tone, and hit **Generate Post**. "
        "Use the bonus buttons to iterate fast."
    )

# ── Input section ─────────────────────────────────────────────────────────────

col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_input(
        "What's your post about?",
        placeholder="e.g. Why I quit my $200k job to build a startup, lessons from failing my first product launch...",
        value=st.session_state.topic,
        max_chars=500,
    )

with col2:
    tone = st.selectbox(
        "Tone",
        options=["professional", "casual", "viral"],
        index=["professional", "casual", "viral"].index(st.session_state.tone),
        format_func=lambda x: {"professional": "💼 Professional", "casual": "😊 Casual", "viral": "🚀 Viral"}[x],
    )

generate_btn = st.button("✨ Generate Post", type="primary", use_container_width=True)

# ── Generate ──────────────────────────────────────────────────────────────────

if generate_btn:
    valid, error_msg = validate_inputs(topic)
    if not valid:
        st.error(error_msg)
    else:
        try:
            client = get_openai_client()
            with st.spinner("Crafting your LinkedIn post..."):
                post = generate_post(topic, tone, client)
            st.session_state.post = post
            st.session_state.topic = topic
            st.session_state.tone = tone
            # Save to history
            st.session_state.history.append({"topic": topic, "tone": tone, "post": post})
            st.rerun()
        except EnvironmentError as e:
            st.error(f"🔑 API Key Error: {e}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ── Results ───────────────────────────────────────────────────────────────────

if st.session_state.post:
    post = st.session_state.post
    topic_used = st.session_state.topic
    tone_used = st.session_state.tone

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ── Hook ──
    st.markdown('<div class="section-label">🪝 Hook</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hook-box">{post["hook"]}</div>', unsafe_allow_html=True)

    # ── Full post ──
    st.markdown('<div class="section-label">📝 Full Post</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="post-box">{post["post"]}</div>', unsafe_allow_html=True)
    word_count = count_words(post["post"])
    st.markdown(f'<div class="word-count">📊 {word_count} words</div>', unsafe_allow_html=True)

    st.markdown("")

    # ── CTA ──
    st.markdown('<div class="section-label">📣 Call to Action</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="cta-box">{post["cta"]}</div>', unsafe_allow_html=True)

    st.markdown("")

    # ── Hashtags ──
    st.markdown('<div class="section-label">🏷️ Hashtags</div>', unsafe_allow_html=True)
    hashtags = post.get("hashtags", [])
    if hashtags:
        chips_html = "".join([f'<span class="hashtag-chip">{h}</span>' for h in hashtags])
        st.markdown(chips_html, unsafe_allow_html=True)
    else:
        st.write("No hashtags generated.")

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ── Bonus action buttons ──
    st.markdown("### ⚡ Refine Your Post")
    bcol1, bcol2, bcol3 = st.columns(3)

    with bcol1:
        if st.button("🚀 Make it More Viral", use_container_width=True):
            try:
                client = get_openai_client()
                with st.spinner("Cranking up the virality..."):
                    updated = modify_post(post, "viral", client)
                st.session_state.post = updated
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    with bcol2:
        if st.button("✂️ Shorten Post", use_container_width=True):
            try:
                client = get_openai_client()
                with st.spinner("Trimming the fat..."):
                    updated = modify_post(post, "shorten", client)
                st.session_state.post = updated
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    with bcol3:
        add_emojis = st.toggle("😄 Add Emojis", value=False)
        if add_emojis:
            try:
                client = get_openai_client()
                with st.spinner("Sprinkling in emojis..."):
                    updated = modify_post(post, "emojis", client)
                st.session_state.post = updated
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ── Alternate versions ──
    with st.expander("🔀 Alternate Versions", expanded=False):
        versions = post.get("alternate_versions", {})

        if versions.get("formal"):
            st.markdown("**💼 Formal Version**")
            st.markdown(f'<div class="post-box">{versions["formal"]}</div>', unsafe_allow_html=True)
            st.markdown("")

        if versions.get("casual"):
            st.markdown("**😊 Casual Version**")
            st.markdown(f'<div class="post-box">{versions["casual"]}</div>', unsafe_allow_html=True)
            st.markdown("")

        if versions.get("viral"):
            st.markdown("**🚀 Viral Version**")
            st.markdown(f'<div class="post-box">{versions["viral"]}</div>', unsafe_allow_html=True)

    # ── Copy-ready full post ──
    with st.expander("📋 Full Post (Ready to Copy)", expanded=False):
        full_post = format_full_linkedin_post(post)
        st.text_area("Copy this directly to LinkedIn:", value=full_post, height=300)

    # ── Export ──
    st.markdown("### 💾 Export")
    export_content = format_post_for_export(post, topic_used, tone_used)
    st.download_button(
        label="⬇️ Download Post as .txt",
        data=export_content,
        file_name=f"linkedin_post_{tone_used}.txt",
        mime="text/plain",
        use_container_width=True,
    )

    # ── Teach Mode Debug ──
    if teach_mode:
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        st.markdown("### 🎓 Teach Mode — Debug Info")

        st.markdown("**System Prompt:**")
        st.code(SYSTEM_PROMPT, language="text")

        st.markdown(f"**Tone Selected:** `{tone_used}`")
        st.markdown(f"**Topic:** `{topic_used}`")

        import json
        st.markdown("**Raw JSON Output:**")
        st.code(json.dumps(post, indent=2), language="json")

# ── No post yet state ─────────────────────────────────────────────────────────

else:
    st.markdown("")
    st.info("👆 Enter a topic above and hit **Generate Post** to get started.")

    st.markdown("### 💡 Example Topics")
    examples = [
        "Why I stopped writing To-Do lists and started getting more done",
        "3 things I learned after failing my first startup",
        "Why remote work is actually killing team creativity",
        "The best career advice I ignored for 5 years",
        "How I got my first 1,000 LinkedIn followers in 30 days",
    ]
    for ex in examples:
        if st.button(f"→ {ex}", key=ex):
            st.session_state.topic = ex
            st.rerun()
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from main import get_openai_client
from generator import generate_post, modify_post
from utils import (
    format_post_for_export,
    format_full_linkedin_post,
    count_words,
    validate_inputs,
)
from prompts import SYSTEM_PROMPT

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI LinkedIn Post Generator",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Main header */
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #0A66C2;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
    }

    /* Section headers */
    .section-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #0A66C2;
        margin-bottom: 0.4rem;
    }

    /* Hook box */
    .hook-box {
        background: linear-gradient(135deg, #0A66C2 0%, #004182 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        font-size: 1.15rem;
        font-weight: 600;
        line-height: 1.5;
        margin-bottom: 1rem;
    }

    /* Post content box */
    .post-box {
        background: #f8f9fa;
        border-left: 4px solid #0A66C2;
        padding: 1.2rem 1.5rem;
        border-radius: 0 10px 10px 0;
        font-size: 0.95rem;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    /* CTA box */
    .cta-box {
        background: #e8f3ff;
        border: 1px solid #0A66C2;
        padding: 1rem 1.4rem;
        border-radius: 10px;
        font-size: 0.95rem;
        font-weight: 500;
        color: #004182;
    }

    /* Hashtag chips */
    .hashtag-chip {
        display: inline-block;
        background: #e8f3ff;
        color: #0A66C2;
        padding: 0.3rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }

    /* Word count badge */
    .word-count {
        font-size: 0.78rem;
        color: #888;
        margin-top: 0.4rem;
    }

    /* Debug box */
    .debug-box {
        background: #1e1e2e;
        color: #cdd6f4;
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
        white-space: pre-wrap;
        overflow-x: auto;
    }

    /* Divider */
    .custom-divider {
        border: none;
        border-top: 2px solid #e8f3ff;
        margin: 1.5rem 0;
    }

    /* Button row */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────

if "post" not in st.session_state:
    st.session_state.post = None
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "tone" not in st.session_state:
    st.session_state.tone = "professional"
if "history" not in st.session_state:
    st.session_state.history = []

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown('<div class="main-title">💼 AI LinkedIn Post Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Turn any topic into a scroll-stopping LinkedIn post in seconds.</div>', unsafe_allow_html=True)

# ── Sidebar: Teach Mode ───────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🎓 Teach Mode")
    teach_mode = st.checkbox("Show debug info", value=False)
    if teach_mode:
        st.info("When a post is generated, you'll see the system prompt, raw JSON output, and selected tone.")

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown(
        "Powered by GPT-4o. Enter a topic, choose a tone, and hit **Generate Post**. "
        "Use the bonus buttons to iterate fast."
    )

# ── Input section ─────────────────────────────────────────────────────────────

col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_input(
        "What's your post about?",
        placeholder="e.g. Why I quit my $200k job to build a startup, lessons from failing my first product launch...",
        value=st.session_state.topic,
        max_chars=500,
    )

with col2:
    tone = st.selectbox(
        "Tone",
        options=["professional", "casual", "viral"],
        index=["professional", "casual", "viral"].index(st.session_state.tone),
        format_func=lambda x: {"professional": "💼 Professional", "casual": "😊 Casual", "viral": "🚀 Viral"}[x],
    )

generate_btn = st.button("✨ Generate Post", type="primary", use_container_width=True)

# ── Generate ──────────────────────────────────────────────────────────────────

if generate_btn:
    valid, error_msg = validate_inputs(topic)
    if not valid:
        st.error(error_msg)
    else:
        try:
            client = get_openai_client()
            with st.spinner("Crafting your LinkedIn post..."):
                post = generate_post(topic, tone, client)
            st.session_state.post = post
            st.session_state.topic = topic
            st.session_state.tone = tone
            # Save to history
            st.session_state.history.append({"topic": topic, "tone": tone, "post": post})
            st.rerun()
        except EnvironmentError as e:
            st.error(f"🔑 API Key Error: {e}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ── Results ───────────────────────────────────────────────────────────────────

if st.session_state.post:
    post = st.session_state.post
    topic_used = st.session_state.topic
    tone_used = st.session_state.tone

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ── Hook ──
    st.markdown('<div class="section-label">🪝 Hook</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hook-box">{post["hook"]}</div>', unsafe_allow_html=True)

    # ── Full post ──
    st.markdown('<div class="section-label">📝 Full Post</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="post-box">{post["post"]}</div>', unsafe_allow_html=True)
    word_count = count_words(post["post"])
    st.markdown(f'<div class="word-count">📊 {word_count} words</div>', unsafe_allow_html=True)

    st.markdown("")

    # ── CTA ──
    st.markdown('<div class="section-label">📣 Call to Action</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="cta-box">{post["cta"]}</div>', unsafe_allow_html=True)

    st.markdown("")

    # ── Hashtags ──
    st.markdown('<div class="section-label">🏷️ Hashtags</div>', unsafe_allow_html=True)
    hashtags = post.get("hashtags", [])
    if hashtags:
        chips_html = "".join([f'<span class="hashtag-chip">{h}</span>' for h in hashtags])
        st.markdown(chips_html, unsafe_allow_html=True)
    else:
        st.write("No hashtags generated.")

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ── Bonus action buttons ──
    st.markdown("### ⚡ Refine Your Post")
    bcol1, bcol2, bcol3 = st.columns(3)

    with bcol1:
        if st.button("🚀 Make it More Viral", use_container_width=True):
            try:
                client = get_openai_client()
                with st.spinner("Cranking up the virality..."):
                    updated = modify_post(post, "viral", client)
                st.session_state.post = updated
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    with bcol2:
        if st.button("✂️ Shorten Post", use_container_width=True):
            try:
                client = get_openai_client()
                with st.spinner("Trimming the fat..."):
                    updated = modify_post(post, "shorten", client)
                st.session_state.post = updated
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    with bcol3:
        add_emojis = st.toggle("😄 Add Emojis", value=False)
        if add_emojis:
            try:
                client = get_openai_client()
                with st.spinner("Sprinkling in emojis..."):
                    updated = modify_post(post, "emojis", client)
                st.session_state.post = updated
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ── Alternate versions ──
    with st.expander("🔀 Alternate Versions", expanded=False):
        versions = post.get("alternate_versions", {})

        if versions.get("formal"):
            st.markdown("**💼 Formal Version**")
            st.markdown(f'<div class="post-box">{versions["formal"]}</div>', unsafe_allow_html=True)
            st.markdown("")

        if versions.get("casual"):
            st.markdown("**😊 Casual Version**")
            st.markdown(f'<div class="post-box">{versions["casual"]}</div>', unsafe_allow_html=True)
            st.markdown("")

        if versions.get("viral"):
            st.markdown("**🚀 Viral Version**")
            st.markdown(f'<div class="post-box">{versions["viral"]}</div>', unsafe_allow_html=True)

    # ── Copy-ready full post ──
    with st.expander("📋 Full Post (Ready to Copy)", expanded=False):
        full_post = format_full_linkedin_post(post)
        st.text_area("Copy this directly to LinkedIn:", value=full_post, height=300)

    # ── Export ──
    st.markdown("### 💾 Export")
    export_content = format_post_for_export(post, topic_used, tone_used)
    st.download_button(
        label="⬇️ Download Post as .txt",
        data=export_content,
        file_name=f"linkedin_post_{tone_used}.txt",
        mime="text/plain",
        use_container_width=True,
    )

    # ── Teach Mode Debug ──
    if teach_mode:
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        st.markdown("### 🎓 Teach Mode — Debug Info")

        st.markdown("**System Prompt:**")
        st.code(SYSTEM_PROMPT, language="text")

        st.markdown(f"**Tone Selected:** `{tone_used}`")
        st.markdown(f"**Topic:** `{topic_used}`")

        import json
        st.markdown("**Raw JSON Output:**")
        st.code(json.dumps(post, indent=2), language="json")

# ── No post yet state ─────────────────────────────────────────────────────────

else:
    st.markdown("")
    st.info("👆 Enter a topic above and hit **Generate Post** to get started.")

    st.markdown("### 💡 Example Topics")
    examples = [
        "Why I stopped writing To-Do lists and started getting more done",
        "3 things I learned after failing my first startup",
        "Why remote work is actually killing team creativity",
        "The best career advice I ignored for 5 years",
        "How I got my first 1,000 LinkedIn followers in 30 days",
    ]
    for ex in examples:
        if st.button(f"→ {ex}", key=ex):
            st.session_state.topic = ex
            st.rerun()
>>>>>>> b7af538 (Switch to Grok (X.AI) via openai client; add XAI_API_KEY placeholder)
