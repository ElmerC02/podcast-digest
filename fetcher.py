"""
Build step 1: fetch recent articles from the RSS feeds listed in feeds.py.

Run it directly to see what it finds:
    python fetcher.py
"""

import calendar
import html
import re
from datetime import datetime, timedelta, timezone

import feedparser

from feeds import FEEDS

# Only keep articles published within this many hours.
HOURS_BACK = 24

# Tell websites who is asking. Some block requests that don't say.
USER_AGENT = "podcast-digest/0.1 (personal RSS reader)"


def clean_text(raw):
    """Turn an HTML snippet into plain text."""
    text = re.sub(r"<[^>]+>", " ", raw)  # remove HTML tags like <p> or <a href="...">
    text = html.unescape(text)  # turn codes like &amp; back into &
    return " ".join(text.split())  # squash runs of spaces and newlines into single spaces


def published_time(entry):
    """Return when an article was published (in UTC), or None if the feed doesn't say."""
    # feedparser gives dates as a UTC time tuple. Some feeds only have an "updated" date.
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed is None:
        return None
    # timegm turns that tuple into "seconds since 1970", which datetime understands.
    return datetime.fromtimestamp(calendar.timegm(parsed), tz=timezone.utc)


def fetch_articles(hours_back=HOURS_BACK):
    """Collect articles from every feed published in the last `hours_back` hours."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_back)
    articles = []
    seen_links = set()  # one story can appear in two feeds (e.g. Ars Technica and Ars Space)

    for feed in FEEDS:
        # A download can break halfway through. Skip that feed instead of stopping everything.
        try:
            parsed = feedparser.parse(feed["url"], agent=USER_AGENT)
        except Exception as error:
            print(f"  ! Could not download {feed['name']}: {error!r}")
            continue

        # For most other problems, feedparser doesn't crash. It sets "bozo" to flag them instead.
        if parsed.bozo and not parsed.entries:
            print(f"  ! Could not read {feed['name']}: {parsed.bozo_exception}")
            continue

        for entry in parsed.entries:
            published = published_time(entry)
            link = entry.get("link", "")

            # Skip articles with no date, older than the cutoff, or already collected.
            if published is None or published < cutoff or link in seen_links:
                continue

            seen_links.add(link)
            articles.append({
                "source": feed["name"],
                "category": feed["category"],
                "title": clean_text(entry.get("title", "")),
                "link": link,
                "published": published,
                "summary": clean_text(entry.get("summary", "")),
            })

    articles.sort(key=lambda a: a["published"], reverse=True)  # newest first
    return articles


# This part only runs when you start this file directly (python fetcher.py).
# Later, the summarizer will import fetch_articles() without triggering it.
if __name__ == "__main__":
    articles = fetch_articles()
    print(f"Found {len(articles)} articles from the last {HOURS_BACK} hours:\n")
    for a in articles:
        print(f"[{a['category']}] {a['source']}: {a['title']}")
        print(f"    {a['published']:%a %H:%M UTC}  {a['link']}")
