import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_custom_css, THEME

st.set_page_config(layout="wide", page_title="Follow-Ups - AcademiaCRM", page_icon="📅")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("Follow-Ups")
st.markdown("### Manage Scheduled Actions")
st.info("Here you will find a list of all your scheduled follow-ups, calls, and email drip sequences.")

html_content = f'<div style="background-color: {THEME["card_color"]}; padding: 20px; border-radius: 8px; margin-top: 20px;"><div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid {THEME["bg_color"]}; padding-bottom: 15px; margin-bottom: 15px;"><div><h4 style="margin: 0;">Follow-up Call with Dr. Sharma</h4><p style="color: {THEME["muted_text"]}; margin: 5px 0 0 0;">GLA University - Data Science</p></div><span style="background-color: rgba(239, 68, 68, 0.2); color: {THEME["accent_red"]}; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.8rem;">Today</span></div><div style="display: flex; align-items: center; justify-content: space-between;"><div><h4 style="margin: 0;">Send Proposal</h4><p style="color: {THEME["muted_text"]}; margin: 5px 0 0 0;">Amity Delhi - Cloud & DevOps</p></div><span style="background-color: rgba(245, 158, 11, 0.2); color: {THEME["accent_yellow"]}; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.8rem;">Tomorrow</span></div></div>'
st.markdown(html_content, unsafe_allow_html=True)
