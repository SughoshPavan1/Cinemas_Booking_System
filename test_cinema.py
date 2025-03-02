import unittest
from cinema import Cinema  # Assuming the Cinema class is in a file called cinema.py


class TestCinema(unittest.TestCase):
    def setUp(self):
        """Set up a fresh cinema instance for each test."""
        self.cinema = Cinema("Test Movie", 5, 10)  # 5 rows (A-E), 10 seats per row

    def test_initialization(self):
        """Test that the cinema initializes correctly."""
        self.assertEqual(self.cinema.title, "Test Movie")
        self.assertEqual(self.cinema.rows, 5)
        self.assertEqual(self.cinema.seats_per_row, 10)
        self.assertEqual(self.cinema.total_seats, 50)
        self.assertEqual(self.cinema.available_seats, 50)
        self.assertEqual(len(self.cinema.bookings), 0)

    def test_default_booking_strategy(self):
        """Test booking seats using the default strategy (middle expansion)."""
        # Book 3 seats
        booking_id, seats = self.cinema.book_seats(3)
        self.assertIsNotNone(booking_id)
        self.assertEqual(len(seats), 3)

        # Check that seats are in the middle of the first row
        row_seats = [seat for seat in seats if seat[0] == 0]  # Row 0 (closest to screen)
        self.assertEqual(len(row_seats), 3)

        # Confirm the booking
        self.cinema.confirm_booking(booking_id, seats)
        self.assertEqual(self.cinema.available_seats, 47)
        self.assertEqual(len(self.cinema.bookings), 1)

        # Verify the booking can be retrieved
        retrieved_seats = self.cinema.check_booking(booking_id)
        self.assertEqual(len(retrieved_seats), 3)

    def test_custom_position_booking(self):
        """Test booking seats from a specified position."""
        # Book 4 seats starting from A3
        booking_id, seats = self.cinema.book_seats(4, "A3")
        self.assertIsNotNone(booking_id)
        self.assertEqual(len(seats), 4)

        # Check seats are sequential from A3
        expected_positions = [(0, 2), (0, 3), (0, 4), (0, 5)]  # A3 to A6
        self.assertEqual(sorted(seats), sorted(expected_positions))

        # Confirm the booking
        self.cinema.confirm_booking(booking_id, seats)
        self.assertEqual(self.cinema.available_seats, 46)

    def test_invalid_starting_position(self):
        """Test booking with an invalid starting position."""
        # Test with position outside the cinema
        booking_id, seats = self.cinema.book_seats(2, "Z1")
        self.assertIsNone(booking_id)
        self.assertIsNone(seats)

        # Test with invalid format
        booking_id, seats = self.cinema.book_seats(2, "A")
        self.assertIsNone(booking_id)
        self.assertIsNone(seats)

        # Test with non-existent seat number
        booking_id, seats = self.cinema.book_seats(2, "A15")
        self.assertIsNone(booking_id)
        self.assertIsNone(seats)

    def test_booking_with_unavailable_seats(self):
        """Test booking when specified seats are already taken."""
        # First booking takes A1-A4
        booking_id1, seats1 = self.cinema.book_seats(4, "A1")
        self.cinema.confirm_booking(booking_id1, seats1)

        # Second booking should fail because it wants to start at A3 (already taken)
        booking_id2, seats2 = self.cinema.book_seats(2, "A3")
        self.assertIsNone(booking_id2)
        self.assertIsNone(seats2)

    def test_booking_with_insufficient_seats(self):
        """Test booking when there aren't enough available seats."""
        # Book all 50 seats
        booking_id1, seats1 = self.cinema.book_seats(50)
        self.cinema.confirm_booking(booking_id1, seats1)

        # Try to book one more seat
        booking_id2, seats2 = self.cinema.book_seats(1)
        self.assertIsNone(booking_id2)
        self.assertIsNone(seats2)

    def test_nonexistent_booking_check(self):
        """Test checking a booking that doesn't exist."""
        result = self.cinema.check_booking("INVALID123")
        self.assertIsNone(result)

    def test_multiple_bookings(self):
        """Test making multiple bookings and ensuring they don't conflict."""
        # First booking takes middle seats in row A
        booking_id1, seats1 = self.cinema.book_seats(3)
        self.cinema.confirm_booking(booking_id1, seats1)

        # Second booking should take A1-A3
        booking_id2, seats2 = self.cinema.book_seats(3, "A1")
        self.cinema.confirm_booking(booking_id2, seats2)

        # Third booking should take A8-A10
        booking_id3, seats3 = self.cinema.book_seats(3, "A8")
        self.cinema.confirm_booking(booking_id3, seats3)

        # Verify all bookings
        self.assertEqual(len(self.cinema.bookings), 3)
        self.assertEqual(self.cinema.available_seats, 41)

        # Check each booking
        self.assertEqual(len(self.cinema.check_booking(booking_id1)), 3)
        self.assertEqual(len(self.cinema.check_booking(booking_id2)), 3)
        self.assertEqual(len(self.cinema.check_booking(booking_id3)), 3)


if __name__ == "__main__":
    unittest.main()