import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import db_configtk
import customtkinter as ctk
from img_modstk import *

def display_post(username, heading, hpage):
    # Create a new window for displaying the post details
    print("*******Displaying*******")
    print(username+" -- "+heading)

    post_frame = tk.Toplevel(hpage)
    
    window_width = post_frame.winfo_screenwidth() // 2
    window_height = post_frame.winfo_screenheight() // 2
    post_frame.geometry(f"{window_width}x{window_height}+{window_width // 2}+{window_height // 2}")
    post_frame.title("Post Details")

    scrollbar = ctk.CTkScrollableFrame(master=post_frame, orientation='vertical')
    scrollbar.pack(fill='both', expand=True)

    post_window=tk.Frame(scrollbar)
    post_window.pack(fill="both", expand=True)
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_configtk.db_config)
        cursor = conn.cursor()

        # Retrieve post data based on username and heading
        sql_query = "SELECT text_data, image_path FROM posts WHERE username = %s AND heading = %s"
        cursor.execute(sql_query, (username, heading))
        post_data = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        if post_data:
            text_data, image_path = post_data

            # Display image if available
            if image_path:
                rounded_image_tk = round_corners(image_path, 25, (576, 324))
                rounded_image_pil = ImageTk.getimage(rounded_image_tk)
                my_image = ctk.CTkImage(light_image=rounded_image_pil, dark_image=rounded_image_pil, size=(432, 243))
                # Load and display image
                image_label = ctk.CTkLabel(post_window, text="", image=my_image)
                image_label.pack(pady=10)

            # Display heading
            heading_label = tk.Label(post_window, text=heading, font=("Ink Free", 16,"bold"), wraplength=window_width-50)
            heading_label.pack()

            # Display text data
            text_label = tk.Label(post_window, text=text_data, font=("Ink Free", 12), wraplength=window_width-50)
            text_label.pack()
        else:
            error_label = tk.Label(post_window, text="Post not found")
            error_label.pack()

    except mysql.connector.Error as err:
        error_label = tk.Label(post_window, text=f"Error: {err}")
        error_label.pack()

def search_posts(query):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_configtk.db_config)
        cursor = conn.cursor()

        # Search for posts where the username or heading matches the query
        sql_query = "SELECT username, heading FROM posts WHERE username LIKE %s OR heading LIKE %s"
        cursor.execute(sql_query, (f'%{query}%', f'%{query}%'))

        # Fetch the results
        results = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return results
    except mysql.connector.Error as err:
        print("Error:", err)
        return []




