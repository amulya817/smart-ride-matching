"""
system_controller.py
--------------------
Thin façade that re-exports the canonical ride lifecycle functions from
ride_controller and sos_manager so that app.py can import them from one place.
"""

from algorithms.ride_controller import (
    book_safe_ride,
    start_safe_ride,
    complete_safe_ride,
    cancel_safe_ride,
)

from algorithms.sos_manager import emergency_sos  # noqa: F401

__all__ = [
    "book_safe_ride",
    "start_safe_ride",
    "complete_safe_ride",
    "cancel_safe_ride",
    "emergency_sos",
]