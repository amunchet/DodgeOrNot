"""
Chat GPT prompt: 
    - python gui create window that is 375px by 220px.  The window has a background color of light blue.  There are two columns.  The first has the text "Our Team" (font Arial, 25px size) followed by a thin gray line, followed by a 150px by 50px green box that contains the large text (30px) "50.7%".  The second column is the same, except the text says "Enemy Team" and the green box is instead orange.  Below the two columns is a button that says "Settings" and opens another window which allows the user to input a file path that is saved to a file.
    - create a new python gui program that has a label with a background of green and text that says "Hello!".  In a new thread, change the background of that label to red and the text to say "New", then change it back every 5 seconds
    - create a python gui that starts with the window in the bottom right corner of the screen
    - Python GUI with top text that says "Please enter the location of LoL" folowed by an input, then followed by a button that saves the input to a file
"""
import os
import sys
import psutil 
import time
import threading
import logging

import tkinter as tk

import client
import stats

# Logging
logger = logging.getLogger("dodgeOrNot_logger")
logger.setLevel(logging.DEBUG)

if os.path.exists("dodgeOrNot.log"):
    os.remove("dodgeOrNot.log")

file_handler = logging.FileHandler("dodgeOrNot.log")
stream_handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def resource_path(relative_path):    
    try:       
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def show_settings_window(): # pragma: no cover
    """
    Shows the settings window on startup
    """
    logger.debug("Showing Settings Window...")
    # Create the main window
    root = tk.Tk()

    root.wm_title("DodgeOrNot")
    root.wm_iconbitmap(resource_path("logo.ico"))
    root.wm_attributes("-topmost", 1)

    # Create the frame to hold the widgets
    frame = tk.Frame(root)
    frame.pack()

    label = tk.Label(frame, text="No running LoL client detected.  Close this program and start up the LoL client.")
    label.pack(pady=10, padx=10)

    # Create the label widget
    label = tk.Label(frame, text="Or you can enter the location of LoL directly:")
    label.pack(pady=10, padx=10)

    # Create the entry widget
    entry = tk.Entry(frame)
    entry.pack()

    # Define the function to handle the button click event
    def save_input():
        # Get the input from the entry widget
        input_text = entry.get()
        
        logger.debug(f"[Settings] Input entry:{input_text}")
        # Write the input to a file
        with open("lockfile-location", "w") as f:
            f.write(input_text.strip())
        
        root.destroy()

    # Create the button widget
    button = tk.Button(frame, text="Save Lockfile Location", command=save_input)
    button.pack(padx=10, pady=10)

    # Run the main loop
    root.mainloop()



def show_main_window(lockfile): # pragma: no cover
    """
    Main Window
    """
    logger.debug("Main Window...")
    # Create the main window
    root = tk.Tk()
    # root.geometry("425x200")
    # root.configure(bg="lightblue")

    root.wm_title("DodgeOrNot")
    root.wm_iconbitmap(resource_path("logo.ico"))

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the window size and position
    window_width = 425
    window_height = 200
    window_x = screen_width - window_width
    window_y = screen_height - window_height
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, window_x, window_y))
    # Set the window to stay on top of other windows
    root.wm_attributes("-topmost", 1)
    root.configure(bg="lightblue")

    # Create the frame for the first column
    frame1 = tk.Frame(root, bg="lightblue")
    frame1.pack(side="left")

    # Create the label for the first column
    label1 = tk.Label(frame1, text="Our Team", font=("Arial", 25), bg="lightblue")
    label1.pack()

    # Create the separator for the first column
    separator1 = tk.Frame(frame1, height=2, bd=1, relief="sunken")
    separator1.pack(fill="x", padx=5, pady=5)

    # Create the green box for the first column
    green_box1 = tk.Label(frame1, text="-", bg="gray", font=("Arial", 30), width=9, height=2)
    green_box1.pack()

    # Create the frame for the second column
    frame2 = tk.Frame(root, bg="lightblue")
    frame2.pack(side="right")

    # Create the label for the second column
    label2 = tk.Label(frame2, text="Enemy Team", font=("Arial", 25), bg="lightblue")
    label2.pack()

    # Create the separator for the second column
    separator2 = tk.Frame(frame2, height=2, bd=1, relief="sunken")
    separator2.pack(fill="x", padx=5, pady=5)

    # Create the orange box for the second column
    orange_box2 = tk.Label(frame2, text="-", bg="gray", font=("Arial", 30), width=9, height=2)
    orange_box2.pack()

    current_lobby = {
        "us" : [],
        "them": [],
    }

    def exit_window():
        thread.join()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", exit_window)

    def color_from_chances(chances:float):
        if float(chances) < 49:
            return "red"
        if float(chances) > 51:
            return "green"
        
        return "orange"

    def update():
        loop_check = True
        while loop_check:
            new_lobby = client.read_lobby(lockfile)
            logger.debug(f"[Main] New lobby:{new_lobby}")
            if new_lobby != current_lobby:
                our_chances = stats.check_synergies(new_lobby["us"])
                their_chances = stats.check_synergies(new_lobby["them"])

                logger.debug(f"Our chances:{our_chances}")
                logger.debug(f"Their chances:{their_chances}")


                green_box1.configure(bg=color_from_chances(our_chances), text=f"{our_chances}%")
                orange_box2.configure(bg=color_from_chances(their_chances), text=f"{their_chances}%")
                root.update()

                if len(new_lobby["us"]) == 5 and len(new_lobby["them"]) == 5:
                    time.sleep(60)

            time.sleep(5)

    # Create and start the thread
    thread = threading.Thread(target=update)
    thread.start()



    # Run the main loop
    root.mainloop()

if __name__ == "__main__": # pragma: no cover
    

    lockfile = ""

    # Check default location for lockfile
    default = "C:\\Program Files\\Riot Games\\League of Legends\\"
    if os.path.exists(default):
        lockfile = os.path.join(default, "lockfile")
        logger.debug("Found default lockfile location")

    # Look for running process and look for lockfile from there
    process = psutil.process_iter(attrs=['name'])
    process = [p for p in process if p.info["name"] == "RiotClientUxRender.exe"]

    if process:
        logger.debug("[Lockfile] Found running client process...")
        executable_path = process[0].exe()

        executable_path = "\\".join(executable_path.split("\\")[:2] + ["League of Legends", "lockfile"])

        if os.path.exists(executable_path):
            lockfile = executable_path

    # Show Settings window if all else fails
    if not lockfile and not os.path.exists("lockfile-location"):
        logger.debug("No lockfile - showing settings window")
        show_settings_window()

    if not lockfile and os.path.exists("lockfile-location"):
        logger.debug("Found a lockfile location...")
        with open("lockfile-location", "r") as f:
            lockfile = f.read()
    
    logger.debug(f"Lockfile:{lockfile}")
    show_main_window(lockfile)
