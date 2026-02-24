from .keywords import (
    tier1_election_keywords, tier2_political_keywords, tier3_context_keywords,
    election_keywords, governance_keywords, exclude_keywords
)
from config import Config

class Classifier:
    """
    WEIGHTED SCORING Classifier for Nepal March 5, 2026 Election
    Pre-election phase: Captures political maneuvering + direct election news
    
    Scoring:
    - Tier 1 (Direct Election): 5 points each
    - Tier 2 (Political Context): 3 points each  
    - Tier 3 (General Context): 1 point each
    - Threshold: 5 points to pass
    """
    def __init__(self):
        # Weighted keyword tiers
        self.tier1_keywords = tier1_election_keywords  # 5 points
        self.tier2_keywords = tier2_political_keywords  # 3 points
        self.tier3_keywords = tier3_context_keywords    # 1 point
        self.exclude_keywords = exclude_keywords
        
        # Scoring weights
        self.TIER1_WEIGHT = 5  # Direct election terms
        self.TIER2_WEIGHT = 3  # High-intent political context
        self.TIER3_WEIGHT = 1  # General context
        
        # Threshold to pass (5 = one direct term OR two political terms)
        self.PASS_THRESHOLD = 5
    
    def classify(self, text):
        """
        WEIGHTED SCORING classification
        Returns a dictionary with categories, relevance score, and exclusion status.
        """
        text_lower = text.lower()
        
        # Extract title for stricter exclusion check
        title_line = text_lower.split('\n')[0] if text_lower else ""
        
        # ===========================================
        # STEP 1: Check exclusion keywords FIRST
        # ===========================================
        for k in self.exclude_keywords:
            k_lower = k.lower()
            # If exclusion keyword is in title, definitely exclude
            if k_lower in title_line:
                return {
                    "categories": [],
                    "relevance_score": 0,
                    "weighted_score": 0,
                    "is_excluded": True,
                    "exclusion_reason": f"Title contains excluded term: {k}"
                }
            
            # Check body for strong exclusion indicators
            strong_excludes = [
                "nepse", "stock market", "share market", "beauty pageant",
                "mrs world", "miss world", "tourist", "tourism", "pilgrimage",
                "trump", "biden", "venezuela", "poem", "poetry", "poet",
                "hacking", "cyber attack", "cricket", "football"
            ]
            if k_lower in strong_excludes and k_lower in text_lower:
                return {
                    "categories": [],
                    "relevance_score": 0,
                    "weighted_score": 0,
                    "is_excluded": True,
                    "exclusion_reason": f"Body contains excluded term: {k}"
                }
        
        # ===========================================
        # STEP 2: Calculate WEIGHTED SCORE
        # ===========================================
        tier1_matches = []
        tier2_matches = []
        tier3_matches = []
        
        # Count Tier 1 matches (5 points each)
        for k in self.tier1_keywords:
            if k.lower() in text_lower:
                tier1_matches.append(k)
        
        # Count Tier 2 matches (3 points each)
        for k in self.tier2_keywords:
            if k.lower() in text_lower:
                tier2_matches.append(k)
        
        # Count Tier 3 matches (1 point each)
        for k in self.tier3_keywords:
            if k.lower() in text_lower:
                tier3_matches.append(k)
        
        # Calculate weighted score
        weighted_score = (
            len(tier1_matches) * self.TIER1_WEIGHT +
            len(tier2_matches) * self.TIER2_WEIGHT +
            len(tier3_matches) * self.TIER3_WEIGHT
        )
        
        # ===========================================
        # STEP 3: Check if passes threshold
        # ===========================================
        if weighted_score < self.PASS_THRESHOLD:
            return {
                "categories": [],
                "relevance_score": 0,
                "weighted_score": weighted_score,
                "is_excluded": True,
                "exclusion_reason": f"Score {weighted_score} below threshold {self.PASS_THRESHOLD}",
                "tier1_matches": len(tier1_matches),
                "tier2_matches": len(tier2_matches),
                "tier3_matches": len(tier3_matches)
            }
        
        # ===========================================
        # STEP 4: Build categories and final score
        # ===========================================
        found_categories = ["Election"]  # Always Election if passes
        
        # Add Governance if has tier1 election commission keywords
        if any("election commission" in k.lower() or "निर्वाचन आयोग" in k for k in tier1_matches):
            found_categories.append("Governance")
        
        # Relevance score for sorting (backward compat)
        relevance_score = weighted_score
        
        return {
            "categories": found_categories,
            "relevance_score": relevance_score,
            "weighted_score": weighted_score,
            "is_excluded": False,
            "tier1_matches": len(tier1_matches),
            "tier2_matches": len(tier2_matches),
            "tier3_matches": len(tier3_matches),
            "matched_keywords": {
                "tier1": tier1_matches[:5],  # Top 5 for logging
                "tier2": tier2_matches[:5],
                "tier3": tier3_matches[:3]
            }
        }
