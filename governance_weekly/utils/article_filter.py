"""
WEIGHTED SCORING filter for Nepal March 5, 2026 Election
Pre-election phase: Captures political maneuvering + direct election news
"""
import re
from difflib import SequenceMatcher
from typing import List, Dict, Set

# Import keyword tiers for validation
try:
    from classifier.keywords import (
        tier1_election_keywords, tier2_political_keywords, 
        tier3_context_keywords, exclude_keywords
    )
except ImportError:
    tier1_election_keywords = []
    tier2_political_keywords = []
    tier3_context_keywords = []
    exclude_keywords = []

# Scoring weights
TIER1_WEIGHT = 5  # Direct election terms
TIER2_WEIGHT = 3  # High-intent political context
TIER3_WEIGHT = 1  # General context
PASS_THRESHOLD = 5

def normalize_text(text: str) -> str:
    """Normalize text for comparison"""
    if not text:
        return ""
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    text = ' '.join(text.split())
    return text

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity ratio between two texts"""
    norm1 = normalize_text(text1)
    norm2 = normalize_text(text2)
    
    if not norm1 or not norm2:
        return 0.0
    
    return SequenceMatcher(None, norm1, norm2).ratio()

def is_duplicate(article: Dict, seen_articles: List[Dict], title_threshold: float = 0.90, summary_threshold: float = 0.80) -> bool:
    """Check if article is duplicate based on title and summary similarity"""
    current_title = article.get('title_translated') or article.get('title_original', '')
    current_summary = article.get('summary', '')
    
    for seen in seen_articles:
        seen_title = seen.get('title_translated') or seen.get('title_original', '')
        seen_summary = seen.get('summary', '')
        
        title_sim = calculate_similarity(current_title, seen_title)
        
        if title_sim >= title_threshold:
            return True
        
        if title_sim >= 0.6:
            summary_sim = calculate_similarity(current_summary, seen_summary)
            if summary_sim >= summary_threshold:
                return True
        
        if title_sim >= 0.7:
            current_combined = f"{current_title} {current_summary}"
            seen_combined = f"{seen_title} {seen_summary}"
            combined_sim = calculate_similarity(current_combined, seen_combined)
            if combined_sim >= 0.85:
                return True
    
    return False

def calculate_weighted_score(article: Dict) -> float:
    """
    Calculate weighted score based on keyword tiers
    Tier 1 (Direct Election): 5 points each
    Tier 2 (Political Context): 3 points each
    Tier 3 (General Context): 1 point each
    """
    title = (article.get('title_translated') or article.get('title_original', '')).lower()
    summary = (article.get('summary', '')).lower()
    combined = f"{title} {summary}"
    
    tier1_count = sum(1 for k in tier1_election_keywords if k.lower() in combined)
    tier2_count = sum(1 for k in tier2_political_keywords if k.lower() in combined)
    tier3_count = sum(1 for k in tier3_context_keywords if k.lower() in combined)
    
    weighted_score = (
        tier1_count * TIER1_WEIGHT +
        tier2_count * TIER2_WEIGHT +
        tier3_count * TIER3_WEIGHT
    )
    
    return weighted_score

def has_exclusion_keyword(article: Dict) -> bool:
    """Check if article contains strong exclusion keywords"""
    title = (article.get('title_translated') or article.get('title_original', '')).lower()
    summary = (article.get('summary', '')).lower()
    combined = f"{title} {summary}"
    
    strong_excludes = [
        "nepse", "stock market", "share market", "trading volume",
        "beauty pageant", "mrs world", "miss world", "mrs nepal",
        "tourist", "tourism", "pilgrimage", "pilgrim", "lumbini",
        "trump", "biden", "venezuela", "foreign policy",
        "poem", "poetry", "poet", "literature", "book launch",
        "cricket", "football", "sports", "entertainment",
        "hacking", "cyber attack", "data theft",
        "weather", "cold wave", "temperature"
    ]
    
    for keyword in strong_excludes:
        if keyword in combined:
            return True
    return False

def calculate_impact_score(article: Dict) -> float:
    """Calculate impact score using weighted scoring"""
    score = 0.0
    
    # Base: weighted score from keyword tiers
    weighted = calculate_weighted_score(article)
    score += weighted
    
    # Add classifier's relevance score
    score += article.get('relevance_score', 0)
    
    # Category bonuses
    categories = article.get('categories', [])
    if "Election" in categories:
        score += 10
    if "Governance" in categories:
        score += 5
    
    # Content depth bonus
    summary_length = len(article.get('summary', ''))
    if summary_length > 300:
        score += 5
    elif summary_length > 150:
        score += 3
    
    return score

def filter_top_articles(articles: List[Dict], max_articles: int = 40, min_impact_score: float = 10.0) -> List[Dict]:
    """
    WEIGHTED SCORING filter
    Passes articles with weighted score >= 5 (threshold)
    
    Args:
        articles: List of all articles
        max_articles: Maximum number of articles to return
        min_impact_score: Minimum impact score threshold
    
    Returns:
        List of filtered articles
    """
    # STEP 1: Filter to only Election/Governance articles
    election_articles = []
    for article in articles:
        categories = article.get('categories', [])
        if "Election" in categories or "Governance" in categories:
            election_articles.append(article)
    
    # STEP 2: Validate with weighted scoring
    validated_articles = []
    for article in election_articles:
        # Must NOT have exclusion keywords
        if has_exclusion_keyword(article):
            continue
        
        # Calculate weighted score
        weighted = calculate_weighted_score(article)
        
        # Must pass threshold (5 points)
        if weighted >= PASS_THRESHOLD:
            article['weighted_score'] = weighted
            validated_articles.append(article)
    
    # STEP 3: Calculate impact scores
    for article in validated_articles:
        article['impact_score'] = calculate_impact_score(article)
    
    # STEP 4: Sort by impact score
    articles_sorted = sorted(validated_articles, key=lambda x: x['impact_score'], reverse=True)
    
    # STEP 5: Deduplicate
    unique_articles = []
    seen_articles = []
    
    for article in articles_sorted:
        if article['impact_score'] < min_impact_score:
            continue
        
        if not is_duplicate(article, seen_articles):
            unique_articles.append(article)
            seen_articles.append(article)
            
            if len(unique_articles) >= max_articles:
                break
    
    return unique_articles

def get_category_distribution(articles: List[Dict]) -> Dict[str, int]:
    """Get count of articles per category"""
    distribution = {}
    for article in articles:
        for cat in article.get('categories', []):
            distribution[cat] = distribution.get(cat, 0) + 1
    return distribution
