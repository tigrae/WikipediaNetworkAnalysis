from util.scraping import extract_wikipedia_links, wiki_url
from util.category_scraper import get_pages_in_category

category = "Category:Foundations_of_mathematics"
links = get_pages_in_category(wiki_url(category))

for l in links:
    print(l)
print(len(links))

get_pages_in_category(wiki_url(category))