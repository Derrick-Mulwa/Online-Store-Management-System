import mysql.connector
import smtplib
import random
from datetime import datetime

# Try to connect to the database
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Firefly."
    )

    my_cursor = db.cursor()
    me = my_cursor.execute

except:
    print("Error connecting to database!")


# The function create_database_and_tables below creates the store's database and appropriate tables that will store the
# stores customers', products', payments'', employees'' and shipping information

def create_database_and_tables():
    # Create database
    me("DROP DATABASE IF EXISTS retail_store;")
    me("CREATE DATABASE retail_store;")
    me("USE retail_store;")
    # Create customers table to store the customer's details
    me("CREATE TABLE customers("
       "customer_username VARCHAR(100) PRIMARY KEY,"
       "first_name VARCHAR(100),"
       "last_name VARCHAR(100),"
       "gender VARCHAR(50),"
       "date_of_birth DATE,"
       "phone_number VARCHAR(100) UNIQUE,"
       "email_address VARCHAR(150) UNIQUE,"
       "home_address VARCHAR(60),"
       "loyalty_points int );")


    # Create a table to store users login credentials
    me("CREATE TABLE login_credentials("
       "customer_username VARCHAR(100) PRIMARY KEY,"
       "password VARCHAR(100))")

    # Create order's table to store the data of an order placed by a customer
    me("CREATE TABLE orders("
       "order_id INT PRIMARY KEY AUTO_INCREMENT,"
       "customer_username VARCHAR(100),"
       "order_date DATETIME,"
       "shipping_status VARCHAR(100),"
       "payment_method_id INT,"
       "ordered_items VARCHAR(1000),"
       "shipper_id int"
       ");")


    # Create the Products' table to store the details of items on sale
    me("CREATE TABLE products("
       "product_id INT PRIMARY KEY AUTO_INCREMENT,"
       "product_name VARCHAR(200),"
       "product_price DECIMAL(9, 2),"
       "product_category_id INT,"
       "reviews int DEFAULT 0,"
       "rating int,"
       "remaining_in_stock int,"
       "product_description VARCHAR(100),"
       "product_image LONGBLOB"
       ")")
    # Create product_category table that stores product's categories
    me("CREATE TABLE product_category("
       "category_id INT PRIMARY KEY AUTO_INCREMENT,"
       "category_name VARCHAR(200));")

    # Create the inventory table to keep track of the stock
    me("CREATE TABLE inventory("
       "inventory_id INT PRIMARY KEY AUTO_INCREMENT,"
       "product_id INT,"
       "max_stock INT,"
       "min_stock INT,"
       "remaining_stock INT"
       ")")

    # Create employees table to store the store's employees' data
    me("CREATE TABLE employees("
       "employee_id INT PRIMARY KEY,"
       "first_name VARCHAR(100),"
       "last_name VARCHAR(100),"
       "email_address VARCHAR(100) UNIQUE,"
       "phone_number VARCHAR(100) UNIQUE,"
       "job_title VARCHAR(100),"
       "salary DECIMAL(9,2),"
       "reports_to VARCHAR(100),"
       "home_address VARCHAR(100)"
       ")")

    # Create table sales that stores the sales made by the store
    me("CREATE TABLE sales("
       "sales_id INT PRIMARY KEY AUTO_INCREMENT,"
       "sale_time DATETIME,"
       "product_sold_id INT,"
       "sale_price DECIMAL(9,2)"
       ");")

    # Create returned_products table for items returned by the customer.
    me("CREATE TABLE returned_products("
       "returned_product_id INT PRIMARY KEY AUTO_INCREMENT,"
       "customer_username VARCHAR(100),"
       "order_id INT,"
       "sales_id INT UNIQUE,"
       "product_id INT,"
       "shipper_id INT,"
       "reason_for_return VARCHAR(2000),"
       "processing_status VARCHAR(100)"
       ");")

    # Create table suppliers_details to store supplier's information
    me("CREATE TABLE suppliers_details("
       "supplier_id INT PRIMARY KEY AUTO_INCREMENT,"
       "suppliers_name VARCHAR(200),"
       "location VARCHAR(100),"
       "phone_number VARCHAR(100) UNIQUE,"
       "email_address VARCHAR(100) UNIQUE,"
       "products_supplied_ids VARCHAR(100)"
       ");")

    # Create supplies table that records supplies details when made to the store
    me("CREATE TABLE supplies("
       "supply_id INT PRIMARY KEY AUTO_INCREMENT,"
       "time_of_supply DATETIME,"
       "supplier_id INT,"
       "product_supplied_id INT,"
       "number_of_products_supplies INT,"
       "total_price DECIMAL(9,2),"
       "price_per_item DECIMAL (9,2)"
       ");")

    # Create company_payment_methods for all the payment methods accepted by the company
    me("CREATE TABLE company_payment_methods("
       "payment_method_id int PRIMARY KEY AUTO_INCREMENT,"
       "payment_method_name VARCHAR(100),"
       "payment_method_description VARCHAR(1000)"
       ");")

    # Create table for the shippers
    me("CREATE TABLE shippers("
       "shipper_id INT PRIMARY KEY AUTO_INCREMENT,"
       "shipper_name VARCHAR(100),"
       "phone_number VARCHAR(100),"
       "email VARCHAR(200) UNIQUE,"
       "headquarter_location VARCHAR(200) );")

    # Create customers_payments_details table to store payment options for the customers
    me("CREATE TABLE customers_payments_details("
       "payment_method_id int PRIMARY KEY AUTO_INCREMENT,"
       "customer_username VARCHAR(200),"
       "company_payment_method_id INT,"
       "payment_details VARCHAR(200)"
       ");")

