from pathlib import Path

from ..config import dir_data, env
from .cache.cache import Cache
from .client.client import Client
from .client.client_impl import ClientImpl


def create_client_from_env(
    host: str = "",
    client_id: str = "",
    secret: str = "",
    username: str = "",
    password: str = "",
) -> Client:
    """Creates an Akeneo REST Client using the config from .env file

    All env values can be overwritten by using the corresponding parameters.

    .env values
    -----------
    AKENEO_HOST:        base url of Akeneo PIM instance
    AKENEO_CLIENT_ID:   client_id of api connection
    AKENEO_SECRET:      secret for of connection
    AKENEO_USERNAME:    username of api connection
    AKENEO_PASSWORD:    password of api connection
    """
    return ClientImpl(
        host if host else env.get("AKENEO_HOST", ""),
        client_id if client_id else env.get("AKENEO_CLIENT_ID", ""),
        secret if secret else env.get("AKENEO_SECRET", ""),
        username if username else env.get("AKENEO_USERNAME", ""),
        password if password else env.get("AKENEO_PASSWORD", ""),
    )


def create_cache_from_env(
    data_dir: Path = None,
    host: str = "",
    client_id: str = "",
    secret: str = "",
    username: str = "",
    password: str = "",
) -> Cache:
    """Creates the Akeneo Cache which can fetch and cache the data from the Api

    All env values can be overwritten by using the corresponding parameters.

    .env values
    -----------
    (all from `create_client_from_env`)
    AKENEO_CACHE_DIR:   name of the directory the data is located in,
                        looks for the directory under the `data` directory
    """
    try:
        client = create_client_from_env(host, client_id, secret, username, password)
    except:
        client = None
    return Cache(
        data_dir if data_dir else dir_data / env.get("AKENEO_CACHE_DIR", ""),
        client,
    )
