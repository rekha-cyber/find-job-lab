
import streamlit as st

st.title("🧠 Data & Methods")
st.write("How we built and compared three job-matching approaches.")

# DATA SECTION
st.header("1. Data Collection")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Job Listings", "162")

with col2:
    st.metric("Candidate Profiles", "5")

with col3:
    st.metric("Evaluation Jobs", "28")

st.markdown("""
**Data source:** Adzuna API

We collected job advertisements from Frankfurt and
surrounding areas using searches for:

- Python, AI and Machine Learning
- Backend and Software Development
- Data Analysis and Business Intelligence
- Cloud Engineering and Technical Support

After removing duplicate job IDs, we retained
162 unique vacancies.

**Data limitation:** Job descriptions are approximately
500 characters long, so some important requirements
may be missing.
""")

st.divider()

# METHODS SECTION
st.header("2. Three Matching Approaches")

tab1, tab2, tab3 = st.tabs([
    "TF-IDF",
    "Sentence Transformers",
    "Zero-Shot"
])

with tab1:
    st.subheader("TF-IDF + Cosine Similarity")

    st.markdown("""
    **Traditional keyword-based approach**

    - Converts text into weighted word-frequency vectors.
    - Compares candidate and job descriptions using cosine similarity.
    - Fast and computationally inexpensive.
    - Limited when similar concepts use different words.

    **Role:** Baseline model
    """)

with tab2:
    st.subheader("Sentence Transformers")

    st.markdown("""
    **Semantic matching**

    - Uses pretrained multilingual sentence embeddings.
    - Captures relationships between words and concepts.
    - Supports German and English job descriptions.
    - Ranks jobs using cosine similarity.

    **Model:** `paraphrase-multilingual-MiniLM-L12-v2`

    **Role:** Improved semantic matching approach
    """)

with tab3:
    st.subheader("Zero-Shot Classification")

    st.markdown("""
    **Relevance classification without task-specific training**

    - Evaluates each candidate-job pair.
    - Predicts strong, partial, or poor relevance.
    - Converts classification scores into a ranking score.
    - More computationally expensive.

    **Model:** `mDeBERTa-v3-base-mnli-xnli`

    **Role:** Third comparison approach
    """)

st.divider()

# PIPELINE
st.header("3. Matching Pipeline")

st.graphviz_chart("""
digraph {
    rankdir=LR;
    node [shape=box, style=rounded];

    Candidate [label="CV / Candidate Text"];
    Jobs [label="Adzuna Job Listings"];
    Model [label="NLP Matching Model"];
    Ranking [label="Similarity / Relevance Score"];
    Results [label="Top 5–10 Jobs"];

    Candidate -> Model;
    Jobs -> Model;
    Model -> Ranking;
    Ranking -> Results;
}
""", use_container_width=True)

st.caption(
    "All three approaches were compared using the same "
    "28 evaluation jobs and five fictional candidate profiles."
)
