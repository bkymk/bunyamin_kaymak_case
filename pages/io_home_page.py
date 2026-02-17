from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://insiderone.com/"

    TOP_MENU = (By.CSS_SELECTOR, "header .header-top-menu")
    TOP_ACTION = (By.CSS_SELECTOR, "header .header-top-action")

    HEADER_LOGO = (By.CSS_SELECTOR, "header .header-logo")
    HEADER_MENU = (By.CSS_SELECTOR, "header .header-menu-list")
    HEADER_ACTION = (By.CSS_SELECTOR, "header .header-menu-action")

    HERO_CONTENT = (By.CLASS_NAME, "homepage-hero-content")
    # FOOTER = (By.TAG_NAME, "footer")
    SECTIONS = (By.XPATH, "//main//section")

    def open_home_page(self):
        self.open_url()
        self.wait_for_page_load()

    def is_home_page_blocks_loaded(self):
        """
            Checks if all critical homepage blocks are visible and loaded.
        """
        # Header validation

        top_menu = self.is_element_visible(self.TOP_MENU)
        top_action = self.is_element_visible(self.TOP_MENU)

        header_logo = self.is_element_visible(self.HEADER_LOGO)
        header_menu = self.is_element_visible(self.HEADER_MENU)
        header_action = self.is_element_visible(self.HEADER_ACTION)

        hero_content = self.is_element_visible(self.HERO_CONTENT)
        # Content sections validation
        sections = self.driver.find_elements(*self.SECTIONS)
        if len(sections) > 3:
            sections_correct = True
        else:
            sections_correct = False
        is_blocks_loaded_correctly = [
            top_menu and top_action and header_logo and header_menu and header_action and hero_content and sections_correct]
        if all(is_blocks_loaded_correctly):
            return True
        else:
            print("\ntop_menu , top_action , header_logo , header_menu , header_action , hero_content , sections_correct")
            print(top_menu, top_action, header_logo, header_menu, header_action, hero_content, sections_correct)
            return False
