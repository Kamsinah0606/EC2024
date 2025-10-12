import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Scientific Visualization"
)

st.header("Genetic Algorithm", divider="gray")

import streamlit as st
import pandas as pd

# Set the title of the Streamlit application
st.title("Faculty Data Loader and Viewer")
st.markdown("This application loads the 'arts_faculty_data.csv' file from GitHub.")



# --- Configuration ---
st.set_page_config(layout="wide") # Use wide layout for better visualization
st.title("Faculty Data Analysis Dashboard 📊")
st.markdown("This application loads and visualizes the 'arts_faculty_data.csv' file from GitHub.")

# --- Data Loading Function (Optimized with Caching) ---
url = "https://raw.githubusercontent.com/Kamsinah0606/EC2024/refs/heads/main/arts_faculty_data.csv"

@st.cache_data
def load_data(data_url):
    """Loads the CSV data efficiently."""
    try:
        df = pd.read_csv(data_url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load the DataFrame
df_onlines = load_data(url)

# --- Visualization Section ---
if df_onlines is not None:
    st.subheader("Data Overview")
    st.write(f"DataFrame loaded successfully with **{df_onlines.shape[0]} rows** and **{df_onlines.shape[1]} columns**.")

    # You can choose to display the data in an expander for cleanliness
    with st.expander("View Raw Data"):
        st.dataframe(df_onlines)

    # Use a container or column for better layout
    st.markdown("---")
    st.subheader("Gender Distribution Analysis")

    # Check if the 'Gender' column exists before trying to plot
    if 'Gender' in df_onlines.columns:
        # Calculate the counts
        gender_counts = df_onlines['Gender'].value_counts()

        # Create the matplotlib figure
        fig, ax = plt.subplots(figsize=(6, 6)) # Use fig, ax convention for best practice
        ax.pie(
            gender_counts,
            labels=gender_counts.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=['#ff9999', '#66b3ff', '#99ff99'] # Added custom colors
        )
        ax.set_title('Distribution of Faculty Staff by Gender')
        ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.

        # Display the plot in Streamlit
        st.pyplot(fig)

    else:
        st.warning("The DataFrame does not contain a 'Gender' column to plot distribution.")

# --- End of App ---
