import streamlit as st
import os

from algorithms.sos_manager import emergency_sos
from algorithms.booking_manager import update_booking_status
from algorithms.ai_engine import analyze_threat_level

st.set_page_config(
    page_title="Emergency SOS",
    layout="wide"
)

st.title("🚨 AI Emergency Escalation System")

# ---------------------------------------------------------------------------
# Session State Defaults
# ---------------------------------------------------------------------------
if "current_booking" not in st.session_state:
    st.session_state.current_booking = None

if "ride_status" not in st.session_state:
    st.session_state.ride_status = "Not Booked"

if "emergency_contact" not in st.session_state:
    st.session_state.emergency_contact = None

# ---------------------------------------------------------------------------
# Emergency Contact Setup
# ---------------------------------------------------------------------------
st.markdown("### 📞 Emergency Safety Contact")

emergency_contact = st.text_input(
    "Enter Emergency Contact Number:",
    placeholder="+919448784632"
)

if emergency_contact:
    st.session_state.emergency_contact = emergency_contact

# SOS Panel
st.markdown(
    '<div class="sos-panel">'
    '<h4>🚨 Emergency SOS</h4>'
    '<p style="font-size:0.82rem;color:#d4d4d4;margin-bottom:0.7rem;">Tap in case of emergency. Alerts authorities and emergency contacts.</p>'
    '<div class="sos-btn">SOS ALERT</div>'
    '</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# STEP 11 - SOS EMERGENCY CONTROLS
# ---------------------------------------------------------------------------
st.markdown("### 🚨 AI Threat Level Analysis")
if st.session_state.current_booking:
    ai_analysis = analyze_threat_level(st.session_state.current_booking, st.session_state.emergency_contact)
    st.markdown(
        f'<div class="ai-insight-panel" style="margin-bottom: 1.5rem;">'
        f'<div class="ai-insight-header" style="background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(220,38,38,0.1)); border-color: rgba(239,68,68,0.3);">'
        f'<span>🚨</span><span style="color:#ef4444;">Live Threat Assessment</span></div>'
        f'<div class="ai-insight-body">'
        f'<div style="display:flex; justify-content:space-between; margin-bottom:10px;">'
        f'<strong>Predicted Threat Level:</strong> <span style="color:#ef4444; font-weight:bold;">{ai_analysis["threat_level"]}</span>'
        f'</div>'
        f'<div style="display:flex; justify-content:space-between; margin-bottom:10px;">'
        f'<strong>AI Confidence:</strong> <span>{ai_analysis["confidence"]}%</span>'
        f'</div>'
        f'<div><strong>System Recommendation:</strong> {ai_analysis["recommendation"]}</div>'
        f'</div></div>',
        unsafe_allow_html=True
    )
st.markdown("### 🚨 Emergency Safety Controls")

sos_col1, sos_col2 = st.columns(2)

with sos_col1:
    if st.button(
        "🚨 Trigger SOS Alert",
        use_container_width=True
    ):

        if (
            st.session_state.current_booking and
            st.session_state.get("emergency_contact")
        ):

            booking = st.session_state.current_booking

            emergency_sos(
                booking["booking_id"],
                booking["driver_id"],
                st.session_state.emergency_contact
            )

            st.session_state.ride_status = "Emergency"

            st.error("🚨 SOS ALERT ACTIVATED!")
            st.warning("Emergency contact notified.")
            st.warning("Live ride details shared.")
            st.warning("Authorities alert simulated.")

        else:
            st.warning(
                "Please set an emergency contact and have an active booking first."
            )

with sos_col2:
    if st.button(
        "❌ Cancel Ride",
        use_container_width=True
    ):

        if st.session_state.current_booking:

            booking = st.session_state.current_booking

            update_booking_status(
                booking["booking_id"],
                "Cancelled"
            )

            st.session_state.ride_status = "Cancelled"

            st.warning(
                "Ride cancelled successfully."
            )
        else:
            st.info("No active booking to cancel.")