import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login_page(driver):
    driver.get('http://127.0.0.1:8000/login/')  # GET request to load the login page
    
    # Wait for the email input field to be present
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'email'))
    )

    password_input = driver.find_element(By.NAME, 'password')
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")  # Submit button

    # Fill in the login credentials
    email_input.send_keys('test@mail.com')
    password_input.send_keys('test')

    # Submit the form via POST by clicking the submit button
    login_button.click()

    # Optionally, wait for the page to load and check for a successful login
    WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))  # Replace with your success condition

    # Check if login was successful
    assert 'Welcome, testuser' in driver.page_source
