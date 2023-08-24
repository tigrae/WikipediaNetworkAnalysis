import os
import json
import warnings
from util.scraping import *


def get_save_path():
    filepath = os.path.dirname(__file__)
    if filepath.endswith("util"):
        filepath = os.path.dirname(filepath)
    return filepath


class Category:
    """
    A category class used to scrape and evaluate wikipedia articles.
    """
    def __init__(self, title, articles=None, autosave=None):
        if title.endswith(".json"):
            self.load(title)
            # overwrite autosave settings
            if autosave is not None:
                self.autosave = autosave
        else:
            self.autosave = True if autosave is None else autosave
            self.title = title
            self.articles = () if articles is None else set(articles)
            if not check_wikipedia_article_exists(f"Category:{self.title}"):
                print(f"\033[91mWarning: Category \"{self.title}\" does not exist.\033[0m")

        if self.autosave:
            self.save()

    def add_articles(self, new_articles):
        """
        Add new articles to the class
        :param new_articles: List or str representing articles
        :return: None
        """

        def add_articles(self, new_articles):
            if isinstance(new_articles, list):
                self.articles.update(new_articles)
            elif isinstance(new_articles, str):
                self.articles.add(new_articles)
            else:
                raise ValueError(f"Error adding articles to Category \"{self.title}\". Pass new articles as string or list.")
            if self.autosave:
                self.save()

    def _create_instance_dict(self):
        return {
            "type": "Category",
            "autosave": self.autosave,
            "title": self.title,
            "articles": list(self.articles)
        }

    def save(self, filename=None, filepath=None):
        # set file name
        if filename is None:
            filename = self.title
        # get save path
        if filepath is None:
            filepath = get_save_path()
            filepath = f"{filepath}\\saved\\categories\\{filename}.json"
        # make directory
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # save file
        with open(filepath, "w") as file:
            json.dump(self._create_instance_dict(), file, indent=4)

    def load(self, path):
        with open(path, "r") as json_file:
            data = json.load(json_file)
        if data["type"] == "Category":
            self.autosave = data["autosave"]
            self.title = data["title"]
            self.articles = set(data["articles"])
        else:
            raise ValueError(f"Loading Category: \"{path}\" is not a Category.")


class Article:
    def __init__(self, title, relations=None, fill=False, autosave=None):
        if title.endswith(".json"):
            self.load(title)
            # overwrite autosave settings
            if autosave is not None:
                self.autosave = autosave
        else:
            self.autosave = True if autosave is None else autosave
            self.title = title
            self.relations = [] if relations is None else set(relations)
            if not check_wikipedia_article_exists(self.title):
                print(f"\033[91mWarning: Article \"{self.title}\" does not exist.\033[0m")

        if fill:
            pass

    def _create_instance_dict(self):
        return {
            "type": "Article",
            "autosave": self.autosave,
            "title": self.title,
            "relations": list(self.relations)
        }

    def save(self, filename=None, filepath=None):
        # set file name
        if filename is None:
            filename = self.title
        # get save path
        if filepath is None:
            filepath = get_save_path()
            filepath = f"{filepath}\\saved\\articles\\{filename}.json"
        # make directory
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # save file
        with open(filepath, "w") as file:
            json.dump(self._create_instance_dict(), file, indent=4)

    def load(self, path):
        with open(path, "r") as json_file:
            data = json.load(json_file)
        if data["type"] == "Article":
            self.autosave = data["autosave"]
            self.title = data["title"]
            self.relations = set(data["relations"])
        else:
            raise ValueError(f"Loading Article: \"{path}\" is not an Article.")


if __name__ == "__main__":

    # test = Category("Mathematics", ["Awhoopsiedoodle", "Schwoppbobberekoogar"])
    # test.save()

    test = Category("C:/Users/tilma/OneDriveUni/OneDrive - Universität Paderborn/Studium Winfo/6. Semester SS 23/Studienarbeit Social Media/WikipediaNetworkAnalysis/saved/Mathematics.json")

    pass

