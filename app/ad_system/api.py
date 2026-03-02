from fastapi import FastAPI
from app.ad_system.engine import serve_ad, track_event
from app.ad_system.campaigns import create_campaign, update_campaign, list_campaigns
from app.ad_system.partners import approve_partner, reject_partner, list_partners

app = FastAPI()

# Viewer endpoints
@app.get("/ads/serve")
def serve_ads(viewer_id: str, content_id: str, tier: str):
    return serve_ad(viewer_id, content_id, tier)

@app.post("/ads/track")
def track_ads(event: dict):
    return track_event(event)

# Partner endpoints
@app.post("/ads/create")
def create_ads(campaign: dict):
    return create_campaign(campaign)

@app.post("/ads/update")
def update_ads(campaign: dict):
    return update_campaign(campaign)

@app.get("/ads/list")
def list_ads(partner_id: str):
    return list_campaigns(partner_id)

# Admin endpoints
@app.post("/partners/approve")
def approve(partner_id: str):
    return approve_partner(partner_id)

@app.post("/partners/reject")
def reject(partner_id: str):
    return reject_partner(partner_id)

@app.get("/partners/list")
def partners():
    return list_partners()
