import random
from typing import List, Optional
from .ad_models import AdCampaign, UserTier


def eligible_campaigns(
    campaigns: List[AdCampaign],
    viewer_id: str,
    user_tier: UserTier
) -> List[AdCampaign]:
    """
    Filters campaigns based on:
    - active status
    - monthly impression cap
    - daily cap
    - viewer frequency cap
    - user tier (Premier sees fewer ads)
    """

    eligible = []

    for c in campaigns:
        if not c.active:
            continue

        # Monthly cap
        if c.impressions_served >= c.max_impressions:
            continue

        # Daily cap
        if c.today_impressions >= c.daily_cap:
            continue

        # Frequency cap per viewer
        freq = c.viewer_frequency_map.get(viewer_id, 0)
        if freq >= c.frequency_cap_per_hour:
            continue

        # Tier-based filtering
        if user_tier == UserTier.PREMIER:
            # Premier users see fewer ads, so only show higher-tier sponsors
            if c.rotation_weight < 3:
                continue

        elif user_tier == UserTier.PREMIUM:
            # Premium users see reduced ads, filter out lowest tier
            if c.rotation_weight < 2:
                continue

        # Prime sees everything

        eligible.append(c)

    return eligible


def weighted_choice(campaigns: List[AdCampaign]) -> Optional[AdCampaign]:
    """
    Selects a campaign using rotation weights.
    """
    if not campaigns:
        return None

    weights = [c.rotation_weight for c in campaigns]
    return random.choices(campaigns, weights=weights, k=1)[0]


def select_ad(
    campaigns: List[AdCampaign],
    viewer_id: str,
    user_tier: UserTier
) -> Optional[AdCampaign]:
    """
    Main entry point:
    - filters eligible campaigns
    - selects one using weighted rotation
    - updates impression counters
    """

    eligible = eligible_campaigns(campaigns, viewer_id, user_tier)

    if not eligible:
        return None

    chosen = weighted_choice(eligible)

    # Update counters
    chosen.impressions_served += 1
    chosen.today_impressions += 1
    chosen.viewer_frequency_map[viewer_id] = (
        chosen.viewer_frequency_map.get(viewer_id, 0) + 1
    )

    return chosen
