
import re
from bs4 import BeautifulSoup

def clean_message_text(message):
    """
    Processes a message to remove HTML tags, extra whitespace, and formatting.
    Falls back to plain text processing if not HTML.
    """
    try:
        # Attempt to parse as HTML and extract text
        soup = BeautifulSoup(message, "html.parser")
        clean_text = soup.get_text(separator=" ")
    except Exception:
        # If HTML parsing fails, assume plain text
        clean_text = message

    # Remove excessive whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text