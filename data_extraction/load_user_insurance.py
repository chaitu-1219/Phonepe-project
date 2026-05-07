import pandas as pd
import sqlite3

print("Starting script...")

# Load CSVs
user_df = pd.read_csv("data/processed/user_data.csv")
ins_df = pd.read_csv("data/processed/insurance_data.csv")

print("User rows:", len(user_df))
print("Insurance rows:", len(ins_df))

# Connect to SQLite
conn = sqlite3.connect("data/phonepe.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_data (
    state TEXT,
    year INTEGER,
    brand TEXT,
    registeredUsers INTEGER,
    appOpens REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS insurance_data (
    state TEXT,
    year INTEGER,
    count INTEGER,
    amount REAL
)
""")

# Clear tables
cursor.execute("DELETE FROM user_data")
cursor.execute("DELETE FROM insurance_data")

# Insert USER DATA
user_query = """
INSERT INTO user_data (state, year, brand, registeredUsers, appOpens)
VALUES (?, ?, ?, ?, ?)
"""

for i, row in user_df.iterrows():
    cursor.execute(user_query, (
        row["state"],
        int(row["year"]),
        row["brand"],
        int(row["registeredUsers"]),
        float(row["appOpens"])
    ))

    if i % 1000 == 0:
        print(f"Inserted user rows: {i}")

conn.commit()
print("User data inserted")

# Insert INSURANCE DATA
ins_query = """
INSERT INTO insurance_data (state, year, count, amount)
VALUES (?, ?, ?, ?)
"""

for i, row in ins_df.iterrows():
    cursor.execute(ins_query, (
        row["state"],
        int(row["year"]),
        int(row["count"]),
        float(row["amount"])
    ))

conn.commit()
print("Insurance data inserted")

cursor.close()
conn.close()
print("Done")