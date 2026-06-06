# ==============================
# Question 3: Build a scraper that will scrape a random page from Wikipedia
# ==============================

import requests
from bs4 import BeautifulSoup

# The special URL that forces Wikipedia to redirect us to a random page
RANDOM_WIKI_URL = "https://en.wikipedia.org/wiki/Special:Random"

def scrape_random_wikipedia_page():
    print("Connecting to Wikipedia to fetch a random page...")

    # Define headers to look like a real browser so wikipedia doesn't block our request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    
    response = requests.get(RANDOM_WIKI_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to access Wikipedia. Status code: {response.status_code}")
        return

    # This property reveals the final destination URL after the redirect
    final_url = response.url
    print(f"Successfully redirected to: {final_url}\n")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the Main Article Title
    title_tag = soup.find('h1', id='firstHeading')
    title = title_tag.text.strip() if title_tag else "Title Not Found"
    
    print(f"TITLE: {title}")
    print("=" * len(title))  # Prints a neat underline matching the title length
    
    # Extract the Main Content / Article Summary
    content_div = soup.find('div', class_='mw-parser-output')
    
    if content_div:
        # Find all direct paragraph (<p>) tags inside the content div
        paragraphs = content_div.find_all('p', recursive=False)
        
        paragraphs_printed = 0
        
        for p in paragraphs:
            # Clean the paragraph text
            p_text = p.text.strip()
            
            # Skip empty paragraphs or coordinates boxes that Wikipedia sometimes formats as <p>
            if not p_text:
                continue
                
            print(p_text)
            print()  # Add an extra newline between paragraphs for readability
            
            paragraphs_printed += 1
            # We stop after printing 2 valid paragraphs so we don't dump a massive wall of text
            if paragraphs_printed >= 2:
                break
                
        if paragraphs_printed == 0:
            print("Could not extract clean text paragraphs from this page template.")
    else:
        print("Error: Could not locate the primary article body element.")

if __name__ == "__main__":
    scrape_random_wikipedia_page()