# conftest.py
import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json", "Accept": "application/json"}
    )
    return session


@pytest.fixture(scope="session")
def auth_token(api_client):
    """
    Automatically fetches a token for the admin user.
    """
    url = "https://restful-booker.herokuapp.com/auth"
    # Ensure these env vars exist, or hardcode for testing
    username = os.getenv("ADMIN_USER", "admin")
    password = os.getenv("ADMIN_PASS", "password123")

    response = api_client.post(url, json={"username": username, "password": password})
    return response.json()["token"]


import pytest
from faker import Faker

# Initialize Faker once
fake = Faker()


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
