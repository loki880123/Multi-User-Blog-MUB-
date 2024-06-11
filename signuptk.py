import tkinter as tk
from tkinter import messagebox
from functionstk import *
import hashlib
import subprocess

signup_app = tk.Tk()
signup_app.attributes('-fullscreen', True)  # Make the application fullscreen
signup_app.title("Signup - Daily Post")

# Adjusted label with bigger text and changed font
label = tk.Label(signup_app, text="Daily Post", font=("Ink Free", 100, "bold"))
label.pack(pady=50)

frame = tk.Frame(master=signup_app, borderwidth=2)
frame.pack(pady=20, padx=40)

signup_user_placeholder = tk.Label(master=frame, text='Enter Username', font=("Ink Free", 16, "bold"))
signup_user_placeholder.grid(row=0, column=0, sticky="w", pady=(0,5))

signup_user_entry = tk.Entry(master=frame, width=30, font=("Ink Free", 16, "bold"))
signup_user_entry.grid(row=1, column=0, pady=5)

signup_pass_placeholder = tk.Label(master=frame, text='Enter Password', font=("Ink Free", 16, "bold"))
signup_pass_placeholder.grid(row=2, column=0, sticky="w", pady=(10,5))

signup_user_pass = tk.Entry(master=frame, show="*", width=30, font=("Ink Free", 16, "bold"))
signup_user_pass.grid(row=3, column=0, pady=5)

signup_email_placeholder = tk.Label(master=frame, text='Enter Email', font=("Ink Free", 16, "bold"))
signup_email_placeholder.grid(row=4, column=0, sticky="w", pady=(10,5))

signup_email_entry = tk.Entry(master=frame, width=30, font=("Ink Free", 16, "bold"))
signup_email_entry.grid(row=5, column=0, pady=5)

signup_phone_placeholder = tk.Label(master=frame, text='Enter Phone Number', font=("Ink Free", 16, "bold"))
signup_phone_placeholder.grid(row=6, column=0, sticky="w", pady=(10,5))

signup_phone_entry = tk.Entry(master=frame, width=30, font=("Ink Free", 16, "bold"))
signup_phone_entry.grid(row=7, column=0, pady=5)

def create_account():
    username = signup_user_entry.get()
    password = signup_user_pass.get()
    email = signup_email_entry.get()
    phone = signup_phone_entry.get()

    if not username or not password or not email or not phone:
        messagebox.showerror("Error", "Please fill all the fields")
    else:      
        if not validate_password(password):
            messagebox.showerror("Error", "Please fill a valid password with a lower case letter, upper case letter, a number, a special character (e.g., !@#$%^&*) and with length of 8 to 12")
        elif not validate_email(email):
            messagebox.showerror("Error", "Please fill a valid mail")
        elif not validate_phone(phone):
            messagebox.showerror("Error", "Please fill a valid phone number")
        else:
            # Encrypt password using SHA-3
            password_hash = hashlib.sha3_256(password.encode()).hexdigest()
            #print(password_hash)
            result = signup(signup_user_entry, password_hash, signup_email_entry, signup_phone_entry)
            if result:  # Assuming signup function returns True on success
                #messagebox.showinfo("Success", "Account created successfully!")
                signup_app.destroy()  # Close the signup window
            else:
                messagebox.showerror("Error", "Failed to create account. Please try again.")

signup_button = tk.Button(master=frame, text="Create Account", font=("Ink Free", 16, "bold"), command=create_account, background='#7a7a7a')
signup_button.grid(row=8, sticky="w", pady=(25,5))

def close_app():
    signup_app.destroy()

button_close = tk.Button(master=frame, text='Cancel', font=("Ink Free", 16, "bold"), command=close_app, background='#ce4646')
button_close.grid(row=8, column=0, sticky="e", pady=(25,5))


signup_app.mainloop()