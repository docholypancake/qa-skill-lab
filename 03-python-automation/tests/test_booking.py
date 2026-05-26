import requests

def test_create_booking_returns_id(booking):
	assert isinstance(booking, int)
	assert booking > 0


def test_read_booking(base_url, booking):
	response = requests.get(f"{base_url}/booking/{booking}")

	assert response.status_code == 200
	assert response.json()["firstname"] == "Jim"


def test_list_bookings(base_url, booking):
	response = requests.get(f"{base_url}/booking?firstname=Jim&lastname=Brown")

	assert response.status_code == 200 
	ids = [b["bookingid"] for b in response.json()]
	assert booking in ids


def test_update_booking_put(base_url, booking, auth_token):
	payload = {
		"firstname": "Jane",
		"lastname": "Brown",
		"totalprice": 111,
		"depositpaid": True,
		"bookingdates": {
			"checkin": "2024-01-01",
			"checkout": "2024-01-05"
		}
	}
	response = requests.put(
		f"{base_url}/booking/{booking}",
		json=payload,
		headers={"Cookie": f"token={auth_token}"}
	)

	assert response.status_code == 200
	assert response.json()["firstname"] == "Jane"


def test_update_booking_patch(base_url, booking, auth_token):
	payload = {"firstname": "Updated"}
	response = requests.patch(
		f"{base_url}/booking/{booking}",
		json=payload,
		headers={"Cookie": f"token={auth_token}"}
	)

	assert response.status_code == 200
	assert response.json()["firstname"] == "Updated"
	assert response.json()["lastname"] == "Brown"


def test_put_without_token(base_url, booking):
	payload = {
		"firstname": "Jane",
		"lastname": "Brown",
		"totalprice": 111,
		"depositpaid": True,
		"bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-05"},
	}
	response = requests.put(f"{base_url}/booking/{booking}", json=payload)
	assert response.status_code == 403


def test_patch_without_token(base_url, booking):
	response = requests.patch(
		f"{base_url}/booking/{booking}",
		json={"firstname": "X"},
	)
	assert response.status_code == 403


def test_delete_booking(base_url, booking, auth_token):
	response = requests.delete(
		f"{base_url}/booking/{booking}",
		headers={"Cookie": f"token={auth_token}"},
	)
	assert response.status_code == 201

