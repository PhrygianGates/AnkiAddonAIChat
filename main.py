from aqt import mw
from aqt.qt import QAction, QIcon
from aqt.utils import showInfo
from .gui.chat_window import ChatWindow
from .config import Config
from .utils.helpers import clean_message_text  # Import the function from utils
from .gui.config_window import ConfigWindow  # Import the ConfigWindow

def start_chat():
    card = mw.reviewer.card
    if card:
        fields = [clean_message_text(field) for field in card.note().fields]
        card_content = fields[0]
        additional_info = "\n".join(fields[1:])
    else:
        showInfo("Please open the card view to start a chat.")
        return
    
    chat_window = ChatWindow(card_content=card_content, additional_info=additional_info, language=Config.get_language())
    chat_window.exec()

def open_config():
    config_window = ConfigWindow()
    config_window.exec()

def add_chat_button():
    menu = mw.form.menuTools.addMenu("AI Chat")
    
    chat_action = QAction(QIcon(":/icons/chat_icon.png"), "Start Chat", mw)
    chat_action.triggered.connect(start_chat)
    menu.addAction(chat_action)
    
    config_action = QAction(QIcon(":/icons/config_icon.png"), "Configure", mw)
    config_action.triggered.connect(open_config)
    menu.addAction(config_action)

# add_chat_button()
