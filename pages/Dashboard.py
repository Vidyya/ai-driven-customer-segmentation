import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
[data-testid="stAppViewContainer"]{background:#f1f5f9;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f172a 0%,#1e293b 100%);border-right:1px solid #334155;}
[data-testid="stSidebar"] *{color:#e2e8f0 !important;}
.page-header{background:linear-gradient(135deg,#1e40af 0%,#7c3aed 100%);padding:2rem 2.5rem;border-radius:16px;margin-bottom:2rem;box-shadow:0 8px 30px rgba(30,64,175,.3);}
.page-header h1{color:white!important;margin:0;font-size:1.8rem;font-weight:700;}
.page-header p{color:rgba(255,255,255,.8);margin:.4rem 0 0;font-size:.93rem;}
.kpi{background:white;border-radius:14px;padding:1.4rem 1.2rem;box-shadow:0 2px 12px rgba(0,0,0,.07);border-left:5px solid;text-align:center;}
.kpi-val{font-size:2rem;font-weight:700;color:#1e293b;margin:.3rem 0;}
.kpi-lbl{font-size:.78rem;color:#64748b;text-transform:uppercase;letter-spacing:.06em;font-weight:600;}
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

@st.cache_data
def load():
    return pd.read_csv("data/mall_customes.csv")

df = load()

st.markdown("""
<div class="page-header">
    <h1>📊 Overview Dashboard</h1>
    <p>Key performance indicators and customer demographics at a glance</p>
</div>
""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
kpis = [
    ("#3b82f6", "👥", len(df),                                   "Total Customers"),
    ("#8b5cf6", "🎂", f"{df['Age'].mean():.1f}",                 "Average Age"),
    ("#059669", "💰", f"${df['Annual Income (k$)'].mean():.1f}k","Average Income"),
    ("#f59e0b", "🛍️", f"{df['Spending Score (1-100)'].mean():.1f}","Avg Spending Score"),
]
for col, (color, icon, val, lbl) in zip([k1, k2, k3, k4], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi" style="border-color:{color};">
            <div style="font-size:1.8rem;">{icon}</div>
            <div class="kpi-val">{val}</div>
            <div class="kpi-lbl">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Age histogram + Gender pie ────────────────────────────────────────
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig = px.histogram(df, x="Age", nbins=20, title="Age Distribution",
                       color_discrete_sequence=["#3b82f6"], template="plotly_white")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      margin=dict(t=40,b=20,l=10,r=10), showlegend=False)
    fig.update_traces(marker_line_color="white", marker_line_width=1.2)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    gc = df["Gender"].value_counts().reset_index()
    gc.columns = ["Gender", "Count"]
    fig2 = px.pie(gc, names="Gender", values="Count", title="Gender Split",
                  color_discrete_sequence=["#3b82f6","#f472b6"], hole=0.45,
                  template="plotly_white")
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=10,l=10,r=10),
                       legend=dict(orientation="h", y=-0.1))
    fig2.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 2: Income vs Spending scatter ────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
fig3 = px.scatter(df, x="Annual Income (k$)", y="Spending Score (1-100)",
                  color="Gender", hover_data=["CustomerID", "Age"],
                  color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"},
                  title="Annual Income vs Spending Score",
                  template="plotly_white", opacity=0.78)
fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                   margin=dict(t=50,b=20,l=10,r=10),
                   legend=dict(orientation="h", y=1.12))
fig3.update_traces(marker=dict(size=9, line=dict(width=1, color="white")))
st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Row 3: Income box + Spending box ─────────────────────────────────────────
c3, c4 = st.columns(2)
with c3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig4 = px.box(df, x="Gender", y="Annual Income (k$)", color="Gender",
                  color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"},
                  title="Income by Gender", template="plotly_white", points="all")
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       margin=dict(t=50,b=20,l=10,r=10), showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig5 = px.box(df, x="Gender", y="Spending Score (1-100)", color="Gender",
                  color_discrete_map={"Male":"#3b82f6","Female":"#f472b6"},
                  title="Spending Score by Gender", template="plotly_white", points="all")
    fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       margin=dict(t=50,b=20,l=10,r=10), showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Raw data ──────────────────────────────────────────────────────────────────
with st.expander("📋 View Raw Dataset"):
    st.dataframe(df, use_container_width=True)
    st.download_button("⬇️ Download Dataset", df.to_csv(index=False).encode(),
                       "mall_customers.csv", "text/csv")
