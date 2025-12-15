try:
    from readability import Document
except ImportError:
    Document = None
from bs4 import BeautifulSoup
import dateparser
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def extract_article(html, url):
    """
    Extracts the main content, title, and metadata from an article HTML.
    """
    if not html:
        return None
        
    try:
        if Document:
            doc = Document(html)
            title = doc.short_title()
            content_html = doc.summary()
        else:
            # Fallback for missing readability
            soup = BeautifulSoup(html, "html.parser")
            title = soup.title.string if soup.title else "No Title"
            # Try to find <article> or just body
            article_body = soup.find('article') or soup.body
            content_html = str(article_body) if article_body else html
        
        # Clean up tags using BeautifulSoup
        soup = BeautifulSoup(content_html, "html.parser")
        text_content = soup.get_text(separator="\n").strip()
        
        # Remove junk patterns (read time, date stamps, social media prompts, etc.)
        import re
        junk_patterns = [
            r'Read Time\s*:.*?\d+\s*(?:minute|min|second|sec)',  # Read Time : < 1 minute
            r'\d{4}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}\s+(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+\d{1,2}:\d{2}',  # Date stamps
            r'Share on Facebook.*?Share on Twitter',  # Social media
            r'Share via Email',
            r'Print this page',
            r'Advertisement',
            r'Related Articles?:?',
            r'Tags?:.*',
            r'Published on:.*',
            r'Updated on:.*',
            r'\[.*?\]',  # [Photo Gallery] etc
        ]
        
        for pattern in junk_patterns:
            text_content = re.sub(pattern, '', text_content, flags=re.IGNORECASE)
        
        # Remove excessive whitespace
        text_content = re.sub(r'\n\s*\n+', '\n\n', text_content)
        text_content = text_content.strip()
        
        # Metadata extraction (heuristic)
        # Often readability doesn't get the date well, so we might need custom parsing per site
        # or use generic meta tag scraping
        
        soup_full = BeautifulSoup(html, "html.parser")
        
        # Attempt to find published time
        published_at = None
        
        # Meta tags check
        meta_date = (
            soup_full.find("meta", property="article:published_time") or
            soup_full.find("meta", attrs={"name": "date"}) or
            soup_full.find("time")
        )
        
        if meta_date:
            content = meta_date.get("content") or meta_date.get("datetime") or meta_date.get_text()
            if content:
                published_at = dateparser.parse(content)
        
        return {
            "title": title,
            "full_text": text_content,
            "published_at": published_at,
            "raw_html": html
        }
        
    except Exception as e:
        logger.error(f"Extraction failed for {url}: {e}")
        return None
