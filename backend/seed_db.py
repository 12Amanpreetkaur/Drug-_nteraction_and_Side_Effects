import sqlite3

conn = sqlite3.connect("drugs.db")
c = conn.cursor()

sample_drugs = [
    ("Aspirin", "1191"),
    ("Paracetamol", "161"),
    ("Ibuprofen", "5640"),
]

for drug in sample_drugs:
    try:
        c.execute("INSERT INTO drugs (name, rxnorm_id) VALUES (?, ?)", drug)
    except sqlite3.IntegrityError:
        print(f"⚠️ Skipped duplicate: {drug[0]}")

conn.commit()
conn.close()
print("Sample drugs inserted/verified ✅")
