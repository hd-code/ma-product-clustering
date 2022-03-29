from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

from .util import CodeAndLabel

ConversionOperator = Literal["add", "sub", "mul", "div"]
_conversion_map: dict[ConversionOperator, Callable[[float, float], float]] = {
    "add": lambda x, y: x + y,
    "sub": lambda x, y: x - y,
    "mul": lambda x, y: x * y,
    "div": lambda x, y: x / y,
}
_conversion_map_reverse: dict[ConversionOperator, ConversionOperator] = {
    "add": "sub",
    "sub": "add",
    "mul": "div",
    "div": "mul",
}


@dataclass
class MeasurementConversion:
    operator: ConversionOperator
    value: float

    def convert(self, amount: float) -> float:
        return _conversion_map[self.operator](amount, self.value)

    def invert(self, amount: float) -> float:
        operator = _conversion_map_reverse[self.operator]
        return _conversion_map[operator](amount, self.value)


@dataclass
class MeasurementUnit(CodeAndLabel):
    # actually describes how to convert TO the standard unit
    convert_from_standard: list[MeasurementConversion]
    symbol: str

    def from_standard(self, amount: float) -> float:
        result = amount
        for conversion in reversed(self.convert_from_standard):
            result = conversion.invert(result)
        return result

    def to_standard(self, amount: float) -> float:
        result = amount
        for conversion in self.convert_from_standard:
            result = conversion.convert(result)
        return result


@dataclass
class MeasurementFamily(CodeAndLabel):
    standard_unit_code: str
    units: dict[str, MeasurementUnit]

    def convert(self, amount: float, unit: str, target_unit: str) -> float:
        if unit == target_unit:
            return amount
        std = self.to_standard_unit(amount, unit)
        return self.from_standard_unit(std, target_unit)

    def from_standard_unit(self, amount: float, target_unit: str) -> float:
        if target_unit == self.standard_unit_code:
            return amount
        try:
            return self.units[target_unit].from_standard(amount)
        except:
            raise ValueError(f"target unit {target_unit} not found")

    def to_standard_unit(self, amount: float, unit: str) -> float:
        if unit == self.standard_unit_code:
            return amount
        try:
            return self.units[unit].to_standard(amount)
        except:
            raise ValueError(f"unit {unit} not found")

    @staticmethod
    def to_dict(measures: list[MeasurementFamily]) -> dict[str, MeasurementFamily]:
        result = {}
        for measure in measures:
            result[measure.code] = measure
        return result
