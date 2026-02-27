from fastapi import FastAPI
from main import get_tier_experience

app = FastAPI()

@app.get("/tier/{tier_name}")
def tier_info(tier_name: str):
    return get_tier_experience(tier_name)
