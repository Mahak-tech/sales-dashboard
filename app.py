"""
Sales Dashboard with Sentiment Analysis
Built with Streamlit + Plotly + TextBlob
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.sentiment import analyze_dataframe

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
@st.cache_data
def load_data(path="data/sales_data.csv"):
    df = pd.read_csv(path, parse_dates=["Date"])
    df = analyze_dataframe(df, text_column="Customer Review")
    return df

df = load_data()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.title("🔎 Filters")

min_date, max_date = df["Date"].min(), df["Date"].max()
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

categories = st.sidebar.multiselect(
    "Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

regions = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

salespeople = st.sidebar.multiselect(
    "Salesperson",
    options=sorted(df["Salesperson"].unique()),
    default=sorted(df["Salesperson"].unique())
)

# Apply filters
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    mask = (df["Date"] >= start) & (df["Date"] <= end)
else:
    mask = pd.Series(True, index=df.index)

filtered_df = df[
    mask
    & df["Category"].isin(categories)
    & df["Region"].isin(regions)
    & df["Salesperson"].isin(salespeople)
]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(filtered_df)}** of {len(df)} records")

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("📊 Sales Performance & Customer Sentiment Dashboard")
st.caption("Interactive dashboard built with Streamlit, Plotly, and TextBlob sentiment analysis")

if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust your filters.")
    st.stop()

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
total_revenue = filtered_df["Revenue"].sum()
total_units = filtered_df["Units Sold"].sum()
avg_order_value = filtered_df["Revenue"].mean()
positive_pct = (filtered_df["Sentiment"] == "Positive").mean() * 100
avg_polarity = filtered_df["Polarity"].mean()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("📦 Units Sold", f"{total_units:,}")
col3.metric("🧾 Avg Order Value", f"₹{avg_order_value:,.0f}")
col4.metric("😊 Positive Reviews", f"{positive_pct:.1f}%")
col5.metric("📈 Avg Sentiment Polarity", f"{avg_polarity:.2f}")

st.markdown("---")

# ---------------------------------------------------------
# ROW 1: Revenue trend + Category breakdown
# ---------------------------------------------------------
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    st.subheader("Revenue Trend Over Time")
    trend_df = filtered_df.groupby(pd.Grouper(key="Date", freq="W"))["Revenue"].sum().reset_index()
    fig_trend = px.line(
        trend_df, x="Date", y="Revenue",
        markers=True,
        labels={"Revenue": "Revenue (₹)"},
        template="plotly_white"
    )
    fig_trend.update_traces(line_color="#4C78A8")
    st.plotly_chart(fig_trend, use_container_width=True)

with row1_col2:
    st.subheader("Revenue by Category")
    cat_df = filtered_df.groupby("Category")["Revenue"].sum().reset_index()
    fig_cat = px.pie(
        cat_df, names="Category", values="Revenue",
        hole=0.45, template="plotly_white"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# ---------------------------------------------------------
# ROW 2: Region performance + Top products
# ---------------------------------------------------------
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("Revenue by Region")
    region_df = filtered_df.groupby("Region")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False)
    fig_region = px.bar(
        region_df, x="Region", y="Revenue",
        color="Region", text_auto=".2s",
        template="plotly_white"
    )
    fig_region.update_layout(showlegend=False)
    st.plotly_chart(fig_region, use_container_width=True)

with row2_col2:
    st.subheader("Top 5 Products by Units Sold")
    top_products = filtered_df.groupby("Product")["Units Sold"].sum().reset_index().sort_values(
        "Units Sold", ascending=False
    ).head(5)
    fig_products = px.bar(
        top_products, x="Units Sold", y="Product",
        orientation="h", color="Units Sold",
        color_continuous_scale="Blues", template="plotly_white"
    )
    fig_products.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_products, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------
# ROW 3: Sentiment Analysis Section
# ---------------------------------------------------------
st.header("💬 Customer Sentiment Analysis (TextBlob)")

row3_col1, row3_col2, row3_col3 = st.columns([1, 1, 1.4])

with row3_col1:
    st.subheader("Sentiment Distribution")
    sentiment_counts = filtered_df["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]
    color_map = {"Positive": "#2ECC71", "Neutral": "#F1C40F", "Negative": "#E74C3C"}
    fig_sentiment = px.pie(
        sentiment_counts, names="Sentiment", values="Count",
        color="Sentiment", color_discrete_map=color_map,
        hole=0.45, template="plotly_white"
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)

with row3_col2:
    st.subheader("Sentiment by Category")
    cat_sentiment = filtered_df.groupby(["Category", "Sentiment"]).size().reset_index(name="Count")
    fig_cat_sentiment = px.bar(
        cat_sentiment, x="Category", y="Count", color="Sentiment",
        color_discrete_map=color_map, barmode="stack",
        template="plotly_white"
    )
    fig_cat_sentiment.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig_cat_sentiment, use_container_width=True)

with row3_col3:
    st.subheader("Polarity vs Subjectivity")
    fig_scatter = px.scatter(
        filtered_df, x="Polarity", y="Subjectivity",
        color="Sentiment", color_discrete_map=color_map,
        hover_data=["Product", "Customer Review"],
        template="plotly_white"
    )
    fig_scatter.add_vline(x=0, line_dash="dash", line_color="gray")
    st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------------------------------------------------
# ROW 4: Raw data + reviews table
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📋 Detailed Records")

show_cols = [
    "Date", "Product", "Category", "Region", "Salesperson",
    "Units Sold", "Unit Price", "Revenue",
    "Customer Review", "Sentiment", "Polarity", "Subjectivity"
]
st.dataframe(
    filtered_df[show_cols].sort_values("Date", ascending=False),
    use_container_width=True,
    height=350
)

csv = filtered_df[show_cols].to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download filtered data as CSV",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit, Plotly, and TextBlob | Sample synthetic dataset")
