import unittest

import requests

from src import config

from .. import util
from .route import Route

client = None


def client_created():
    try:
        host = config.env["AKENEO_HOST"]
        if requests.get(f"{host}/api/rest/v1").ok:
            global client
            client = util.create_client_from_env()
            return True
        return False
    except:
        return False


@unittest.skipUnless(client_created(), "tests need a working Akeneo PIM instance")
class Test_ClientImpl(unittest.TestCase):
    def setUp(self) -> None:
        global client
        self.client = client

    def test_get_routes(self):
        routes = self.client.get_routes()

        self.assertEqual(len(routes), 63)
        self.assertIsInstance(routes[0], Route)

    def test_request_get(self):
        res = self.client.request("pim_api_measurement_family_get")

        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], dict)

    def test_request_get_missing_path_var(self):
        with self.assertRaises(AssertionError):
            self.client.request("pim_api_locale_get")

        with self.assertRaises(AssertionError):
            self.client.request("pim_api_locale_get", path_vars={"unknown": 42})

    def test_request_get_list(self):
        res = self.client.request("pim_api_locale_list")

        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], dict)

    def test_request_get_list_with_params(self):
        params = {"search": '{"enabled":[{"operator":"=","value":true}]}'}
        res = self.client.request("pim_api_locale_list", params=params)

        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], dict)

    def test_request_post_get_delete(self):
        prod_id = "test_product_from_post"

        res = self.client.request(
            "pim_api_product_create", body={"identifier": prod_id}
        )

        self.assertEqual(res["status"], 201)

        self.client.request("pim_api_product_delete", path_vars={"code": prod_id})

    def test_request_post_invalid_body(self):
        res = self.client.request("pim_api_category_create", body={"unknown_key": 42})

        self.assertEqual(res["code"], 422)
        self.assertEqual(
            res["message"],
            'Property "unknown_key" does not exist. Check the expected format on the API documentation.',
        )

    def test_request_patch_get_delete(self):
        prod_id = "test_product_from_patch"

        res = self.client.request(
            "pim_api_product_partial_update",
            path_vars={"code": prod_id},
            body={"enabled": True},
        )
        self.assertEqual(res["status"], 201)

        prod = self.client.request("pim_api_product_get", path_vars={"code": prod_id})
        self.assertEqual(prod["enabled"], True)

        res = self.client.request(
            "pim_api_product_partial_update",
            path_vars={"code": prod_id},
            body={"enabled": False},
        )
        self.assertEqual(res["status"], 204)

        prod = self.client.request("pim_api_product_get", path_vars={"code": prod_id})
        self.assertEqual(prod["enabled"], False)

        self.client.request("pim_api_product_delete", path_vars={"code": prod_id})

    def test_request_patch_list(self):
        with self.assertRaises(AssertionError):
            self.client.request("pim_api_category_partial_update_list")
