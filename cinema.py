import threading


class Cinema:
    def __init__(self, title, rows, seats_per_row):
        """Initialize a new cinema with the given title and seating configuration.

        Args:
            title (str): The name of the movie
            rows (int): Number of rows in the cinema
            seats_per_row (int): Number of seats in each row
        """
        self.title = title
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seats = [['.' for _ in range(seats_per_row)] for _ in range(rows)]
        self.bookings = {}
        self.lock = threading.Lock()  # Lock for thread safety
        self.current_booking_id = 1  # For sequential booking IDs
        self.total_seats = rows * seats_per_row
        self.available_seats = self.total_seats

    def display_seats(self):
        """Display the current state of cinema seats."""
        print("          S C R E E N")
        print("--------------------------------")
        for i in range(self.rows - 1, -1, -1):  # Reverse row order for display
            row_label = chr(ord('A') + i)
            row_str = row_label + " " + "  ".join(self.seats[i])
            print(row_str)
        print("  " + "  ".join(map(str, range(1, self.seats_per_row + 1))))

    def _create_temp_seats_map(self):
        """Create a temporary map of all seats with current bookings marked.

        Returns:
            list: 2D array representing seats with '.' for available and '#' for booked
        """
        # Create a fresh representation of all seats
        temp_seats = [['.' for _ in range(self.seats_per_row)] for _ in range(self.rows)]

        # Mark existing bookings
        for booking_seats in self.bookings.values():
            for row, col in booking_seats:
                temp_seats[row][col] = '#'

        return temp_seats

    def _parse_seat_position(self, start_pos):
        """Parse a seat position string (e.g., 'A1') into row and column indices.

        Args:
            start_pos (str): Seat position in format like 'A1', 'B3', etc.

        Returns:
            tuple: (row_index, col_index) or (None, None) if invalid
        """
        try:
            row_char = start_pos[0].upper()
            # Convert to array index
            row_index = ord(row_char) - ord('A')
            col_index = int(start_pos[1:]) - 1

            # Validate indices
            if row_index < 0 or row_index >= self.rows or col_index < 0 or col_index >= self.seats_per_row:
                return None, None  # Invalid starting position

            return row_index, col_index

        except (ValueError, IndexError):
            return None, None  # Invalid starting position format

    def _allocate_from_custom_position(self, temp_seats, num_tickets, start_pos):
        """Allocate seats starting from a custom position specified by the user.

        Args:
            temp_seats (list): 2D array representing current seat status
            num_tickets (int): Number of tickets to allocate
            start_pos (str): Starting seat position (e.g., 'A1')

        Returns:
            list: List of allocated seat positions as (row, col) tuples, or empty list if unable to allocate
        """
        row_index, col_index = self._parse_seat_position(start_pos)
        if row_index is None:
            return []

        # Check if the starting seat is already taken
        if temp_seats[row_index][col_index] == '#':
            return []

        selected_seats = []
        current_row = row_index
        current_col = col_index
        remaining = num_tickets

        # Allocate seats row by row, starting from the specified position
        while remaining > 0 and current_row < self.rows:
            # Try current row first, going sequentially from the starting point
            while current_col < self.seats_per_row and remaining > 0:
                if temp_seats[current_row][current_col] == '.':
                    selected_seats.append((current_row, current_col))
                    temp_seats[current_row][current_col] = 'o'
                    remaining -= 1
                current_col += 1

            # If we still need more seats, move to the next row
            if remaining > 0:
                current_row += 1  # Move to the next row (from A to B, etc.)
                # If we reach beyond the last row, we can't fulfill the request
                if current_row >= self.rows:
                    return []

                # For the next row, start from the leftmost seat
                current_col = 0

        # If we couldn't allocate all requested seats
        if len(selected_seats) < num_tickets:
            return []

        return selected_seats

    def _allocate_default_seats(self, temp_seats, num_tickets):
        """Allocate seats using the default strategy (middle expansion).

        Args:
            temp_seats (list): 2D array representing current seat status
            num_tickets (int): Number of tickets to allocate

        Returns:
            list: List of allocated seat positions as (row, col) tuples
        """
        selected_seats = []
        remaining = num_tickets

        # Start allocation from row 0 (closest to screen)
        for row_index in range(self.rows):
            if remaining == 0:
                break

            # Start from the middle and expand outward
            mid_col = self.seats_per_row // 2
            right = mid_col
            left = mid_col - 1

            # Try the middle position first
            if temp_seats[row_index][mid_col] == '.':
                selected_seats.append((row_index, mid_col))
                temp_seats[row_index][mid_col] = 'o'
                remaining -= 1

            # Then expand outward from middle
            while remaining > 0 and (left >= 0 or right < self.seats_per_row):
                if right < self.seats_per_row and temp_seats[row_index][right] == '.':
                    selected_seats.append((row_index, right))
                    temp_seats[row_index][right] = 'o'
                    remaining -= 1

                if remaining > 0 and left >= 0 and temp_seats[row_index][left] == '.':
                    selected_seats.append((row_index, left))
                    temp_seats[row_index][left] = 'o'
                    remaining -= 1

                right += 1
                left -= 1

        return selected_seats

    def book_seats(self, num_tickets, start_pos=None):
        """Book seats either from a specified position or using default allocation.

        Args:
            num_tickets (int): Number of tickets to book
            start_pos (str, optional): Starting seat position (e.g., 'A1'). Defaults to None.

        Returns:
            tuple: (booking_id, list of seat positions) or (None, None) if booking failed
        """
        with self.lock:  # Acquire lock for booking operation
            # Check if enough seats are available
            if num_tickets > self.available_seats:
                return None, None

            # Create a temporary representation of all seats
            temp_seats = self._create_temp_seats_map()

            # Select seats based on allocation strategy
            if start_pos:
                # Custom seat selection
                selected_seats = self._allocate_from_custom_position(temp_seats, num_tickets, start_pos)
                if not selected_seats:
                    return None, None
            else:
                # Default allocation - starting from row 0 (closest to screen)
                selected_seats = self._allocate_default_seats(temp_seats, num_tickets)

            # Update the seat display for visualization
            self.seats = [row[:] for row in temp_seats]

            # Generate booking ID
            booking_id = f"GIC{self.current_booking_id:04d}"

            return booking_id, selected_seats

    def confirm_booking(self, booking_id, selected_seats):
        """Confirm and save the booking.

        Args:
            booking_id (str): The booking ID to confirm
            selected_seats (list): List of (row, col) tuples representing selected seats

        Returns:
            str: The confirmed booking ID
        """
        self.bookings[booking_id] = selected_seats
        self.current_booking_id += 1
        self.available_seats -= len(selected_seats)

        # Update the actual seats status to mark booked seats
        for row, col in selected_seats:
            self.seats[row][col] = '#'

        return booking_id

    def check_booking(self, booking_id):
        """Check an existing booking and highlight it in the seat display.

        Args:
            booking_id (str): The booking ID to check

        Returns:
            list: List of (row, col) tuples for the booking, or None if not found
        """
        if booking_id not in self.bookings:
            return None

        # Reset seats to '.' for visualization
        temp_seats = [['.' for _ in range(self.seats_per_row)] for _ in range(self.rows)]

        # Mark all bookings
        for bid, booking_seats in self.bookings.items():
            for row, col in booking_seats:
                if bid == booking_id:
                    temp_seats[row][col] = 'o'  # Highlight the requested booking
                else:
                    temp_seats[row][col] = '#'  # Other bookings

        # Update display
        self.seats = temp_seats

        return self.bookings.get(booking_id)