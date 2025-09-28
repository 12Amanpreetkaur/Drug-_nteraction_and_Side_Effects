import sqlite3
import csv
import os

DB = 'drugs.db'
CSV_FILE = 'uploads/interactions.csv'

con = sqlite3.connect(DB)
cur = con.cursor()

with open(CSV_FILE, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        a = row['drug_a'].strip()
        b = row['drug_b'].strip()
        severity = row['severity'].strip()
        note = row['description'].strip()  # or note if your CSV column is named note

        # Insert drugs if missing
        try:
            cur.execute('INSERT INTO drugs (name) VALUES (?)', (a,))
        except:
            pass
        try:
            cur.execute('INSERT INTO drugs (name) VALUES (?)', (b,))
        except:
            pass

        # Insert interactions
        existing = cur.execute('SELECT id FROM interactions WHERE drug_a=? AND drug_b=?', (a,b)).fetchone()
        if not existing:
            cur.execute('INSERT INTO interactions (drug_a, drug_b, severity, note) VALUES (?,?,?,?)', (a,b,severity,note))
        existing = cur.execute('SELECT id FROM interactions WHERE drug_a=? AND drug_b=?', (b,a)).fetchone()
        if not existing:
            cur.execute('INSERT INTO interactions (drug_a, drug_b, severity, note) VALUES (?,?,?,?)', (b,a,severity,note))

con.commit()
con.close()
print("CSV imported successfully")
