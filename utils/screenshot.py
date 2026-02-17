import os
from datetime import datetime


def take_screenshot(driver, test_name):
    """
    Take screenshot and save to screenshots folder

    Args:
        driver: WebDriver instance
        test_name: Name of the test
    """
    screenshots_dir = "screenshots"

    # Create screenshots directory if it doesn't exist
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_name}_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)

    # Take screenshot
    driver.save_screenshot(filepath)
    print(f"\nScreenshot saved: {filepath}")

    return filepath