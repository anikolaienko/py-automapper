from copy import deepcopy
from typing import Any, Dict

from automapper import mapper


class Candy:
    def __init__(self, name: str, brand: str):
        self.name = name
        self.brand = brand


class Shop:
    def __init__(self, products: Dict[str, Any], annual_income: int):
        self.products: Dict[str, Any] = deepcopy(products)
        self.annual_income = annual_income


class ShopPublicInfo:
    def __init__(self, products: Dict[str, Any]):
        self.products: Dict[str, Any] = deepcopy(products)


def test_map__with_dict_field():
    products = {
        "magazines": ["Forbes", "Time", "The New Yorker"],
        "candies": [
            Candy("Reese's cups", "The Hershey Company"),
            Candy("Snickers", "Mars, Incorporated"),
        ],
    }
    shop = Shop(products=products, annual_income=10000000)

    public_info = mapper.to(ShopPublicInfo).map(shop)

    assert public_info.products["magazines"] == shop.products["magazines"]
    assert id(public_info.products["magazines"]) != id(shop.products["magazines"])

    assert public_info.products["candies"] != shop.products["candies"]
    assert public_info.products["candies"][0] != shop.products["candies"][0]
    assert public_info.products["candies"][1] != shop.products["candies"][1]

    assert public_info.products["candies"][0].name == "Reese's cups"
    assert public_info.products["candies"][0].brand == "The Hershey Company"

    assert public_info.products["candies"][1].name == "Snickers"
    assert public_info.products["candies"][1].brand == "Mars, Incorporated"
