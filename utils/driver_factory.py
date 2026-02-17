from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class DriverFactory:
    """Factory class for creating WebDriver instances"""

    @staticmethod
    def get_driver(browser_name="chrome"):
        """
        Create and return WebDriver instance

        Args:
            browser_name: Name of the browser (chrome/firefox)

        Returns:
            WebDriver instance
        """
        if browser_name.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
        elif browser_name.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
            driver.maximize_window()
        else:
            raise ValueError(f"Browser {browser_name} is not supported")

        driver.implicitly_wait(10)
        return driver