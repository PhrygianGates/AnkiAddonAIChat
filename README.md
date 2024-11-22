# AI Chat with Card

This Anki add-on enables chatting with an AI around each card word. It integrates with Anki to provide an interactive chat interface for better understanding and memorization of card content.

## Features
- Adds a button to each Anki card to start a chat session.
- Provides a chat window for interaction with the AI.
- Supports multiple languages (English and French).
- Configurable API key and language settings.

## Installation
1. Anki Addon ID: 1442059032

## Configuration
1. Open Anki and go to `Tools > AI Chat > Configure`.
2. Enter your gemini API key and select your preferred language.
3. Click `Save` to apply the settings.

## Usage
1. Open a card in Anki.
2. Click the `AI Chat` button in the card reviewer interface.
3. A chat window will appear, allowing you to interact with the AI about the card content.

## Project Structure
```
anki-addon-ai-chat/
├── __init__.py
├── manifest.json
├── main.py
├── gui/
│   ├── chat_window.py
│   └── __init__.py
│   └── config_window.py
├── api/
│   ├── ai_interface.py
│   └── __init__.py
├── resources/
│   ├── styles.css
│   └── icons/
│       └── chat_icon.png
├── utils/
│   ├── helpers.py
│   └── __init__.py
├── config.py
└── README.md
```

## Contributing
Feel free to submit issues or pull requests if you have any improvements or bug fixes.

## License
This project is licensed under the MIT License.
