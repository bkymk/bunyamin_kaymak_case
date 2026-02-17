from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class QAPage(BasePage):

    URL = "https://insiderone.com/careers/quality-assurance/"

    SEE_ALL_QA_JOBS = (
        By.CSS_SELECTOR,
        "#page-head a[href*='open-positions'][href*='qualityassurance']"
    )

    def open_qa_page(self):
        self.open_url()
        self.wait_for_page_load()

    def click_see_all_jobs(self):
        self.wait_and_click(self.SEE_ALL_QA_JOBS)