from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from src.akeneo.models.attribute_option import AttributeOption

from .util import CodeAndLabel


class AttributeType(Enum):
    ID = "pim_catalog_identifier"
    TEXT = "pim_catalog_text"
    TEXTAREA = "pim_catalog_textarea"
    SELECT_SINGLE = "pim_catalog_simpleselect"
    SELECT_MULTI = "pim_catalog_multiselect"
    BOOL = "pim_catalog_boolean"
    DATE = "pim_catalog_date"
    NUMBER = "pim_catalog_number"
    METRIC = "pim_catalog_metric"
    PRICE = "pim_catalog_price_collection"
    IMAGE = "pim_catalog_image"
    FILE = "pim_catalog_file"
    REFERENCE_SINGLE = "pim_reference_data_simpleselect"
    REFERENCE_MULTI = "pim_reference_data_multiselect"


@dataclass
class Attribute(CodeAndLabel):
    type: AttributeType
    localizable: bool
    scopable: bool
    unique: bool

    # group
    group: str
    group_labels: dict[str, str]
    sort_order: int

    # constraints – depending on type
    allowed_extensions: list[str]
    auto_option_sorting: Optional[bool]
    available_locales: list[str]
    date_max: Optional[datetime]
    date_min: Optional[datetime]
    decimals_allowed: Optional[bool]
    default_metric_unit: Optional[str]
    default_value: Optional[bool]
    max_characters: Optional[int]
    max_file_size: Optional[int]
    metric_family: Optional[str]
    minimum_input_length: Optional[int]
    negative_allowed: Optional[bool]
    number_min: Optional[float]
    number_max: Optional[float]
    reference_data_name: Optional[str]
    validation_rule: Optional[str]
    validation_regexp: Optional[str]
    wysiwyg_enabled: Optional[bool]

    # useable_as_grid_filter: Optional[bool]

    def get_group_label(self, locale: str) -> str:
        return self.group_labels.get(locale, f"[{self.code}]")

    @property
    def options(self) -> list[AttributeOption]:
        return self._options if hasattr(self, "_options") else []

    @options.setter
    def options(self, options: list[AttributeOption]):
        self._options = options

    def get_option(self, option_code: str) -> AttributeOption | None:
        if not hasattr(self, "_options"):
            return None
        for opt in self._options:
            if opt.code == option_code:
                return opt
        return None

    @staticmethod
    def to_dict(attributes: list[Attribute]) -> dict[str, Attribute]:
        result = {}
        for attribute in attributes:
            result[attribute.code] = attribute
        return result
