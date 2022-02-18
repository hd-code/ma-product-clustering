from dataclasses import dataclass
from enum import Enum
from typing import Type

from .. import models


@dataclass
class FileInfo:
    route_id: str
    filename: str
    model_cls: Type


class Files(Enum):
    ATTRIBUTE_GROUPS = FileInfo(
        "pim_api_attribute_group_list",
        "attribute-groups.json",
        models.AttributeGroup,
    )
    ATTRIBUTES = FileInfo("pim_api_attribute_list", "attributes.json", models.Attribute)
    CATEGORIES = FileInfo("pim_api_category_list", "categories.json", models.Category)
    CHANNELS = FileInfo("pim_api_channel_list", "channels.json", models.Channel)
    CURRENCIES = FileInfo("pim_api_currency_list", "currencies.json", models.Currency)
    FAMILIES = FileInfo("pim_api_family_list", "families.json", models.Family)
    LOCALES = FileInfo("pim_api_locale_list", "locales.json", models.Locale)
    MEASUREMENTS = FileInfo(
        "pim_api_measurement_family_get",
        "measurements.json",
        models.MeasurementFamily,
    )
    PRODUCTS = FileInfo("pim_api_product_list", "products.json", models.Product)
