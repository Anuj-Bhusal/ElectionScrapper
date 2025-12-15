print("DEBUG: BS imports start", flush=True)
import requests
print("DEBUG: Imported requests", flush=True)
from bs4 import BeautifulSoup
print("DEBUG: Imported BS4", flush=True)
import time
import logging
from urllib.parse import urljoin
from utils.robots_checker import is_allowed
print("DEBUG: Imported Robots", flush=True)
from utils.selenium_manager import get_driver
print("DEBUG: Imported Selenium Manager", flush=True)
from config import Config
print("DEBUG: Imported Config", flush=True)

logger = logging.getLogger(__name__)

class BaseScraper:
    def __init__(self, base_url, domain):
        self.base_url = base_url
        self.domain = domain
        self.rate_limit = Config.RATE_LIMIT_SEC
        self.max_articles = Config.MAX_ARTICLES_PER_SITE
        self.headers = {"User-Agent": Config.USER_AGENT}
        
    def fetch(self, url, use_selenium=False):
        if not is_allowed(url, self.headers["User-Agent"]):
            logger.warning(f"Robots.txt disallows: {url}")
            return None
            
        try:
            time.sleep(self.rate_limit)
            
            if use_selenium or Config.USE_SELENIUM: # Global override or per-call
                driver = get_driver()
                driver.get(url)
                # Implement implicit wait or check for ready state if needed
                return driver.page_source
            else:
                r = requests.get(url, headers=self.headers, timeout=15)
                r.raise_for_status()
                return r.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def extract_links(self, html, pattern=None):
        if not html: return set()
        soup = BeautifulSoup(html, "html.parser")
        links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("/"):
                href = urljoin(self.base_url, href)
            
            # Basic domain check
            if self.domain in href:
                # Optional pattern filtering
                if pattern and pattern not in href:
                    continue
                links.add(href.split("#")[0])
        return links

    def run(self):
        """
        Main execution method found in subclasses.
        Should return a list of extracted article dictionaries.
        """
        raise NotImplementedError
