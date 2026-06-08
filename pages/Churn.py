import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Customer Churn",
    page_icon="📉",
    layout="wide"
)

st.title("📉 Customer Churn Analysis")

# Load Dataset
df = pd.read_csv("data/mall_customes.csv")

# Create Churn Logic
df["Churn"] = (
    (df["Spending Score (1-100)"] < 30)
    &
    (df["Annual Income (k$)"] < 40)
).astype(int)

# Metrics
total_customers = len(df)

churned_customers = df["Churn"].sum()

active_customers = total_customers - churned_customers

churn_rate = (
    churned_customers / total_customers
) * 100

col1,col2,col3 = st.columns(3)

with col1:
    st.metric(
        "Total Customers",
        total_customers
    )

with col2:
    st.metric(
        "Active Customers",
        active_customers
    )

with col3:
    st.metric(
        "Churn Rate",
        f"{churn_rate:.2f}%"
    )

# Pie Chart

st.subheader("Customer Status Distribution")

status_df = pd.DataFrame({
    "Status":[
        "Active",
        "Churned"
    ],
    "Count":[
        active_customers,
        churned_customers
    ]
})

fig = px.pie(
    status_df,
    names="Status",
    values="Count",
    title="Active vs Churned Customers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Churn Table

st.subheader("⚠️ Customers Likely To Leave")

churn_df = df[
    df["Churn"] == 1
]

st.dataframe(
    churn_df,
    use_container_width=True
)

# Risk Customers Graph

st.subheader("Risk Customers")

fig2 = px.scatter(
    df,
    x="Annual Income (k$)",
    y="Spending Score (1-100)",
    color=df["Churn"].map({
        0:"Active",
        1:"Churn Risk"
    }),
    title="Customer Churn Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# Recommendation

st.subheader("AI Recommendation")

if churn_rate > 20:

    st.error(
        """
        High churn rate detected.

        Suggested Actions:
        - Loyalty Programs
        - Discount Coupons
        - Personalized Marketing
        - Customer Retention Campaigns
        """
    )

else:

    st.success(
        """
        Customer retention is healthy.
        Continue engagement campaigns.
        """
    )