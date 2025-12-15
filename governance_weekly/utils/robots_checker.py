import urllib.robotparser
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class RobotsChecker:
    _parsers = {}

    @classmethod
    def is_allowed(cls, url, user_agent):
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}::{parsed.netloc}" # simplified key
        
        if base_url not in cls._parsers:
            rp = urllib.robotparser.RobotFileParser()
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            rp.set_url(robots_url)
            try:
                rp.read()
                cls._parsers[base_url] = rp
            except Exception as e:
                logger.warning(f"Could not read robots.txt for {parsed.netloc}: {e}")
                # If robots.txt fails, default to allowed or disallowed? 
                # Usually standard practice is to allow if robots.txt is missing/unreachable
                # unless strict.
                return True 
        
        return cls._parsers[base_url].can_fetch(user_agent, url)

def is_allowed(url, user_agent):
    return RobotsChecker.is_allowed(url, user_agent)
