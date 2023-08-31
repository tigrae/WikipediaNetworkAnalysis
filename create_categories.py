import tqdm
from util import *


if __name__ == "__main__":
    """
    This script creates all Category objects for the subclasses of a given root class.
    The root class for this project (Fields_of_Mathematics) is hard-coded, but can be changed. 
    """

    root_category = "Fields_of_mathematics"
    subcategories = get_direct_subcategories(root_category)
    for subcategory in tqdm.tqdm(subcategories, desc=f"Creating subcategories of \"{root_category}\""):
        pages = get_pages_in_category(wiki_url(subcategory))
        Category(subcategory, pages)
    print(f"Done!")