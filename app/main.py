from fastapi import FastAPI
from app.routes.students import *

from app.middleware.requestvalidation import JSONValidationMiddleware

app = FastAPI(title="CRUD REST API  USING FASTAPI,UVICORN")
app.add_middleware(JSONValidationMiddleware)
app.include_router(router, prefix="/students", tags=["Students"])


