import logging
import traceback
from logging import Logger

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from qoutes.core.config import Config
from qoutes.models.Posts import Post
from qoutes.services.SeleniumServices import SeleniumManager
from qoutes.services.StorageService import Storage


class Parser:
    def __init__(
        self,
        config: Config,
        selenium_service: SeleniumManager,
        logger: Logger,
        storage: Storage,
    ):
        self.selenium = selenium_service
        self.storage = storage
        self.config = config
        self.logger = logger

    async def check_next_page(self, page_data: WebDriver):
        try:
            next_page = page_data.find_element(By.CLASS_NAME, "next").text
            if not next_page:
                return False
            return True
        except NoSuchElementException:
            self.logger.info("Last page")
            return False
        except Exception:
            logging.warning(traceback.format_exc())
            return False

    async def pars_posts(self, pages):
        url = self.config.url_for_page
        count_pages = 0
        count_posts = 0
        for page in pages:
            url_for_pars = f"{url}/{page}"
            max_retries = self.config.max_retries
            request_timeout = self.config.request_timeout

            page_data = await self.selenium.get_page(
                url=url_for_pars,
                max_retries=max_retries,
                request_timeout=request_timeout,
            )
            if not await self.check_next_page(page_data):
                break
            if not page_data:
                self.logger.warning(f"No data found for page: {page}, trying next page")
                continue
            try:
                table = page_data.find_element(By.XPATH, "/html/body/div/div[2]/div[1]")
                posts = table.find_elements(By.CLASS_NAME, "quote")
                for post in posts:
                    post_text = post.find_element(By.CLASS_NAME, "text").text
                    post_author = post.find_element(By.CLASS_NAME, "author").text
                    tags_list = [
                        i.text
                        for i in post.find_element(By.CLASS_NAME, "tags").find_elements(
                            By.CLASS_NAME, "tag"
                        )
                    ]
                    post_obj = Post(text=post_text, author=post_author, tags=tags_list)
                    await self.storage.add_post(post=post_obj)
                    self.logger.info(f"Successfully scraped post: {post_obj}")
                    count_posts += 1
            except Exception:
                self.logger.warning(traceback.format_exc())
                continue
            self.logger.info(f"Successfully scraped page: {page}")
            count_pages += 1

        await self.storage.save_posts(path=self.config.output_file)
        await self.selenium.close()
        self.logger.info(
            f"Successfully scrapped {count_pages} - pages, {count_posts} - posts"
        )
