import pytest
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json", "Accept": "application/json"}
    )
    return session


def test_get_and_print_bookings_by_date(api_client):
    url = os.getenv("BOOKING")
    target_checkin = "2026-02-01"
    query_params = {"checkin": target_checkin}

    response = api_client.get(url, params=query_params)
    assert response.status_code == 200, f"Error: {response.text}"

    booking_list = response.json()
    print(f"\n📅 Found {len(booking_list)} bookings for {target_checkin}")

    # Initialize the list OUTSIDE the loop
    corrrect_b_ids = []

    for item in booking_list:
        # 1. Stop immediately if we already have 5 valid IDs
        if len(corrrect_b_ids) >= 5:
            print("🛑 Limit of 5 valid bookings reached. Stopping.")
            break

        b_id = item["bookingid"]

        # FIX: Added the slash '/' between URL and ID
        detail_res = api_client.get(f"{url}/{b_id}")

        if detail_res.status_code == 200:
            full_data = detail_res.json()

            # Add to list
            corrrect_b_ids.append(b_id)

            actual_checkin = full_data["bookingdates"]["checkin"]
            assert actual_checkin >= target_checkin, f"Data mismatch for ID {b_id}!"

            print(f"\n🆔 ID {b_id} Verified | Total Found: {len(corrrect_b_ids)}")
        else:
            print(f"⚠️ ID {b_id} skipped (Status: {detail_res.status_code})")

    print(f"Final List: {corrrect_b_ids}")
