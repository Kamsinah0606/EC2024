import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Scientific Visualization"
)

st.header("Genetic Algorithm", divider="gray")


# Set the page configuration
st.set_page_config(layout="centered")
st.title("Faculty Gender Distribution Dashboard 📊")
st.markdown("This app visualizes the gender distribution from `arts_faculty_data.csv` using **Plotly**.")

# --- 1. Data Loading ---
url = "https://raw.githubusercontent.com/Kamsinah0606/EC2024/refs/heads/main/arts_faculty_data.csv"

# Use st.cache_data for efficient loading, preventing repeated downloads
@st.cache_data
def load_data(data_url):
    """Loads the CSV data from the specified URL."""
    try:
        df = pd.read_csv(data_url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df_onlines = load_data(url)

# --- 2. Plotly Visualization ---
if df_onlines is not None:
    # Check if the required column exists
    if 'Gender' in df_onlines.columns:
        st.subheader("Gender Distribution of Faculty Staff")

        # Prepare data for Plotly: value_counts() to DataFrame
        # Plotly Express expects a DataFrame with columns for names (Gender) and values (Count)
        gender_counts_df = df_onlines['Gender'].value_counts().reset_index()
        gender_counts_df.columns = ['Gender', 'Count']

        # Create the Plotly figure
        fig = px.pie(
            gender_counts_df,
            values='Count',
            names='Gender',
            title='Distribution of Faculty Staff by Gender',
            hole=0.4, # Make it a donut chart
            color_discrete_sequence=px.colors.qualitative.Set3 # Use a vibrant color scheme
        )

        # Optional: Customize the text shown on the chart
        fig.update_traces(
            textposition='outside',
            textinfo='percent+label',
            marker=dict(line=dict(color='#000000', width=1))
        )

        # Display the Plotly figure in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("The DataFrame is missing the required column: 'Gender'.")

### How to Run the App
# 1. Install libraries: pip install streamlit pandas plotly
# 2. Run in terminal: streamlit run app.py
