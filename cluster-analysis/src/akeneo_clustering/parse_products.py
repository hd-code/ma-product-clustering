from src import akeneo

from .datapoint import Datapoint
from .parse_product import parse_product


def parse_products(
    cache: akeneo.Cache,
    *_,
    product_family: str = None,
    attribute_types: list[akeneo.AttributeType] = None,
    remove_faulty_attributes: bool = True,
    channel: str = "default",
    locale: str = "en_US",
    currency: str = "USD",
) -> list[Datapoint]:
    attr_dict = akeneo.Attribute.to_dict(cache.attributes)
    meas_dict = akeneo.MeasurementFamily.to_dict(cache.measurements)

    result: list[Datapoint] = []
    min_max_values: dict[str, tuple[float, float]] = {}

    products = filter(
        lambda prod: product_family is None or prod.family == product_family,
        cache.products,
    )

    for product in products:
        prod, numericals = parse_product(
            product,
            attr_dict,
            attribute_types,
            remove_faulty_attributes,
            meas_dict,
            channel,
            locale,
            currency,
        )
        result.append(prod)
        for key, value in numericals.items():
            if key not in min_max_values:
                min_max_values[key] = (value, value)
            else:
                min_max_values[key] = (
                    min(min_max_values[key][0], value),
                    max(min_max_values[key][1], value),
                )

    for i in range(len(result)):
        for key, (min_value, max_value) in min_max_values.items():
            if key not in result[i]:
                continue

            diff = max_value - min_value
            if diff == 0:
                result[i][key] = 0.0
            else:
                value = result[i][key]  # type: ignore
                result[i][key] = (value - min_value) / diff

    return result
