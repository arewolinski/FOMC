import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import requests
import os


def download_transcripts_for_year(year):
    # Navigate to the year-specific meetings page
    driver.get(f"https://www.federalreserve.gov/monetarypolicy/fomchistorical{year}.htm")

    # Wait until at least one meeting element is present
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//h5[contains(text(), 'Meeting')]")))

    # Find all h5 elements containing the word "Meeting"
    meeting_elements = driver.find_elements(By.XPATH, "//h5[contains(text(), 'Meeting')]")

    # Check the count
    if len(meeting_elements) != 8:
        print(f"Warning for {year}: Found {len(meeting_elements)} meetings, expected 8.")

    # Loop through each meeting title and download its Transcript PDF
    for i in range(8):
        try:
            element = driver.find_elements(By.XPATH, "//h5[contains(text(), 'Meeting')]")[i]
            file_name = f"{i+1}_{year}_transcript.pdf"
            
            # Find the parent div of h5
            parent_div = element.find_element(By.XPATH, "./ancestor::div[@class='panel-heading']")
            
            # Locate the sibling div containing the transcript link
            sibling_div = parent_div.find_element(By.XPATH, "./following-sibling::div")
            
            # Locate the Transcript link within the sibling div
            transcript_link = sibling_div.find_element(By.XPATH, ".//a[contains(text(), 'Transcript')]")
            
            # Get the URL of the transcript
            transcript_url = transcript_link.get_attribute('href')
            
            # Use requests to download the PDF
            r = requests.get(transcript_url, stream=True)
            with open(f"/Users/yeldagungor/Dropbox/YH/FOMC_code/transcripts/{file_name}", 'wb') as fd:
                for chunk in r.iter_content(chunk_size=2000):
                    fd.write(chunk)
        except StaleElementReferenceException:
            print(f"StaleElementReferenceException encountered for element {i + 1}. Retrying...")
            continue

    # Sleep for a short duration before moving to the next year to be considerate to the server
    time.sleep(5)


# Initialize the Selenium WebDriver
service = Service(executable_path='/Users/yeldagungor/Dropbox/YH/FOMC_code/chromedriver')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Loop over each year and download transcripts
for year in range(1987, 2007):  # This will cover 1987 to 2006 inclusive
    print(f"Processing year: {year}")
    download_transcripts_for_year(year)

# Close the browser window
driver.quit()
