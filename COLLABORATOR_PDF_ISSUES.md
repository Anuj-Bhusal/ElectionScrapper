# PDF Differences: Analysis & Fix Guide

## Quick Summary of Problems

Your friend's PDF has **3 distinct bugs** compared to your correct output. None of these are
keyword or classification issues — they are all **content extraction and scraping environment issues**.

---

## Bug 1 — Wrong summaries for Kathmandu Post articles (most critical)

### What you see
Multiple different KP articles ("Balen Shah drops BRI-tied industrial park",
"Voters are no longer passive listeners", "Government declares three-day public holiday",
"Candidates in Bardiya pledge...") all show the **same text** as their body:

> *Postponement rumours swirl ahead of March 5 polls.*

These are completely different articles but they all got that one sentence as content.

### Why it happens

Kathmandu Post is **English-only and requires JavaScript to render full content**.
The scraper does `self.fetch(link)` which does a plain `requests.get()` for English sites
(no Selenium triggered). When KP blocks or partially serves a non-JS client, the page HTML
contains almost nothing — only a small teaser or a "related article" snippet.

The `readability` library then picks up whatever short text it finds. Because the last
article on KP's page was the "Postponement rumours..." article, its teaser leaked into
other articles that had empty bodies.

**Environment-specific:** On your machine, Selenium cookies / your IP / your browser session
may already have KP loaded and cached properly. On a fresh clone, Selenium starts with a
blank profile — KP may serve a JS-only skeleton page.

### Fix

Force Selenium for Kathmandu Post article fetches:

```python
# kathmandu_post.py
for link in article_links:
    html = self.fetch(link, use_selenium=True)   # <-- add use_selenium=True
```

---

## Bug 2 — Raw website UI boilerplate in article bodies

### What you see (Ekantipur + OnlineKhabar articles)

```
News Sign In Voters of Dolakha say ... Read In English Facebook Messenger
Twitter Whatsapp Viber Copy Link What you should know ...
```

```
0 Comments Shares General Election Forecasting ... Your browser does not
support the audio element.
```

These are the website's **nav bar, login prompt, share buttons, and audio player fallback text**
leaking into the article body.

### Why it happens

The `article_extractor.py` junk pattern list does not cover these site-specific strings.
The `readability` library extracted the full visible text including chrome elements.

**Environment-specific:** Your Selenium session on Ekantipur may have the site rendered in
a way that `readability` gets only the article. On a fresh session, the full page layout
including Sign In overlay is picked up.

### Fix (already applied in repo — pull latest)

The `junk_patterns` list in `article_extractor.py` needs these additions:

```python
r'News\s*Sign\s*In',
r'Sign\s*In\s*$',
r'Read In English',
r'Facebook\s+Messenger\s+Twitter\s+Whatsapp\s+Viber\s+Copy Link',
r'What you should know',
r'Your browser does not support the audio element',
r'\d+\s*Comments?\s*Shares?',
r'Pvt\.\s+\w+\s+\w+\s+\d+\s+\w+\s+\d+\s+at\s+\d+:\d+',
```

---

## Bug 3 — Author / date metadata bleeding into summary

### What you see

```
Pvt. Krishna Pokharel 13 February 2082 at 10:03
```

This is the author byline shown inside the article body text.

### Why it happens

Ekantipur wraps author info inside the same `<article>` container that `readability` extracts.
The junk pattern for Nepali calendar dates in `article_extractor.py` matches BS dates but
not this specific "Pvt. Name DD Month YYYY at HH:MM" format.

---

## Root Cause Summary Table

| Issue | Your PDF | Friend's PDF | Root Cause |
|-------|----------|--------------|------------|
| KP article bodies | Correct content | All show same "Postponement rumours" text | Selenium blank profile, KP needs JS |
| Ekantipur boilerplate | Clean text | "Sign In", share buttons visible | Fresh Selenium session picks up full page chrome |
| Author byline in body | Stripped | "Pvt. Name Date" visible | Junk pattern doesn't cover this format |

---

## Steps to Fix Right Now

### Step 1 — Pull latest changes
```bash
git pull
```

### Step 2 — Check Selenium profile
Make sure `USE_SELENIUM=True` and `SELENIUM_HEADLESS=True` are set in `.env`.
A headless Selenium session may not handle JS paywalls well.

Try setting headless to `False` temporarily so you can see what the browser sees:
```env
SELENIUM_HEADLESS=False
```

### Step 3 — Validate your translation is working
```bash
cd governance_weekly
python validate_setup.py
```

### Step 4 — Run the pipeline
```bash
python ../start_governance_weekly.py
```

---

## Why Your Machine Works Fine

| Factor | Your machine | Collaborator's machine |
|--------|-------------|----------------------|
| Selenium session | Has cookies/history from prior runs | Fresh blank profile |
| KP JS rendering | May load correctly from prior state | JS-only skeleton served |
| Ekantipur layout | Site may render differently per session | Full login overlay captured |
| Translation | Gemini configured and tested | May have just been set up |

This class of bug is **non-deterministic** — it depends on how the remote site
responds to a cold Selenium session vs a warm one.

---

## Long-term Fix (in the code)

The permanent fix is in `kathmandu_post.py` — force Selenium for article body fetches:

```python
for link in article_links:
    html = self.fetch(link, use_selenium=True)  # Force for JS rendering
```

And add the boilerplate patterns to `article_extractor.py`'s `junk_patterns` list.

Both fixes have been pushed to the repo. Pull and re-run.
