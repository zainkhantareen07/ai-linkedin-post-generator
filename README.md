# 💼 AI LinkedIn Post Generator

Turn any topic into a scroll-stopping LinkedIn post in seconds — powered by GPT-4o.

---

## Features

- **3 tone modes**: Professional, Casual, Viral
- **Structured output**: Hook, Full Post, CTA, Hashtags
- **3 alternate versions** per post: Formal, Casual, Viral rewrites
- **Bonus modifiers**: Make it More Viral, Shorten Post, Add Emojis
- **Teach Mode**: See the system prompt, raw JSON, and tone used
- **Export**: Download post as `.txt`
- **Example topics** to get started instantly

---

## Setup

### 1. Clone or download the project

```bash
cd ai-linkedin-post-generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your API key

```bash
cp .env.example .env
```

Open `.env` and replace `your-key-here` with your [OpenAI API key](https://platform.openai.com/api-keys):

```
OPENAI_API_KEY=sk-...
```

### 4. Run the app

```bash
streamlit run src/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

```
ai-linkedin-post-generator/
├── src/
│   ├── main.py        # Entry point, OpenAI client init
│   ├── app.py         # Streamlit UI
│   ├── prompts.py     # System prompts & prompt builders
│   ├── generator.py   # GPT call logic & JSON parsing
│   └── utils.py       # Export, formatting, validation helpers
├── .env.example       # API key template
├── requirements.txt
└── README.md
```

---

## Quick CLI Test

```bash
cd src
python main.py
```

---

## How It Works

1. You enter a **topic** and select a **tone**
2. The app sends a structured prompt to GPT-4o with a JSON schema
3. GPT returns a structured post with hook, body, CTA, hashtags, and 3 alternate versions
4. You can further refine it with modifier buttons (viral / shorten / emojis)
5. Download the final post as `.txt`

---

## Tips for Best Results

- Be specific with your topic: *"Why I quit my PM job to build a SaaS"* beats *"career change"*
- Use **Viral** tone for controversial or hot-take style content
- Use **Casual** for personal stories and lessons learned
- Use **Professional** for thought leadership and industry insights
- Hit **Make it More Viral** 1-2x on a decent post to push it further

---

## Requirements

- Python 3.10+
- OpenAI API key (GPT-4o access recommended)
### 3. Configure your API key

```bash
cp .env.example .env
```

Open `.env` and replace `your-key-here` with your [OpenAI API key](https://platform.openai.com/api-keys):

```
OPENAI_API_KEY=sk-...
```

### 4. Run the app

```bash
streamlit run src/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

```
ai-linkedin-post-generator/
├── src/
│   ├── main.py        # Entry point, OpenAI client init
│   ├── app.py         # Streamlit UI
│   ├── prompts.py     # System prompts & prompt builders
│   ├── generator.py   # GPT call logic & JSON parsing
│   └── utils.py       # Export, formatting, validation helpers
├── .env.example       # API key template
├── requirements.txt
└── README.md
```

---

## Quick CLI Test

```bash
cd src
python main.py
```

---

## How It Works

1. You enter a **topic** and select a **tone**
2. The app sends a structured prompt to GPT-4o with a JSON schema
3. GPT returns a structured post with hook, body, CTA, hashtags, and 3 alternate versions
4. You can further refine it with modifier buttons (viral / shorten / emojis)
5. Download the final post as `.txt`

---

## Tips for Best Results

- Be specific with your topic: *"Why I quit my PM job to build a SaaS"* beats *"career change"*
- Use **Viral** tone for controversial or hot-take style content
- Use **Casual** for personal stories and lessons learned
- Use **Professional** for thought leadership and industry insights
- Hit **Make it More Viral** 1-2x on a decent post to push it further

---

## Requirements

- Python 3.10+
- OpenAI API key (GPT-4o access recommended)
>>>>>>> b7af538 (Switch to Grok (X.AI) via openai client; add XAI_API_KEY placeholder)
