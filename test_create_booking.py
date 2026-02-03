import pytest
import json
import os
import requests
from dotenv import load_dotenv

# 1. Load the .env file immediately
load_dotenv()


# --- HELPER: Local Fixture (Solves the "Fixture Not Found" error) ---
@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json", "Accept": "application/json"}
    )
    return session


# --- HELPER: Load JSON Data ---
def load_booking_data():
    # Looks for 'booking_data.json' in the parent folder (..)
    # If your json is in the SAME folder, change ".." to "."
    file_path = os.path.join(os.path.dirname(__file__), ".", "booking_data.json")

    with open(file_path, "r") as f:
        return json.load(f)


# --- TEST FUNCTION ---
@pytest.mark.parametrize("booking_payload", load_booking_data())
def test_create_booking_print_only(api_client, booking_payload):
    """
    Data-Driven Test: Creates bookings and prints the JSON response.
    """
    # 2. Use os.getenv instead of Config
    url = os.getenv("BOOKING")

    # 3. Create the booking
    response = api_client.post(url, json=booking_payload)
    assert response.status_code == 200

    if response.status_code != 200:
        print(f"\n❌ FAILED: Received {response.status_code}")
        print(f"Error Body: {response.text}")

    # 4. Extract Data
    response_data = response.json()
    booking_id = response_data["bookingid"]
    expected_dates = booking_payload["bookingdates"]
    actual_dates = response_data["booking"]["bookingdates"]

    # 5. Print the Full Response
    print(f"\n📝 Booking Created! ID: {booking_id}")
    # print("⬇️ Full Server Response:")
    print(json.dumps(response_data, indent=2))

    # 6. Assertions
    # Extract just the booking details from the response
    actual_booking_details = response_data["booking"]

    # Loop through your SOURCE data (the payload)
    for field in booking_payload:
        assert (
            actual_booking_details[field] == booking_payload[field]
        ), f"Mismatch in field: {field}"

    print(f"✅ All fields for ID {booking_id} match the API response!")
