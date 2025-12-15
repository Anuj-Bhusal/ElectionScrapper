from scrapers.base_scraper import BaseScraper
from extractor.article_extractor import extract_article
import logging

logger = logging.getLogger(__name__)

class KathmanduPostScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://kathmandupost.com", "kathmandupost.com")

    def run(self):
        logger.info(f"Starting scrape for {self.domain}")
        
        homepage_html = self.fetch(self.base_url)
        if not homepage_html:
            return []
            
        links = self.extract_links(homepage_html)
        
        # KP links: https://kathmandupost.com/national/2024/01/01/...
        article_links = [l for l in links if any(x in l for x in ["/national/", "/politics/", "/investigation/"])]
        
        article_links = list(article_links)[:self.max_articles]
        
        results = []
        for link in article_links:
            html = self.fetch(link)
            if html:
                data = extract_article(html, link)
                if data and data['title']:
                    data['url'] = link
                    data['source_domain'] = self.domain
                    data['language'] = 'en' # KP is English
                    results.append(data)
                    
        return results
