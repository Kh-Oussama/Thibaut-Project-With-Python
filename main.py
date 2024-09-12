import os

PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

from bs4 import BeautifulSoup
from requests_html import HTML, HTMLSession
import numpy as np
import pandas as pd

# URL to scrape
url = "https://news.ycombinator.com/item?id=33384577"

# Initialize an HTML session
session = HTMLSession()
response = session.get(url)


# Render the JavaScript on the page and scroll down to load more content
response.html.render()

# Re-parse the HTML after rendering
soup = BeautifulSoup(response.html.html, 'html.parser')

# Extract the comments section
comments = soup.select('tr.comtr')

# Initialize a list to store extracted data
data = []

# Loop through each comment
for index, comment in enumerate(comments):
    # Find the author
    author = comment.find('a', class_='hnuser').get_text() if comment.find('a', class_='hnuser') else "N/A"
    # Find the date
    date = comment.find('span', class_='age').get_text() if comment.find('span', class_='age') else "N/A"
    # Find the comment text
    comment_text = comment.find('div', class_='commtext c00').get_text() if comment.find('div',
                                                                                         class_='commtext c00') else "N/A"
    # Append the data to the list as a dictionary
    data.append({
        "Author": author,
        "Publication Date": date,
        "Review": comment_text
    })

    # Print the extracted information
    print(f"Box {index + 1} content:")
    print(f"Author: {author}")
    print(f"Publication Date: {date}")
    print(f"Review:\n{comment_text}")
    print("-" * 50)

# Convert the list of dictionaries into a pandas DataFrame
df = pd.DataFrame(data)

# Export the DataFrame to CSV and Excel files
df.to_csv('scraped_data_second_4.csv', index=False)
df.to_excel('scraped_data_second_4.xlsx', index=False)

print("Data has been saved to CSV and Excel files.")