import json
from dataclasses import asdict
from logging import Logger
from typing import List

from qoutes.models.Posts import Post


class Storage:
    def __init__(self,logger:Logger):
        self.posts:List[Post] = []
        self.logger = logger

    async def add_post(self, post: Post):
        self.posts.append(post)

    async def save_posts(self,path:str):
        with open(path,'w', encoding='utf-8') as f:
            posts_dict = [asdict(p) for p in self.posts]
            json.dump(posts_dict, f, ensure_ascii=False, indent=3)
            self.logger.info(f"Successfully saved posts to {path}")

    async def find_by_author(self, author_name: str) -> List[Post]:
        author_name_norm = author_name.strip().lower()
        return [
            post for post in self.posts
            if post.author.strip().lower() == author_name_norm
        ]

    @staticmethod
    async def save_author_quotes(posts: List[Post], path: str) -> None:
        data = {
            "author": posts[0].author if posts else None,
            "count": len(posts),
            "posts": [asdict(post) for post in posts],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)



