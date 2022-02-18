import unittest

from .measures import MeasurementConversion, MeasurementFamily, MeasurementUnit


class Test_MeasurementFamily(unittest.TestCase):
    def setUp(self):
        self.family = MeasurementFamily(
            "weight",
            "Weight",
            "gram",
            {
                "gram": MeasurementUnit(
                    "gram",
                    "Gram",
                    [
                        MeasurementConversion("mul", 1),
                    ],
                    "g",
                ),
                "kilogram": MeasurementUnit(
                    "kilogram",
                    "Kilogram",
                    [
                        MeasurementConversion("mul", 1000),
                    ],
                    "kg",
                ),
                "bettergram": MeasurementUnit(
                    "bettergram",
                    "Bettergram",
                    [
                        MeasurementConversion("sub", 42),
                    ],
                    "bg",
                ),
            },
        )

    def test_from_standard_unit(self):
        test_cases = [
            ("same unit", 23.5, "gram", 23.5),
            ("to kilogram", 1253, "kilogram", 1.253),
            ("to bettergram", 1253, "bettergram", 1295),
        ]
        for name, amount, target_unit, want in test_cases:
            with self.subTest(name):
                got = self.family.from_standard_unit(amount, target_unit)
                self.assertEqual(got, want)

    def test_to_standard_unit(self):
        test_cases = [
            ("same unit", 23.5, "gram", 23.5),
            ("from kilogram", 1.253, "kilogram", 1253),
            ("from bettergram", 1295, "bettergram", 1253),
        ]
        for name, amount, unit, want in test_cases:
            with self.subTest(name):
                got = self.family.to_standard_unit(amount, unit)
                self.assertEqual(got, want)

    def test_convert(self):
        test_cases = [
            ("stays gram", 23.5, "gram", "gram", 23.5),
            ("stays kilogram", 23.5, "kilogram", "kilogram", 23.5),
            ("gram to kilogram", 1253, "gram", "kilogram", 1.253),
            ("bettergram to gram", 1253, "bettergram", "gram", 1211),
            ("kilogram to bettergram", 3.5, "kilogram", "bettergram", 3542),
            ("bettergram to kilogram", 3.5, "bettergram", "kilogram", -0.0385),
        ]
        for name, amount, unit, target_unit, want in test_cases:
            with self.subTest(name):
                got = self.family.convert(amount, unit, target_unit)
                self.assertEqual(got, want)
