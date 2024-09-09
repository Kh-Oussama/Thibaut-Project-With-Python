import os

PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

from bs4 import BeautifulSoup
from requests_html import HTML, HTMLSession
import numpy as np
import pandas as pd

# URL to scrape
url = "https://news.ycombinator.com/item?id=20600128"

# Initialize an HTML session
session = HTMLSession()
response = session.get(url)


# Render the JavaScript on the page and scroll down to load more content
response.html.render()

# Re-parse the HTML after rendering
soup = BeautifulSoup(response.html.html, 'html.parser')

# Extract the comments section
comments = soup.select('tr.comtr')

# Initialize lists to store extracted data
authors = []
dates = []
comment_texts = []

# Loop through each comment
for comment in comments:
    # Find the author
    author = comment.find('a', class_='hnuser').get_text() if comment.find('a', class_='hnuser') else "N/A"
    # Find the date
    date = comment.find('span', class_='age').get_text() if comment.find('span', class_='age') else "N/A"
    # Find the comment text
    comment_text = comment.find('div', class_='commtext c00').get_text() if comment.find('div',
                                                                                         class_='commtext c00') else "N/A"

    # Append the data to lists
    authors.append(author)
    dates.append(date)
    comment_texts.append(comment_text)

# Create a DataFrame to store the extracted information
data = {'Author': authors, 'Date': dates, 'Comment': comment_texts}
df = pd.DataFrame(data)

df.to_csv('agile_reviews.csv', index=False)
