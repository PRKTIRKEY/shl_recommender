# required libraries
import os
import pandas as pd
import requests

def validate_and_clean(input_path="shl_assessments.csv", output_path="shl_assessments_clean.csv"):
    # Step 1: Ensuring the output folder exists
    # os.makedirs will create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Step 2: Loading the dataset from CSV
    df = pd.read_csv(input_path)

    # Step 3: Removing duplicate rows
    # First droping duplicates based on "Name"
    df = df.drop_duplicates(subset=["Name"])
    # Then droping duplicates based on "URL"
    df = df.drop_duplicates(subset=["URL"])

    # Step 4: Removing rows missing critical fields (Name or URL)
    df = df.dropna(subset=["Name", "URL"])

    # Step 5: Normalizing text fields
    # Strip whitespace from Name and URL
    df["Name"] = df["Name"].str.strip()
    df["URL"] = df["URL"].str.strip()
    # Filling missing Category with "Other" and strip whitespace
    df["Category"] = df["Category"].fillna("Other").str.strip()
    # Filling missing Description with empty string and strip whitespace
    df["Description"] = df["Description"].fillna("").str.strip()

    # Step 6: Validating URLs by sending HEAD requests
    valid_urls = []
    for url in df["URL"]:
        try:
            # Trying to reach the URL with a short timeout
            r = requests.head(url, timeout=5, allow_redirects=True)
            # Marking as valid if status code is 200
            valid_urls.append(r.status_code == 200)
        except Exception:
            # If request fails, mark as invalid
            valid_urls.append(False)

    # Adding validation results to DataFrame
    df["ValidURL"] = valid_urls
    # Keeping only rows with valid URLs
    df = df[df["ValidURL"]]

    # Step 7: Saving cleaned dataset to absolute path
    abs_output_path = os.path.abspath(output_path)
    df.to_csv(abs_output_path, index=False)

    # Step 8: Printing summary message
    print(f"Cleaned catalog saved to {abs_output_path} with {len(df)} assessments.")

    # Return the absolute path of the cleaned file
    return abs_output_path

# Entry point: runs validate_and_clean if script is executed directly
if __name__ == "__main__":
    validate_and_clean()
