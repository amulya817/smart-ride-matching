import pandas as pd
import os

SOS_FILE = "data/sos_alerts.csv"


def send_emergency_alert(phone_number, booking_id, driver_id):
    print(f"Emergency alert sent to {phone_number}")
    print(f"Booking ID: {booking_id}")
    print(f"Driver ID: {driver_id}")


def trigger_sos(booking_id, driver_id, phone_number):
    """Save an SOS record and send an emergency alert."""
    sos_data = {
        "booking_id": booking_id,
        "driver_id": driver_id,
        "emergency_contact": phone_number,
        "status": "SOS Triggered"
    }

    if os.path.exists(SOS_FILE):
        df = pd.read_csv(SOS_FILE)
        df = pd.concat([df, pd.DataFrame([sos_data])], ignore_index=True)
    else:
        df = pd.DataFrame([sos_data])

    df.to_csv(SOS_FILE, index=False)

    send_emergency_alert(phone_number, booking_id, driver_id)

    return sos_data


# Alias so pages can import either name
def emergency_sos(booking_id, driver_id, emergency_contact):
    """Alias for trigger_sos; matches the name used in pages."""
    return trigger_sos(booking_id, driver_id, emergency_contact)