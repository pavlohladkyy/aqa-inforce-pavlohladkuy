base_url = "https://automationintesting.online"
api_url = f"{base_url}/booking"

admin_credentials = {
    "username": "admin",
    "password": "password"
}

valid_booking_data = {
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com",
    "phone": "1234567890"
}

invalid_booking_data = {
    "firstname": "",
    "lastname": "",
    "email": "not-an-email",
    "phone": "abcde"
}

room_data = {
    "roomName": "Test Room",
    "type": "Single",
    "accessible": True,
    "description": "Test room for automation",
    "features": ["WiFi", "TV", "Safe"],
    "roomPrice": 100
}
