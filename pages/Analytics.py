import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Customer Analytics", page_icon="🔍", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
[data-testid="stAppViewContainer"]{background:#f1f5f9;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f172a 0%,#1e293b 100%);border-right:1px solid #334155;}
[data-testid="stSidebar"] *{color:#e2e8f0 !important;}
.page-header{background:linear-gradient(135deg,#7c3aed 0%,#db2777 100%);padding:2rem 2.5rem;border-radius:16px;margin-bottom:2rem;box-shadow:0 8px 30px rgba(124,58,237,.3);}
.page-header h1{color:white!important;margin:0;font-size:1.8rem;font-weight:700;}
.page-header p{color:rgba(255,255,255,.8);margin:.4rem 0 0;font-size:.93rem;}
.card{background:white;border-radius:14px;padding:1.4rem;box-shadow:0 2px 12px rgba(0,0,0,.07);margin-bottom:1.4rem;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:1.4rem 1rem 1rem;border-bottom:1px solid #334155;margin-bottom:1rem;">
        <div style="font-size:2rem;">🤖</div>
        <div style="font-size:1.1rem;font-weight:700;margin-top:.3rem;">AI Customer Analytics</div>
        <div style="font-size:.73rem;color:#94a3b8;">K-Means Clustering System</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("**Navigate**")
    st.page_link("app.py",                label="🏠  Home")
    st.page_link("pages/Dashboard.py",    label="📊  Dashboard")
    st.page_link("pages/Analytics.py",    label="🔍  Customer Analytics")
    st.page_link("pages/Segmentation.py", label="🎯  Segmentation")
    st.page_link("pages/Insights.py",     label="💡  Business Insights")
    st.markdown("---")
    uploaded = st.file_uploader("Upload CSV dataset", type=["csv"])

@st.cache_data
def load():
    return pd.read_csv("data/mall_customes.csv")

df = pd.read_csv(uploaded) if uploaded else load()

st.markdown("""
<div class="page-header">
    <h1>🔍 Customer Analytics</h1>
    <p>Gender, age, income and spending score distributions</p>
</div>
""", unsafe_allow_html=True)

if uploaded:
    st.success("Showing analysis for uploaded dataset.")

# ── 1. Gender Distribution ────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### 👥 Gender Distribution")
c1, c2 = st.columns(2)
with c1:
    gc = df["Gender"].value_counts().reset_index()
    gc.columns = ["Gender", "Count"]
    fig = px.bar(gc, x="Gender", y="Count", color="Gender",
                 color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"},
                 text="Count", template="plotly_white",
                 title="Customer Count by Gender")
    fig.update_traces(textposition="outside", marker_line_color="white", marker_line_width=1)
    fig.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=20,l=10,r=10))
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig2 = px.pie(gc, names="Gender", values="Count", hole=0.5,
                  color_discrete_sequence=["#3b82f6","#f472b6"],
                  template="plotly_white", title="Gender Percentage Split")
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=10,l=10,r=10),
                       legend=dict(orientation="h", y=-0.1))
    fig2.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig2, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── 2. Age Distribution ───────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### 🎂 Age Distribution")
c3, c4 = st.columns(2)
with c3:
    fig3 = px.histogram(df, x="Age", nbins=20, color="Gender",
                        barmode="overlay", opacity=0.75,
                        color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"},
                        title="Age Histogram by Gender", template="plotly_white")
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       margin=dict(t=40,b=20,l=10,r=10))
    st.plotly_chart(fig3, use_container_width=True)
with c4:
    fig4 = px.box(df, x="Gender", y="Age", color="Gender",
                  color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"},
                  points="all", template="plotly_white",
                  title="Age Box Plot by Gender")
    fig4.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=20,l=10,r=10))
    st.plotly_chart(fig4, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── 3. Income Distribution ────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### 💰 Income Distribution")
c5, c6 = st.columns(2)
with c5:
    fig5 = px.histogram(df, x="Annual Income (k$)", nbins=20, color="Gender",
                        barmode="overlay", opacity=0.75,
                        color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"},
                        title="Annual Income Histogram", template="plotly_white")
    fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       margin=dict(t=40,b=20,l=10,r=10))
    st.plotly_chart(fig5, use_container_width=True)
with c6:
    fig6 = px.violin(df, x="Gender", y="Annual Income (k$)", color="Gender",
                     box=True, points="all",
                     color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"},
                     title="Income Violin by Gender", template="plotly_white")
    fig6.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=20,l=10,r=10))
    st.plotly_chart(fig6, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── 4. Spending Distribution ──────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### 🛍️ Spending Score Distribution")
c7, c8 = st.columns(2)
with c7:
    fig7 = px.histogram(df, x="Spending Score (1-100)", nbins=20, color="Gender",
                        barmode="overlay", opacity=0.75,
                        color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"},
                        title="Spending Score Histogram", template="plotly_white")
    fig7.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       margin=dict(t=40,b=20,l=10,r=10))
    st.plotly_chart(fig7, use_container_width=True)
with c8:
    fig8 = px.violin(df, x="Gender", y="Spending Score (1-100)", color="Gender",
                     box=True, points="all",
                     color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"},
                     title="Spending Score Violin", template="plotly_white")
    fig8.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=20,l=10,r=10))
    st.plotly_chart(fig8, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── 5. Statistical Summary ────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### 📋 Statistical Summary")
st.dataframe(
    df[["Age","Annual Income (k$)","Spending Score (1-100)"]].describe().T
      .style.format("{:.2f}").background_gradient(cmap="Blues", subset=["mean","std"]),
    use_container_width=True
)
st.markdown('</div>', unsafe_allow_html=True)
