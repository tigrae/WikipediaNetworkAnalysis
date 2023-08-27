from util import *


def count_articles_by_root_cats(articles):
    count_dict = {}  # Dictionary to store the count for each number of root categories

    for article in articles:
        num_root_cats = len(article.root_cats)  # Calculate the number of root categories for the article

        if num_root_cats in count_dict:
            count_dict[num_root_cats] += 1
        else:
            count_dict[num_root_cats] = 1

    return count_dict


if __name__ == "__main__":

    """ load categories and articles """
    categories = load_all_categories("./saved/categories")
    articles = load_all_articles("./saved/articles")

    """ get number of categories """
    article_count_by_root_cats = count_articles_by_root_cats(articles)
    for num_root_cats, count in article_count_by_root_cats.items():
        print(f"Articles with {num_root_cats} root categories: {count}")

    """ fill articles """
    for article in tqdm.tqdm(articles, desc="Finding related articles"):
        article.fill()

    """ get number of relations over all articles"""
    num_relations = 0
    for article in articles:
        num_relations += len(article.relations)
    print(f"Number of related articles: {num_relations}")

    """ create related articles """
    for i, article in enumerate(articles):
        for relation in tqdm.tqdm(article.relations, desc=f"Creating related article instances for {article.title}"):
            Article(relation, source=article.title, related_cats=article.root_cats, autosave=True)
        print(f"{i}/{len(articles)} Done!")

    pass
