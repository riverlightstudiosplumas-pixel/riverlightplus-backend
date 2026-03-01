from datetime import datetime
from typing import List
from .ad_models import AdCampaign
from .ad_pacing import reset_daily, reset_monthly


def run_daily_reset(campaigns: List[AdCampaign]) -> None:
    """
    Wrapper for daily reset logic.
    Clears:
    - today_impressions
    - viewer frequency maps
    """
    reset_daily(campaigns)
    print(f"[AdSystem] Daily reset completed at {datetime.now()}")


def run_monthly_reset(campaigns: List[AdCampaign]) -> None:
    """
    Wrapper for monthly reset logic.
    Clears:
    - impressions_served
    - reactivates campaigns
    """
    reset_monthly(campaigns)
    print(f"[AdSystem] Monthly reset completed at {datetime.now()}")
