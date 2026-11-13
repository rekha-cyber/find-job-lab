
import streamlit as st

# Configure the application
st.set_page_config(
    page_title="JobMatch AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Pages appear in the order defined below
pages = [
    st.Page(
        "pages/overview.py",
        title="1. Project Overview",
        icon="🏠",
        default=True
    ),
    st.Page(
        "pages/methods.py",
        title="2. Data & Methods",
        icon="🧠"
    ),
    st.Page(
        "pages/evaluation.py",
        title="3. Model Evaluation",
        icon="📊"
    ),
    st.Page(
        "pages/errors.py",
        title="4. Error Analysis",
        icon="🔍"
    ),
    st.Page(
        "streamlit_app.py",
        title="5. Live Demo",
        icon="💼"
    )
]

# Display sidebar navigation and run the selected page
navigation = st.navigation(
    pages,
    position="sidebar"
)

navigation.run()
