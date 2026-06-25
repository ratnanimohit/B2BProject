import os

# Database configurations
SQLITE_DB_PATH = "academia_crm.db"
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/academia_crm")
MONGO_DB_NAME = "academia_crm"

# Theme Colors (Dark Navy Theme)
THEME = {
    "bg_color": "#0B0E1A",
    "sidebar_color": "#111526",
    "card_color": "#161B2E",
    "text_color": "#FFFFFF",
    "muted_text": "#9CA3AF",
    "accent_blue": "#4F8EF7",
    "accent_indigo": "#6366F1",
    "accent_green": "#22C55E",
    "accent_yellow": "#F59E0B",
    "accent_red": "#EF4444",
    "accent_purple": "#A855F7",
    "accent_cyan": "#06B6D4"
}

# Streamlit custom CSS
def get_custom_css():
    return f"""
    <style>
    /* Global background */
    .stApp {{
        background-color: {THEME['bg_color']};
        color: {THEME['text_color']};
    }}
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {THEME['sidebar_color']};
    }}
    /* Cards/Containers */
    div[data-testid="stMetric"], div[data-testid="stExpander"] {{
        background-color: {THEME['card_color']};
        padding: 1rem;
        border-radius: 8px;
    }}
    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: {THEME['text_color']} !important;
    }}
    /* Status Pills */
    .pill-high {{
        background-color: rgba(34, 197, 94, 0.2);
        color: {THEME['accent_green']};
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }}
    .pill-med {{
        background-color: rgba(245, 158, 11, 0.2);
        color: {THEME['accent_yellow']};
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }}
    .pill-low {{
        background-color: rgba(239, 68, 68, 0.2);
        color: {THEME['accent_red']};
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }}
    </style>
    """
