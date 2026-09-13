"""
spec.py

Defines the structure ("spec") for a digital product before content
is generated. Each spec describes the sections a product needs and
the design principles content generation should follow.

Add new niches as new dicts in NICHE_SPECS.
"""

PLANNER_SPEC = {
    "niche": "adhd_daily_planner",
    "title": "ADHD-Friendly Daily Planner",
    "sections": [
        {"name": "brain_dump", "purpose": "unstructured space to offload thoughts before planning"},
        {"name": "top_3_priorities", "purpose": "forces focus instead of an overwhelming full task list"},
        {"name": "time_blocks", "purpose": "loose hourly blocks, not rigid — flexible scheduling"},
        {"name": "energy_check", "purpose": "track energy/focus level to match tasks to capacity"},
        {"name": "habit_tracker", "purpose": "small daily habits, visual checkboxes"},
        {"name": "reflection", "purpose": "end-of-day: what worked, what didn't"},
    ],
    "design_principles": [
        "low visual clutter",
        "generous white space",
        "clear visual hierarchy (headers, boxes)",
        "flexible, not rigid, structure",
    ],
}

NICHE_SPECS = {
    "adhd_daily_planner": PLANNER_SPEC,
}


def get_spec(niche: str) -> dict:
    """Look up a niche spec by name."""
    if niche not in NICHE_SPECS:
        raise ValueError(f"Unknown niche: {niche}. Available: {list(NICHE_SPECS)}")
    return NICHE_SPECS[niche]