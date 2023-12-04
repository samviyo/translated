from .translation_batcher import TranslationBatcher


class TranslationBatcherMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        translation_batcher = TranslationBatcher()
        request.translation_batcher = translation_batcher
        response = self.get_response(request)

        translation_batcher.load_translations()

        return response
