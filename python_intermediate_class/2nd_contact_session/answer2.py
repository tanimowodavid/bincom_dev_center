# ==================================
# Question 2: Scrape 10-20 distinct quote authors from [Quotes to Scrape](https://quotes.toscrape.com/)
# ==================================

import requests
from bs4 import BeautifulSoup
import csv
import time

# Base URLs
BASE_URL = "https://quotes.toscrape.com"
START_URL = "https://quotes.toscrape.com/"

def scrape_author_profile(profile_url):
    """
    Navigates to an author's specific 'about' page and extracts their personal data.
    """
    response = requests.get(profile_url)
    if response.status_code != 200:
        return None
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. Author Name
    name_tag = soup.find('h3', class_='author-title')
    name = name_tag.text.strip() if name_tag else "Unknown"
    
    # 2. Date of Birth
    dob_tag = soup.find('span', class_='author-born-date')
    dob = dob_tag.text.strip() if dob_tag else "Unknown"
    
    # 3. Nationality / Place of Birth
    # The site formats this like "in Ulm, Germany"
    pob_tag = soup.find('span', class_='author-born-location')
    pob = pob_tag.text.strip() if pob_tag else "Unknown"
    # Clean up the "in " prefix if it exists to get a cleaner nationality/location string
    if pob.startswith("in "):
        pob = pob[3:]
        
    # 4. Description
    desc_tag = soup.find('div', class_='author-description')
    description = desc_tag.text.strip() if desc_tag else "No description available."
    
    return {
        "Name": name,
        "Date of Birth": dob,
        "Nationality/Location": pob,
        "Description": description
    }

def main():
    # Using a set to ensure we only store DISTINCT relative URLs for author profiles
    unique_author_links = set()
    TARGET_COUNT = 10
    
    current_url = START_URL
    print("Gathering unique author profile links...")
    
    # Loop to navigate pages until we have enough distinct authors or hit the last page
    while len(unique_author_links) < TARGET_COUNT and current_url:
        response = requests.get(current_url)
        if response.status_code != 200:
            print(f"Failed to fetch page: {current_url}")
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Every quote card has an '(about)' link inside it
        # So we find all <a> tags that contain the text '(about)'
        about_tags = soup.find_all('a', string='(about)')
        
        for tag in about_tags:
            href = tag.get('href')
            if href:
                unique_author_links.add(href)
                # Break early if we hit our target number of authors mid-page
                if len(unique_author_links) >= TARGET_COUNT:
                    break
        
        print(f"Collected {len(unique_author_links)} distinct author links so far.")
        
        # Find the "Next" button to go to the next page of quotes if we need more
        next_button = soup.find('li', class_='next')
        if next_button and next_button.find('a'):
            next_relative_url = next_button.find('a').get('href')
            current_url = BASE_URL + next_relative_url
        else:
            current_url = None  # No more pages left
            
    print(f"\nStep 2: Successfully collected {len(unique_author_links)} distinct links.")
    print("Now scraping deep profile information...")
    
    authors_data = []
    
    # Visit each unique author link to scrape their deep bio details
    for relative_url in unique_author_links:
        full_profile_url = BASE_URL + relative_url
        print(f"Scraping bio from: {full_profile_url}")
        
        profile_data = scrape_author_profile(full_profile_url)
        if profile_data:
            authors_data.append(profile_data)
            
        time.sleep(0.2)  # Polite scraping delay
        
    # Write everything out cleanly to a CSV file
    csv_columns = ["Name", "Date of Birth", "Nationality/Location", "Description"]
    csv_file = "scraped_authors.csv"
    
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in authors_data:
                writer.writerow(data)
        print(f"\nSuccess! Data for {len(authors_data)} distinct authors saved to '{csv_file}'.")
    except IOError:
        print("An error occurred while saving the CSV file.")

if __name__ == "__main__":
    main()


