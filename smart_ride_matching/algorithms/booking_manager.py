import pandas as pd
import os

BOOKING_FILE = "data/bookings.csv"


def save_booking(booking_data):
    if os.path.exists(BOOKING_FILE):
        df = pd.read_csv(BOOKING_FILE)
        df = pd.concat([df, pd.DataFrame([booking_data])], ignore_index=True)
    else:
        df = pd.DataFrame([booking_data])

    df.to_csv(BOOKING_FILE, index=False)


def update_booking_status(booking_id, new_status):
    if os.path.exists(BOOKING_FILE):
        df = pd.read_csv(BOOKING_FILE)

        df.loc[df["booking_id"] == booking_id, "status"] = new_status

        df.to_csv(BOOKING_FILE, index=False)


def get_booking_history():
    if os.path.exists(BOOKING_FILE):
        return pd.read_csv(BOOKING_FILE)

    return pd.DataFrame()