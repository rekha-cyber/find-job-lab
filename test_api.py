import os
import requests
from dotenv import load_dotenv

# Load API credentials
load_dotenv()

app_id = os.getenv("ADZUNA_APP_ID")
app_key = os.getenv("ADZUNA_APP_KEY")

# Search for jobs in Germany
url = "https://api.adzuna.com/v1/api/jobs/de/search/1"

params = {
    "app_id": app_id,
    "app_key": app_key,
    "what": "Python Developer",
    "where": "Frankfurt",
    "results_per_page": 5
}

response = requests.get(url, params=params, timeout=20)
response.raise_for_status()

data = response.json()

# Display job titles
for job in data.get("results", []):
    print(job["title"])