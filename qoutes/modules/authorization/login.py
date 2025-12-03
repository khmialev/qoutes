import traceback
from logging import Logger

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from qoutes.core.config import Config
from qoutes.services.SeleniumServices import SeleniumManager


class Login:
    def __init__(self, selenium_service: SeleniumManager, logger: Logger, config: Config):
        self.selenium = selenium_service
        self.logger = logger
        self.config = config

    async def check_success_login(self, driver:WebDriver):
        try:
            check = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/p/a").text
            if not check == "Logout":
                self.logger.warning("Login Failed")
                driver.close()
                return False
            self.logger.info("Login Success")
            return True
        except Exception:
            self.logger.warning(traceback.format_exc())
            driver.close()



    async def auth(self):
        url =  self.config.url_for_login
        username = self.config.username
        password = self.config.password
        max_retries= self.config.max_retries
        request_timeout=self.config.request_timeout
        driver = await self.selenium.login(url=url, username=username, key=password, max_retries=max_retries, request_timeout=request_timeout)
        if not driver:
            self.logger.warning("Login Failed, try latter")
            return False

        return await self.check_success_login(driver=driver)


