from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests
import time


def setup_driver():
    # Setup Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment if you don't want the browser to open
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def download_file(url, folder="downloaded_pdfs_100"):
    local_filename = url.split('/')[-1]
    path = os.path.join(folder, local_filename)
    response = requests.get(url, stream=True)
    os.makedirs(folder, exist_ok=True)
    with open(path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return local_filename


def try_click_next_button(driver, button_id, c_page, retry_limit=50):
    attempts = 0
    while attempts < retry_limit:
        try:
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, button_id))
            )
            next_button.click()
            return True
        except (ElementClickInterceptedException, TimeoutException):
            time.sleep(1)
            attempts += 1
    print(f"Failed to click the next button after several attempts on page {c_page}.")
    return False  # Failed to click after retries


def select_dropdown_option(driver, dropdown_css_selector, value):
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, dropdown_css_selector))
        )
        dropdown = Select(driver.find_element(By.CSS_SELECTOR, dropdown_css_selector))
        dropdown.select_by_value(value)
        print(f"Set page length to {value} successfully.")
    except Exception as e:
        print(f"Failed to set page length due to: {str(e)}")


def scrape_and_download(driver, base_url, start_page, end_page):
    driver.get(base_url)

    time.sleep(5)

    select_dropdown_option(driver, "select[name='posts_length']", "100")

    current_page = 1

    while current_page < start_page:

        percentage = 5
        scroll_script = f"""
                                    var height = document.body.scrollHeight;
                                    window.scrollBy(0, -height * {percentage / 100});
                                    """
        driver.execute_script(scroll_script)

        if not try_click_next_button(driver, "posts_next", current_page):
            break
        current_page += 1
        print(f"Current page: {current_page}")

        time.sleep(0.5)

    current_page = start_page

    while current_page <= end_page:
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "posts"))
            )
            time.sleep(0.1)
            table = driver.find_element(By.ID, "posts")
            tbody = table.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")

            print(rows)

            for row in rows:
                pdf_link_elements = row.find_elements(By.TAG_NAME, "td")[6].find_elements(By.TAG_NAME, "a")
                if pdf_link_elements and pdf_link_elements[0].get_attribute('href').endswith(".pdf"):
                    pdf_url = pdf_link_elements[0].get_attribute('href')
                    downloaded_file = download_file(pdf_url)
                    print(f"Downloaded {downloaded_file}")

            if current_page < end_page:

                percentage = 5
                scroll_script = f"""
                    var height = document.body.scrollHeight;
                    window.scrollBy(0, -height * {percentage / 100});
                    """
                driver.execute_script(scroll_script)

                if not try_click_next_button(driver, "posts_next", current_page):
                    break

            current_page += 1

            time.sleep(1)

            print(f"Current page: {current_page}")

        except Exception as e:
            print(f"Error on page {current_page}: {str(e)}")
            break  # Exit the loop if an error occurs


driver = setup_driver()
base_url = "https://www.titck.gov.tr/kubkt"
scrape_and_download(driver, base_url, 85, 149)
driver.quit()
