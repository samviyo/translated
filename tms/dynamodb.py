import redis
from django.conf import settings

class DynamoDB:
  def __init__(self):
      self.redis_client = redis.StrictRedis(
          host=settings.REDIS_HOST,
          port=settings.REDIS_PORT,
          db=settings.REDIS_DB,
          decode_responses=True
      )

  def translate_all(self, texts):
      translations = {text: self.translate(f"translation:{text}", text) for text in texts}
      return translations

  def translate(self, key, text):
      translation = self.redis_client.get(key)

      if not translation:
          translated_text = f"Translated: {text}"
          self.redis_client.set(key, translated_text)
          return text
      else:
          return translation