import sqlite3

# Connect to your local database
conn = sqlite3.connect("drugs.db")
c = conn.cursor()

# --- 1. Insert sample drugs ---
sample_drugs = [
    ("Aspirin", "1191"),
    ("Paracetamol", "161"),
    ("Ibuprofen", "5640"),
    ("Amoxicillin", "723"),
    ("Metformin", "8606")
]

for drug in sample_drugs:
    try:
        c.execute("INSERT INTO drugs (name, rxnorm_id) VALUES (?, ?)", drug)
    except sqlite3.IntegrityError:
        pass  # skip duplicates

# --- 2. Insert demo drug interactions ---
demo_interactions = [
    ("Aspirin", "Ibuprofen", "Increased risk of bleeding", "High"),
    ("Aspirin", "Metformin", "Possible stomach irritation", "Medium"),
    ("Paracetamol", "Metformin", "No major interaction", "Low"),
    ("Ibuprofen", "Amoxicillin", "No major interaction", "Low"),
    ("Paracetamol", "Amoxicillin", "No major interaction", "Low"),
    ("Metformin", "Amoxicillin", "No major interaction", "Low"),
]

for interaction in demo_interactions:
    try:
        c.execute("""
            INSERT INTO interactions (drug_a, drug_b, description, severity)
            VALUES (?, ?, ?, ?)
        """, interaction)
    except sqlite3.IntegrityError:
        pass  # skip duplicates

conn.commit()
conn.close()
print("Demo drugs + interactions inserted successfully ✅")
