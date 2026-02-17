import time

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OpenPositionsPage(BasePage):
    URL = "https://insiderone.com/careers/open-positions"
    DEPARTMENT_FILTER = (By.ID, "filter-by-department")
    JOB_LIST = (By.ID, "jobs-list")
    LOCATION_FILTER = (By.ID, "filter-by-location")
    JOB_LIST_LOC = (By.ID, "jobs-list")
    JOB_ITEM = (By.CSS_SELECTOR, ".position-list-item")  # Her job card'ın ortak class'ı

    def filter_by_location(self, location):
        """Filter jobs by location"""
        self.find_element(self.LOCATION_FILTER).click()
        location_dropdown = Select(self.find_element(self.LOCATION_FILTER))
        location_dropdown.select_by_visible_text(location)

        dropdown_toggle = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#career-position-filter .new_filter .dropdown-toggle"))
        )
        dropdown_toggle.click()

        # 2. İstenen lokasyon seçeneğini bekleyip tıklayın
        target_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(@class, 'dropdown-menu show')]//*[text()='{location}']"))
        )
        target_option.click()

    def wait_until_reload(self):
        # Waiting for DOM the refresh
        a = time.time()
        WebDriverWait(self.driver, 25).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "#filter-by-department option[selected]"),
                "Quality Assurance"
            )
        )
        # self.wait_for_page_load()
        # self.wait_for_visibility(self.JOB_LIST_LOC)
        # WebDriverWait(self.driver, 30).until(
        #     lambda d: d.execute_script("return document.readyState") == "complete"
        # )
        # WebDriverWait(self.driver, timeout=30).until(lambda x: self.wait_for_page_load())
        print("Reload Time", time.time() - a)

    def wait_until_qa_department_op(self):
        # Since reaching open positions page from Quality Assurance, should be waiting department filter to be presented as Quality Assurance
        a = time.time()
        WebDriverWait(self.driver, 30).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "#filter-by-department option[selected]"),
                "Quality Assurance"
            )
        )
        print("\nTime Passed to Filter Quality Assurance as Department", time.time() - a)

    def is_job_list_present(self):
        """Job listesinde en az 1 eleman var mı kontrol eder"""
        jobs = self.driver.find_elements(*self.JOB_ITEM)
        return len(jobs) > 0

    def get_job_count(self):
        """Listelenen toplam job sayısını döner"""
        return len(self.driver.find_elements(*self.JOB_ITEM))

    def wait_for_job_list_to_load(self):
        """
        En az 1 tane job card (.position-list-item) görünür olana kadar bekler.
        Spesifik metin beklenmez, sadece element yapısı beklenir.
        """
        a = time.time()
        # En az 1 tane job item görünür olana kadar bekle
        # WebDriverWait(self.driver, 30).until(lambda d: len(d.find_elements(*self.JOB_ITEM)) > 0)
        WebDriverWait(self.driver, 30).until(EC.visibility_of_any_elements_located(self.JOB_ITEM))
        print("Time Passed to Job List", time.time() - a)

        return True

    def filter_by_location(self, location):
        self.wait_and_click(self.LOCATION_FILTER)
        option = (By.XPATH, f"//li[text()='{location}']")
        self.wait_and_click(option)

    def filter_by_department(self, department):
        self.wait_and_click(self.DEPARTMENT_FILTER)
        option = (By.XPATH, f"//li[text()='{department}']")
        self.wait_and_click(option)

    def is_job_list_present(self):
        self.wait_for_visibility(self.JOB_LIST)
        return True
