import os
import glob
import tqdm
from util.classes import load_all_articles, Article


if __name__ == "__main__":
    """ This file will fix sources for all articles """

    root_articles = load_all_articles("./saved/_root_articles", autosave=False)

    """ create relations and save """
    # for article in tqdm.tqdm(root_articles, desc="Finding related articles"):
    #     article.fill()
    #     article.save(filepath="./saved/_root_articles")
    #     article.save()

    articles = load_all_articles("./saved/articles")

    for article in tqdm.tqdm(articles, desc="Repairing Sources"):
        for root_article in root_articles:
            if article.title in root_article.relations:
                article.add_source(root_article.title)

    pass
