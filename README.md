# JobMatch AI

**CV-to-job matching with NLP | Ironhack Data Science & Machine Learning — Final Project 3**

JobMatch AI is a Streamlit prototype that recommends job vacancies based on a candidate's skills and experience. Users can paste an experience summary or upload a text-based PDF CV, choose a location and work-arrangement preference, and review the top 5–10 matches with links to the original vacancies.

> **Scope:** This is a job-*relevance* recommender, not a hiring-probability estimator. Similarity scores do not predict whether an employer will invite or hire a candidate.

## Problem and users

**Target users:** Job seekers exploring software engineering, data, AI/ML, cloud, analytics, and technical-support roles.

**Question:** Given a candidate profile and a collection of vacancies, which jobs should the candidate review first?

Traditional keyword search can miss related roles that use different terminology. The project compares lexical, semantic, and zero-shot methods to see whether semantic matching ranks suitable jobs more effectively.

## What the app does

- Accepts a free-text description **or** a PDF CV and extracts text locally with PyMuPDF.
- Uses a pretrained multilingual Sentence Transformer to rank vacancies by semantic similarity.
- Allows selection of **5–10 recommendations**.
- Filters by a preferred location string and by work arrangement (**Any, Remote, Hybrid, On-site**).
- Shows title, company, location, description excerpt, similarity score, and a link to view the vacancy.
- Uses a saved CSV snapshot for the demo; it does **not** require an Adzuna API request for each recommendation.

**Current filter limitations:** Location filtering matches text in a saved location field rather than geographic distance. Work arrangement is inferred from keywords in titles/descriptions, so it is not verified; an unmentioned arrangement is *unknown*, not necessarily on-site. Saved jobs may be outdated.

**PDF limitation:** Only text-based PDFs are supported; scanned/image-only PDFs require OCR, which is outside this version's scope.

## Architecture

```text
Adzuna API → download_data.py → data/raw/jobs.csv
                                      ↓
User text / PDF → text extraction → optional filters → multilingual embeddings
                                                        ↓
                                             cosine similarity ranking
                                                        ↓
                                                Streamlit top 5–10
```

The Streamlit app is in `app/streamlit_app.py`; reusable extraction, filtering, and ranking functions are in `src/functions.py`.

## Data

