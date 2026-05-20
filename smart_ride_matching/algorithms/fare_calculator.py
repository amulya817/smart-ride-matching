def calculate_fare(distance, base_fare=50, per_unit=10, safety_fee=20):
    total_fare = base_fare + (distance * per_unit) + safety_fee
    return total_fare
