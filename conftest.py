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
