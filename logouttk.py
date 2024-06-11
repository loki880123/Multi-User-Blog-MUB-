# logout.py

import customtkinter as ctk
from tkinter import *
import tkinter as tk
import subprocess

# Function to handle the logout action
def logout(hpage, logout_window):
    hpage.destroy()  # Destroy the main page
    subprocess.run(["python", "logintk.py"])

# Create a new window for the logout page
def logout_page(hpage):

    def on_enter(event):
        hpage.destroy() 
        subprocess.run(["python", "logintk.py"])
      
    logout_window = tk.Toplevel()
    #logout_window.attributes('-fullscreen', False)  # Set the window to fullscreen
    # Set the window size
    window_width = 500
    window_height = 150

    # Get the screen width and height
    screen_width = logout_window.winfo_screenwidth()
    screen_height = logout_window.winfo_screenheight()

    # Calculate the position to center the window
    x = (screen_width - window_width) / 2
    y = (screen_height - window_height) / 2

    # Set the window size and position
    logout_window.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))
    logout_window.title("Logout")

    # Add a label to display a logout confirmation message
    logout_label = Label(logout_window, text="Are you sure you want to logout?", font=("Ink Free", 18, "bold"))
    logout_label.pack(pady=5)

    # Add a button to confirm the logout action
    confirm_button = Button(logout_window, text="Logout", font=("Ink Free", 15, "bold"), relief="flat", command=lambda: logout(hpage, logout_window), background='#ce4646')
    confirm_button.pack(pady=5)  # Adjusted padx

    logout_window.bind('<Return>', on_enter)
    hpage.bind('<Return>', on_enter)

    # Run the logout window's main loop
    logout_window.mainloop()

    return logout_window  # Return the logout window object
