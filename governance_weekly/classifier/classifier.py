from .keywords import *
from config import Config

class Classifier:
    def __init__(self):
        self.categories = {
            "Corruption": corruption_keywords,
            "Irregularity": irregularity_keywords,
            "Gender Equality and Social Inclusion": gender_equality_keywords,
            "Economy": economy_keywords,
            "Political": political_keywords,
            "Service Delivery": service_delivery_keywords,
            "Human Rights": human_rights_keywords,
            "Election": election_keywords,
            "Environment/Climate Change": environment_keywords,
            "Education": education_keywords,
            "Health": health_keywords,
            "Migration": migration_keywords,
            "Natural Disaster": natural_disaster_keywords,
            "Governance": governance_keywords
        }
        
        # Category priority weights (higher = more important)
        self.priority_weights = {
            "Corruption": 10,
            "Irregularity": 9,
            "Human Rights": 8,
            "Gender Equality and Social Inclusion": 7,
            "Election": 6,
            "Political": 5,
            "Service Delivery": 4,
            "Health": 3,
            "Education": 3,
            "Economy": 2,
            "Environment/Climate Change": 2,
            "Migration": 2,
            "Natural Disaster": 2,
            "Governance": 1
        }
    
    def classify(self, text):
        """
        Returns a dictionary with categories, relevance score, and exclusion status.
        Text should ideally be English (translated).
        """
        text_lower = text.lower()
        
        # Extract title (first line) for stricter exclusion check
        # We don't want to exclude news just because the body contains "opinion"
        title_line = text_lower.split('\n')[0] if text_lower else ""
        
        # Check exclusion - primarily against Title
        # Some keywords might be safe to check in body (like "photo gallery"), but "opinion" is risky in body
        
        # Split exclude keywords into "title only" (risky ones) and "anywhere" (safe ones)
        # For now, let's apply ALL exclude keywords to TITLE ONLY to be safe and avoid missing news
        # Exception: "photo gallery" etc might be in body. 
        
        # Better approach: Check if exclude keyword is in Title OR if it's a very strong content indicator
        
        is_excluded = False
        for k in exclude_keywords:
            k_lower = k.lower()
            # If keyword is in title, definitely exclude
            if k_lower in title_line:
                is_excluded = True
                break
            
            # If keyword is "photo gallery" or similar non-text content, check body too
            if k_lower in ["photo gallery", "in pictures", "gallery", "तस्बिर", "तस्वीर", "फोटो फिचर"] and k_lower in text_lower:
                is_excluded = True
                break
                
        if is_excluded:
            return {
                "categories": [],
                "relevance_score": 0,
                "is_excluded": True
            }

        found_categories = []
        score = 0
        
        for cat, keywords in self.categories.items():
            count = sum(1 for k in keywords if k.lower() in text_lower)
            # Stricter requirements: 3+ matches for high-priority, 2+ for medium, 1+ for low
            priority = self.priority_weights.get(cat, 0)
            if priority >= 7:
                min_matches = 3  # Corruption, Irregularity, Human Rights, Gender Equality
            elif priority >= 4:
                min_matches = 2  # Election, Political, Service Delivery
            else:
                min_matches = 1  # Economy, Health, Education, etc.
            
            if count >= min_matches:
                found_categories.append(cat)
                # Use priority weight for scoring
                weight = self.priority_weights.get(cat, 1.0)
                score += (count * weight)
        
        # Sort categories by priority (highest first) so primary category is first
        found_categories.sort(key=lambda c: self.priority_weights.get(c, 0), reverse=True)
        
        return {
            "categories": found_categories,
            "relevance_score": score,
            "is_excluded": False
        }
