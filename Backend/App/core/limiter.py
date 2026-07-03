from slowapi.util import get_remote_address
from slowapi import Limiter
from fastapi import Request
from core.config import REDIS_URL
def user_or_ip(request:Request):
    user = getattr(request.state, "user_id", None)
    if user :
        return f"ratelimit:user:{user}"
    else:
        return f"ratelimit:ip:{get_remote_address(request)}"
limiter = Limiter(key_func=user_or_ip,storage_uri=REDIS_URL)
