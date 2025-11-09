# required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL of the SHL product catalog page
BASE_URL = "https://www.shl.com/products/product-catalog/"  

# Keyword mapping to assign categories based on text content
CATEGORY_KEYWORDS = {
    "Coding": ["coding", "developer", "programming", "java", "python", "sql"],
    "Knowledge & Skills": ["skills", "knowledge", "competency", "expertise"],
    "Personality & Behavior": ["personality", "behavior", "collaboration", "team", "communication", "leadership"],
    "Cognitive Ability": ["reasoning", "analytical", "problem solving", "aptitude", "logic"],
    "Language": ["english", "verbal", "writing", "language"],
    "Domain-Specific": ["finance", "sales", "marketing", "hr", "support"]
}

def assign_category(text: str) -> str:
    """
    Assigning a category to an assessment based on keywords found in its text.
    If no keywords match, return "Other".
    """
    text = text.lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return cat
    return "Other"

def fetch_page(url):
    """
    Fetching a webpage and return a BeautifulSoup object.
    Includes error handling for failed requests.
    """
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        resp.raise_for_status()  # Raise exception if status code is not 200
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def crawl_catalog(base_url=BASE_URL):
    """
    Crawl the SHL product catalog page to extract assessment information.
    Returns a DataFrame with Name, URL, Category and Description.
    """
    assessments = []
    soup = fetch_page(base_url)
    if not soup:
        return pd.DataFrame()  # Return empty DataFrame if page fetch fails

    # Loop through all anchor tags (links) on the catalog page
    for card in soup.select("a"):
        name = card.get_text(strip=True)  # Extract link text as assessment name
        url = card.get("href")            # Extract link URL

        # Filter only relevant assessment links
        if url and "assessments" in url.lower() and name:
            # Handle relative URLs by prefixing with domain
            if url.startswith("/"):
                url = "https://www.shl.com" + url

            # Initialize description as empty
            desc = ""
            # Fetching detail page for each assessment
            detail_soup = fetch_page(url)
            if detail_soup:
                # Extracting first <p> tag as description (adjust selector if needed)
                desc_tag = detail_soup.select_one("p")
                if desc_tag:
                    desc = desc_tag.get_text(strip=True)

            # Assigning category based on name + description text
            category = assign_category(name + " " + desc)

            # Appending assessment info to list
            assessments.append({
                "Name": name,
                "URL": url,
                "Category": category,
                "Description": desc
            })

            # Polite delay to avoid overwhelming the server
            time.sleep(1)

    # Converting list of assessments to DataFrame
    return pd.DataFrame(assessments)

if __name__ == "__main__":
    # Runing crawler and save results to CSV
    df = crawl_catalog()
    df.to_csv("shl_assessments.csv", index=False)
    print(f"Saved {len(df)} assessments with categories to shl_assessments.csv")
