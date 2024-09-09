import os

PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

from bs4 import BeautifulSoup
from requests_html import HTML, HTMLSession
import numpy as np
import pandas as pd

# URL to scrape
url = "https://www.quora.com/Why-do-I-feel-like-Agile-sucks-for-software-development"

# Initialize an HTML session
session = HTMLSession()
response = session.get(url)


# Render the JavaScript on the page and scroll down to load more content
response.html.render(scrolldown=5, sleep=2)

# Re-parse the HTML after rendering
soup = BeautifulSoup(response.html.html, 'html.parser')

# Initialize lists to store extracted data
authors = []
dates = []
comments = []

# Use soup.select to select relevant elements
# Select all divs with the class that contains 'dom_annotate_question_answer_item_0'
review_boxes = soup.select('div.q-box.dom_annotate_question_answer_item_1')

# Loop through each review box
for box in review_boxes:
    # Find the author using soup.select and CSS selectors
    author = box.select('span.q-text.qu-dynamicFontSize--small.qu-bold.qu-color--gray_dark')
    author = author[0].get_text() if author else "N/A"

    # Find the date using soup.select
    date = box.select('div.q-text.qu-dynamicFontSize--small.qu-color--gray')
    date = date[0].get_text() if date else "N/A"

    # Find the comment text using soup.select
    comment = box.select('div.q-text.qu-wordBreak--break-word')
    comment_text = comment[0].get_text(separator=' ') if comment else "N/A"

    # Append to lists
    authors.append(author)
    dates.append(date)
    comments.append(comment_text)

# Print extracted information
for i in range(len(authors)):
    print(f"Author: {authors[i]}")
    print(f"Date: {dates[i]}")
    print(f"Comment: {comments[i]}")
    print("-" * 50)