# Create table actions_recorder. This table record actions taking place in the tables ie new customer account created,
# new login attempt, new product returned, updating customer details, new employee, new order created, new
# supplier account created, sales made etc.
    me("CREATE TABLE actions_recorder("
       "action_id INT PRIMARY KEY AUTO_INCREMENT,"
       "action_taken VARCHAR(200),"
       "description VARCHAR(500))")

# Remainder table for security.py
    me("CREATE TABLE last_action_acted("
       "acting_id INT PRIMARY KEY AUTO_INCREMENT,"
       "last_action_id INT);")
    me("INSERT INTO last_action_acted(last_action_id) VALUES (1)")

    # UPDATE ALL FOREIGN KEYS USED TO LINK ALL TABLES
    # FOREIGN KEYS FOR THE ORDERS TABLE
    me("ALTER TABLE orders ADD CONSTRAINT fk_customer_username "
       "FOREIGN KEY (customer_username) REFERENCES customers(customer_username)"
       " ON DELETE SET NULL ON UPDATE CASCADE;")

    me("ALTER TABLE orders ADD CONSTRAINT fk_payment_method_id "
       "FOREIGN KEY (payment_method_id) REFERENCES customers_payments_details(payment_method_id)"
       " ON DELETE SET NULL ON UPDATE CASCADE;")

    me("ALTER TABLE orders ADD CONSTRAINT fk_shipper_id "
       "FOREIGN KEY (shipper_id) REFERENCES shippers(shipper_id)"
       " ON DELETE SET NULL ON UPDATE CASCADE;")

    # Create a foreign key on the login_credentials table
    me("ALTER TABLE login_credentials ADD CONSTRAINT fk_login_credentials_customer_username "
       "FOREIGN KEY (customer_username) REFERENCES customers(customer_username)"
       " ON DELETE CASCADE ON UPDATE CASCADE;")

    # product_category_id product_category(category_id),remaining_in_stock inventory(remaining_stock)
    # Foreign keys for product table
    me("ALTER TABLE products ADD CONSTRAINT fk_product_category_id "
       "FOREIGN KEY (product_category_id) REFERENCES product_category(category_id)"
       " ON DELETE SET NULL ON UPDATE CASCADE;")

    # Foreign keys for the inventory table
    me("ALTER TABLE inventory ADD CONSTRAINT fk_product_id "
       "FOREIGN KEY (product_id) REFERENCES products(product_id)"
       " ON DELETE SET NULL ON UPDATE CASCADE;")

    # Foreign keys on the sales table
    me("ALTER TABLE sales ADD CONSTRAINT fk_product_sold_id "
       "FOREIGN KEY (product_sold_id) REFERENCES products(product_id)"
       " ON DELETE SET NULL ON UPDATE CASCADE;")

    # Foreign key on returned_products table
    me("ALTER TABLE returned_products ADD CONSTRAINT fk_sales_id "
       "FOREIGN KEY (sales_id) REFERENCES sales(sales_id)"
       " ON DELETE SET NULL ON UPDATE CASCADE;")

    me("ALTER TABLE returned_products ADD CONSTRAINT fk_returned_products_product_id "
       "FOREIGN KEY (product_id) REFERENCES products(product_id)"
       " ON DELETE SET NULL ON UPDATE CASCADE;")

    me("ALTER TABLE returned_products ADD CONSTRAINT fk_returned_products_shipper_id "
       "FOREIGN KEY (shipper_id) REFERENCES shippers(shipper_id)"
       " ON DELETE SET NULL ON UPDATE CASCADE;")

    me("ALTER TABLE returned_products ADD CONSTRAINT fk_returned_products_customer_username "
       "FOREIGN KEY (customer_username) REFERENCES customers(customer_username) "
       "ON DELETE SET NULL ON UPDATE CASCADE")

    me("ALTER TABLE returned_products ADD CONSTRAINT fk_returned_products_order_id "
       "FOREIGN KEY (order_id) REFERENCES orders(order_id) "
       "ON DELETE SET NULL ON UPDATE CASCADE")

    # Foreign key on supplies table
    me("ALTER TABLE supplies ADD CONSTRAINT fk_supplies_supplier_id "
       "FOREIGN KEY (supplier_id) REFERENCES suppliers_details(supplier_id)"
       " ON DELETE SET NULL ON UPDATE CASCADE;")

    me("ALTER TABLE supplies ADD CONSTRAINT fk_product_supplied_id "
       "FOREIGN KEY (product_supplied_id) REFERENCES products(product_id)"
       " ON DELETE SET NULL ON UPDATE CASCADE;")

    # Foreign key for customers_payments_details
    me("ALTER TABLE customers_payments_details ADD CONSTRAINT fk_customers_payments_details_customer_username "
       "FOREIGN KEY (customer_username) REFERENCES customers(customer_username)"
       " ON DELETE SET NULL ON UPDATE CASCADE;")

    me("ALTER TABLE customers_payments_details ADD CONSTRAINT fk_customers_payments_details_payment_method_id "
       "FOREIGN KEY (company_payment_method_id) REFERENCES company_payment_methods(payment_method_id)"
       " ON DELETE SET NULL ON UPDATE CASCADE;")

