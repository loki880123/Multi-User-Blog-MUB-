import customtkinter as ctk
from tkinter import *
from PIL import ImageTk
from tkinter import filedialog
import os
import logouttk
import my_profiletk
import tkinter as tk
from functionstk import *
from img_modstk import *
import tkinter.messagebox as messagebox
from commentstk import *
from searchtk import *
import math

username = os.environ.get("USERNAME")  # Retrieve environment variable
print("Welcome "+ username)
hpage = None

# Function to open the profile window and close the homepage window
def open_profile(username):
    hpage.destroy()
    my_profiletk.profile_page(username)
    #hpage.destroy()  # Close the homepage window

# Function to display fetched data using customtkinter
def display_data(data):
    global hpage  # Declare hpage as a global variable
    if not data:
        return

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    hpage = tk.Tk()
    hpage.attributes('-fullscreen', True) 
    hpage.title("Daily Post Homepage")

    label = Label(hpage, text="Daily Post", font=("Ink Free", 50, "bold"))
    label.pack(pady=40)
   
    my_post_button = Button(hpage, text="\U0001F464"+"My Account", font=("Ink Free", 15, "bold"), relief="flat", command=lambda: open_profile(username), background='#7a7a7a')
    my_post_button.place(relx=0.13, rely=0.05, anchor='ne')

    # Search field and icon
    search_frame = Frame(hpage)
    search_frame.place(relx=0.34, rely=0.065, anchor='ne')

    search_entry = Entry(search_frame, font=("Ink Free", 15, "bold"), relief="groove")
    search_entry.pack(side=LEFT)

    global search_results_menu
    search_results_menu = Menu(search_frame, tearoff=0)  # Create a dropdown menu for search results

    def handle_enter(event):
        entered = search_entry.get()
        perform_search(entered)

    search_entry.bind("<Return>", handle_enter)

    search_icon_label = Label(search_frame, text="\U0001F50E", cursor='hand2', font=("Ink Free", 16))
    search_icon_label.bind("<Button-1>", lambda event: perform_search(search_entry.get())) 
    search_icon_label.pack(side=LEFT)

    def perform_search(query):
        global search_results_menu
        search_results_menu.delete(0, END)
        results = search_posts(query)

        def print_post(post):
            print("*******SELECTED*******")
            print(post)
            display_post(post[0],post[1],hpage)
            return post
        if results:
            for post in results:
                search_results_menu.add_command(label=post, command=lambda p=post: print_post(p), font=("Ink Free", 12, "bold"))  # Add each post as a menu item
            search_results_menu.post(search_frame.winfo_rootx(), search_frame.winfo_rooty() + search_frame.winfo_height())  # Display the dropdown menu
        else:
            print("No results found")
            search_results_menu.delete(0, "end")
            search_results_menu.add_command(label="No results found", font=("Ink Free", 12, "bold"))
            search_results_menu.post(search_frame.winfo_rootx(), search_frame.winfo_rooty() + search_frame.winfo_height())
        return print_post
    
    def show_full_text(full_text):
        full_text_window = tk.Toplevel()
        #full_text_window.attributes('-fullscreen', True)
        # Set the width and height of the window to be half the screen
        window_width = full_text_window.winfo_screenwidth() // 2
        window_height = full_text_window.winfo_screenheight() // 2
        full_text_window.geometry(f"{window_width}x{window_height}+{window_width // 2}+{window_height // 2}")
        full_text_window.title("Full Text")
            
        frame = Frame(master=full_text_window, borderwidth=5, height=50, relief="flat")
        frame.pack(pady=20, padx=40, fill="both" , expand=True)

        scrollbar = ctk.CTkScrollableFrame(master=frame, orientation='vertical')
        scrollbar.pack(fill='both', expand=True)

        # Display the full text
        full_text_label = ctk.CTkLabel(master=scrollbar, text=full_text, text_color='black', font=("Calibri Body", 16, "normal"), justify='left', wraplength=600)
        full_text_label.pack(pady=10, padx=10)

        full_text_window.mainloop()

    add_post_button = Button(hpage, text="➕Add Post", font=("Ink Free", 15, "bold"), command=add_post_window, relief="flat", background='#7a7a7a')
    add_post_button.place(relx=0.894, rely=0.05, anchor='ne')
    
    logout_button = Button(hpage, text="Logout", font=("Ink Free", 15, "bold"), command=lambda: logouttk.logout_page(hpage), relief="flat", background='#ce4646')
    logout_button.place(relx=0.97, rely=0.05, anchor='ne')

    frame = Frame(master=hpage, borderwidth=2, height=50, relief="flat")
    frame.pack(pady=20, padx=40, fill="both" , expand=True)

    scrollbar = ctk.CTkScrollableFrame(master=frame, orientation='vertical')
    scrollbar.pack(fill='both', expand=True)

    num_columns = 2
    num_rows = fetch_counter()
    num_rows_per_column = math.ceil(num_rows / num_columns)

    for row_index, row in enumerate(data):

        # Calculate row and column indices for the 2xX matrix
        grid_column = row_index // num_rows_per_column
        grid_row = row_index % num_rows_per_column
        row_frame = ctk.CTkFrame(master=scrollbar)
        if grid_column==0:
            row_frame.grid(row=grid_row, column=grid_column, padx=100, pady=10)
        else:
            row_frame.grid(row=grid_row, column=grid_column, padx=10, pady=10)
        image_path = row[1]
        text_data = row[2]
        user_name = row[3]
        heading = row[4]
        timestamp = row[5]
        comments = row[6]
        date = str(timestamp).split(" ")[0]

        # Create a frame to contain both labels
        label_frame = ctk.CTkFrame(master=row_frame)
        label_frame.pack(side="top")

        # for username
        user_label = ctk.CTkLabel(label_frame, text=f"{user_name} ", font=("Ink Free", 25, "bold"))
        date_label = ctk.CTkLabel(label_frame, text=f"({date})", font=("Ink Free", 14))

        user_label.pack(side="left", padx=(5,5))
        date_label.pack(side="left", padx=(0,5))

        rounded_image_tk = round_corners(image_path, 25, (480,270))
        rounded_image_pil = ImageTk.getimage(rounded_image_tk)

        my_image = ctk.CTkImage(light_image=rounded_image_pil,
                                dark_image=rounded_image_pil,
                                size=(576,324))
        
        # Create a label to display the image
        image_label = ctk.CTkLabel(master=row_frame,text="", image=my_image)
        #image_label.pack(side='top', anchor='w', padx=100)
        image_label.pack()
        #image_label.grid(row=0, column=0, padx=100)       
        if len(heading)>=35:
            trunc_heading=heading[:35]

            heading_label=ctk.CTkLabel(master=row_frame, text=trunc_heading+"...read more", cursor='hand2', text_color='black', font=("Cascadia Code", 16, "bold"), justify='left')
            heading_label.bind("<Button-1>", lambda event, data=text_data: show_full_text(data))
            heading_label.pack()
        else:
            heading_label=ctk.CTkLabel(master=row_frame, text=heading+"...read more", cursor='hand2', text_color='black', font=("Cascadia Code", 16, "bold"), justify='left')
            heading_label.bind("<Button-1>", lambda event, data=text_data: show_full_text(data))
            heading_label.pack()
        if comments == "1":
            comment_label=ctk.CTkLabel(master=row_frame, text="View all comments", cursor='hand2', text_color='black', font=("Cascadia Code", 16, "bold"))
            comment_label.bind("<Button-1>", lambda event, id=row[0]: display_comments(id,username))
            comment_label.pack()

    hpage.mainloop()

