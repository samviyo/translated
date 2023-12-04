import threading
from functools import wraps

thread_local = threading.local()


def translated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thread_local.translated = True
        try:
            return func(*args, **kwargs)
        finally:
            thread_local.translated = False

    return wrapper


def use_translated():
    if hasattr(thread_local, "translated"):
        return thread_local.translated

    return False
