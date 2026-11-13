
import streamlit as st
import pandas as pd
from pathlib import Path

st.title("🔍 Error Analysis")
st.write("Where does JobMatch AI struggle, and how could we improve it?")

# Load saved error analysis
ROOT = Path(__file__).resolve().parents[2]

errors_path = ROOT / "data/results/semantic_errors.csv"

if errors_path.exists():
    errors = pd.read_csv(errors_path)
else:
    errors = pd.DataFrame()

# Summary metrics
st.subheader("Incorrect Recommendations")

col1, col2 = st.columns(2)

col1.metric(
    "Irrelevant Top-5 Recommendations",
    "7 / 25"
)

col2.metric(
    "Profiles Evaluated",
    "5"
)

st.caption(
    "Seven of the 25 top-five recommendations were labeled "
    "not relevant in our AI-assisted evaluation dataset."
)

st.divider()

# Error examples
st.subheader("Examples of Model Errors")

examples = [
    {
        "Candidate": "ML Engineer",
        "Recommended Job": "Junior Data Analyst",
        "Problem": "Related data skills, but different responsibilities."
    },
    {
        "Candidate": "ML Engineer",
        "Recommended Job": "Data Management Upskilling",
        "Problem": "Training advertisement rather than a regular vacancy."
    },
    {
        "Candidate": "Cloud Engineer",
        "Recommended Job": ".NET Software Engineer",
        "Problem": "Overlapping technical terms, but different specialization."
    },
    {
        "Candidate": "Technical Support",
        "Recommended Job": "BI / Data Warehouse Developer",
        "Problem": "General IT terminology does not imply matching job responsibilities."
    }
]

st.dataframe(
    pd.DataFrame(examples),
    hide_index=True,
    use_container_width=True
)

# Optional saved errors
if not errors.empty:
    with st.expander("View all detected errors"):
        st.dataframe(
            errors[
                [
                    "profile_id",
                    "title",
                    "semantic_rank",
                    "semantic_score",
                    "relevance"
                ]
            ],
            hide_index=True,
            use_container_width=True
        )

st.divider()

# Limitations
st.subheader("Why Do These Errors Happen?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### Skill Overlap

    Related technical vocabulary does not always
    indicate suitable job responsibilities.
    """)

with col2:
    st.markdown("""
    #### Short Descriptions

    Adzuna provides approximately 500-character
    excerpts, limiting available information.
    """)

with col3:
    st.markdown("""
    #### No Hard Constraints

    The semantic model does not explicitly verify
    seniority or required qualifications.
    """)

st.divider()

# Improvements
st.subheader("Potential Improvements")

st.markdown("""
**1. Vacancy Validation**

Exclude advertisements for courses or training programs
that are not genuine job vacancies.

**2. Structured Skill Matching**

Extract required skills and compare them directly
against the candidate's experience.

**3. Career Transition Data**

Use historical occupation transitions to identify
realistic career paths beyond exact title matching.

**4. Better Job Metadata**

Improve location, work arrangement, seniority,
and employment-type filtering.
""")

st.info(
    "Conclusion: Semantic similarity is useful for ranking, "
    "but it should be combined with structured job requirements "
    "and data validation."
)
