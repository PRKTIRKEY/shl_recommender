# required libraries
import requests
from bs4 import BeautifulSoup

def fetch_text_from_url(url: str, timeout: int = 10) -> str:
    """
    Fetching and extracting readable text content from a given URL.
    
    Parameters:
    - url: the webpage URL to fetch
    - timeout: request timeout in seconds (default = 10)
    
    Returns:
    - Cleaned text extracted from the webpage, or an empty string if request fails
    """
    try:
        # Sends GET request with a user-agent header to avoid blocking
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()  # Raising exception if status code is not 200

        # Parsing HTML content with BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")

        # Removing non-content tags (script, style, noscript)
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        # Extracting visible text, normalize whitespace
        text = " ".join(soup.get_text(separator=" ").split())
        return text
    except Exception:
        # Returns empty string if any error occurs (e.g., timeout, invalid URL)
        return ""

def clean_text(txt: str) -> str:
    """
    Cleaning and normalizeing text by stripping whitespace and collapsing multiple spaces.
    
    Parameters:
    - txt: input text string
    
    Returns:
    - Cleaned text string
    """
    return " ".join((txt or "").strip().split())

def categorize_query(text: str) -> dict:
    """
    Categorizesing a query into different intent types based on keyword matching.
    
    Parameters:
    - text: input query string
    
    Returns:
    - Dictionary with boolean flags for each category:
      { "technical": True/False, "behavioral": True/False, ... }
    """
    t = text.lower()  # Converting to lowercase for case-insensitive matching
    return {
        # intents
        "technical": any(k in t for k in ["developer", "engineer", "coding", "java", "python", "sql", "data", "cloud"]),
        "behavioral": any(k in t for k in ["collaborat", "team", "communication", "stakeholder", "leadership", "culture"]),
        "cognitive": any(k in t for k in ["reasoning", "analytical", "problem solving", "aptitude"]),
        "language": any(k in t for k in ["english", "verbal", "writing"]),
        "domain": any(k in t for k in ["finance", "sales", "marketing", "hr", "support"])
    }
