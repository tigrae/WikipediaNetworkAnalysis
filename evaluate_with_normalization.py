"""
In this script, data is evaluated.
Evaluated data is brought into a format that is usable for visualization using Gephi
"""
import tqdm
import csv
import numpy as np
import matplotlib.pyplot as plt
from util.classes import load_all_articles, load_all_categories
from itertools import combinations
from counting import count_cat_occurrences_in_articles
from statistics import mean


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

    """ Normalize values """
    rep = count_cat_occurrences_in_articles(categories, articles)
    rep_mean = mean([value for value in rep.values()])
    normalized_cat_comb_occurrences = dict()
    for comb, value in cat_comb_occurrences.items():
        # calculate normalization factor
        comb_list = comb.split("+")
        cat_a = f"Category:{comb_list[0]}"
        cat_b = f"Category:{comb_list[1]}"
        normalization_factor = 1/(rep[cat_a]/rep_mean) + 1/(rep[cat_b]/rep_mean)
        normalized_cat_comb_occurrences[comb] = cat_comb_occurrences[comb] * normalization_factor

    pass


    """ Visualize relations in table """
    value_array = np.array([[0 for _ in range(22)] for _ in range(22)])
    for cat_pair, value in normalized_cat_comb_occurrences.items():
        cat_pair = cat_pair.split("+")
        value_array[category_titles.index(cat_pair[0])][category_titles.index(cat_pair[1])] = value
        value_array[category_titles.index(cat_pair[1])][category_titles.index(cat_pair[0])] = value
    # Normalize the data for color mapping
    normalized_value_array = (value_array - np.min(value_array)) / (np.max(value_array) - np.min(value_array))

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Create a heatmap using imshow
    heatmap = ax.imshow(normalized_value_array, cmap='BuGn', interpolation='nearest')

    # Show colorbar
    cbar = plt.colorbar(heatmap, ax=ax)
    cbar.set_label('Relation Strength')

    # Set x and y axis labels
    ax.set_xticks(np.arange(len(category_titles)))
    ax.set_yticks(np.arange(len(category_titles)))
    ax.set_xticklabels(category_titles, rotation=45, ha="right")
    ax.set_yticklabels(category_titles)

    # Display values in the cells
    for i in range(len(category_titles)):
        for j in range(len(category_titles)):
            ax.text(j, i, f'{value_array[i, j]}', ha='center', va='center', color='black')

    # Set title
    plt.title('Relation Strength Between Categories')

    # Show the heatmap
    plt.show()


    """ Create node csv """
    node_data = [["Id", "Label"]]
    for i, category in enumerate(category_titles):
        node_data.append([i, category.replace("Category:", "")])
    with open("./results/nodes_normalized.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=";")
        for row in node_data:
            csvwriter.writerow(row)

    """ Create edge csv """
    edge_data = [["Source", "Target", "Type", "Weight"]]
    for key, value in normalized_cat_comb_occurrences.items():
        source, target = key.split("+")
        edge_data.append([category_titles.index(source), category_titles.index(target), "Undirected", round(value)])
    with open("./results/edges_normalized.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=";")
        for row in edge_data:
            csvwriter.writerow(row)

