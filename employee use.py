import mysql.connector
import smtplib
import random


try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Firefly."
    )

    mycursor = db.cursor()
    mycursor.execute("USE retail_store;")

except:
    print("Error connecting to database!")

user_details = ("abu1121", "Abu", "Boubakar", "Male", "1990-09-22", 25479938479, "mymail@yahoo.dob", "Kiambu, Kenya", 0)
mycursor.execute("USE retail_store;")
mycursor.execute(f"INSERT INTO retail_store.customers VALUES {user_details};")
db.commit()
