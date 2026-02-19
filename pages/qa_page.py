from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class QAPage(BasePage):
    URL = "https://insiderone.com/careers/quality-assurance/"

    SEE_ALL_QA_JOBS = (By.CSS_SELECTOR, "#page-head a.btn-outline-secondary")

    def open_qa_page(self):
        self.open_url(self.URL)
        self.wait_for_page_load()

    def click_see_all_jobs(self):
        self.click_element(self.SEE_ALL_QA_JOBS)
