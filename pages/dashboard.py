import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_custom_css, THEME
from database.sqlite_db import get_all_institutions
from ai_engine.intelligence import get_lead_priority_score

st.set_page_config(layout="wide", page_title="Dashboard - AcademiaCRM", page_icon="📊")
st.markdown(get_custom_css(), unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.title("Dashboard")
    st.caption("Overview of your academia sales pipeline")
with col2:
    st.text_input("Search institutions...", placeholder="Search...")
    st.markdown("<div style='text-align: right; margin-top: -30px;'><b>AK</b></div>", unsafe_allow_html=True)

institutions = get_all_institutions()

total_institutions = len(institutions)
active_leads = sum(1 for i in institutions if i['lead_status'] not in ['Closed', 'Lost'])
high_priority = sum(1 for i in institutions if i.get('priority_score', 0) >= 80)
meetings_sched = sum(1 for i in institutions if i['lead_status'] == 'Meeting Scheduled')
proposals_sent = sum(1 for i in institutions if i['lead_status'] == 'Proposal Sent')

m1, m2, m3, m4 = st.columns(4)
with m1:
    html_m1 = f'<div style="background-color: {THEME["card_color"]}; padding: 20px; border-radius: 8px; border-top: 4px solid {THEME["accent_blue"]};"><p style="color: {THEME["muted_text"]}; margin: 0;">Total Institutions</p><h2 style="margin: 0; padding: 10px 0;">{total_institutions}</h2><span style="background-color: rgba(79, 142, 247, 0.2); color: {THEME["accent_blue"]}; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem;">+12 this month</span></div>'
    st.markdown(html_m1, unsafe_allow_html=True)

with m2:
    html_m2 = f'<div style="background-color: {THEME["card_color"]}; padding: 20px; border-radius: 8px; border-top: 4px solid {THEME["accent_yellow"]};"><p style="color: {THEME["muted_text"]}; margin: 0;">Active Leads</p><h2 style="margin: 0; padding: 10px 0;">{active_leads}</h2><span style="background-color: rgba(245, 158, 11, 0.2); color: {THEME["accent_yellow"]}; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem;">{high_priority} high priority</span></div>'
    st.markdown(html_m2, unsafe_allow_html=True)

with m3:
    html_m3 = f'<div style="background-color: {THEME["card_color"]}; padding: 20px; border-radius: 8px; border-top: 4px solid {THEME["accent_green"]};"><p style="color: {THEME["muted_text"]}; margin: 0;">Meetings Scheduled</p><h2 style="margin: 0; padding: 10px 0;">{meetings_sched}</h2><span style="background-color: rgba(34, 197, 94, 0.2); color: {THEME["accent_green"]}; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem;">5 this week</span></div>'
    st.markdown(html_m3, unsafe_allow_html=True)

with m4:
    html_m4 = f'<div style="background-color: {THEME["card_color"]}; padding: 20px; border-radius: 8px; border-top: 4px solid {THEME["accent_purple"]};"><p style="color: {THEME["muted_text"]}; margin: 0;">Proposals Sent</p><h2 style="margin: 0; padding: 10px 0;">{proposals_sent}</h2><span style="background-color: rgba(168, 85, 247, 0.2); color: {THEME["accent_purple"]}; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem;">11 in negotiation</span></div>'
    st.markdown(html_m4, unsafe_allow_html=True)

st.write("")

r2c1, r2c2 = st.columns([2, 3])

with r2c1:
    st.markdown("### Sales Pipeline")
    statuses = ['New Lead', 'Contacted', 'Meeting Scheduled', 'Proposal Sent', 'Negotiation', 'Closed']
    counts = {s: 0 for s in statuses}
    for i in institutions:
        if i['lead_status'] in counts:
            counts[i['lead_status']] += 1
    
    counts = {'New Lead': 148, 'Contacted': 89, 'Meeting Scheduled': 63, 'Proposal Sent': 34, 'Negotiation': 18, 'Closed': 11}
    
    fig = go.Figure(go.Funnel(y=list(counts.keys()), x=list(counts.values()), textinfo="value", marker={"color": [THEME['accent_blue'], THEME['accent_cyan'], THEME['accent_green'], THEME['accent_yellow'], THEME['accent_purple'], THEME['accent_indigo']]}))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=THEME['text_color'], margin=dict(t=0, l=0, r=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

with r2c2:
    col_ai_h1, col_ai_h2 = st.columns([4, 1])
    with col_ai_h1:
        st.markdown("### AI Lead Intelligence")
    with col_ai_h2:
        st.markdown("<div class='pill-high' style='text-align: center;'>Live</div>", unsafe_allow_html=True)
    
    sorted_insts = sorted(institutions, key=lambda x: x.get('priority_score', 0), reverse=True)[:5]
    
    for i in sorted_insts:
        score = i.get('priority_score', 0)
        color = THEME['accent_green'] if score >= 80 else THEME['accent_yellow'] if score >= 60 else THEME['accent_red']
        priority = "HIGH" if score >= 80 else "MED" if score >= 60 else "LOW"
        pill_class = "pill-high" if score >= 80 else "pill-med" if score >= 60 else "pill-low"
        
        html_feed = f'<div style="background-color: {THEME["card_color"]}; padding: 15px; border-radius: 8px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;"><div style="display: flex; align-items: center;"><div style="width: 40px; height: 40px; border-radius: 50%; background-color: {color}; color: black; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 15px;">{int(score)}</div><div><div style="font-weight: bold;">{i["name"]}</div><div style="color: {THEME["muted_text"]}; font-size: 0.9rem;">{i["student_strength"]}+ students · {i["program_interest"]}</div></div></div><div class="{pill_class}">{priority}</div></div>'
        st.markdown(html_feed, unsafe_allow_html=True)

st.write("")

r3c1, r3c2 = st.columns(2)

with r3c1:
    st.markdown("### Lead & Conversion Trend")
    df = pd.DataFrame({'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], 'Leads': [45, 52, 48, 70, 85, 110], 'Closed': [5, 8, 12, 15, 18, 25]})
    fig2 = px.line(df, x='Month', y=['Leads', 'Closed'], markers=True, color_discrete_sequence=[THEME['accent_blue'], THEME['accent_green']])
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=THEME['text_color'], legend_title="", margin=dict(t=0, l=0, r=0, b=0))
    st.plotly_chart(fig2, use_container_width=True)

with r3c2:
    st.markdown("### Upcoming Follow-Ups")
    tasks = [
        {"inst": "GLA University", "action": "Send Proposal", "due": "Today", "color": THEME['accent_red']},
        {"inst": "Amity Delhi", "action": "Schedule Demo Call", "due": "Tomorrow", "color": THEME['accent_yellow']},
        {"inst": "Lovely Pro Univ", "action": "Follow-up Email", "due": "Jun 27", "color": THEME['accent_blue']},
        {"inst": "KIIT Bhubaneswar", "action": "Intro Call", "due": "Jun 28", "color": THEME['accent_green']},
        {"inst": "SRM Chennai", "action": "Share Brochure", "due": "Jun 29", "color": THEME['accent_purple']}
    ]
    for t in tasks:
        pill_style = f"background-color: rgba({int(t['color'][1:3], 16)}, {int(t['color'][3:5], 16)}, {int(t['color'][5:7], 16)}, 0.2); color: {t['color']}; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: bold;"
        html_task = f'<div style="background-color: {THEME["card_color"]}; padding: 12px; border-radius: 8px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;"><div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; border-radius: 50%; background-color: {t["color"]}; margin-right: 15px;"></div><div><div style="font-weight: bold;">{t["inst"]}</div><div style="color: {THEME["muted_text"]}; font-size: 0.8rem;">{t["action"]}</div></div></div><div style="{pill_style}">{t["due"]}</div></div>'
        st.markdown(html_task, unsafe_allow_html=True)
