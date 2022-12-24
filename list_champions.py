"""
ChatGPT Prompt:
    - can you create a python program that downloads a webpage and then parses the title of all links with the class "category-page__member-link"?
"""
import requests
import os
import re
import urllib.parse

from bs4 import BeautifulSoup
from PIL import Image
from typing import List



def list_champions():
    """
    Generates a list of champions
    """
    # Download the webpage
    url = "https://leagueoflegends.fandom.com/wiki/Category:Playable_characters"
    class_name = 'category-page__member-link'


    page = requests.get(url)

    # Parse the HTML of the webpage
    soup = BeautifulSoup(page.text, 'html.parser')

    # Find all links with the class "category-page__member-link"
    links = soup.find_all('a', class_=class_name)

    # Print the titles of the links
    a = []
    for link in links:
        a.append(link.get("title"))
    return a

def find_all_champion_links():
    """
    Downloads all champion thumbnails

    """
    base_url = "https://leagueoflegends.fandom.com/wiki/Category:Champion_circles?from="
    class_name = "category-page__member-thumbnail"
    letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    results = []

    for letter in letters:
        print("Starting on", letter)
        page = requests.get(f"{base_url}{letter}")

        soup = BeautifulSoup(page.text, 'html.parser')

        # Find all links with the class "category-page__member-link"
        links = soup.find_all('img', class_= class_name)
        print("Links:", links)
        for link in links:
            print("Looking at", link)
            if "OriginalCircle" in link.get("alt"):
                temp = link.get("src").split("/revision/")[0]
                results.append(temp)
                print("Found", temp)
    
    return results

def download_image(url:str):
    """
    ChatGPT Prompt:
        - python program to download an image from a given url
    """
    # Send a GET request to the URL
    response = requests.get(url)

    # Save the image to a file
    filename = urllib.parse.unquote(url.split("/")[-1]).replace("_OriginalCircle.png", "").lower()
    filename = re.sub(r"[^a-zA-Z]", "", filename)

    output_filename = f"images/{filename}.png"

    with open(output_filename, "wb") as file:
        file.write(response.content)
    
    return output_filename

def trim_images(path:str):
    """
    Trims images
    """
    image = Image.open(path)

    # Crop the image 20 pixels from each side
    width, height = image.size
    cropped_image = image.crop((20, 20, width - 20, height - 20))

    image.close()

    # Resize to 60x60
    cropped_image = cropped_image.resize((60,60))

    # Save the cropped image to a file
    cropped_image.save(path)

def download_missing_champions():
    """
    Downloads all the missing champion items
    """
    def parse_champ_name(name:str):
        """Parses the champ name from the URL"""
        return name.split("/")[-1].split("_")[0]

    links = find_all_champion_links()

    if not os.path.exists("images"):
        os.mkdir("images")

    current_files = os.listdir("images")

    for link in links:
        if parse_champ_name(link) + ".png" not in current_files:
            print("Downloading", parse_champ_name(link),"...")
            output_filename = download_image(link)
            trim_images(output_filename)