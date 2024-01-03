import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_website(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"Error while requesting URL: {e}")
        return None

def extract_data(soup):
    # Modify this function based on the structure of the web page and data needed
    # Example: Extracting all headlines from a news site
    headlines = [h.text for h in soup.find_all('h2')]
    paragraphs = [h.text for h in soup.find_all('p')]
    return [headlines,paragraphs]

def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Data'])
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    url = 'https://www.verton.com.au/'  # Replace with the URL you want to scrape
    soup = scrape_website(url)
    if soup:
        data = extract_data(soup)
        save_to_csv(data[0], 'scraped_headlines.csv')
        save_to_csv(data[1], 'scraped_paragraphs.csv')

if __name__ == '__main__':
    main()