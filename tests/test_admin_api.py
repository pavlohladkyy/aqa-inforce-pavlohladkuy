import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import TestUtils

class TestAdminAPI:
    """Admin API Test Suite"""

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self):
        """Initialize test utils and shared data"""
        self.utils = TestUtils()
        self.token = self.utils.get_admin_auth_token()
        assert self.token is not None, "Failed to retrieve admin token"

        self.headers = {
            "Content-Type": "application/json",
            "Cookie": f"token={self.token}",
            "User-Agent": "pytest"
        }

        self.api_base = f"{self.utils.base_url}/room"
        self.booking_api = f"{self.utils.base_url}/booking"

    def test_create_room(self):
        """Test admin can create a new room"""
        room_data = self.utils.test_data["room_data"]
        response = self.utils.create_room(self.api_base, room_data, self.headers)
        assert "roomid" in response or "id" in response, "Room creation failed"
        self.__class__.room_id = response.get("roomid") or response.get("id")

    def test_get_all_rooms(self):
        """Test retrieving all rooms"""
        rooms = self.utils.get_available_rooms()
        assert isinstance(rooms, list), "Rooms should be returned as a list"
        assert any(room.get("roomid") == self.room_id for room in rooms), "Created room not found"

    def test_verify_created_room(self):
        """Check that created room actually exists"""
        exists = self.utils.verify_room_exists(self.room_id)
        assert exists, "Room not found after creation"

    def test_create_booking_for_room(self):
        """Test admin can create a booking for a room"""
        booking_data = self.utils.test_data["valid_booking_data"]
        booking_id = self.utils.create_test_booking(self.room_id, booking_data)
        assert booking_id, "Booking creation failed"
        self.__class__.booking_id = booking_id

    def test_get_booking_details(self):
        """Test retrieving booking details"""
        booking = self.utils.get_booking_details(self.booking_id)
        assert booking is not None, "Failed to fetch booking details"
        assert booking.get("bookingid") == self.booking_id or booking.get("id") == self.booking_id

    def test_delete_booking(self):
        """Test deleting the created booking"""
        deleted = self.utils.delete_booking(self.booking_api, self.booking_id, self.headers)
        assert deleted, "Booking deletion failed"

    def test_delete_room(self):
        """Test deleting the created room"""
        deleted = self.utils.delete_room(self.api_base, self.room_id, self.headers)
        assert deleted, "Room deletion failed"
