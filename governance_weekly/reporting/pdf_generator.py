from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

# Use default Helvetica for English text (translations are in English)
# No need for Devanagari font since we're using translated English text
UNICODE_FONT = 'Helvetica'
logger.info("Using Helvetica font for English translations")

def build_pdf(items_by_category, out_path, date_range_str):
    doc = SimpleDocTemplate(out_path, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    
    # Custom Styles - Compact layout for shorter PDF
    styles.add(ParagraphStyle(name='GovTitle', parent=styles['Title'], fontSize=20, spaceAfter=12, fontName=UNICODE_FONT))
    styles.add(ParagraphStyle(name='GovHeading', parent=styles['Heading2'], fontSize=14, spaceBefore=8, spaceAfter=6, textColor=colors.darkblue, fontName=UNICODE_FONT))
    styles.add(ParagraphStyle(name='ArticleTitle', parent=styles['Heading3'], fontSize=11, spaceBefore=6, spaceAfter=3, fontName=UNICODE_FONT))
    styles.add(ParagraphStyle(name='ArticleMeta', parent=styles['BodyText'], fontSize=8, textColor=colors.grey, spaceAfter=2, fontName=UNICODE_FONT))
    styles.add(ParagraphStyle(name='ArticleSummary', parent=styles['BodyText'], fontSize=9, leading=11, fontName=UNICODE_FONT, alignment=TA_JUSTIFY))

    flow = []
    
    # Cover Page - Compact
    flow.append(Paragraph("Nepal Election Weekly", styles['GovTitle']))
    flow.append(Paragraph(f"March 5, 2026 Election Coverage", styles['Normal']))
    flow.append(Paragraph(f"Date Range: {date_range_str}", styles['Normal']))
    flow.append(Spacer(1, 12))
    flow.append(Paragraph("Election and Governance news from Nepal - Focused coverage for March 2026 Election.", styles['Italic']))
    flow.append(Spacer(1, 12))
    
    # Content - Sort categories (Election first, then Governance)
    priority_order = [
        "Election",
        "Governance"
    ]
    sorted_categories = sorted(items_by_category.keys(), 
                              key=lambda x: priority_order.index(x) if x in priority_order else 999)
    
    for cat in sorted_categories:
        items = items_by_category[cat]
        if not items: continue
        
        flow.append(Paragraph(f"{cat} ({len(items)} articles)", styles['GovHeading']))
        
        # Sort items within category by impact score (not just relevance)
        sorted_items = sorted(items, key=lambda x: x.get('impact_score', x.get('relevance_score', 0)), reverse=True)
        
        for it in sorted_items:
            # Title with impact indicator
            title_text = it.get('title_translated') or it.get('title_original', 'Untitled')
            # Escape special characters for PDF
            title_text = title_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            impact = it.get('impact_score', 0)
            relevance = it.get('relevance_score', 0)
            
            # Visual impact indicator with stars
            if impact >= 40:
                priority_marker = "★★★★★"  # Critical
            elif impact >= 30:
                priority_marker = "★★★★"   # High
            elif impact >= 20:
                priority_marker = "★★★"    # Medium
            elif impact >= 15:
                priority_marker = "★★"     # Low
            else:
                priority_marker = "★"      # Minimal
                
            flow.append(Paragraph(f"{priority_marker} {title_text}", styles['ArticleTitle']))
            
            # Meta with clickable URL
            source = it.get('source_domain', 'Unknown')
            date_pub = it.get('published_at', 'Unknown Date')
            url = it.get('url', '#')
            
            # Create clickable link
            meta_line = f'Source: <a href="{url}" color="blue">{url}</a> | {date_pub} | Impact: {impact:.1f}'
            flow.append(Paragraph(meta_line, styles['ArticleMeta']))
            
            # Summary - Full comprehensive summary (5-6 lines, ~500 chars)
            summary_text = it.get('summary', 'No summary available.')
            summary_text = summary_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            flow.append(Paragraph(summary_text, styles['ArticleSummary']))
            
            flow.append(Spacer(1, 8))
            
    # Footer logic can be added via canvas maker if strictly needed
    
    try:
        doc.build(flow)
        logger.info(f"PDF generated at {out_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to generate PDF: {e}")
        return False
