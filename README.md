# BooksDataExtraction-v2
This python project is designed to scrape book details from the "Books to Scrape" website. It fetches information such as the title, price, availability, description, category, review rating, and an image of each book.

 Features
- Scrape Book Details
- Image Download
- Category-wise Scraping
- CSV Export

 Requirements
- Python 3.x
- Libraries: requests, bs4 (BeautifulSoup), csv, os

 Usage

Set up a Python Virtual Environment:
# Book Scraper

This Python project is designed to scrape book details from the "Books to Scrape" website. It fetches information such as the title, price, availability, description, category, review rating, and an image of each book.

 Features
- Scrape Book Details
- Image Download
- Category-wise Scraping
- CSV Export

 Requirements
- Python 3.x
- Libraries: requests, bs4 (BeautifulSoup), csv, os

 Usage

Set up a Python Virtual Environment:

1. Ensure Python 3.x is installed:
   - If you don't have Python installed, download and install it from the [official Python website](https://www.python.org/downloads/).
   - During installation, make sure to check the box that says "Add Python to PATH."

2. Open a Terminal or Command Prompt:
   - Open the terminal or command prompt on your machine. You can do this by searching for "Terminal" on Mac/Linux or "Command Prompt" on Windows.

3. Navigate to the Project Directory:
   - Use the cd command to navigate to the directory where you have saved the project files.

4. Create a Virtual Environment:
   - Run the following command to create a virtual environment named "venv":

     `bash
     python -m venv venv
     `
5. Activate the Virtual Environment:
   - On Windows, run:

     `bash
     .\venv\Scripts\activate
     `

   - On Mac/Linux, run:

     `bash
     source venv/bin/activate
     `

# Install Required Libraries:

Run the following command to install the necessary libraries:

`bash
pip install -r requirements.txt                         Run the python scraper_script.py in a python environment.
The script will automatically create directories for storing CSV files and images.

Scraped data will be saved in CSV files within the book_categories directory.
Downloaded images will be saved in the book_images directory.
