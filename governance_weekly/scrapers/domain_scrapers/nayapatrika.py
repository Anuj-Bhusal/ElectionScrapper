from scrapers.base_scraper import BaseScraper
from extractor.article_extractor import extract_article
import logging

logger = logging.getLogger(__name__)

class NayapatrikaScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://nayapatrikadaily.com", "nayapatrikadaily.com")

    def run(self):
        logger.info(f"Starting scrape for {self.domain}")
        
        homepage_html = self.fetch(self.base_url)
        if not homepage_html:
            return []
            
        links = self.extract_links(homepage_html)
        
        # Nayapatrika links: /news-details/{id}/
        article_links = [l for l in links if "/news-details/" in l]
        
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
                    data['language'] = 'ne'  # Nayapatrika is Nepali
                    results.append(data)
            
        return results
