import time

from pycparser.c_ast import Return
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

    def wait_until_qa_department_op(self):
        # Since reaching open positions page from Quality Assurance, should be waiting department filter to be presented as Quality Assurance
        a = time.time()
        if WebDriverWait(self.driver, 40).until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "#filter-by-department option[selected]"),
                    "Quality Assurance"
                )
        ):
            print("\nTime Passed to Filter Quality Assurance as Department", time.time() - a)
            return True
        else:
            return False

    def wait_for_job_list_to_load(self):
        """
        En az 1 tane job card (.position-list-item) görünür olana kadar bekler.
        Spesifik metin beklenmez, sadece element yapısı beklenir.
        """
        a = time.time()
        # En az 1 tane job item görünür olana kadar bekle
        # WebDriverWait(self.driver, 30).until(lambda d: len(d.find_elements(*self.JOB_ITEM)) > 0)
        WebDriverWait(self.driver, 40).until(EC.visibility_of_any_elements_located(self.JOB_ITEM))
        print("Time Passed to Job List", time.time() - a)

        return True

    def filter_by_location(self, location):
        location_dropdown = Select(self.find_element(self.LOCATION_FILTER))
        location_dropdown.select_by_visible_text(location)

    def filter_by_department(self, department):
        location_dropdown = Select(self.find_element(self.DEPARTMENT_FILTER))
        location_dropdown.select_by_visible_text(department)
