from pathlib import Path
import shutil

from src import akeneo, config


dir_cache: Path = config.dir_data / config.env["AKENEO_CACHE_DIR"]
shutil.rmtree(dir_cache, ignore_errors=True)
dir_cache.mkdir(parents=True, exist_ok=True)

akeneo.fetch_with_client_from_env()
