"""
algorithms/driver_auth.py
--------------------------
Driver authentication — login against the driver_accounts CSV.
Falls back to the main drivers CSV if driver_accounts does not yet exist
(so the app works even before any driver has registered via the UI).
"""

import pandas as pd
import os

DRIVER_ACCOUNTS_FILE = "data/driver_accounts.csv"
DRIVER_FALLBACK_FILE = "data/drivers.csv"


def driver_login(phone, password):
    """
    Authenticate a driver by phone + password.

    Returns
    -------
    (True, driver_dict)  on success
    (False, error_str)   on failure
    """
    phone = str(phone).strip()
    password = str(password).strip()

    if not phone or not password:
        return False, "Phone and password are required."

    # Try registered accounts first
    for filepath in (DRIVER_ACCOUNTS_FILE, DRIVER_FALLBACK_FILE):
        if not os.path.exists(filepath):
            continue

        try:
            df = pd.read_csv(filepath)
        except Exception:
            continue

        if "phone" not in df.columns:
            continue

        match = df[df["phone"].astype(str).str.strip() == phone]

        if match.empty:
            continue

        row = match.iloc[0]

        # If the CSV has a password column check it; otherwise allow any password
        # (demo mode: drivers.csv has no passwords)
        if "password" in df.columns:
            if str(row["password"]).strip() != password:
                return False, "Invalid phone or password."
        # else: demo mode — skip password check

        return True, row.to_dict()

    return False, "Driver not found. Please register first."
