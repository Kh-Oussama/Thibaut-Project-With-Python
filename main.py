import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

# URL to scrape
url = "https://www.quora.com/What-are-the-disadvantages-of-agile-software-development"

# Initialize WebDriver
driver = webdriver.Chrome()

# Open the URL
driver.get(url)

# Pause to ensure the page is fully loaded
time.sleep(5)

# Create an empty list to store data
data = []

# Get the current date
current_date = datetime.now()

# Define a list of month abbreviations
months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

try:
    # Scroll down incrementally to load all dynamic content
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # After scrolling, locate all posts (boxes)
    boxes = driver.find_elements(By.XPATH, "//*[contains(@class, 'dom_annotate_question_answer_item_')]")
    print(f"Number of boxes found: {len(boxes)}")

    for index, box in enumerate(boxes):
        try:
            # Find the "More" button (if exists) within each box
            try:
                button = box.find_element(By.CLASS_NAME, 'puppeteer_test_read_more_button')

                # Scroll to the button and ensure it's visible
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(1)

                # Use JavaScript to click the button, bypassing the interception issue
                driver.execute_script("arguments[0].click();", button)
                print(f"Clicked 'More' button in box {index + 1}")
                time.sleep(2)
            except:
                print(f"No 'More' button found in box {index + 1}")

            # Extract the author
            try:
                author_element = box.find_element(By.CSS_SELECTOR, "span.q-text.qu-dynamicFontSize--small.qu-bold.qu-color--gray_dark")
                author = author_element.text
            except:
                author = "N/A"

            # Extract the author description right after the author's name
            try:
                description_element = box.find_element(By.XPATH, ".//span[contains(@class, 'c1h7helg')]")
                author_description = description_element.text
            except:
                author_description = "N/A"

            # Extract the "time ago" and calculate the publication date (year/month)
            try:
                time_ago_element = box.find_element(By.CSS_SELECTOR, "span.q-text.qu-whiteSpace--nowrap")
                time_ago_text = time_ago_element.text.lower().strip()

                # Handle "Updated Xy", "Xy", "Xm", and month name cases
                if "updated" in time_ago_text and "y" in time_ago_text:
                    years_ago = int(time_ago_text.split("updated")[1].strip().replace("y", ""))  # Extract the number of years from "Updated Xy"
                    publication_date = str(current_date.year - years_ago)
                elif "y" in time_ago_text:
                    years_ago = int(time_ago_text.replace("y", "").strip())  # Extract the number of years from "Xy"
                    publication_date = str(current_date.year - years_ago)
                elif "m" in time_ago_text:
                    months_ago = int(time_ago_text.replace("m", "").strip())  # Extract the number of months from "Xm"
                    publication_date = (current_date - relativedelta(months=months_ago)).strftime("%Y-%m")  # Subtract months
                else:
                    # Handle full month names (e.g., May, Jul, etc.)
                    for month in months:
                        if month in time_ago_text:
                            month_index = months.index(month) + 1  # Convert month name to its index
                            publication_date = f"{current_date.year}-{month_index:02d}"  # Format as YYYY-MM
                            break
                    else:
                        publication_date = "N/A"
            except:
                publication_date = "N/A"

            # Extract the votes, else put 0 if not found
            try:
                vote_element = box.find_element(By.CSS_SELECTOR, "span.q-text.qu-whiteSpace--nowrap.qu-display--inline-flex.qu-alignItems--center.qu-justifyContent--center")
                votes = vote_element.text
            except:
                votes = "0"  # Default to 0 if votes are not found

            # Extract the review (comments)
            try:
                comment = box.find_element(By.CLASS_NAME, "spacing_log_answer_content")
                review = comment.text  # Changed "Content" to "Review"
            except:
                review = "N/A"

            # Append the extracted information to the list
            data.append({
                "Author": author,
                "Author Description": author_description,
                "Publication Date": publication_date,  # Changed "Time Ago" to "Publication Date"
                "Votes": votes,
                "Review": review  # Changed "Content" to "Review"
            })

            # Print the extracted information
            print(f"Box {index + 1} content:")
            print(f"Author: {author}")
            print(f"Author Description: {author_description}")
            print(f"Publication Date: {publication_date}")
            print(f"Review:\n{review}")
            print(f"Votes: {votes}")
            print("-" * 50)

        except Exception as extract_error:
            print(f"Error extracting content from box {index + 1}: {extract_error}")

except Exception as e:
    print(f"Error during execution: {e}")

finally:
    # Close the browser
    driver.quit()

# Convert the list of dictionaries into a pandas DataFrame
df = pd.DataFrame(data)

# Export the DataFrame to CSV and Excel files
df.to_csv('scraped_data-4.csv', index=False)
df.to_excel('scraped_data-4.xlsx', index=False)

print("Data has been saved to CSV and Excel files.")
