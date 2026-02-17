from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class OpenPositionsPage(BasePage):

    LOCATION_FILTER = (By.ID, "select2-filter-by-location-container")
    DEPARTMENT_FILTER = (By.ID, "select2-filter-by-department-container")
    JOB_LIST = (By.ID, "jobs-list")

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