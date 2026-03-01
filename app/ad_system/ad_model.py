from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


class UserTier(str, Enum):
    PRIME = "prime"        # Free tier, full ads
    PREMIUM = "premium"    # $8.99, reduced ads
    PREMIER = "premier"    # $12.99, minimal ads


@dataclass
class AdPackageConfig:
    name: str
    monthly_price: int
    max_impressions: int
    daily_cap: int
    rotation_weight: int
    frequency_cap_per_hour: int


AD_PACKAGES: Dict[str, AdPackageConfig] = {
    "starter": AdPackageConfig(
        name="starter",
        monthly_price=150,
        max_impressions=20_000,
        daily_cap=800,
        rotation_weight=1,
        frequency_cap_per_hour=2,
    ),
    "community": AdPackageConfig(
        name="community",
        monthly_price=250,
        max_impressions=40_000,
        daily_cap=1_500,
        rotation_weight=2,
        frequency_cap_per_hour=3,
    ),
    "premium": AdPackageConfig(
        name="premium",
        monthly_price=500,
        max_impressions=80_000,
        daily_cap=3_000,
        rotation_weight=3,
        frequency_cap_per_hour=4,
    ),
    "gold": AdPackageConfig(
        name="gold",
        monthly_price=1_000,
        max_impressions=150_000,
        daily_cap=5_000,
        rotation_weight=4,
        frequency_cap_per_hour=5,
    ),
}


@dataclass
class AdCampaign:
    id: str
    sponsor_name: str
    package_key: str  # "starter", "community", etc.
    active: bool = True

    impressions_served: int = 0
    today_impressions: int = 0
    viewer_frequency_map: Dict[str, int] = field(default_factory=dict)

    def config(self) -> AdPackageConfig:
        return AD_PACKAGES[self.package_key]

    @property
    def max_impressions(self) -> int:
        return self.config().max_impressions

    @property
    def daily_cap(self) -> int:
        return self.config().daily_cap

    @property
    def rotation_weight(self) -> int:
        return self.config().rotation_weight

    @property
    def frequency_cap_per_hour(self) -> int:
        return self.config().frequency_cap_per_hour

