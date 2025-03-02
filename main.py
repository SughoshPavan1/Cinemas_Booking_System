from booking import Booking
from cinema import Cinema

def main():
    while True:
        try:
            movie_input = input("Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:\n> ")
            title, rows, seats_per_row = movie_input.split()
            rows = int(rows)
            seats_per_row = int(seats_per_row)
            if 1 <= rows <= 26 and 1 <= seats_per_row <= 50:
                break
            else:
                print("Invalid input. Row must be between 1 and 26, and seats per row must be between 1 and 50.")
        except ValueError:
            print("Invalid input format.")

    cinema = Cinema(title, rows, seats_per_row)
    booking = Booking(cinema)

    while True:
        booking.display_menu()
        try:
            selection = input("Please enter your selection:\n> ")
            if selection == '1':
                booking.book_tickets()
            elif selection == '2':
                booking.check_bookings()
            elif selection == '3':
                print("\nThank you for using GIC Cinemas system. Bye!")
                break
            else:
                print("Invalid selection. Please choose 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()