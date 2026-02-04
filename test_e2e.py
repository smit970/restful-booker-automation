import pytest
import os
import json


@pytest.mark.regression
@pytest.mark.e2e
# We use a Class to group the steps together
class TestBookingFlow:

    # CLASS VARIABLE to store data between steps
    booking_id = None

    def test_01_create_booking(self, api_client):
        """Step 1: Create a new booking and save the ID"""
        url = os.getenv("BOOKING")
        payload = {
            "firstname": "Data",
            "lastname": "E2E",
            "totalprice": 999,
            "depositpaid": True,
            "bookingdates": {"checkin": "2023-01-01", "checkout": "2023-01-05"},
            "additionalneeds": "Integration Testing",
        }

        response = api_client.post(url, json=payload)
        assert response.status_code == 200

        # SAVE THE ID to the class variable so Step 2 can use it
        TestBookingFlow.booking_id = response.json()["bookingid"]
        print(f"\n✅ Created Booking ID: {self.booking_id}")

    def test_02_verify_booking(self, api_client):
        """Step 2: Check if the ID from Step 1 actually exists"""
        # Retrieve the ID from Step 1
        b_id = TestBookingFlow.booking_id
        assert b_id is not None, "Create Booking failed, ID is missing!"

        url = os.getenv("BOOKING")
        response = api_client.get(f"{url}{b_id}")

        assert response.status_code == 200
        print(f"✅ Verified ID {b_id} exists")

    def test_03_update_booking(self, api_client, auth_token):
        """Step 3: Update the name using the Token from conftest"""
        b_id = TestBookingFlow.booking_id
        url = os.getenv("BOOKING")

        update_payload = {
            "firstname": "Data_Updated",
            "lastname": "E2E",
            "totalprice": 9999,
            "depositpaid": True,
            "bookingdates": {"checkin": "2023-01-01", "checkout": "2023-01-05"},
            "additionalneeds": "Integration Testing",
        }

        # Use the auth_token fixture directly!
        headers = {"Cookie": f"token={auth_token}"}

        response = api_client.put(f"{url}{b_id}", json=update_payload, headers=headers)
        assert response.status_code == 200
        assert response.json()["firstname"] == update_payload["firstname"]
        print(f"✅ Updated ID {b_id} successfully")

    def test_04_delete_booking(self, api_client, auth_token):
        """Step 4: Delete the booking and confirm it's gone"""
        b_id = TestBookingFlow.booking_id
        url = os.getenv("BOOKING")
        headers = {"Cookie": f"token={auth_token}"}

        # Delete
        del_response = api_client.delete(f"{url}{b_id}", headers=headers)
        assert del_response.status_code == 201

        # Double Check (Negative Testing)
        get_response = api_client.get(f"{url}{b_id}")
        assert get_response.status_code == 404
        print(f"✅ Deleted ID {b_id} and verified 404")
