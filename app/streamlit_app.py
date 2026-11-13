
import sys
from pathlib import Path

import pandas as pd
import streamlit as st



from src.functions import (
    load_matching_model,
    match_jobs,
    extract_text_from_pdf,
    filter_jobs
)

# Make the project root accessible for imports
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))



st.title("💼 JobMatch AI")
st.write("Find jobs that match your skills and experience.")


# Load model only once
@st.cache_resource
def get_model():
    return load_matching_model()


# Load saved job listings
@st.cache_data
def get_jobs():
    return pd.read_csv(ROOT / "data/raw/jobs.csv")


# User input
st.subheader("Your experience")


input_method = st.radio(
    "How would you like to provide your experience?",
    ["Write a description", "Upload CV (PDF)"]
)

candidate_text = ""

if input_method == "Write a description":

    candidate_text = st.text_area(
        "Describe your skills and experience:",
        height=180,
        placeholder="I have experience with Python, SQL, machine learning..."
    )

else:

    uploaded_cv = st.file_uploader(
        "Upload your CV",
        type=["pdf"]
    )

    if uploaded_cv is not None:

        try:
            candidate_text = extract_text_from_pdf(uploaded_cv)

            if candidate_text:
                st.success("CV text extracted successfully!")

                with st.expander("Preview extracted CV text"):
                    st.text(candidate_text[:3000])
            else:
                st.warning(
                    "No text found in the PDF. "
                    "Please try a text-based PDF."
                )

        except Exception as e:
            st.error(f"Could not read PDF: {e}")

top_n = st.slider(
    "Number of recommendations",
    min_value=5,
    max_value=10,
    value=5
)

st.subheader("Job preferences")

preferred_location = st.text_input(
    "Preferred location",
    value="Frankfurt",
    placeholder="e.g. Frankfurt, Berlin, Munich"
)

work_arrangement = st.selectbox(
    "Work arrangement",
    ["Any", "Remote", "Hybrid", "On-site"]
)

# Search button
if st.button("Find matching jobs", type="primary"):

    if not candidate_text.strip():
        st.warning("Please describe your experience first.")

    else:
        with st.spinner("Finding your best matches..."):

                model = get_model()
                jobs = get_jobs()

                filtered_jobs = filter_jobs(
                    jobs,
                    preferred_location,
                    work_arrangement
                )

                if filtered_jobs.empty:
                    st.warning(
                        "No jobs found with these filters. "
                        "Try a different location or work arrangement."
                    )
                    st.stop()

                results = match_jobs(
                    candidate_text,
                    filtered_jobs,
                    model,
                    top_n=top_n
                )

        st.success(f"Found {len(results)} matching jobs!")

        for _, job in results.iterrows():

            with st.container(border=True):

                st.subheader(job["title"])

                st.write(f"**Company:** {job['company']}")
                st.write(f"**Location:** {job['location']}")

                st.write(job["description"])

                st.caption(
                    f"Semantic similarity: {job['match_score']:.3f}"
                )

                if pd.notna(job["url"]):
                    st.link_button(
                        "View job",
                        job["url"]
                    )
