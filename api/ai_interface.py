import requests
import os
import json

class AIInterface:
    def __init__(self, api_key, language="en"):
        self.api_key = api_key
        self.language = language
        self.debug = os.getenv('DEBUG_AI_INTERFACE', 'false').lower() == 'true'

    def get_response(self, card_content, additional_info, chat_history):
        system_prompt = {
            "en": "Respond as if you are having a face-to-face chat with the user. Keep your responses concise and to the point.",
            "fr": "Répondez comme si vous discutiez en face à face avec l'utilisateur. Gardez vos réponses concises et précises."
        }.get(self.language, "en")
        full_message = f"Card Content: {card_content}\nAdditional Info: {additional_info}\nChat History:\n{chat_history}\nSystem Prompt: {system_prompt}"
        if self.debug:
            print(f"Sending to AI: {full_message}")
        try:
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{"text": full_message}]
                    }]
                },
                proxies={"http": "socks5h://localhost:10808", "https": "socks5h://localhost:10808"}
            )
            response.raise_for_status()
            response_json = response.json()
            if self.debug:
                print("Response:", response_json)
            return response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error occurred: {http_err} - Response: {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"

    def get_purposes(self):
        return {
            "en": [
                "Understanding and Explanation: Ensure the user comprehends the meaning or intent of the content on the card.",
                "Context and Practical Usage: Help the user understand how the content fits into real-world situations.",
                "Connection and Personalization: Help the user build a personal or memorable association with the content."
            ],
            "fr": [
                "Compréhension et Explication : Assurez-vous que l'utilisateur comprend le sens ou l'intention du contenu de la carte.",
                "Contexte et Utilisation Pratique : Aidez l'utilisateur à comprendre comment le contenu s'intègre dans des situations réelles.",
                "Connexion et Personnalisation : Aidez l'utilisateur à établir une association personnelle ou mémorable avec le contenu."
            ]
        }.get(self.language, "en")

    def get_all_questions(self, card_content, additional_info):
        purposes = self.get_purposes()
        num_questions = len(purposes)
        system_prompt = {
            "en": f"Generate {num_questions} questions that help the user understand and remember the content. The user has seen this card before but is not currently viewing it.",
            "fr": f"Générez {num_questions} questions qui aident l'utilisateur à comprendre et à se souvenir du contenu. L'utilisateur a déjà vu cette carte mais ne la regarde pas actuellement."
        }.get(self.language, "en")
        full_message = f"Card Content: {card_content}\nAdditional Info: {additional_info}\nPurposes: {purposes}\nSystem Prompt: {system_prompt}"
        if self.debug:
            print(f"Sending to AI: {full_message}")
        try:
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-002:generateContent?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{"text": full_message}]
                    }],
                    "generationConfig": {
                        "response_mime_type": "application/json",
                        "response_schema": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "question": {"type": "STRING"}
                                }
                            }
                        }
                    }
                },
                proxies={"http": "socks5h://localhost:10808", "https": "socks5h://localhost:10808"}
            )
            response.raise_for_status()
            response_json = response.json()
            if self.debug:
                print("Response:", response_json)
            return [item.get("question", "").strip() for item in json.loads(response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", ""))]
        except requests.exceptions.HTTPError as http_err:
            return [f"HTTP error occurred: {http_err} - Response: {response.text}"]
        except Exception as e:
            return [f"Error: {str(e)}"]