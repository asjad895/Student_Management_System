from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from json import JSONDecodeError

class JSONValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.method in ("POST", "PUT", "PATCH"):
            try:
                await request.json()
            except JSONDecodeError:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Malformed JSON in request body"},
                )
        return await call_next(request)
