import sqlite3
import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.sqlite_db import get_connection, init_db

def seed():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM institutions")
    if cursor.fetchone()[0] > 0:
        print("Data already seeded.")
        conn.close()
        return

    sample_institutions = [
        ("GLA University", "Mathura, UP", "Uttar Pradesh", "University", 12000, "Dr. R. Sharma", "r.sharma@gla.ac.in", "9876543210", "Data Science, Python Bootcamp", "LinkedIn", "New Lead", "Amit Kumar", 94.0),
        ("Amity Delhi", "Delhi NCR", "Delhi", "University", 25000, "Prof. K. Mehta", "k.mehta@amity.edu", "9876543211", "Cloud & DevOps", "Website Form", "Contacted", "Priya Singh", 87.0),
        ("MIT Manipal", "Manipal, KA", "Karnataka", "University", 15000, "Dr. P. Nair", "p.nair@manipal.edu", "9876543212", "Full Stack Web Dev", "Referral", "Meeting Scheduled", "Amit Kumar", 74.0),
        ("KIIT Bhubaneswar", "Bhubaneswar, OR", "Odisha", "University", 20000, "Mr. S. Das", "s.das@kiit.ac.in", "9876543213", "Cybersecurity", "Cold Email", "Proposal Sent", "Rahul Verma", 61.0),
        ("SRM Chennai", "Chennai, TN", "Tamil Nadu", "University", 30000, "Ms. R. Iyer", "r.iyer@srm.ac.in", "9876543214", "AI/ML Workshop", "LinkedIn", "Negotiation", "Priya Singh", 88.0),
        ("Lovely Professional University", "Phagwara, PB", "Punjab", "University", 35000, "Dr. A. Singh", "a.singh@lpu.co.in", "9876543215", "Data Science", "Event", "New Lead", "Rahul Verma", 52.0),
        ("VIT Vellore", "Vellore, TN", "Tamil Nadu", "University", 25000, "Prof. M. Raj", "m.raj@vit.ac.in", "9876543216", "Full Stack Web Dev", "Cold Call", "Contacted", "Amit Kumar", 45.0),
        ("Manipal Jaipur", "Jaipur, RJ", "Rajasthan", "University", 10000, "Dr. C. Patel", "c.patel@jaipur.manipal.edu", "9876543217", "Cloud & DevOps", "Referral", "Closed", "Priya Singh", 91.0),
        ("Sharda University", "Greater Noida, UP", "Uttar Pradesh", "University", 12000, "Mr. V. Kumar", "v.kumar@sharda.ac.in", "9876543218", "Python Bootcamp", "Website Form", "New Lead", "Rahul Verma", 66.0),
        ("Chandigarh University", "Chandigarh", "Chandigarh", "University", 28000, "Ms. S. Kaur", "s.kaur@cu.edu.in", "9876543219", "Cybersecurity", "LinkedIn", "Meeting Scheduled", "Amit Kumar", 79.0),
        ("Symbiosis Pune", "Pune, MH", "Maharashtra", "University", 18000, "Dr. N. Joshi", "n.joshi@symbiosis.edu", "9876543220", "Data Science", "Referral", "Proposal Sent", "Priya Singh", 82.0),
        ("Thapar University", "Patiala, PB", "Punjab", "University", 9000, "Prof. G. Singh", "g.singh@thapar.edu", "9876543221", "AI/ML Workshop", "Event", "Negotiation", "Rahul Verma", 70.0),
        ("Bennett University", "Greater Noida, UP", "Uttar Pradesh", "University", 5000, "Mr. A. Gupta", "a.gupta@bennett.edu.in", "9876543222", "Cloud & DevOps", "Cold Email", "Closed", "Amit Kumar", 85.0),
        ("Christ University", "Bangalore, KA", "Karnataka", "University", 16000, "Dr. M. Thomas", "m.thomas@christuniversity.in", "9876543223", "Full Stack Web Dev", "Website Form", "Contacted", "Priya Singh", 68.0),
        ("Presidency College", "Chennai, TN", "Tamil Nadu", "College", 4000, "Prof. K. Raman", "k.raman@presidency.edu.in", "9876543224", "Python Bootcamp", "Referral", "New Lead", "Rahul Verma", 55.0),
        ("BITS Pilani", "Pilani, RJ", "Rajasthan", "University", 11000, "Dr. S. Reddy", "s.reddy@bits-pilani.ac.in", "9876543225", "AI/ML Workshop", "Event", "Meeting Scheduled", "Amit Kumar", 95.0),
        ("NIT Trichy", "Trichy, TN", "Tamil Nadu", "University", 8000, "Mr. T. Krishnan", "t.krishnan@nitt.edu", "9876543226", "Data Science", "LinkedIn", "Proposal Sent", "Priya Singh", 92.0),
        ("IIT Indore", "Indore, MP", "Madhya Pradesh", "University", 5000, "Prof. V. Sharma", "v.sharma@iiti.ac.in", "9876543227", "Cybersecurity", "Cold Call", "Negotiation", "Rahul Verma", 89.0),
        ("Jain University", "Bangalore, KA", "Karnataka", "University", 14000, "Dr. P. Hegde", "p.hegde@jainuniversity.ac.in", "9876543228", "Cloud & DevOps", "Website Form", "Contacted", "Amit Kumar", 63.0),
        ("PES University", "Bangalore, KA", "Karnataka", "University", 12000, "Ms. A. Rao", "a.rao@pes.edu", "9876543229", "Full Stack Web Dev", "Referral", "New Lead", "Priya Singh", 76.0)
    ]

    now = datetime.datetime.now().isoformat()
    for inst in sample_institutions:
        cursor.execute('''
            INSERT INTO institutions (
                name, location, state, institution_type, student_strength, 
                contact_person, email, phone, program_interest, lead_source, 
                lead_status, assigned_to, priority_score, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (*inst, now, now))
    
    conn.commit()
    print(f"Successfully seeded {len(sample_institutions)} institutions.")
    conn.close()

if __name__ == "__main__":
    seed()
