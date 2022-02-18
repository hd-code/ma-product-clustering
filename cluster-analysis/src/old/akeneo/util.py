from akeneo.client.client import Client
from akeneo.client.client_impl import ClientImpl
from akeneo.connector.connector import Connector
from akeneo.connector.connector_impl import ConnectorImpl
from config import dir_data, env


def create_client_from_env() -> Client:
    return ClientImpl(
        env["AKENEO_HOST"],
        env["AKENEO_CLIENT_ID"],
        env["AKENEO_SECRET"],
        env["AKENEO_USERNAME"],
        env["AKENEO_PASSWORD"],
    )


def create_from_env() -> Connector:
    client = create_client_from_env()

    locale = env.get("AKENEO_LOCALE", "en_US")
    currency = env.get("AKENEO_CURRENCY", "USD")
    channel = env.get("AKENEO_CHANNEL", "ecommerce")

    cache_filepath = env.get("AKENEO_CACHE_FILE", "")
    cache_file = None if cache_filepath == "" else dir_data / cache_filepath

    return ConnectorImpl(client, locale, currency, channel, cache_file)
