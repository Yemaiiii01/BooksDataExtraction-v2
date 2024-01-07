# Main Python script for scraping
import requests
from bs4 import BeautifulSoup
import csv
import os


# Function to download an image from a URL
def download_image(image_url, folder_path, book_title):
    # Make a GET request to fetch the raw image data
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        # Clean/replace characters that are invalid for file names
        safe_title = "".join([c for c in book_title if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
        # Create the image file path
        image_file_path = os.path.join(folder_path, f'{safe_title}.jpg')
        with open(image_file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return image_file_path
    else:
        print(f"Failed to retrieve image from {image_url}")


# Function to scrape book details
def scrape_book_details(url, image_folder_path):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the required details
    product_details = {
        'product_page_url': url,
        'universal_product_code': soup.find('th', text='UPC').find_next_sibling('td').text,
        'title': soup.find('div', class_='product_main').h1.text,
        'price_including_tax': soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text,
        'price_excluding_tax': soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text,
        'quantity_available': soup.find('th', text='Availability').find_next_sibling('td').text,
        'product_description': soup.find('meta', attrs={'name': 'description'})['content'].strip(),
        'category': soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip(),
        'review_rating': soup.find('p', class_='star-rating')['class'][1],
        'image_url': soup.find('img')['src'].replace('../../', 'http://books.toscrape.com/')
    }

    # Download the image
    product_details['image_file_path'] = download_image(product_details['image_url'], image_folder_path,
                                                        product_details['title'])

    return product_details


# Function to fetch book URLs from a single category, including pagination
def fetch_book_urls(category_url):
    book_urls = []
    while True:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.select('h3 > a')
        for book in books:
            book_url = book['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
            book_urls.append(book_url)

        # Check for a 'next' button for pagination
        next_button = soup.select_one('li.next > a')
        if next_button:
            next_page_url = next_button['href']
            category_url = '/'.join(category_url.split('/')[:-1]) + '/' + next_page_url
        else:
            break
    return book_urls


# Function to extract all categories
def extract_categories(main_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    category_links = soup.select('ul.nav-list > li > ul > li > a')
    categories = {cat.text.strip(): main_url + cat['href'] for cat in category_links}
    return categories


# The main URL of 'Books to Scrape'
main_url = 'http://books.toscrape.com/'

# Extract all categories
categories = extract_categories(main_url)

# Directory to store CSV files
csv_dir = 'book_categories'
os.makedirs(csv_dir, exist_ok=True)

# Directory to store book images
image_dir = 'book_images'
os.makedirs(image_dir, exist_ok=True)

# Process each category
for category_name, category_url in categories.items():
    # Fetch book URLs for the category
    book_urls = fetch_book_urls(category_url)

    # List to store all books' details
    books_data = []

    # Scrape details for each book
    for book_url in book_urls:
        book_details = scrape_book_details(book_url, image_dir)
        books_data.append(book_details)

    # Define the CSV file path for the category
    csv_file_path = os.path.join(csv_dir, f'{category_name.replace("/", "-")}.csv')

    # Save the book details in a CSV file named after the category
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = list(books_data[0].keys())  # Assumes all dictionaries have the same keys
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for book_data in books_data:
            writer.writerow(book_data)

    print(f"Completed category: {category_name}")

print("All categories have been processed.")
