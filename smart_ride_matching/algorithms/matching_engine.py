import pandas as pd
import sys
import os

# Ensure algorithms package is importable regardless of working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dijkstra import shortest_path_distance  # noqa: E402

# Re-export so callers can do: from algorithms.matching_engine import shortest_path_distance
__all__ = ["find_top_drivers", "shortest_path_distance"]


def compute_safety_score(driver):
    """Compute a composite safety score (lower = better match)."""
    distance = driver["_distance"]
    rating = driver.get("safety_rating", 4.0)
    verified = 1 if driver.get("verification_status", "") == "verified" else 0

    # Normalize rating to 0-1 (rating is 3.5-5.0 range)
    rating_factor = (rating - 3.0) / 2.0  # maps 3.0->0, 5.0->1.0

    # Lower composite = better driver
    verification_boost = 1.15 if verified else 1.0
    safety_boost = 0.7 + (0.3 * rating_factor)  # 0.7 to 1.0

    adjusted_distance = distance / (verification_boost * safety_boost)
    return adjusted_distance


def find_top_drivers(pickup, drivers_df, top_n=5):
    """Return top-N drivers sorted by safety-weighted score."""
    candidates = []

    for _, driver in drivers_df.iterrows():

        if driver["status"] != "available":
            continue

        driver_loc = (
            int(driver["x"]),
            int(driver["y"])
        )

        try:
            dist, path = shortest_path_distance(driver_loc, pickup)
        except Exception:
            dist = abs(driver_loc[0] - pickup[0]) + abs(driver_loc[1] - pickup[1])
            path = []

        candidates.append({
            "driver_id": driver["driver_id"],
            "name": driver["name"],
            "x": driver_loc[0],
            "y": driver_loc[1],
            "dist": dist,
            "path": path,
            "_distance": dist,
            "safety_rating": driver["safety_rating"],
            "verification_status": driver["verification_status"]
        })

    candidates.sort(
        key=lambda x: (
            -x["safety_rating"],
            x["dist"]
        )
    )

    return candidates[:top_n]