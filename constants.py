from collections import defaultdict

SUPPORTED_LANGUAGES = ("en", "es")
DEFAULT_LANGUAGE = "en"

SUPPORTED_THEMES = ("light", "dark")
DEFAULT_THEME = "dark"

LANGUAGE_TABLE = {
    "es": {"es": "español",     "en": "inglés",     "and": "y",     "page_not_available": "Esta página no está disponible en español. Solo está disponible en "},
    "en": {"es": "Spanish",     "en": "English",    "and": "and",   "page_not_available": "This page is not available in English. <br> It's only available in "}
}
