import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Scientific Visualization"
)

st.header("Scientific Visualization", divider="gray")

def app():
    # Set the title of the app
    st.title('CSV File Uploader and Viewer')
    st.markdown("""
    Upload your CSV file below to display the first few rows 
    and see the dataframe's shape.
    """)

    # 1. Use st.file_uploader to let the user upload a file
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            # 2. Read the uploaded file into a pandas DataFrame
            # st.cache_data is used to cache the result of the function call
            # so data isn't reloaded every time the script reruns.
            @st.cache_data
            def load_data(file):
                # We use io.BytesIO or just the file object, pandas handles the rest
                # using the file-like object provided by Streamlit
                return pd.read_csv(file, encoding='latin-1')

            df = load_data(uploaded_file)

            st.success('File loaded successfully! 🎉')

            # 3. Display the head of the DataFrame (equivalent of display(df.head()))
            st.header('First 5 Rows of the Data')
            st.dataframe(df.head())

            # 4. Display the shape of the DataFrame (equivalent of print(df.shape))
            st.header('DataFrame Shape')
            # st.write is flexible and can display various data types
            st.write(f'The DataFrame has **{df.shape[0]}** rows and **{df.shape[1]}** columns.')
            st.code(df.shape)

        except Exception as e:
            # 5. Display the error message in Streamlit
            st.error(f'Error loading data: {e}')
            st.warning('Please check the file format and the specified encoding (`latin-1`).')

if __name__ == '__main__':
    app()


# Set the page configuration
st.set_page_config(layout="centered")
st.title("Faculty Gender Distribution Dashboard")
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
