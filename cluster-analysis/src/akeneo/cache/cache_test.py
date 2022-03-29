import unittest
from pathlib import Path

from src import config

from .cache import Cache

data_dir = Path()


def has_data_dir():
    try:
        dir = config.dir_data / config.env["AKENEO_CACHE_DIR"]
        if dir.exists():
            global data_dir
            data_dir = dir
            return True
        return False
    except:
        return False


@unittest.skipUnless(has_data_dir(), "tests need a populated data cache directory")
class Test_ClientImpl(unittest.TestCase):
    def setUp(self) -> None:
        self.cache = Cache(data_dir)

    def test_no_failures(self):
        properties = [
            "attribute_groups",
            "attributes",
            "categories",
            "channels",
            "currencies",
            "families",
            "locales",
            "measurements",
            "products",
        ]
        for property_name in properties:
            with self.subTest(property_name):
                got = self.cache.__getattribute__(property_name)
                self.assertIsInstance(got, list)
