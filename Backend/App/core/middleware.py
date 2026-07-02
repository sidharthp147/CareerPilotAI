from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError,jwt
import redis
from slowapi.errors import RateLimitExceeded 
from core.redis import redis_client as redis
import time
import logging
import os
from core.config import SECRET_KEY,ALGORITHM

logger = logging.getLogger("api")

async def block_middleware(request:Request,call_next):
  if request.method=="OPTIONS":
    return await call_next(request)
  SECRET=SECRET_KEY
  ALGORITHM=ALGORITHM
  token=request.headers.get("Authorization")
  print("token")
  user_id=None
  if token and token.startswith("Bearer "):
    token=token.split(" ")[1]
    try:
        payload=jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        user_id=payload.get("sub")
        request.state.user_id=user_id
    except JWTError:
        print("error")
        pass
    if user_id:
      print("user_id",user_id)
      user_key=f"blocked:user:{user_id}"
      if await redis.get(user_key):
        print("inisde")
        remaining_seconds=await redis.ttl(user_key)
        response= JSONResponse(status_code=403,content={"detail":"You are Blocked","remaining_seconds":int(remaining_seconds)})
        response.headers["Access-Control-Allow-Origin"]="http://localhost:5173"
        response.headers["Access-Control-Allow-Credentials"]="true"
        return response
  client_ip=request.client.host
  print("ip",client_ip)
  ip_key=f"blocked:ip:{client_ip}"
  if await redis.get(ip_key):
    print("await")
    remaining_seconds=await redis.ttl(ip_key)
    print("remaining_seconds",remaining_seconds)
    response= JSONResponse(status_code=403,content={"detail":"You are Blocked","remaining_seconds":int(remaining_seconds)})
    response.headers["Access-Control-Allow-Origin"]="http://localhost:5173"
    response.headers["Access-Control-Allow-Credentials"]="true"
    print("response",response)
    return response  
  print("222222222")
  return await call_next(request)
async def logging_middleware(request:Request,call_next):
    start_time=time.time()
    response=await call_next(request)
    process_time=(time.time()-start_time)*1000
    logger.info("request_log",extra={"method":request.method,
                                     "url":request.url.path,
                                     "status_code":response.status_code,
                                     "process_time":process_time})
    print("res2",response)
    return response