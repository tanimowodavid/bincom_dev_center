# ====================================================
# Question 1: Scrape books from [All products | Books to Scrape - Sandbox](https://books.toscrape.com/)
# Scrape the first 5 pages (20 books per page)
# ====================================================

import requests
from bs4 import BeautifulSoup
import time
import csv
from typing import Dict

# Base URL of the website
BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-{}.html"

def scrape_book_details(book_url: str) -> Dict[str, str] | None:
    """
    Navigates to an individual book's page and extracts detailed information.
    """
    response = requests.get(book_url)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. Book Name / Title
    # Found inside the main product gallery h1 tag
    title_tag = soup.find('h1')
    if title_tag is not None:
        title: str = title_tag.text.strip()
    else:
        title: str = "Title not found"

    # 2. Price
    # Found inside a paragraph tag with class 'price_color'
    price_tag = soup.find('p', class_='price_color')
    if price_tag is not None:
        price: str = price_tag.text.strip()
    else:
        price: str = "Price not found"

    # 3. Stock Status
    # Found inside a paragraph tag with class 'instock availability'
    stock_tag = soup.find('p', class_='instock availability')
    if stock_tag is not None:
        stock_text: str = stock_tag.text.strip()
    else:
        stock_text: str = "Stock status not found"

    # 4. Rating
    # The rating is stored as a class name (e.g., "star-rating Three")
    rating_tag = soup.find('p', class_='star-rating')
    # Get the second class name which represents the actual words (One, Two, Three, etc.)
    rating: str = rating_tag['class'][1] if rating_tag else "No Rating"
    
    # 5. Description
    # The description paragraph is directly after a div with ID 'product_description'
    desc_tag = soup.find('div', id='product_description')
    if desc_tag is not None:
        description: str = desc_tag.find_next('p').text.strip()
    else:
        description: str = "No description available"

    # 6. Category
    # Found in the breadcrumb navigation links at the top
    breadcrumb = soup.find('ul', class_='breadcrumb')
    category: str = breadcrumb.find_all('li')[2].text.strip() if breadcrumb else "Unknown"
    
    # 7. Product Information Table
    # Traverses the table rows (tr) to find specific data matching headers (th)
    product_info: Dict[str, str] = {}
    table_rows = soup.find_all('tr')
    for row in table_rows:
        header = row.find('th').text.strip()
        value = row.find('td').text.strip()
        product_info[header] = value
        
    # Extracting keys from product info table safely
    upc: str = product_info.get("UPC", "N/A")
    product_type: str = product_info.get("Product Type", "N/A")
    reviews: str = product_info.get("Number of reviews", "N/A")

    return {
        "Book Name": title,
        "Price": price,
        "Stock Status": stock_text,
        "Rating": rating,
        "Description": description,
        "Category": category,
        "UPC": upc,
        "Product Type": product_type,
        "Number of Reviews": reviews
    }

def main():
    all_books_data = []
    
    print("Starting scraping process for 5 pages...")
    
    # Loop through the first 5 pages
    for page_num in range(1, 6):
        print(f"Scraping Page {page_num}...")
        page_url = START_URL.format(page_num)
        
        response = requests.get(page_url)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_num}")
            continue
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all article items with class 'product_pod' (this holds each book on the listing page)
        books = soup.find_all('article', class_='product_pod')
        
        for book in books:
            # Extract the partial link to the book's individual page
            relative_link = book.find('h3').find('a')['href']
            
            # Clean up the URL format because links on sub-pages look like '../../book_name/index.html'
            clean_link = relative_link.replace('../../../', '').replace('../', '')
            full_book_url = BASE_URL + clean_link
            
            # Scrape deep details from the book's page
            book_details = scrape_book_details(full_book_url)
            
            if book_details:
                all_books_data.append(book_details)
                
            # Sleep for a fraction of a second to avoid overwhelming the server
            time.sleep(0.2)

    # Save the gathered data into a clean CSV file
    csv_columns = ["Book Name", "Price", "Stock Status", "Rating", "Description", "Category", "UPC", "Product Type", "Number of Reviews"]
    csv_file = "scraped_books.csv"
    
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in all_books_data:
                writer.writerow(data)
        print(f"Success! Data for {len(all_books_data)} books saved to '{csv_file}'.")
    except IOError:
        print("I/O error occurred while writing CSV.")

if __name__ == "__main__":
    main()