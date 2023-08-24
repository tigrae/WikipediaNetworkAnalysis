import json
import os

from util.category_scraper import get_direct_subcategories, get_pages_in_category
from util.classes import Category, Article

if __name__ == "__main__":

    root_category = "Fields_of_mathematics"
    subcategories = get_direct_subcategories(root_category)

    # for subcategory in subcategories:
    #     pages = get_pages_in_category(subcategory)
    #     Category(subcategory, pages)

    directorie = "./saved/categories"

    articles = {}
    for file in os.listdir(directorie):
        path = os.path.join(directorie, file)
        if os.path.isfile(path):
            f = open(path)
            data = json.load(f)
            for article in data["articles"]:
                articles.add(article)
    print(articles)