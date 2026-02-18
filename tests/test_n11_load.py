from locust import HttpUser, task, between, events
import random


class N11SearchUser(HttpUser):
    """
    Load test for N11.com search functionality
    """

    wait_time = between(1, 3)
    host = "https://www.n11.com"

    search_keywords = [
        "laptop",
        "telefon",
        "kulaklık",
        "kitap",
        "ayakkabı",
        "çanta",
        "saat",
        "oyuncak"
    ]

    def on_start(self):
        """Set headers to avoid 403 and visit homepage"""
        self.client.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        })
        # Visit homepage first
        self.client.get("/", name="Homepage")

    @task(5)
    def search_product(self):
        """
        Positive: Search for a product
        Weight: 5 (most common operation)
        """
        keyword = random.choice(self.search_keywords)

        with self.client.get(
            "/arama",
            params={"q": keyword},
            name="Search Product",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code: {response.status_code}")

    @task(3)
    def search_with_pagination(self):
        """
        Positive: Search and navigate to next page
        Weight: 3
        """
        keyword = random.choice(self.search_keywords)

        # First search
        self.client.get(
            "/arama",
            params={"q": keyword},
            name="Search for Pagination - Initial"
        )

        # Navigate to page 2-5
        page_number = random.randint(2, 5)
        with self.client.get(
            "/arama",
            params={
                "q": keyword,
                "pg": page_number
            },
            name="Search for Pagination - Page Navigation",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Pagination failed with status: {response.status_code}")

    @task(2)
    def search_with_filters(self):
        """
        Positive: Search with price filter
        Weight: 2
        """
        keyword = random.choice(self.search_keywords)

        with self.client.get(
            "/arama",
            params={
                "q": keyword,
                "srt": "PRICE_LOW"
            },
            name="Search with Filter",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Filtered search failed: {response.status_code}")

    @task(2)
    def search_with_sorting(self):
        """
        Positive: Search and apply sorting
        Weight: 2
        """
        keyword = random.choice(self.search_keywords)
        sort_options = ["PRICE_LOW", "PRICE_HIGH", "REVIEW_COUNT"]
        sort_by = random.choice(sort_options)

        with self.client.get(
            "/arama",
            params={
                "q": keyword,
                "srt": sort_by
            },
            name="Search with Sorting",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Sorted search failed: {response.status_code}")

    @task(1)
    def empty_search(self):
        """
        Negative: Perform empty search
        Weight: 1
        """
        with self.client.get(
            "/arama",
            params={"q": ""},
            name="Empty Search (Negative)",
            catch_response=True
        ) as response:
            if response.status_code in [200, 302]:
                response.success()
            else:
                response.failure(f"Empty search failed: {response.status_code}")

    @task(1)
    def special_character_search(self):
        """
        Negative: Search with special characters
        Weight: 1
        """
        special_queries = ["@#$%", "'''", "---", "123456789"]
        query = random.choice(special_queries)

        with self.client.get(
            "/arama",
            params={"q": query},
            name="Special Character Search (Negative)",
            catch_response=True
        ) as response:
            if response.status_code in [200, 404]:
                response.success()
            else:
                response.failure(f"Special char search failed: {response.status_code}")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("\n" + "=" * 50)
    print("Starting N11.com Search Module Load Test")
    print("=" * 50 + "\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("\n" + "=" * 50)
    print("N11.com Search Module Load Test Completed")
    print("=" * 50 + "\n")