def format_text(text_data):
    # Split the text into paragraphs using newline characters
    paragraphs = text_data.split('\n\n')
    formatted_text = ""

    # Add HTML markup to format the text
    for paragraph in paragraphs:
        # Check for headings (lines starting with '#')
        if paragraph.startswith('#'):
            heading = paragraph.strip('#').strip()
            formatted_text += f"<h2>{heading}</h2>"
        else:
            # Add paragraphs with bold text
            formatted_text += f"<p><b>{paragraph}</b></p>"

    return formatted_text

# Function to add a post using a separate window
def add_post_window():

    global hpage  # Declare hpage as a global variable
    selected_image_path = ""
    formatted_path = ""

    # Function to handle the "Select Photo" button click
    def select_photo():
        nonlocal selected_image_path
        nonlocal formatted_path
        if hpage:
            hpage.destroy()
        selected_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        formatted_path = selected_image_path.replace('/', '\\')
        print(formatted_path)
        #display_image(formatted_path)
        # Display label indicating image upload and its path
        upload_label.config(text="Image Uploaded", fg="green")
        path_label.config(text=f"Image Path: {formatted_path}", fg="blue")
        
        return formatted_path

    # Function to handle the "Add Post" button click
    def add_post_in_window():
        #new_text_data = save_content()
        new_text_data = text_entry.get("1.0", "end-1c")
        new_heading_entry = heading_entry.get()
        selected_value = commentState.get()

        if selected_value == "1":
            print("On - comments")
        elif selected_value == "2":
            print("Off - comments")
        else:
            print("Unexpected value")

        if selected_image_path and new_text_data and new_heading_entry and selected_value:
            insert_post(selected_image_path, new_text_data, new_heading_entry, selected_value)
            add_post_window.destroy()
            fetched_data = fetch_data()
            display_data(fetched_data)
    
    add_post_window = tk.Tk()
     # Set the width and height of the window to be half the screen
    #window_width = add_post_window.winfo_screenwidth() // 2
    #window_height = add_post_window.winfo_screenheight() // 2
    #add_post_window.geometry(f"{window_width}x{window_height}+{window_width // 2}+{window_height // 2}")
    add_post_window.attributes('-fullscreen', True) 
    add_post_window.title("Add New Post")

    label = Label(add_post_window, text="Daily Post", font=("Ink Free", 50, "bold"))
    label.grid(row=0, column=0, padx=10, pady=20, sticky='w')

    frame = tk.Frame(add_post_window, borderwidth=2)
    frame.grid(row=1, column=0, pady=5, padx=300, sticky='w')

    # Create labels to display image upload status
    upload_label = tk.Label(frame, font=("Ink Free", 16, "bold"))
    upload_label.grid(row=1, column=0, pady=5, padx=5)

    # Create and pack widgets for the "Add New Post" window
    tk.Button(frame, text="Select Photo", command=select_photo, font=("Ink Free", 16, "bold"), relief="flat", background='#7a7a7a').grid(row=2, column=0, pady=5)

    # Create labels to display image upload path
    path_label = tk.Label(frame, font=("Ink Free", 12), relief="flat")
    path_label.grid(row=3, column=0, pady=5, padx=5)

    tk.Label(frame, width=30, text="Heading:", font=("Ink Free", 16, "bold"), relief="flat").grid(row=6, column=0, pady=5)
    heading_entry = tk.Entry(frame, font=("Ink Free", 16, "bold"), relief="flat", width=50)
    heading_entry.grid(row=7, column=0, pady=5)

    tk.Label(frame, text="Text Data:", font=("Ink Free", 16, "bold"), relief="flat").grid(row=8, column=0, pady=5)
    text_entry = tk.Text(frame, font=("Ink Free", 16, "bold"), relief="flat", wrap="word", width=75, height=10)
    text_entry.grid(row=9, column=0, pady=5)

    tk.Label(frame, text="Comments:", font=("Ink Free", 16, "bold"), relief="flat").grid(row=10, column=0, pady=5)
    commentState = StringVar(frame,"1") 
    values = {"On" : "1", "Off" : "2"} 
    row_counter=0
    for (text, value) in values.items():
        Radiobutton(frame, text = text, variable = commentState, value = value, font=("Ink Free", 16, "bold")).grid(row=11+row_counter, column=0, pady=2)
        row_counter += 1 

    tk.Button(frame, text="Add Post", font=("Ink Free", 16, "bold"), relief="flat", background='#7a7a7a', command=add_post_in_window).grid(row=12, column=1, pady=5)

    def close_app():
        add_post_window.destroy()

    button_close = tk.Button(frame, text='Cancel', font=("Ink Free", 16, "bold"), relief="flat", command=close_app, background='#ce4646')
    #button_close.place(relx=1, rely=0, anchor=tk.NE, x=-10, y=10)
    button_close.grid(row=13, column=1, pady=5)

    add_post_window.mainloop()

# Fetch data from the database
fetched_data = fetch_data()

# Display the fetched data using customtkinter
display_data(fetched_data)

