import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Profile",
    layout="wide"
)

st.title("👤 My SafeHer Profile")

username = st.session_state.get(
    "username",
    "Guest User"
)

emergency_contact = st.session_state.get(
    "emergency_contact",
    "Not Set"
)

st.subheader(f"Welcome, {username}")

p1, p2 = st.columns(2)

with p1:
    st.write(f"**Username:** {username}")
    st.write(f"**Emergency Contact:** {emergency_contact}")

with p2:
    st.write("**Account Type:** Rider")
    st.write("**Platform:** SafeHer Ride")

# ------------------------------------------------------------
# Booking Summary
# ------------------------------------------------------------
st.markdown("### 📜 Ride Statistics")

try:
    bookings = pd.read_csv("data/bookings.csv")

    total_rides = len(bookings)
    completed = len(
        bookings[
            bookings["status"] == "Completed"
        ]
    )

    cancelled = len(
        bookings[
            bookings["status"] == "Cancelled"
        ]
    )

    total_spend = bookings["fare"].sum()

except:
    total_rides = 0
    completed = 0
    cancelled = 0
    total_spend = 0

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Rides", total_rides)
m2.metric("Completed", completed)
m3.metric("Cancelled", cancelled)
m4.metric("Total Spend", f"₹{total_spend}")

# ------------------------------------------------------------
# Emergency Contact Update
# ------------------------------------------------------------
st.markdown("### 📞 Update Emergency Contact")

new_contact = st.text_input(
    "New Emergency Contact"
)

if st.button("Update Contact"):

    if new_contact:
        st.session_state.emergency_contact = new_contact
        st.success("Emergency contact updated.")

# ------------------------------------------------------------
# Logout
# ------------------------------------------------------------
if st.button("🚪 Logout"):

    st.session_state.authenticated = False
    st.session_state.username = None

    st.success("Logged out successfully.")
    st.rerun()