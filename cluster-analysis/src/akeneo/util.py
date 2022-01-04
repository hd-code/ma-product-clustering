from typing import TypeVar


T = TypeVar('T')


def clean_response(obj: T) -> T:
    if isinstance(obj, list):
        result = []
        for entry in obj:
            entry_ = clean_response(entry)
            if _is_allowed_value(entry_):
                result.append(entry_)
        return result

    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            if not _is_allowed_key(key):
                continue
            value_ = clean_response(value)
            if _is_allowed_value(value_):
                result[key] = value_
        return result

    return obj


def _is_allowed_key(key: T) -> bool:
    return not isinstance(key, str) or key[0] != "_"


def _is_allowed_value(value: T) -> bool:
    return value not in [None, [], {}]
