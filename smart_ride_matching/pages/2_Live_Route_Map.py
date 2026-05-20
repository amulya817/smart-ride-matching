import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

from config.locations import REVERSE_LOCATION_MAP

from algorithms.matching_engine import shortest_path_distance
from algorithms.visualization import (
    draw_route,
    draw_fleet_map,
    build_path_timeline_html
)

from algorithms.ai_engine import (
    get_match_confidence,
    generate_safety_report
)

from algorithms.ride_controller import (
    start_safe_ride,
    complete_safe_ride,
    cancel_safe_ride
)

# -------------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Live Route Map",
    layout="wide"
)

st.title("🗺️ SafeHer Live Route Tracking")

# -------------------------------------------------------------------
# SESSION STATE LOAD
# -------------------------------------------------------------------
booking = st.session_state.get(
    "current_booking",
    None
)

run_match = booking is not None

if booking:

    pickup = booking["pickup"]
    destination = booking["destination"]

    driver_id = booking["driver_id"]
    driver_name = booking["driver_name"]

    safety_rating = booking.get(
        "safety_rating",
        5.0
    )

    verif_status = booking.get(
        "verification_status",
        "verified"
    )

else:

    pickup = None
    destination = None
    driver_id = None
    driver_name = None
    safety_rating = None
    verif_status = None

# -------------------------------------------------------------------
# DATA LOAD
# -------------------------------------------------------------------
drivers_df = pd.read_csv(
    "data/drivers.csv"
)

riders_df = pd.read_csv(
    "data/riders.csv"
)

available_drivers = len(
    drivers_df[
        drivers_df["status"] == "available"
    ]
)

total_drivers = len(
    drivers_df
)

api_key = None

# -------------------------------------------------------------------
# DRIVER LOOKUP
# -------------------------------------------------------------------
driver_loc = None
pickup_dist = 0
pickup_path = []
trip_dist = 0
trip_path = []
candidates = []
best = None

if booking and driver_id:

    matched_driver = drivers_df[
        drivers_df["driver_id"] == driver_id
    ]

    if not matched_driver.empty:

        driver_row = matched_driver.iloc[0]

        driver_loc = (
            int(driver_row["x"]),
            int(driver_row["y"])
        )

        best = {
            "driver_id": driver_id,
            "name": driver_name,
            "x": driver_loc[0],
            "y": driver_loc[1],
            "safety_rating": safety_rating,
            "verification_status": verif_status,
            "dist": 0,
            "path": []
        }

        candidates = [best]

        try:
            pickup_dist, pickup_path = shortest_path_distance(
                driver_loc,
                pickup
            )

        except:
            pickup_dist = (
                abs(driver_loc[0] - pickup[0]) +
                abs(driver_loc[1] - pickup[1])
            )

            pickup_path = []

        try:
            trip_dist, trip_path = shortest_path_distance(
                pickup,
                destination
            )

        except:
            trip_dist = (
                abs(destination[0] - pickup[0]) +
                abs(destination[1] - pickup[1])
            )

            trip_path = []

