"""
ChatGPT Prompt: 
    - can you make a Windows python program that takes a screenshot of the desktop and then searches it to see if one of several given images matches?
"""
import os
import pyautogui
import cv2
import numpy as np

from PIL import Image

# Set the path to the images to search for
image_paths = os.listdir("images")

# Load the images into memory
images = []
for image_path in image_paths:
    image = cv2.imread(os.path.join("images", image_path))
    images.append((image_path,image))

# Take a screenshot of the desktop
screenshot = pyautogui.screenshot()
screenshot.save("screenshot.jpg")


# Convert the screenshot to a NumPy array
screenshot_np = np.array(screenshot)

# Convert the screenshot to grayscale
screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

# Loop through the images to search for
for (image_path,image) in images:
    # Convert the image to grayscale
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Use template matching to find the image in the screenshot
    result = cv2.matchTemplate(screenshot_gray, image_gray, cv2.TM_CCOEFF_NORMED)

    # Get the coordinates of the match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # If the match is above a certain threshold, print the result
    print("Max val:", max_val, "for", image_path)
    if max_val > 0.8:
        print(f"Found {image_path} at ({max_loc[0]}, {max_loc[1]})")

        with Image.open("screenshot.jpg") as s:
            s =  s.crop((max_loc[0], max_loc[1], max_loc[0] + 60, max_loc[1] + 60))
            s.save(f"screenshot-{image_path}.jpg")

# If no match was found, print a message
print("No match found.")
