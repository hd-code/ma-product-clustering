from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer


def tokenize(text: str, locale: str) -> set[str]:
    lang = _map_locale[locale.split("_")[0]]
    stemmer = SnowballStemmer(lang)
    words = RegexpTokenizer(r"\w\S*\w|\w").tokenize(text)
    tokens = [stemmer.stem(word) for word in words]
    return set(tokens)


_map_locale = {
    "en": "english",
    "de": "german",
    "fr": "french",
    "nl": "dutch",
}
