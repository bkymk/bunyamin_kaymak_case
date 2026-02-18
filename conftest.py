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
    """Add command line options for browser selection and headless mode"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome or firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode (no browser window)"
    )


@pytest.fixture(scope="function")
def driver(request):
    """Setup and teardown browser driver"""
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # --- STABİLİTE İÇİN GEREKLİ ARGÜMANLAR ---
        options.add_argument("--no-sandbox")  # İşletim sistemi güvenlik duvarı engellemelerini aşar
        options.add_argument("--disable-dev-shm-usage")  # RAM şişmesini engeller
        options.add_argument("--disable-gpu")  # GPU ivmelenmesinden kaynaklı çökmeleri önler
        options.add_argument("--window-size=1920,1080")  # Headless modda ekran çözünürlüğü
        options.add_argument("--log-level=3")  # 0 = INFO, 1 = WARNING, 2 = ERROR, 3 = FATAL
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # --- HEADLESS MOD ---
        if headless:
            options.add_argument("--headless=new")  # Yeni headless modu (Chrome 109+)
            print("🚀 TEST HEADLESS MODDA ÇALIŞIYOR (Tarayıcı penceresi görünmeyecek)")
        else:
            print("🚀 TEST NORMAL MODDA ÇALIŞIYOR (Tarayıcı penceresi görünecek)")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()

        # --- HEADLESS MOD (Firefox) ---
        if headless:
            options.add_argument("--headless")
            print("\n🚀 TEST HEADLESS MODDA ÇALIŞIYOR (Firefox)\n")
        else:
            print("\n🚀 TEST NORMAL MODDA ÇALIŞIYOR (Firefox)\n")

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