import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Path to your ChromeDriver
chromedriver_path = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"  # Update with your actual path

# Set up ChromeDriver service
service = Service(chromedriver_path)

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # Open the Django search page
    driver.get("http://127.0.0.1:8000/books/2")  # Update the URL if needed (e.g., your local Django app)

    time.sleep(8)
    search_box = driver.find_element(By.NAME, "q")

    search_box.send_keys("Harry Potter")
    language_dropdown = driver.find_element(By.NAME, "language")
    language_dropdown.send_keys("English")
    search_box.send_keys(Keys.RETURN)
    time.sleep(8)
    results = driver.find_elements(By.TAG_NAME, "li")  # Assuming results are in <li> tags


    search_results = []
    if results:
        for result in results:
            search_results.append(result.text)  # Adjust if results contain more structure (e.g., titles, links)

        # Serialize the data to JSON
        results_json = {
            "search_term": "Harry Potter",
            "language": "English",
            "results_count": len(search_results),
            "results": search_results,
        }

        # Save JSON data to a file
        with open("search_results.json", "w", encoding="utf-8") as json_file:
            json.dump(results_json, json_file, ensure_ascii=False, indent=4)

        print("Search results saved to 'search_results.json'.")
    else:
        print("No results found.")

finally:
    # Close the browser
    driver.quit()
