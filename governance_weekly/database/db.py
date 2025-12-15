import sqlite3
import json
import logging
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)

class DB:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(Config.DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()

    def init_db(self):
        self.connect()
        # Create table mimicking the previous SQLAlchemy model
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                url TEXT PRIMARY KEY,
                source_domain TEXT NOT NULL,
                title_original TEXT,
                full_text_original TEXT,
                published_at TIMESTAMP,
                fetched_at TIMESTAMP,
                language TEXT,
                title_translated TEXT,
                full_text_translated TEXT,
                translation_metadata TEXT,
                summary TEXT,
                categories TEXT,
                relevance_score REAL,
                content_hash TEXT,
                raw_html TEXT,
                status TEXT,
                requires_review INTEGER,
                reviewer_notes TEXT
            )
        ''')
        self.conn.commit()

# Singleton-ish pattern for main.py to use
def get_db():
    db = DB()
    db.connect()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = DB()
    db.init_db()
    db.close()
