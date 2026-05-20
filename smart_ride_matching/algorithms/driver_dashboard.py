"""
algorithms/driver_dashboard.py
-------------------------------
Functions for the driver dashboard: fetching pending requests and
accepting / rejecting rides.
"""

import pandas as pd
import os

BOOKING_FILE = "data/bookings.csv"


def get_pending_requests(driver_id):
    """
    Return a DataFrame of bookings assigned to *driver_id* with status 'Pending'.
    Returns an empty DataFrame if no bookings file exists or no pending rides.
    """
    if not os.path.exists(BOOKING_FILE):
        return pd.DataFrame()

    try:
        df = pd.read_csv(BOOKING_FILE)
    except Exception:
        return pd.DataFrame()

    if df.empty:
        return pd.DataFrame()

    pending = df[
        (df["driver_id"] == driver_id) &
        (df["status"] == "Pending")
    ]

    return pending.reset_index(drop=True)


def accept_ride(booking_id):
    """Set the booking status to 'Confirmed'."""
    _update_status(booking_id, "Confirmed")


def reject_ride(booking_id):
    """Set the booking status to 'Rejected'."""
    _update_status(booking_id, "Rejected")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _update_status(booking_id, new_status):
    if not os.path.exists(BOOKING_FILE):
        return

    try:
        df = pd.read_csv(BOOKING_FILE)
        df.loc[df["booking_id"] == booking_id, "status"] = new_status
        df.to_csv(BOOKING_FILE, index=False)
    except Exception:
        pass
