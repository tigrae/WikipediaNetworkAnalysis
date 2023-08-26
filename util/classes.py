import os
import json
import warnings
from util.scraping import *
from urllib.parse import quote


def get_save_path():
    """
    Instances of both the Category and Article class can be saved and loaded as a json file.
    The directory in which these are saved is hardcoded:

        project_root
         └─── saved
               ├─── categories      # category instance json files
               └─── articles        # article instance json files

    Depending on where in the code the save function is called, the path to the "saved" directory can be retrieved here

    :return: path under which classes should be saved
    """
    path = os.path.dirname(__file__)
    if path.endswith("util"):
        path = os.path.dirname(path)
    return path


class Category:
    """
    Class representing a wikipedia category
    Contains title of the category as well as pages assigned to it
    """
    def __init__(self, title, articles=None, autosave=None):
        """
        Initialize a category instance
        :param title: title of the category or path to .json file to load instance from
        :param articles: str or list of articles
        :param autosave: manual call of the save() function necessary if False. Default: True
        """

        if title.endswith(".json"):
            # load saved instance
            self.load(title)
            # overwrite autosave settings
            if autosave is not None:
                self.autosave = autosave
        else:
            # initialize new instance
            self.autosave = True if autosave is None else autosave
            self.title = url_encode(title)
            self.articles = ()
            self.articles = set() if articles is None else {articles} if isinstance(articles, str) else set(articles)

            if not check_wikipedia_article_exists(f"{self.title}"):
                print(f"\033[91mWarning: Category \"{self.title}\" does not exist.\033[0m")
                self.autosave = False

            if self.autosave:
                self.save()

    def add_articles(self, new_articles, no_save=False):
        """
        Add new articles to the class
        :param new_articles: str or list of articles
        :param no_save: ignore autosave if True
        """
        def add_articles(self, new_articles):
            if isinstance(new_articles, list):
                self.articles.update(new_articles)
            elif isinstance(new_articles, str):
                self.articles.add(new_articles)
            else:
                raise ValueError(f"Error adding articles to Category \"{self.title}\". Pass new articles as string or list.")

            if not no_save:
                if self.autosave:
                    self.save()

    def _create_instance_dict(self):
        """ return instance attributes as dict for saving """
        return {
            "type": "Category",
            "autosave": self.autosave,
            "title": self.title,
            "articles": list(self.articles)
        }

    def save(self, filename=None, filepath=None):
        """
        Save instance as json file
        :param filename: file name. Default: Class name
        :param filepath: save path. Default: save\categories
        """
        # set file name
        if filename is None:
            filename = self.title
        # get save path
        if filepath is None:
            filepath = get_save_path()
            filepath = f"{filepath}\\saved\\categories\\{filename.replace('Category:', '')}.json"
        # make directory
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # save file
        with open(filepath, "w") as file:
            json.dump(self._create_instance_dict(), file, indent=4)

    def load(self, path):
        """
        Load instance from json file
        :param path: Path to json file
        """
        with open(path, "r") as json_file:
            data = json.load(json_file)
        if data["type"] == "Category":
            self.autosave = data["autosave"]
            self.title = data["title"]
            self.articles = set(data["articles"])
        else:
            raise ValueError(f"Loading Category: \"{path}\" is not a Category.")

    def __str__(self):
        return f"{self.title}. {len(self.articles)} articles."


class Article:
    """
    Class representing a wikipedia article
    Contains title of the article and related articles, which are other articles linked in the text of the page.
    """
    def __init__(self, title, relations=None, root_cats=None, fill=False, autosave=None):
        """
        Initialize a article instance
        :param title: title of the article or path to .json file to load instance from
        :param relations: str or list of related (linked) articles
        :param root_cats: str or list of root categories
        :param fill: Automatically get related articles if True
        :param autosave: manual call of the save() function necessary if False. Default: True
        """

        if title.endswith(".json"):
            self.load(title)
            # overwrite autosave settings
            if autosave is not None:
                self.autosave = autosave
        else:
            self.autosave = True if autosave is None else autosave
            self.title = url_encode(title)
            self.relations = set() if relations is None else {relations} if isinstance(relations, str) else set(relations)
            self.root_cats = set() if root_cats is None else {root_cats} if isinstance(root_cats, str) else set(root_cats)

            if not check_wikipedia_article_exists(self.title):
                print(f"\033[91mWarning: Article \"{self.title}\" does not exist.\033[0m")
                self.autosave = False

            if autosave:
                self.save()

        if fill:
            pass

    def _create_instance_dict(self):
        """ return instance attributes as dict for saving """
        return {
            "type": "Article",
            "autosave": self.autosave,
            "title": self.title,
            "relations": list(self.relations),
            "root categories": list(self.root_cats)
        }

    def save(self, filename=None, filepath=None):
        """
        Save instance as json file
        :param filename: file name. Default: Class name
        :param filepath: save path. Default: save\categories
        """
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
        """
        Load instance from json file
        :param path: Path to json file
        """
        with open(path, "r") as json_file:
            data = json.load(json_file)
        if data["type"] == "Article":
            self.autosave = data["autosave"]
            self.title = data["title"]
            self.relations = set(data["relations"])
        else:
            raise ValueError(f"Loading Article: \"{path}\" is not an Article.")

    def __str__(self):
        return f"Article:{self.title}. {len(self.relations)} related articles. Root categories: {list(self.root_cats)}"


if __name__ == "__main__":

    test = Category("Mathematics", ["Whoopsiedoodle", "Schwoppbobberekoogar"])
    test.save()

    pass
