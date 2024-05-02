import mysql.connector
from db_operations import db_operations

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

class HotelManageApp:

    def create_tables(self):
        db_ops.create_hotel_table()
        db_ops.create_staff_table()
        db_ops.create_roomType_table()
        db_ops.create_room_table()
        db_ops.create_guest_table()
        db_ops.create_booking_table()
        db_ops.create_payment_table()

    def populate_sample_data(self):
    # Inserting data into the HOTEL table
        #db_ops.create_hotel("Hilton Anaheim", "777 W Convention Way, Anaheim, CA 92802", "(714) 750-4321", 4.1)
        #db_ops.create_hotel("Hyatt Regency Orange County", "11999 Harbor Blvd. Garden Grove, California, 92840", "(714) 750-1234", 4.5)
        #db_ops.create_hotel("Marriott Suites Anaheim", "12015 Harbor Blvd, Garden Grove, CA 92840", "(714) 750-1000", 4.0)

    # Inserting data into the STAFF table
        db_ops.create_staff("John Jones", 1, "Sales Manager", "2016-04-25", "(714) 665-1554", "Jones@HiltonAnaheim.com")
        db_ops.create_staff("Kate Brown", 1, "Concierge", "2022-08-13", "(714) 445-5578", "Brown@HiltonAnaheim.com")
        db_ops.create_staff("Annie Smith", 2, "Assistant Manager", "2017-11-05", "(626) 401-9987", "Smith@HyattRegencyOC.com")

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
        #db_ops.create_payment("2018-01-30", "Debit", 1)
        #db_ops.create_payment("2023-09-25", "Credit", 2)
        #db_ops.create_payment("2024-07-22", "Cash", 3)


    def startScreen(self):
        # Start screen logic goes here
        # For example:
        print("Welcome to the Hotel Management App!")
        # You can add more options or functionality here

# Instantiate the HotelManageApp class and start the application
app = HotelManageApp()
#app.create_tables()
app.populate_sample_data()
app.startScreen()
# Close the connection
conn.close()
