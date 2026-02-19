import os
import pytest
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.screenshot import take_screenshot

# HTML raporu özelleştirmeleri için
try:
    import pytest_html
except ImportError:
    pytest_html = None


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


def pytest_configure(config):
    """Rapor adını dinamik olarak belirler: dosya_adı_timestamp veya fulltest_timestamp"""
    report_dir = "reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Koşulan hedefleri analiz et (config.args)
    # Örn: pytest tests/test_io_ui.py -> args: ['tests/test_io_ui.py']
    if len(config.args) == 1 and config.args[0].endswith(".py"):
        # Tek bir test dosyası koşuluyorsa dosya adını al
        target_name = os.path.basename(config.args[0]).replace(".py", "")
    else:
        # Klasör koşuluyorsa veya birden fazla dosya varsa 'fulltest' de
        target_name = "fulltest"

    report_file = f"{target_name}_{timestamp}.html"
    config.option.htmlpath = os.path.join(report_dir, report_file)
    config.option.self_contained_html = True


@pytest.fixture(scope="function")
def driver(request):
    """Tarayıcı kurulum ve kapatma işlemleri"""
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
            print("TEST HEADLESS MODDA ÇALIŞIYOR (Tarayıcı penceresi görünmeyecek)")
        else:
            print("TEST NORMAL MODDA ÇALIŞIYOR (Tarayıcı penceresi görünecek)")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()

        # --- HEADLESS MOD (Firefox) ---
        if headless:
            options.add_argument("--headless")
            print("\nTEST HEADLESS MODDA ÇALIŞIYOR (Firefox)\n")
        else:
            print("\nTEST NORMAL MODDA ÇALIŞIYOR (Firefox)\n")

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
    """Hata anında screenshot alır ve HTML raporuna gömer"""
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            driver = item.funcargs.get("driver")
            if driver:
                # Screenshot al
                screenshot_path = take_screenshot(driver, item.name)
                if screenshot_path and os.path.exists(screenshot_path):
                    import base64
                    with open(screenshot_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode()

                    # HTML'e göm
                    html_content = f'<div><img src="data:image/png;base64,{encoded_string}" alt="screenshot" style="width:304px;height:228px;" ' \
                                   f'onclick="window.open(this.src)" align="right"/></div>'
                    extra.append(pytest_html.extras.html(html_content))
        report.extra = extra


def pytest_html_report_title(report):
    report.title = "QA Automation Assessment Report"