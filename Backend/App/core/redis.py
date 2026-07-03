import redis.asyncio as redis
from core.config import REDIS_URL
try:
  redis_client = redis.from_url(REDIS_URL,decode_responses=True)
  redis_client.ping()
  print("Redis client initialized successfully.")
except Exception as e:
  print(f"Error initializing Redis client: {e}")
  redis_client = None
