import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

from main import get_client
from generator import generate_post, modify_post
from utils import (
    format_full_linkedin_post,
    format_post_for_export,
    count_words,
    validate_inputs,
)

st.set_page_config(page_title="AI LinkedIn Generator", layout="wide")

if "post" not in st.session_state:
    st.session_state.post = None

st.title("💼 AI LinkedIn Post Generator")

topic = st.text_input("Enter topic")
tone = st.selectbox("Tone", ["professional", "casual", "viral"])

if st.button("Generate"):
    valid, msg = validate_inputs(topic)

    if not valid:
        st.error(msg)
    else:
        try:
            client = get_client()
            post = generate_post(topic, tone, client)

            st.session_state.post = post

        except Exception as e:
            st.error(str(e))


if st.session_state.post:
    post = st.session_state.post

    st.subheader("Hook")
    st.write(post["hook"])

    st.subheader("Post")
    st.write(post["post"])

    st.subheader("CTA")
    st.write(post["cta"])

    st.subheader("Hashtags")
    st.write(" ".join(post.get("hashtags", [])))

    st.download_button(
        "Download Post",
        format_post_for_export(post, topic, tone),
        file_name="linkedin_post.txt"
    )

    st.text_area(
        "Copy Full Post",
        format_full_linkedin_post(post),
        height=300
    )