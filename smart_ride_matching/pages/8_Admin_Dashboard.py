import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ Admin Dashboard")
st.markdown("Monitor platform metrics and manage users.")

# Load Data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    drivers = pd.read_csv(os.path.join(base, "data", "drivers.csv"))
    riders = pd.read_csv(os.path.join(base, "data", "riders.csv"))
    bookings = pd.read_csv(os.path.join(base, "data", "bookings.csv"))
    return drivers, riders, bookings

drivers_df, riders_df, bookings_df = load_data()

# Summary Metrics
total_drivers = len(drivers_df)
verified_drivers = len(drivers_df[drivers_df["verification_status"] == "verified"])
pending_drivers = total_drivers - verified_drivers
total_riders = len(riders_df)
total_bookings = len(bookings_df)

st.markdown(
    '<div class="section-header"><span class="step-num">1</span>Platform Overview</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Drivers", total_drivers)
m2.metric("Verified Drivers", verified_drivers)
m3.metric("Pending Verification", pending_drivers)
m4.metric("Total Riders", total_riders)
m5.metric("Total Bookings", total_bookings)

st.markdown("---")

st.markdown(
    '<div class="section-header"><span class="step-num">2</span>Driver Management</div>',
    unsafe_allow_html=True
)

st.dataframe(drivers_df, use_container_width=True)

st.markdown("---")

st.markdown(
    '<div class="section-header"><span class="step-num">3</span>Rider Directory</div>',
    unsafe_allow_html=True
)

st.dataframe(riders_df, use_container_width=True)

st.markdown("---")

st.markdown(
    '<div class="section-header"><span class="step-num">4</span>Recent Bookings</div>',
    unsafe_allow_html=True
)

st.dataframe(bookings_df, use_container_width=True)
