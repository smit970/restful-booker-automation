import pytest
import os
import json


@pytest.mark.regression
def test_create_dynamic_booking(api_client, random_booking_data):
    # 1. Print what we generated (So you can see it in the logs)
    print("\n🎲 Generated Data:")
    print(json.dumps(random_booking_data, indent=2))

    # 2. Send the Request
    url = os.getenv("BOOKING")
    response = api_client.post(url, json=random_booking_data)

    # 3. Validation
    assert response.status_code == 200
    response_data = response.json()

    # Verify the API saved exactly what we sent
    assert response_data["booking"]["firstname"] == random_booking_data["firstname"]
    assert response_data["booking"]["totalprice"] == random_booking_data["totalprice"]

    print(f"✅ Booking Created with ID: {response_data['bookingid']}")
