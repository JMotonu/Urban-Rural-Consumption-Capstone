import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="KCHS 2021 Consumption Analysis",
    layout="wide"
)

st.title("Kenya Household Consumption Analysis")
st.write(
    "Urban-rural household consumption analysis using KCHS 2021 data."
)

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/processed/analysis_dataset.csv"
    )

df = load_data()

# Sidebar
st.sidebar.header("Filters")

areas = st.sidebar.multiselect(
    "Select Residence",
    options=df["urban_rural"].dropna().unique(),
    default=df["urban_rural"].dropna().unique()
)

filtered = df[
    df["urban_rural"].isin(areas)
]

# Key statistics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Households",
        f"{len(filtered):,}"
    )

with col2:
    st.metric(
        "Mean Consumption",
        f"{filtered['total_consumption'].mean():,.2f}"
    )

with col3:
    st.metric(
        "Median Consumption",
        f"{filtered['total_consumption'].median():,.2f}"
    )

# Objective 1
st.header("Objective 1: Urban vs Rural Consumption")

summary = (
    filtered
    .groupby("urban_rural")["total_consumption"]
    .agg(["count", "mean", "median", "std"])
    .reset_index()
)

st.dataframe(summary)

fig1 = px.box(
    filtered,
    x="urban_rural",
    y="total_consumption",
    title="Household Consumption by Residence"
)

st.plotly_chart(
    fig1,
    width="stretch"
)

# Objective 2
st.header("Objective 2: Household Size and Consumption")

fig2 = px.scatter(
    filtered,
    x="hhsize_x",
    y="total_consumption",
    title="Household Size vs Total Consumption",
    labels={
        "hhsize_x": "Household Size",
        "total_consumption": "Total Consumption"
    },
    trendline="ols"
)

st.plotly_chart(fig2, width="stretch")

# Data
st.header("Sample of Analysis Dataset")

st.dataframe(
    filtered.head(100)
)