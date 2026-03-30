import streamlit as st
import plotly.express as px
import pandas as pd

from data_loader import load_data, prepare_data
from model import train_models, predict_future
from analytics import add_analytics, get_insights
from chatbot import ask_gpt
from ui import apply_ui

# Page setup
st.set_page_config(layout="wide")
apply_ui()

st.markdown("""
<div class="title">
CoviSense AI
</div>

<p style='text-align:center; font-size:16px; color:#bbbbbb; letter-spacing:1px;'>🦠
COVID-19 Monitoring & Forecasting System
</p>

<p style='text-align:center; color:#00f2fe;'>
AI • Data • Prediction • Insights
</p>
""", unsafe_allow_html=True)

# Load data
placeholder = st.empty()

with placeholder.container():
  with st.spinner("Loading..."):
    df = load_data()


# Sidebar
country = st.sidebar.selectbox("🌍 Select Country", df.columns)
days = st.sidebar.slider("📅 Prediction Days", 7, 60, 30)

# Prepare data
data = prepare_data(df, country)
data = add_analytics(data)

X = data[['Days']]
y = data['Cases']

# Model
model, _ = train_models(X, y)

# Insights
insights = get_insights(data)

# 📊 METRICS
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("📊 Cases", insights["current"])
c2.metric("📈 Growth", f"{insights['growth']}%")
c3.metric("🔥 Avg Cases Daily", insights["avg_daily"])
c4.metric("📉 Trend", insights["trend"])
c5.metric("⚠ Risk", insights["risk"])

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 📈 CASES GRAPH
fig = px.line(data, x="Date", y="Cases", title="Cases Over Time")
st.plotly_chart(fig, use_container_width=True)

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 📊 DAILY CASES
st.subheader("📊 Daily Cases Analysis")
st.line_chart(data.set_index("Date")["Daily"])

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 🔮 PREDICTION
pred = predict_future(model, X['Days'].max(), days)

future_dates = pd.date_range(
    start=data['Date'].max(),
    periods=days+1
)[1:]

forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Prediction": pred
})

st.subheader("🔮 Future Prediction")
fig2 = px.line(forecast_df, x="Date", y="Prediction")
fig2.update_traces(line=dict(width=3, dash="dot"))
st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.subheader("🌍 Global COVID-19 Live Globe")

# Prepare data
latest = df.iloc[-1]

map_df = pd.DataFrame({
    "Country": latest.index,
    "Cases": latest.values
})

map_df = map_df.dropna()
map_df = map_df[map_df["Cases"] > 0]

# Keep names same
map_df["Country"] = map_df["Country"].str.replace("_", " ")

# 🎛️ Rotation control
angle = st.slider("🔄 Rotate Globe", 0, 360, 40)

# Globe plot
fig_globe = px.choropleth(
    map_df,
    locations="Country",
    locationmode="country names",
    color="Cases",
    hover_name="Country",
    color_continuous_scale="Inferno"
)

fig_globe.update_geos(
    projection_type="orthographic",
    projection_rotation=dict(lon=angle),
    showcoastlines=True,
    coastlinecolor="white",
    showland=True,
    landcolor="blue",
    showocean=True,
    oceancolor="#1677B3"
)

fig_globe.update_layout(
    template="plotly_dark",
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(fig_globe, use_container_width=True)

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 🧠 INSIGHTS PANEL
st.subheader("🧠 AI Insights")

st.markdown(f"""
<div style="
background: rgba(255,255,255,0.05);
padding: 20px;
border-radius: 15px;
backdrop-filter: blur(10px);
">
📊 Cases :     {insights['current']} <br>
📈 Growth :    {insights['growth']}% <br>
🔥 Avg Cases : {insights['avg_daily']} <br>
⚠  Risk :      {insights['risk']} <br>
📉 Trend :     {insights['trend']}
</div>
""", unsafe_allow_html=True)

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 🤖 SMART CHATBOT
st.subheader("🤖 Smart AI Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("💬 Ask about COVID-19 trends, risk, prediction...")

if user_input:
    context = {
        "cases": insights["current"],
        "growth": insights["growth"],
        "peak": insights["peak"],
        "trend": insights["trend"],
        "risk": insights["risk"]
    }

    response = ask_gpt(user_input, context)
    st.session_state.chat.append(("AI", response))

# Display chat
for role, msg in st.session_state.chat:
        st.markdown(f"{msg}")