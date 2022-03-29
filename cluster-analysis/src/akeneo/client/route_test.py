import unittest

from .route import Route


class Test_AkeneoRoute(unittest.TestCase):
    def setUp(self):
        self.routes = [
            Route(
                "pim_api_locale_list",
                "/api/rest/v1/locales",
                "GET",
            ),
            Route(
                "pim_api_attribute_option_get",
                "/api/rest/v1/attributes/{attributeCode}/options/{code}",
                "GET",
            ),
            Route(
                "pim_api_attribute_group_partial_update",
                "/api/rest/v1/attribute-groups/{code}",
                "PATCH",
            ),
        ]

    def test_path_vars(self):
        test_cases = [
            [],
            ["attributeCode", "code"],
            ["code"],
        ]
        for i in range(len(test_cases)):
            want = test_cases[i]
            with self.subTest(want):
                got = self.routes[i].path_vars
                self.assertListEqual(want, got)

    def test_make_path(self):
        test_cases = [
            (None, "/api/rest/v1/locales"),
            (
                {"attributeCode": "abc", "code": "cba"},
                "/api/rest/v1/attributes/abc/options/cba",
            ),
            ({"code": "abc"}, "/api/rest/v1/attribute-groups/abc"),
        ]
        for i in range(len(test_cases)):
            (input, want) = test_cases[i]
            with self.subTest(i):
                got = self.routes[i].make_path(input)
                self.assertEqual(want, got)
