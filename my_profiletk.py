import tkinter as tk
import mysql.connector
import tkinter.messagebox as tkmb
import db_configtk
import subprocess
from tkinter import *
from PIL import ImageTk
from functionstk import *
from img_modstk import *

def get_user_information(username):
    # Connect to the MySQL database using the provided configuration
    conn = mysql.connector.connect(**db_configtk.db_config)
    cursor = conn.cursor()

    # Execute a query to fetch user information based on the username
    cursor.execute("SELECT email, phone FROM users WHERE username=%s", (username,))
    user_info = cursor.fetchone()  # Assuming only one row for each username

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return user_info

def update_user_information(username, email, phone):
    # Connect to the MySQL database using the provided configuration
    conn = mysql.connector.connect(**db_configtk.db_config)
    cursor = conn.cursor()

    # Execute a query to update user information based on the username
    cursor.execute("UPDATE users SET email=%s, phone=%s WHERE username=%s", (email, phone, username))

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

def profile_page(username):
    def edit_email():
        email_entry.config(state="normal")
        email_edit_button.config(state="disabled")

    def edit_phone():
        phone_entry.config(state="normal")
        phone_edit_button.config(state="disabled")

    def save_changes():
        new_email = email_entry.get()
        new_phone = phone_entry.get()
        if not validate_email(new_email):
            tkmb.showerror("Error", "Please fill a valid mail")
        elif not validate_phone(new_phone):
            tkmb.showerror("Error", "Please fill a valid phone number")
        else:
            update_user_information(username, new_email, new_phone)

        email_entry.config(state="disabled")
        phone_entry.config(state="disabled")
        email_edit_button.config(state="normal")
        phone_edit_button.config(state="normal")

    def delete_post(post_id):
        conn = mysql.connector.connect(**db_configtk.db_config)
        cursor = conn.cursor()
        # Delete comments associated with the post
        cursor.execute("DELETE FROM comments WHERE post_id = %s", (post_id,))
        cursor.execute("DELETE FROM posts WHERE id=%s", (post_id,))
        conn.commit()
        cursor.close()
        conn.close()
        posts_frame.destroy()
        load_posts()

    def load_posts():
        conn = mysql.connector.connect(**db_configtk.db_config)
        cursor = conn.cursor()
        if username != "admin":
            cursor.execute("SELECT id, heading, image_path FROM posts WHERE username=%s", (username,))
        else: 
            cursor.execute("SELECT id, heading, image_path, username as u FROM posts")
        posts = cursor.fetchall()
        cursor.close()
        conn.close()

        global posts_frame

        # Create a frame to contain the posts
        posts_frame = tk.Frame(profile_window)
        posts_frame.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        scrollbar = ctk.CTkScrollableFrame(master=posts_frame, orientation='vertical')
        scrollbar.pack(fill='both', expand=True)

        # Populate the posts frame with posts
        if username != "admin":
            for post_id, heading, image_path in posts:
                post_frame = tk.Frame(scrollbar)
                post_frame.pack(pady=10, fill="x")

                # Display picture
                rounded_image_tk = round_corners(image_path, 25, (576, 324))
                rounded_image_pil = ImageTk.getimage(rounded_image_tk)
                my_image = ctk.CTkImage(light_image=rounded_image_pil, dark_image=rounded_image_pil, size=(144, 81))
                image_label = ctk.CTkLabel(post_frame, text="", image=my_image)
                image_label.pack(side="left", padx=10)

                # Display heading
                heading_label = tk.Label(post_frame, text=heading, font=("Ink Free", 12, "bold"))
                heading_label.pack(side="left", padx=10)

                # Edit button
                edit_button = tk.Button(post_frame, text="Edit✎", font=("Ink Free", 12, "bold"), relief="flat", command=lambda post_id=post_id, heading=heading: edit_post_window(post_id, heading), background='#7a7a7a')
                edit_button.pack(side="left", padx=10)

                # Delete button
                delete_button = tk.Button(post_frame, text="Delete"+"\U0001F5D1", font=("Ink Free", 12, "bold"), relief="flat", command=lambda post_id=post_id: delete_post(post_id), background='#ce4646')
                delete_button.pack(side="left", padx=10)
        else:

            for post_id, heading, image_path, u in posts:
                post_frame = tk.Frame(scrollbar)
                post_frame.pack(pady=10, fill="x")

                # Display picture
                rounded_image_tk = round_corners(image_path, 25, (576, 324))
                rounded_image_pil = ImageTk.getimage(rounded_image_tk)
                my_image = ctk.CTkImage(light_image=rounded_image_pil, dark_image=rounded_image_pil, size=(144, 81))
                image_label = ctk.CTkLabel(post_frame, text="", image=my_image)
                image_label.pack(side="left", padx=10)

                # Display heading
                heading_label = tk.Label(post_frame, text=heading, font=("Ink Free", 12, "bold"))
                heading_label.pack(side="left", padx=10)

                user_label = tk.Label(post_frame, text=u, font=("Ink Free", 12, "bold"))
                user_label.pack(side="left", padx=10)

                # Edit button
                edit_button = tk.Button(post_frame, text="Edit✏️ ", font=("Ink Free", 12, "bold"), relief="flat", command=lambda post_id=post_id, heading=heading: edit_post_window(post_id, heading), background='#7a7a7a')
                edit_button.pack(side="left", padx=10)

                # Delete button
                delete_button = tk.Button(post_frame, text="Delete"+"\U0001F5D1", font=("Ink Free", 12, "bold"), relief="flat", command=lambda post_id=post_id: delete_post(post_id), background='#ce4646')
                delete_button.pack(side="left", padx=10)
            




    def edit_post_window(post_id, current_heading):
        def save_changes():
            new_heading = heading_entry.get()
            new_text_data = text_data_entry.get("1.0", tk.END)
            comments_change = commentState.get()

            # Update the post with new heading and text data
            update_post(post_id, new_heading, new_text_data, comments_change)

            # Close the edit post window
            edit_post_window.destroy()
            posts_frame.destroy()

            # Reload posts to reflect changes
            load_posts()

        # Create a new window for editing the post
        edit_post_window = tk.Toplevel(profile_window)
        edit_post_window.title("Edit Post")

        # Heading entry
        heading_label = tk.Label(edit_post_window, text="Heading:", font=("Ink Free", 14, "bold"))
        heading_label.pack(pady=10)
        heading_entry = tk.Entry(edit_post_window, width=50, relief="flat", font=("Ink Free", 12, "bold"))
        heading_entry.insert(0, current_heading)
        heading_entry.pack(padx=10)

        # Text data entry
        text_data_label = tk.Label(edit_post_window, text="Text Data:", font=("Ink Free", 14, "bold"))
        text_data_label.pack()
        text_data_entry = tk.Text(edit_post_window, width=50, height=10, relief="flat", font=("Ink Free", 12, "bold"))
        text_data_entry.pack(padx=10)

        #comments entry
        tk.Label(edit_post_window, text="Comments:", font=("Ink Free", 14, "bold")).pack()
        commentState = StringVar(edit_post_window,"1") 
        values = {"On" : "1", "Off" : "2"} 
        row_counter=0
        for (text, value) in values.items():
            Radiobutton(edit_post_window, text = text, variable = commentState, value = value, font=("Ink Free", 14, "bold")).pack()
            row_counter += 1 

        # Save button
        save_button = tk.Button(edit_post_window, text="Save Changes"+"\U0001F4BE", font=("Ink Free", 12, "bold"), relief="flat", command=save_changes, background='#64b0d1')
        save_button.pack(pady=10)

        # Fetch existing text data of the post
        conn = mysql.connector.connect(**db_configtk.db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT text_data,comments FROM posts WHERE id=%s", (post_id,))
        text_data = cursor.fetchone()[0]
        # Fetch comments
        cursor.execute("SELECT comments FROM posts WHERE id=%s", (post_id,))
        current_comments = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        # Insert existing text data into the text entry
        text_data_entry.insert(tk.END, text_data)
        commentState.set(current_comments)

    def update_post(post_id, new_heading, new_text_data, comments_change):
        conn = mysql.connector.connect(**db_configtk.db_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE posts SET heading=%s, text_data=%s, comments=%s WHERE id=%s", (new_heading, new_text_data, comments_change, post_id))
        conn.commit()
        cursor.close()
        conn.close()


    def go_back():
        profile_window.destroy()
        subprocess.run(["python", "homepagetk.py"])

    # Create a new window for the profile page
    profile_window = tk.Tk()
    profile_window.attributes('-fullscreen', True)
    profile_window.title("My Profile")

    label = tk.Label(profile_window, text="Daily Post", font=("Ink Free", 50, "bold"))
    label.pack(pady=50)

    # Fetch user information from the database
    email, phone = get_user_information(username)

    # Display user information
    username_label = tk.Label(profile_window, text=f"Welcome, {username}!", font=("Ink Free", 20, "bold"))
    username_label.pack(pady=20)

    email_frame = tk.Frame(profile_window)
    email_frame.pack(pady=10)

    email_entry = tk.Entry(email_frame, font=("Ink Free", 14, "bold"), relief="groove", width=30)
    email_entry.insert(0, email)
    email_entry.config(state="disabled")
    email_entry.pack(side="left", padx=10)

    email_edit_button = tk.Button(email_frame, text="Edit✎", command=edit_email, font=("Ink Free", 12, "bold"), relief="flat", background='#7a7a7a')
    email_edit_button.pack(side="left")

    phone_frame = tk.Frame(profile_window)
    phone_frame.pack(pady=10)

    phone_entry = tk.Entry(phone_frame, font=("Ink Free", 14, "bold"), relief="groove", width=30)
    phone_entry.insert(0, phone)
    phone_entry.config(state="disabled")
    phone_entry.pack(side="left", padx=10)

    phone_edit_button = tk.Button(phone_frame, text="Edit✎", command=edit_phone, font=("Ink Free", 12, "bold"), relief="flat", background='#7a7a7a')
    phone_edit_button.pack(side="left")

    save_button = tk.Button(profile_window, text="Save Changes"+"\U0001F4BE", font=("Ink Free", 12, "bold"), relief="flat", command=save_changes, background='#449ac1')
    save_button.pack(pady=10)

    back_button = tk.Button(profile_window, text="Home⬅️", font=("Ink Free", 12, "bold"), relief="flat", command=go_back, background='#7a7a7a')
    back_button.pack(pady=10)

    # Load and display user's posts
    load_posts()

    # Run the tkinter event loop
    profile_window.mainloop()
