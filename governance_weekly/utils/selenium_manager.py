from config import Config

_driver_instance = None

def get_driver():
    """
    Returns a singleton instance of the Selenium WebDriver.
    """
    global _driver_instance
    if _driver_instance is None:
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
        except ImportError:
            print("WARNING: Selenium not installed. Dynamic scraping disabled.", flush=True)
            return None

        options = Options()
        if Config.SELENIUM_HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"user-agent={Config.USER_AGENT}")
        
        # You might need to specify the path to chromedriver if it's not in PATH
        # service = Service("/path/to/chromedriver")
        # _driver_instance = webdriver.Chrome(service=service, options=options)
        
        _driver_instance = webdriver.Chrome(options=options)
        
    return _driver_instance

def close_driver():
    global _driver_instance
    if _driver_instance:
        _driver_instance.quit()
        _driver_instance = None
