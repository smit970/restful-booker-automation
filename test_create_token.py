import pytest
import requests
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()


def test_auth_token_generation_success():
    """Generates a token once per test session."""
    # Use single quotes inside the getenv to avoid syntax errors
    url = os.getenv("CREATE_TOKEN")

    payload = {
        "username": os.getenv("ADMIN_USER"),
        "password": os.getenv("ADMIN_PASS"),
    }

    response = requests.post(url, json=payload)

    # 1. Verify Status Code
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

    # 2. Verify Token Presence
    data = response.json()
    assert "token" in data, "Response body does not contain 'token' key"

    # 3. Verify Token Format (Basic Check)
    token = data["token"]
    assert len(token) > 0, "Token is empty"
    assert isinstance(token, str), "Token is not a string"

    print(f"\n✅ Token Generation Verified: {token[:5]}*****")


# def test_auth_token_generation_failure():
#     """Check if token is generated for invalid creds."""
#     # Use single quotes inside the getenv to avoid syntax errors
#     url = os.getenv("CREATE_TOKEN")

#     payload = {
#         "username": os.getenv("ADMIN_USER"),
#         "password": os.getenv("ADMIN_PASS"),
#     }

#     response = requests.post(url, json=payload)

#     # 1. Verify Status Code
#     assert response.status_code == 401
#     print("\n✅ Negative Test Passed: Access denied for wrong credentials.")

#     # 2. Some APIs return 401, Booker returns a 200 with an error message
#     # Let's check the response content
#     assert "Bad credentials" in response.text
#     print("\n✅ Negative Test Passed: Access denied for wrong credentials.")
