from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def main():
    # Setup Chrome WebDriver with automatic ChromeDriver management
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Basic navigation
        print("1. Basic Navigation")
        driver.get("https://www.python.org")
        print(f"Title: {driver.title}")

        # Finding elements (various methods)
        print("\n2. Finding Elements")
        # By ID
        search_bar = driver.find_element(By.ID, "id-search-field")
        search_bar.clear()
        search_bar.send_keys("selenium")
        search_bar.send_keys(Keys.RETURN)

        # Explicit wait for search results
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "list-recent-events"))
        )

        # Finding multiple elements
        print("\n3. Finding Multiple Elements")
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"Number of links on page: {len(links)}")

        # Working with browser windows
        print("\n4. Browser Window Management")
        print(f"Current window size: {driver.get_window_size()}")
        driver.maximize_window()
        time.sleep(5)  # Brief pause to see the maximization

        # Taking screenshots
        print("\n5. Taking Screenshots")
        driver.save_screenshot("python_org_search.png")

        # Browser navigation
        print("\n6. Browser Navigation")
        driver.back()
        print("Navigated back")
        time.sleep(5)
        driver.forward()
        print("Navigated forward")

        # Handling cookies
        print("\n7. Cookie Management")
        cookies = driver.get_cookies()
        print(f"Number of cookies: {len(cookies)}")

        # Example of executing JavaScript
        print("\n8. JavaScript Execution")
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        print(f"Page height: {scroll_height}px")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Always quit the browser
        print("\n9. Cleaning up")
        driver.quit()
        print("Browser closed")


if __name__ == "__main__":
    main()
