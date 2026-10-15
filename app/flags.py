"""Environment-based feature flags.

Flags are read once from `DEPOT_FLAG_<NAME>` (upper case, 1/true/yes = on).
Add a flag by adding an entry to ALL_FLAGS; ship code behind `is_enabled`.
"""

import os

# All known flags. Any env var not listed here is ignored.
ALL_FLAGS: frozenset[str] = frozenset(
    {
        "webhooks",
    }
)

_TRUTHY = {"1", "true", "yes", "on"}


def is_enabled(flag: str) -> bool:
    """Return True if DEPOT_FLAG_<FLAG> is set to a truthy value."""
    if flag not in ALL_FLAGS:
        raise ValueError(f"unknown feature flag: {flag} (known: {sorted(ALL_FLAGS)})")
    return os.getenv(f"DEPOT_FLAG_{flag.upper()}", "").lower() in _TRUTHY
