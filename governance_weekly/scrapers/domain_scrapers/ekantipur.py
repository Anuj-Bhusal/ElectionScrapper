print("DEBUG: Importing BaseScraper", flush=True)
from scrapers.base_scraper import BaseScraper
print("DEBUG: Importing Extractor", flush=True)
from extractor.article_extractor import extract_article
print("DEBUG: Extractor Imported", flush=True)
import logging

logger = logging.getLogger(__name__)

class EkantipurScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://ekantipur.com", "ekantipur.com")

    def run(self):
        logger.info(f"Starting scrape for {self.domain}")
        
        # 1. Fetch Homepage
        homepage_html = self.fetch(self.base_url)
        if not homepage_html:
            return []
            
        # 2. Extract Links
        # Ekantipur article links usually look like: /news/2024/01/01/title...
        # or /business/2024...
        links = self.extract_links(homepage_html)
        
        # Filter for likely article links (simple heuristic: has year/month or strict 'news' path)
        article_links = [l for l in links if any(x in l for x in ["/news/", "/business/", "/national/", "/pradesh/"])]
        
        # Limit
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
                    data['language'] = 'ne' # Default for Ekantipur
                    results.append(data)
            
        return results
