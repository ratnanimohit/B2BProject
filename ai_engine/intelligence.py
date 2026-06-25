import torch
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.lead_scorer import get_model
from models.train_scorer import MODEL_PATH

# Load model lazily
_model = None

def load_model():
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = get_model()
            _model.load_state_dict(torch.load(MODEL_PATH))
            _model.eval()
        else:
            print("Model not found. Train it first.")
    return _model

def get_lead_priority_score(institution_dict) -> float:
    model = load_model()
    if not model:
        return 50.0  # fallback
    
    # Simple heuristic to map dictionary fields to our 8 input features
    # This is a mock translation for demonstration purposes
    ss = min(institution_dict.get('student_strength', 5000) / 40000.0, 1.0)
    it_encoded = 1.0 if institution_dict.get('institution_type') == 'University' else 0.5
    has_prior = 1.0 if 'partnership' in institution_dict.get('notes', '').lower() else 0.0
    pi_match = 0.8  # dummy logic
    ls_score = 0.9 if institution_dict.get('lead_source') == 'Referral' else 0.6
    cs_score = 0.7  # dummy
    days_created = 0.1
    fu_count = 0.2
    
    input_tensor = torch.tensor([[ss, it_encoded, has_prior, pi_match, ls_score, cs_score, days_created, fu_count]], dtype=torch.float32)
    
    with torch.no_grad():
        output = model(input_tensor)
        
    score = output.item() * 100
    return round(score, 1)

def get_next_best_action(score: float) -> str:
    if score >= 80:
        return "Schedule demo call immediately"
    elif score >= 60:
        return "Send personalized proposal within 2 days"
    elif score >= 40:
        return "Send intro email and share brochure"
    else:
        return "Add to monthly newsletter drip"

def generate_outreach_message(institution_dict) -> str:
    contact = institution_dict.get('contact_person', 'Professor')
    name = institution_dict.get('name', 'your institution')
    program = institution_dict.get('program_interest', 'tech programs')
    
    return f"""Dear {contact},
    
I hope this message finds you well. I am reaching out regarding a tailored {program} designed specifically for {name}'s students.

Based on your current focus areas, I believe our training solutions could provide immense value to your student base.

Would you be open to a brief 10-minute introductory call next week?

Best regards,
AcademiaCRM Team"""

def get_follow_up_suggestions(institution_dict) -> list:
    return [
        {"title": "Send WhatsApp Follow-Up", "desc": "A quick message will re-engage.", "meta": "WhatsApp · Today"},
        {"title": "Schedule Campus Visit", "desc": "In-person demo closes 3x faster.", "meta": "Calendar · This Week"},
        {"title": "Share Success Case Study", "desc": "Share a case study with a similar profile.", "meta": "Email · Tomorrow"}
    ]

def analyze_lead_reasoning(institution_dict, score: float) -> str:
    ss = institution_dict.get('student_strength', 0)
    return f"{institution_dict.get('name')} has {ss}+ students. Based on their program interests and profile, the AI assigns a score of {score}. Recommend appropriate outreach."
