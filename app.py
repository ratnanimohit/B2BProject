import streamlit as st
import os

# 1. Set Page Config (Must be first)
st.set_page_config(layout="wide", page_title="AcademiaCRM", page_icon="🎓")

# Imports
from config import get_custom_css, THEME
from database.sqlite_db import init_db
from database.mongo_db import get_client
from models.train_scorer import train_and_save_model
from models.lead_scorer import get_model
from ai_engine.automation import check_overdue_followups

def initialize_app():
    # 2. Init SQLite
    init_db()
    # 3. Verify Mongo
    get_client()
    # 4. Train model if missing
    train_and_save_model()

initialize_app()

# CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# 6. Check overdue
overdue_tasks = check_overdue_followups()
overdue_count = len(overdue_tasks)

# Layout: Sidebar
with st.sidebar:
    st.markdown(f"""
        <div style="background-color: {THEME['accent_indigo']}; padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 20px;">
            <h2 style="margin:0; color: white;">AcademiaCRM</h2>
        </div>
    """, unsafe_allow_html=True)

    # st.page_link doesn't allow custom styles easily, so we use it as is but wrap pages
    st.page_link("pages/dashboard.py", label="Dashboard", icon="📊")
    st.page_link("pages/leads.py", label="Leads", icon="👥")
    st.page_link("pages/ai_insights.py", label="AI Insights", icon="🧠")
    st.page_link("pages/follow_ups.py", label="Follow-Ups", icon="📅")
    st.page_link("pages/reports.py", label="Reports", icon="📈")
    st.write("---")
    st.write("⚙️ Settings")

    st.write("")
    st.write("")
    if overdue_count > 0:
        st.markdown(f"""
            <div style="background-color: rgba(239, 68, 68, 0.2); border: 1px solid {THEME['accent_red']}; padding: 10px; border-radius: 8px; text-align: center;">
                <span style="color: {THEME['accent_red']}; font-weight: bold;">🔴 {overdue_count} Overdue Tasks</span>
            </div>
        """, unsafe_allow_html=True)

# Redirect to dashboard on initial load if no page selected
# Since Streamlit handles multi-page via the pages/ directory natively,
# running `app.py` acts as the entry point. We can put a welcome message here
# or redirect. For now, just a simple welcome.
st.markdown("## Welcome to AcademiaCRM")
st.write("Select a page from the sidebar to begin.")
