"""
In this script, data is evaluated.
Evaluated data is brought into a format that is usable for visualization using Gephi
"""
import tqdm
import csv
from util.classes import load_all_articles, load_all_categories
from itertools import combinations


if __name__ == "__main__":

    # load all categories and articles instances from JSON files
    categories = load_all_categories("./saved/categories", autosave=False)
    articles = load_all_articles("./saved/articles", autosave=False)

    category_titles = [category.title.replace("Category:", "") for category in categories]
    category_titles.sort()

    # create dict with category pairs
    cat_combs = set(combinations(category_titles, 2))
    cat_comb_occurrences = {f"{comb[0]}+{comb[1]}": 0 for comb in cat_combs}

    for article in tqdm.tqdm(articles, desc="Evaluating articles"):
        if len(article.related_cats) > 1:
            article_related_categories = [r.replace("Category:", "") for r in article.related_cats]
            article_related_categories.sort()

            article_cat_combs = set(combinations(article_related_categories, 2))
            article_cat_combs = set(f"{comb[0]}+{comb[1]}" for comb in article_cat_combs)
            for comb in article_cat_combs:
                cat_comb_occurrences[comb] += 1

    """ Create node csv """
    node_data = [["Id", "Label"]]
    for i, category in enumerate(category_titles):
        node_data.append([i, category.replace("Category:", "")])
    with open("./results/nodes.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=";")
        for row in node_data:
            csvwriter.writerow(row)

    edge_data = [["Source", "Target", "Type", "Weight"]]
    for key, value in cat_comb_occurrences.items():
        source, target = key.split("+")
        edge_data.append([category_titles.index(source), category_titles.index(target), "Undirected", value])
    with open("./results/edges.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=";")
        for row in edge_data:
            csvwriter.writerow(row)


