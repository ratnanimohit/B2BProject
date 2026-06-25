# 🎓 AcademiaCRM

**AcademiaCRM** is a complete AI-powered B2B Sales CRM system designed specifically for educational partnerships, university outreach, and academia sales. 

Built with a sleek, custom **Dark Navy UI** in Streamlit, the platform leverages a custom **PyTorch Neural Network** to intelligently score incoming institutional leads and recommend the next best action, helping your sales team close high-value partnerships faster.

---

## 🚀 Key Features

* **🧠 AI Lead Intelligence**: A built-in PyTorch model automatically scores leads (0-100) based on student strength, program interest match, prior partnerships, and more.
* **📊 Sales Pipeline Dashboard**: Visualizes your entire pipeline from 'New Lead' to 'Closed' using Plotly charts.
* **✉️ Automated Outreach Gen**: Uses lead context to auto-generate personalized email templates.
* **📅 Smart Follow-ups**: Automatically surfaces priority actions, ensuring no high-value institution falls through the cracks.
* **🗄️ Dual-Database Architecture**:
  * **SQLite** for robust, structured CRM tracking (leads, statuses, tasks).
  * **MongoDB** hooks built-in for unstructured event logging and activity feeds.

---

## 🛠️ Tech Stack

* **Frontend & UI**: Python, Streamlit, Plotly (Custom CSS Dark Theme)
* **AI Engine**: PyTorch, Scikit-Learn
* **Databases**: SQLite3 (Primary), PyMongo (Secondary/Logging)
* **Data Manipulation**: Pandas, Numpy

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/zoyausmani40-stacks/academia_crm.git
   cd academia_crm
   ```

2. **Install dependencies**
   Ensure you have Python 3.10+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Start MongoDB**
   If you have MongoDB installed locally, ensure it is running on `mongodb://localhost:27017` to enable the activity logging features. *If you don't have MongoDB, the app will fail gracefully and still function entirely using SQLite.*

4. **Launch the CRM**
   ```bash
   streamlit run app.py
   ```

---

## 🧠 How the AI Works

On the very first launch, the CRM will run `train_scorer.py` in the background. 
This script:
1. Generates a synthetic dataset of 500 institutional leads.
2. Trains a 4-layer fully connected Neural Network (`LeadScorerNet`) over 100 epochs.
3. Saves the model weights to `lead_scorer.pt`.

Whenever a lead is viewed in the **AI Insights** tab, the CRM runs inference in real-time to compute the priority score and deduce the *Next Best Action*.

---

## 📸 Project Structure

```text
academia_crm/
├── app.py                      # Main Streamlit Entry Point
├── config.py                   # Theme & DB configurations
├── seed_data.py                # Auto-populates 20 sample universities
├── requirements.txt            
├── database/
│   ├── sqlite_db.py            # SQLite CRUD & Schema
│   └── mongo_db.py             # MongoDB Activity Hooks
├── models/
│   ├── lead_scorer.py          # PyTorch Model Architecture
│   └── train_scorer.py         # Training Script & Data Gen
├── ai_engine/
│   ├── intelligence.py         # Inference & Scoring Rules
│   └── automation.py           # Follow-up logic
└── pages/
    ├── dashboard.py            # KPI & Funnel Dashboard
    ├── leads.py                # Lead Management Table
    ├── ai_insights.py          # Deep Dive Lead Analysis
    ├── follow_ups.py           # Scheduled Tasks
    └── reports.py              # Analytics & Conversions
```

---
*Built with Python 🐍 + Streamlit 🎈 + PyTorch 🔥*
