# Import necessary Libraries
from pathlib import Path
import yaml
from yaml.loader import SafeLoader
from  PIL import Image
import streamlit as st
import streamlit_authenticator as stauth
from askbaba import main
#from quicknews import run

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Ouad|Jet MS", 
                   page_icon=":rainbow:", 
                   layout="wide")

# Adjusting page Top and bottom padding
st.markdown("""
            <style>
                    .block-container {
                        padding-top:0rem;
                        padding-bottom: 0rem
                    }
            </style>
            """, unsafe_allow_html=True)

hide_bar= """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        visibility:hidden;
        width: 0px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        visibility:hidden;
    }
    </style>
"""
# Openning the YAML config file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
# Loading authentication parameters
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Define a login form and where it should located
name, authentication_status, username = authenticator.login("🔒 Login", "main")

# Check for authentication statuses
if authentication_status == False:
    st.error("username or password is incorrect!")
    st.markdown(hide_bar, unsafe_allow_html=True)

if authentication_status == None:
    # ADD SOME TEXTS TO MAIN PAGE
    st.warning("Please enter your username and password")
    st.markdown(hide_bar, unsafe_allow_html=True)
    st.title(':eyes: :orange[**Ouad|Jet**] Management System✨')
    with st.expander(":violet[**About OMS**] 🌍"):
        st.markdown('This web app enable you to manage and administer your database by performing \
                    :blue[**CRUD operations**].It also generate BI statistical data and visualization\
                    to always push you on top of your business decisions to :violet[**smoothly & successfully**] run it.')
    # Adding top header image into a container
    with st.container():
        image = Image.open("E:/VS_Code/Webapps/Datarec/ressources/images/bannertech1.png")
        st.image(image, width=1280, use_column_width=True)

if authentication_status:
    main()
    #run()
    # # ---- SIDEBAR ---------------------
    st.sidebar.title(f"🔓 Welcome {name}")
    st.sidebar.success("Select a page above 👒")
    # Adding logout feature
    authenticator.logout("Logout", "sidebar", key='uniquekey')
    ###---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    st.sidebar.markdown('###')
    st.sidebar.markdown('''
            ---
            Developed with 💖 by:''') 
    # Define Brand Logo image
    image = Image.open('E:/VS_Code/Webapps/Datarec/ressources/images/techno.png')
    # Add logo 
    st.sidebar.image(image,  width=250)

