import streamlit as st
from algorithms.driver_registration import register_driver
st.set_page_config(
    page_title="Driver Registration",
    layout="wide"
)

st.title("🪪 SafeHer Driver Registration")
st.subheader("Join as a verified female driver")

with st.form("driver_registration_form"):

    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    password = st.text_input("Create Password", type="password")
    license_number = st.text_input("Driving License Number")
    vehicle_number = st.text_input("Vehicle Registration Number")
    vehicle_type = st.selectbox(
        "Vehicle Type",
        ["Scooter", "Car", "Auto", "Bike"]
    )

    submitted = st.form_submit_button(
        "🚘 Register as Driver"
    )

    if submitted:

        if not all([
            name,
            phone,
            password,
            license_number,
            vehicle_number
        ]):
            st.error("Please fill all required details.")

        else:
            driver = register_driver(
                name,
                phone,
                password,
                license_number,
                vehicle_number,
                vehicle_type
            )

            st.success(
                f"Driver registered successfully! Your Driver ID is {driver['driver_id']}"
            )

            st.info(
                "Verification pending until admin approval."
            )