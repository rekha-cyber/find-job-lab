
import streamlit as st
import pandas as pd

st.title("📊 Model Evaluation")
st.write("Which matching approach recommends the most relevant jobs?")

# Results from Notebook 3
results = pd.DataFrame({
    "Model": [
        "TF-IDF",
        "Sentence Transformers",
        "Zero-Shot"
    ],
    "Precision@5": [0.24, 0.44, 0.08],
    "nDCG@5": [0.675, 0.781, 0.242],
    "nDCG Std": [0.302, 0.142, 0.232]
})

# Evaluation setup
st.subheader("Evaluation Setup")

col1, col2, col3 = st.columns(3)

col1.metric("Candidate Profiles", "5")
col2.metric("Evaluation Jobs", "28")
col3.metric("Relevance Judgments", "140")

st.caption(
    "Relevance labels: 0 = not relevant, "
    "1 = partially relevant, 2 = highly relevant. "
    "Labels were AI-assisted and require further independent validation."
)

st.divider()

# Main results
st.subheader("Model Performance")

tab1, tab2 = st.tabs(["nDCG@5", "Precision@5"])

with tab1:
    st.markdown(
        "**nDCG@5** measures ranking quality, giving "
        "more importance to highly relevant jobs near the top."
    )

    st.bar_chart(
        results.set_index("Model")[["nDCG@5"]],
        horizontal=True
    )

with tab2:
    st.markdown(
        "**Precision@5** measures the proportion of "
        "top-five recommendations labeled highly relevant."
    )

    st.bar_chart(
        results.set_index("Model")[["Precision@5"]],
        horizontal=True
    )

st.dataframe(
    results.set_index("Model").round(3),
    use_container_width=True
)

st.divider()

# Comparison to baseline
st.subheader("Improvement Over Baseline")

col1, col2 = st.columns(2)

col1.metric(
    "Precision@5 Improvement",
    "+83.3%",
    help="Relative increase from 0.24 to 0.44"
)

col2.metric(
    "nDCG@5 Improvement",
    "+15.7%",
    help="Relative increase from 0.675 to 0.781"
)

st.success(
    "Sentence Transformers achieved the highest "
    "mean Precision@5 and nDCG@5."
)

# Computational cost
st.subheader("Computational Cost")

st.markdown("""
Zero-shot classification required **2,156.71 seconds
(approximately 36 minutes)** to process 140
candidate–job pairs on CPU.

This was substantially more expensive than the
similarity-based approaches in our experiment.

This measurement is inference time, not model training time.
""")

st.divider()

# Conclusions
st.subheader("Model Selection")

st.markdown("""
**Selected model:** `paraphrase-multilingual-MiniLM-L12-v2`

We selected Sentence Transformers because:

- It achieved the highest ranking quality on our evaluation set.
- It supports both German and English text.
- Embeddings can be reused for efficient ranking.
- It is practical for an interactive Streamlit application.

**Evaluation limitations:** The experiment used only five
fictional candidate profiles, a curated sample of 28 jobs,
and AI-assisted relevance labels. The results should be
considered exploratory rather than proof of real-world
recruitment performance.
""")
