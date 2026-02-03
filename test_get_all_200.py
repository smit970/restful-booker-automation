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


# ---Test Function---


def test_get_all_booking_ids(api_client):
    url = os.getenv("BOOKING")

    # 1. Get initial count
    response = api_client.get(url)
    assert response.status_code == 200
    all_ids = response.json()

    # FIX: Use curly braces to print the variable value
    total_count = len(all_ids)
    print(f"\n📊 Total bookings in system: {total_count}")

    # 2. Iterate through IDs (limiting to 10 for safety)
    # FIX: [:10] prevents the test from running for 20 minutes
    counter: int = 0
    valid_ids_list = []
    for item in all_ids:
        b_id = item["bookingid"]
        detail_res = api_client.get(f"{url}{b_id}")

        # FIX: Check status code before calling .json() to avoid crashes
        if detail_res.status_code == 200:
            details = detail_res.json()
            valid_ids_list.append(b_id)
            print(
                f"\n🆔 ID {b_id}:"
                f"\n   NAME: {details['firstname']} {details['lastname']}"
                f"\n   DATES: {details['bookingdates']['checkin']} to {details['bookingdates']['checkout']}"
            )
        # else:
        #     counter += 1
        #     print(
        #         f"\n⚠️ ID {b_id}: Could not retrieve details (Status: {detail_res.status_code})"
        #     )

        # if counter > 15:
        #     print("Too Many 404 entries in DB Exiting...")
        #     exit

    # --- SAVE TO FILE ---
    # We save as a JSON dictionary for easy reading later
    output_file = "valid_ids.json"
    with open(output_file, "w") as f:
        json.dump({"valid_ids": valid_ids_list}, f, indent=4)

    print(f"\n📂 Successfully saved {len(valid_ids_list)} IDs to {output_file}")
