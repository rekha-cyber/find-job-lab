import pandas as pd

from src.functions import load_matching_model, match_jobs

jobs = pd.read_csv("data/raw/jobs.csv")

candidate = """
Python developer with experience in SQL,
machine learning, Pandas, and REST APIs.
"""

model = load_matching_model()

results = match_jobs(
    candidate_text=candidate,
    jobs=jobs,
    model=model,
    top_n=5
)

print(results[["title", "match_score"]])