# A function to reset users email in case of suspicious login activity by resetting password and sending it to
# user's email address'
def reset_customer_password(username):
    mycursor = db.cursor(())
    # Generate a new random password of 8 characters
    password_characters = 'abcdefghigklmnopqrstuvwxyz1234567890'
    password_characters = password_characters + password_characters.upper()
    reset_password = ''

    for i in range(8):
        reset_password += random.choice(password_characters)

    # Update password in the database.
    subject = "Security alert"

    mycursor.execute("USE retail_store;")
    mycursor.execute(f"SELECT first_name, email_address "
                     f"FROM retail_store.customers WHERE customer_username = '{username}'")
    details = [i for i in mycursor][0]
    user_first_name = details[0]
    receivers_email = details[1]

    mycursor.execute(f"UPDATE retail_store.login_credentials "
                     f"SET password = '{reset_password}' WHERE customer_username = '{username}'")
    db.commit()

    # Send email to the customer

    connection = smtplib.SMTP('64.233.184.108', 587)
    connection.ehlo()
    connection.starttls()
    connection.ehlo()
    connection.login("mbalukaderrik@gmail.com", "azratciiegqyupjc")

    message = f"subject: {subject}\n" \
              f"Hello {user_first_name}! \n\nWe noticed an unusual attempt to login to your Firefly Online Store " \
              f"account. Consequently, your password was reset to {reset_password} because of security reasons. \n\n" \
              f"Use this password to log in to your account next time. You can change the password after logging in." \
              f"\n\n\nFirefly Security Team."
    connection.sendmail(
        from_addr="mbalukaderrik@gmail.com",

        to_addrs=receivers_email,
        msg=message
    )
    action = "password_reset"
    reset_time = datetime.now()
    sql_statement = f"INSERT INTO retail_store.actions_recorder (action_taken, description) " \
                    f"VALUES ('{action}', '({username}, {reset_time})') "
    mycursor.execute(sql_statement)
    db.commit()


