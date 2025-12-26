from scrapers.base_scraper import BaseScraper
from extractor.article_extractor import extract_article
import logging
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class MyRepublicaScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://myrepublica.nagariknetwork.com", "myrepublica.nagariknetwork.com")

    def run(self):
        logger.info(f"Starting scrape for {self.domain}")
        
        homepage_html = self.fetch(self.base_url)
        if not homepage_html:
            return []
            
        links = self.extract_links(homepage_html)
        
        # Filter by current year (check for year pattern in URL)
        today = datetime.now()
        current_year_pattern = str(today.year)
        
        # MyRepublica links with year filter
        article_links = [l for l in links if ("/news/story/" in l or "/news/corruption/" in l or "/news/politics/" in l) and current_year_pattern in l]
        
        # Exclude opinion/blog/column/interview URLs
        article_links = [l for l in article_links if not any(x in l.lower() for x in ['/opinion/', '/blog/', '/column/', '/interview/', '/editorial/', '/perspective/', '/commentary/'])]
        
        article_links = list(article_links)[:self.max_articles]
        logger.info(f"Found {len(article_links)} potential articles")
        
        results = []
        for link in article_links:
            html = self.fetch(link)
            if html:
                data = extract_article(html, link)
                if data and data['title']:
                    data['url'] = link
                    data['source_domain'] = self.domain
                    data['language'] = 'en'  # MyRepublica is English
                    results.append(data)
            
        return results
