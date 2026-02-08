import pytest
import sqlite3


def test_verify_booking_in_db():
    # 1. Simulate: API returns ID 1
    booking_id = 1
    expected_name = "Sumit"

    # 2. Connect to the DB (The "Back Door")
    conn = sqlite3.connect("test_database.db")
    cursor = conn.cursor()

    # 3. Query: "Select * from bookings where id = 1"
    cursor.execute(
        "SELECT firstname, lastname, totalprice FROM bookings WHERE id=?", (booking_id,)
    )
    row = cursor.fetchone()

    conn.close()

    # 4. Verification
    print(f"\n🔍 DB Row Found: {row}")

    assert row is not None, "Booking ID 1 not found in DB!"
    assert row[0] == expected_name
    assert row[2] == 150
