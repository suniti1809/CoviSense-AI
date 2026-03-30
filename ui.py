def apply_ui():
    import streamlit as st

    st.markdown("""
    <style>

    /* 🌿 MAIN BACKGROUND (SOFT DARK GREEN) */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #1a2e25);
        color: #e2e8f0;
        font-family: 'Segoe UI', sans-serif;
    }

    /* 🏆 TITLE */
    .title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        color: #22c55e;
        margin-bottom: 5px;
        text-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
    }

    /* Subtitle */
    p {
        text-align: center;
        color: #cbd5f5;
    }

    /* Divider */
    .divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #22c55e, transparent);
        margin: 25px 0;
    }

    /* 💎 METRIC CARDS */
    .stMetric {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 18px;
        border: 1px solid rgba(34, 197, 94, 0.25);
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }

    .stMetric:hover {
        transform: translateY(-4px);
        box-shadow: 0 0 18px rgba(34, 197, 94, 0.3);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #061410, #0b2a1e);
        border-right: 2px solid rgba(34, 197, 94, 0.4);
        box-shadow: 4px 0 20px rgba(34, 197, 94, 0.2);
    }

    /* Inputs */
    .stTextInput input {
        background: rgba(255,255,255,0.06);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(34, 197, 94, 0.4);
    }

    .stSelectbox div {
        background: rgba(255,255,255,0.06);
    }

    /* Buttons */
    button {
        background: linear-gradient(90deg, #22c55e, #4ade80);
        color: black;
        border-radius: 10px;
        font-weight: bold;
        border: none;
    }

    /* Charts */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
    }

    </style>
    """, unsafe_allow_html=True)