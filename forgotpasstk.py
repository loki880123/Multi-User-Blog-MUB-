import tkinter as tk
import mysql.connector
from tkinter import messagebox
import db_configtk
import subprocess
import hashlib

def open_password_reset_window(login_app):
    def check_user_details():
        # Retrieve values from the entry fields
        username = username_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        
        # Connect to the MySQL database using the configuration from db_configtk
        conn = mysql.connector.connect(**db_configtk.db_config)
        cursor = conn.cursor()
        
        # Query the database to check if the details match a single entry
        query = "SELECT * FROM users WHERE username=%s AND email=%s AND phone=%s"
        cursor.execute(query, (username, email, phone))
        result = cursor.fetchone()
        
        # Close the database connection
        cursor.close()
        conn.close()
        
        if result:
            # If details match, display fields to enter new password
            username_label.grid_forget()
            username_entry.grid_forget()
            email_label.grid_forget()
            email_entry.grid_forget()
            phone_label.grid_forget()
            phone_entry.grid_forget()
            next_button.grid_forget()
            cancel_button.grid_forget()

            new_password_label.grid(row=0, column=0, sticky="w", pady=10)
            new_password_entry.grid(row=0, column=1, pady=10)
            confirm_password_label.grid(row=1, column=0, sticky="w", pady=10)
            confirm_password_entry.grid(row=1, column=1, pady=10)
            show_password_checkbox_1.grid(row=2, column=0, columnspan=2, pady=10)
            cancel_button1.grid(row=3, column=1, sticky="w", pady=10, padx=70)
            submit_button.grid(row=3, column=1, pady=10, padx=100)
        else:
            # If details don't match, show error popup
            messagebox.showerror("Error", "Details not matching or not found in the database")

    def reset_password():

        # Connect to the MySQL database using the configuration from db_configtk
        conn = mysql.connector.connect(**db_configtk.db_config)
        cursor = conn.cursor()

        # Retrieve values from the entry fields
        username = username_entry.get()
        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()

        # Retrieve the old password from the database based on the provided username
        select_query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(select_query, (username,))
        result = cursor.fetchone()
        old_password = result[0]

        if hashlib.sha3_256(new_password.encode()).hexdigest() == old_password:
            messagebox.showerror("Error", "New password is similar to old password, please change")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        password_hash = hashlib.sha3_256(new_password.encode()).hexdigest()
        #print(password_hash)


        
        # Update the password in the database
        update_query = "UPDATE users SET password = %s WHERE username = %s"
        cursor.execute(update_query, (password_hash, username))
        conn.commit()
        
        # Close the database connection
        cursor.close()
        conn.close()
        
        messagebox.showinfo("Success", "Password updated successfully")
        password_reset_window.destroy()
        subprocess.run(["python", "logintk.py"])

    def cancel():
        print("Password reset cancelled")
        password_reset_window.destroy()
        subprocess.run(["python", "logintk.py"])

    login_app.destroy()
    password_reset_window = tk.Tk()  # Creating a new Tk instance for password reset window
    password_reset_window.attributes('-fullscreen', True)  # Make the password reset window full screen
    password_reset_window.title("Reset Password")

    

    # Adjusted label with bigger text and changed font
    label = tk.Label(password_reset_window, text="Daily Post", font=("Ink Free", 100, "bold"))
    label.pack(pady=50)

    frame = tk.Frame(master=password_reset_window, borderwidth=2)
    frame.pack(pady=20, padx=40)

    # GUI for password reset window
    username_label = tk.Label(frame, text="Username:", font=("Ink Free", 16, "bold"))
    username_label.grid(row=0, column=0, sticky="w", pady=10)
    username_entry = tk.Entry(frame, width=30, font=("Ink Free", 16, "bold"))
    username_entry.grid(row=0, column=1, pady=10)

    email_label = tk.Label(frame, text="Email:", font=("Ink Free", 16, "bold"))
    email_label.grid(row=1, column=0, sticky="w", pady=10)
    email_entry = tk.Entry(frame, width=30, font=("Ink Free", 16, "bold"))
    email_entry.grid(row=1, column=1, pady=10)

    phone_label = tk.Label(frame, text="Phone Number:", font=("Ink Free", 16, "bold"))
    phone_label.grid(row=2, column=0, sticky="w", pady=10)
    phone_entry = tk.Entry(frame, width=30, font=("Ink Free", 16, "bold"))
    phone_entry.grid(row=2, column=1, pady=10)

    cancel_button = tk.Button(frame, text="Cancel", font=("Ink Free", 16, "bold"), command=cancel, background='#ce4646')
    cancel_button.grid(row=3, column=1, sticky="w", pady=10, padx=70)
    next_button = tk.Button(frame, text="Next", font=("Ink Free", 16, "bold"), command=check_user_details, background='#7a7a7a')
    next_button.grid(row=3, column=1, pady=10, padx=100) 

    new_password_label = tk.Label(frame, text="New Password:", font=("Ink Free", 16, "bold"))
    new_password_entry = tk.Entry(frame, show="*", width=30, font=("Ink Free", 16, "bold"))
    confirm_password_label = tk.Label(frame, text="Confirm Password:", font=("Ink Free", 16, "bold"))
    confirm_password_entry = tk.Entry(frame, show="*", width=30, font=("Ink Free", 16, "bold"))
    submit_button = tk.Button(frame, text="Submit", font=("Ink Free", 16, "bold"), command=reset_password, background='#7a7a7a')
    cancel_button1 = tk.Button(frame, text="Cancel", font=("Ink Free", 16, "bold"), command=cancel, background='#ce4646')
    #show_password_1 = tk.BooleanVar()
    #show_password_1.set(False)
    show_password_1 = False
    def toggle_password_visibility():
        nonlocal show_password_1
        show_password_1 = not show_password_1
        if show_password_1:
            new_password_entry.config(show="")
            confirm_password_entry.config(show="")
        else:
            new_password_entry.config(show="*")
            confirm_password_entry.config(show="*")
    show_password_checkbox_1 = tk.Checkbutton(frame, text="Show Password", variable=show_password_1, font=("Ink Free", 16, "bold"), command=toggle_password_visibility)

    password_reset_window.mainloop()  # Start the Tkinter event loop for the password reset window

