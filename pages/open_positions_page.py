import time

from pycparser.c_ast import Return
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OpenPositionsPage(BasePage):
    URL = "https://insiderone.com/careers/open-positions"
    DEPARTMENT_FILTER = (By.ID, "filter-by-department")
    LOCATION_FILTER = (By.ID, "filter-by-location")
    JOB_ITEM = (By.CSS_SELECTOR, ".position-list-item")  # Her job card'ın ortak class'ı
    JOB_LOCATION = (By.CSS_SELECTOR, ".position-location")  # Her job card'ın location class'ı
    JOB_DEPARTMENT = (By.CSS_SELECTOR, ".position-department")  # Her job card'ın depoartment class'ı

    def wait_until_qa_department_op(self):
        # Since reaching open positions page from Quality Assurance, should be waiting department filter to be presented as Quality Assurance
        initial_time = time.time()
        if WebDriverWait(self.driver, 40).until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "#filter-by-department option[selected]"),
                    "Quality Assurance"
                )
        ):
            print("\nTime Passed to Filter Department as Quality Assurance", time.time() - initial_time)
            return True
        else:
            return False

    def wait_for_job_list_to_load(self):
        """
        En az 1 tane job card (.position-list-item) görünür olana kadar bekler.
        Spesifik metin beklenmez, sadece element yapısı beklenir.
        """
        initial_time = time.time()
        # En az 1 tane job item görünür olana kadar bekle
        WebDriverWait(self.driver, 40).until(EC.visibility_of_any_elements_located(self.JOB_ITEM))
        print("Time Passed to List QA Jobs", time.time() - initial_time)
        return True

    def filter_by_location(self, location):
        location_dropdown = Select(self.find_element(self.LOCATION_FILTER))
        location_dropdown.select_by_visible_text(location)

    def filter_by_department(self, department):
        location_dropdown = Select(self.find_element(self.DEPARTMENT_FILTER))
        location_dropdown.select_by_visible_text(department)

    def wait_for_jobs_by_location(self, location_text):
        """
        Location filtresi uygulandıktan sonra eski ilanların gidip,
        sadece seçilen lokasyona ait ilanların görünür olmasını bekler.
        """
        a = time.time()

        def filter_applied(driver):
            jobs = driver.find_elements(*self.JOB_ITEM)
            visible_jobs = [job for job in jobs if job.is_displayed()]

            # Eğer hiç görünür job yoksa (liste yenilenirken boşalmışsa), beklemeye devam et
            if len(visible_jobs) == 0:
                return False

            # Görünen TÜM ilanların metninde aradığımız lokasyon (örn: "Istanbul, Turkiye") geçmeli
            for job in visible_jobs:
                if location_text not in job.text:
                    # İçinde Istanbul geçmeyen bir ilan hala ekrandaysa, eski liste gitmemiştir.
                    return False

                    # Eğer döngü başarıyla bittiyse, ekrandaki tüm ilanlar "Istanbul, Turkiye"ye aittir!
            return True

        # Custom yazdığımız bu koşulun gerçekleşmesini bekle
        WebDriverWait(self.driver, 40).until(filter_applied)

        # Artık güvenle sayabiliriz
        job_count = self.get_job_count()
        print(f"⏱️ Time Passed for Location '{location_text}': {time.time() - a:.2f}s")
        print(f"✅ {job_count} job(s) found for location: {location_text}")

        return job_count

    def get_job_count(self):
        """
        Görünür job sayısını döner.
        """
        jobs = self.driver.find_elements(*self.JOB_ITEM)
        return len([job for job in jobs if job.is_displayed()])

    def wait_until_jobs_match_location(self, location_text, timeout=40):
        """
        Location filtresi uygulandıktan sonra:
        1. Liste güncellenmesini bekler.
        2. En az 1 job görünmesini bekler.
        3. Tüm job'ların location'ı location_text ile eşleşsin.

        Returns:
            bool: True (en az 1 job var ve hepsi eşleşiyor)
            False: 0 job var (filtre sonucu boş liste)

        Raises:
            TimeoutException: Liste 40 saniye boyunca yanlış lokasyonlu job'ları göstermeye devam ederse
        """
        start = time.time()

        def predicate(driver):
            try:
                jobs = driver.find_elements(*self.JOB_ITEM)
                visible_jobs = [job for job in jobs if job.is_displayed()]

                # 0 job varsa: False dön (beklenen en az 1 job)
                if not visible_jobs:
                    return False

                # Tüm job'ların location'ı eşleşmeli
                for job in visible_jobs:
                    loc = job.find_element(*self.JOB_LOCATION).text.strip()
                    if loc != location_text:
                        return False

                return True  # En az 1 job var ve hepsi eşleşiyor

            except (StaleElementReferenceException, NoSuchElementException):
                return False  # DOM güncellenirken elementler stale/ulaşılamaz olabilir

        try:
            WebDriverWait(self.driver, timeout).until(predicate)
            elapsed = time.time() - start
            print(
                f"{len(self.driver.find_elements(*self.JOB_ITEM))} job(s) found for '{location_text}' in {elapsed:.2f}s")
            return True
        except TimeoutException:
            # Liste 40 saniye boyunca yanlış lokasyonlu job'ları göstermeye devam ederse
            jobs = self.driver.find_elements(*self.JOB_ITEM)
            visible_jobs = [job for job in jobs if job.is_displayed()]

            if not visible_jobs:
                # 0 job var
                print(f"No jobs found for '{location_text}'")
                return False
            else:
                # Gerçekten yanlış lokasyonlu job'lar var
                print(f"Timeout: Some jobs still do not match location '{location_text}' after {timeout}s")
                raise  # TimeoutException'ı tekrar fırlat

    def click_first_job_view_role(self):
        """
        Görünür olan ilk job'ın 'View Role' butonuna tıklar.
        """
        jobs = self.driver.find_elements(*self.JOB_ITEM)
        visible_jobs = [job for job in jobs if job.is_displayed()]

        if not visible_jobs:
            raise Exception("No visible jobs to click!")

        first_job = visible_jobs[0]
        view_role_button = first_job.find_element(By.CLASS_NAME, "btn-navy")

        # Bazen sayfanın altında kalırsa tıklayamayabilir, garanti olsun diye elemente scroll yapalım:
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_role_button)
        time.sleep(1)  # Scrollun bitmesini bekle

        view_role_button.click()
        print("First job's 'View Role' button clicked!")
