import unittest
import unittest.mock as mock

from akeneo import models
from akeneo.cache.cache_base import CacheBase
from akeneo.client.client import Client


class ClientMock(Client, mock.Mock):
    pass


class Test_CacheBase(unittest.TestCase):
    def setUp(self) -> None:
        self.client_mock: ClientMock = mock.Mock(Client)
        self.cache_base = CacheBase(self.client_mock)

    def test_currencies(self):
        want = [
            models.Currency("EUR", True),
            models.Currency("USD", True),
            models.Currency("GBP", False),
        ]
        self.client_mock.get_list.return_value = [c.__dict__ for c in want]

        with self.subTest("first call to api"):
            got = self.cache_base.currencies

            self.assertListEqual(got, want)
            self.client_mock.get_list.assert_called_once()

        with self.subTest("second call from cache"):
            got = self.cache_base.currencies

            self.assertListEqual(got, want)
            self.client_mock.get_list.assert_called_once()

    def test_locales(self):
        want = [
            models.Locale("en_US", True),
            models.Locale("de_DE", True),
            models.Locale("fr_FR", False),
        ]
        self.client_mock.get_list.return_value = [c.__dict__ for c in want]

        with self.subTest("first call to api"):
            got = self.cache_base.locales

            self.assertListEqual(got, want)
            self.client_mock.get_list.assert_called_once()

        with self.subTest("second call from cache"):
            got = self.cache_base.locales

            self.assertListEqual(got, want)
            self.client_mock.get_list.assert_called_once()
