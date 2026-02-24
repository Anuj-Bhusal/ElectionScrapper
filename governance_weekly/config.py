import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Scraper Settings
    MAX_ARTICLES_PER_SITE = int(os.getenv("MAX_ARTICLES_PER_SITE", 100))
    RATE_LIMIT_SEC = float(os.getenv("RATE_LIMIT_SEC", 1.0))
    USER_AGENT = os.getenv("USER_AGENT", "GovernanceWeeklyBot/1.0 (+https://accountabilitylab.org/)")
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "data", "gov_weekly.db").replace("\\", "/")
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    
    # Translation
    TRANSLATION_BACKEND = os.getenv("TRANSLATION_BACKEND", "google") # google, marian, gemini
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Drive
    DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")
    
    # Classification
    RELEVANCE_THRESHOLD = int(os.getenv("RELEVANCE_THRESHOLD", 1))
    
    # Report Filtering
    MAX_ARTICLES_IN_REPORT = int(os.getenv("MAX_ARTICLES_IN_REPORT", 40))
    MIN_IMPACT_SCORE = float(os.getenv("MIN_IMPACT_SCORE", 10.0))

    # Selenium
    USE_SELENIUM = os.getenv("USE_SELENIUM", "True").lower() == "true"
    SELENIUM_HEADLESS = os.getenv("SELENIUM_HEADLESS", "True").lower() == "true"
    
    # Robots.txt - Skip for personal/research use
    SKIP_ROBOTS_CHECK = os.getenv("SKIP_ROBOTS_CHECK", "True").lower() == "true"

os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(Config.DB_PATH), exist_ok=True)
