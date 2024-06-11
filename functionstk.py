# functions.py
import mysql.connector
import tkinter.messagebox as tkmb
import customtkinter as ctk
import db_configtk
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont

username = os.environ.get("USERNAME")  # Retrieve environment variable
hpage = None

def login(user_entry, user_pass):
    # Connect to the MySQL database
    try:
        connection = mysql.connector.connect(**db_configtk.db_config)
        cursor = connection.cursor()
    
        # Perform a SELECT query to check the username and password
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (user_entry.get(), user_pass))
        result = cursor.fetchone()

        if result:
            print(user_entry.get()+" login"+" successful.")
            op=True
            return op
        else:
            tkmb.showerror(title="Login Failed", message="Invalid Username or password")

    except mysql.connector.Error as err:
        tkmb.showerror(title="Database Error", message=f"Error: {err}")

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

def signup(signup_user_entry, signup_user_pass, signup_email_entry, signup_phone_entry):
    try:
        dbc = mysql.connector.connect(**db_configtk.db_config)
        cursor = dbc.cursor()
        # Check if the username already exists
        check_query = "SELECT * FROM users WHERE username = %s or email = %s"
        check_data = (signup_user_entry.get(), signup_email_entry.get(),)
        #cursor.execute(check_query, (signup_user_entry.get(),signup_email_entry.get(),))
        cursor.execute(check_query,check_data)
        existing_user = cursor.fetchone()

        if not existing_user:
            # Insert into blog_author
            cursor.execute('INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)',
                        (signup_user_entry.get(),
                         signup_user_pass,
                         signup_email_entry.get(),
                         signup_phone_entry.get()))
            dbc.commit()
            tkmb.showinfo(title="Signup Successful", message="Account created successfully. You can now log in.")
            return True
        else:
            tkmb.showerror(title="Signup Failed", message="Username or email already exists. Please choose a different username.")
            
            
    except Exception as e:
        print('Error in signing up:', e)
        dbc.rollback()
        tkmb.showerror(title="Error", message="Operation Failed")

    finally:
        # Close the database connection
        if dbc.is_connected():
            cursor.close()
            dbc.close()

# Function to connect to the database and fetch data
def fetch_data():
    try:
        connection = mysql.connector.connect(**db_configtk.db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM posts ORDER BY id DESC")
        data = cursor.fetchall()

        return data

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_counter():
    try:
        connection = mysql.connector.connect(**db_configtk.db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT count(1) FROM posts")
        data = cursor.fetchone()  # Fetch one row
        count = data[0]

        return count

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def insert_post(image_path, text_data, heading, comments, user_name=username):
    try:
        connection = mysql.connector.connect(**db_configtk.db_config)
        cursor = connection.cursor()
        # Assuming your "posts" table has columns: id, image_path, text_data, username
        insert_query = "INSERT INTO posts (image_path, text_data, username, heading, comments, timestamp) VALUES (%s, %s, %s, %s, %s, NOW())"
        post_data = (image_path, text_data, user_name, heading, comments)
        cursor.execute(insert_query, post_data)
        connection.commit()
        print("Post added successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def validate_email(email):
    # Basic email format validation
    if "@" in email and "." in email:
        return True
    else:
        return False

def validate_phone(phone):
    # Basic phone number format validation
    if phone.isdigit() and len(phone) == 10:  # Assuming phone numbers are 10 digits long
        return True
    else:
        return False
    
def validate_password(password):
    MIN_LENGTH = 8
    MAX_LENGTH = 12
    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in "!@#$%^&*" for char in password)

    return (len(password) >= MIN_LENGTH and len(password) <= MAX_LENGTH and
        has_lowercase and has_uppercase and has_digit and has_special)
