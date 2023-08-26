import glob
import os
import tqdm
from util.classes import Category, Article
from util.category_scraper import get_direct_subcategories, get_pages_in_category


if __name__ == "__main__":

    category_save_dir = "./saved/categories"
    category_json_files = glob.glob(os.path.join(category_save_dir, "*.json"))
    categories = []
    articles = []

    num_articles = 0
    for file in category_json_files:
        current_category = Category(file)
        categories.append(current_category)
        num_articles += len(current_category.articles)

        for article in tqdm.tqdm(current_category.articles, desc=f"Fetching articles for {current_category.title}"):
            articles.append(Article(article, root_cats=current_category.title, autosave=True))

        print(f"{current_category.title} done! ({len(categories)}/{len(category_json_files)})")

    pass
