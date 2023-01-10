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





