# Required libraries
import streamlit as st
from  PIL import Image
from streamlit_option_menu import option_menu
#from calendar_view.calendar import Calendar
#from calendar_view.config import style
#from calendar_view.core import data
#from calendar_view.core.event import Event

# Setting the web app basic information
st.set_page_config (page_title="Ouad|Jet",
                    page_icon=":date:",
                    layout="wide"
) 

st.subheader("💪 COMING SOON !!! 🚴‍♂️")



# # -----SIDEBAR-----
st.sidebar.success("Select a page above.")
# Define Brand Logo image
image = Image.open('E:/VS_Code/Webapps/Datarec/ressources/images/techno.png')
# Add logo to the bottom right position of the page
st.sidebar.image(image,  width=250)