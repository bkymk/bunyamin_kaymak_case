from typing import Tuple

from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

Locator = Tuple[str, str]


class BasePage:
    URL = ""
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    def open_url(self):
        self.driver.get(self.URL)

    def wait_for_page_load(self, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def wait_for_visibility(self, locator: Locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_and_click(self, locator: Locator, timeout: int = 10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def is_url_contains(self, text: str, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )

    def is_element_visible(self, locator: Locator, timeout: int = 10) -> bool:
        """
        Returns True if element becomes visible within timeout.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
