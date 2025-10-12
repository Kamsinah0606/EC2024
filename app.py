import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Genetic Algorithm"
)

st.header("Genetic Algorithm", divider="gray")


# Set the page configuration
st.set_page_config(layout="centered")
st.title("Faculty Gender Distribution Dashboard 📊")
st.markdown("This app visualizes the gender distribution from `arts_faculty_data.csv` using **Plotly**.")


# URL for the dataset
url = "https://raw.githubusercontent.com/Kamsinah0606/EC2024/refs/heads/main/arts_faculty_data.csv"

# Set the title for the Streamlit app
st.title('Gender Distribution Analysis')

@st.cache_data
def load_data(data_url):
    """Loads data from the URL and caches it."""
    try:
        df = pd.read_csv(data_url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame() # Return an empty DataFrame on error

# Load the data
df = load_data(url)

# Check if the DataFrame is loaded and 'Gender' column exists
if not df.empty and 'Gender' in df.columns:
    # 1. Calculate the counts for each gender
    gender_counts = df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']

    # 2. Create the Plotly Pie Chart
    # Plotly Express is generally preferred for simple Plotly figures
    fig = px.pie(
        gender_counts,
        names='Gender',         # Column for labels
        values='Count',         # Column for values
        title='Distribution of Gender',
        hole=0.3,               # Optional: Creates a donut chart
        color_discrete_sequence=px.colors.qualitative.Pastel # Optional: Set colors
    )

    # 3. Customize the layout (optional but good practice)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    # 4. Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Optional: Display the raw counts
    st.subheader('Raw Gender Counts')
    st.dataframe(gender_counts, use_container_width=True)

else:
    st.warning("Data could not be loaded or the 'Gender' column is missing.")
