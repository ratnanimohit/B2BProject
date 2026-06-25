import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_custom_css, THEME

st.set_page_config(layout="wide", page_title="Reports - AcademiaCRM", page_icon="📈")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("Reports")
st.markdown("### Performance & Conversion Analytics")

c1, c2 = st.columns(2)

with c1:
    st.markdown(f'<div style="background-color: {THEME["card_color"]}; padding: 20px; border-radius: 8px;"><h4>Lead Source Performance</h4></div>', unsafe_allow_html=True)
    df_pie = pd.DataFrame({'Source': ['LinkedIn', 'Referral', 'Website Form', 'Event', 'Cold Email'], 'Count': [45, 30, 25, 15, 33]})
    fig1 = px.pie(df_pie, values='Count', names='Source', hole=0.4, color_discrete_sequence=[THEME['accent_blue'], THEME['accent_green'], THEME['accent_yellow'], THEME['accent_purple'], THEME['accent_cyan']])
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=THEME['text_color'], margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown(f'<div style="background-color: {THEME["card_color"]}; padding: 20px; border-radius: 8px;"><h4>Revenue by Program</h4></div>', unsafe_allow_html=True)
    df_bar = pd.DataFrame({'Program': ['Data Science', 'Cloud & DevOps', 'Web Dev', 'Cybersecurity', 'AI/ML'], 'Revenue': ['120k', '95k', '110k', '80k', '140k']})
    df_bar['Revenue_Num'] = [120, 95, 110, 80, 140]
    fig2 = px.bar(df_bar, x='Program', y='Revenue_Num', color='Program', color_discrete_sequence=[THEME['accent_indigo'], THEME['accent_blue'], THEME['accent_cyan'], THEME['accent_green'], THEME['accent_yellow']])
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=THEME['text_color'], margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
