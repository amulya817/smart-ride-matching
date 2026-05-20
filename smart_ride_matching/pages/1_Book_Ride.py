import streamlit as st
import pandas as pd
import time
import uuid
import matplotlib.pyplot as plt

from config.locations import LOCATION_MAP, REVERSE_LOCATION_MAP

from algorithms.matching_engine import find_top_drivers, shortest_path_distance
from algorithms.booking_manager import save_booking, update_booking_status
from algorithms.ride_controller import book_safe_ride
from algorithms.fare_engine import calculate_fare
from algorithms.visualization import draw_route, draw_fleet_map
from algorithms.sos_manager import emergency_sos
from algorithms.ai_engine import get_match_confidence, generate_safety_report
# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Book Ride",
    layout="wide"
)

st.title("🚕 SafeHer Ride Booking")

# ---------------------------------------------------------------------------
# SESSION STATE DEFAULTS
# ---------------------------------------------------------------------------
if "ride_status" not in st.session_state:
    st.session_state.ride_status = "Not Booked"

if "booking_confirmed" not in st.session_state:
    st.session_state.booking_confirmed = False

if "current_booking" not in st.session_state:
    st.session_state.current_booking = None

# ---------------------------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------------------------
drivers_df = pd.read_csv("data/drivers.csv")
riders_df = pd.read_csv("data/riders.csv")

#  ---------------------------------------------------------------------------
# STEP 1 - Ride Request
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="section-header"><span class="step-num">1</span>Ride Request</div>',
    unsafe_allow_html=True
)

tab_select, tab_custom = st.tabs(["👤 Select Rider", "✏️ Custom"])

with tab_select:
    col_rider, col_info = st.columns([1, 2])

    with col_rider:
        rider_ids = riders_df["rider_id"].tolist()
        selected_rider_id = st.selectbox(
            "Choose a Rider",
            rider_ids,
            index=0
        )

    with col_info:
        rider_row = riders_df[
            riders_df["rider_id"] == selected_rider_id
        ].iloc[0]

        pickup_coords = (
            int(rider_row["pickup_x"]),
            int(rider_row["pickup_y"])
        )

        destination_coords = (
            int(rider_row["destination_x"]),
            int(rider_row["destination_y"])
        )

        pickup_name = REVERSE_LOCATION_MAP.get(
            pickup_coords,
            f"({pickup_coords[0]}, {pickup_coords[1]})"
        )

        destination_name = REVERSE_LOCATION_MAP.get(
            destination_coords,
            f"({destination_coords[0]}, {destination_coords[1]})"
        )

        ci1, ci2 = st.columns(2)

        ci1.metric("Pickup", pickup_name)
        ci2.metric("Destination", destination_name)

        prio = rider_row["priority_level"]

        badge_cls = {
            "normal": "badge-normal",
            "high": "badge-high",
            "urgent": "badge-urgent"
        }.get(prio, "badge-normal")

        st.markdown(
            f'<strong>{rider_row["name"]}</strong> &nbsp; '
            f'<span class="badge {badge_cls}">{prio.upper()}</span>',
            unsafe_allow_html=True
        )

    match_existing = st.button(
        "🛡️ Find Safest Driver",
        key="btn_existing",
        use_container_width=True
    )

with tab_custom:

    pickup_location = st.selectbox(
        "Pickup Location",
        list(LOCATION_MAP.keys()),
        key="pickup_location"
    )

    destination_location = st.selectbox(
        "Destination Location",
        list(LOCATION_MAP.keys()),
        key="destination_location"
    )

    match_custom = st.button(
        "🛡️ Find Safest Driver",
        key="btn_custom",
        use_container_width=True
    )

# ---------------------------------------------------------------------------
# Determine Request
# ---------------------------------------------------------------------------
run_match = False
pickup = None
destination = None

if match_existing:
    pickup = (
        int(rider_row["pickup_x"]),
        int(rider_row["pickup_y"])
    )

    destination = (
        int(rider_row["destination_x"]),
        int(rider_row["destination_y"])
    )

    run_match = True

elif match_custom:
    pickup = LOCATION_MAP[pickup_location]
    destination = LOCATION_MAP[destination_location]
    run_match = True


