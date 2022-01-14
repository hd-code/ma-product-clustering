from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Optional

from akeneo.models.util import LocalStr


class AkeneoAttributeType(Enum):
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
class AkeneoAttribute:
    code: str
    type: AkeneoAttributeType
    labels: LocalStr

    localizable: bool
    scopable: bool
    unique: bool

    # group
    group: str
    group_labels: LocalStr
    sort_order: int

    # depending on type
    allowed_extensions: list[str]
    auto_option_sorting: Optional[bool]
    available_locales: list[str]
    date_max: Optional[date]
    date_min: Optional[date]
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


_map_attribute_to_type: dict[AkeneoAttributeType, type] = {
    AkeneoAttributeType.ID: str,
    AkeneoAttributeType.TEXT: str,
    AkeneoAttributeType.TEXTAREA: str,
    AkeneoAttributeType.SELECT_SINGLE: str,
    AkeneoAttributeType.SELECT_MULTI: list[str],
    AkeneoAttributeType.BOOL: bool,
    AkeneoAttributeType.DATE: datetime,
    AkeneoAttributeType.NUMBER: float,
    AkeneoAttributeType.METRIC: float,
    AkeneoAttributeType.PRICE: float,
    AkeneoAttributeType.IMAGE: str,
    AkeneoAttributeType.FILE: str,
    AkeneoAttributeType.REFERENCE_SINGLE: str,
    AkeneoAttributeType.REFERENCE_MULTI: list[str],
}
