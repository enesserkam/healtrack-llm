def scrape_and_download(driver, base_url,start_page, end_page):
    driver.get(base_url)
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "posts"))
        )
    except Exception as e:
        print(f"Initial page load error: {str(e)}")
        return

    for page in range(start_page, end_page + 1):
        try:

            page_link = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.XPATH, f'//a[@data-dt-idx="{page}" and @aria-controls="posts"]'))
            )
            page_link.click()

            # Check for JavaScript and AJAX loads to complete
            WebDriverWait(driver, 25).until(lambda driver: driver.execute_script('return jQuery.active == 0'))
            WebDriverWait(driver, 25).until(lambda driver: driver.execute_script('return document.readyState == "complete"'))

            WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.ID, "posts"))
            )

            table = driver.find_element(By.ID, "posts")
            tbody = table.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                try:
                    pdf_link_element = row.find_elements(By.TAG_NAME, "td")[6].find_element(By.TAG_NAME, "a")
                    pdf_url = pdf_link_element.get_attribute('href')
                    if pdf_url.endswith(".pdf"):
                        downloaded_file = download_file(pdf_url)
                        print(f"Downloaded {downloaded_file}")
                except IndexError:
                    continue  # Skip rows that don't match the structure

        except Exception as e:
            print(f"Error on page {page}: {str(e)}")

        time.sleep(3)


driver_main = setup_driver()
base_url = "https://www.titck.gov.tr/kubkt"
scrape_and_download(driver_main, base_url, 1, 1481)  # Adjust the range based on actual page numbers
driver_main.quit()