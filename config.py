class Config:
    API_KEY = "input your gemini api key here"
    LANGUAGE = "fr"  # Default language is French

    @staticmethod
    def set_language(language):
        if language in ["en", "fr"]:
            Config.LANGUAGE = language

    @staticmethod
    def get_language():
        return Config.LANGUAGE

    @staticmethod
    def load_from_file(file_path):
        import json
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                Config.API_KEY = data.get("API_KEY", Config.API_KEY)
                Config.set_language(data.get("LANGUAGE", Config.LANGUAGE))
        except FileNotFoundError:
            pass

    @staticmethod
    def save_to_file(file_path):
        import json
        data = {
            "API_KEY": Config.API_KEY,
            "LANGUAGE": Config.get_language()
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

Config.load_from_file("config.json")


