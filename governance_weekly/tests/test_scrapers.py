import unittest
from unittest.mock import MagicMock, patch
from scrapers.base_scraper import BaseScraper
from scrapers.domain_scrapers.ekantipur import EkantipurScraper

class TestBaseScraper(unittest.TestCase):
    def test_extract_links(self):
        scraper = BaseScraper("https://example.com", "example.com")
        html = '<html><body><a href="/news/123">Link 1</a><a href="https://other.com">Link 2</a></body></html>'
        links = scraper.extract_links(html)
        self.assertIn("https://example.com/news/123", links)
        self.assertNotIn("https://other.com", links)

class TestEkantipurScraper(unittest.TestCase):
    @patch('scrapers.base_scraper.requests.get')
    def test_run_mock(self, mock_get):
        # Mock homepage
        mock_response_home = MagicMock()
        mock_response_home.text = '<html><a href="/news/2024/01/01/test">Test Article</a></html>'
        mock_response_home.status_code = 200
        
        # Mock article page
        mock_response_art = MagicMock()
        mock_response_art.text = '<html><title>Test Title</title><article>Test content here.</article></html>'
        mock_response_art.status_code = 200
        
        mock_get.side_effect = [mock_response_home, mock_response_art]
        
        with patch('scrapers.base_scraper.is_allowed', return_value=True):
            scraper = EkantipurScraper()
            scraper.max_articles = 1
            results = scraper.run()
            
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]['title'], "Test Title")

if __name__ == '__main__':
    unittest.main()
