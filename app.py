import streamlit as st

st.set_page_config(
    page_title= "Student Survey"
)  # <-- Closing parenthesis was missing here

visualise = st.Page('page1.py', title='Pencapaian Akademik', icon=":material/school:")

# Note: The original code had 'pg.run()' here, which would run the navigation 
# before it was fully defined. I am assuming you meant to define 'pg' first.

home = st.Page('home.py', title='Homepage', default=True, icon=":material/home:")

# Assuming you meant to define 'pg' as st.navigation
pg = st.navigation(
    {
        "Menu":[home, visualise]
    }
)

pg.run()
