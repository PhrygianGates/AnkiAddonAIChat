
class LanguageSettings:
    LANGUAGE = "en"  # Default language is English

    @staticmethod
    def set_language(language):
        if language in ["en", "fr"]:
            LanguageSettings.LANGUAGE = language

    @staticmethod
    def get_language():
        return LanguageSettings.LANGUAGE