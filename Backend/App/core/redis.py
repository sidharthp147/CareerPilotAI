from time import time

import redis.asyncio as redis
from core.config import REDIS_URL
MAX_RETRIES=5
RETRY_DELAY=20
for attempt in range(MAX_RETRIES):
  try:
    redis_client = redis.from_url(REDIS_URL,decode_responses=True)
    break
  except Exception as e:
    if attempt==MAX_RETRIES-1:
      raise e
    time.sleep(RETRY_DELAY)