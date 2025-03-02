class Booking:
    def __init__(self, cinema):
        self.cinema = cinema

    def display_menu(self):
        print("\nWelcome to GIC Cinemas")
        print(f"[1] Book tickets for {self.cinema.title} ({self.cinema.available_seats} seats available)")
        print("[2] Check bookings")
        print("[3] Exit")

    def book_tickets(self):
        while True:
            try:
                num_tickets_input = input(
                    "\nEnter number of tickets to book, or enter blank to go back to main menu:\n> ")
                if not num_tickets_input:
                    break
                num_tickets = int(num_tickets_input)
                if num_tickets <= 0:
                    print("Number of tickets must be greater than 0.")
                    continue

                booking_id, selected_seats = self.cinema.book_seats(num_tickets)

                if booking_id:
                    print(f"\nSuccessfully reserved {num_tickets} {self.cinema.title} tickets.")
                    print(f"Booking id: {booking_id}")
                    print("Selected seats:")
                    self.cinema.display_seats()

                    while True:
                        new_seat_input = input(
                            "\nEnter blank to accept seat selection, or enter new seating position:\n> ")
                        if not new_seat_input:
                            # Confirm the booking
                            self.cinema.confirm_booking(booking_id, selected_seats)
                            print(f"Booking id: {booking_id} confirmed.")
                            break

                        new_booking_id, new_selected_seats = self.cinema.book_seats(num_tickets, new_seat_input)
                        if new_booking_id:
                            booking_id = new_booking_id
                            selected_seats = new_selected_seats
                            print(f"Booking id: {booking_id}")
                            print("Selected seats:")
                            self.cinema.display_seats()
                        else:
                            print("Invalid seat selection or seats already taken.")
                    break
                else:
                    print(f"Sorry, there are only {self.cinema.available_seats} seats available.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def check_bookings(self):
        while True:
            booking_id_input = input("\nEnter booking id, or enter blank to go back to main menu:\n> ")
            if not booking_id_input:
                break
            selected_seats = self.cinema.check_booking(booking_id_input)
            if selected_seats:
                print(f"Booking id: {booking_id_input}")
                print("Selected seats:")
                self.cinema.display_seats()
            else:
                print("Invalid booking id.")