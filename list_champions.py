"""
ChatGPT Prompt:
    - can you create a python program that downloads a webpage and then parses the title of all links with the class "category-page__member-link"?
"""
import requests
from bs4 import BeautifulSoup
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
    for link in links:
        print(link.get('title'))

def download_all_thumbnails(champions: List[str]):
    """
    Downloads all champion thumbnails

    Script found here: https://gitlab.com/amunchet/one-trick-fan/-/tree/master/images
    """

    # TODO: Copy over from gitlab repo
