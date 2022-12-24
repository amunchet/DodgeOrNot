"""
Chat GPT prompt: 
    - python gui create window that is 375px by 220px.  The window has a background color of light blue.  There are two columns.  The first has the text "Our Team" (font Arial, 25px size) followed by a thin gray line, followed by a 150px by 50px green box that contains the large text (30px) "50.7%".  The second column is the same, except the text says "Enemy Team" and the green box is instead orange.  Below the two columns is a button that says "Settings" and opens another window which allows the user to input a file path that is saved to a file.
    - create a new python gui program that has a label with a background of green and text that says "Hello!".  In a new thread, change the background of that label to red and the text to say "New", then change it back every 5 seconds
    - create a python gui that starts with the window in the bottom right corner of the screen
"""

import tkinter as tk

# Create the main window
root = tk.Tk()
# root.geometry("425x200")
# root.configure(bg="lightblue")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size and position
window_width = 425
window_height = 200
window_x = screen_width - window_width
window_y = screen_height - window_height
root.geometry("{}x{}+{}+{}".format(window_width, window_height, window_x, window_y))
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
green_box1 = tk.Label(frame1, text="50.7%", bg="green", font=("Arial", 30), width=9, height=2)
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
orange_box2 = tk.Label(frame2, text="50.7%", bg="orange", font=("Arial", 30), width=9, height=2)
orange_box2.pack()


# Run the main loop
root.mainloop()
