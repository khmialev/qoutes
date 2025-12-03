from dataclasses import dataclass


@dataclass
class Post:
    text: str
    author: str
    tags: list[str]