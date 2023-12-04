import threading
from functools import wraps

thread_local = threading.local()


def translated(owner):
    def translated_decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            thread_local.translated = True
            thread_local.translation_batcher = request.translation_batcher
            thread_local.owner = owner
            try:
                return func(request, *args, **kwargs)
            finally:
                thread_local.translated = False

        return wrapper

    return translated_decorator


def use_translated():
    if hasattr(thread_local, "translated"):
        return thread_local.translated

    return False


def lazy_translate(text):
    if (
        not use_translated()
        or not hasattr(thread_local, "translation_batcher")
        or not hasattr(thread_local, "owner")
        or not thread_local.translation_batcher
    ):
        return text

    return thread_local.translation_batcher.add(text, thread_local.owner)
