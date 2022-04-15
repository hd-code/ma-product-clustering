from src import akeneo

ATTR_GROUP_FAULTY = "faulty"


t = akeneo.AttributeType
TYPES_NUMERICAL = [t.DATE, t.METRIC, t.NUMBER, t.PRICE]
TYPES_CATEGORICAL = [t.BOOL, t.SELECT_SINGLE, t.REFERENCE_SINGLE]
TYPES_MULTI = [t.SELECT_MULTI, t.REFERENCE_MULTI]
TYPES_TEXT = [t.TEXT]
TYPES_TEXTAREA = [t.TEXTAREA]


def map_to_attribute_kind(attr_type: akeneo.AttributeType) -> str:
    if attr_type in TYPES_NUMERICAL:
        return "numerical"
    if attr_type in TYPES_CATEGORICAL:
        return "categorical"
    if attr_type in TYPES_MULTI:
        return "multi-categorical"
    if attr_type in TYPES_TEXT:
        return "string"
    return "other"
