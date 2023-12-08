from celery import shared_task
import redis
import requests
import json

from django.conf import settings

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


@shared_task
def add(x, y):
    return x + y


@shared_task
def translate(key, text):
    url = "http://0.0.0.0:6000/translate"
    payload = {
        "q": text,
        "source": "en",
        "target": "fr",
        "format": "text",
    }

    response = requests.post(url, json=payload)
    json = response.json()
    redis_client.set(key, json.get("translatedText", text))
