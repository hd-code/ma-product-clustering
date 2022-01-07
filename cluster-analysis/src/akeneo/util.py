from akeneo.client import AkeneoClient
from akeneo.client_impl import AkeneoClientImpl
from akeneo.connector import AkeneoConnector
from config import env


def create_client_from_env() -> AkeneoClient:
    return AkeneoClientImpl(
        env["AKENEO_HOST"],
        env["AKENEO_CLIENT_ID"],
        env["AKENEO_SECRET"],
        env["AKENEO_USERNAME"],
        env["AKENEO_PASSWORD"],
    )


def create_connector_from_env(locale: str = "en_US") -> AkeneoConnector:
    client = create_client_from_env()
    return AkeneoConnector(client, locale)
