import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
import joblib

st.set_page_config(page_title="Business Insights", page_icon="💡", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
[data-testid="stAppViewContainer"]{background:#f1f5f9;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f172a 0%,#1e293b 100%);border-right:1px solid #334155;}
[data-testid="stSidebar"] *{color:#e2e8f0 !important;}
.page-header{background:linear-gradient(135deg,#f59e0b 0%,#ef4444 100%);padding:2rem 2.5rem;border-radius:16px;margin-bottom:2rem;box-shadow:0 8px 30px rgba(245,158,11,.3);}
.page-header h1{color:white!important;margin:0;font-size:1.8rem;font-weight:700;}
.page-header p{color:rgba(255,255,255,.88);margin:.4rem 0 0;font-size:.93rem;}
.card{background:white;border-radius:14px;padding:1.4rem;box-shadow:0 2px 12px rgba(0,0,0,.07);margin-bottom:1.4rem;}
.insight-box{border-radius:14px;padding:1.4rem 1.6rem;margin-bottom:1rem;border-left:6px solid;}
.ins-title{font-size:1.05rem;font-weight:700;margin-bottom:.5rem;}
.ins-row{font-size:.86rem;color:#374151;margin:.25rem 0;}
.ins-row b{color:#1e293b;}
.strategy{background:#f0fdf4;border:1px solid #86efac;border-radius:10px;padding:.9rem 1rem;margin-top:.7rem;font-size:.85rem;color:#166534;line-height:1.65;}
.strategy-title{font-weight:700;margin-bottom:.35rem;font-size:.88rem;}
[data-testid="stButton"]>button{background:linear-gradient(135deg,#f59e0b,#ef4444);color:white;border:none;border-radius:10px;padding:.65rem 2rem;font-weight:700;}
[data-testid="stButton"]>button:hover{opacity:.85;color:white;}
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

# ── Load + run clustering ─────────────────────────────────────────────────────
@st.cache_data
def load():
    return pd.read_csv("data/mall_customes.csv")

@st.cache_data
def run_kmeans():
    df = load()
    X  = df[["Annual Income (k$)", "Spending Score (1-100)"]].values
    model = KMeans(n_clusters=5, random_state=42, n_init=10)
    df["Cluster"] = model.fit_predict(X)
    return df, model

df, model = run_kmeans()

# ── Cluster metadata ──────────────────────────────────────────────────────────
CLUSTER_META = {
    0: {
        "title":    "Cluster 0 — VIP Customers",
        "badge":    "💎 High Income · High Spending",
        "color":    "#3b82f6",
        "bg":       "#eff6ff",
        "strategy_title": "Retention & Upsell",
        "strategy": (
            "These are your most valuable customers. Offer exclusive loyalty programs, "
            "early access to new products, and personalised premium services. "
            "Maintain engagement through VIP events and dedicated account managers. "
            "Focus on retention — a lost VIP customer is very expensive to replace."
        ),
    },
    1: {
        "title":    "Cluster 1 — Potential Customers",
        "badge":    "📈 High Income · Low Spending",
        "color":    "#f59e0b",
        "bg":       "#fffbeb",
        "strategy_title": "Re-engagement & Conversion",
        "strategy": (
            "High earners who spend conservatively — they can afford more but are not convinced yet. "
            "Target with premium product showcases, personalised recommendations, and limited-time "
            "exclusive offers. Investigate purchase barriers through surveys. "
            "Improve trust signals: reviews, guarantees and quality storytelling."
        ),
    },
    2: {
        "title":    "Cluster 2 — Impulse Buyers",
        "badge":    "🛍️ Low Income · High Spending",
        "color":    "#ef4444",
        "bg":       "#fef2f2",
        "strategy_title": "Flash Sales & Bundle Deals",
        "strategy": (
            "These customers love to spend even with limited income. Leverage flash sales, "
            "BOGO deals, and affordable bundles to drive volume. Introduce a buy-now-pay-later "
            "or EMI option to increase average order value. Use social proof and influencer "
            "marketing — they respond strongly to trends and peer recommendations."
        ),
    },
    3: {
        "title":    "Cluster 3 — Low Priority Customers",
        "badge":    "💤 Low Income · Low Spending",
        "color":    "#8b5cf6",
        "bg":       "#f5f3ff",
        "strategy_title": "Low-Cost Engagement",
        "strategy": (
            "Limited budget and spending appetite. Keep engagement costs low — email newsletters, "
            "discount coupons, and value-for-money product lines. Do not over-invest in this segment; "
            "focus on low-cost digital campaigns. Monitor for signals of income growth "
            "that may move them to a higher-value segment over time."
        ),
    },
    4: {
        "title":    "Cluster 4 — Regular Customers",
        "badge":    "⭐ Medium Income · Medium Spending",
        "color":    "#059669",
        "bg":       "#f0fdf4",
        "strategy_title": "Loyalty & Cross-Sell",
        "strategy": (
            "Your steady backbone segment. Nurture loyalty with membership programs, "
            "reward points, and consistent value. Cross-sell and upsell through "
            "targeted recommendations based on purchase history. "
            "Seasonal promotions and referral bonuses work well here. "
            "Goal: gradually shift them toward the High Value cluster."
        ),
    },
}

st.markdown("""
<div class="page-header">
    <h1>💡 Business Insights</h1>
    <p>Per-cluster analysis — customer count, average metrics and suggested marketing strategies</p>
</div>
""", unsafe_allow_html=True)

# ── Summary KPIs ──────────────────────────────────────────────────────────────
cols = st.columns(5)
for i in range(5):
    meta  = CLUSTER_META[i]
    count = (df["Cluster"] == i).sum()
    avg_i = df.loc[df["Cluster"] == i, "Annual Income (k$)"].mean()
    avg_s = df.loc[df["Cluster"] == i, "Spending Score (1-100)"].mean()
    with cols[i]:
        st.markdown(f"""
        <div style="background:{meta['bg']};border-radius:14px;padding:1.1rem;
                    border-left:5px solid {meta['color']};text-align:center;">
            <div style="font-size:1.5rem;margin-bottom:.3rem;">{meta['badge'].split()[0]}</div>
            <div style="font-size:1.5rem;font-weight:700;color:{meta['color']};">{count}</div>
            <div style="font-size:.72rem;color:#64748b;text-transform:uppercase;
                        letter-spacing:.05em;font-weight:600;">Cluster {i}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Insight cards (one per cluster) ──────────────────────────────────────────
for i in range(5):
    meta  = CLUSTER_META[i]
    mask  = df["Cluster"] == i
    count = mask.sum()
    avg_i = df.loc[mask, "Annual Income (k$)"].mean()
    avg_s = df.loc[mask, "Spending Score (1-100)"].mean()
    avg_a = df.loc[mask, "Age"].mean()

    st.markdown(f"""
    <div class="insight-box" style="background:{meta['bg']};border-color:{meta['color']};">
        <div class="ins-title" style="color:{meta['color']};">{meta['title']}</div>
        <div style="display:inline-block;background:{meta['color']};color:white;
                    font-size:.75rem;font-weight:600;padding:.2rem .75rem;
                    border-radius:999px;margin-bottom:.7rem;">{meta['badge']}</div>
        <div class="ins-row">👥 <b>Customer Count:</b> {count}</div>
        <div class="ins-row">💰 <b>Average Annual Income:</b> ${avg_i:.1f}k</div>
        <div class="ins-row">🛍️ <b>Average Spending Score:</b> {avg_s:.1f} / 100</div>
        <div class="ins-row">🎂 <b>Average Age:</b> {avg_a:.1f} years</div>
        <div class="strategy">
            <div class="strategy-title">📌 Suggested Marketing Strategy — {meta['strategy_title']}</div>
            {meta['strategy']}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Comparison bar charts ─────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### 📊 Cluster Comparison")

summary = df.groupby("Cluster").agg(
    Count=("CustomerID", "count"),
    Avg_Income=("Annual Income (k$)", "mean"),
    Avg_Spending=("Spending Score (1-100)", "mean"),
    Avg_Age=("Age", "mean")
).round(1).reset_index()
summary["Segment"] = summary["Cluster"].apply(
    lambda x: CLUSTER_META[x]["title"].split("—")[1].strip()
)

COLORS = [CLUSTER_META[i]["color"] for i in range(5)]

tab1, tab2, tab3 = st.tabs(["Avg Income", "Avg Spending Score", "Cluster Size"])

with tab1:
    fig = px.bar(summary, x="Segment", y="Avg_Income",
                 color="Segment", color_discrete_sequence=COLORS,
                 text="Avg_Income", template="plotly_white",
                 title="Average Annual Income per Cluster")
    fig.update_traces(texttemplate="$%{text}k", textposition="outside",
                      marker_line_color="white", marker_line_width=1)
    fig.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=60,l=10,r=10), height=360)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig2 = px.bar(summary, x="Segment", y="Avg_Spending",
                  color="Segment", color_discrete_sequence=COLORS,
                  text="Avg_Spending", template="plotly_white",
                  title="Average Spending Score per Cluster")
    fig2.update_traces(texttemplate="%{text}", textposition="outside",
                       marker_line_color="white", marker_line_width=1)
    fig2.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=60,l=10,r=10), height=360)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fig3 = px.pie(summary, names="Segment", values="Count",
                  color_discrete_sequence=COLORS, hole=0.45,
                  template="plotly_white", title="Customer Distribution Across Clusters")
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=10,l=10,r=10),
                       legend=dict(orientation="h", y=-0.15))
    fig3.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig3, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Cluster summary table + export ────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### 📋 Cluster Summary Table")

summary["Marketing Strategy"] = summary["Cluster"].apply(
    lambda x: CLUSTER_META[x]["strategy_title"]
)
st.dataframe(
    summary[["Cluster","Segment","Count","Avg_Income","Avg_Spending","Avg_Age","Marketing Strategy"]]
    .style.background_gradient(subset=["Avg_Income","Avg_Spending"], cmap="YlGn")
          .format({"Avg_Income":"{:.1f}", "Avg_Spending":"{:.1f}", "Avg_Age":"{:.1f}"}),
    use_container_width=True
)

full_export = df[["CustomerID","Gender","Age","Annual Income (k$)","Spending Score (1-100)","Cluster"]]
full_export = full_export.copy()
full_export["Segment"] = full_export["Cluster"].map(
    {k: v["title"].split("—")[1].strip() for k, v in CLUSTER_META.items()}
)
full_export["Marketing Strategy"] = full_export["Cluster"].map(
    {k: v["strategy_title"] for k, v in CLUSTER_META.items()}
)

st.download_button(
    label="📥 Download Full Insights CSV",
    data=full_export.to_csv(index=False).encode("utf-8"),
    file_name="customer_insights.csv",
    mime="text/csv"
)
st.markdown('</div>', unsafe_allow_html=True)
