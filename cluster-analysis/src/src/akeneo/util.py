from src.akeneo.cache.cache import Cache
from src.akeneo.cache.fetcher import Fetcher
from src.akeneo.client.client import Client
from src.akeneo.client.client_impl import ClientImpl
from src.config import dir_data, env


def create_client_from_env() -> Client:
    """Creates an Akeneo REST Client using the config from .env file
    
    .env values
    -----------
    AKENEO_HOST:        base url of Akeneo PIM instance
    AKENEO_CLIENT_ID:   client_id of api connection
    AKENEO_SECRET:      secret for of connection
    AKENEO_USERNAME:    username of api connection
    AKENEO_PASSWORD:    password of api connection
    """
    return ClientImpl(
        env["AKENEO_HOST"],
        env["AKENEO_CLIENT_ID"],
        env["AKENEO_SECRET"],
        env["AKENEO_USERNAME"],
        env["AKENEO_PASSWORD"],
    )


def fetch_from_client_from_env() -> None:
    """Fetches all important data from Akeneo PIM using the config from .env
    
    .env values
    -----------
    (all from `create_client_from_env`)
    AKENEO_CACHE_DIR:   name of the directory the data should be put in,
                        is automatically put under the `data` directory
    """
    client = create_client_from_env()
    data_dir = dir_data / env["AKENEO_CACHE_DIR"]
    Fetcher(client, data_dir)


def load_cache_from_env() -> Cache:
    """Creates a `Cache` which loads and parses the previously fetched data

    The data has to be fetched from the Akeneo PIM Api first.
    E.g. use `fetch_from_client_from_env` to do so
    
    .env values
    -----------
    AKENEO_CACHE_DIR:   name of the directory the data is located in,
                        looks for the directory under the `data` directory
    AKENEO_CHANNEL:     default channel of scopable values
    AKENEO_CURRENCY:    default currency for prices
    AKENEO_LOCALE:      default locale for any localizeable values
    """
    data_dir = dir_data / env["AKENEO_CACHE_DIR"]
    channel = env["AKENEO_CHANNEL"]
    currency = env["AKENEO_CURRENCY"]
    locale = env["AKENEO_LOCALE"]
    Cache(data_dir, locale, currency, channel)
