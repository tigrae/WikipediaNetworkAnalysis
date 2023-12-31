"""
This script contains several functions used to count certain values of multiple articles or categories
"""
import matplotlib.pyplot as plt
from util.classes import *

def count_articles_by_root_cats(articles):
    count_dict = {}  # Dictionary to store the count for each number of root categories

    for article in articles:
        num_root_cats = len(article.root_cats)  # Calculate the number of root categories for the article

        if num_root_cats in count_dict:
            count_dict[num_root_cats] += 1
        else:
            count_dict[num_root_cats] = 1

    return count_dict


def count_articles_by_related_cats(articles):
    count_dict = {}  # Dictionary to store the count for each number of root categories

    for article in articles:
        num_related_cats = len(article.related_cats)  # Calculate the number of root categories for the article

        if num_related_cats in count_dict:
            count_dict[num_related_cats] += 1
        else:
            count_dict[num_related_cats] = 1

    return count_dict


def count_relations(articles):
    num_relations = 0
    individual_relations = set()
    for article in articles:
        num_relations += len(article.relations)
        individual_relations.update(article.relations)
    print(f"{num_relations} Links leading to {len(individual_relations)} individual articles.")


def count_sources(articles, prt=True):
    count_dict = {}  # Dictionary to store the count for each number of root categories

    for article in articles:
        num_sources = len(article.source)  # Calculate the number of root categories for the article

        if num_sources in count_dict:
            count_dict[num_sources] += 1
        else:
            count_dict[num_sources] = 1

    if prt:
        for num_sources, count in count_dict.items():
            print(f"Articles with {num_sources} sources: {count}")

    return count_dict


def count_cat_occurrences_in_articles(categories, articles, prt=True):

    count_dict = {category.title: 0 for category in categories}

    for article in tqdm.tqdm(articles, desc="Counting category occurrences in articles"):
        for category in [c.title for c in categories]:
            if category in article.related_cats:
                count_dict[category] += 1

    if prt:
        for num_cat_occs, count in count_dict.items():
            print(f"{num_cat_occs} occurrences: {count}")

    return count_dict


if __name__ == "__main__":

    """ load categories and articles """
    categories = load_all_categories("./saved/categories", autosave=False)
    root_articles = load_all_articles("./saved/_root_articles", autosave=False)
    articles = load_all_articles("./saved/articles", autosave=False)

    """ get number of root categories """
    # article_count_by_root_cats = count_articles_by_root_cats(articles)
    # for num_root_cats, count in article_count_by_root_cats.items():
    #     print(f"Articles with {num_root_cats} root categories: {count}")

    """ get number relations in root articles """
    # count_relations(articles)

    """ get number of related categories """
    article_count_by_related_cats = count_articles_by_related_cats(articles)
    # for num_related_cats, count in article_count_by_related_cats.items():
    #     print(f"Articles with {num_related_cats} related categories: {count}")

    """ get number of related categories """
    article_count_by_related_cats = count_sources(articles, prt=True)

    """ get number of category occurrences in articles """
    ncaia = count_cat_occurrences_in_articles(categories, articles)

    # fig, ax = plt.subplots(figsize=(10, 6))
    # bars = ax.barh(list(ncaia.keys())[::-1], list(ncaia.values())[::-1], color='blue')
    # plt.xlabel("Number of occurrences")
    # plt.ylabel("Category")
    # plt.title("Category Occurrences in Articles")
    # plt.tight_layout()
    #
    # for bar in bars:
    #     plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.0f}', ha='left',
    #              va='center', color='black')
    #
    # ax.grid(axis='x', which='both', linestyle='dashed', linewidth=0.8, color='gray')
    #
    # plt.show()

