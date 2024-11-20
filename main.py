from aqt import mw
from aqt.qt import QAction, QIcon
from aqt.utils import showInfo
from .gui.chat_window import ChatWindow
from .api.ai_interface import AIInterface
from .config import Config
from .utils.helpers import clean_message_text  # Import the function from utils
import re
from bs4 import BeautifulSoup

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
