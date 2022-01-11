from typing import Any
from akeneo.client import AkeneoClient


class AkeneoConnector:
    def __init__(self, client: AkeneoClient, locale: str = "en_US") -> None:
        self._client = client
        self._locale = locale

    def get_attributes(self) -> list[dict]:
        result = self._client.get_list("pim_api_attribute_list")
        [self._base_transform(entry) for entry in result]
        return result

    def get_categories(self) -> list[dict]:
        result = self._client.get_list("pim_api_category_list")
        [self._base_transform(entry) for entry in result]
        return result

    def get_families(self) -> list[dict]:
        result = self._client.get_list("pim_api_family_list")

        def cleanup(entry):
            del entry["attribute_as_label"]
            del entry["attribute_as_image"]
            del entry["attribute_requirements"]
            self._base_transform(entry)

        [cleanup(entry) for entry in result]
        return result

    def get_product_models(self) -> list[dict]:
        result = self._client.get_list("pim_api_product_model_list")
        [self._base_transform(entry) for entry in result]
        return result

    def get_products(self) -> list[dict]:
        result = self._client.get_list("pim_api_product_list")
        [self._base_transform(entry) for entry in result]
        return result

    def _base_transform(self, entry: dict[str, Any]):
        self._replace_labels(entry)

    def _replace_labels(self, entry: dict[str, dict[str, str]]):
        for key in entry:
            if isinstance(entry[key], dict) and key.find("labels") != -1:
                if self._locale in entry[key]:
                    entry[key] = entry[key][self._locale]
                else:
                    entry[key] = ""
