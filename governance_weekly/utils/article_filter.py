"""
Smart filtering utilities for selecting top governance articles
"""
import re
from difflib import SequenceMatcher
from typing import List, Dict, Set

def normalize_text(text: str) -> str:
    """Normalize text for comparison"""
    if not text:
        return ""
    # Remove special chars, extra spaces, lowercase
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
    """
    Check if article is duplicate based on title and summary similarity
    Very strict thresholds to ensure no duplicates
    
    Args:
        article: Article to check
        seen_articles: List of already seen articles
        title_threshold: Similarity threshold for titles (0-1, default 0.90 = very strict)
        summary_threshold: Similarity threshold for summaries (0-1, default 0.80 = very strict)
    
    Returns:
        True if duplicate found
    """
    current_title = article.get('title_translated') or article.get('title_original', '')
    current_summary = article.get('summary', '')
    
    for seen in seen_articles:
        seen_title = seen.get('title_translated') or seen.get('title_original', '')
        seen_summary = seen.get('summary', '')
        
        # Check title similarity (very strict)
        title_sim = calculate_similarity(current_title, seen_title)
        
        if title_sim >= title_threshold:
            return True
        
        # Check summary similarity if titles are moderately similar
        if title_sim >= 0.6:
            summary_sim = calculate_similarity(current_summary, seen_summary)
            
            if summary_sim >= summary_threshold:
                return True
        
        # Also check combined title+summary for sneaky duplicates
        if title_sim >= 0.7:
            current_combined = f"{current_title} {current_summary}"
            seen_combined = f"{seen_title} {seen_summary}"
            combined_sim = calculate_similarity(current_combined, seen_combined)
            
            if combined_sim >= 0.85:
                return True
    
    return False

def calculate_impact_score(article: Dict) -> float:
    """
    Calculate impact score based on multiple factors
    
    Factors:
    - Category priority (Corruption > Irregularity > Human Rights > etc.)
    - Keyword relevance score
    - Content length (longer = more detailed)
    - Source reputation (can be enhanced later)
    """
    score = 0.0
    
    # Base relevance score from classifier
    score += article.get('relevance_score', 0)
    
    # Category priority bonus
    categories = article.get('categories', [])
    category_weights = {
        "Corruption": 20,
        "Irregularity": 18,
        "Human Rights": 15,
        "Gender Equality and Social Inclusion": 12,
        "Election": 10,
        "Political": 8,
        "Service Delivery": 7,
        "Health": 6,
        "Education": 6,
        "Economy": 5,
        "Environment/Climate Change": 5,
        "Migration": 4,
        "Natural Disaster": 4,
        "Governance": 3
    }
    
    # Add highest category weight
    if categories:
        max_cat_weight = max(category_weights.get(cat, 0) for cat in categories)
        score += max_cat_weight
    
    # Content depth bonus (longer summaries = more substantive)
    summary_length = len(article.get('summary', ''))
    if summary_length > 300:
        score += 5
    elif summary_length > 150:
        score += 3
    
    # Multiple category bonus (cross-cutting issues are important)
    if len(categories) >= 3:
        score += 5
    elif len(categories) >= 2:
        score += 2
    
    return score

def filter_top_articles(articles: List[Dict], max_articles: int = 40, min_impact_score: float = 10.0) -> List[Dict]:
    """
    Filter articles to get top N most impactful and unique ones
    
    Args:
        articles: List of all articles
        max_articles: Maximum number of articles to return
        min_impact_score: Minimum impact score threshold
    
    Returns:
        List of filtered articles
    """
    # Calculate impact scores
    for article in articles:
        article['impact_score'] = calculate_impact_score(article)
    
    # Sort by impact score (highest first)
    articles_sorted = sorted(articles, key=lambda x: x['impact_score'], reverse=True)
    
    # Deduplicate while maintaining order
    unique_articles = []
    seen_articles = []
    
    for article in articles_sorted:
        # Skip if below minimum threshold
        if article['impact_score'] < min_impact_score:
            continue
        
        # Check for duplicates
        if not is_duplicate(article, seen_articles):
            unique_articles.append(article)
            seen_articles.append(article)
            
            # Stop if we've reached max articles
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
