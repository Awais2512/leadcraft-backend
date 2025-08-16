# import jwt
# from fastapi import Depends, HTTPException, Header
# from app.core.config import settings

# def verify_jwt(authorization: str = Header(...)):
#     try:
#         scheme, token = authorization.split()
#         if scheme.lower() != "bearer":
#             raise ValueError("Invalid auth scheme")
#         payload = jwt.decode(token, settings.supabase_jwt_secret, algorithms=["HS256"])
#         return payload
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")


import httpx
import jwt
from fastapi import Header, HTTPException

JWKS_URL = "https://wbzhkrtlnlpbmyeurkjh.supabase.co/auth/v1/.well-known/jwks.json"


def get_jwks():
    """Fetch JWKS from Supabase's well-known URL (public, no API key needed)."""
    resp = httpx.get(JWKS_URL)
    resp.raise_for_status()
    return resp.json()


import jwt
from fastapi import Header, HTTPException
from app.core.config import settings

def verify_jwt(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid auth scheme")

        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,   # from .env (legacy HS256 secret)
            algorithms=["HS256"],
            audience="authenticated"
        )
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"JWT verification failed: {str(e)}")

if __name__ == "__main__":
    # quick test
    print(get_jwks())
