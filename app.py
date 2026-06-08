import streamlit as st

st.set_page_config(
    page_title="AI Customer Analytics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
[data-testid="stAppViewContainer"] { background: #f1f5f9; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1e40af, #7c3aed);
    color: white; border: none; border-radius: 10px;
    padding: .6rem 1.5rem; font-weight: 600;
}
[data-testid="stButton"] > button:hover { opacity: .85; color: white; }
.hero {
    background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
    padding: 2.5rem; border-radius: 18px; margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(30,64,175,.35);
}
.hero h1 { color: white !important; font-size: 2.2rem; font-weight: 700; margin: 0; }
.hero p  { color: rgba(255,255,255,.82); margin: .6rem 0 0; font-size: 1rem; }
.feat-card {
    background: white; border-radius: 16px; padding: 1.6rem;
    box-shadow: 0 2px 14px rgba(0,0,0,.07);
    border-top: 4px solid; height: 100%;
}
.feat-icon  { font-size: 2.4rem; margin-bottom: .6rem; }
.feat-title { font-size: 1.05rem; font-weight: 700; color: #1e293b; margin-bottom: .4rem; }
.feat-desc  { font-size: .85rem; color: #64748b; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="padding:1.4rem 1rem 1rem;border-bottom:1px solid #334155;margin-bottom:1rem;">
        <div style="font-size:2rem;">🤖</div>
        <div style="font-size:1.1rem;font-weight:700;margin-top:.3rem;">AI Customer Analytics</div>
        <div style="font-size:.73rem;color:#94a3b8;margin-top:.2rem;">K-Means Clustering System</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("**Navigate**")
    st.page_link("app.py",                 label="🏠  Home")
    st.page_link("pages/Dashboard.py",     label="📊  Dashboard")
    st.page_link("pages/Analytics.py",     label="🔍  Customer Analytics")
    st.page_link("pages/Segmentation.py",  label="🎯  Segmentation")
    st.page_link("pages/Insights.py",      label="💡  Business Insights")
    st.markdown("---")
    st.markdown("<div style='font-size:.73rem;color:#64748b;'>Dataset: Mall Customers<br>Model: K-Means (k=5)<br>Framework: Streamlit + Plotly</div>", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <h1>🤖 AI Driven Customer Analytics System</h1>
    <p>Intelligent customer segmentation using K-Means Clustering &nbsp;|&nbsp; Mall Customers Dataset</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
features = [
    ("#3b82f6", "📊", "Dashboard",         "KPI cards, demographics and spending overview."),
    ("#8b5cf6", "🔍", "Customer Analytics", "Gender, age, income and spending distributions."),
    ("#059669", "🎯", "Segmentation",       "Run K-Means, visualise clusters and download results."),
    ("#f59e0b", "💡", "Business Insights",  "Per-cluster marketing strategies and action plans."),
]
for col, (color, icon, title, desc) in zip([c1, c2, c3, c4], features):
    with col:
        st.markdown(f"""
        <div class="feat-card" style="border-color:{color};">
            <div class="feat-icon">{icon}</div>
            <div class="feat-title">{title}</div>
            <div class="feat-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.info("👈 Use the sidebar to navigate between pages.")
