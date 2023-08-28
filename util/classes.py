import os
import json
import glob
import tqdm
import warnings
from util.scraping import *


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


def load_all_categories(save_dir):
    """
    Loads all categories from json files in a given directory.
    :param save_dir: Path to directory with category json files
    :return: List of all category instances initialized by the function
    """
    category_json_files = glob.glob(os.path.join(save_dir, "*.json"))
    categories = []
    for file in tqdm.tqdm(category_json_files, desc=f"Loading categories from {save_dir}"):
        current_category = Category(file)
        categories.append(current_category)
    return categories


def load_all_articles(save_dir, autosave=True):
    """
    Loads all articles from json files in a given directory.
    :param save_dir: Path to directory with article json files
    :return: List of all article instances initialized by the function
    """
    article_json_files = glob.glob(os.path.join(save_dir, "*.json"))
    articles = []
    for file in tqdm.tqdm(article_json_files, desc=f"Loading articles from {save_dir}"):
        current_article = Article(file, autosave=autosave)
        articles.append(current_article)
    return articles


def get_num_pages_in_categories(category_list):
    num_articles = 0
    for category in category_list:
        num_articles += len(category.articles)
    return num_articles


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
    def __init__(self, title, source=None, relations=None, root_cats=None, related_cats=None, fill=False, autosave=None):
        """
        Initialize a article instance
        :param title: title of the article or path to .json file to load instance from
        :param relations: str or list of related (linked) articles
        :param root_cats: str or list of root categories
        :param fill: Automatically get related articles if True
        :param autosave: manual call of the save() function necessary if False. Default: True
        """

        file_path = f"{get_save_path()}\\saved\\articles\\{url_encode(title)}.json"
        exists = os.path.exists(file_path)

        if title.endswith(".json"):
            """ load instance from json file """
            self.load(title)
            # overwrite autosave settings
            self.autosave = autosave if autosave is not None else self.autosave

        elif exists:
            """ update instance if it already exists"""
            # print(f"{title} already exists.")
            self.load(file_path)
            self.add_relations(relations) if relations is not None else None
            self.add_root_cats(root_cats) if root_cats is not None else None
            self.add_related_cats(related_cats) if related_cats is not None else None

            # overwrite autosave settings
            self.autosave = autosave if autosave is not None else self.autosave

            if self.autosave:
                self.save()

        else:
            """ initialize new instance """
            self.autosave = True if autosave is None else autosave
            self.title = url_encode(title)
            self.source = set() if source is None else {source}
            self.relations = set() if relations is None else {relations} if isinstance(relations, str) else set(relations)
            self.root_cats = set() if root_cats is None else {root_cats} if isinstance(root_cats, str) else set(root_cats)
            self.related_cats = set() if related_cats is None else {related_cats} if isinstance(related_cats, str) else set(related_cats)

            if not check_wikipedia_article_exists(self.title):
                print(f"\033[91mWarning: Article \"{self.title}\" does not exist.\033[0m")
                self.autosave = False

            if autosave:
                self.save()

        if fill:
            self.fill()

    def fill(self):
        """ get related articles """
        related_articles = set(extract_wikipedia_links(self.title))
        self.add_relations(related_articles)

    def add_root_cats(self, root_cats):
        """ adds one or more root category to the article """
        if isinstance(root_cats, str):
            self.root_cats.add(root_cats)
        elif isinstance(root_cats, list):
            self.root_cats.update(root_cats)

        if self.autosave:
            self.save()

    def add_relations(self, relations):
        """ adds one or more related articles to the article """
        if isinstance(relations, str):
            self.relations.add(relations)
        elif isinstance(relations, (list, set)):
            self.relations.update(relations)

        if self.autosave:
            self.save()

    def add_related_cats(self, related_cats):
        """ adds one or more related articles to the article """
        if isinstance(related_cats, str):
            self.related_cats.add(related_cats)
        elif isinstance(related_cats, (list, set)):
            self.related_cats.update(related_cats)

        if self.autosave:
            self.save()

    def add_source(self, source):
        """ adds one or more related articles to the article """
        if isinstance(source, str):
            self.source.add(source)
        elif isinstance(source, (list, set)):
            self.source.update(source)

        if self.autosave:
            self.save()

    def _create_instance_dict(self):
        """ return instance attributes as dict for saving """
        return {
            "type": "Article",
            "autosave": self.autosave,
            "title": self.title,
            "source": list(self.source),
            "root categories": list(self.root_cats),
            "related categories": list(self.related_cats),
            "relations": list(self.relations)
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
        elif filepath == "./saved/_root_articles":
            filepath = get_save_path()
            filepath = f"{filepath}\\saved\\_root_articles\\{filename}.json"
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
            self.source = set(data.get("source", set()))
            self.relations = set(data["relations"])
            self.root_cats = set(data["root categories"])
            self.related_cats = set(data["related categories"])
        else:
            raise ValueError(f"Loading Article: \"{path}\" is not an Article.")

    def __str__(self):
        return f"Article:{self.title}. {len(self.relations)} related articles. Root categories: {list(self.root_cats)}"


if __name__ == "__main__":
    """ main block for testing only """

    test = Category("Mathematics", ["Whoopsiedoodle", "Schwoppbobberekoogar"])
    test.save()

    pass
