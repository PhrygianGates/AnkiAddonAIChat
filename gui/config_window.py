
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from ..config import Config

class ConfigWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure AI Chat")
        self.setGeometry(100, 100, 300, 200)
        
        self.layout = QVBoxLayout()
        
        self.api_key_label = QLabel("API Key:", self)
        self.layout.addWidget(self.api_key_label)
        
        self.api_key_input = QLineEdit(self)
        self.api_key_input.setText(Config.API_KEY)
        self.layout.addWidget(self.api_key_input)
        
        self.language_label = QLabel("Language:", self)
        self.layout.addWidget(self.language_label)
        
        self.language_combo = QComboBox(self)
        self.language_combo.addItems(["en", "fr"])
        self.language_combo.setCurrentText(Config.get_language())
        self.layout.addWidget(self.language_combo)
        
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_config)
        self.layout.addWidget(self.save_button)
        
        self.setLayout(self.layout)
    
    def save_config(self):
        Config.API_KEY = self.api_key_input.text()
        Config.set_language(self.language_combo.currentText())
        Config.save_to_file("config.json")
        self.accept()