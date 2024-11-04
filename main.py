
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

# List of URLs to scrape
urls = [
    "https://www.quora.com/In-a-nutshell-why-do-a-lot-of-developers-dislike-Agile-What-are-better-project-management-paradigm-alternatives",
    "https://www.quora.com/Do-programmers-really-like-Scrum",
    "https://www.quora.com/What-is-agile-methodology-and-what-are-the-advantages-and-disadvantages-of-agile-methodology",
    "https://www.quora.com/What-are-the-disadvantages-of-agile-software-development"
]

# Initialize WebDriver
driver = webdriver.Chrome()

# Pause to ensure the page is fully loaded
scroll_pause_time = 5

# Create an empty list to store data
data = []

# Get the current date
current_date = datetime.now()

# Define a list of month abbreviations
months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

# Loop through each URL
for url in urls:
    try:
        # Open the URL
        driver.get(url)
        time.sleep(8)  # Adjust the time to ensure the page is fully loaded

        # Click the "All related" button
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'q-click-wrapper') and .//div[contains(text(), 'All related')]]")
            )
        )
        button.click()
        print("Clicked the 'All related' button.")

        # Click the "Answers" dropdown item
        dropdown_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[contains(@class, 'puppeteer_test_popover_item') and .//div[starts-with(text(), 'Answers')]]")
            )
        )
        dropdown_item.click()
        print("Clicked the 'Answers' dropdown item.")

        # Allow the dropdown to process
        time.sleep(10)

        # Scroll down incrementally to load all dynamic content
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Locate all posts (boxes)
        boxes = driver.find_elements(By.XPATH, "//*[contains(@class, 'dom_annotate_question_answer_item_')]")
        print(f"Number of boxes found: {len(boxes)} for URL: {url}")

        for index, box in enumerate(boxes):
            try:
                # Find the "More" button (if exists) within each box
                try:
                    button = box.find_element(By.CLASS_NAME, 'puppeteer_test_read_more_button')
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(3)
                    driver.execute_script("arguments[0].click();", button)
                    print(f"Clicked 'More' button in box {index + 1}")
                    time.sleep(3)
                except:
                    print(f"No 'More' button found in box {index + 1}")

                # Extract the author
                try:
                    author_element = box.find_element(By.CSS_SELECTOR, "span.q-text.qu-dynamicFontSize--small.qu-bold.qu-color--gray_dark")
                    author = author_element.text
                except:
                    author = "N/A"

                # Extract the author description
                try:
                    description_element = box.find_element(By.XPATH, ".//span[contains(@class, 'c1h7helg')]")
                    author_description = description_element.text
                except:
                    author_description = "N/A"

                # Extract the "time ago" and calculate the publication date (year/month)
                try:
                    time_ago_element = box.find_element(By.CSS_SELECTOR, "span.q-text.qu-whiteSpace--nowrap")
                    time_ago_text = time_ago_element.text.lower().strip()

                    if "updated" in time_ago_text and "y" in time_ago_text:
                        years_ago = int(time_ago_text.split("updated")[1].strip().replace("y", ""))
                        publication_date = str(current_date.year - years_ago)
                    elif "y" in time_ago_text:
                        years_ago = int(time_ago_text.replace("y", "").strip())
                        publication_date = str(current_date.year - years_ago)
                    elif "m" in time_ago_text:
                        months_ago = int(time_ago_text.replace("m", "").strip())
                        publication_date = (current_date - relativedelta(months=months_ago)).strftime("%Y-%m")
                    else:
                        for month in months:
                            if month in time_ago_text:
                                month_index = months.index(month) + 1
                                publication_date = f"{current_date.year}-{month_index:02d}"
                                break
                        else:
                            publication_date = "N/A"
                except:
                    publication_date = "N/A"

                # Extract the votes
                try:
                    vote_element = box.find_element(By.CSS_SELECTOR, "span.q-text.qu-whiteSpace--nowrap.qu-display--inline-flex.qu-alignItems--center.qu-justifyContent--center")
                    votes = vote_element.text
                except:
                    votes = "0"

                # Extract the review
                try:
                    comment = box.find_element(By.CLASS_NAME, "spacing_log_answer_content")
                    review = comment.text
                except:
                    review = "N/A"

                # Append the extracted information to the list
                data.append({
                    "URL": url,  # Add URL for each entry
                    "Author": author,
                    "Author Description": author_description,
                    "Publication Date": publication_date,
                    "Votes": votes,
                    "Review": review
                })

            except Exception as extract_error:
                print(f"Error extracting content from box {index + 1} on {url}: {extract_error}")

    except Exception as e:
        print(f"Error scraping URL {url}: {e}")

# Close the browser
driver.quit()

# Convert the list of dictionaries into a pandas DataFrame
df = pd.DataFrame(data)

# Export the combined DataFrame to CSV and Excel files
df.to_csv('combined_scraped_data.csv', index=False)
df.to_excel('combined_scraped_data.xlsx', index=False)

print("Data has been saved to CSV and Excel files.")
