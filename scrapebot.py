from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from ordered_set import OrderedSet
import time
import uuid

def scrape():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    # "Start search"
    query = "naklecha"

    driver.get(f"https://duckduckgo.com?q={query}")

    for _ in range(0):
        # Scroll down using JavaScript
        driver.find_element(By.CSS_SELECTOR, "#more-results").click()
        # Wait for a short duration to allow the content to load
        time.sleep(1)

    # Click on the first link to open it
    links = driver.find_elements(By.CSS_SELECTOR, "a")

    filtered_links = OrderedSet()

    for element in links:
        link = element.get_attribute("href")
        if((type(link) == str) and ("http" in link) and ("duckduckgo" not in link)):
            filtered_links.add(link)

    print(filtered_links)
    print(len(filtered_links))

    # Iterate through filtered links and add information to the PDF
    for link in filtered_links:
        driver.get(link)
        time.sleep(2)
        # Set the window size to the size of the whole page
        driver.set_window_size(driver.execute_script('return document.body.parentNode.scrollWidth'), 2000)
        screenshot = driver.get_screenshot_as_png()
        with open(f"screenshots/screenshot_{uuid.uuid4()}.png", "wb") as file:
            file.write(screenshot)

    # Close the browser window
    driver.quit()

if __name__ == "__main__":
    scrape()