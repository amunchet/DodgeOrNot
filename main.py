"""
Chat GPT prompt: 
    - python gui create window that is 375px by 220px.  The window has a background color of light blue.  There are two columns.  The first has the text "Our Team" (font Arial, 25px size) followed by a thin gray line, followed by a 150px by 50px green box that contains the large text (30px) "50.7%".  The second column is the same, except the text says "Enemy Team" and the green box is instead orange.  Below the two columns is a button that says "Settings" and opens another window which allows the user to input a file path that is saved to a file.
    - create a new python gui program that has a label with a background of green and text that says "Hello!".  In a new thread, change the background of that label to red and the text to say "New", then change it back every 5 seconds
    - create a python gui that starts with the window in the bottom right corner of the screen
    - Python GUI with top text that says "Please enter the location of LoL" folowed by an input, then followed by a button that saves the input to a file
"""
import os
import time
import threading
import tkinter as tk

import client
import stats

def show_settings_window(): # pragma: no cover
    """
    Shows the settings window on startup
    """

    # Create the main window
    root = tk.Tk()

    root.wm_title("DodgeOrNot")
    root.wm_iconbitmap("logo.ico")

    # Create the frame to hold the widgets
    frame = tk.Frame(root)
    frame.pack()

    # Create the label widget
    label = tk.Label(frame, text="Please enter the location of LoL:")
    label.pack()

    # Create the entry widget
    entry = tk.Entry(frame)
    entry.pack()

    # Define the function to handle the button click event
    def save_input():
        # Get the input from the entry widget
        input_text = entry.get()
        
        # Write the input to a file
        with open("lockfile-location", "w") as f:
            f.write(input_text.strip())
        
        root.destroy()

    # Create the button widget
    button = tk.Button(frame, text="Save", command=save_input)
    button.pack()

    # Run the main loop
    root.mainloop()



def show_main_window(lockfile): # pragma: no cover
    """
    Main Window
    """
    # Create the main window
    root = tk.Tk()
    # root.geometry("425x200")
    # root.configure(bg="lightblue")

    root.wm_title("DodgeOrNot")
    root.wm_iconbitmap("logo.ico")

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
            if new_lobby != current_lobby:
                our_chances = stats.check_synergies(new_lobby["us"])
                their_chances = stats.check_synergies(new_lobby["them"])

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
    if not os.path.exists("lockfile-location"):
        show_settings_window()

    with open("lockfile-location", "r") as f:
        lockfile = f.read()

    show_main_window(lockfile)
