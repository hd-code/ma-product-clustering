import json
from os import scandir
from pathlib import Path

from ..client.client import Client, JsonBody
from .files import ATTRIBUTE_OPTIONS_DIR_NAME, FileInfo, Files


class Fetcher:
    def __init__(self, client: Client, data_dir: Path) -> None:
        self._client = client

        self._data_dir = data_dir
        self._opts_dir = data_dir / ATTRIBUTE_OPTIONS_DIR_NAME

        self._init_data_dir()
        self._fetch_files()

    def _init_data_dir(self) -> None:
        data_dir = self._data_dir

        if data_dir.exists():
            assert data_dir.is_dir(), data_dir.name + " is not a directory"
            assert not any(scandir(data_dir)), data_dir.name + " is not empty"
        else:
            data_dir.mkdir(parents=True)

        self._opts_dir.mkdir(parents=True, exist_ok=True)

    def _fetch_files(self) -> None:
        for filedata in Files:
            self._fetch_file(filedata.value)

    def _fetch_file(self, filedata: FileInfo) -> None:
        data = self._client.request(filedata.route_id)
        self._save_to_file(data, self._data_dir / filedata.filename)

        if filedata == Files.ATTRIBUTES.value:
            self._fetch_attributes_options(data)

    def _fetch_attributes_options(self, attributes: JsonBody) -> None:
        for attribute in attributes:
            if attribute["type"] in [
                "pim_catalog_simpleselect",
                "pim_catalog_multiselect",
            ]:
                code = attribute["code"]
                options = self._client.request(
                    "pim_api_attribute_option_list", {"attributeCode": code}
                )
                self._save_to_file(options, self._opts_dir / f"{code}.json")

    def _save_to_file(self, data: JsonBody, filepath: Path):
        filehandle = open(filepath, "w")
        json.dump(data, filehandle)
