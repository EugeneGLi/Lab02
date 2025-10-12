# Import Streamlit
import streamlit as st

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Homepage",  # The title that appears in the browser tab
    page_icon="🏠",         # An emoji that appears as the icon in the browser tab
)

# WELCOME PAGE TITLE
st.title("Welcome to My Data Dashboard!")
st.write("📊📊📊📊📊📊📊📊📊📊📊📊📊📊📊📊📊📊📊📊📊📊📊")
st.image('images/dashboard.webp')
# INTRODUCTORY TEXT

st.write("""
This application is designed to collect and visualize data.
You can navigate to the different pages using the sidebar on the left.

### How to use this app:
""")


if st.button("**Survey Page**:"):
    st.switch_page("pages/Survey.py")
st.write('Go here to input new data into my CSV file.')

if st.button('**Visuals Page**:'):
    st.switch_page('pages/Visuals.py')
st.write ('Go here to see the data visualized in different graphs.')
st.divider()


st.write("""This project is part of CS 1301's Lab 2.
""")

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your Lab02 directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
#
# st.image("images/welcome_image.png")