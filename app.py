import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Scientific Visualization"
)

st.header("Genetic Algorithm", divider="gray")


# Set the title of the Streamlit application
st.title("Faculty Data Loader and Viewer")
st.markdown("This application loads the 'arts_faculty_data.csv' file from GitHub.")



# --- Configuration ---
st.set_page_config(layout="wide") # Use wide layout for better visualization
st.title("Faculty Data Analysis Dashboard 📊")
st.markdown("This application loads and visualizes the 'arts_faculty_data.csv' file from GitHub.")


# --- Configuration ---
st.set_page_config(layout="centered")
st.title("Faculty Gender Distribution (Plotly)")
st.markdown("Interactive visualization of the 'arts_faculty_data.csv' using Plotly.")

# --- Data Loading (Using st.cache_data for efficiency) ---
url = "https://raw.githubusercontent.com/Kamsinah0606/EC2024/refs/heads/main/arts_faculty_data.csv"

@st.cache_data
def load_data(data_url):
    """Loads the CSV data into a pandas DataFrame."""
    try:
        df = pd.read_csv(data_url)
        return df
    except Exception as e:
        st.error(f"Error loading data from URL: {e}")
        return None

df_onlines = load_data(url)

# --- Plotly Visualization ---
if df_onlines is not None:
    # 1. Calculate the gender counts
    # Unlike Matplotlib, Plotly Express needs two columns for the pie chart: 
    # the category (names) and the value (counts).
    gender_counts_df = df_onlines['Gender'].value_counts().reset_index()
    gender_counts_df.columns = ['Gender', 'Count']

    # 2. Create the Plotly figure using Plotly Express
    fig = px.pie(
        gender_counts_df,
        values='Count',
        names='Gender',
        title='Distribution of Faculty Staff by Gender',
        # Customizing the hover info and text
        hole=0.3, # Optional: makes it a donut chart
        color_discrete_sequence=px.colors.qualitative.Pastel # Use a nice color scheme
    )

    # Optional: Customize the layout for better presentation
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='#000000', width=1))
    )

    # 3. Display the Plotly figure in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Optional: Show the underlying data
    if st.checkbox('Show Gender Count Data'):
        st.dataframe(gender_counts_df)

else:
    st.warning("Could not display chart because data failed to load.")