def create_new_customer_account():
    mycursor=db.cursor()
    print("Welcome to Firefly online store! \n"
          "Enter your credentials correctly to create your account. Starred* fields should not be blank!\n")

# Get existing usernames, phone number and email address to avoid duplication of usernames and ensure a customer has only
# one account
    mycursor.execute("USE retail_store;")
    mycursor.execute(f"SELECT customer_username, phone_number, email_address FROM retail_store.customers")
    data = [i for i in mycursor]
    existing_usernames = [i[0] for i in data]
    existing_phone_numbers = [i[1] for i in data]
    existing_email_address = [i[2] for i in data]

# Get customers First and last names
    customer_first_name = input("Enter your first name: ")
    while len(customer_first_name) > 100:
        customer_first_name = input("Your first name is too long. Please shorten it. Re-enter your first name: ")

    customer_last_name = input("Enter your last name: ")
    while len(customer_last_name) > 100:
        customer_last_name = input("Your last name is too long. Please shorten it. Re-enter your first name: ")

# Get unique customer's username that is not already registered'
    customer_username = input("Enter your username. This will be your unique identifier. "
                              "You can combine letters and numbers: ").lower()

    while len(customer_username) > 100 or customer_username in existing_usernames:
        customer_username = input("The username is either taken or is too long. Enter another : ")

# Get a secure password for the customer's account'
    verify_password = False
    while verify_password is False:
        customer_password = input("Enter password. "
                                  "Password MUST have at least 8 characters and MUST include a number: ")
        confirm_customer_password = input("Confirm password: ")
        if customer_password == confirm_customer_password:
            if len(customer_password) >= 8:
                number_inclusive = False
                for letter in customer_password:
                    try:
                        int(letter)
                        number_inclusive = True
                        verify_password = True
                    except:
                        continue
                if number_inclusive is False:
                    print("\nPassword does not have a number! Re-enter password. ")
            else:
                print("\nPassword is too short! Re-enter password. ")
        else:
            print("\nPasswords Do not match. Enter passwords again.")

# Get customers Gender
    customer_gender = input("Enter your gender(Enter M for male and F for female):").upper()
    while customer_gender not in ["M", "F"]:
        customer_gender = input("Incorrect input! Re-enter your gender(Enter M for male and F for female):").upper()
    if customer_gender == "M":
        customer_gender = "Male"
    else:
        customer_gender = "Female"

