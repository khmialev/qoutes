import json
from dataclasses import dataclass
from typing import Any, Dict
from pathlib import Path


ROOT_DIR_PATH = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT_DIR_PATH / "config.json"

class ConfigError(Exception):
    pass


@dataclass
class Config:
    base_url: str
    url_for_login: str
    url_for_page:str
    username: str
    password: str

    pages_to_scrape: int
    max_pages:int
    request_timeout: int
    max_retries: int

    output_file: str
    author_output_file: str
    logger_path: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        required_fields = [
            "base_url",
            "url_for_login",
            "url_for_page",
            "username",
            "password",
            "pages_to_scrape",
            "max_pages",
            "request_timeout",
            "max_retries",
            "output_file",
            "author_output_file",
            "logger_path",
        ]

        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ConfigError(f"Missing config fields: {', '.join(missing)}")

        if data["pages_to_scrape"] <= 0:
            raise ConfigError("'pages_to_scrape' must be > 0")
        if data["max_pages"] < data["pages_to_scrape"]:
            raise ConfigError("'max_pages' must be >= 'pages_to_scrape'")
        if data["max_retries"] <= 0:
            raise ConfigError("'max_retries' must be > 0")

        return cls(
            base_url=data["base_url"],
            url_for_login=data["url_for_login"],
            url_for_page= data["url_for_page"],
            username=data["username"],
            password=data["password"],
            pages_to_scrape=int(data["pages_to_scrape"]),
            max_pages=int(data["max_pages"]),
            request_timeout=int(data["request_timeout"]),
            max_retries=int(data["max_retries"]),
            output_file=ROOT_DIR_PATH /"files"/ data["output_file"],
            author_output_file=ROOT_DIR_PATH /"files"/data["author_output_file"],
            logger_path=ROOT_DIR_PATH /"files"/ data["logger_path"],
        )

    @classmethod
    def load_config(cls, path: str = None) -> "Config":
        if path is None:
            path = CONFIG_PATH

        path = Path(path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise ConfigError(f"Config file not found: {path}")
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON in config file: {e}")

        return cls.from_dict(data)



