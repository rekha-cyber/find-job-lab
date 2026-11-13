
import streamlit as st

st.title("💼 JobMatch AI")
st.subheader("From CV to Career Opportunities")

st.markdown("""
### The Problem

Finding relevant job vacancies can be time-consuming.

Traditional keyword-based job searches often:
- Miss relevant jobs that use different terminology.
- Return positions requiring different skills.
- Provide limited personalization based on a candidate's experience.

### Our Solution

JobMatch AI recommends vacancies based on a candidate's
skills and professional experience.

Users can:
- Upload a PDF CV or describe their experience.
- Specify their preferred location.
- Choose remote, hybrid, or on-site work.
- Receive their top 5–10 matching job vacancies.

### Our Research Question

**Can semantic matching improve job recommendations
compared with traditional keyword-based matching?**
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Job Listings", "162")

with col2:
    st.metric("ML Approaches", "3")

with col3:
    st.metric("Best nDCG@5", "0.781")

st.info(
    "The project compares TF-IDF, Sentence Transformers, "
    "and zero-shot classification using a fixed evaluation dataset."
)
