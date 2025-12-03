import asyncio
import random
from typing import List

from qoutes.cli import parse_args
from qoutes.core.config import Config, ConfigError
from qoutes.logger import setup_logger
from qoutes.models.Posts import Post
from qoutes.modules.authorization.login import Login
from qoutes.modules.parsing.parser import Parser
from qoutes.services.SeleniumServices import SeleniumManager
from qoutes.services.StorageService import Storage



async def choose_random_pages(pages_to_scrape: int, max_pages: int) -> List[int]:
    """
    Выбираем случайные номера страниц [1..max_pages] без повторов.
    """
    all_pages = list(range(1, max_pages + 1))
    return sorted(random.sample(all_pages, pages_to_scrape))

async def main():
    args = parse_args()

    try:
        config: Config = Config.load_config(args.config)
    except ConfigError as e:
        print(f"Config error: {e}")
        return

    logger = setup_logger(config.logger_path)

    if args.pages is not None:
        config.pages_to_scrape = args.pages
        logger.info(f"Pages to scrape: {config.pages_to_scrape}")
    if args.output is not None:
        config.output_file = args.output
        logger.info(f"Output file: {config.output_file}")


    logger.info("Script started.")
    pages = await choose_random_pages(config.pages_to_scrape, config.max_pages)
    logger.info(f"Chose {pages} pages to scrape.")


    storage = Storage(logger=logger)
    selenium_service = SeleniumManager(logger=logger)
    login = Login(selenium_service=selenium_service, logger=logger, config=config)

    if not await login.auth():
        logger.error("Login failed. Exiting.")

    parser = Parser(selenium_service=selenium_service, logger=logger, config=config, storage=storage)
    await parser.pars_posts(pages=pages)

    if args.author:
        author = args.author
        logger.info(f"Author to scrape: {author}")
        author_posts: List[Post] = await storage.find_by_author(author)
        if author_posts:
            logger.info(
                f"Found {len(author_posts)} quotes for author {author!r}"
            )
            print(f"Quotes by {author}:")
            print("-" * 40)
            for q in author_posts:
                print(q.text)
                print(f"  — {q.author}  [tags: {', '.join(q.tags)}]")
                print()
            try:
                await storage.save_author_quotes(
                    author_posts, config.author_output_file
                )
                logger.info(
                    f"Saved author quotes to {config.author_output_file}"
                )
            except Exception as e:
                logger.error(
                    f"Error saving author quotes to {config.author_output_file}: {e}"
                )
        else:
            logger.warning(f"No quotes found for author {author!r}.")



asyncio.run(main())