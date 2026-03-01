from typing import List
from .ad_models import AdCampaign
from .ad_pacing import pacing_score


def order_for_rotation(campaigns: List[AdCampaign]) -> List[AdCampaign]:
    """
    Orders campaigns using pacing score first, then rotation weight.
    Lower pacing score = higher priority.
    Higher rotation weight = higher priority.
    """

    return sorted(
        campaigns,
        key=lambda c: (pacing_score(c), -c.rotation_weight)
    )


def fallback_rotation(campaigns: List[AdCampaign]) -> List[AdCampaign]:
    """
    If pacing-based ordering results in ties or too few options,
    fall back to simple weight-based ordering.
    """

    return sorted(
        campaigns,
        key=lambda c: -c.rotation_weight
    )


def prepare_rotation_list(campaigns: List[AdCampaign]) -> List[AdCampaign]:
    """
    Main rotation preparation pipeline:
    1. Try pacing-aware ordering.
    2. If too few campaigns remain, fall back to weight-only ordering.
    """

    if len(campaigns) <= 1:
        return campaigns

    ordered = order_for_rotation(campaigns)

    # If pacing produces a weird edge case (e.g., all campaigns identical),
    # fallback ensures stable rotation.
    if len(ordered) < len(campaigns):
        return fallback_rotation(campaigns)

    return ordered
