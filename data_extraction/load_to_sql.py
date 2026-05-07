import pandas as pd
import sqlite3
import os

print("Starting script...")

# Load CSV
try:
    df = pd.read_csv("data/processed/aggregated_transaction.csv")
    print("CSV loaded. Rows:", len(df))
except Exception as e:
    print("CSV Error:", e)
    exit()

# Connect to SQLite (creates file if it doesn't exist)
try:
    print("Connecting to SQLite...")

    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/phonepe.db")

    print("Connected to SQLite")

    cursor = conn.cursor()

except Exception as e:
    print("Connection Error:", e)
    exit()

try:
    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS aggregated_transaction (
        state TEXT,
        year INTEGER,
        type TEXT,
        count INTEGER,
        amount REAL
    )
    """)

    # Clear table
    cursor.execute("DELETE FROM aggregated_transaction")
    print("Table cleared")

    insert_query = """
    INSERT INTO aggregated_transaction
    (state, year, type, count, amount)
    VALUES (?, ?, ?, ?, ?)
    """

    batch_size = 500
    batch = []

    for i, row in df.iterrows():
        batch.append((
            row["state"],
            int(row["year"]),
            row["type"],
            int(row["count"]),
            float(row["amount"])
        ))

        if len(batch) == batch_size:
            cursor.executemany(insert_query, batch)
            conn.commit()
            print(f"Inserted {i+1} rows")
            batch = []

    if batch:
        cursor.executemany(insert_query, batch)
        conn.commit()

    print("Data inserted successfully")

except Exception as e:
    print("Insert Error:", e)

finally:
    cursor.close()
    conn.close()
    print("Connection closed")