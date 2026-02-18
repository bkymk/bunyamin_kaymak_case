from pages.io_home_page import HomePage
from pages.qa_page import QAPage
from pages.open_positions_page import OpenPositionsPage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_qa_flow(driver):
    home = HomePage(driver)
    qa = QAPage(driver)
    open_positions = OpenPositionsPage(driver)

    # 1 - Home page
    home.open_home_page()
    home.accept_cookies()
    # URL validation
    assert home.get_current_url() == "https://insiderone.com/", "Home Page URL Is Not Correct"
    # Title validation
    assert "Insider One" in home.driver.title, "Title is not correct"
    # Main Blocks Load validation
    assert home.verify_main_blocks_loaded()

    # 2 - QA page
    qa.open_qa_page()
    # URL validation
    assert qa.get_current_url() == "https://insiderone.com/careers/quality-assurance/", "Home Page URL Is Not Correct"
    # clicking button
    qa.click_see_all_jobs()
    # URL validation
    assert open_positions.wait_for_url_contains(open_positions.URL), "Open Position PageURL Not As Expected"
    # Waiting Department Filter to Become Quality Assurance
    assert open_positions.wait_until_qa_department_op()
    # Waiting Jobs to be listed
    open_positions.wait_for_job_list_to_load()
    open_positions.filter_by_location("Istanbul, Turkiye")
    assert open_positions.wait_until_jobs_match_location("Istanbul, Turkiye")
    # 1. Butona tıkla (Tarayıcı yeni sekmeyi açar)
    open_positions.click_first_job_view_role()

    # 2. Selenium'u YENİ SEKMEYE taşı! (ZORUNLU ADIM)
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))  # 2. sekmenin açılmasını bekle
    window_handles = driver.window_handles  # Açık olan tüm sekmelerin ID'lerini al
    driver.switch_to.window(window_handles[1])  # Selenium'u 2. sekmeye (index 1) odakla

    # 3. Artık yeni sekmedeyiz, URL'in Lever sayfası olduğunu doğrula
    assert WebDriverWait(driver, 15).until(EC.url_contains("jobs.lever.co/insiderone")), f"HATA: Lever sayfası açılamadı!"

    # guncel_url = driver.get_current_url
    # assert "jobs.lever.co/insiderone" in guncel_url, f"HATA: Lever sayfası açılamadı! URL: {guncel_url}"

    print("TEST BAŞARIYLA TAMAMLANDI! Lever sayfasına ulaşıldı.")