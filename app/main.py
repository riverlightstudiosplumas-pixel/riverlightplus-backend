from fastapi import FastAPI
from app.ad_system.endpoints import router as ad_router

app = FastAPI()

app.include_router(ad_router)