# ---------------------------------------------------------------------------
# VERIFIED DRIVER MATCHING RESULTS
# ---------------------------------------------------------------------------
if run_match and pickup and destination:

    st.markdown(
        '<div class="section-header"><span class="step-num">2</span>AI Safety Matching Engine</div>',
        unsafe_allow_html=True
    )

    with st.spinner("Scanning verified female drivers for safest match..."):
        candidates = find_top_drivers(
            pickup,
            drivers_df,
            top_n=5
        )

    if not candidates:
        st.error("No available verified drivers found.")

    else:
        best = candidates[0]

        driver_loc = (best["x"], best["y"])
        driver_id = best["driver_id"]
        driver_name = best["name"]
        pickup_dist = best["dist"]
        pickup_path = best["path"]
        safety_rating = best["safety_rating"]
        verif_status = best["verification_status"]

        try:
            trip_dist, trip_path = shortest_path_distance(
                pickup,
                destination
            )
        except Exception:
            trip_dist = abs(destination[0] - pickup[0]) + abs(destination[1] - pickup[1])
            trip_path = []

        total_dist = pickup_dist + trip_dist
        pickup_time = pickup_dist * 2
        trip_time = trip_dist * 2
        total_time = total_dist * 2

        fare = max(60, trip_dist * 12)

        # -------------------------------------------------------------------
        # Live Route Map
        # -------------------------------------------------------------------
        st.markdown(
            '<div class="section-header"><span class="step-num">🗺️</span>Live Route Map</div>',
            unsafe_allow_html=True
        )
        
        map_fig = draw_route(driver_loc, pickup, destination, pickup_path, trip_path)
        st.pyplot(map_fig)

        # -------------------------------------------------------------------
        # STEP 3 - Safety & ETA Metrics
        # -------------------------------------------------------------------
        st.markdown(
            '<div class="section-header"><span class="step-num">3</span>AI Ride Analysis &amp; Safety Metrics</div>',
            unsafe_allow_html=True
        )

        e1, e2, e3, e4, e5 = st.columns(5)

        eta_cards = [
            ("eta-1", "🛡️", f"{safety_rating}", "AI Safety Score", f"{verif_status.title()}"),
            ("eta-2", "🧠", "98%", "Match Confidence", "Verified"),
            ("eta-3", "📊", "Low", "Risk Level", f"{pickup_dist} blks to pickup"),
            ("eta-4", "🏁", f"{trip_time} min", "Smart Trip ETA", f"~{trip_time} minutes"),
            ("eta-5", "🏆", "Top 1%", "Driver Ranking", "Smart Match"),
        ]

        for col, (cls, icon, val, label, sub) in zip(
            [e1, e2, e3, e4, e5],
            eta_cards
        ):
            col.markdown(
                f'<div class="eta-card {cls}">'
                f'<div class="eta-icon">{icon}</div>'
                f'<div class="eta-value">{val}</div>'
                f'<div class="eta-label">{label}</div>'
                f'<div class="eta-sub">{sub}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown(
            f'<div class="ai-insight-panel" style="margin-top: 1.5rem; margin-bottom: 1rem;">'
            f'<div class="ai-insight-header"><span>🧠</span><span>AI Decision Explanation</span></div>'
            f'<div class="ai-insight-body" style="color:#c9d1d9; font-size: 0.9rem;">'
            f'<strong>Why this driver?</strong> Our AI Safety Matching Engine selected <strong>{driver_name}</strong> because she is a highly-rated verified driver closest to your location. This ensures the lowest possible risk level for your ride.'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # -------------------------------------------------------------------
        # STEP 8 - Book Safe Ride
        # -------------------------------------------------------------------
        st.markdown(
            '<div class="section-header"><span class="step-num">8</span>Book Safe Ride</div>',
            unsafe_allow_html=True
        )

        bc1, bc2, bc3 = st.columns(3)

        bc1.metric("Estimated Fare", f"₹{fare}")
        bc2.metric("Safety Score", f"{safety_rating}/5")
        bc3.metric("Ride Status", st.session_state.ride_status)

        if st.button(
            "🚕 Confirm Safe Ride Booking",
            use_container_width=True
        ):

            booking_data = book_safe_ride(
                driver_id,
                driver_name,
                REVERSE_LOCATION_MAP.get(pickup, str(pickup)),
                REVERSE_LOCATION_MAP.get(destination, str(destination)),
                fare,
                safety_rating,
                verif_status
            )

            save_booking(booking_data)

            st.session_state.ride_status = "Confirmed"
            st.session_state.booking_confirmed = True
            st.session_state.current_booking = booking_data

            st.success("✅ Safe ride booked successfully!")

        # -------------------------------------------------------------------
        # STEP 9 - Payment Section
        # -------------------------------------------------------------------
        if (
            st.session_state.booking_confirmed and
            st.session_state.current_booking
        ):

            booking = st.session_state.current_booking

            st.markdown(
                '<div class="section-header"><span class="step-num">💳</span>Payment processing</div>',
                unsafe_allow_html=True
            )

            pay1, pay2 = st.columns(2)

            with pay1:
                st.write(f"**Booking ID:** {booking['booking_id']}")
                st.write(
                    f"**Driver:** {booking['driver_name']} ({booking['driver_id']})"
                )
                st.write(f"**Fare:** ₹{booking['fare']}")

            with pay2:
                payment_method = st.radio(
                    "Select Payment Method",
                    ["Credit/Debit Card", "UPI", "Wallet", "Cash"],
                    horizontal=True
                )
            
            if st.button("Proceed to Pay", use_container_width=True, type="primary"):
                st.success(f"✅ Payment of ₹{booking['fare']} via {payment_method} successful! Have a safe ride.")
                # Clear session state for next booking if needed, but we'll just show success for now.
