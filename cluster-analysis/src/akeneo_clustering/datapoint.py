import math
from typing import NewType, Union

DataValue = Union[float, str, set[str]]

KEY_ID = "__id__"
KEY_FAMILY = "__family__"
KEY_CATEGORIES = "__categories__"
KEYS = [KEY_ID, KEY_FAMILY, KEY_CATEGORIES]

Datapoint = NewType("Datapoint", dict[str, DataValue])


def dataset_from_records(records: list[dict]) -> list[Datapoint]:
    result: list[Datapoint] = []
    for record in records:
        values = {}
        for key, value in record.items():
            if key in KEYS:
                continue
            if type(value) == float and math.isnan(value):
                continue
            values[key] = value
        if len(values) > 0:
            result.append(Datapoint(values))
    return result
