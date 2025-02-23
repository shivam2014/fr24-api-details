from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set up Selenium with ChromeDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Headless mode disabled for visibility
service = Service("./chromedriver.exe")  # Assumes chromedriver.exe is in the same folder
driver = webdriver.Chrome(service=service, options=chrome_options)

# URLs to scrape
urls = {
    "departures": "https://www.flightstats.com/v2/flight-tracker/departures/ARN/?year=2025&month=2&date=20&hour=6",
    "arrivals": "https://www.flightstats.com/v2/flight-tracker/arrivals/ARN/?year=2025&month=2&date=20&hour=6"
}

# Function to dismiss cookie consent popup
def dismiss_cookie_popup():
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_button.click()
        time.sleep(1)
        print("Cookie popup dismissed.")
    except Exception as e:
        print(f"No cookie popup found or error dismissing it: {e}")

# Function to scrape table data from a page
def scrape_table():
    data = []
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table__TableContainer-sc-1x7nv9w-5"))
        )
        container = driver.find_element(By.CLASS_NAME, "table__TableContainer-sc-1x7nv9w-5")
        rows = container.find_elements(By.CLASS_NAME, "table__A-sc-1x7nv9w-2")
        print(f"Found {len(rows)} rows on this page.")
        
        for row in rows:
            table_rows = row.find_elements(By.CLASS_NAME, "table__TableRow-sc-1x7nv9w-7")
            if len(table_rows) >= 2:
                main_cells = table_rows[0].find_elements(By.CLASS_NAME, "table__Cell-sc-1x7nv9w-13")
                main_data = [cell.text.strip() for cell in main_cells if cell.text.strip()]
                
                sub_cells = table_rows[1].find_elements(By.CLASS_NAME, "table__Cell-sc-1x7nv9w-13")
                sub_data = [cell.text.strip() for cell in sub_cells if cell.text.strip()]
                
                if len(main_data) >= 4 and len(sub_data) >= 2:
                    row_data = main_data[:4] + sub_data[:2]
                    data.append(row_data)
    except Exception as e:
        print(f"Error scraping table: {e}")
    return data

# Function to set "Show Codeshares?" to "Hide" (simplified to use label only)
def set_codeshares_to_hide():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "toggle__ToggleFieldWithLabel-sc-ud0tsg-0"))
        )
        toggle = driver.find_element(By.CSS_SELECTOR, "input[name='showCodeshares']")
        is_checked = toggle.is_selected()
        print(f"Toggle initial state: {'Hide (checked)' if is_checked else 'Show (unchecked)'}")
        
        if not is_checked:  # If unchecked (Show), click the label to set to Hide
            label = driver.find_element(By.CLASS_NAME, "styled-elements__ToggleControl-sc-1dy6vsq-4")
            label.click()
            print("Clicked label to set to 'Hide'.")
        
        time.sleep(1)
        is_checked = toggle.is_selected()
        if is_checked:
            print("Codeshares successfully set to 'Hide'.")
        else:
            print("Failed to set codeshares to 'Hide' - still unchecked.")
    except Exception as e:
        print(f"Error setting codeshares toggle: {e}")

# Scrape both pages and store data
all_data = {"departures": [], "arrivals": []}

for page_type, url in urls.items():
    print(f"\nScraping {page_type} from {url}")
    driver.get(url)
    time.sleep(10)  # Initial page load
    
    dismiss_cookie_popup()
    set_codeshares_to_hide()
    
    page_num = 1
    prev_page_data = None
    max_pages = 20  # Failsafe to prevent infinite loop
    
    while page_num <= max_pages:
        print(f"Scraping page {page_num}...")
        page_data = scrape_table()
        
        # Check for duplicate data before adding
        if prev_page_data and page_data == prev_page_data:
            print(f"Page {page_num} data matches page {page_num-1}. Assuming last page reached.")
            break
        
        # Add data only if it’s new
        all_data[page_type].extend(page_data)
        print(f"Collected {len(page_data)} rows from page {page_num}. Total so far: {len(all_data[page_type])}")
        
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='pagination__PageNavigation-sc-1515b5x-3 bFumhV' and text()='→']"))
            )
            parent = next_button.find_element(By.XPATH, "..")
            parent_classes = parent.get_attribute("class")
            
            if "kymFjQ" in parent_classes or "kNhNYC" not in parent_classes:
                print(f"Reached the last page ({page_num}). 'Next' button disabled (classes: {parent_classes}).")
                break
            
            driver.execute_script("arguments[0].click();", next_button)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "table__TableContainer-sc-1x7nv9w-5"))
            )
            prev_page_data = page_data  # Store current page data for comparison
            page_num += 1
            time.sleep(1)
        except Exception as e:
            print(f"Pagination ended or error: {e}")
            break

driver.quit()

# Define headers for each type
headers = {
    "departures": ["Flight", "Departure Time", "Arrival Time", "Destination Code", "Airline", "Destination Full"],
    "arrivals": ["Flight", "Departure Time", "Arrival Time", "Origin Code", "Airline", "Origin Full"]
}

# Save data to CSV and Excel files
for page_type in all_data:
    df = pd.DataFrame(all_data[page_type], columns=headers[page_type])
    df.to_csv(f"flight_{page_type}.csv", index=False)
    #df.to_excel(f"flight_{page_type}.xlsx", index=False)
    print(f"{page_type.capitalize()} data scraped: {len(all_data[page_type])} rows saved to flight_{page_type}.csv")

print("Scraping complete.")