from .connector import Client, Connector
from .connector.client_impl import ClientImpl
from .connector.connector_impl import ConnectorImpl
from config import env


def create_client_from_env() -> Client:
    return ClientImpl(
        env["AKENEO_HOST"],
        env["AKENEO_CLIENT_ID"],
        env["AKENEO_SECRET"],
        env["AKENEO_USERNAME"],
        env["AKENEO_PASSWORD"],
    )


def create_from_env(
    preferred_channel: str = "ecommerce",
    locale: str = "en_US"
) -> tuple[Connector, Client]:
    client = create_client_from_env()
    connector = ConnectorImpl(client, preferred_channel, locale)
    return connector, client
