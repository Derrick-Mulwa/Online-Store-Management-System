import mysql.connector

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
       "phone_number int UNIQUE,"
       "email_address VARCHAR(150) UNIQUE,"
       "home_address VARCHAR(60),"
       "loyalty_points int );")

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
       "phone_number int UNIQUE,"
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
       "sales_id INT UNIQUE,"
       "product_id INT,"
       "shipper_id INT,"
       "reason_for_return VARCHAR(2000)"
       ");")

    # Create table suppliers_details to store supplier's information
    me("CREATE TABLE suppliers_details("
       "supplier_id INT PRIMARY KEY AUTO_INCREMENT,"
       "suppliers_name VARCHAR(200),"
       "location VARCHAR(100),"
       "phone_number INT UNIQUE,"
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
       "phone_number INT,"
       "email VARCHAR(200) UNIQUE,"
       "headquarter_location VARCHAR(200) );")

    # Create customers_payments_details table to store payment options for the customers
    me("CREATE TABLE customers_payments_details("
       "payment_method_id int PRIMARY KEY AUTO_INCREMENT,"
       "customer_username VARCHAR(200),"
       "company_payment_method_id INT,"
       "payment_details VARCHAR(200)"
       ");")

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
