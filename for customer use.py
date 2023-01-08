import mysql.connector
import smtplib
import random

# Connect to database
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


def reset_customer_password(username):
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


def create_new_customer_account():
    print("Welcome to Firefly online store! \n"
          "Enter your credentials correctly to create your account. Starred* fields should not be blank!\n"
          "")


action = input("Welcome to Firefly online store!\n"
               "Press 1 to login or any other key to register a new account: ")

if action == "1":
    tries = 1
    while tries < 4:
        username = input("\nEnter your username: ")
        try:
            password_tries = 2
            mycursor.execute(f"SELECT * FROM login_credentials WHERE customer_username = '{username}'")
            real_password = [i for i in mycursor][0][1]
            tries = 4

            password = input("Enter your password: ")

            while password != real_password and password_tries > 0:
                password = input(f"\nIncorrect password! Enter password again. You have {password_tries} tries"
                                     f" remaining: ")
                password_tries -= 1

            if password == real_password:
                print("Login successful!")
            else:
                print("Login unsuccessful after four tries! We have reset your password and sent it to your email!")

                reset_customer_password(username)

        except:
            action = input("\nUsername entered DOES NOT exist! \n"
                           "Press 1 to create a new account or any other key to re-enter username:")
            if action == "1":
                create_new_customer_account()

            else:
                tries += 1
                continue
else:
    create_new_customer_account()

# print(password)

