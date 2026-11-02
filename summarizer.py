"""
Build step 2: turn the fetched articles into a spoken podcast script with Claude.

Run it directly to write today's script to the output/ folder:
    python summarizer.py
"""

from datetime import date
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from fetcher import fetch_articles

# Copy ANTHROPIC_API_KEY from .env into this program's environment, where the
# anthropic library looks for it. It only lasts while this script runs.
load_dotenv()

MODEL = "claude-haiku-5-5"  # the cheapest current Claude model, good enough for summaries
TARGET_WORDS = 1800  # about 12 minutes at ~150 spoken words per minute

# Haiku 5.5 prices in US dollars per 1 million tokens (for prompts under 100K tokens).
INPUT_PRICE_PER_MILLION = 0.10
OUTPUT_PRICE_PER_MILLION = 0.50
EPISODES_PER_MONTH = 22  # weekdays only

OUTPUT_DIR = Path("output")

# The standing instructions for Claude. Everything it writes will be read aloud by a
# text-to-speech voice, so it must be plain spoken sentences with no formatting.
SYSTEM_PROMPT = f"""You write the script for a short daily news podcast called Podcast Digest, \
covering technology and aerospace. One host reads it aloud, and a text-to-speech voice will \
speak your text exactly as written.

Write about {TARGET_WORDS} words of plain spoken English:
- Open with a one-line greeting that mentions the day and date.
- Do a technology segment, then an aerospace segment, with a short spoken transition between them.
- You will get more stories than fit. Choose the 12 to 15 most significant or interesting ones, \
giving aerospace a fair share even if it has fewer stories. Merge stories that cover the same news.
- For each story, say what happened and why it matters, in two to four sentences. Mention the \
source naturally, like "Ars Technica reports...".
- Close with a brief sign-off.

Because this will be heard, not read: no headings, bullet points, markdown, emoji, URLs, or \
stage directions. Spell out abbreviations a listener might not know the first time. Only use \
facts from the stories provided. Don't invent details."""


def format_articles(articles):
    """Turn the article list into numbered plain text for Claude to read."""
    lines = []
    for number, a in enumerate(articles, start=1):
        lines.append(f"{number}. [{a['category']}] {a['source']}: {a['title']}")
        if a["summary"]:
            lines.append(f"   {a['summary']}")
    return "\n".join(lines)


def write_script(articles):
    """Ask Claude for a podcast script. Returns the script text and the API response."""
    client = anthropic.Anthropic()  # finds ANTHROPIC_API_KEY automatically

    today = date.today().strftime("%A, %B %d, %Y")  # e.g. "Monday, November 02, 2026"
    user_message = f"Today is {today}. Here are today's stories:\n\n{format_articles(articles)}"

    response = client.messages.create(
        model=MODEL,
        max_tokens=16000,  # an upper limit, not a target: high enough that the script is never cut off
        output_config={"effort": "medium"},  # how hard Claude thinks before writing (low/medium/high)
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    # stop_reason says why Claude stopped. Anything other than "end_turn" means a problem.
    if response.stop_reason == "refusal":
        raise RuntimeError("Claude declined to write this script.")
    if response.stop_reason == "max_tokens":
        raise RuntimeError("The script hit the max_tokens limit and was cut off.")

    # The reply is a list of "blocks". Keep only the text ones (skipping Claude's thinking).
    script = "".join(block.text for block in response.content if block.type == "text")
    return script, response


def estimate_cost(usage):
    """Work out what one API call cost, from the token counts Claude reports back."""
    input_cost = usage.input_tokens / 1_000_000 * INPUT_PRICE_PER_MILLION
    output_cost = usage.output_tokens / 1_000_000 * OUTPUT_PRICE_PER_MILLION
    return input_cost + output_cost


if __name__ == "__main__":
    articles = fetch_articles()
    print(f"Fetched {len(articles)} articles. Asking Claude for a script...")

    script, response = write_script(articles)

    OUTPUT_DIR.mkdir(exist_ok=True)  # create output/ the first time
    script_path = OUTPUT_DIR / f"{date.today()}.txt"  # e.g. output/2026-11-02.txt
    script_path.write_text(script)

    words = len(script.split())
    cost = estimate_cost(response.usage)
    print(f"Saved script to {script_path}")
    print(f"Length: {words} words, about {words / 150:.0f} minutes spoken")
    print(f"Tokens: {response.usage.input_tokens} in, {response.usage.output_tokens} out")
    print(f"Cost: ${cost:.4f} this episode, about ${cost * EPISODES_PER_MONTH:.2f} per month")
