# required libraries
import streamlit as st
import pandas as pd
from recommender import SHLRecommender   # custom recommender class
from utils import fetch_text_from_url, clean_text  # helper functions

# Configure the Streamlit page
st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")

# App title and description
st.title("SHL Assessment Recommender")
st.write(
    "Enter a job description or a JD URL. "
    "Get 5–10 relevant individual assessments, balanced across technical and behavioral where applicable."
)

# recommender system
reco = SHLRecommender()

# Create two tabs: one for raw JD text, one for JD URL
tab1, tab2 = st.tabs(["JD text", "JD URL"])

# -------------------------------
# TAB 1: User pastes job description text
# -------------------------------
with tab1:
    # Text area for job description input
    jd_text = st.text_area("Paste job description or recruiter query:")
    
    # Slider to choose number of recommendations (between 5 and 10)
    k = st.slider("Number of recommendations (K)", 5, 10, 10)
    st.write("Click On Below Button For Result And Scroll Up")
    # Button to trigger recommendation from text
    if st.button("Recommend from text"):
        if jd_text.strip():  # Ensure text is not empty
            # Call recommender with the provided text
            results = reco.recommend(jd_text, k=k, diversify=True)
            
            # Display results in a dataframe
            st.write("### Recommended Assessments")
            st.dataframe(results.reset_index(drop=True))
        else:
            # Show warning if no text was entered
            st.warning("Please paste some text"
                       "OR"
                       "Kindly Remove URL From Input Box And Than Try Again")

# -------------------------------
# TAB 2: User provides a JD URL
# -------------------------------
with tab2:
    # Input field for job description URL
    jd_url = st.text_input("Enter JD URL (publicly accessible):")
    
    # Separate slider for number of recommendations in this tab
    k2 = st.slider("Number of recommendations (K)", 5, 10, 10, key="k2")
    st.write("Click On Below Button For Result And Scroll Up")
    # Button to trigger recommendation from URL
    if st.button("Recommend from URL"):
        if jd_url.strip():  # Ensure URL is not empty
            # Fetch and clean text from the given URL
            text = fetch_text_from_url(jd_url)
            text = clean_text(text)
            
            # Validate that enough text was extracted
            if len(text) < 200:
                st.warning(
                    "Could not extract enough text from the URL. "
                    "Please try another link or paste the JD text."
                    "OR"
                    "Kindly Remove Text From Input Box And Than Try Again"
                )
            else:
                # Call recommender with the extracted text
                results = reco.recommend(text, k=k2, diversify=True)
                
                # Display results in a dataframe
                st.write("### Recommended Assessments")
                st.dataframe(results.reset_index(drop=True))
        else:
            # Show warning if no URL was entered
            st.warning("Please enter a JD URL."
                       "OR"
                       "Kindly Remove Text From Input Box And Than Try Again")
