from datetime import datetime
from typing import Any, Callable

from src import akeneo

from .datapoint import KEY_CATEGORIES, KEY_FAMILY, KEY_ID, Datapoint, DataValue

MeasureDict = dict[str, akeneo.MeasurementFamily]


def parse_product(
    product: akeneo.Product,
    attributes: dict[str, akeneo.Attribute],
    measures: MeasureDict,
    channel: str,
    locale: str,
    currency: str,
) -> tuple[Datapoint, dict[str, float]]:
    result = Datapoint(
        {
            KEY_ID: product.identifier,
            KEY_FAMILY: product.family if product.family else "",
            KEY_CATEGORIES: product.categories,  # type: ignore
        }
    )
    numericals: dict[str, float] = {}

    for attr_code, values in product.values.items():
        attribute = attributes[attr_code]
        parsed_value = _parse_product_values(
            values,
            attribute,
            measures,
            channel,
            locale,
            currency,
        )
        if type(parsed_value) == float:
            numericals[attr_code] = parsed_value
        result[attr_code] = parsed_value

    return result, numericals


def _parse_product_values(
    values: list[akeneo.ProductValue],
    attribute: akeneo.Attribute,
    measures: MeasureDict,
    channel: str,
    locale: str,
    currency: str,
) -> DataValue:
    value = _select_product_value(values, channel, locale)
    return _parse_product_value(value, attribute, measures, currency)


def _select_product_value(
    values: list[akeneo.ProductValue],
    channel: str,
    locale: str,
) -> akeneo.ProductValue:
    index = 0
    for i in range(1, len(values)):
        value = values[i]
        if value.locale in [None, locale] and value.scope in [None, channel]:
            index = i
    return values[index]


# ------------------------------------------------------------------------------


def _parse_product_value(
    value: akeneo.ProductValue,
    attribute: akeneo.Attribute,
    measures: MeasureDict,
    currency: str,
) -> DataValue:
    return _parse_attr_type[attribute.type](value.data, attribute, measures, currency)


def _parse_metric(
    data: Any,
    attribute: akeneo.Attribute,
    measures: MeasureDict,
    *_,
) -> DataValue:
    amount, unit = [float(data["amount"]), data["unit"]]
    default_unit = attribute.default_metric_unit

    measure = measures[attribute.metric_family]  # type: ignore
    target_unit = default_unit if default_unit else measure.standard_unit_code
    return measure.convert(amount, unit, target_unit)


def _parse_price(
    data: Any,
    _1: akeneo.Attribute,
    _2: MeasureDict,
    currency: str,
) -> DataValue:
    index = 0
    for i in range(1, len(data)):
        if data[i]["currency"] == currency:
            index = i
    return float(data[index]["amount"])


_parse_attr_type: dict[
    akeneo.AttributeType, Callable[[Any, akeneo.Attribute, MeasureDict, str], DataValue]
] = {
    akeneo.AttributeType.ID: lambda x, *_: str(x),
    akeneo.AttributeType.TEXT: lambda x, *_: str(x),
    akeneo.AttributeType.TEXTAREA: lambda x, *_: str(x),
    akeneo.AttributeType.SELECT_SINGLE: lambda x, *_: str(x),
    akeneo.AttributeType.SELECT_MULTI: lambda x, *_: set([str(y) for y in x]),
    akeneo.AttributeType.REFERENCE_SINGLE: lambda x, *_: str(x),
    akeneo.AttributeType.REFERENCE_MULTI: lambda x, *_: set([str(y) for y in x]),
    akeneo.AttributeType.BOOL: lambda x, *_: str(x),
    akeneo.AttributeType.DATE: lambda x, *_: datetime.fromisoformat(x).timestamp(),
    akeneo.AttributeType.NUMBER: lambda x, *_: float(x),
    akeneo.AttributeType.IMAGE: lambda x, *_: str(x),
    akeneo.AttributeType.FILE: lambda x, *_: str(x),
    akeneo.AttributeType.METRIC: _parse_metric,
    akeneo.AttributeType.PRICE: _parse_price,
}
