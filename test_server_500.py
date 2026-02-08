import pytest
import requests
import responses
import os


# 1. We use the @responses.activate decorator
# This turns on the "Interceptor" for this specific test
@responses.activate
def test_simulate_server_error():

    # 2. Define the Target URL (The one we want to intercept)
    url = "https://restful-booker.herokuapp.com/booking"

    # 3. Register the Mock
    # "If anyone tries to GET this URL, return status 500 instantly."
    responses.add(
        responses.GET,  # Method
        url,  # URL to match
        json={"error": "Crash!"},  # Fake Response Body
        status=500,  # Fake Status Code
    )

    # 4. Run the code (This looks real, but it never hits the internet!)
    print("\n🚀 Attempting to connect to API...")
    response = requests.get(url)

    # 5. Verify our code handles the error correctly
    print(f"Server replied: {response.status_code}")

    assert response.status_code == 500
    assert response.json()["error"] == "Crash!"
