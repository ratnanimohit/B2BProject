import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_custom_css, THEME
from database.sqlite_db import get_all_institutions

st.set_page_config(layout="wide", page_title="Leads - AcademiaCRM", page_icon="👥")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("Institution Leads")
st.caption("Manage and track all college & university leads")

col_f1, col_f2 = st.columns([4, 1])
with col_f1:
    filter_status = st.radio("Filter", ['All Status', 'New Lead', 'Contacted', 'Meeting Scheduled', 'Proposal Sent', 'Closed'], horizontal=True, label_visibility="collapsed")
with col_f2:
    if st.button("+ Add Lead", type="primary"):
        st.info("Add Lead modal triggered. (Implement via Streamlit dialog)")

st.write("")

institutions = get_all_institutions()

if filter_status != 'All Status':
    institutions = [i for i in institutions if i['lead_status'] == filter_status]

html_table = f'<table style="width:100%; border-collapse: collapse; color: {THEME["text_color"]};"><tr style="border-bottom: 1px solid {THEME["card_color"]}; color: {THEME["muted_text"]}; text-align: left;"><th style="padding: 10px;">Institution</th><th style="padding: 10px;">Location</th><th style="padding: 10px;">Contact</th><th style="padding: 10px;">Program Interest</th><th style="padding: 10px;">Status</th><th style="padding: 10px;">Score</th><th style="padding: 10px;">Action</th></tr>'

for i, inst in enumerate(institutions):
    bg = THEME['card_color'] if i % 2 == 0 else THEME['bg_color']
    score = inst.get('priority_score', 0)
    score_color = THEME['accent_green'] if score >= 80 else THEME['accent_yellow'] if score >= 60 else THEME['accent_red']
    status_colors = {
        'New Lead': THEME['accent_blue'],
        'Contacted': THEME['accent_cyan'],
        'Meeting Scheduled': THEME['accent_green'],
        'Proposal Sent': THEME['accent_yellow'],
        'Negotiation': THEME['accent_purple'],
        'Closed': THEME['accent_green'],
    }
    s_col = status_colors.get(inst['lead_status'], THEME['muted_text'])
    
    row_html = f'<tr style="background-color: {bg}; border-bottom: 1px solid {THEME["card_color"]};"><td style="padding: 15px;"><div style="display: flex; align-items: center;"><div style="width: 30px; height: 30px; border-radius: 50%; background-color: {THEME["accent_indigo"]}; margin-right: 10px;"></div><b>{inst["name"]}</b></div></td><td style="padding: 15px; color: {THEME["muted_text"]}; font-size: 0.9rem;">{inst["location"]}</td><td style="padding: 15px;">{inst["contact_person"]}</td><td style="padding: 15px; color: {THEME["muted_text"]};">{inst["program_interest"]}</td><td style="padding: 15px;"><span style="background-color: rgba({int(s_col[1:3],16)},{int(s_col[3:5],16)},{int(s_col[5:7],16)},0.2); color: {s_col}; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem;">{inst["lead_status"]}</span></td><td style="padding: 15px;"><div style="display: flex; align-items: center;"><div style="width: 10px; height: 10px; border-radius: 50%; background-color: {score_color}; margin-right: 5px;"></div><b>{int(score)}</b></div></td><td style="padding: 15px;"><button style="background-color: {THEME["accent_blue"]}; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; margin-right: 5px;">Edit</button><button style="background-color: {THEME["accent_purple"]}; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer;">AI</button></td></tr>'
    html_table += row_html

html_table += "</table>"
st.markdown(html_table, unsafe_allow_html=True)

st.write("")
st.caption(f"Showing {len(institutions)} of 148 institutions (mocked total)")