**Source:** [Adzuna Jobs API](https://developer.adzuna.com/overview) (German endpoint, Frankfurt-area searches).

- **162 unique job listings** collected from several search keywords, including Python, Data Scientist, Machine Learning, Backend Developer, Data Analyst, Tableau, software engineering, cloud engineering, and technical support.
- Listings were de-duplicated by **Adzuna job ID**, not by near-identical text.
- Main fields: `id`, `title`, `company`, `location`, `description`, `url`, `search_keyword`.
- The original collection showed no missing values in the inspected fields; descriptions were approximately **500 characters**, limiting how much of a job's requirements can be observed.
- A fixed **28-job evaluation subset** was selected for reproducible comparison of approaches.
- Five fictional candidate profiles represent ML engineering, backend development, data analysis, cloud engineering, and technical support.
- Each of the **140 profile–job pairs** was assigned an ordinal relevance label: `0` = not relevant, `1` = partially relevant, `2` = highly relevant. The final labels were **AI-assisted revisions** of an initial manual pass and should not be described as independently verified human ground truth.

**Data-use note:** Check Adzuna's current API/redistribution terms before committing or publishing downloaded job descriptions. The original Ironhack template ignores `data/raw/` and instructs students not to commit downloaded source data. If you cannot redistribute the data, keep it local and explain that fresh users need API credentials and must regenerate their own snapshot (which may not reproduce the historical evaluation set).

## Three approaches compared

| Approach | Mechanism | Role in project |
|---|---|---|
| **TF-IDF + cosine similarity** | Lexical token weighting and similarity | Baseline |
| **Multilingual Sentence Transformers + cosine similarity** | Pretrained sentence embeddings encode candidate and vacancy text | Selected app approach |
| **Multilingual zero-shot NLI classifier** | Scores the candidate–job pair against strong, partial, and poor match hypotheses | Third experiment |

**Embedding model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.

**Zero-shot model:** `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`. Its three hypothesis scores were reduced to a ranking score using weights `1.0` (strong), `0.5` (partial), and `0.0` (poor). This is a heuristic ranking score, **not a calibrated probability**.

These experiments compare *pretrained retrieval and classification approaches*. They do not train a supervised classifier on the 140 labels. Clarify with the instructor whether this interpretation satisfies the **model track** requirement for a trained model.

## Evaluation design

All approaches were ranked on the **same 28 fixed jobs × 5 profiles**. Relevance was assessed at the candidate–job-pair level rather than inferred from search keywords.

- **Precision@5:** Fraction of the first five results with relevance label `2` (highly relevant).
- **nDCG@5:** Measures ranking quality using graded relevance labels `0`, `1`, and `2`.
- Reported aggregates are **means across five profiles**; nDCG standard deviation reflects variation across those profiles, not statistical uncertainty over a representative population.

### Results

| Model | Mean Precision@5 | Mean nDCG@5 | SD of nDCG@5 |
|---|---:|---:|---:|
| **Sentence Transformers** | **0.44** | **0.781** | **0.142** |
| TF-IDF | 0.24 | 0.675 | 0.302 |
| Zero-shot NLI | 0.08 | 0.242 | 0.232 |

Sentence Transformers had the highest measured performance on this small curated evaluation set and was chosen for the application. Compared with TF-IDF, mean Precision@5 increased by **0.20 absolute** and nDCG@5 by **0.106 absolute**.

**Cost/performance:** The zero-shot model took **2,156.71 seconds (~35 min 57 sec)** on CPU to score 140 pairs (about **15.4 seconds/pair** in that run), excluding any earlier model download. TF-IDF and Sentence Transformer timing should be measured and reported separately for a complete apples-to-apples runtime comparison; pretrained-model loading, corpus embedding, and per-query inference are different operations. Model artifact sizes have **not yet been measured**.

### Error analysis

Sentence Transformers returned **seven label-0 jobs in the combined top-five rankings** (25 recommendations across five profiles). Examples include:

- A technical-support listing ranked for a backend developer.
- A .NET software-engineering role ranked for a cloud engineer.
- A junior data-analyst role ranked for an ML engineer.
- An upskilling/training advertisement ranked as a job vacancy.

Likely failure modes include occupational overlap without role fit, misleading/truncated descriptions, and the absence of explicit checks for vacancy type, seniority, and required skills. The 28-job evaluation set can contain duplicate-like ads, and its curated composition is not representative of all vacancies.

**Evaluation limitation:** The same fixed subset was used during exploration and final comparison, and AI-assisted labels were reviewed after earlier model results were known. Therefore the reported scores are **exploratory validation results, not an untouched held-out test score**. This is a gap against the stricter Ironhack model-track rubric; a truly independent test set and predeclared labeling rules would be needed before claiming rigorous generalization.

## Repository structure

```text
.
├── README.md
├── RUBRIC.md
├── requirements.txt
├── download_data.py
├── .env.example
├── app/
│   └── streamlit_app.py
├── src/
│   └── functions.py
├── notebooks/
│   ├── 01_framing_and_baseline.ipynb
│   ├── 02_build.ipynb
│   └── 03_evaluate.ipynb
├── data/
│   ├── raw/                       # Local Adzuna snapshot, if permitted
│   ├── candidate_profiles.json
│   ├── evaluation_jobs.csv
│   ├── relevance_labels_reviewed.csv
│   ├── zero_shot_scores.csv
│   └── results/
└── models/                      # Optional cached/saved artifacts
```

Some data or result files may be local-only depending on `.gitignore` and redistribution permissions. Confirm file names and availability before submission.

## Run locally

**Requirements:** Python 3.11 recommended, Git, internet connection for the initial Hugging Face model download. CPU is sufficient for the Streamlit semantic-matching app; full zero-shot evaluation is substantially slower.

On Windows PowerShell, from a fresh clone:

```powershell
git clone https://github.com/YOUR_USERNAME/jobmatch-ai.git
cd jobmatch-ai
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**Data setup:** The app currently reads `data/raw/jobs.csv`. If the file is not included in the clone, create a `.env` file (never commit it):

```dotenv
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

Then run:

```powershell
python download_data.py
```

Adzuna calls may be rate-limited or billable under your plan. This command retrieves *current* jobs and will not reconstruct the exact 162-job historical snapshot. To reproduce the reported evaluation metrics exactly, you need the original fixed evaluation data and saved score artifacts, subject to sharing rights.

Launch the app:

```powershell
python -m streamlit run app/streamlit_app.py
```

For the notebooks:

```powershell
python -m jupyter lab
```

Run notebooks in order: `01_framing_and_baseline.ipynb`, `02_build.ipynb`, `03_evaluate.ipynb`. Reusing the saved `zero_shot_scores.csv` avoids repeating the long inference run. Notebook 03 should report its conclusions and limitations independently.

## Reproducibility and safety

- Keep `.env`, `.venv/`, cached model weights, and user-uploaded CVs out of Git.
- The app extracts PDF text in memory; it does not intentionally persist the uploaded CV to disk.
- Model downloads and live Adzuna search require network access; scoring saved jobs does not require Adzuna calls.
- Fix and record package versions, model revisions, and dataset snapshots for stronger reproducibility.
- Before submitting, verify a fresh clone starts the Streamlit app and reproduces the notebook results when the required local data is supplied.
- Treat recommendations as browsing assistance; applicants should verify actual requirements, location, work arrangement, and vacancy status at the original listing.

## Future improvements

- Add explicit vacancy-type, seniority, and required-skill filters; exclude training advertisements.
- Replace location-string matching with geographic-distance filtering and structured remote/hybrid metadata.
- Detect near-duplicate ads and diversify recommendations.
- Evaluate on a larger, independently labeled and held-out test set, with additional real candidate profiles where consent permits.
- Explore occupation taxonomies (e.g., ESCO) and aggregated career-transition data without inferring hiring probabilities.
- Cache job embeddings and add live Adzuna refresh with call-budget controls.

## Presentation

Ironhack's suggested format is **7 minutes of slides + 3 minutes of live Streamlit demo**. Add a link to the final slides here when they are created.

---

*Educational prototype for Ironhack Project 3. Not a production recruitment decision system.*


## How to run streamlit:
python -m streamlit run app/job_search.py 
