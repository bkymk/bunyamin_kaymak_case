import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.screenshot import take_screenshot
import os
from datetime import datetime


def pytest_addoption(parser):
    """Add command line options for browser selection"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome or firefox"
    )


@pytest.fixture(scope="function")
def driver(request):
    """Setup and teardown browser driver"""
    browser = request.config.getoption("--browser").lower()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
        driver.maximize_window()
    else:
        raise ValueError(f"Browser {browser} is not supported")

    driver.implicitly_wait(10)

    yield driver

    # Teardown
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            take_screenshot(driver, item.name)