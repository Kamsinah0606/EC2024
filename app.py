import streamlit as st

st.set_page_config(
    page_title= "Student Survey"
)  

visualise = st.Page('page1.py', title='Data Visualization', icon=":material/school:")

home = st.Page('home.py', title='Homepage', default=True, icon=":material/home:")

# Assuming you meant to define 'pg' as st.navigation
pg = st.navigation(
    {
        "Menu":[home, visualise]
    }
)

pg.run()