# Get the customers Date of Birt and ensure it is a valid date
    customer_date_of_birth = input("Enter your date of birth(YYYY-MM-DD): ")
    valid_date = False
    while valid_date is False:
        try:
            datetime.strptime(customer_date_of_birth, "%Y-%m-%d")
            valid_date = True
        except:
            customer_date_of_birth = input("Incorrect date format. Include(-). Enter your date of birth(YYYY-MM-DD): ")

    # Get a legit phone number with country code
    customer_phone_number = input("Enter your phone number, including country code (eg: 254712345678): ")
    valid_phone_number = False
    while valid_phone_number is False:
        if customer_phone_number not in existing_phone_numbers:
            if len(customer_phone_number) > 10:
                try:
                    customer_phone_number = int(customer_phone_number)
                    valid_phone_number = True
                except:
                    customer_phone_number = input("Enter Digits only! Re-enter your phone number, "
                                                  "including country code (eg: 254712345678): ")
            else:
                customer_phone_number = input("Phone number lacks country code! Re-enter your phone number, "
                                              "including country code (eg: 254712345678): ")
        else:
            customer_phone_number = input("Phone number is already linked to an account! \nEnter another phone number, "
                                          "including country code (eg: 254712345678): ")

    # Get a legitimate email from the customer. The email is verified by sending a OTP to the email and confirming it
    customer_email_address = input("Enter your email address: ").lower()
    verified_email_address = False
    while verified_email_address is False:
        if customer_email_address in existing_email_address:
            customer_email_address = input("Entered email address is already linked to an account. "
                                           "Use a different email address: ").lower()
        else:
            confirm_email = False
            while confirm_email is False:
                confirm_email_address = input("Confirm email address: ").lower()
                if confirm_email_address == customer_email_address:
                    confirm_email = True
                else:
                    customer_email_address = input(
                        "\nEmail address do not match! Enter email address(abc@xyz.com): ").lower()

            connection = smtplib.SMTP('64.233.184.108', 587)
            connection.ehlo()
            connection.starttls()
            connection.ehlo()
            connection.login("mbalukaderrik@gmail.com", "azratciiegqyupjc")

            otp = ""
            for i in range(6):
                otp = otp + str(random.randint(0, 9))

            subject = "Email verification"
            body = f"Welcome to Firefly Online Store. Your OTP is {otp}.\n" \
                   f"Enter the code to verify your email and complete your verification process.\n\n" \
                   f"Firefly Online Store"
            message = f"subject: {subject}\n\n{body}"
            connection.sendmail(
                from_addr="mbalukaderrik@gmail.com",

                to_addrs=customer_email_address,
                msg=message
            )

            user_otp = input(f"\nEnter the OPT code sent to {customer_email_address}. \n"
                             f"Check the spam folder if you cannot find the email in inbox: ")

            if user_otp == str(otp):
                print("Email verified successfully!")
                verified_email_address = True

            else:
                tries = 0
                verify_otp = False
                while tries < 3 and verify_otp is False:
                    user_otp = input(f"Wrong OTP.Re-enter the OPT code sent to {customer_email_address}: ")
                    tries += 1
                    if user_otp == str(otp):
                        print("Email verified successfully!")
                        verified_email_address = True
                        verify_otp = True
                if tries >= 3:
                    customer_email_address = input("You entered wrong OTP many times."
                                                   "Enter your email address (abc@xyz.com): ").lower()
    home_address = input("Enter your address (county/state, Country): ")
    loyalty_points = 1

    # Insert customers credentials to customers table
    user_details = (customer_username, customer_first_name, customer_last_name, customer_gender, customer_date_of_birth,
                    customer_phone_number, customer_email_address, home_address, loyalty_points)
    logins = (customer_username, customer_password)
    mycursor.execute("USE retail_store;")
    mycursor.execute(f"INSERT INTO retail_store.customers VALUES {user_details};")
    db.commit()
    mycursor.execute(f"INSERT INTO retail_store.login_credentials VALUES {logins};")
    db.commit()

    # Insert action in actions recorder table
    action = "newuser"
    created_time = datetime.now()
    sql_statement = f"INSERT INTO retail_store.actions_recorder (action_taken, description) " \
                    f"VALUES ('{action}', '({customer_username}, {created_time})') "
    mycursor.execute(sql_statement)
    db.commit()
