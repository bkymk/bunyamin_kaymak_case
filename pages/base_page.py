from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base Page Object Model class with common methods"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open_url(self, url):
        """Navigate to URL"""
        self.driver.get(url)

    def wait_for_page_load(self, timeout: int = 30):
        """Wait for Page to load"""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def find_element(self, locator, timeout=15):
        """Find element with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator, timeout=15):
        """Find multiple elements with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator, timeout=15):
        """Click element with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def scroll_to_element(self, element):
        """Scroll to element"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def is_element_visible(self, locator, timeout=15):
        """Check if element is visible"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_text(self, locator, timeout=15):
        """Get text from element"""
        element = self.find_element(locator, timeout)
        return element.text

    def wait_for_url_contains(self, url_part, timeout=15):
        """Wait for URL to contain specific string"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.url_contains(url_part))

    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url

    def switch_to_new_window(self):
        """Switch to newly opened window"""
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
