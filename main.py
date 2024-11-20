from aqt import mw
from aqt.qt import QAction, QIcon
from aqt.utils import showInfo
from .gui.chat_window import ChatWindow
from .api.ai_interface import AIInterface
from .config import Config
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

def start_chat():
    card = mw.reviewer.card
    if card:
        fields = [clean_message_text(field) for field in card.note().fields]
        card_content = fields[0]
        additional_info = "\n".join(fields[1:])
    else:
        card_content = "No content available"
        additional_info = "No additional information available"
    
    chat_window = ChatWindow(card_content=card_content, additional_info=additional_info, language=Config.get_language())
    chat_window.exec()

def add_chat_button():
    action = QAction(QIcon(":/icons/chat_icon.png"), "Chat with AI", mw)
    action.triggered.connect(start_chat)
    mw.form.menuTools.addAction(action)

# add_chat_button()
