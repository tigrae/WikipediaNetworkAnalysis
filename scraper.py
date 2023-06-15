import requests
from bs4 import BeautifulSoup


def url_request(url):
    """
    Make a request to the given url
    :param url
    :return: response of the request
    """
    return requests.get(url)


def get_title(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title_element = soup.find('h1', id='firstHeading')
    return title_element.text


if __name__ == "__main__":

    url = "https://en.wikipedia.org/wiki/Mathematics"
    response = requests.get(url)
    html_content = response.text

    title = get_title(html_content)




    pass
