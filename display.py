"""
Chat GPT prompt: 
    - create a python program to show a window on the bottom right of the screen that says either "Play" with a green background or "Dodge" with a red background
    - Can you make a table above with 3 rows?  In the first row, the left column item should say "Our Champion", the right column should say the contents of the variable our_champ.  The second row, the left column should say "Our/Theirs Agg. WR" and the right column should say "50-40".  The third row first column should say "Our Synergy" and the second column should say "45%"
"""

import tkinter as tk

# Create the main window
window = tk.Tk()

# Set the window title
window.title("Action Window")

# Set the window size
window.geometry("200x150+1200+700")

# Create a frame to hold the buttons
button_frame = tk.Frame(window)

# Create a button with the text "Capture" and a blue background
capture_button = tk.Button(window, text="Capture", bg="blue", fg="white", width=20, height=5)

# Display the capture button on the window
capture_button.pack(side="top")

# Create a button with the text "Play" and a green background
play_button = tk.Button(button_frame, text="Play", bg="green", fg="white", width=20, height=5)

# Create a button with the text "Dodge" and a red background
dodge_button = tk.Button(button_frame, text="Dodge", bg="red", fg="white", width=20, height=5)

# Display the buttons on the frame
play_button.pack(side="left")
dodge_button.pack(side="right")

# Display the frame on the window
button_frame.pack(side="bottom")

# Create a frame to hold the table
table_frame = tk.Frame(window)

# Create the first row of the table
row1 = tk.Frame(table_frame)

# Create the left column of the first row
col1 = tk.Label(row1, text="Our Champion", width=15)

# Create the right column of the first row
our_champ = "Diana"
col2 = tk.Label(row1, text=our_champ, width=15)

# Display the columns in the first row
col1.pack(side="left")
col2.pack(side="right")

# Create the second row of the table
row2 = tk.Frame(table_frame)

# Create the left column of the second row
col3 = tk.Label(row2, text="Our/Theirs Agg. WR", width=15)

# Create the right column of the second row
col4 = tk.Label(row2, text="50-40", width=15)

# Display the columns in the second row
col3.pack(side="left")
col4.pack(side="right")

# Create the third row of the table
row3 = tk.Frame(table_frame)

# Create the left column of the third row
col5 = tk.Label(row3, text="Our Synergy", width=15)

# Create the right column of the third row
col6 = tk.Label(row3, text="45%", width=15)

# Display the columns in the third row
col5.pack(side="left")
col6.pack(side="right")

# Display the rows in the frame
row1.pack()
row2.pack()
row3.pack()

# Display the frame on the window
table_frame.pack()

# Run the main loop
window.mainloop()
