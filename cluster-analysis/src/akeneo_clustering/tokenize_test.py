import unittest

from .tokenize import tokenize


class Test_Tokenize(unittest.TestCase):
    def test_tokenize(self):
        test_cases = [
            (
                "Samsung Galaxy S21 128GB Black",
                "en_US",
                {"samsung", "galaxi", "s21", "128gb", "black"},
            ),
            (
                "Samsung Galaxy S21 128GB Black",
                "en_GB",
                {"samsung", "galaxi", "s21", "128gb", "black"},
            ),
            (
                "Samsung Galaxy S21 128GB Black",
                "de_DE",
                {"samsung", "galaxy", "s21", "128gb", "black"},
            ),
            (
                "Mobiparts 104889 Handy-Schutzhülle 15,8 cm (6.2 Zoll) Cover Schwarz",
                "de_DE",
                {
                    "mobipart",
                    "104889",
                    "handy-schutzhull",
                    "15,8",
                    "cm",
                    "6.2",
                    "zoll",
                    "cov",
                    "schwarz",
                },
            ),
            (
                "Mobiparts 104890 a SMartphone-Cover 15.8 cm",
                "en_GB",
                {"mobipart", "104890", "a", "smartphone-cov", "15.8", "cm"},
            ),
        ]
        for text, locale, want in test_cases:
            with self.subTest(f"{text} – {locale}"):
                got = tokenize(text, locale)
                self.assertSetEqual(want, got)
