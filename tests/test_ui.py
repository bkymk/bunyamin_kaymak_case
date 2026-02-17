from pages.io_home_page import HomePage
from pages.qa_page import QAPage
from pages.open_positions_page import OpenPositionsPage


def test_insider_qa_flow(driver):

    home = HomePage(driver)
    qa = QAPage(driver)
    open_positions = OpenPositionsPage(driver)

    # 1 - Home page
    home.open_home_page()
    # URL validation
    assert home.current_url == "https://insiderone.com/", "Home Page URL Is Not Correct"
    # Title validation
    assert "Insider One" in home.driver.title , "Title is not correct"
    # Main Blocks Load validation
    assert home.is_home_page_blocks_loaded()

    # 2 - QA page
    qa.open_qa_page()
    assert qa.current_url == "https://insiderone.com/careers/quality-assurance/", "Home Page URL Is Not Correct"
    qa.click_see_all_jobs()
    #
    # # 3 - Filter
    # open_positions.filter_by_location("Istanbul, Turkey")
    # open_positions.filter_by_department("Quality Assurance")
    #
    # assert open_positions.is_job_list_present()