from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# URL to scrape
url = "https://www.quora.com/In-a-nutshell-why-do-a-lot-of-developers-dislike-Agile-What-are-better-project-management-paradigm-alternatives"

# Initialize WebDriver
driver = webdriver.Chrome()

# Open the URL
driver.get(url)

# Pause to ensure the page is fully loaded
time.sleep(5)

try:
    # Scroll down incrementally to load all dynamic content
    scroll_pause_time = 2  # Pause to allow content to load
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page
        time.sleep(scroll_pause_time)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same, it will exit the function
            break
        last_height = new_height

    # After clicking all buttons, extract the updated content from each box
    boxes = driver.find_elements(By.XPATH, "//*[contains(@class, 'dom_annotate_question_answer_item_')]")
    print(f"Number of boxes found: {len(boxes)}")

    for index, box in enumerate(boxes):
        try:
            # Find the "More" button (if exists) within each box
            button = box.find_element(By.CLASS_NAME, 'puppeteer_test_read_more_button')

            # Scroll to the button and ensure it's visible
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)  # Allow time for scrolling

            # Use JavaScript to click the button, bypassing the interception issue
            driver.execute_script("arguments[0].click();", button)
            print(f"Clicked 'More' button in box {index + 1}")
            time.sleep(2)  # Wait for the content to load after each click

            # Extract the author
            try:
                author_element = box.find_element(By.CSS_SELECTOR,
                                                  "span.q-text.qu-dynamicFontSize--small.qu-bold.qu-color--gray_dark")
                author = author_element.text
            except:
                author = "N/A"

            # Extract the author description right after the author's name
            try:
                description_element = box.find_element(By.XPATH, ".//span[contains(@class, 'c1h7helg')]")
                author_description = description_element.text
            except:
                author_description = "N/A"

            # Extract the "years ago" (e.g., 4y) from the span
            try:
                years_ago_element = box.find_element(By.CSS_SELECTOR, "span.q-text.qu-whiteSpace--nowrap")
                years_ago = years_ago_element.text
            except:
                years_ago = "N/A"

            # Extract the votes
            try:
                vote_element = box.find_element(By.CSS_SELECTOR,
                                                "span.q-text.qu-whiteSpace--nowrap.qu-display--inline-flex.qu-alignItems--center.qu-justifyContent--center")
                votes = vote_element.text
            except:
                votes = "N/A"


            # Extract the votes
            try:
                comment = box.find_element(By.CLASS_NAME,
                                                "spacing_log_answer_content")
                text_content = comment.text
            except:
                text_content = "N/A"


            # Print the extracted information in the desired order
            print(f"Box {index + 1} content:")
            print(f"Author: {author}")
            print(f"Author Description: {author_description}")
            print(f"Years Ago: {years_ago}")
            print(f"Full text content of the box:\n{text_content}")
            print(f"Votes: {votes}")
            print("-" * 50)  # Separator between boxes

        except Exception as extract_error:
            print(f"Error extracting content from box {index + 1}: {extract_error}")

except Exception as e:
    print(f"Error during execution: {e}")

finally:
    # Close the browser once done
    driver.quit()








# # Locate the button containing the shares count
# # try:
# #     # Locate the share button with both 'qu-display--inline-block' AND 'qu-whiteSpace--nowrap'
# #     share_button = box.find_element(By.CSS_SELECTOR,
# #                                     "div.q-flex.qu-alignItems--center")
# #
# #     shares = share_button.text  # Extract the visible share count
# #     print(f"Post {index + 1}: Number of shares: {shares}")
# # except Exception as e:
# #     print(f"Error extracting shares for post {index + 1}: {e}")
# #     shares = "N/A"
#
# # # Extract the shares by targeting the specific structure you provided
# # comments_element = box.find_element(By.XPATH,
# #                                   ".//div[@class='q-text qu-overflow--hidden qu-display--inline-flex qu-color--gray qu-ml--tiny']//span[contains(@class, 'qu-whiteSpace--nowrap')]")
# # shares = comments_element.text
#
# # Extract the full text content after clicking the button
# text_content = box.text