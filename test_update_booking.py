import pytest
import json
import os
import requests
from dotenv import load_dotenv

# 1. Load the .env file immediately
load_dotenv()


@pytest.fixture(scope="session")
def payload():
    return {
        "firstname": "Mike_Updated",
        "lastname": "Patel",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {"checkin": "2023-01-01", "checkout": "2023-01-02"},
        "additionalneeds": "Breakfast",
    }


# --- HELPER: Local Fixture (Solves the "Fixture Not Found" error) ---
@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json", "Accept": "application/json"}
    )
    return session


def get_auth_token(api_client):
    auth_url = os.getenv("CREATE_TOKEN")
    # These credentials are standard for Restful-Booker
    username = os.getenv("ADMIN_USER")
    password = os.getenv("ADMIN_PASS")
    credentials = {"username": username, "password": password}

    response = api_client.post(auth_url, json=credentials)
    return response.json()["token"]


# --- TEST FUNCTION ---
def test_update_bookings(api_client, payload):
    url = os.getenv("BOOKING")

    # ⚠️ WARNING: ID 1046 might be deleted!
    # Ideally, you should CREATE one first to get a valid ID.
    # For now, let's assume 1046 exists (or change this to a known valid ID).
    booking_id = 1046

    update_url = f"{url}{booking_id}"

    # --- FIX 4: Add the Token to Headers ---
    token = get_auth_token(api_client)
    headers = {"Cookie": f"token={token}"}

    print(f"\n🔄 Updating ID {booking_id}...")

    # Send PUT with Headers
    response = api_client.put(update_url, json=payload, headers=headers)

    # Debugging if it fails
    if response.status_code != 200:
        print(f"\n❌ FAILED: Received {response.status_code}")
        print(f"Error Body: {response.text}")

    assert response.status_code == 200

    # --- FIX 5: Handle PUT Response Structure ---
    # PUT returns the data directly. It does NOT have "bookingid" or "booking" keys.
    response_data = response.json()

    print(f"\n📝 Update Successful!")
    print(json.dumps(response_data, indent=2))

    # Loop through payload to verify
    for field in payload:
        # We compare response_data[field] directly
        assert response_data[field] == payload[field], f"Mismatch in field: {field}"

    print(f"✅ All fields for ID {booking_id} match the payload!")
