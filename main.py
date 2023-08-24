from util.category_scraper import get_direct_subcategories, get_pages_in_category
from util.classes import Category, Article

if __name__ == "__main__":

    root_category = "Fields_of_mathematics"
    subcategories = get_direct_subcategories(root_category)

    for subcategory in subcategories:
        pages = get_pages_in_category(subcategory)
        Category(subcategory, pages)

