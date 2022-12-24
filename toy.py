import tkinter as tk
import threading
import time

# Create the main window
root = tk.Tk()

# Create the label
label = tk.Label(root, text="Hello!", bg="green", font=("Arial", 30))
label.pack()

# Define the function to update the label
def update_label():
    while True:
        label.configure(bg="red", text="New")
        root.update()
        time.sleep(5)
        label.configure(bg="green", text="Hello!")
        root.update()
        time.sleep(5)

# Create and start the thread
thread = threading.Thread(target=update_label)
thread.start()

# Run the main loop
root.mainloop()
