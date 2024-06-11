import tkinter as tk
import subprocess
import os
import hashlib
from functionstk import login
from forgotpasstk import open_password_reset_window  
from tkinter import *

login_app = tk.Tk()
login_app.attributes('-fullscreen', True)  # Make the application fullscreen
login_app.title("Daily Post")

# Adjusted label with bigger text and changed font
label = tk.Label(login_app, text="Daily Post", font=("Ink Free", 100, "bold"))
label.pack(pady=50)

# Creating a frame for the login fields
login_frame = tk.Frame(login_app, borderwidth=3, relief="flat", width=1200, height=800, background='white')
login_frame.pack(pady=20, padx=40)

label_username = tk.Label(master=login_frame, text="\U0001F464"+"Username", font=("Ink Free", 16, "bold"), background='white')
label_username.grid(row=0, column=0, sticky="w", pady=(5,10))

user_entry = tk.Entry(master=login_frame, width=30, relief="flat", font=("Ink Free", 16, "bold"), background='#dddddd')
user_entry.grid(row=1, column=0, padx=20, pady=10)

label_password = tk.Label(master=login_frame, text="\U0001F512"+"Password", font=("Ink Free", 16, "bold"), background='white')
label_password.grid(row=2, column=0, sticky="w", pady=(10,5))

user_pass = tk.Entry(master=login_frame, show="*", width=30, relief="flat", font=("Ink Free", 16, "bold"), background='#dddddd')
user_pass.grid(row=3, column=0, padx=20, pady=10)

# Checkbox for showing password
show_password = tk.BooleanVar()
show_password.set(False)

def toggle_password_visibility():
    global show_password
    show_password = not show_password
    if show_password:
        user_pass.config(show="")
    else:
        user_pass.config(show="*")

show_password_checkbox = tk.Checkbutton(master=login_frame, text="Show Password", variable=show_password, font=("Ink Free", 16, "bold"), command=toggle_password_visibility, background='white')
show_password_checkbox.grid(row=4, column=0, sticky="w", padx=20, pady=(10,5))

forgotpass = tk.Label(master=login_frame, text="Forgot password?", cursor='hand2', font=("Ink Free", 16, "bold"), justify='left', background='white')
forgotpass.bind("<Button-1>", lambda event: open_password_reset_window(login_app)) 
forgotpass.grid(row=5, column=0, sticky="w", padx=20, pady=(10,5))

def on_enter(event):
    login_success()

def login_success():
    password_hash = hashlib.sha3_256(user_pass.get().encode()).hexdigest()
    op = login(user_entry, password_hash)
    username_str = user_entry.get()
    os.environ["USERNAME"] = username_str
    if op:
        login_app.destroy()
        subprocess.run(["python", "homepagetk.py"])

button_login = tk.Button(master=login_frame, text='Login', relief="flat", font=("Ink Free", 14, "bold"), command=login_success, background='#888888')
button_login.grid(row=6, column=0, padx=20, pady=10)

# Creating a frame for signup option
signup_frame = tk.Frame(login_app, borderwidth=2, relief="flat", background='white')
signup_frame.pack(pady=20, padx=40)

signup_label = tk.Label(master=signup_frame, text="Don't have an account?", font=("Ink Free", 15, "bold"), background='white')
signup_label.grid(row=0, column=0, sticky="w", padx=20, pady=10)

def open_signup():
    subprocess.run(["python", "signuptk.py"])  # Execute signup.py using subprocess

button_signup = tk.Button(master=signup_frame, text='Join Now', font=("Ink Free", 14, "bold"), relief="flat", command=open_signup, background='#888888')
button_signup.grid(row=1, column=0, pady=10)

# Close button
button_close = tk.Button(master=login_app, text='Close❌', font=("Ink Free", 14, "bold"), relief="flat", command=login_app.destroy, background='#ce4646')
button_close.place(relx=1, rely=0, anchor=tk.NE, x=-10, y=10)

login_app.bind('<Return>', on_enter)

login_app.mainloop()
