# main.py

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional


# -----------------------------
# Tier model
# -----------------------------

@dataclass
class DownloadRules:
    enabled: bool = False
    drmProtected: bool = False
    exportable: bool = False
    expirationDays: int = 0
    extensionRules: Optional[Dict[str, int]] = None


@dataclass
class TierConfig:
    name: str
    price: float
    preRoll: Optional[str]
    midRolls: List[str]
    postRoll: Optional[str]
    bumper: Optional[str]
    monetization: str
    discoveryBanners: bool
    advertiserBanners: Any  # bool or "low_frequency"
    allowEventBanners: bool
    fullPDLibrary: bool
    fullCreatorLibrary: bool
    licensedLibraryLevel: str  # "some", "expanded", "full"
    originalsAccess: str       # "none", "standard", "full"
    premiereEvents: bool
    vaultAccess: bool
    contentRolloutTier: Optional[str]
    identityBanners: bool
    downloads: DownloadRules
    exclusive: bool


# -----------------------------
# Tier definitions
# -----------------------------

TIERS: Dict[str, TierConfig] = {
    "topaz": TierConfig(
        name="Topaz",
        price=0.00,
        preRoll="ad_preroll_standard",
        midRolls=["ad_mid_standard"],
        postRoll="ad_postroll_standard",
        bumper="programming_bumper",
        monetization="full_ads",
        discoveryBanners=True,
        advertiserBanners=True,
        allowEventBanners=True,
        fullPDLibrary=True,
        fullCreatorLibrary=True,
        licensedLibraryLevel="some",   # some licensed IP
        originalsAccess="none",
        premiereEvents=False,
        vaultAccess=False,
        contentRolloutTier=None,
        identityBanners=False,
        downloads=DownloadRules(),
        exclusive=False,
    ),
    "emerald": TierConfig(
        name="Emerald",
        price=9.99,
        preRoll="ad_preroll_standard",
        midRolls=["ad_mid_light"],     # reduced frequency
        postRoll="pd_bumper",
        bumper="sponsored_bumper",     # branded/sponsored bumpers allowed
        monetization="light_ads",
        discoveryBanners=True,
        advertiserBanners=False,       # removed from Emerald
        allowEventBanners=True,
        fullPDLibrary=True,
        fullCreatorLibrary=True,
        licensedLibraryLevel="expanded",
        originalsAccess="standard",    # Riverlight Originals available
        premiereEvents=False,
        vaultAccess=False,
        contentRolloutTier=None,
        identityBanners=False,
        downloads=DownloadRules(),
        exclusive=False,
    ),
    "sapphire": TierConfig(
        name="Sapphire",
        price=14.99,
        preRoll=None,                  # no pre-rolls
        midRolls=["ad_mid_light"],     # light mid-rolls
        postRoll="pd_bumper",          # bumper, not ads
        bumper="sponsored_bumper",
        monetization="light_ads",
        discoveryBanners=True,
        advertiserBanners=True,
        allowEventBanners=True,
        fullPDLibrary=True,
        fullCreatorLibrary=True,
        licensedLibraryLevel="full",   # full licensed IP library
        originalsAccess="full",        # full Originals
        premiereEvents=True,           # film + originals premiere events
        vaultAccess=False,
        contentRolloutTier="standard",
        identityBanners=True,          # “Thank you for choosing Sapphire…” etc.
        downloads=DownloadRules(),
        exclusive=False,
    ),
    "onyx": TierConfig(
        name="Onyx",
        price=24.99,
        preRoll=None,
        midRolls=["ad_mid_ultralight"],  # extremely light mid-rolls
        postRoll=None,
        bumper=None,
        monetization="ultralight_ads",
        discoveryBanners=False,
        advertiserBanners="low_frequency",  # premium brands only
        allowEventBanners=True,
        fullPDLibrary=True,
        fullCreatorLibrary=True,
        licensedLibraryLevel="full",
        originalsAccess="full",
        premiereEvents=True,
        vaultAccess=True,
        contentRolloutTier="onyx_timeline",  # different roll-out windows
        identityBanners=False,
        downloads=DownloadRules(
            enabled=True,
            drmProtected=True,
            exportable=False,
            expirationDays=7,
            extensionRules={
                # if not watched in first 3 days → +3 days
                "noWatchFirst3Days": 3,
                # if watched early → no extension
                "watchedEarly": 0,
                # heavy engagement → up to +3 days
                "highEngagementMax": 3,
            },
        ),
        exclusive=True,
    ),
}


# -----------------------------
# Public API
# -----------------------------

def get_tier_experience(tier_key: str) -> Dict[str, Any]:
    """
    Return the full experience configuration for a given tier key:
    "topaz", "emerald", "sapphire", or "onyx".
    """
    tier_key = tier_key.lower()
    if tier_key not in TIERS:
        raise ValueError(f"Unknown tier: {tier_key}")
    tier = TIERS[tier_key]
    data = asdict(tier)
    # Flatten downloads for convenience
    data["downloads"] = asdict(tier.downloads)
    return data


def describe_tier(tier_key: str) -> str:
    """
    Human-readable summary for debugging, admin tools, or docs.
    """
    cfg = get_tier_experience(tier_key)
    return (
        f"{cfg['name']} (${cfg['price']}/month)\n"
        f"- Monetization: {cfg['monetization']}\n"
        f"- Licensed library: {cfg['licensedLibraryLevel']}\n"
        f"- Originals access: {cfg['originalsAccess']}\n"
        f"- Premiere events: {cfg['premiereEvents']}\n"
        f"- Vault access: {cfg['vaultAccess']}\n"
        f"- Downloads: {cfg['downloads']}\n"
    )


if __name__ == "__main__":
    # Example: print all tiers for quick inspection
    for key in TIERS:
        print(describe_tier(key))
        print("-" * 40)
