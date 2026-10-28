# Podcast Digest

## Project Overview
A private daily podcast of tech and aerospace news. Each weekday morning, a script
fetches new articles from RSS feeds I choose, uses the Claude API to turn them into a
10–15 minute podcast-style script, converts it to an MP3, and publishes it to a private
podcast feed that I listen to on my phone at work.

Pipeline:
1. Fetch new articles from my chosen RSS feeds
2. Summarize them into a podcast script with the Claude API
3. Convert the script to MP3 with text-to-speech
4. Upload the MP3 to AWS S3 and update a private podcast RSS feed
5. Subscribe to the feed in a podcast app

Language: Python

## About Me
- I work in IT support and am building portfolio projects toward cloud, DevOps,
  AI infrastructure, or security roles.
- I know basic scripting but am still learning. I want to understand every part of
  this project, not just have it work.
- I prefer one step at a time. Don't overload me with information.

## Hosting Plan
- **Phase 1:** Run on a schedule with GitHub Actions (weekdays, early morning).
  Store MP3s and the feed file in AWS S3.
- **Phase 2:** Migrate the pipeline to AWS Lambda + S3 as a portfolio upgrade.

## Rules

### Learning
- Build in small pieces, one per session (30–45 minutes of work).
- Explain every file and every non-obvious line in plain English, in two places:
  short comments in the code, and a plain-English walkthrough in chat after each file.
- After each piece, suggest one small change I can make myself to practice.
- Keep code simple and readable over clever.

### Security and Boundaries
- Only create or edit files inside this project folder. Never touch anything outside
  it or change system settings.
- Never hardcode the API key. Load it from a `.env` file locally and from GitHub
  Secrets in the cloud.
- Never set `ANTHROPIC_API_KEY` in my shell profile or system environment.
- Make sure `.env` is listed in `.gitignore` before anything is committed.
- Ask before installing any package, and explain what it's for.

### Cost
- My Claude API budget is $30/month total.
- Use a cost-efficient model for summaries (e.g. Claude Haiku).
- Once the summarizer exists, estimate the cost per daily episode and per month
  (about 22 weekday episodes) and confirm it fits the budget.

### Content and Privacy
- The feed is for my personal listening only.
- The feed must stay private, served from an unguessable URL. Never commit that URL
  to the repo or print it in public logs.

## Suggested Build Order
1. **RSS fetcher** – read my chosen feeds and collect new articles
2. **Summarizer** – send articles to Claude and get back a podcast script;
   estimate cost per episode
3. **Text-to-speech** – turn the script into an MP3 (after choosing a provider)
4. **Run the whole pipeline locally** end to end
5. **AWS setup** – create an AWS account, an S3 bucket, and a limited-permission
   user for this project
6. **Upload + feed** – upload the MP3 to S3 and generate/update the podcast RSS feed
7. **Subscribe** – add the private feed to my podcast app and test on my phone
8. **GitHub Actions** – schedule the pipeline for weekday mornings using GitHub Secrets
9. **Phase 2** – migrate to AWS Lambda

## Open Decisions
- **TTS provider** – not chosen yet
- **RSS sources** – which tech and aerospace feeds to use
- **Episode length** – target within the 10–15 minute range
- **Podcast app** – leaning toward Apple Podcasts (supports "Follow a Show by URL")
- **Python version** – my Mac has Python 3.9.6 (outdated); decide whether to install
  a newer version before starting

## Accounts
- GitHub: set up
- Anthropic API: set up
- AWS: not yet (see build step 5)

## Current Status
_Update at the end of each session._

- **Last session:** — (not started)
- **Completed:** CLAUDE.md created
- **Next step:** Build step 1 – RSS fetcher
- **Notes / questions:** —
