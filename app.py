# ============================================================
# URBAN-RURAL CONSUMPTION CAPSTONE
# Streamlit Dashboard | KCHS 2021
# ============================================================

from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, pearsonr


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Urban-Rural Consumption | KCHS 2021",
    page_icon="📊",
    layout="wide"
)

st.title("Urban–Rural Household Consumption in Kenya")
st.caption(
    "KCHS 2021 | Data Science Capstone | CRISP-DM"
)

st.markdown("""
This dashboard examines household consumption patterns using
five visual analyses, descriptive statistics, hypothesis testing,
and correlation analysis.
""")


# ============================================================
# 2. LOAD PROCESSED DATA
# ============================================================

DATA_FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "processed"
    / "analysis_dataset.csv"
)


@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data


if not DATA_FILE.exists():
    st.error(
        "Processed dataset not found. Please save "
        "analysis_dataset.csv in data/processed/."
    )
    st.stop()

df = load_data(str(DATA_FILE))


# ============================================================
# 3. VALIDATE REQUIRED COLUMNS
# ============================================================

required_columns = [
    "urban_rural",
    "total_consumption",
    "total_nonfood_consumption",
    "hhsize_x",
    "padqexp"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "The dataset is missing these required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


# Convert analysis columns to numeric where appropriate.
numeric_columns = [
    "total_consumption",
    "total_nonfood_consumption",
    "hhsize_x",
    "padqexp"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["urban_rural"] = (
    df["urban_rural"]
    .astype("string")
    .str.strip()
)

# Exclude missing or invalid values from the main analysis.
df = df.dropna(
    subset=["urban_rural", "total_consumption"]
).copy()

df = df[
    (df["total_consumption"] >= 0)
    & (df["urban_rural"] != "")
].copy()


# ============================================================
# 4. SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Dashboard Filters")

available_areas = sorted(
    df["urban_rural"].dropna().unique().tolist()
)

selected_areas = st.sidebar.multiselect(
    "Select residence category",
    options=available_areas,
    default=available_areas
)

filtered = df[
    df["urban_rural"].isin(selected_areas)
].copy()

if filtered.empty:
    st.warning("Select at least one residence category.")
    st.stop()


# ============================================================
# 5. KEY PERFORMANCE INDICATORS
# ============================================================

st.header("Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Households / Records",
        f"{len(filtered):,}"
    )

with col2:
    st.metric(
        "Mean Total Consumption",
        f"{filtered['total_consumption'].mean():,.2f}"
    )

with col3:
    st.metric(
        "Median Total Consumption",
        f"{filtered['total_consumption'].median():,.2f}"
    )

with col4:
    st.metric(
        "Mean Non-Food Consumption",
        f"{filtered['total_nonfood_consumption'].mean():,.2f}"
        if filtered["total_nonfood_consumption"].notna().any()
        else "N/A"
    )

st.caption(
    "Consumption units and the interpretation of records depend "
    "on the definitions and structure of the prepared KCHS dataset."
)


# ============================================================
# FIGURE 1
# URBAN VS RURAL MEAN NON-FOOD CONSUMPTION
# ============================================================

st.header("Figure 1: Mean Non-Food Consumption by Residence")

urban_rural = (
    filtered.groupby("urban_rural")["total_nonfood_consumption"]
    .agg(["mean", "std", "count"])
    .reset_index()
)

fig1 = px.bar(
    urban_rural,
    x="urban_rural",
    y="mean",
    error_y="std",
    title="Mean Non-Food Consumption by Urban-Rural Residence",
    labels={
        "urban_rural": "Residence",
        "mean": "Mean Non-Food Consumption"
    },
    hover_data=["count", "std"]
)

st.plotly_chart(fig1, use_container_width=True)

with st.expander("View Figure 1 summary data"):
    st.dataframe(urban_rural, use_container_width=True)


# ============================================================
# FIGURE 2
# DISTRIBUTION OF NON-FOOD CONSUMPTION
# ============================================================

st.header("Figure 2: Distribution of Non-Food Consumption")

distribution_df = filtered.dropna(
    subset=["total_nonfood_consumption"]
)

fig2 = px.histogram(
    distribution_df,
    x="total_nonfood_consumption",
    color="urban_rural",
    nbins=50,
    histnorm="probability density",
    marginal="box",
    barmode="overlay",
    opacity=0.65,
    title="Distribution of Household Non-Food Consumption",
    labels={
        "total_nonfood_consumption": "Total Non-Food Consumption",
        "urban_rural": "Residence",
        "count": "Density"
    }
)

st.plotly_chart(fig2, use_container_width=True)


# ============================================================
# FIGURE 3
# HOUSEHOLD SIZE VS TOTAL CONSUMPTION
# ============================================================

st.header("Figure 3: Household Size and Total Consumption")

scatter_df = filtered.dropna(
    subset=["hhsize_x", "total_consumption"]
)

fig3 = px.scatter(
    scatter_df,
    x="hhsize_x",
    y="total_consumption",
    color="urban_rural",
    opacity=0.45,
    trendline="ols",
    title="Relationship Between Household Size and Total Consumption",
    labels={
        "hhsize_x": "Household Size",
        "total_consumption": "Total Consumption",
        "urban_rural": "Residence"
    }
)

st.plotly_chart(fig3, use_container_width=True)


# ============================================================
# OBJECTIVE 1
# URBAN-RURAL COMPARISON AND WELCH'S T-TEST
# ============================================================

st.subheader("Objective 1: Urban–Rural Consumption Comparison")

st.write(
    "**H₀₁:** Mean total consumption does not differ between "
    "urban and rural households."
)

st.write(
    "**H₁₁:** Mean total consumption differs between "
    "urban and rural households."
)

urban = filtered.loc[
    filtered["urban_rural"].str.lower() == "urban",
    "total_consumption"
].dropna()

rural = filtered.loc[
    filtered["urban_rural"].str.lower() == "rural",
    "total_consumption"
].dropna()

if len(urban) >= 2 and len(rural) >= 2:

    test = ttest_ind(
        urban,
        rural,
        equal_var=False
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Urban Mean", f"{urban.mean():,.2f}")

    with col2:
        st.metric("Rural Mean", f"{rural.mean():,.2f}")

    with col3:
        st.metric(
            "Difference (Urban − Rural)",
            f"{urban.mean() - rural.mean():,.2f}"
        )

    st.write(f"**Welch t-statistic:** {test.statistic:.4f}")
    st.write(f"**p-value:** {test.pvalue:.6g}")

    if test.pvalue < 0.05:
        st.success(
            "Reject H₀₁ at the 5% significance level: "
            "the observed mean difference is statistically significant."
        )
    else:
        st.info(
            "Fail to reject H₀₁ at the 5% significance level: "
            "the evidence is insufficient to establish a difference."
        )

else:
    st.info(
        "Select both urban and rural categories and ensure each "
        "has at least two valid observations to run the t-test."
    )

st.caption(
    "The comparison is observational. Statistical significance "
    "does not establish that residence causes consumption differences."
)


# ============================================================
# FIGURE 4
# CORRELATION HEATMAP
# ============================================================

st.header("Figure 4: Correlation Heatmap")

correlation_variables = [
    "hhsize_x",
    "padqexp",
    "total_consumption",
    "total_nonfood_consumption"
]

corr_data = filtered[correlation_variables].dropna()

if len(corr_data) >= 2:

    corr = corr_data.corr()

    fig4 = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Correlation Matrix of Household Consumption Variables"
    )

    st.plotly_chart(fig4, use_container_width=True)

    with st.expander("View correlation matrix"):
        st.dataframe(corr, use_container_width=True)

else:
    st.info("Insufficient complete observations for the correlation heatmap.")


# ============================================================
# OBJECTIVE 2
# PEARSON CORRELATION
# ============================================================

st.subheader("Objective 2: Household Size and Consumption")

st.write(
    "**H₀₂:** There is no statistically significant linear "
    "correlation between household size and total consumption."
)

st.write(
    "**H₁₂:** There is a statistically significant linear "
    "correlation between household size and total consumption."
)

correlation_df = filtered[
    ["hhsize_x", "total_consumption"]
].dropna()

if (
    len(correlation_df) >= 3
    and correlation_df["hhsize_x"].nunique() > 1
    and correlation_df["total_consumption"].nunique() > 1
):

    r, p_value = pearsonr(
        correlation_df["hhsize_x"],
        correlation_df["total_consumption"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Pearson Correlation (r)", f"{r:.3f}")

    with col2:
        st.metric("p-value", f"{p_value:.6g}")

    with col3:
        st.metric("Complete Observations", f"{len(correlation_df):,}")

    if p_value < 0.05:
        st.success(
            "Reject H₀₂ at the 5% significance level: "
            "the linear correlation is statistically significant."
        )
    else:
        st.info(
            "Fail to reject H₀₂ at the 5% significance level: "
            "the evidence is insufficient to establish a linear correlation."
        )

else:
    st.info(
        "Insufficient variation or valid observations to calculate "
        "Pearson correlation."
    )

st.caption(
    "Correlation measures linear association, not causation. "
    "Extreme values and survey design may affect interpretation."
)


# ============================================================
# FIGURE 5
# A/B-STYLE GROUP COMPARISON BY HOUSEHOLD SIZE
# ============================================================

st.header("Figure 5: Household-Size Group Comparison")

st.write(
    "Group A contains households at or below the median household size; "
    "Group B contains households above the median."
)

ab_df = filtered.dropna(
    subset=["hhsize_x", "total_consumption"]
).copy()

if not ab_df.empty:

    median_size = ab_df["hhsize_x"].median()

    ab_df["AB_group"] = np.where(
        ab_df["hhsize_x"] <= median_size,
        "Group A",
        "Group B"
    )

    ab_summary = (
        ab_df.groupby("AB_group")["total_consumption"]
        .agg(["mean", "count"])
        .reindex(["Group A", "Group B"])
        .reset_index()
    )

    fig5 = px.bar(
        ab_summary,
        x="AB_group",
        y="mean",
        text_auto=".2f",
        title="Mean Total Consumption: Household-Size Group Comparison",
        labels={
            "AB_group": "Household-Size Group",
            "mean": "Mean Total Consumption"
        },
        hover_data=["count"]
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.dataframe(ab_summary, use_container_width=True)

    st.caption(
        f"Median household size in the selected records: {median_size:.2f}. "
        "This is an observational group comparison, not a randomized A/B test."
    )

else:
    st.info(
        "No valid household-size and consumption observations are available."
    )


# ============================================================
# DATA TABLE
# ============================================================

st.header("Analysis Dataset")

st.write("Explore the records included by the current residence filter.")

st.dataframe(
    filtered.head(100),
    use_container_width=True
)

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered analysis data (CSV)",
    data=csv_data,
    file_name="filtered_consumption_analysis.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Academic capstone | KCHS 2021 | CRISP-DM | "
    "Descriptive statistics, hypothesis testing, A/B Comparison,and correlation analysis"
)
