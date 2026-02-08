import pytest
import requests
import os
import json
import pytest
from faker import Faker

# Initialize Faker once
fake = Faker()


# --- HELPER: Local Fixture (Solves the "Fixture Not Found" error) ---
@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json", "Accept": "application/json"}
    )
    return session


@pytest.fixture
def random_booking_data():
    """
    Generates a fresh, random payload for every test function.
    """
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=100, max=5000),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            # Generate a date this year, convert to String YYYY-MM-DD
            "checkin": fake.date_this_year().strftime("%Y-%m-%d"),
            "checkout": fake.date_this_year().strftime("%Y-%m-%d"),
        },
        "additionalneeds": fake.sentence(nb_words=3),
    }


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
