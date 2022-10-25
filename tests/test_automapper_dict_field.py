from typing import Any, Dict
from unittest import TestCase

from automapper import create_mapper, mapper


class Candy:
    def __init__(self, name: str, brand: str):
        self.name = name
        self.brand = brand


class Shop:
    def __init__(self, products: Dict[str, Any], annual_income: int):
        self.products: Dict[str, Any] = products
        self.annual_income = annual_income


class ShopPublicInfo:
    def __init__(self, products: Dict[str, Any]):
        self.products: Dict[str, Any] = products


class AutomapperTest(TestCase):
    def setUp(self) -> None:
        products = {
            "magazines": ["Forbes", "Time", "The New Yorker"],
            "candies": [
                Candy("Reese's cups", "The Hershey Company"),
                Candy("Snickers", "Mars, Incorporated"),
            ],
        }
        self.shop = Shop(products=products, annual_income=10000000)
        self.mapper = create_mapper()

    def test_map__with_dict_field(self):
        public_info = mapper.to(ShopPublicInfo).map(self.shop)

        self.assertEqual(
            public_info.products["magazines"], self.shop.products["magazines"]
        )
        self.assertNotEqual(
            id(public_info.products["magazines"]), id(self.shop.products["magazines"])
        )

        self.assertNotEqual(
            public_info.products["candies"], self.shop.products["candies"]
        )
        self.assertNotEqual(
            public_info.products["candies"][0], self.shop.products["candies"][0]
        )
        self.assertNotEqual(
            public_info.products["candies"][1], self.shop.products["candies"][1]
        )

        self.assertEqual(public_info.products["candies"][0].name, "Reese's cups")
        self.assertEqual(
            public_info.products["candies"][0].brand, "The Hershey Company"
        )

        self.assertEqual(public_info.products["candies"][1].name, "Snickers")
        self.assertEqual(public_info.products["candies"][1].brand, "Mars, Incorporated")

    def test_map__use_deepcopy_false(self):
        public_info_deep = mapper.to(ShopPublicInfo).map(self.shop, use_deepcopy=False)
        public_info = mapper.to(ShopPublicInfo).map(self.shop)

        self.assertIsNot(public_info.products, self.shop.products)
        self.assertEqual(
            public_info.products["magazines"], self.shop.products["magazines"]
        )
        self.assertNotEqual(
            public_info.products["magazines"], id(self.shop.products["magazines"])
        )

        self.assertIs(public_info_deep.products, self.shop.products)
        self.assertEqual(
            id(public_info_deep.products["magazines"]),
            id(self.shop.products["magazines"]),
        )
