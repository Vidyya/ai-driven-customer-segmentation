import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
import joblib

st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Customer Segmentation")

# =========================
# LOAD DATA
# =========================

@st.cache_data
def load_data():
    return pd.read_csv("data/mall_customes.csv")

df = load_data()

# =========================
# ADD CUSTOMER FORM
# =========================

st.subheader("➕ Add New Customer")

with st.form("customer_form"):

    customer_id = int(df["CustomerID"].max()) + 1

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=80,
        value=25
    )

    income = st.number_input(
        "Annual Income (k$)",
        min_value=10,
        max_value=150,
        value=50
    )

    spending = st.number_input(
        "Spending Score (1-100)",
        min_value=1,
        max_value=100,
        value=50
    )

    submit = st.form_submit_button(
        "Add Customer"
    )

if submit:

    new_customer = pd.DataFrame({
        "CustomerID": [customer_id],
        "Gender": [gender],
        "Age": [age],
        "Annual Income (k$)": [income],
        "Spending Score (1-100)": [spending]
    })

    df = pd.concat(
        [df, new_customer],
        ignore_index=True
    )

    df.to_csv(
        "data/mall_customes.csv",
        index=False
    )

    st.success("Customer Added Successfully")

    st.cache_data.clear()

    st.rerun()

# =========================
# DATA PREVIEW
# =========================

st.subheader("📋 Dataset Preview")

st.dataframe(
    df.head(),
    use_container_width=True
)

# =========================
# K-MEANS SECTION
# =========================

st.subheader("⚙️ K-Means Clustering")

k = st.slider(
    "Select Number of Clusters",
    2,
    10,
    5
)

if st.button("🚀 Run K-Means"):

    X = df[
        [
            "Annual Income (k$)",
            "Spending Score (1-100)"
        ]
    ]

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    df["Cluster"] = model.fit_predict(X)

    joblib.dump(
        model,
        "models/kmeans_model.pkl"
    )

    cluster_stats = (
        df.groupby("Cluster")
        .agg({
            "Annual Income (k$)": "mean",
            "Spending Score (1-100)": "mean"
        })
    )

    labels = {}

    for cluster in cluster_stats.index:

        income = cluster_stats.loc[
            cluster,
            "Annual Income (k$)"
        ]

        spending = cluster_stats.loc[
            cluster,
            "Spending Score (1-100)"
        ]

        if income > 60 and spending > 60:
            labels[cluster] = "VIP Customers"

        elif income > 60 and spending <= 60:
            labels[cluster] = "Potential Customers"

        elif income <= 60 and spending > 60:
            labels[cluster] = "Impulse Buyers"

        elif income < 40 and spending < 40:
            labels[cluster] = "Low Priority Customers"

        else:
            labels[cluster] = "Regular Customers"

    df["Segment"] = df["Cluster"].map(labels)

    st.success("K-Means Completed Successfully")

    latest_customer = df.iloc[-1]

    st.info(
        f"Latest Customer belongs to: {latest_customer['Segment']}"
    )

    # =========================
    # GRAPH
    # =========================

    st.subheader("📊 Customer Segmentation Graph")

    fig = px.scatter(
        df,
        x="Annual Income (k$)",
        y="Spending Score (1-100)",
        color="Segment",
        hover_data=[
            "CustomerID",
            "Age",
            "Gender"
        ],
        title="Customer Segments"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =========================
    # SUMMARY
    # =========================

    st.subheader("📈 Segment Summary")

    summary = (
        df.groupby("Segment")
        .agg(
            Customers=("CustomerID", "count"),
            Avg_Income=("Annual Income (k$)", "mean"),
            Avg_Spending=("Spending Score (1-100)", "mean")
        )
        .round(2)
        .reset_index()
    )

    st.dataframe(
        summary,
        use_container_width=True
    )

    # =========================
    # TABLE
    # =========================

    st.subheader("👥 Customer Segment Table")

    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )

    csv = df.to_csv(index=False)

    st.download_button(
        "📥 Download Clustered Dataset",
        csv,
        "customer_segments.csv",
        "text/csv"
    )