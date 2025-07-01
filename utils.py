import json
import requests
from datetime import datetime, timedelta
import time

class TestUtils:
    """Utility class for common test operations and data management"""

    def __init__(self):
        self.test_data_file = "test_data.json"
        self.test_data = self.get_test_data()
        self.base_url = self.test_data["base_url"]
        self.api_url = self.test_data.get("api_url", f"{self.base_url}/booking")
        self.admin_credentials = self.test_data["admin_credentials"]
        self.session = requests.Session()

    def get_test_data(self):
        try:
            with open(self.test_data_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return self._get_default_test_data()

    def _get_default_test_data(self):
        """Default test data structure"""
        return {
            "base_url": "https://automationintesting.online",
            "api_url": "https://automationintesting.online/booking",
            "admin_credentials": {
                "username": "admin",
                "password": "password"
            },
            "valid_booking_data": {
                "firstname": "John",
                "lastname": "Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890"
            },
            "invalid_booking_data": {
                "firstname": "",
                "lastname": "",
                "email": "not-an-email",
                "phone": "abcde"
            },
            "room_data": {
                "roomName": "Test Room",
                "type": "Single",
                "accessible": True,
                "description": "Test room for automation",
                "features": ["WiFi", "TV", "Safe"],
                "roomPrice": 100
            }
        }

    def get_admin_auth_token(self):
        """Get authentication token for admin operations"""
        try:
            login_url = f"{self.base_url}/auth/login"
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = self.session.post(
                login_url, 
                json=self.admin_credentials,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("token")
            else:
                print(f"[API LOGIN FAIL] Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"[API LOGIN FAIL] Exception: {e}")
        return None

    def create_test_room(self, room_data=None):
        """Create a test room and return room ID"""
        if not room_data:
            room_data = self.test_data["room_data"]

        token = self.get_admin_auth_token()
        if not token:
            raise Exception("Failed to get admin token")
            
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"token={token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        try:
            response = self.session.post(
                f"{self.base_url}/room", 
                json=room_data, 
                headers=headers,
                timeout=30
            )
            if response.status_code in [200, 201]:
                result = response.json()
                return result.get("roomid") or result.get("id")
            else:
                raise Exception(f"Failed to create test room: Status {response.status_code}, {response.text}")
        except Exception as e:
            raise Exception(f"Failed to create test room: {e}")

    def delete_test_room(self, room_id):
        """Delete a test room"""
        token = self.get_admin_auth_token()
        if not token:
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"token={token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        try:
            response = self.session.delete(
                f"{self.base_url}/room/{room_id}", 
                headers=headers,
                timeout=30
            )
            return response.status_code in [200, 202, 204]
        except Exception as e:
            print(f"Failed to delete room {room_id}: {e}")
            return False

    def get_available_rooms(self):
        """Get list of available rooms"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = self.session.get(f"{self.base_url}/room/", headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get("rooms", [])
        except Exception as e:
            print(f"Failed to get rooms: {e}")
        return []

    def create_test_booking(self, room_id, booking_data=None):
        """Create a test booking and return booking ID"""
        if not booking_data:
            booking_data = self.test_data["valid_booking_data"]

        today = datetime.today().date()
        tomorrow = today + timedelta(days=1)

        payload = {
            "bookingdates": {
                "checkin": today.strftime("%Y-%m-%d"),
                "checkout": tomorrow.strftime("%Y-%m-%d")
            },
            "roomid": room_id,
            "firstname": booking_data["firstname"],
            "lastname": booking_data["lastname"],
            "email": booking_data["email"],
            "phone": booking_data["phone"]
        }

        try:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = self.session.post(
                f"{self.base_url}/booking/", 
                json=payload,
                headers=headers,
                timeout=30
            )
            if response.status_code in [200, 201]:
                result = response.json()
                return result.get("bookingid") or result.get("id")
            else:
                raise Exception(f"Booking failed: Status {response.status_code}, {response.text}")
        except Exception as e:
            raise Exception(f"Booking failed: {e}")

    def cleanup_test_rooms(self, api_base, headers):
        """Delete all rooms with 'Test' in their name"""
        try:
            response = self.session.get(api_base, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                rooms = data.get("rooms", [])
                for room in rooms:
                    room_name = room.get("roomName", "")
                    if "Test" in room_name:
                        room_id = room.get("roomid") or room.get("id")
                        if room_id:
                            self.session.delete(f"{api_base}/{room_id}", headers=headers, timeout=30)
                            time.sleep(0.5)  # Small delay between deletions
        except Exception as e:
            print(f"Cleanup failed: {e}")

    def create_room(self, api_base, room_data, headers):
        """Create a room via API"""
        try:
            response = self.session.post(api_base, json=room_data, headers=headers, timeout=30)
            if response.status_code in [200, 201]:
                return response.json()
            raise Exception(f"Failed to create room: Status {response.status_code}, {response.text}")
        except Exception as e:
            raise Exception(f"Failed to create room: {e}")

    def delete_room(self, api_base, room_id, headers):
        """Delete a room via API"""
        try:
            response = self.session.delete(f"{api_base}/{room_id}", headers=headers, timeout=30)
            return response.status_code in [200, 202, 204]
        except Exception as e:
            print(f"Failed to delete room {room_id}: {e}")
            return False

    def create_booking(self, booking_api, booking_data):
        """Create a booking via API"""
        try:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = self.session.post(booking_api, json=booking_data, headers=headers, timeout=30)
            if response.status_code in [200, 201]:
                return response.json()
            raise Exception(f"Failed to create booking: Status {response.status_code}, {response.text}")
        except Exception as e:
            raise Exception(f"Failed to create booking: {e}")

    def delete_booking(self, booking_api, booking_id, headers):
        """Delete a booking via API"""
        try:
            response = self.session.delete(f"{booking_api}/{booking_id}", headers=headers, timeout=30)
            return response.status_code in [200, 202, 204]
        except Exception as e:
            print(f"Failed to delete booking {booking_id}: {e}")
            return False

    def wait_for_api_response(self, url, method="GET", data=None, headers=None, timeout=30, retries=3):
        """Wait for API response with retries"""
        for attempt in range(retries):
            try:
                if method.upper() == "GET":
                    response = self.session.get(url, headers=headers, timeout=timeout)
                elif method.upper() == "POST":
                    response = self.session.post(url, json=data, headers=headers, timeout=timeout)
                elif method.upper() == "DELETE":
                    response = self.session.delete(url, headers=headers, timeout=timeout)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                if response.status_code < 500:  # Don't retry client errors
                    return response
                    
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(1)  # Wait before retry
        
        return None

    def verify_room_exists(self, room_id):
        """Verify if a room exists"""
        try:
            rooms = self.get_available_rooms()
            return any(room.get("roomid") == room_id or room.get("id") == room_id for room in rooms)
        except:
            return False

    def get_booking_details(self, booking_id):
        """Get booking details by ID"""
        try:
            token = self.get_admin_auth_token()
            if not token:
                return None
                
            headers = {
                "Content-Type": "application/json",
                "Cookie": f"token={token}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = self.session.get(f"{self.api_url}/{booking_id}", headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Failed to get booking details: {e}")
        return None