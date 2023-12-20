from django.utils.translation import gettext as _, activate
from django.utils.functional import lazy
from .dynamodb import DynamoDB


class TranslationBatcher:
    def __init__(self):
        activate("fr")
        self.to_translate = set()
        self.translations = {}
        self.dynamodb = DynamoDB()

    def add(self, text, owner):
        self.to_translate.add(text)
        return lazy(self.get_translation, str)(text)

    def get_translation(self, text):
        po_translation = _(text)
        print(po_translation)

        if po_translation != text:
            return po_translation

        if not self.translations.get(text):
            self.load_translations()

        return self.translations.get(text, text)

    def load_translations(self):
        if not self.to_translate:
            return

        self.translations.update(self.dynamodb.translate_all(self.to_translate))
        self.to_translate.clear()
