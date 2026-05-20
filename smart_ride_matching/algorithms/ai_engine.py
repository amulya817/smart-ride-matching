from genai.route_explainer import explain_route, generate_decision_insight

def get_match_confidence(best_driver, candidates, pickup, destination, available_drivers, total_drivers, api_key=None):
    """Alias for generate_decision_insight to match AI Engine branding."""
    return generate_decision_insight(
        best_driver,
        candidates,
        pickup,
        destination,
        available_drivers,
        total_drivers,
        api_key=api_key
    )

def generate_safety_report(driver_id, driver_name, driver_loc, pickup, destination, pickup_path, trip_path, pickup_dist, trip_dist, safety_rating=None, verification_status=None, api_key=None):
    """Alias for explain_route to match AI Engine branding."""
    return explain_route(
        driver_id,
        driver_name,
        driver_loc,
        pickup,
        destination,
        pickup_path,
        trip_path,
        pickup_dist,
        trip_dist,
        safety_rating=safety_rating,
        verification_status=verification_status,
        api_key=api_key
    )

def analyze_threat_level(booking, emergency_contact):
    """Analyzes the threat level and simulates escalation for the SOS system."""
    # Simplified AI simulation for frontend visibility
    threat_level = "CRITICAL" if booking.get("safety_rating", 5) < 4.0 else "HIGH"
    recommendation = "Dispatching nearest patrol unit based on AI trajectory prediction."
    return {
        "threat_level": threat_level,
        "recommendation": recommendation,
        "confidence": 94,
        "action": "Authorities alerted automatically"
    }

def get_booking_intelligence(driver_id):
    """Generate mock AI intelligence metrics for the driver dashboard."""
    return {
        "demand_forecast": "High demand in your zone for the next 2 hours.",
        "safety_score_impact": "+0.2 expected if next ride is completed smoothly.",
        "optimal_positioning": "Move 2 blocks North for better AI match rates."
    }
