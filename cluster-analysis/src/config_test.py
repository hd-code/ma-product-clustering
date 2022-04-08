import os
import unittest
import uuid

from .config import dir_data, load_or_create


class Test_Config(unittest.TestCase):
    def setUp(self) -> None:
        self.file = dir_data / uuid.uuid1().hex

    def tearDown(self) -> None:
        if self.file.exists():
            os.remove(self.file)

    def test_load_or_create(self):
        data = {
            "name": "John Doe",
            "age": 25,
        }
        want = data.copy()

        got = None
        create_called = False

        def create_user():
            nonlocal create_called
            create_called = True
            return data.copy()

        with self.subTest("create when file does not exist"):
            got = load_or_create(self.file, create_user)
            self.assertEqual(want, got)
            self.assertEqual(True, create_called)

        with self.subTest("load from file when exist"):
            got = None
            create_called = False

            got = load_or_create(self.file, create_user)
            self.assertEqual(want, got)
            self.assertEqual(False, create_called)