if run_match and pickup and destination:

    # -------------------------------------------------------------------
    # STEP 4 - Secure Route Visualization
    # -------------------------------------------------------------------
    st.markdown(
        '<div class="section-header"><span class="step-num">4</span>Secure Route Visualization</div>',
        unsafe_allow_html=True
    )

    col_map, col_timeline = st.columns([3, 2])

    with col_map:
        fig = draw_route(
            driver_loc,
            pickup,
            destination,
            pickup_path,
            trip_path
        )
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with col_timeline:
        st.markdown(
            '<div class="glass-container"><h4 style="color:#c084fc;margin:0 0 0.5rem 0;font-size:0.92rem;">🗺️ Route Waypoints</h4>',
            unsafe_allow_html=True
        )

        st.markdown(
            build_path_timeline_html(
                pickup_path,
                trip_path,
                driver_loc,
                pickup,
                destination
            ),
            unsafe_allow_html=True
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        with st.expander("Pickup path"):
            if pickup_path:
                st.code(
                    " -> ".join(
                        f"({p[0]},{p[1]})"
                        for p in pickup_path
                    ),
                    language=None
                )
            else:
                st.info("No path data.")

        with st.expander("Trip path"):
            if trip_path:
                st.code(
                    " -> ".join(
                        f"({p[0]},{p[1]})"
                        for p in trip_path
                    ),
                    language=None
                )
            else:
                st.info("No path data.")

    # -------------------------------------------------------------------
    # STEP 5 - Fleet Overview
    # -------------------------------------------------------------------
    st.markdown(
        '<div class="section-header"><span class="step-num">5</span>Fleet Overview</div>',
        unsafe_allow_html=True
    )

    fig2 = draw_fleet_map(
        drivers_df,
        pickup,
        destination,
        matched_id=driver_id
    )

    st.pyplot(fig2, use_container_width=True)
    plt.close(fig2)

    # -------------------------------------------------------------------
    # STEP 6 - AI Safety Insight
    # -------------------------------------------------------------------
    st.markdown(
        '<div class="section-header"><span class="step-num">6</span>AI Route Intelligence</div>',
        unsafe_allow_html=True
    )

    with st.spinner("Analyzing safety factors..."):
        insight = get_match_confidence(
            best,
            candidates,
            pickup,
            destination,
            available_drivers,
            total_drivers,
            api_key=api_key
        )
        time.sleep(0.2)

    col_insight, col_cands = st.columns([3, 2])

    with col_insight:
        if isinstance(insight, dict):
            factors_html = "".join(
                f'<div class="ai-factor"><div class="ai-factor-dot"></div><div>{f}</div></div>'
                for f in insight["factors"]
            )

            conf = insight["confidence"]
            conf_label = insight["confidence_label"]

        else:
            factors_html = (
                f'<div style="color:#c9d1d9;line-height:1.7;font-size:0.9rem;">'
                f'{insight}'
                f'</div>'
            )

            conf = 85
            conf_label = "High"

        st.markdown(
            f'<div class="ai-insight-panel">'
            f'<div class="ai-insight-header"><span>🧠</span><span>AI Match Intelligence</span></div>'
            f'<div class="ai-insight-body">{factors_html}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    with col_cands:
        st.markdown(
            f'<div style="text-align:center;margin-bottom:1rem;">'
            f'<div style="font-size:0.78rem;color:#8b949e;margin-bottom:0.5rem;text-transform:uppercase;letter-spacing:1px;font-weight:600;">Safety Confidence</div>'
            f'<div class="confidence-ring" style="--pct:{conf}%;">'
            f'<div class="confidence-inner">'
            f'<div class="confidence-val">{conf}%</div>'
            f'<div class="confidence-lbl">{conf_label}</div>'
            f'</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div style="font-size:0.78rem;color:#8b949e;text-transform:uppercase;letter-spacing:1px;font-weight:600;margin-bottom:0.4rem;">Top Candidates</div>',
            unsafe_allow_html=True
        )

        for idx, c in enumerate(candidates[:3]):
            winner = " cand-winner" if idx == 0 else ""

            st.markdown(
                f'<div class="cand-card{winner}">'
                f'<span class="cand-rank">{idx+1}</span>'
                f'<div class="cand-info">'
                f'<div class="cand-id">{c["driver_id"]} - {c["name"]}</div>'
                f'<div class="cand-loc">⭐ {c["safety_rating"]}/5 • ({c["x"]},{c["y"]})</div>'
                f'</div>'
                f'<div class="cand-dist">{c["dist"]} blk</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # -------------------------------------------------------------------
    # STEP 7 - AI Route Safety Report
    # -------------------------------------------------------------------
    st.markdown(
        '<div class="section-header"><span class="step-num">7</span>AI Route Safety Report</div>',
        unsafe_allow_html=True
    )

    with st.spinner("Generating safety report..."):
        explanation = generate_safety_report(
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
            verification_status=verif_status,
            api_key=api_key
        )
        time.sleep(0.2)

    st.markdown(
        f'<div class="route-explanation-panel">'
        f'<div class="re-header"><span>🤖</span><span>SafeHer Route Safety Report</span></div>'
        f'<div class="re-body">{explanation}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # -------------------------------------------------------------------
    # STEP 10 - Ride Lifecycle
    # -------------------------------------------------------------------
    st.markdown("### 🚦 Ride Lifecycle")

    ride_stage = st.selectbox(
        "Ride Progress",
        [
            "Confirmed",
            "Driver Arriving",
            "Ride Started",
            "Ride Completed"
        ]
    )

    st.session_state.ride_status = ride_stage

    st.info(
        f"Current Ride Status: {st.session_state.ride_status}"
    )

    # -------------------------------------------------------------------
    # STEP 12 - Live Ride Controls
    # -------------------------------------------------------------------
    st.markdown("### 🚘 Live Ride Controls")

    op1, op2 = st.columns(2)

    with op1:

        if st.button(
            "🚦 Start Ride",
            use_container_width=True
        ):

            if st.session_state.current_booking:

                booking = st.session_state.current_booking

                start_safe_ride(
                    booking["booking_id"]
                )

                st.session_state.ride_status = "Ride Started"

                st.success(
                    "Ride started successfully!"
                )

        if st.button(
            "🏁 Complete Ride",
            use_container_width=True
        ):

            if st.session_state.current_booking:

                booking = st.session_state.current_booking

                complete_safe_ride(
                    booking["booking_id"],
                    booking["driver_id"]
                )

                st.session_state.ride_status = "Completed"

                st.success(
                    "Ride completed successfully!"
                )

    with op2:

        if st.button(
            "❌ Cancel Ride",
            use_container_width=True
        ):

            if st.session_state.current_booking:

                booking = st.session_state.current_booking

                cancel_safe_ride(
                    booking["booking_id"],
                    booking["driver_id"]
                )

                st.session_state.ride_status = "Cancelled"

                st.warning(
                    "Ride cancelled successfully."
                )


# ---------------------------------------------------------------------------
# Fleet & Rider Tables
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="section-header"><span class="step-num">📋</span>Fleet &amp; Rider Data</div>',
    unsafe_allow_html=True
)

tab_avail, tab_all, tab_riders = st.tabs(
    [
        "Available Drivers",
        "All Drivers",
        "Rider Requests"
    ]
)

with tab_avail:

    avail_df = drivers_df[
        drivers_df["status"] == "available"
    ][
        [
            "driver_id",
            "name",
            "x",
            "y",
            "verification_status",
            "safety_rating"
        ]
    ].copy()

    avail_df.columns = [
        "ID",
        "Name",
        "X",
        "Y",
        "Verification",
        "Safety"
    ]

    st.dataframe(
        avail_df,
        use_container_width=True,
        hide_index=True
    )

with tab_all:

    all_df = drivers_df[
        [
            "driver_id",
            "name",
            "x",
            "y",
            "status",
            "verification_status",
            "safety_rating"
        ]
    ].copy()

    all_df.columns = [
        "ID",
        "Name",
        "X",
        "Y",
        "Status",
        "Verification",
        "Safety"
    ]

    st.dataframe(
        all_df,
        use_container_width=True,
        hide_index=True
    )

with tab_riders:

    riders_display = riders_df.copy()

    riders_display["Pickup"] = riders_display.apply(
        lambda row: REVERSE_LOCATION_MAP.get(
            (
                int(row["pickup_x"]),
                int(row["pickup_y"])
            ),
            f"({row['pickup_x']},{row['pickup_y']})"
        ),
        axis=1
    )

    riders_display["Destination"] = riders_display.apply(
        lambda row: REVERSE_LOCATION_MAP.get(
            (
                int(row["destination_x"]),
                int(row["destination_y"])
            ),
            f"({row['destination_x']},{row['destination_y']})"
        ),
        axis=1
    )

    riders_display = riders_display[
        [
            "rider_id",
            "name",
            "Pickup",
            "Destination",
            "priority_level"
        ]
    ]

    riders_display.columns = [
        "ID",
        "Name",
        "Pickup",
        "Destination",
        "Priority"
    ]

    st.dataframe(
        riders_display,
        use_container_width=True,
        hide_index=True
    )