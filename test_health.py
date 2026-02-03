import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def test_api_health_check():

    url = f"{os.getenv("HEALTH_PING")}"

    try:
        response = requests.get(url, timeout=5)  # 5 second timeout is standard

        # Booker API specifically returns 201 Created for a successful ping
        assert (
            response.status_code == 201
        ), f"Health check failed! Status: {response.status_code}"

        print("\n🚀 API is Healthy and Ready for Testing!")

    except requests.exceptions.ConnectionError:
        pytest.fail("❌ Server is DOWN. Connection refused.")
    except requests.exceptions.Timeout:
        pytest.fail("🐢 Server is SLOW. Request timed out.")
