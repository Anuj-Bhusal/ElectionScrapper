from sqlalchemy import Column, String, Integer, Float, Text, DateTime, JSON, Boolean, create_engine
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    url = Column(String, primary_key=True)
    source_domain = Column(String, nullable=False, index=True)
    title_original = Column(String, nullable=True)
    full_text_original = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    
    language = Column(String, default="ne") # ne or en
    
    # Translation
    title_translated = Column(String, nullable=True)
    full_text_translated = Column(Text, nullable=True)
    translation_metadata = Column(JSON, nullable=True) # engine used, confidence
    
    # Classification & Reporting
    summary = Column(Text, nullable=True)
    categories = Column(JSON, nullable=True) # list of strings
    relevance_score = Column(Float, default=0.0)
    
    # Deduplication & Provenance
    content_hash = Column(String, index=True, nullable=True)
    raw_html = Column(Text, nullable=True)
    
    # Review Workflow
    status = Column(String, default="pending_review", index=True) # pending_review, verified, rejected
    requires_review = Column(Boolean, default=False)
    reviewer_notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Article(source={self.source_domain}, title={self.title_original})>"
