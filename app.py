import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Genetic Algorithm"
)

st.header("Genetic Algorithm", divider="gray")

# Define the URL for the data
URL = 'https://raw.githubusercontent.com/Kamsinah0606/EC2024/refs/heads/main/arts_faculty_data.csv'

# --- Data Loading and Preprocessing ---
@st.cache_data
def load_data(file_path):
    """Loads and preprocesses the Arts Faculty data."""
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found.")
        return pd.DataFrame()

    # Filter for 'Arts' Faculty
    arts_df = df[df['Faculty'] == 'Arts'].copy()

    # List of GPA columns to convert to numeric
    gpa_cols = [
        'S.S.C (GPA)', 
        'H.S.C (GPA)', 
        '1st Year Semester 1', 
        '1st Year Semester 2', 
        '2nd Year Semester 1', 
        '2nd Year Semester 2', 
        '3rd Year Semester 1', 
        '3rd Year Semester 2'
    ]

    for col in gpa_cols:
        # Coerce to numeric, setting non-convertible values to NaN
        arts_df.loc[:, col] = pd.to_numeric(arts_df[col], errors='coerce')

    # Calculate the average GPA across all recorded semesters
    semester_gpa_cols = [col for col in gpa_cols if 'Semester' in col]
    arts_df['Average_Semester_GPA'] = arts_df[semester_gpa_cols].mean(axis=1)

    # Drop rows with missing values in key columns for analysis
    arts_df.dropna(subset=['H.S.C or Equivalent study medium', 'Average_Semester_GPA'], inplace=True)

    # Clean up 'H.S.C or Equivalent study medium'
    arts_df['Study_Medium'] = arts_df['H.S.C or Equivalent study medium'].replace({
        'Bangla Medium': 'Bangla', 
        'English Medium': 'English'
    })

    # Prepare 'Coaching Center' variable
    arts_df['Attended_Coaching'] = arts_df['Did you ever attend a Coaching center?'].fillna('No').replace({
        'No': 'No', 
        'Yes': 'Yes'
    })
    
    # Prepare 'Conducive_Learning_Env_Rating'
    arts_df.rename(columns={'Area of Evaluation [Department ensures a conducive learning environment]': 'Conducive_Learning_Env_Rating'}, inplace=True)
    arts_df.dropna(subset=['Conducive_Learning_Env_Rating'], inplace=True)
    arts_df['Conducive_Learning_Env_Rating'] = arts_df['Conducive_Learning_Env_Rating'].astype(int).astype(str)

    return arts_df, semester_gpa_cols

# Define the file path (assuming the file is in the same directory)
FILE_PATH = 'arts_faculty_data.csv'
arts_df, semester_gpa_cols = load_data(FILE_PATH)

if arts_df.empty:
    st.stop()

st.title("Arts Faculty Data Visualizations")
st.markdown("---")


# --- 1. Distribution of Average Semester GPA (Histogram) ---
st.header("1. Distribution of Average Semester GPA")
st.write("This histogram shows the distribution of the average GPA across all recorded semesters for Arts Faculty students.")
try:
    fig_hist = px.histogram(
        arts_df, 
        x='Average_Semester_GPA', 
        nbins=20, 
        title='Distribution of Average Semester GPA',
        color_discrete_sequence = 'pink'
        
# Use update_traces to add the black outer border
fig_hist.update_traces(
    marker_line_width= 1,       # Sets the line width
    marker_line_color= 'black'  # Sets the line color
    )
    )
        
    fig_hist.update_layout(xaxis_title="Average Semester GPA", yaxis_title="Number of Students")
    st.plotly_chart(fig_hist, use_container_width=True)
except Exception as e:
    st.error(f"Error generating Histogram: {e}")

st.markdown("---")

# --- 2. Average GPA by Study Medium (Box Plot) ---
st.header("2. Average GPA Distribution by Prior Study Medium")
st.write("A box plot comparing the spread of average semester GPA for students based on their H.S.C. or equivalent study medium (Bangla vs. English).")
try:
    fig_box = px.box(
        arts_df, 
        x='Study_Medium', 
        y='Average_Semester_GPA', 
        color='Study_Medium',
        title='Average Semester GPA Distribution by Study Medium',
        color_discrete_map={'Bangla': 'skyblue', 'English': 'coral'}
    )
    fig_box.update_layout(xaxis_title="Study Medium", yaxis_title="Average Semester GPA")
    st.plotly_chart(fig_box, use_container_width=True)
except Exception as e:
    st.error(f"Error generating Box Plot: {e}")

st.markdown("---")

# --- 3. Student Feedback on Conducive Learning Environment (Bar Chart) ---
st.header("3. Student Feedback on Conducive Learning Environment")
st.write("A bar chart illustrating student ratings for the statement: 'Department ensures a conducive learning environment.' (Ratings: 1=Low, 5=High).")
try:
    # Calculate value counts and convert to DataFrame for Plotly
    rating_counts_df = arts_df['Conducive_Learning_Env_Rating'].value_counts().sort_index().reset_index()
    rating_counts_df.columns = ['Rating', 'Count']

    fig_bar = px.bar(
        rating_counts_df, 
        x='Rating', 
        y='Count', 
        text='Count',
        title='Student Feedback: Conducive Learning Environment Rating',
        color='Rating',
        color_discrete_sequence=px.colors.sequential.Teal
    )
    fig_bar.update_layout(xaxis_title="Rating (1=Low, 5=High)", yaxis_title="Number of Students")
    fig_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)
except Exception as e:
    st.error(f"Error generating Feedback Bar Chart: {e}")

st.markdown("---")

# --- 4. Correlation Heatmap of Semester GPAs ---
st.header("4. Correlation Heatmap of Semester GPAs")
st.write("A heatmap showing the linear correlation between the GPAs of the first few academic semesters, indicating consistency or change in student performance over time.")
try:
    # Select relevant columns and calculate correlation
    correlation_subset_df = arts_df[semester_gpa_cols].dropna()
    correlation_matrix_subset = correlation_subset_df.corr()

    fig_heat = px.imshow(
        correlation_matrix_subset, 
        text_auto=".2f", 
        aspect="equal",
        color_continuous_scale=px.colors.sequential.Viridis,
        title='Correlation Heatmap of Semester GPAs'
    )
    fig_heat.update_xaxes(side="top")
    st.plotly_chart(fig_heat, use_container_width=True)
except Exception as e:
    st.error(f"Error generating Heatmap: {e}")

st.markdown("---")

# --- 5. Average Semester GPA by Coaching Center Attendance (Violin Plot) ---
st.header("5. Average GPA by Coaching Center Attendance")
st.write("A violin plot comparing the full density distribution of average semester GPA between students who attended a coaching center and those who did not.")
try:
    fig_violin = px.violin(
        arts_df, 
        x='Attended_Coaching', 
        y='Average_Semester_GPA', 
        color='Attended_Coaching',
        box=True, # Show quartiles inside the violin
        points=False, # Do not show individual data points
        title='Average Semester GPA by Coaching Center Attendance',
        color_discrete_map={'Yes': 'lightgreen', 'No': 'red'}
    )
    fig_violin.update_layout(xaxis_title="Attended a Coaching Center?", yaxis_title="Average Semester GPA")
    st.plotly_chart(fig_violin, use_container_width=True)
except Exception as e:
    st.error(f"Error generating Violin Plot: {e}")
