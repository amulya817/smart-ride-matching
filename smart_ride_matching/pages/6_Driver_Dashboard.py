import streamlit as st
import pandas as pd

from algorithms.driver_auth import driver_login
from algorithms.ai_engine import get_booking_intelligence
from algorithms.driver_dashboard import (
    get_pending_requests,
    accept_ride,
    reject_ride
)

st.set_page_config(
    page_title="Driver Dashboard",
    layout="wide"
)

st.title("🚘 SafeHer Driver Dashboard")

if "driver_logged_in" not in st.session_state:
    st.session_state.driver_logged_in = False


# -------------------------------------------------------------------
# DRIVER LOGIN
# -------------------------------------------------------------------
if not st.session_state.driver_logged_in:

    st.subheader("Driver Login")

    with st.form("driver_login_form"):

        phone = st.text_input("Phone Number")

        password = st.text_input(
            "Password",
            type="password"
        )

        login_btn = st.form_submit_button(
            "Login"
        )

        if login_btn:

            success, result = driver_login(
                phone,
                password
            )

            if success:
                st.session_state.driver_logged_in = True
                st.session_state.driver_data = result
                st.success("Login successful!")
                st.rerun()

            else:
                st.error(result)


# -------------------------------------------------------------------
# DRIVER DASHBOARD
# -------------------------------------------------------------------
else:

    driver = st.session_state.driver_data

    st.success(
        f"Welcome {driver['name']}"
    )

    d1, d2, d3 = st.columns(3)

    d1.metric(
        "Driver ID",
        driver["driver_id"]
    )

    d2.metric(
        "Verification",
        driver["verification_status"]
    )

    d3.metric(
        "Safety Rating",
        driver["safety_rating"]
    )

    st.markdown("### 🚗 Vehicle Details")

    st.write(
        f"**Vehicle Type:** {driver['vehicle_type']}"
    )

    st.write(
        f"**Vehicle Number:** {driver['vehicle_number']}"
    )

    # -------------------------------------------------------------------
    # Availability Toggle
    # -------------------------------------------------------------------
    availability = st.toggle(
        "Available for Rides",
        value=(driver["status"] == "available")
    )

    if availability:
        st.success("You are live for bookings.")
    else:
        st.warning("You are offline.")

    # -------------------------------------------------------------------
    # PENDING RIDE REQUESTS
    # -------------------------------------------------------------------
    st.markdown("### 🧠 AI Booking Intelligence")
    intel = get_booking_intelligence(driver["driver_id"])
    st.markdown(
        f'<div class="ai-insight-panel" style="margin-bottom: 1.5rem;">'
        f'<div class="ai-insight-header"><span>📈</span><span>Performance & Forecast</span></div>'
        f'<div class="ai-insight-body" style="font-size:0.9rem; color:#c9d1d9;">'
        f'<div style="margin-bottom:8px;"><strong>Demand Forecast:</strong> {intel["demand_forecast"]}</div>'
        f'<div style="margin-bottom:8px;"><strong>Safety Impact:</strong> <span style="color:#10b981;">{intel["safety_score_impact"]}</span></div>'
        f'<div><strong>Optimal Positioning:</strong> {intel["optimal_positioning"]}</div>'
        f'</div></div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🧠 AI Assigned Ride Requests")

    pending_requests = get_pending_requests(
        driver["driver_id"]
    )

    if pending_requests.empty:

        st.info("No AI assigned ride requests currently. The Smart Matching Engine is actively scanning.")

    else:

        for _, ride in pending_requests.iterrows():

            st.markdown("---")

            st.write(
                f"**Booking ID:** {ride['booking_id']}"
            )

            st.write(
                f"**Pickup:** {ride['pickup']}"
            )

            st.write(
                f"**Destination:** {ride['destination']}"
            )

            st.write(
                f"**Fare:** ₹{ride['fare']}"
            )

            pr1, pr2 = st.columns(2)

            with pr1:
                if st.button(
                    f"✅ Accept {ride['booking_id']}"
                ):

                    accept_ride(
                        ride["booking_id"]
                    )

                    st.success(
                        "Ride accepted successfully!"
                    )

                    st.rerun()

            with pr2:
                if st.button(
                    f"❌ Reject {ride['booking_id']}"
                ):

                    reject_ride(
                        ride["booking_id"]
                    )

                    st.warning(
                        "Ride rejected."
                    )

                    st.rerun()

    # -------------------------------------------------------------------
    # ASSIGNED RIDES
    # -------------------------------------------------------------------
    st.markdown("### 📋 Assigned Ride History")

    try:

        bookings = pd.read_csv(
            "data/bookings.csv"
        )

        my_rides = bookings[
            bookings["driver_id"] == driver["driver_id"]
        ]

        if my_rides.empty:

            st.info(
                "No assigned rides yet."
            )

        else:

            st.dataframe(
                my_rides,
                use_container_width=True
            )

    except:
        st.info(
            "No bookings available yet."
        )

    # -------------------------------------------------------------------
    # Earnings Summary
    # -------------------------------------------------------------------
    st.markdown("### 💰 Earnings Summary")

    try:

        completed = my_rides[
            my_rides["status"] == "Completed"
        ]

        earnings = completed[
            "fare"
        ].sum()

        st.metric(
            "Total Earnings",
            f"₹{earnings}"
        )

    except:

        st.metric(
            "Total Earnings",
            "₹0"
        )

    # -------------------------------------------------------------------
    # LOGOUT
    # -------------------------------------------------------------------
    if st.button("🚪 Logout"):

        st.session_state.driver_logged_in = False
        st.session_state.driver_data = None

        st.rerun()