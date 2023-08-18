# Required libraries
import streamlit as st
from  PIL import Image
from streamlit_option_menu import option_menu

# Setting the web app basic information
st.set_page_config (page_title="Ouad|Jet",
                    page_icon=":date:",
                    layout="wide"
) 
# Adjusting page Top and bottom padding
st.markdown("""
            <style>
                    .block-container {
                        padding-top:1.7rem;
                        padding-bottom: 0rem
                    }
            </style>
            """, unsafe_allow_html=True)

# Adding top header image into a container
with st.container():
    image2 = Image.open('E:/VS_Code/Webapps/Datarec/ressources/images/Report1.png')
    st.image(image2, width=1280, use_column_width=True)
#st.divider()
st.subheader("💪BUSINEESS STATS AND :orange[**REPORTS**]")

# Creating tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["SALES", "CUSTOMERS", "PRODUCTS", "ORDERS", "MEMBERS"])
with tab1:
    st.write("")
with tab2:
    st.write("")
with tab3:
    st.write("")
with tab4:
    st.write("")
with tab5:
    st.write("")




# # -----SIDEBAR-----
st.sidebar.success("Select a page above.")
# Define Brand Logo image
image = Image.open('E:/VS_Code/Webapps/Datarec/ressources/images/techno.png')
# Add logo to the bottom right position of the page
st.sidebar.image(image,  width=250)