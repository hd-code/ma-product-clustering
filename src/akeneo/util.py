from akeneo.connector.client import AkeneoClient
from akeneo.connector.client_impl import AkeneoClientImpl
from akeneo.connector.connector import AkeneoConnector
from akeneo.connector.connector_impl import AkeneoConnectorImpl
from config import get_env


def create_client_from_env() -> AkeneoClient:
    env = get_env()
    return AkeneoClientImpl(
        env["AKENEO_HOST"],
        env["AKENEO_CLIENT_ID"],
        env["AKENEO_SECRET"],
        env["AKENEO_USERNAME"],
        env["AKENEO_PASSWORD"],
    )


def create_connector_from_env(preferred_channel: str = "ecommerce", locale: str = "en_US") -> AkeneoConnector:
    client = create_client_from_env()
    return AkeneoConnectorImpl(client, preferred_channel, locale)


def create_from_env(
    preferred_channel: str = "ecommerce",
    locale: str = "en_US"
) -> tuple[AkeneoConnector, AkeneoClient]:
    client = create_client_from_env()
    connector = AkeneoConnectorImpl(client, preferred_channel, locale)
    return connector, client
