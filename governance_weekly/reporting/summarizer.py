import logging

logger = logging.getLogger(__name__)

class Summarizer:
    def __init__(self):
        # Could init API clients here (Gemini, OpenAI etc.)
        self.mode = "heuristic" # text rank or first N sentences

    def summarize(self, text):
        if not text:
            return ""
            
        # Extract key sentences for a comprehensive 5-6 line summary
        # Aim for ~400-500 characters to fit important details
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        if not sentences:
            return ""
        
        summary_parts = []
        char_count = 0
        max_chars = 500  # Enough for 5-6 lines with important info
        min_chars = 300  # Ensure we get enough detail
        
        # Take sentences until we have good coverage
        for i, sent in enumerate(sentences):
            # Skip very short sentences (likely fragments)
            if len(sent) < 10:
                continue
            
            potential_length = char_count + len(sent) + 2  # +2 for ". "
            
            # If we're past min and adding this exceeds max, check if we should stop
            if char_count >= min_chars and potential_length > max_chars:
                break
            
            # If way over max, truncate this sentence and stop
            if potential_length > max_chars + 50:
                remaining = max_chars - char_count
                if remaining > 50:  # Only add if meaningful space left
                    summary_parts.append(sent[:remaining].strip() + "...")
                break
            
            summary_parts.append(sent)
            char_count = potential_length
            
            # Got enough sentences (5-6 sentences or ~500 chars)
            if len(summary_parts) >= 6 or char_count >= max_chars:
                break
        
        summary = ". ".join(summary_parts)
        if summary and not summary.endswith(('.', '...')):
            summary += "."
        
        return summary

# Placeholder for actual Gemini integration
# class GeminiSummarizer(Summarizer): ...
