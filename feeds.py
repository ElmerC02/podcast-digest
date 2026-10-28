# The RSS feeds the podcast pulls news from.
# To add or remove a source, edit this list. No other code needs to change.
# "category" lets the podcast script group stories into tech and aerospace segments.
#
# Order matters: if a story appears in two feeds, the first feed listed wins.
# Aerospace goes first so space stories from the main Ars Technica feed
# get labeled "aerospace" (via Ars Technica Space) instead of "tech".

FEEDS = [
    # Aerospace
    {"name": "SpaceNews", "category": "aerospace", "url": "https://spacenews.com/feed/"},
    {"name": "NASA", "category": "aerospace", "url": "https://www.nasa.gov/news-release/feed/"},
    {"name": "Ars Technica Space", "category": "aerospace", "url": "https://arstechnica.com/space/feed/"},
    # Tech
    {"name": "Ars Technica", "category": "tech", "url": "https://feeds.arstechnica.com/arstechnica/index"},
    {"name": "The Verge", "category": "tech", "url": "https://www.theverge.com/rss/index.xml"},
    {"name": "Hacker News", "category": "tech", "url": "https://hnrss.org/frontpage"},
]
