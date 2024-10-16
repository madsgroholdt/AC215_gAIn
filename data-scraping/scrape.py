import os
import requests
from bs4 import BeautifulSoup

def get_article_content(url):
    try:
        # Send a request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request fails

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content (adjust for different websites)
        # 'p' = paragraphs
        paragraphs = soup.find_all('p')

        title = soup.title.get_text() if soup.title else 'No title found'

        # Extract and combine the text from each paragraph
        content = '\n'.join([para.get_text() for para in paragraphs])

        # Save the content to a text file
        with open(f"/articles/{title}", 'w') as file:
            file.write(content)
        
        print(f"Article saved to {title}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching article: {e}")

# Example usage
url = 'https://www.cnn.com/2024/10/15/politics/early-voting-record-georgia/index.html'
get_article_content(url)