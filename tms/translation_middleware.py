from .translation_batcher import translation_batcher

class TranslationBatcherMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        translation_batcher.load_translations()

        return response
