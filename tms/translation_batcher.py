from django.utils.functional import lazy
from .dynamodb import DynamoDB


class TranslationBatcher:
    def __init__(self):
        self.to_translate = set()
        self.dynamodb = DynamoDB()

    def add(self, text):
        self.to_translate.add(text)
        return lazy(self.get_translation, str)(text)

    def get_translation(self, text):
        if not hasattr(self, "translations"):
            self.load_translations()
        return self.translations.get(text, text)

    def load_translations(self):
        if not self.to_translate:
            return
        self.translations = self.dynamodb.translate_all(self.to_translate)
        self.to_translate.clear()


translation_batcher = TranslationBatcher()


def lazy_translate(text):
    return translation_batcher.add(text)
