from datetime import datetime, date, time
import mysql.connector
import smtplib
import random
import main


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


mycursor.execute("USE retail_store;")
mycursor.execute("SELECT last_action_id FROM last_action_acted WHERE acting_id = 1;")
last_acted_id = [i for i in mycursor][0][0]

mycursor.execute("USE retail_store;")
mycursor.execute("SELECT action_id FROM retail_store.actions_recorder order by action_id DESC LIMIT 1;")
data = [i for i in mycursor]

print(f"Last acted id: {last_acted_id}\ncurrent_id: {data}")

