import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def url_encode(url):
    return url.replace("*", "%2A").replace("/", "%2F")

def wiki_url(url):
    if url.startswith("https://en.wikipedia.org/wiki/"):
        return url
    else:
        return f"https://en.wikipedia.org/wiki/{url}"


def url_request(url):
    """
    Make a request to the given url
    :param url
    :return: response of the request
    """
    return requests.get(wiki_url(url))


def get_categories(url):

    # Make a request to the article URL
    response = url_request(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the article
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the categories section in the article
        categories_section = soup.find(id='mw-normal-catlinks')

        # Extract the category links
        categories = []
        if categories_section:
            category_links = categories_section.find_all('a')
            for link in category_links:
                category = link.text
                if category != 'Categories':
                    categories.append(category)

        return categories
    else:
        print("Error retrieving article:", response.status_code)
        return None


def extract_wikipedia_links(article_url):
    # Make a request to the article URL
    response = url_request(article_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the article
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the anchor tags in the article
        links = soup.find_all('a')

        pass

        # Extract the Wikipedia links
        wikipedia_links = set()
        for link in links:
            href = link.get('href')
            if href and re.match(r'^/wiki/[^:]+$', href):
                wikipedia_links.add(url_encode(href.replace("/wiki/", "").split("#", 1)[0]))

        # Remove the link to the page itself
        wikipedia_links.discard(article_url.replace("https://en.wikipedia.org", ""))

        return list(wikipedia_links)
    else:
        print('Error retrieving article:', response.status_code)
        return None


def check_wikipedia_article_exists(url):
    # if not url.startswith("https://en.wikipedia.org/wiki/"):
    #     url = f"https://en.wikipedia.org/wiki/{url}"
    response = requests.head(wiki_url(url))
    return response.status_code == 200


def get_title(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title_element = soup.find('h1', id='firstHeading')
    return title_element.text


if __name__ == "__main__":

    root_url = "https://en.wikipedia.org/wiki/Mathematics"

    categories = get_categories(root_url)
    links = extract_wikipedia_links(root_url)

    if categories:
        print(f"Categories: {categories}")

    for link in links:
        print(f"  {link}")

    for link in links:
        if not check_wikipedia_article_exists(link):
            print(f"{link} not found")



    pass
