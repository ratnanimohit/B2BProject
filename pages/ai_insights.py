import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_custom_css, THEME
from database.sqlite_db import get_all_institutions
from ai_engine.intelligence import get_lead_priority_score, get_next_best_action, generate_outreach_message, get_follow_up_suggestions, analyze_lead_reasoning

st.set_page_config(layout="wide", page_title="AI Insights - AcademiaCRM", page_icon="🧠")
st.markdown(get_custom_css(), unsafe_allow_html=True)

institutions = get_all_institutions()

col1, col2 = st.columns([3, 1])
with col1:
    selected_inst_name = st.selectbox("Select Institution", [i['name'] for i in institutions], label_visibility="collapsed")
with col2:
    st.button("Analyze Lead", type="primary", use_container_width=True)

selected_inst = next((i for i in institutions if i['name'] == selected_inst_name), None)

if selected_inst:
    st.markdown(f"### {selected_inst['name']} — {selected_inst['location']}")
    st.caption(f"{selected_inst['student_strength']}+ students | {selected_inst['institution_type']}")
    st.write("")

    score = selected_inst.get('priority_score', get_lead_priority_score(selected_inst))
    score_color = THEME['accent_green'] if score >= 80 else THEME['accent_yellow'] if score >= 60 else THEME['accent_red']
    priority_text = "HIGH PRIORITY" if score >= 80 else "MEDIUM PRIORITY" if score >= 60 else "LOW PRIORITY"
    
    action = get_next_best_action(score)
    msg = generate_outreach_message(selected_inst).replace('\n', '<br>')
    suggestions = get_follow_up_suggestions(selected_inst)
    reasoning = analyze_lead_reasoning(selected_inst, score)

    r1c1, r1c2 = st.columns([1, 1])
    
    with r1c1:
        html1 = f'<div style="background-color: {THEME["card_color"]}; padding: 20px; border-radius: 8px; height: 100%;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;"><h3 style="margin: 0;">Priority Score</h3><span style="background-color: rgba(34, 197, 94, 0.2); color: {THEME["accent_green"]}; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem;">+31 vs avg</span></div><div style="display: flex; margin-bottom: 30px;"><div style="width: 120px; height: 120px; border-radius: 50%; border: 8px solid {score_color}; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-right: 30px;"><h1 style="margin: 0; color: {score_color};">{int(score)}</h1></div><div><h4 style="color: {score_color}; margin: 10px 0 5px 0;">{priority_text}</h4><div style="color: {THEME["muted_text"]}; font-size: 0.9rem;">AI Confidence: 92%</div></div></div><h4 style="margin-bottom: 10px;">Score Breakdown</h4><div style="margin-bottom: 8px;"><div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 4px;"><span>Student Strength</span><span>92%</span></div><div style="width: 100%; background-color: {THEME["bg_color"]}; height: 8px; border-radius: 4px;"><div style="width: 92%; background-color: {THEME["accent_green"]}; height: 100%; border-radius: 4px;"></div></div></div><div style="margin-bottom: 8px;"><div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 4px;"><span>Program Match</span><span>85%</span></div><div style="width: 100%; background-color: {THEME["bg_color"]}; height: 8px; border-radius: 4px;"><div style="width: 85%; background-color: {THEME["accent_green"]}; height: 100%; border-radius: 4px;"></div></div></div><div style="margin-bottom: 8px;"><div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 4px;"><span>Lead Source</span><span>80%</span></div><div style="width: 100%; background-color: {THEME["bg_color"]}; height: 8px; border-radius: 4px;"><div style="width: 80%; background-color: {THEME["accent_blue"]}; height: 100%; border-radius: 4px;"></div></div></div><div style="margin-top: 20px; background-color: {THEME["bg_color"]}; padding: 15px; border-radius: 8px; border-left: 4px solid {THEME["accent_purple"]};"><p style="margin: 0; font-size: 0.9rem; color: {THEME["muted_text"]};"><b>AI Reasoning:</b> {reasoning}</p></div></div>'
        st.markdown(html1, unsafe_allow_html=True)
        
    with r1c2:
        html2 = f'<div style="background-color: {THEME["card_color"]}; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-top: 4px solid {THEME["accent_indigo"]};"><h3 style="margin-top: 0;">Next Best Action</h3><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;"><div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; border-radius: 50%; background-color: {THEME["accent_green"]}; margin-right: 15px;"></div><div><div style="font-weight: bold; font-size: 1.1rem;">Schedule Demo Call</div><div style="color: {THEME["muted_text"]}; font-size: 0.9rem;">Priority action — within 48h</div></div></div><span class="pill-high">HIGH</span></div><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;"><div style="display: flex; align-items: center;"><div style="width: 12px; height: 12px; border-radius: 50%; background-color: {THEME["accent_yellow"]}; margin-right: 15px;"></div><div><div style="font-weight: bold; font-size: 1.1rem;">Send Custom Proposal</div><div style="color: {THEME["muted_text"]}; font-size: 0.9rem;">Tailor to Data Science interest</div></div></div><span class="pill-med">NOW</span></div></div><div style="background-color: {THEME["card_color"]}; padding: 20px; border-radius: 8px; border-top: 4px solid {THEME["accent_blue"]};"><div style="display: flex; justify-content: space-between; align-items: center;"><h3 style="margin-top: 0;">Personalized Outreach</h3><span style="background-color: rgba(168, 85, 247, 0.2); color: {THEME["accent_purple"]}; padding: 4px 8px; border-radius: 12px; font-size: 0.7rem;">AI-Gen</span></div><p style="color: {THEME["accent_blue"]}; font-weight: bold; margin-bottom: 5px;">Subject: Partnership Opportunity - {selected_inst["program_interest"]}</p><div style="background-color: {THEME["bg_color"]}; padding: 15px; border-radius: 8px; font-size: 0.9rem; color: {THEME["muted_text"]}; margin-bottom: 15px;">{msg}</div><div style="display: flex; gap: 10px;"><button style="flex: 1; background-color: transparent; border: 1px solid {THEME["accent_blue"]}; color: {THEME["accent_blue"]}; padding: 8px; border-radius: 4px; cursor: pointer;">Copy</button><button style="flex: 2; background-color: {THEME["accent_blue"]}; border: none; color: white; padding: 8px; border-radius: 4px; cursor: pointer;">Send Email</button></div></div>'
        st.markdown(html2, unsafe_allow_html=True)

    st.write("")
    st.markdown("### Follow-Up Suggestions")
    
    s_cols = st.columns(3)
    colors = [THEME['accent_cyan'], THEME['accent_green'], THEME['accent_yellow']]
    
    for idx, (col, sug) in enumerate(zip(s_cols, suggestions)):
        with col:
            html_sug = f'<div style="background-color: {THEME["card_color"]}; padding: 0; border-radius: 8px; overflow: hidden; height: 100%; display: flex; flex-direction: column;"><div style="background-color: {colors[idx]}; height: 30px; display: flex; align-items: center; justify-content: center; color: black; font-weight: bold;">{idx + 1}</div><div style="padding: 20px; flex: 1; display: flex; flex-direction: column;"><h4 style="margin-top: 0;">{sug["title"]}</h4><p style="color: {THEME["muted_text"]}; font-size: 0.9rem; flex: 1;">{sug["desc"]}</p><p style="color: {colors[idx]}; font-size: 0.8rem; font-weight: bold; margin-bottom: 15px;">{sug["meta"]}</p><button style="background-color: transparent; border: 1px solid {colors[idx]}; color: {colors[idx]}; padding: 8px; border-radius: 4px; cursor: pointer; width: 100%;">Execute Action</button></div></div>'
            st.markdown(html_sug, unsafe_allow_html=True)
