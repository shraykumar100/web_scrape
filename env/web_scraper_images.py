import requests
from bs4 import BeautifulSoup
import os
import pytesseract
from PIL import Image

def download_image(url, folder_name, img_name):
    try:
        # Send a GET request to the image URL
        response = requests.get(url)
        response.raise_for_status()

        image_path = os.path.join(folder_name, img_name)
        text_path = os.path.join(folder_name, img_name.split('.')[0] + '.txt')

        # Save the image file
        with open(image_path, 'wb') as file:
            file.write(response.content)

        # Perform OCR on the image
        try:
            text = pytesseract.image_to_string(Image.open(image_path))
            # Save the extracted text
            with open(text_path, 'w') as file:
                file.write(text)
        except IOError:
            print(f"Cannot identify image file {image_path}. Skipping OCR.")

    except requests.RequestException as e:
        print(f"Error downloading {img_name}: {e}")

def scrape_images(url, folder_name):
    try:
        # Create folder for images if it doesn't exist
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all image tags and download images
        for i, img_tag in enumerate(soup.find_all('img')):
            img_url = img_tag.get('src')
            if img_url:
                # Ensure a valid image URL
                if not img_url.startswith('http'):
                    img_url = url + img_url

                # Download and save each image
                download_image(img_url, folder_name, f"image_{i}.jpg")

        print("Images and texts downloaded successfully.")
    except requests.RequestException as e:
        print(f"Error: {e}")

def main():
    url = 'https://www.achievers.com/blog/company-core-value-examples/'  # Replace with the URL you want to scrape
    folder_name = 'downloaded_images'  # Folder to save images
    scrape_images(url, folder_name)

if __name__ == '__main__':
    main()
