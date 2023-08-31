import matplotlib.pyplot as plt
import tqdm
from statistics import mean, stdev
from util.classes import load_all_categories, load_all_articles, Article
from counting import count_cat_occurrences_in_articles


def draw_horizontal_bar_chart(plot_dict, title="", xlabel="", ylabel=""):
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(list(plot_dict.keys())[::-1], list(plot_dict.values())[::-1], color="#00b87a")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()

    for bar in bars:
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.0f}', ha='left',
                 va='center', color='black')

    ax.grid(axis='x', which='both', linestyle='dashed', linewidth=0.8, color='gray')
    # for i in range(25, max(plot_dict.values()) + 1, 25):
    #     ax.vlines(i, ymin=-0.5, ymax=len(plot_dict), color='0.8', linestyle='solid', linewidth=0.5, zorder=0)

    plt.show()


def draw_category_article_number(categories, n=0):
    """
    Counts the articles belonging to each category and represents the data in a bar chart
    :param categories: list of category objects
    :return:
    """

    cat_article_count = {}
    for category in categories:
        cat_article_count[category.title.replace("Category:", "").replace("_", " ")] = len(category.articles)

    # sort and get max name length
    cat_article_count = dict(sorted(cat_article_count.items(), key=lambda item: item[1], reverse=True))
    max_name_length = max(map(len, cat_article_count.keys()))

    # print and draw
    for category, num_articles in cat_article_count.items():
        print(f"\033[34;1m{category.ljust(max_name_length)}: {num_articles} Articles\033[31;0m")
    print(f"-> Mean: {mean(cat_article_count.values())}")
    print(f"-> Standard Deviation: {stdev(cat_article_count.values())}")
    print()

    # draw_horizontal_bar_chart(cat_article_count, title="Number of Articles per Category", xlabel="Articles", ylabel="Category")



    loaded_articles = {}
    related_article_count = {}
    for category in categories:
        related_article_count[category.title.replace("Category:", "").replace("_", " ")] = 0
        for article_title in category.articles:
            _current_article = None
            if article_title not in loaded_articles:
                _current_article = Article(article_title, autosave=False)
                loaded_articles[article_title] = _current_article
            else:
                _current_article = loaded_articles[article_title]
            related_article_count[category.title.replace("Category:", "").replace("_", " ")] += len(_current_article.relations)

    # sort and get max name length
    # related_article_count = dict(sorted(related_article_count.items(), key=lambda item: item[1], reverse=True))
    related_article_count = {key: related_article_count[key] for key in cat_article_count.keys()}
    # related_article_count = dict(sorted(related_article_count.items(), key=lambda item: item[1], reverse=True))
    max_name_length = max(map(len, related_article_count.keys()))

    # print and draw
    for category, num_articles in related_article_count.items():
        print(f"\033[34;1m{category.ljust(max_name_length)}: {num_articles} Related Articles (1st degree)\033[31;0m")
    print(f"-> Mean: {mean(related_article_count.values())}")
    print(f"-> Standard Deviation: {stdev(related_article_count.values())}")
    print()

    # draw_horizontal_bar_chart(related_article_count, title="Number of related Articles", xlabel="Articles", ylabel="Category")

    """ representation as bar chart """
    # Create a figure with two subplots arranged side by side
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Plot the first bar chart (directly linked articles)
    bars1 = axs[0].barh(list(cat_article_count.keys())[::-1], list(cat_article_count.values())[::-1], color='blue')
    axs[0].set_title('Directly Linked Articles')
    axs[0].set_xlabel('Number of Articles')

    # Plot the second bar chart (indirectly linked articles)
    bars2 = axs[1].barh(list(related_article_count.keys())[::-1], list(related_article_count.values())[::-1],
                        color='green')
    axs[1].set_title('Indirectly Linked Articles')
    axs[1].set_xlabel('Number of Articles')
    axs[1].set_yticklabels([])

    for i, bars in enumerate([bars1, bars2]):
        for bar in bars:
            axs[i].text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.0f}', ha='left',
                            va='center', color='black')

    # Configure grid and layout
    axs[0].grid(axis='x', which='both', linestyle='dashed', linewidth=0.8, color='gray')
    axs[1].grid(axis='x', which='both', linestyle='dashed', linewidth=0.8, color='gray')
    plt.tight_layout()

    # Show the combined figure with both bar charts
    plt.show()

    if n == 2:
        cat_occurrences = count_cat_occurrences_in_articles(categories, articles)
        cat_occurrences_short_title = {key.replace("Category:", "").replace("_", " "): value for key, value in cat_occurrences.items()}
        cat_occurrences_short_title = dict(sorted(cat_occurrences_short_title.items(), key=lambda item: item[1], reverse=True))
        draw_horizontal_bar_chart(cat_occurrences_short_title, "Category Occurrences in Articles", "Number of occurrences")
        print(f"-> Mean: {mean(cat_occurrences_short_title.values())}")
        print(f"-> Standard Deviation: {stdev(cat_occurrences_short_title.values())}")


if __name__ == "__main__":

    categories = load_all_categories("./saved/categories", autosave=False)
    articles = load_all_articles("./saved/articles", autosave=False)
    draw_category_article_number(categories, n=2)


    pass

