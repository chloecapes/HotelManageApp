import mysql.connector
from db_operations import db_operations
from helper import helper
import datetime
import streamlit as st

# Connect to the database with correct casing
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CPSC408!",
    auth_plugin='mysql_native_password',
    database="HotelApp"
)

# Instantiate db_operations object with the connection
db_ops = db_operations(conn)
st.title('Hotel Management App')

class HotelManageApp:

    #def create_tables(self):
        #db_ops.create_hotel_table()
        #db_ops.create_staff_table()
        #db_ops.create_roomType_table()
        #db_ops.create_room_table()
        #db_ops.create_guest_table()
        #db_ops.create_booking_table()
        #db_ops.create_payment_table()
        #db_ops.create_hotelRatings_table()

    #def populate_sample_data(self):
    # Inserting data into the HOTEL table
        #db_ops.create_hotel("Hilton Anaheim", "777 W Convention Way, Anaheim, CA 92802", "(714) 750-4321", 4.1)
        #db_ops.create_hotel("Hyatt Regency Orange County", "11999 Harbor Blvd. Garden Grove, California, 92840", "(714) 750-1234", 4.5)
        #db_ops.create_hotel("Marriott Suites Anaheim", "12015 Harbor Blvd, Garden Grove, CA 92840", "(714) 750-1000", 4.0)

    # Inserting data into the STAFF table
        #db_ops.create_staff("John Jones", 1, "Sales Manager", "2016-04-25", "(714) 665-1554", "Jones@HiltonAnaheim.com")
        #db_ops.create_staff("Kate Brown", 1, "Concierge", "2022-08-13", "(714) 445-5578", "Brown@HiltonAnaheim.com")
        #db_ops.create_staff("Annie Smith", 2, "Assistant Manager", "2017-11-05", "(626) 401-9987", "Smith@HyattRegencyOC.com")

    # Inserting data into the ROOM TYPE table
        #db_ops.create_room_type("King Room", 1, 1, 195)
        #db_ops.create_room_type("2 Queen Beds", 2, 1, 155)
        #db_ops.create_room_type("VIP Suite", 2, 2, 275)
        
    # Inserting data into the ROOM table
        #db_ops.create_room(101, True, 1, 1)
        #db_ops.create_room(102, True, 2, 1)
        #db_ops.create_room(103, False, 2, 1)

    # Inserting data into the GUEST table
        #db_ops.create_guest("Aidan Johnson", "(665) 408-9974", "AJohnson@gmail.com")
        #db_ops.create_guest("Cary Jameson", "(435) 335-2214", "CJameson@hotmail.com")
        #db_ops.create_guest("Vivienne West", "(818) 467-0943", "WestVivienne@gmail.com")

    # Inserting data into the BOOKING table
        #db_ops.create_booking("2024-01-24", "2024-01-28", 652, 1, 1)
        #db_ops.create_booking("2024-02-22", "2024-02-24", 288, 2, 2)
        #db_ops.create_booking("2024-03-04", "2024-03-07", 557, 3, 3)

    # Inserting data into the PAYMENT table
        #db_ops.create_payment("2018-01-30", "Debit")
        #db_ops.create_payment("2023-09-25", "Credit")
        #db_ops.create_payment("2024-07-22", "Cash")


    def startScreen(self):
        # Start screen logic goes here
        print("Welcome to the Hotel Management App!")
        self.options()        

    def options(self):
        print('''Select from the following menu options: 
            1. New User
            2. Guest Login
            3. Exit''')
        choice = helper.get_choice([1, 2, 3])
        if choice == 1:
            self.new_user()
            self.options()
        elif choice == 2:
            self.login('Guest')
        elif choice == 3:
            print("Goodbye!")

    def new_user(self):
        print("Creating a new account...")
        while True:  # Loop until valid input is provided
            user_type = input("Are you Staff or a Guest?: ").lower()
            if user_type in ['staff', 'guest']:
                db_ops.create_account(user_type)
                break  # Exit the loop after successful account creation
            else:
                print("Invalid choice. Please try again.")
        self.options()  # After account creation, return to the options menu

    def login(self, user_type):
        print(f"Logging in as {user_type}...")
        user_id = int(input("Enter your ID: "))  
        account_exists = False

        if user_type == 'Staff':
            account_exists = db_ops.staff_exists(user_id)
        elif user_type == 'Guest':
            account_exists = db_ops.guest_exists(user_id)

        if account_exists:
            print(f"{user_type.capitalize()} logged in successfully!")
            if user_type == 'Staff':
                #don't have time to implement but want to in future
               pass
            elif user_type == 'Guest':
                self.guest_options(user_id)  # Call guest_options method here
        else:
            print(f"Error: {user_type.capitalize()} account with ID {user_id} does not exist.")


    def guest_options(self, user_id):
        print('''Guest Options: 
            1. Make a hotel reservation
            2. View or edit hotel reservation
            3. Check-in/Checkout
            4. Make a payment
            5. Rate Hotel
            6. Back to Main Menu''')
        choice = helper.get_choice([1, 2, 3, 4, 5, 6])

        if choice == 1:
            #make hotel reservation
            self.make_hotel_reservation(user_id)
            self.guest_options(user_id)

        elif choice == 2:
            #view or edit hotel reservation  
            while True:  # Loop until valid input is provided
                user_type = input(
                    '''What would you like to do? (Enter choice number):
                        1. View Hotel Reservation
                        2. Edit Hotel Reservation
                        3. Return to Guest Options
                        ''')
                if user_type == '1':
                    check_in_date = input("Enter your check-in date (YYYY-MM-DD): ")
                    db_ops.view_reservation(user_id, check_in_date)
                elif user_type == '2':
                    check_in_date = input("Enter your check-in date (YYYY-MM-DD): ")
                    db_ops.edit_reservation(check_in_date)
                    break
                elif user_type == '3':
                    self.guest_options(user_id)
                else:
                    print("Invalid choice. Please try again.")
            self.guest_options(user_id)

        elif choice == 3:
            #Check-in/Checkout
            db_ops.checkIn_checkOut(user_id)
            self.guest_options(user_id)
        
        elif choice == 4:
            # Make a payment
            check_in_date = input("Enter your check-in date (YYYY-MM-DD): ")
            payment_method = input("How will you be paying? Cash, Debit, or Credit? ").lower()
            payment_date = datetime.date.today()  # Get current date
            
            # Query the table to get the booking ID based on the user ID and check-in date
            booking_id = db_ops.get_booking_id(user_id, check_in_date)
            
            # Create the payment
            payment_id = db_ops.create_payment(payment_date, payment_method)

            db_ops.add_booking_payment(booking_id, payment_id)

            print("You have successfully paid for your stay! Thanks!")
            self.guest_options(user_id)

        elif choice == 5:
            # Rate Hotel
            # Display available hotels for the guest to choose from
            print("Which Hotel are you rating?:")
            hotels = db_ops.get_hotels_list()  
            for i, hotel in enumerate(hotels, start=1):
                print(f"{i}. {hotel[0]}")  # Access the first element of the tuple (hotel name)

            # Prompt the guest to enter the number corresponding to the hotel they want to rate
            hotel_id = int(input("Enter the number corresponding to the hotel you want to rate: "))

            rating = int(input("What would you rate your experience on a scale of 1 to 5?: "))
            # Store the user's rating in the database
            db_ops.add_hotel_rating(hotel_id, rating)
            print("Thank you for your feedback!")
            self.guest_options(user_id)

        elif choice == 6:
            #Back to Main Menu
            self.options()  # Return to main menu

        else:
            print("Invalid choice. Please try again.")
            self.guest_options(user_id)  # Retry guest options if choice is invalid
    
    def make_hotel_reservation(self, user_id):
        # Input check-in and check-out dates
        check_in_date = input("Enter your check-in date (YYYY-MM-DD): ")
        check_out_date = input("Enter your check-out date (YYYY-MM-DD): ")

        # Input room preferences
        num_beds = int(input("Enter the number of beds you prefer: "))
        num_baths = int(input("Enter the number of baths you prefer: "))

        # Query the database to retrieve all vacant rooms matching the guest's preferences
        available_rooms = db_ops.get_available_rooms(check_in_date, check_out_date, num_beds, num_baths)

        # Display the list of available rooms to the user
        if available_rooms:
            print("Available Rooms:")
            for i, room in enumerate(available_rooms, 1):
                room_id, hotel_name, room_type, price_per_night = room
                print(f"{i}. Room ID: {room_id}, Hotel: {hotel_name}, Room Type: {room_type}, Price per Night: ${price_per_night}")

            selected_room_index = input("Enter the number of the room you want to book, or 'back' to return to the menu: ")

            if selected_room_index.lower() == 'back':
                return  # Return to the menu

            selected_room_index = int(selected_room_index)
            if selected_room_index not in range(1, len(available_rooms) + 1):
                print("Invalid room number. Please try again.")
                return

            selected_room = available_rooms[selected_room_index - 1]
            room_id, _, _, price_per_night = selected_room

            # Book the selected room
            db_ops.book_room(user_id, room_id, check_in_date, check_out_date, price_per_night)
        else:
            print("No available rooms match your preferences.")


# Instantiate the HotelManageApp class and start the application
app = HotelManageApp()
app.startScreen()

# Close the connection
conn.close()
