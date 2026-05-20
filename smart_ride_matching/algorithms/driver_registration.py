import pandas as pd
import os
import uuid

DRIVER_ACCOUNTS_FILE = "data/driver_accounts.csv"


def register_driver(
    name,
    phone,
    password,
    license_number,
    vehicle_number,
    vehicle_type
):

    driver_data = {
        "driver_id": f"W{str(uuid.uuid4())[:6]}",
        "name": name,
        "phone": phone,
        "password": password,
        "license_number": license_number,
        "vehicle_number": vehicle_number,
        "vehicle_type": vehicle_type,
        "verification_status": "pending",
        "safety_rating": 5.0,
        "status": "available",
        "x": 2,
        "y": 3
    }

    if os.path.exists(DRIVER_ACCOUNTS_FILE):
        df = pd.read_csv(DRIVER_ACCOUNTS_FILE)
        df = pd.concat([df, pd.DataFrame([driver_data])], ignore_index=True)
    else:
        df = pd.DataFrame([driver_data])

    df.to_csv(DRIVER_ACCOUNTS_FILE, index=False)

    return driver_data