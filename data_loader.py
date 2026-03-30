import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/" \
          "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    
    try:
        with st.spinner("📡 Fetching COVID-19 data..."):
            df = pd.read_csv(url)

        # Drop unnecessary columns safely
        cols_to_drop = ['Province/State', 'Lat', 'Long']
        df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

        # Group by country
        df = df.groupby('Country/Region').sum()

        # Transpose (dates as index)
        df = df.T

        # Convert index to datetime
        df.index = pd.to_datetime(df.index)

        return df

    except Exception as e:
        st.error("❌ Failed to load dataset. Please check your internet connection.")
        st.exception(e)
        return pd.DataFrame()


def prepare_data(df, country):
    try:
        if country not in df.columns:
            st.warning(f"⚠️ {country} not found in dataset.")
            return pd.DataFrame()

        data = df[country].reset_index()
        data.columns = ['Date', 'Cases']

        # Create time-based feature
        data['Days'] = (data['Date'] - data['Date'].min()).dt.days

        return data

    except Exception as e:
        st.error("❌ Error while preparing data.")
        st.exception(e)
        return pd.DataFrame()