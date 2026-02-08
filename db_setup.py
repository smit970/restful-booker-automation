import sqlite3
import os

# Delete old DB to start fresh (Optional but easiest)
if os.path.exists("test_database.db"):
    os.remove("test_database.db")

conn = sqlite3.connect("test_database.db")
cursor = conn.cursor()

# Create table with ALL fields
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY,
        firstname TEXT,
        lastname TEXT,
        totalprice INTEGER,
        depositpaid BOOLEAN,
        checkin DATE,
        checkout DATE,
        additionalneeds TEXT
    )
"""
)

conn.commit()
conn.close()
print("✅ Database reset with new schema!")
