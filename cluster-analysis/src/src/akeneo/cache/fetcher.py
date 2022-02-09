import json
from dataclasses import dataclass
from os import scandir
from pathlib import Path

from ..client.client import Client, JsonBody


@dataclass
class _CacheFileData:
    filename: str
    route_id: str
    is_list: bool = True


class Fetcher:
    def __init__(self, client: Client, data_dir: Path) -> None:
        self._data_dir = data_dir
        self._client = client

        self._init_data_dir()
        self._fetch_files()

    def _init_data_dir(self) -> None:
        data_dir = self._data_dir

        if data_dir.exists():
            assert data_dir.is_dir(), data_dir.name + " is not a directory"
            assert not any(scandir(data_dir)), data_dir.name + " is not empty"
        else:
            data_dir.mkdir(parents=True)

    _files = [
        _CacheFileData("attributes.json", "pim_api_attribute_list"),
        _CacheFileData("categories.json", "pim_api_category_list"),
        _CacheFileData("channels.json", "pim_api_channel_list"),
        _CacheFileData("currencies.json", "pim_api_currency_list"),
        _CacheFileData("families.json", "pim_api_family_list"),
        _CacheFileData("products.json", "pim_api_product_list"),
        _CacheFileData("measurements.json", "pim_api_measurement_family_get", False),
    ]

    def _fetch_files(self) -> None:
        for filedata in self._files:
            self._fetch_file(filedata)

    def _fetch_file(self, filedata: _CacheFileData) -> None:
        if filedata.is_list:
            data = self._client.get_list(filedata.route_id)
        else:
            data = self._client.get(filedata.route_id)
        filehandle = open(self._data_dir / filedata.filename, "w")
        json.dump(data, filehandle)

        if filedata.filename == "attributes.json":
            self._fetch_attributes_options(data)

    def _fetch_attributes_options(self, attributes: JsonBody) -> None:
        opts_dir = self._data_dir / "attribute-options"
        opts_dir.mkdir()

        for attribute in attributes:
            if attribute["type"] in [
                "pim_catalog_simpleselect",
                "pim_catalog_multiselect",
            ]:
                code = attribute["code"]
                options = self._client.get_list(
                    "pim_api_attribute_option_list", {"attributeCode": code}
                )
                filehandle = open(opts_dir / f"{code}.json", "w")
                json.dump(options, filehandle)
