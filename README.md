# AI LinkedIn Post Generator

A Streamlit app that generates viral LinkedIn posts using OpenAI.

## Setup

1. Copy `.env.example` to `.env`.
2. Add your `OPENAI_API_KEY` and optionally `LINKEDIN_ACCESS_TOKEN`.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run:

```bash
streamlit run src/main.py
```

> Tip: keep your `.env` file private and do not commit it to GitHub.

## Features

- Generates hooks, full posts, CTAs, hashtags, and alternate versions.
- Optional "Make it more viral" and "Shorten post" actions.
- Emoji toggle.
- Teach mode reveals the system prompt, raw JSON, and tone selection.
- Export generated post as `.txt`.
