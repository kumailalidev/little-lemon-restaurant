import os
import json
from django import setup as django_setup

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "littlelemonrestaurant.settings")
django_setup()

# import Menu model
from restaurant.models import Menu


def add_menu_items(json_file_path):
    """
    Function to store menu items into database from
    an json file.
    """

    with open(json_file_path, "r") as json_file:
        menu_data = json.load(json_file)

        for menu_item in menu_data:
            menu = Menu(
                name=menu_item["name"],
                price=menu_item["price"],
                menu_item_description=menu_item["description"],
            )
            menu.save()


if __name__ == "__main__":
    json_file_path = "data/menu_items.json"
    add_menu_items(json_file_path)
