import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Booking History",
    layout="wide"
)

st.title("📜 SafeHer Booking History")

# ---------------------------------------------------------------------------
# Booking History
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="section-header"><span class="step-num">📜</span>Booking History</div>',
    unsafe_allow_html=True
)

booking_file = "data/bookings.csv"

if os.path.exists(booking_file):

    bookings_df = pd.read_csv(booking_file)

    if not bookings_df.empty:

        bookings_display = bookings_df.copy()

        st.dataframe(
            bookings_display,
            use_container_width=True,
            hide_index=True
        )

        total_bookings = len(bookings_df)
        avg_fare = round(bookings_df["fare"].mean(), 2)

        bh1, bh2 = st.columns(2)

        bh1.metric("Total Bookings", total_bookings)
        bh2.metric("Average Fare", f"₹{avg_fare}")

    else:
        st.info("No bookings available yet.")

else:
    st.info("No booking history found yet.")