import asyncio
import traceback
from logging import Logger

import chromedriver_autoinstaller
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from qoutes.core.config import ROOT_DIR_PATH


class SeleniumManager:
    def __init__(self, logger:Logger):
        self.ua = UserAgent()
        self.driver: WebDriver = None
        self.logger = logger


    async def __create_driver(self, driver_path:str):
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f"user-agent={self.ua.random}")


        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--no-sandbox')
        options.add_argument("--headless=new")

        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)

    async def get_driver(self):
        driver_path = chromedriver_autoinstaller.install()
        return await self.__create_driver(driver_path=driver_path)


    async def login(self, url:str, username: str, key: str, max_retries:int,request_timeout:int):
        try:
            await self.get_driver()
            driver = await self.get_page(url=url, max_retries=max_retries, request_timeout=request_timeout)
            if not driver:
                return False
            account = driver.find_element(By.ID, "username")
            account.send_keys(username)

            password = driver.find_element(By.ID, "password")
            password.send_keys(key)

            login_btn = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary")
            login_btn.click()
            await asyncio.sleep(2)
            driver.save_screenshot(ROOT_DIR_PATH /"files"/"success_login.png")
            return driver
        except Exception:
            self.logger.warning(traceback.format_exc())
            await self.close()


    async def get_page(self, url:str, max_retries:int, request_timeout:int):
        for trying in range(max_retries):
            try:
                self.driver.get(url=url)
                return self.driver
            except Exception:
                self.logger.warning(traceback.format_exc())
                await asyncio.sleep(request_timeout)
                continue
        return None

    async def close(self):
        self.driver.close()







