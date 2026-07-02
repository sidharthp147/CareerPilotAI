
import time
from fastapi import Request
from fastapi.responses import JSONResponse
import redis
from slowapi.errors import RateLimitExceeded 
from core.redis import redis_client as redis
async def rate_limit_handler(request:Request,exp:RateLimitExceeded):
  blocked_until=int(time.time())+60
  user=getattr(request.state,"user_id",None)
  if user:
     await redis.setex(f"blocked:user:{user}",60,blocked_until)
     return JSONResponse(status_code=429,content={"detail":"Too Many Requests,You Are Blocked For 1 Hour","retry_after":60})
  client_ip=request.client.host
  await redis.setex(f"blocked:ip:{client_ip}",60,blocked_until)
  return JSONResponse(status_code=429,content={"detail":"Too Many Requests,You Are Blocked For 1 Hour","retry_after":60})
