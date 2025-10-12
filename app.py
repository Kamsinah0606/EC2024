import streamlit as st

st.set_page_config(
    page_title="Scientific Visualization"
)

st.header("Genetic Algorithm", divider="gray")

import streamlit as st
import pandas as pd

# Set the title of the Streamlit application
st.title("Faculty Data Loader and Viewer")
st.markdown("This application loads the 'arts_faculty_data.csv' file from GitHub.")

# Define the URL for the CSV file
url = "https://raw.githubusercontent.com/Kamsinah0606/EC2024/refs/heads/main/arts_faculty_data.csv"

# Use st.cache_data to load the data efficiently
# This prevents the data from being reloaded every time the app updates
@st.cache_data
def load_data(data_url):
    """
    Loads the CSV data from the specified URL into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(data_url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load the DataFrame
df_onlines = load_data(url)

# Check if the data loaded successfully and display it
if df_onlines is not None:
    st.subheader("Raw Data Display")
    st.write(f"DataFrame loaded successfully with **{df_onlines.shape[0]} rows** and **{df_onlines.shape[1]} columns**.")

    # Display the DataFrame using st.dataframe
    st.dataframe(df_onlines)

    # Optionally display a quick summary
    if st.checkbox('Show Data Info'):
        st.subheader("Data Information (`df.info()`)")
        # st.write(df_onlines.info()) # st.info() is not a direct way to show df.info() output
        # A workaround to show info is to print it to a string or show basic stats
        st.code(df_onlines.info(buf=None), language='text')

        st.subheader("Descriptive Statistics (`df.describe()`)")
        st.dataframe(df_onlines.describe())
