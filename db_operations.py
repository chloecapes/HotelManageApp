#import MySQL
import mysql.connector
from helper import helper
import random
from datetime import datetime

class db_operations():
    # constructor with connection path to DB
    def __init__(self, conn):
        self.connection = conn
        self.cursor = conn.cursor()
        print("Connection made..")

    def execute_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        print("Query executed successfully!")

    # function to simply execute a DDL or DML query.
    # commits query, returns no results. 
    # best used for insert/update/delete queries with no parameters
    def modify_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    # function to simply execute a DDL or DML query with parameters
    # commits query, returns no results. 
    # best used for insert/update/delete queries with named placeholders
    def modify_query_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()

    # function to simply execute a DQL query
    # does not commit, returns results
    # best used for select queries with no parameters
    def select_query(self, query):
        result = self.cursor.execute(query)
        return result.fetchall()
    
    # function to simply execute a DQL query with parameters
    # does not commit, returns results
    # best used for select queries with named placeholders
    def select_query_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        result = self.cursor.fetchall() if self.cursor else None
        return result if result else []


    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with no parameters
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with named placeholders
    def single_record_params(self, query, params):
        self.cursor.execute(query, params)
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None

    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with no parameters
    def single_attribute(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        results.remove(None)
        return results
    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with named placeholders
    def single_attribute_params(self, query, dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results
    
    # function for bulk inserting records
    # best used for inserting many records with parameters
    def bulk_insert(self, query, data):
        self.cursor.executemany(query, data)
        self.connection.commit()

    def create_hotel_table(self):
        query = '''
        CREATE TABLE hotel (
            HotelID INTEGER NOT NULL PRIMARY KEY,
            Name VARCHAR(50),
            Address VARCHAR(150),
            PhoneNumber VARCHAR(25),
            Rating DOUBLE
        );
        '''
        self.cursor.execute(query)
        print('Hotel table created')

    def create_staff_table(self):
        query = '''
        CREATE TABLE staff (
            StaffID INTEGER NOT NULL PRIMARY KEY,
            HotelID INTEGER,
            Name VARCHAR(50),
            Position VARCHAR(150),
            HireDate DATETIME,
            PhoneNumber VARCHAR(25),
            Email VARCHAR(150),
            FOREIGN KEY (HotelID) REFERENCES hotel(HotelID)
        );
        '''
        self.cursor.execute(query)
        print('Staff table created')

    def create_roomType_table(self):
        query = '''
        CREATE TABLE roomType (
            TypeID INTEGER NOT NULL PRIMARY KEY,
            Name VARCHAR(50),
            NumBeds INTEGER,
            NumBaths INTEGER,
            PricePerNight INTEGER
        );
        '''
        self.cursor.execute(query)
        print('RoomType table created')

    def create_room_table(self):
        query = '''
        CREATE TABLE room (
            RoomID INTEGER NOT NULL PRIMARY KEY,
            RoomNumber INTEGER,
            VacancyStatus BOOLEAN,
            TypeID INTEGER,
            HotelID INTEGER,
            FOREIGN KEY (TypeID) REFERENCES roomType(TypeID),
            FOREIGN KEY (HotelID) REFERENCES hotel(HotelID)
        );
        '''
        self.cursor.execute(query)
        print('Room table created')


    def create_guest_table(self):
        query = '''
        CREATE TABLE guest (
            GuestID INTEGER NOT NULL PRIMARY KEY,
            Name VARCHAR(50),
            PhoneNumber VARCHAR(25),
            Email VARCHAR(150)
        );
        '''
        self.cursor.execute(query)
        print('Guest table created')

    def create_booking_table(self):
        query = '''
        CREATE TABLE booking (
            BookingID INTEGER NOT NULL PRIMARY KEY,
            CheckInDate DATETIME,
            CheckoutDate DATETIME,
            TotalPrice INTEGER,
            GuestID INTEGER,
            RoomID INTEGER,
            FOREIGN KEY (GuestID) REFERENCES guest(GuestID),
            FOREIGN KEY (RoomID) REFERENCES room(RoomID)
        );
        '''
        self.cursor.execute(query)
        print('Booking table created')

    def create_payment_table(self):
        query = '''
        CREATE TABLE payment (
            PaymentID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            PaymentDate DATETIME,
            PaymentMethod VARCHAR(150),
        );
        '''
        self.cursor.execute(query)
        print('Payment table created')

    def create_hotelRatings_table(self):
        query = '''
                CREATE TABLE hotel_ratings (
                RatingID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                HotelID INT NOT NULL,
                Rating INT NOT NULL,
                CONSTRAINT fk_hotel_ratings_hotel FOREIGN KEY (HotelID) REFERENCES hotel(HotelID)
            )
            '''
        self.cursor.execute(query)
        print('HotelRatings table created')


    # Function to create a new hotel entry
    def create_hotel(self, name, address, phone_number, rating):
        query = '''
        SELECT MAX(HotelID) FROM hotel
        '''
        self.cursor.execute(query)
        last_hotel_id = self.cursor.fetchone()[0]  # Get the maximum HotelID
        new_hotel_id = last_hotel_id + 1 if last_hotel_id else 1  # Increment by 1 if there is a last hotel ID, otherwise start from 1

        insert_query = '''
        INSERT INTO hotel (HotelID, Name, Address, PhoneNumber, Rating) 
        VALUES (%s, %s, %s, %s, %s)
        '''
        self.cursor.execute(insert_query, (new_hotel_id, name, address, phone_number, rating))
        self.connection.commit()
        return new_hotel_id


    # Function to create a new staff member entry
    def create_staff(self, name, hotel_id, position, hire_date, phone_number, email):
        query = '''
        SELECT MAX(StaffID) FROM staff
        '''
        self.cursor.execute(query)
        last_staff_id = self.cursor.fetchone()[0]
        new_staff_id = last_staff_id + 1 if last_staff_id else 1

        insert_query = '''
        INSERT INTO staff (StaffID, HotelID, Name, Position, HireDate, PhoneNumber, Email) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        self.cursor.execute(insert_query, (new_staff_id, hotel_id, name, position, hire_date, phone_number, email))
        self.connection.commit()
        return new_staff_id

    # Function to create a new room type entry
    def create_room_type(self, name, num_beds, num_baths, price_per_night):
        query = '''
        SELECT MAX(TypeID) FROM roomType
        '''
        self.cursor.execute(query)
        last_type_id = self.cursor.fetchone()[0]
        new_type_id = last_type_id + 1 if last_type_id else 1

        insert_query = '''
        INSERT INTO roomType (TypeID, Name, NumBeds, NumBaths, PricePerNight) 
        VALUES (%s, %s, %s, %s, %s)
        '''
        self.cursor.execute(insert_query, (new_type_id, name, num_beds, num_baths, price_per_night))
        self.connection.commit()
        return new_type_id


    # Function to create a new room entry
    def create_room(self, room_number, vacancy_status, type_id, hotel_id):
        query = '''
        SELECT MAX(RoomID) FROM room
        '''
        self.cursor.execute(query)
        last_room_id = self.cursor.fetchone()[0]
        new_room_id = last_room_id + 1 if last_room_id else 1

        insert_query = '''
        INSERT INTO room (RoomID, RoomNumber, VacancyStatus, TypeID, HotelID) 
        VALUES (%s, %s, %s, %s, %s)
        '''
        self.cursor.execute(insert_query, (new_room_id, room_number, vacancy_status, type_id, hotel_id))
        self.connection.commit()
        return new_room_id


    # Function to create a new guest entry
    def create_guest(self, name, phone_number, email):
        query = '''
        SELECT MAX(GuestID) FROM guest
        '''
        self.cursor.execute(query)
        last_guest_id = self.cursor.fetchone()[0]
        new_guest_id = last_guest_id + 1 if last_guest_id else 1

        insert_query = '''
        INSERT INTO guest (GuestID, Name, PhoneNumber, Email) 
        VALUES (%s, %s, %s, %s)
        '''
        self.cursor.execute(insert_query, (new_guest_id, name, phone_number, email))
        self.connection.commit()
        return new_guest_id


    def create_booking(self, check_in_date, checkout_date, total_price, guest_id, room_id):
        query = '''
        SELECT MAX(BookingID) FROM booking
        '''
        self.cursor.execute(query)
        last_booking_id = self.cursor.fetchone()[0]
        new_booking_id = last_booking_id + 1 if last_booking_id else 1

        insert_query = '''
        INSERT INTO booking (BookingID, CheckInDate, CheckoutDate, TotalPrice, GuestID, RoomID) 
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        self.cursor.execute(insert_query, (new_booking_id, check_in_date, checkout_date, total_price, guest_id, room_id))
        self.connection.commit()
        return new_booking_id


    # Function to create a new payment entry
    def create_payment(self, payment_date, payment_method):
        insert_query = '''
        INSERT INTO payment (PaymentDate, PaymentMethod) 
        VALUES (%s, %s)
        '''
        self.cursor.execute(insert_query, (payment_date, payment_method))
        self.connection.commit()

        # Retrieve the last inserted payment ID
        new_payment_id = self.cursor.lastrowid

        return new_payment_id


    def create_account(self, user_type):
        name = input("Enter your name: ")
        phone_number = input("Enter your phone number: ")
        email = input("Enter your email: ")

        if user_type.lower() == 'staff':
            # Create a Staff account
            hotels = self.get_hotels_list()
            if hotels:
                print("Select the hotel you work at:")
                for i, hotel in enumerate(hotels, 1):
                    print(f"{i}. {hotel[1]}")  # Display hotel name with number
                choice = int(input("Enter the number corresponding to your hotel: "))
                if 1 <= choice <= len(hotels):
                    hotel_id = hotels[choice - 1][0]  # Get the hotel ID from the selected hotel
                    position = input("Enter your position: ")
                    hire_date = input("Enter your hire date (YYYY-MM-DD): ")
                    
                    staff_id = self.create_staff(name, hotel_id, position, hire_date, phone_number, email)
                    print(f"{user_type.capitalize()} account created successfully! Your ID is: {staff_id}")
                else:
                    print("Invalid choice. Please enter a valid number.")
            else:
                print("No hotels found in the database. Please add hotels first.")
            
        elif user_type.lower() == 'guest':
            # Create a Guest account
            guest_id = self.create_guest(name, phone_number, email)
            print(f"{user_type.capitalize()} account created successfully! Your ID is: {guest_id}")
        else:
            print("Invalid user type. Please choose either 'Staff' or 'Guest'.")

    # Function to check if a driver exists based on rider ID
    def staff_exists(self, staffID):
        query = '''
        SELECT COUNT(*)
        FROM staff
        WHERE staffID = %s
        '''
        result = self.single_record_params(query, (staffID,))
        return result > 0

    # Function to check if a rider exists based on rider ID
    def guest_exists(self, guestID):
        query = '''
        SELECT COUNT(*)
        FROM guest
        WHERE guestID = %s
        '''
        result = self.single_record_params(query, (guestID,))
        return result > 0


    def get_hotels_list(self):
        # Query the database to get the list of hotels
        query = '''SELECT Name 
                FROM hotel
                '''
        return self.select_query_params(query, {})
    
    def get_available_rooms(self, check_in_date, check_out_date, num_beds, num_baths):
        query = '''
                SELECT r.RoomID, h.Name AS HotelName, rt.Name AS RoomType, rt.PricePerNight
                FROM Room r
                INNER JOIN Hotel h ON r.HotelID = h.HotelID
                INNER JOIN RoomType rt ON r.TypeID = rt.TypeID
                WHERE rt.NumBeds >= %s AND rt.NumBaths >= %s
                AND r.RoomID NOT IN (
                    SELECT b.RoomID
                    FROM Booking b
                    WHERE (%s BETWEEN b.CheckInDate AND b.CheckOutDate)
                    OR (%s BETWEEN b.CheckInDate AND b.CheckOutDate)
                );
                '''
        params = (num_beds, num_baths, check_in_date, check_out_date)
        return self.select_query_params(query, params)

    def book_room(self, user_id, room_id, check_in_date, check_out_date, price_per_night):
        # Find the maximum BookingID currently in the database
        max_booking_id_query = '''
                                SELECT MAX(BookingID) 
                                FROM Booking
                                '''
        max_booking_id = self.single_record_params(max_booking_id_query, {})

        # If no bookings exist yet, set max_booking_id to 0
        if max_booking_id is None:
            max_booking_id = 0

        # Increment the max_booking_id to generate the new BookingID
        new_booking_id = max_booking_id + 1

        # Calculate the number of nights
        query = '''
                SELECT DATEDIFF(%s, %s)
                '''
        datediff_params = (check_out_date, check_in_date)
        num_nights = self.single_record_params(query, datediff_params)
        num_nights = int(num_nights)

        # Calculate the total price
        total_price = price_per_night * num_nights

        # Insert the new booking into the database
        insert_query = '''
                        INSERT INTO Booking (BookingID, GuestID, RoomID, CheckInDate, CheckOutDate, TotalPrice)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        '''
        booking_data = (new_booking_id, user_id, room_id, check_in_date, check_out_date, total_price)
        self.modify_query_params(insert_query, booking_data)

        # Retrieve the booking details
        booking_info_query = '''
                            SELECT *
                            FROM Booking
                            WHERE BookingID = %s
                            '''
        booking_info = self.single_record_params(booking_info_query, (new_booking_id,))

        # Print the booking information to the user
        print("Booking successful! Your booking details:")
        print("Booking ID:", new_booking_id)  
        print("Guest ID:", user_id)           
        print("Room ID:", room_id)           
        print("Check-in Date:", check_in_date)  
        print("Check-out Date:", check_out_date)  
        print("Total Price: $", total_price)   

    def checkIn_checkOut(self, user_id):
        # get room status based on user_id
        query = '''
            SELECT r.RoomID, r.VacancyStatus
            FROM booking b
            JOIN room r ON b.RoomID = r.RoomID
            WHERE b.GuestID = %s AND b.CheckInDate <= CURDATE() AND b.CheckOutDate >= CURDATE()
        '''
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        
        if result:
            room_id, vacancy_status = result
            if vacancy_status == 0:  # vacant
                update_query = '''
                    UPDATE room
                    SET VacancyStatus = 1
                    WHERE RoomID = %s
                '''
                self.cursor.execute(update_query, (room_id,))
                self.connection.commit()
                print("Checked in successfully!")
            else:  # occupied
                update_query = '''
                    UPDATE room
                    SET VacancyStatus = 0
                    WHERE RoomID = %s
                '''
                self.cursor.execute(update_query, (room_id,))
                self.connection.commit()
                print("Checked out successfully!")
        else:
            print("No booking found for the user or the booking dates are not valid.")

    def view_reservation(self, user_id, check_in_date):
        query = '''
                SELECT *
                FROM booking
                WHERE GuestID = %s AND CheckInDate = %s
                '''

        results = self.select_query_params(query, (user_id, check_in_date))
        if results:  
            print("Your current reservations are:")
            for booking in results:
                print("Booking ID:", booking[0])
                print("Guest ID:", booking[4])
                print("Room ID:", booking[5])
                print("Check-in Date:", booking[1])
                print("Check-out Date:", booking[2])
                print("Total Price: $", booking[3])
                print()
        else:
            print("You have not made any reservations under that date for the provided guest ID")


    def edit_reservation(self, check_in_date):
        # Check if the user has a reservation for the provided check-in date
        query = '''
                SELECT * FROM booking
                WHERE CheckInDate = %s
                '''
        booking_details = self.select_query_params(query, (check_in_date,))
        
        if not booking_details:
            print("You do not have a reservation for the provided check-in date.")
            return

        booking = booking_details[0]
        check_out_date = booking[2]
        room_id = booking[5]

        while True:
            print('''What would you like to edit?:
                    1. New Check-in Date
                    2. New Check-out Date
                    3. Change Room Type
                    4. Cancel Reservation
                    5. Go Back''')

            user_input = input("Enter the number corresponding to your choice: ")

            if user_input == '1':
                # New check-in date
                new_check_in_date = input("Enter your new check-in date (YYYY-MM-DD): ")

                # Check if the room is available for the new check-in date
                if self.is_room_available(room_id, new_check_in_date):
                    query = '''
                            UPDATE booking
                            SET CheckInDate = %s
                            WHERE CheckInDate = %s
                            '''
                    self.modify_query_params(query, (new_check_in_date, check_in_date))
                    print("Check-in date updated successfully!")
                    break
                else:
                    print("The room is not available for the selected check-in date. Please choose a different date.")

            elif user_input == '2':
                # New checkout date
                new_check_out_date = input("Enter your new check-out date (YYYY-MM-DD): ")

                # Check if the room is available for the new check-out date
                if self.is_room_available(room_id, new_check_out_date):
                    query = '''
                            UPDATE booking
                            SET CheckoutDate = %s
                            WHERE CheckInDate = %s
                            '''
                    self.modify_query_params(query, (new_check_out_date, check_in_date))
                    print("Check-out date updated successfully!")
                    break
                else:
                    print("The room is not available for the selected check-out date. Please choose a different date.")

            elif user_input == '3':
                # Change Room Type
                num_beds = int(input("Enter the desired number of beds: "))
                num_baths = int(input("Enter the desired number of bathrooms: "))

                # Retrieve available room options based on user input
                available_rooms = self.get_available_rooms(check_in_date, check_out_date, num_beds, num_baths)

                if available_rooms:
                    print("Available room options:")
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
                    selected_room_id, _, _, _ = selected_room

                    # Update the reservation with the selected room ID
                    query = '''
                            UPDATE booking
                            SET RoomID = %s
                            WHERE CheckInDate = %s
                            '''
                    self.modify_query_params(query, (selected_room_id, check_in_date))
                    print("Room type updated successfully!")
                    break

                else:
                    print("No available rooms matching the criteria. Please try again later.")

            elif user_input == '4':
                confirm_cancel = input("Are you sure you want to cancel your reservation? (yes/no): ")
                if confirm_cancel.lower() == "yes":
                    # Check if the trigger already exists
                    trigger_check_query = '''
                                        SHOW TRIGGERS 
                                        LIKE 'Delete_booking_payments'
                                        '''
                    self.cursor.execute(trigger_check_query)
                    existing_trigger = self.cursor.fetchone()

                    if not existing_trigger:
                        # Create trigger if it doesn't exist
                        create_trigger_query = '''
                                                CREATE TRIGGER Delete_booking_payments
                                                AFTER DELETE ON booking
                                                FOR EACH ROW
                                                BEGIN
                                                    DELETE FROM payment
                                                    WHERE BookingID = OLD.BookingID;
                                                END;
                                                '''
                        self.execute_query(create_trigger_query)

                    #delete the booking
                    delete_booking_query = '''
                                            DELETE FROM booking
                                            WHERE CheckInDate = %s
                                            '''
                    self.modify_query_params(delete_booking_query, (check_in_date,))
                    
                    print("Your reservation has been cancelled.")
                else:
                    print("Cancellation aborted.")
                break

            elif user_input == '5':
                # Return to the view/edit reservation menu
                return


    def is_room_available(self, RoomID, new_date):
        #check if the room is available for the given date
        query = '''
                SELECT COUNT(*)
                FROM booking
                WHERE RoomID = %s
                AND %s BETWEEN CheckInDate AND CheckOutDate
                '''
        # Execute the query with room_id and date as parameters
        result = self.single_record_params(query, (RoomID, new_date))

        # If result is 0, the room is available for the given date; otherwise, it's booked
        return result == 0

    def get_booking_id(self, user_id, check_in_date):
        query = '''
                SELECT BookingID
                FROM booking
                WHERE GuestID = %s AND CheckInDate = %s
                '''
        self.cursor.execute(query, (user_id, check_in_date))

        result = self.cursor.fetchone()
        if result:
            return result[0]  # Return the booking ID if found
        else:
            return None  # Return None if no booking ID found for the given user ID and check-in date

    def add_booking_payment(self, booking_id, payment_id):
        query = '''
                UPDATE Booking
                SET PaymentID = %s
                WHERE BookingID = %s
                '''
        self.modify_query_params(query, (payment_id, booking_id))


    def add_hotel_rating(self, hotel_id, rating):
        query = '''
                INSERT INTO hotel_ratings (HotelID, Rating)
                VALUES (%s, %s)
                '''
        self.cursor.execute(query, (hotel_id, rating))
        self.connection.commit()

    def calculate_average_rating(self, hotel_id):
        query = ''' 
                SELECT AVG(Rating) 
                FROM hotel_ratings 
                WHERE HotelID = %s
                '''
        self.cursor.execute(query, (hotel_id,))
        average_rating = self.cursor.fetchone()[0]
        return average_rating

    # destructor that closes connection with DB
    def destructor(self):
        self.cursor.close()
        self.connection.close()