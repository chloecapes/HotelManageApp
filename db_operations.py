#import MySQL
import mysql.connector
from helper import helper
import random

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
    def single_record_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        return self.cursor.fetchone()[0]
    
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
            PaymentID INTEGER NOT NULL PRIMARY KEY,
            PaymentDate DATETIME,
            PaymentMethod VARCHAR(150),
            BookingID INTEGER,
            FOREIGN KEY (BookingID) REFERENCES booking(BookingID)
        );
        '''
        self.cursor.execute(query)
        print('Payment table created')

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
    def create_payment(self, payment_date, payment_method, booking_id):
        query = '''
        SELECT MAX(PaymentID) FROM payment
        '''
        self.cursor.execute(query)
        last_payment_id = self.cursor.fetchone()[0]
        new_payment_id = last_payment_id + 1 if last_payment_id else 1

        insert_query = '''
        INSERT INTO payment (PaymentID, PaymentDate, PaymentMethod, BookingID) 
        VALUES (%s, %s, %s, %s)
        '''
        self.cursor.execute(insert_query, (new_payment_id, payment_date, payment_method, booking_id))
        self.connection.commit()
        return new_payment_id





    # destructor that closes connection with DB
    def destructor(self):
        self.cursor.close()
        self.connection.close()