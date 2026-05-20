import uuid


def book_safe_ride(
    driver_id,
    driver_name,
    pickup,
    destination,
    fare,
    safety_rating,
    verification_status
):

    booking_data = {
        "booking_id": str(uuid.uuid4())[:8],
        "driver_id": driver_id,
        "driver_name": driver_name,
        "pickup": pickup,
        "destination": destination,
        "fare": fare,
        "safety_rating": safety_rating,
        "verification_status": verification_status,
        "status": "Pending"
    }

    return booking_data


def start_safe_ride(
    booking_id
):
    from algorithms.booking_manager import update_booking_status

    update_booking_status(
        booking_id,
        "Ride Started"
    )


def complete_safe_ride(
    booking_id,
    driver_id
):
    from algorithms.booking_manager import update_booking_status

    update_booking_status(
        booking_id,
        "Completed"
    )


def cancel_safe_ride(
    booking_id,
    driver_id
):
    from algorithms.booking_manager import update_booking_status

    update_booking_status(
        booking_id,
        "Cancelled"
    )