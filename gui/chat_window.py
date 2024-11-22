from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout
from ..api.ai_interface import AIInterface
from ..config import Config
from ..utils.record_audio import AudioRecorder

class ChatWindow(QDialog):
    def __init__(self, parent=None, card_content="", additional_info="", language="en"):
        super().__init__(parent)
        self.setWindowTitle("Chat with AI")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QVBoxLayout()
        
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.layout.addWidget(self.chat_display)
        
        self.input_field = QLineEdit(self)
        self.layout.addWidget(self.input_field)
        
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        
        self.audio_recorder = AudioRecorder()

        self.record_button = QPushButton("Record", self)
        self.record_button.clicked.connect(self.record_audio)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.record_button)
        self.layout.addLayout(button_layout)
        
        self.setLayout(self.layout)
        
        self.card_content = card_content
        self.additional_info = additional_info
        self.chat_history = ""
        self.language = language
        self.ai_interface = AIInterface(api_key=Config.API_KEY, language=self.language)
        
        self.questions = self.ai_interface.get_all_questions(self.card_content, self.additional_info)
        self.question_counter = 0
        
        self.ai_ask_question()

    def send_message(self):
        user_message = self.input_field.text()
        if user_message:
            self.chat_display.append(f"User: {user_message}")
            self.chat_history += f"User: {user_message}\n"
            self.input_field.clear()
            ai_response = self.get_ai_response()
            self.chat_display.append(f"AI: {ai_response}")
            self.chat_history += f"AI: {ai_response}\n"
            self.ai_ask_question()
    
    def get_ai_response(self):
        return self.ai_interface.get_response(self.card_content, self.additional_info, self.chat_history)
    
    def ai_ask_question(self):
        if self.question_counter < len(self.questions):
            ai_question = self.questions[self.question_counter]
            self.chat_display.append(f"AI: {ai_question}")
            self.chat_history += f"AI: {ai_question}\n"
            self.question_counter += 1
        else:
            self.chat_display.append("AI: No more questions for now. Good luck with your studies!")

    def record_audio(self):
        transcribed_text = self.audio_recorder.record_and_transcribe()
        if transcribed_text:
            self.input_field.setText(transcribed_text)