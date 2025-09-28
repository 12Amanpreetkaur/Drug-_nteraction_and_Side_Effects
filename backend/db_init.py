import sqlite3

conn = sqlite3.connect("drugs.db")
c = conn.cursor()

# Drugs table
c.execute("""
CREATE TABLE IF NOT EXISTS drugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    rxnorm_id TEXT
)
""")

# Interactions table
c.execute("""
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug_a TEXT NOT NULL,
    drug_b TEXT NOT NULL,
    description TEXT,
    severity TEXT,
    UNIQUE(drug_a, drug_b)
)
""")

conn.commit()
conn.close()
print("DB initialized at drugs.db with drugs + interactions ✅")
