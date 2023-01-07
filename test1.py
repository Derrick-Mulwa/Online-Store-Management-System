me("ALTER TABLE orders ADD CONSTRAINT fk_customer_username "
   "FOREIGN KEY (customer_username) REFERENCES customers(customer_username)"
   "ON DELETE SET NULL "
   "ON UPDATE CASCADE")