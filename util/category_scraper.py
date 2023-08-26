import requests
import re
from queue import Queue
from bs4 import BeautifulSoup
from util.scraping import *
from urllib.parse import quote


class Category_Node:
    def __init__(self, name, parent=None, subcategories=None):
        self.name = name
        self.parent = parent
        self.subcategories = subcategories if subcategories else []

    def add_subcategory(self, category_object):
        self.subcategories.append(category_object)

    def __str__(self):
        return f"Category: {self.name}"


def get_direct_subcategories(category):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmtype": "subcat",
        "cmlimit": "max"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        subcategories = [category['title'].replace(" ", "_") for category
                         in data['query']['categorymembers']]
        return subcategories
    else:
        print('Error retrieving direct subcategories:', response.status_code)
        return None


def get_pages_in_category(url):
    # Make a request to the article URL
    response = url_request(url)

    # Check if the request was successful
    if response.status_code == 200:

        # Remove everything before "pages in category" from response text
        text = "".join(response.text.split("Pages in category", 1)[1:])

        # Parse the manipulated HTML content of the article
        soup = BeautifulSoup(text, 'html.parser')

        # Find all the anchor tags in the article
        links = soup.find_all('a')

        # Extract the Wikipedia links
        wikipedia_links = set()
        for link in links:
            href = link.get('href')
            if href and re.match(r'^/wiki/[^:]+$', href):
                wikipedia_links.add(url_encode(href.replace("/wiki/", "")))

        # Remove the link to Main Page
        wikipedia_links.discard("Main_Page")

        return list(wikipedia_links)
    else:
        print('Error retrieving article:', response.status_code)
        return None


if __name__ == "__main__":

    root_category = Category_Node("Fields of mathematics")

    # define queue for categories not yet explored and categories_done set. Put root category in queue.
    categories_queue = Queue()
    categories_queue.put(root_category)
    # categories_done = set()
    categories_seen = set()

    i = 0

    while not categories_queue.empty():
        current_category = categories_queue.get()

        # check if the current category has been processed before
        if current_category.name in categories_seen:
            continue

        found_subcategories = get_direct_subcategories(current_category.name)

        # create objects for found subcategories, add them to current_category subcategories and queue.
        for category in found_subcategories:

            new_class = Category_Node(category, current_category.name)
            current_category.add_subcategory(new_class)
            categories_queue.put(new_class)

        # categories_done.add(current_category)
        categories_seen.add(current_category.name)

        i += 1
        if i % 10 == 0:
            print(f"Progress after {i} iterations: Done = {len(categories_seen)}, in Queue = {categories_queue.qsize()}")


    pass

    # subcategories = get_direct_subcategories("Fields of mathematics")
    # for c in subcategories:
    #     print(c)
    #
    # print()
    # subcategories = get_direct_subcategories(subcategories[0])
    # for c in subcategories:
    #     print(c)
