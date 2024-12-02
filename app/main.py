from fastapi import FastAPI
from app.routes.students import *

app = FastAPI(title="CRUD REST API  USING FASTAPI,UVICORN")

app.include_router(router, prefix="/students", tags=["Students"])


