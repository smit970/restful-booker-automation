import pytest
import json
import os
import requests
from dotenv import load_dotenv
import sqlite3
from datetime import datetime

# 1. Load the .env file immediately
load_dotenv()


# --- HELPER: Local Fixture ---
@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json", "Accept": "application/json"}
    )
    return session


# --- HELPER: Load JSON Data ---
def load_booking_data():
    file_path = os.path.join(os.path.dirname(__file__), ".", "booking_data.json")
    with open(file_path, "r") as f:
        return json.load(f)


# --- TEST FUNCTION ---
@pytest.mark.parametrize("booking_payload", load_booking_data())
def test_create_booking_print_only(api_client, booking_payload):
    url = os.getenv("BOOKING")

    # 1. Create the booking
    response = api_client.post(url, json=booking_payload)
    assert response.status_code == 200

    # 2. Extract Data
    response_data = response.json()
    booking_id = response_data["bookingid"]

    print(f"\n📝 Booking Created! ID: {booking_id}")

    # 3. Assertions (API Level)
    actual_booking_details = response_data["booking"]
    for field in booking_payload:
        assert (
            actual_booking_details[field] == booking_payload[field]
        ), f"Mismatch in field: {field}"
    print(f"✅ API Response Validated.")

    # 4. Save to DB
    save_booking_to_db(response_data)

    # 5. Verify DB (Round Trip Check)
    # We pass the full response_data so the verification function can parse it
    verify_db_entry(response_data)


# --- DATE VALIDATOR ---
def validate_dates(checkin_str, checkout_str):
    """
    Validates date format and order.
    Returns: (bool, checkin_val, checkout_val)
    """
    try:
        fmt = "%Y-%m-%d"
        d1 = datetime.strptime(checkin_str, fmt)
        d2 = datetime.strptime(checkout_str, fmt)

        if d1 > d2:
            print(
                f"   ⚠️ Date Order Error: Checkin ({checkin_str}) is after Checkout ({checkout_str})"
            )
            return False, "00-00-0000", "00-00-0000"

        return True, checkin_str, checkout_str

    except ValueError:
        print(f"   ⚠️ Date Format Error: {checkin_str} / {checkout_str}")
        return False, "00-00-0000", "00-00-0000"


# --- DB ENTRY ---
def save_booking_to_db(response_data):
    booking_id = response_data["bookingid"]
    details = response_data["booking"]

    # 🛠️ FIX 1: Call validate_dates with BOTH dates at once
    # It returns 3 values: boolean, valid_checkin, valid_checkout
    is_valid, final_checkin, final_checkout = validate_dates(
        details["bookingdates"]["checkin"], details["bookingdates"]["checkout"]
    )

    try:
        conn = sqlite3.connect("test_database.db")
        cursor = conn.cursor()

        sql = """
        INSERT OR REPLACE INTO bookings (id, firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            sql,
            (
                booking_id,
                details["firstname"],
                details["lastname"],
                details["totalprice"],
                details["depositpaid"],
                final_checkin,  # <--- Use the validated variables!
                final_checkout,  # <--- Use the validated variables!
                details["additionalneeds"],
            ),
        )

        conn.commit()
        print(f"   └── 💾 Saved ID {booking_id} to Database.")

    except Exception as e:
        print(f"   └── ❌ DB Error: {e}")
    finally:
        conn.close()


# --- VERIFY DB ENTRIES ---
def verify_db_entry(response_data):
    # 🛠️ FIX 2: Correctly map the incoming JSON
    booking_id = response_data[
        "bookingid"
    ]  # Note: API Key is "bookingid", not "booking_id"
    expected_data = response_data["booking"]  # We need to dig into the nested object

    conn = sqlite3.connect("test_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings WHERE id=?", (booking_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        pytest.fail(f"❌ Verification Failed: Booking ID {booking_id} not found in DB!")

    # Map DB Row (Tuple)
    db_id = row[0]
    db_firstname = row[1]
    db_lastname = row[2]
    db_price = row[3]
    db_deposit = row[4]
    db_checkin = row[5]
    db_checkout = row[6]
    db_needs = row[7]

    print(f"\n   🔍 Verifying DB Data for ID {booking_id}...")

    try:
        assert db_id == booking_id
        # 🛠️ FIX 3: Compare against 'expected_data' (the nested 'booking' object)
        assert db_firstname == expected_data["firstname"]
        assert db_lastname == expected_data["lastname"]
        assert db_price == expected_data["totalprice"]
        assert bool(db_deposit) == expected_data["depositpaid"]

        if db_checkin == "00-00-0000":
            print(
                "      ⚠️ Note: Dates were saved as '00-00-0000' (Invalid input detected)"
            )
        else:
            assert db_checkin == expected_data["bookingdates"]["checkin"]
            assert db_checkout == expected_data["bookingdates"]["checkout"]

        assert db_needs == expected_data["additionalneeds"]

        print("      ✅ DB Verification Passed! Data is identical.")

    except AssertionError as e:
        # We print the mismatch to help debugging before failing
        print(f"      ❌ DB Mismatch! {e}")
        pytest.fail(f"DB Verification Failed: {e}")
