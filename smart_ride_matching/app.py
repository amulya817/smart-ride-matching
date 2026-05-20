import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
from algorithms.fare_engine import calculate_fare
from algorithms.booking_manager import save_booking
import uuid
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from algorithms.system_controller import (
    book_safe_ride,
    start_safe_ride,
    complete_safe_ride,
    cancel_safe_ride,
    emergency_sos
)
from algorithms.dijkstra import shortest_path_distance, create_city_graph
from genai.route_explainer import explain_route, generate_decision_insight
from auth import login, signup


# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SafeHer Ride - Women's Safe Mobility",
    page_icon="\U0001F6E1\uFE0F",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS  -  SafeHer Ride theme (purple / rose / teal)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
/* ===== GLOBAL ===== */
.block-container { padding-top: 1rem; padding-bottom: 1rem; }
[data-testid="stAppViewContainer"] { background: #0a0a14; }

/* ===== AUTH PAGE ===== */
.auth-wrapper {
    max-width: 440px; margin: 6vh auto; padding: 2.5rem;
    background: linear-gradient(160deg, rgba(20,10,30,0.95), rgba(30,15,45,0.92));
    border: 1px solid rgba(168,85,247,0.25);
    border-radius: 22px; box-shadow: 0 8px 60px rgba(168,85,247,0.1);
}
.auth-logo { text-align: center; margin-bottom: 1.5rem; }
.auth-logo .logo-icon { font-size: 3rem; }
.auth-logo h2 { color: #c084fc; margin: 0.5rem 0 0 0; font-size: 1.6rem; font-weight: 800; }
.auth-logo p { color: #a78bfa; font-size: 0.85rem; opacity: 0.7; margin-top: 0.3rem; }

/* ===== HERO BANNER ===== */
.hero-banner {
    background: linear-gradient(135deg, #1a0a2e 0%, #2d1b4e 35%, #4a1942 70%, #1a0a2e 100%);
    background-size: 200% 200%;
    animation: gradientShift 8s ease infinite;
    padding: 2.2rem 2.8rem; border-radius: 18px; margin-bottom: 1.8rem;
    color: #fff; position: relative; overflow: hidden;
    border: 1px solid rgba(168,85,247,0.2);
}
@keyframes gradientShift {
    0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}
}
.hero-banner::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(circle at 80% 20%, rgba(236,72,153,0.1) 0%, transparent 50%);
    pointer-events: none;
}
.hero-banner h1 { font-size: 2.2rem; font-weight: 800; margin: 0; position: relative; }
.hero-banner p  { font-size: 1rem; opacity: 0.8; margin: 0.5rem 0 0 0; position: relative; }
.hero-badge {
    display: inline-block; background: rgba(168,85,247,0.2); border: 1px solid rgba(168,85,247,0.35);
    border-radius: 20px; padding: 4px 14px; font-size: 0.76rem; color: #c084fc; font-weight: 600;
    margin-top: 0.8rem; position: relative; letter-spacing: 0.5px;
}

/* ===== SECTION HEADERS ===== */
.section-header {
    display: flex; align-items: center; gap: 10px;
    font-size: 1.2rem; font-weight: 700; color: #e6edf3;
    margin: 2rem 0 1.2rem 0; padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(168,85,247,0.2);
}
.section-header .step-num {
    background: linear-gradient(135deg, #a855f7, #ec4899);
    color: #fff; font-size: 0.76rem; font-weight: 800;
    width: 26px; height: 26px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0;
}

/* ===== TOP METRIC CARDS ===== */
.top-metric {
    background: linear-gradient(145deg, rgba(25,15,40,0.95), rgba(15,10,25,0.95));
    border: 1px solid rgba(168,85,247,0.2); border-radius: 14px;
    padding: 1.2rem 1.3rem; text-align: center; position: relative; overflow: hidden;
}
.top-metric::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 14px 14px 0 0; }
.top-metric.tm-purple::before { background: linear-gradient(90deg, #a855f7, #c084fc); }
.top-metric.tm-green::before  { background: linear-gradient(90deg, #059669, #10b981); }
.top-metric.tm-rose::before   { background: linear-gradient(90deg, #db2777, #ec4899); }
.top-metric.tm-amber::before  { background: linear-gradient(90deg, #d97706, #f59e0b); }
.top-metric .tm-icon { font-size: 1.4rem; margin-bottom: 0.3rem; }
.top-metric .tm-value { font-size: 2rem; font-weight: 800; line-height: 1.1; }
.top-metric.tm-purple .tm-value { color: #c084fc; }
.top-metric.tm-green .tm-value  { color: #10b981; }
.top-metric.tm-rose .tm-value   { color: #ec4899; }
.top-metric.tm-amber .tm-value  { color: #f59e0b; }
.top-metric .tm-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #8b949e; margin-top: 0.35rem; font-weight: 600; }

/* ===== DRIVER RESULT CARD ===== */
.driver-result-card {
    background: linear-gradient(160deg, rgba(25,10,45,0.95), rgba(40,20,60,0.95));
    border: 1px solid rgba(168,85,247,0.3); border-radius: 18px; padding: 0; overflow: hidden;
    box-shadow: 0 4px 40px rgba(168,85,247,0.08);
}
.drc-header {
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    padding: 1.1rem 1.5rem; display: flex; align-items: center; gap: 14px;
}
.drc-avatar {
    width: 52px; height: 52px; border-radius: 50%;
    background: rgba(255,255,255,0.15); display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; color: #fff; border: 2px solid rgba(255,255,255,0.3); flex-shrink: 0;
}
.drc-header-text .drc-id { font-size: 1.3rem; font-weight: 800; color: #fff; }
.drc-header-text .drc-subtitle { font-size: 0.8rem; color: rgba(255,255,255,0.7); margin-top: 2px; }
.drc-body { padding: 1.3rem 1.5rem; }
.drc-stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 0.8rem; }
.drc-stat {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(168,85,247,0.15);
    border-radius: 10px; padding: 0.7rem 0.8rem; text-align: center;
}
.drc-stat-value { font-size: 1.2rem; font-weight: 700; color: #e6edf3; }
.drc-stat-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.7px; color: #8b949e; margin-top: 2px; }
.drc-score-bar { background: rgba(255,255,255,0.05); border-radius: 8px; height: 8px; overflow: hidden; margin-top: 0.7rem; }
.drc-score-fill { height: 100%; border-radius: 8px; background: linear-gradient(90deg, #a855f7, #10b981); }

/* ===== BADGES ===== */
.badge { padding: 4px 12px; border-radius: 20px; font-size: 0.74rem; font-weight: 700; letter-spacing: 0.3px; display: inline-block; }
.badge-verified  { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.35); }
.badge-pending   { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.35); }
.badge-available { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.35); }
.badge-busy      { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid rgba(239,68,68,0.35); }
.badge-normal    { background: rgba(168,85,247,0.1); color: #c084fc; border: 1px solid rgba(168,85,247,0.25); }
.badge-high      { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
.badge-urgent    { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }

/* ===== SAFETY STARS ===== */
.safety-stars { color: #f59e0b; letter-spacing: 2px; font-size: 1.1rem; }

/* ===== ETA METRIC CARDS ===== */
.eta-card {
    background: rgba(25,15,40,0.8); border: 1px solid rgba(168,85,247,0.15);
    border-radius: 14px; padding: 1.1rem; text-align: center; position: relative; overflow: hidden;
}
.eta-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
.eta-card.eta-1::before { background: #a855f7; }
.eta-card.eta-2::before { background: #10b981; }
.eta-card.eta-3::before { background: #ec4899; }
.eta-card.eta-4::before { background: #f59e0b; }
.eta-card.eta-5::before { background: #ef4444; }
.eta-icon  { font-size: 1.5rem; margin-bottom: 0.3rem; }
.eta-value { font-size: 1.7rem; font-weight: 800; color: #e6edf3; line-height: 1.1; }
.eta-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; color: #8b949e; margin-top: 0.3rem; font-weight: 600; }
.eta-sub   { font-size: 0.78rem; color: #c084fc; margin-top: 0.35rem; font-weight: 600; }

/* ===== RIDE DETAIL CARD ===== */
.ride-detail-card {
    background: rgba(15,10,25,0.8); border: 1px solid rgba(168,85,247,0.15);
    border-radius: 14px; padding: 1.2rem 1.4rem; margin-top: 1rem;
}
.ride-detail-card h4 { color: #c084fc; margin: 0 0 0.8rem 0; font-size: 0.95rem; }
.rd-row { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid rgba(168,85,247,0.08); }
.rd-row:last-child { border-bottom: none; }
.rd-label { color: #8b949e; font-size: 0.85rem; }
.rd-value { color: #e6edf3; font-weight: 700; font-size: 0.9rem; }

/* ===== AI INSIGHT PANEL ===== */
.ai-insight-panel {
    background: linear-gradient(160deg, rgba(15,10,25,0.9), rgba(30,15,50,0.9));
    border: 1px solid rgba(168,85,247,0.25); border-radius: 18px; padding: 0; overflow: hidden;
    box-shadow: 0 4px 40px rgba(168,85,247,0.06);
}
.ai-insight-header {
    background: linear-gradient(135deg, rgba(168,85,247,0.15), rgba(236,72,153,0.08));
    padding: 1rem 1.5rem; display: flex; align-items: center; gap: 10px;
    border-bottom: 1px solid rgba(168,85,247,0.15);
}
.ai-insight-header span:first-child { font-size: 1.2rem; }
.ai-insight-header span:last-child  { font-size: 1rem; font-weight: 700; color: #c084fc; }
.ai-insight-body { padding: 1.3rem 1.5rem; }
.ai-factor { display: flex; align-items: flex-start; gap: 10px; padding: 0.55rem 0; border-bottom: 1px solid rgba(168,85,247,0.08); font-size: 0.88rem; color: #c9d1d9; line-height: 1.55; }
.ai-factor:last-child { border-bottom: none; }
.ai-factor-dot { width: 8px; height: 8px; border-radius: 50%; background: #c084fc; flex-shrink: 0; margin-top: 7px; }

/* ===== CONFIDENCE RING ===== */
.confidence-ring { width: 80px; height: 80px; border-radius: 50%; background: conic-gradient(#a855f7 var(--pct), rgba(168,85,247,0.15) 0); display: flex; align-items: center; justify-content: center; margin: 0 auto; }
.confidence-inner { width: 62px; height: 62px; border-radius: 50%; background: #0a0a14; display: flex; align-items: center; justify-content: center; flex-direction: column; }
.confidence-val { font-size: 1.15rem; font-weight: 800; color: #c084fc; line-height: 1; }
.confidence-lbl { font-size: 0.58rem; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; }

/* ===== CANDIDATE CARDS ===== */
.cand-card { background: rgba(25,15,40,0.7); border: 1px solid rgba(168,85,247,0.15); border-radius: 10px; padding: 0.7rem 1rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center; }
.cand-card.cand-winner { border-color: rgba(16,185,129,0.4); background: rgba(16,185,129,0.06); }
.cand-rank { font-size: 0.73rem; font-weight: 800; color: #8b949e; width: 24px; height: 24px; border-radius: 50%; background: rgba(255,255,255,0.05); display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; }
.cand-card.cand-winner .cand-rank { background: rgba(16,185,129,0.15); color: #10b981; }
.cand-info { flex: 1; margin-left: 10px; }
.cand-id   { font-weight: 700; color: #e6edf3; font-size: 0.88rem; }
.cand-loc  { font-size: 0.75rem; color: #8b949e; }
.cand-dist { font-weight: 700; font-size: 0.88rem; color: #c084fc; white-space: nowrap; }

/* ===== ROUTE EXPLANATION ===== */
.route-explanation-panel { background: linear-gradient(160deg, rgba(20,10,35,0.9), rgba(35,18,55,0.9)); border: 1px solid rgba(168,85,247,0.2); border-radius: 18px; overflow: hidden; }
.re-header { background: linear-gradient(135deg, rgba(168,85,247,0.12), rgba(236,72,153,0.06)); padding: 1rem 1.5rem; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid rgba(168,85,247,0.12); }
.re-header span:first-child { font-size: 1.2rem; }
.re-header span:last-child  { font-size: 1rem; font-weight: 700; color: #c084fc; }
.re-body { padding: 1.4rem 1.6rem; color: #c9d1d9; line-height: 1.75; font-size: 0.9rem; }

/* ===== SOS PANEL ===== */
.sos-panel { background: linear-gradient(135deg, rgba(127,29,29,0.3), rgba(153,27,27,0.15)); border: 1px solid rgba(239,68,68,0.3); border-radius: 14px; padding: 1.2rem 1.5rem; text-align: center; }
.sos-panel h4 { color: #ef4444; margin: 0 0 0.5rem 0; }
.sos-btn { display: inline-block; background: linear-gradient(135deg, #dc2626, #ef4444); color: #fff; padding: 10px 28px; border-radius: 30px; font-weight: 800; font-size: 0.9rem; letter-spacing: 1px; cursor: pointer; border: none; }

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f0a1a 0%, #150f24 100%); border-right: 1px solid rgba(168,85,247,0.15); }
section[data-testid="stSidebar"] .stMarkdown h2, section[data-testid="stSidebar"] .stMarkdown h3 { color: #c084fc; }
.sidebar-stat-card { background: rgba(25,15,40,0.6); border: 1px solid rgba(168,85,247,0.12); border-radius: 10px; padding: 0.65rem 1rem; margin-bottom: 0.4rem; display: flex; justify-content: space-between; align-items: center; }
.sidebar-stat-card .ss-label { font-size: 0.83rem; color: #8b949e; }
.sidebar-stat-card .ss-value { font-size: 1.05rem; font-weight: 700; color: #e6edf3; }

/* ===== GLASS CONTAINER ===== */
.glass-container { background: rgba(15,10,25,0.7); backdrop-filter: blur(12px); border: 1px solid rgba(168,85,247,0.12); border-radius: 16px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }

/* ===== PATH TIMELINE ===== */
.path-timeline { display: flex; align-items: center; gap: 0; overflow-x: auto; padding: 0.8rem 0; margin: 0.5rem 0; }
.path-node { display: flex; flex-direction: column; align-items: center; flex-shrink: 0; }
.path-dot { width: 12px; height: 12px; border-radius: 50%; border: 2px solid; }
.path-dot.pd-driver { background: #10b981; border-color: #10b981; }
.path-dot.pd-pickup { background: #ec4899; border-color: #ec4899; }
.path-dot.pd-dest   { background: #a855f7; border-color: #a855f7; }
.path-dot.pd-mid    { background: transparent; border-color: #484f58; width: 8px; height: 8px; }
.path-coord { font-size: 0.63rem; color: #8b949e; margin-top: 4px; white-space: nowrap; }
.path-connector { width: 18px; height: 2px; flex-shrink: 0; margin-bottom: 14px; }
.path-connector.pc-pickup { background: #c084fc; }
.path-connector.pc-trip   { background: #ec4899; }

/* ===== LLM STATUS ===== */
.llm-status { display: flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 8px; font-size: 0.78rem; font-weight: 600; }
.llm-active   { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); color: #10b981; }
.llm-fallback { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.3); color: #f59e0b; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Session State Init & Auth Sync
# ---------------------------------------------------------------------------
# Check for auth token passed from React
query_params = st.query_params
if "auth_user" in query_params:
    st.session_state.authenticated = True
    st.session_state.username = query_params["auth_user"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
if "ride_status" not in st.session_state:
    st.session_state.ride_status = "Not Booked"

if "booking_confirmed" not in st.session_state:
    st.session_state.booking_confirmed = False

if "current_booking" not in st.session_state:
    st.session_state.current_booking = None
    


# ---------------------------------------------------------------------------
# AUTH PAGE
# ---------------------------------------------------------------------------
def show_auth_page():
    st.markdown(
        '<div class="auth-logo">'
        '<div class="logo-icon">\U0001F6E1\uFE0F</div>'
        '<h2>SafeHer Ride</h2>'
        '<p>AI-Powered Women\'s Safe Mobility Platform</p>'
        '</div>', unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        with st.form("login_form"):
            lu = st.text_input("Username", key="login_user")
            lp = st.text_input("Password", type="password", key="login_pass")
            submitted = st.form_submit_button("Login", use_container_width=True)
            if submitted:
                ok, msg = login(lu, lp)
                if ok:
                    st.session_state.authenticated = True
                    st.session_state.username = lu
                    st.rerun()
                else:
                    st.error(msg)

    with tab_signup:
        with st.form("signup_form"):
            su = st.text_input("Choose Username", key="signup_user")
            sp = st.text_input("Choose Password", type="password", key="signup_pass")
            sp2 = st.text_input("Confirm Password", type="password", key="signup_pass2")
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            if submitted:
                if sp != sp2:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = signup(su, sp)
                    if ok:
                        st.success(msg + " Please login.")
                    else:
                        st.error(msg)


if not st.session_state.authenticated:
    show_auth_page()
    st.stop()


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    drivers = pd.read_csv(os.path.join(base, "data", "drivers.csv"))
    riders = pd.read_csv(os.path.join(base, "data", "riders.csv"))
    return drivers, riders


drivers_df, riders_df = load_data()

total_drivers = len(drivers_df)
available_drivers = len(drivers_df[drivers_df["status"] == "available"])
busy_drivers = total_drivers - available_drivers
verified_drivers = len(drivers_df[drivers_df["verification_status"] == "verified"])
avg_safety = drivers_df["safety_rating"].mean()
total_riders = len(riders_df)
urgent_riders = len(riders_df[riders_df["priority_level"] == "urgent"])


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def compute_safety_score(distance, safety_rating, verification_status):
    """Lower = better. Distance adjusted by safety/verification."""
    rating_factor = (safety_rating - 3.0) / 2.0
    verification_boost = 1.15 if verification_status == "verified" else 1.0
    safety_boost = 0.7 + (0.3 * rating_factor)
    return distance / (verification_boost * safety_boost)


def find_top_drivers(pickup, drivers, top_n=5):
    """Return top-N drivers sorted by safety-weighted score."""
    candidates = []
    for _, driver in drivers.iterrows():
        if driver["status"] == "available":
            loc = (int(driver["x"]), int(driver["y"]))
            try:
                distance, path = shortest_path_distance(loc, pickup)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue
            score = compute_safety_score(distance, driver["safety_rating"], driver["verification_status"])
            candidates.append({
                "driver_id": driver["driver_id"],
                "name": driver["name"],
                "x": int(driver["x"]),
                "y": int(driver["y"]),
                "dist": distance,
                "score": score,
                "path": path,
                "safety_rating": driver["safety_rating"],
                "verification_status": driver["verification_status"],
                "series": driver,
            })
    candidates.sort(key=lambda c: c["score"])
    return candidates[:top_n]


def render_stars(rating):
    full = int(rating)
    half = 1 if rating - full >= 0.3 else 0
    empty = 5 - full - half
    return "\u2605" * full + ("\u00BD" if half else "") + "\u2606" * empty


def draw_route(driver_loc, pickup, destination, pickup_path, trip_path, grid_size=20):
    fig, ax = plt.subplots(figsize=(9, 9), dpi=100)
    fig.patch.set_facecolor("#0a0a14")
    ax.set_facecolor("#0a0a14")

    for i in range(grid_size):
        for j in range(grid_size):
            if (i + j) % 2 == 0:
                ax.add_patch(plt.Rectangle((i - 0.5, j - 0.5), 1, 1,
                             facecolor=(25/255, 15/255, 40/255, 0.4), edgecolor="none", zorder=0))
    for i in range(grid_size):
        ax.axhline(y=i, color="#1a1525", linewidth=0.3, zorder=1)
        ax.axvline(x=i, color="#1a1525", linewidth=0.3, zorder=1)

    if pickup_path and len(pickup_path) > 1:
        ppx = [p[0] for p in pickup_path]
        ppy = [p[1] for p in pickup_path]
        ax.plot(ppx, ppy, color="#a855f7", linewidth=8, alpha=0.1, zorder=2, solid_capstyle="round")
        ax.plot(ppx, ppy, color="#a855f7", linewidth=3, alpha=0.9, zorder=3, solid_capstyle="round")

    if trip_path and len(trip_path) > 1:
        ttx = [p[0] for p in trip_path]
        tty = [p[1] for p in trip_path]
        ax.plot(ttx, tty, color="#ec4899", linewidth=8, alpha=0.1, zorder=2, solid_capstyle="round")
        ax.plot(ttx, tty, color="#ec4899", linewidth=3, alpha=0.9, zorder=3, solid_capstyle="round")

    def _add_arrows(path, color):
        step = max(len(path) // 4, 2)
        for i in range(step, len(path), step):
            ddx = path[i][0] - path[i - 1][0]
            ddy = path[i][1] - path[i - 1][1]
            if ddx == 0 and ddy == 0:
                continue
            ax.annotate("", xy=(path[i][0], path[i][1]), xytext=(path[i-1][0], path[i-1][1]),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=13), zorder=4)

    if pickup_path and len(pickup_path) > 2:
        _add_arrows(pickup_path, "#a855f7")
    if trip_path and len(trip_path) > 2:
        _add_arrows(trip_path, "#ec4899")

    for loc, color in [(driver_loc, "#10b981"), (pickup, "#ec4899"), (destination, "#a855f7")]:
        circle = plt.Circle(loc, 1.2, facecolor=color, alpha=0.06, edgecolor=color, linewidth=0.8, linestyle="--", zorder=2)
        ax.add_patch(circle)

    mpe = [pe.withStroke(linewidth=3, foreground="#0a0a14")]
    ax.plot(*driver_loc, marker="s", color="#10b981", markersize=16, zorder=6, markeredgecolor="#fff", markeredgewidth=1.5)
    ax.annotate("DRIVER", driver_loc, textcoords="offset points", xytext=(12, 12), fontsize=8, color="#10b981", fontweight="bold", path_effects=mpe)
    ax.plot(*pickup, marker="^", color="#ec4899", markersize=16, zorder=6, markeredgecolor="#fff", markeredgewidth=1.5)
    ax.annotate("PICKUP", pickup, textcoords="offset points", xytext=(12, 12), fontsize=8, color="#ec4899", fontweight="bold", path_effects=mpe)
    ax.plot(*destination, marker="*", color="#a855f7", markersize=22, zorder=6, markeredgecolor="#fff", markeredgewidth=1.2)
    ax.annotate("DEST", destination, textcoords="offset points", xytext=(12, 12), fontsize=8, color="#a855f7", fontweight="bold", path_effects=mpe)

    legend_handles = [
        mpatches.Patch(color="#10b981", label="Driver"),
        mpatches.Patch(color="#ec4899", label="Pickup"),
        mpatches.Patch(color="#a855f7", label="Destination"),
    ]
    ax.legend(handles=legend_handles, loc="upper left", fontsize=7.5, facecolor="#150f24", edgecolor="#2d1b4e", labelcolor="#c9d1d9", framealpha=0.92)
    ax.set_xlim(-1, grid_size)
    ax.set_ylim(-1, grid_size)
    ax.set_xlabel("X", color="#484f58", fontsize=9, labelpad=8)
    ax.set_ylabel("Y", color="#484f58", fontsize=9, labelpad=8)
    ax.set_title("SafeHer - Secure Route Map", color="#c084fc", fontsize=12, fontweight="bold", pad=14)
    ax.tick_params(colors="#484f58", labelsize=7)
    for spine in ax.spines.values():
        spine.set_color("#2d1b4e")
    ax.set_aspect("equal")
    plt.tight_layout()
    return fig


def draw_fleet_map(drivers, pickup=None, destination=None, matched_id=None, grid_size=20):
    """Bird's-eye view of all drivers on the grid."""
    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
    fig.patch.set_facecolor("#0a0a14")
    ax.set_facecolor("#0a0a14")

    for i in range(grid_size):
        ax.axhline(y=i, color="#1a1525", linewidth=0.2, zorder=1)
        ax.axvline(x=i, color="#1a1525", linewidth=0.2, zorder=1)

    for _, d in drivers.iterrows():
        c = "#10b981" if d["status"] == "available" else "#ef4444"
        alpha = 0.9 if d["status"] == "available" else 0.4
        sz = 8
        if d["driver_id"] == matched_id:
            c = "#f59e0b"
            sz = 14
            alpha = 1.0
            ax.annotate(d["driver_id"], (d["x"], d["y"]), textcoords="offset points", xytext=(8, 8),
                        fontsize=7, color="#f59e0b", fontweight="bold")
        ax.plot(d["x"], d["y"], "o", color=c, markersize=sz, alpha=alpha, zorder=3,
                markeredgecolor="#fff" if d["driver_id"] == matched_id else "none",
                markeredgewidth=1 if d["driver_id"] == matched_id else 0)

    if pickup:
        ax.plot(*pickup, marker="^", color="#ec4899", markersize=14, zorder=5, markeredgecolor="#fff", markeredgewidth=1.2)
    if destination:
        ax.plot(*destination, marker="*", color="#a855f7", markersize=16, zorder=5, markeredgecolor="#fff", markeredgewidth=1.2)

    legend_handles = [
        mpatches.Patch(color="#10b981", label="Available"),
        mpatches.Patch(color="#ef4444", label="Busy"),
        mpatches.Patch(color="#f59e0b", label="Matched"),
    ]
    ax.legend(handles=legend_handles, loc="upper left", fontsize=7, facecolor="#150f24", edgecolor="#2d1b4e", labelcolor="#c9d1d9", framealpha=0.9)
    ax.set_xlim(-0.5, grid_size - 0.5)
    ax.set_ylim(-0.5, grid_size - 0.5)
    ax.set_title("Fleet Overview - All Drivers", color="#c084fc", fontsize=11, fontweight="bold", pad=10)
    ax.tick_params(colors="#484f58", labelsize=6)
    for spine in ax.spines.values():
        spine.set_color("#2d1b4e")
    ax.set_aspect("equal")
    plt.tight_layout()
    return fig


def build_path_timeline_html(pickup_path, trip_path, driver_loc, pickup, destination):
    nodes = []
    nodes.append(f'<div class="path-node"><div class="path-dot pd-driver"></div><div class="path-coord">D {driver_loc[0]},{driver_loc[1]}</div></div>')
    if pickup_path and len(pickup_path) > 2:
        step = max(len(pickup_path) // 3, 1)
        for i in range(step, len(pickup_path) - 1, step):
            p = pickup_path[i]
            nodes.append(f'<div class="path-connector pc-pickup"></div>')
            nodes.append(f'<div class="path-node"><div class="path-dot pd-mid"></div><div class="path-coord">{p[0]},{p[1]}</div></div>')
    nodes.append(f'<div class="path-connector pc-pickup"></div>')
    nodes.append(f'<div class="path-node"><div class="path-dot pd-pickup"></div><div class="path-coord">P {pickup[0]},{pickup[1]}</div></div>')
    if trip_path and len(trip_path) > 2:
        step = max(len(trip_path) // 3, 1)
        for i in range(step, len(trip_path) - 1, step):
            p = trip_path[i]
            nodes.append(f'<div class="path-connector pc-trip"></div>')
            nodes.append(f'<div class="path-node"><div class="path-dot pd-mid"></div><div class="path-coord">{p[0]},{p[1]}</div></div>')
    nodes.append(f'<div class="path-connector pc-trip"></div>')
    nodes.append(f'<div class="path-node"><div class="path-dot pd-dest"></div><div class="path-coord">* {destination[0]},{destination[1]}</div></div>')
    return '<div class="path-timeline">' + ''.join(nodes) + '</div>'


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## \U0001F6E1\uFE0F SafeHer Ride")
    st.markdown(f"##### Welcome, **{st.session_state.username}**")
    if st.button("Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()
    st.markdown("---")

    st.markdown("### \U0001F4CA Safety Analytics")
    st.markdown(
        f'<div class="sidebar-stat-card"><span class="ss-label">Total Drivers</span><span class="ss-value">{total_drivers}</span></div>'
        f'<div class="sidebar-stat-card"><span class="ss-label">Available</span><span class="ss-value" style="color:#10b981">{available_drivers}</span></div>'
        f'<div class="sidebar-stat-card"><span class="ss-label">Verified</span><span class="ss-value" style="color:#a855f7">{verified_drivers}</span></div>'
        f'<div class="sidebar-stat-card"><span class="ss-label">Avg Safety</span><span class="ss-value" style="color:#f59e0b">{avg_safety:.1f}/5</span></div>'
        f'<div class="sidebar-stat-card"><span class="ss-label">Rider Requests</span><span class="ss-value" style="color:#ec4899">{total_riders}</span></div>'
        f'<div class="sidebar-stat-card"><span class="ss-label">Urgent Rides</span><span class="ss-value" style="color:#ef4444">{urgent_riders}</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### \U0001F4C8 Driver Status")
    st.bar_chart(
        pd.DataFrame({"Status": ["Available", "Busy"], "Count": [available_drivers, busy_drivers]}).set_index("Status"),
        color=["#a855f7"],
    )

    st.markdown("---")
    st.markdown("### \U0001F512 LLM Integration")
    api_key_input = st.text_input("Google API Key (optional)", type="password", key="api_key_input")
    api_key = api_key_input or os.environ.get("GOOGLE_API_KEY", "")
    if api_key:
        st.markdown('<div class="llm-status llm-active">\u2705 LLM Active</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="llm-status llm-fallback">\u26A0\uFE0F Algorithmic Fallback</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;opacity:0.4;font-size:0.72rem;padding:0.5rem 0;'>"
        "SafeHer Ride v1.0<br>Dijkstra + AI Safety Engine</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# MAIN CONTENT
# ---------------------------------------------------------------------------

# Hero
st.markdown(
    '<div class="hero-banner">'
    "<h1>\U0001F6E1\uFE0F SafeHer Ride</h1>"
    "<p>AI-powered safe mobility platform &mdash; exclusively for women riders and verified female drivers</p>"
    '<span class="hero-badge">VERIFIED DRIVERS &bull; SAFETY INTELLIGENCE &bull; SECURE ROUTES</span>'
    "</div>",
    unsafe_allow_html=True,
)

# Top Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="top-metric tm-purple"><div class="tm-icon">\U0001F46E\u200D\u2640\uFE0F</div><div class="tm-value">{verified_drivers}</div><div class="tm-label">Verified Drivers</div></div>', unsafe_allow_html=True)
with m2:
    pct = f"{verified_drivers / max(total_drivers, 1) * 100:.0f}%"
    st.markdown(f'<div class="top-metric tm-green"><div class="tm-icon">\u2705</div><div class="tm-value">{pct}</div><div class="tm-label">Verified Rate</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="top-metric tm-amber"><div class="tm-icon">\u2B50</div><div class="tm-value">{avg_safety:.1f}</div><div class="tm-label">Avg Safety Score</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="top-metric tm-rose"><div class="tm-icon">\U0001F6A8</div><div class="tm-value">{urgent_riders}</div><div class="tm-label">Urgent Requests</div></div>', unsafe_allow_html=True)

if "ride_status" not in st.session_state:
    st.session_state.ride_status = "Not Booked"

if "booking_confirmed" not in st.session_state:
    st.session_state.booking_confirmed = False

if "current_booking" not in st.session_state:
    st.session_state.current_booking = None

if "emergency_contact" not in st.session_state:
    st.session_state.emergency_contact = None

if "driver_logged_in" not in st.session_state:
    st.session_state.driver_logged_in = False

if "driver_data" not in st.session_state:
    st.session_state.driver_data = None