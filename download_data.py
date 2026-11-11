
import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Three searches = three API calls
# KEYWORDS = ["Python", "Data Scientist", "Machine Learning"]

KEYWORDS = [
    "Backend Developer",
    "Data Analyst",
    "Computer programmer",
    "Tableau",
    "Technical support specialists",
    "Software engineers",
    "Cloud engineers"
]

def download_jobs():
    if not APP_ID or not APP_KEY:
        raise ValueError("Adzuna credentials missing from .env")

    all_jobs = []

    for keyword in KEYWORDS:
        print(f"Searching for: {keyword}")

        url = "https://api.adzuna.com/v1/api/jobs/de/search/1"

        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": keyword,
            "where": "Frankfurt",
            "distance": 50,
            "results_per_page": 20,
        }

        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()

        jobs = response.json().get("results", [])

        for job in jobs:
            all_jobs.append({
                "id": job.get("id"),
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "description": job.get("description"),
                "url": job.get("redirect_url"),
                "search_keyword": keyword,
            })
            
    new_df = pd.DataFrame(all_jobs)
    if new_df.empty:
        print("No new jobs found.")
        return pd.DataFrame()

    output = Path("data/raw/jobs.csv")

    # Load existing jobs if available
    if output.exists():
        existing_df = pd.read_csv(output, dtype={"id": str})
        print(f"Existing jobs: {len(existing_df)}")

        # Combine old and new jobs
        df = pd.concat(
            [existing_df, new_df],
            ignore_index=True
        )
    else:
        df = new_df

    # Remove duplicates using Adzuna job IDs
    df["id"] = df["id"].astype(str)
    df = df.drop_duplicates(subset=["id"], keep="first")

    # Save updated dataset
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)

    print(f"New jobs retrieved: {len(new_df)}")
    print(f"Total unique jobs: {len(df)}")

    return df


if __name__ == "__main__":
    download_jobs()
