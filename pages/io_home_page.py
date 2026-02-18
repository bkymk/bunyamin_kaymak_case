from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://insiderone.com/"

    TOP_MENU = (By.CSS_SELECTOR, "header .header-top-menu")
    TOP_ACTION = (By.CSS_SELECTOR, "header .header-top-action")

    HEADER_LOGO = (By.CSS_SELECTOR, "header .header-logo")
    HEADER_MENU = (By.CSS_SELECTOR, "header .header-menu-list")
    HEADER_ACTION = (By.CSS_SELECTOR, "header .header-menu-action")

    COOKIE_ACCEPT = (By.ID, "wt-cli-accept-all-btn")

    def open_home_page(self):
        """Open Insider Home Page and wait to load"""
        self.open_url(self.URL)
        self.wait_for_page_load()

    def accept_cookies(self):
        """Accept cookies if banner appears"""
        try:
            if self.is_element_visible(self.COOKIE_ACCEPT, timeout=5):
                self.click_element(self.COOKIE_ACCEPT)
        except:
            pass  # Cookie banner not present

    def is_logo_visible(self):
        """Check if logo is visible"""
        return self.is_element_visible(self.HEADER_LOGO)

    def is_navigation_menu_visible(self):
        """Check if navigation menu is visible"""
        return self.is_element_visible(self.HEADER_MENU)

    def verify_main_blocks_loaded(self):
        """Verify all main blocks are loaded on home page"""
        blocks_status = {
            'logo': self.is_logo_visible(),
            'navigation': self.is_navigation_menu_visible()
        }
        return all(blocks_status.values())
