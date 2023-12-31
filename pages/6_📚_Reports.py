# Required libraries
import streamlit as st
from  PIL import Image
from streamlit_option_menu import option_menu
from sqlquery import sales_report, monthly_sales_by_product
import pandas as pd
import datetime
from datetime import datetime
import calendar
import base64
import io
import openpyxl

# Defining some variables to get current Month and year
month_num = datetime.now().month
month_name = calendar.month_name[month_num]
year = datetime.now().year

# Function to convert dataframe to excel 
def excel_export(df):
    towrite = io.BytesIO()
    downloaded_file = df.to_excel(towrite, index=False, header=True)
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()  # some strings
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="myfilename.xlsx">Download excel file</a>'
    return linko

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
    image2 = Image.open('ressources/images/Report1.png')
    st.image(image2, width=1280, use_column_width=True)

st.subheader("💪BUSINESS STATS AND :red[**REPORTS**]")
st.divider()

# Defining data frames
sales_rep =  sales_report()
df_sale = pd.DataFrame(sales_rep, columns = ["Day", "Month", "Year", "Qty Sold", "Total Sales"])
# -------------------------
monthly_sales_rep =  monthly_sales_by_product()
df_sale2 = pd.DataFrame(monthly_sales_rep, columns = ["Product", "Qty Sold", "Total Sales"])
# --------------------------

# Creating tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["SALES", "CUSTOMERS", "PRODUCTS", "ORDERS", "MEMBERS"])
with tab1:
    with st.expander("Expand to view report 1"):
        # Displaying the result of the sales report query
        st.subheader(":violet[**Quarterly**] Daily Sales Report 📗")
        st.checkbox("Use container width", value=False, key="use_container_width_A")
        st.dataframe(df_sale, use_container_width=st.session_state.use_container_width_A)
        st.markdown(excel_export(df_sale), unsafe_allow_html=True)
    with st.expander("Expand to view report 2"):
        # Displaying the result of the sales report query
        st.subheader(f":orange[**{month_name}**] {year} Sales Report By Product 📘")
        st.checkbox("Use container width", value=False, key="use_container_width_B")
        st.dataframe(df_sale2, use_container_width=st.session_state.use_container_width_B)
        st.markdown(excel_export(df_sale2), unsafe_allow_html=True)
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
st.sidebar.divider()
# Define Brand Logo image
image = Image.open('ressources/images/techno.png')
# Add logo to the bottom right position of the page
st.sidebar.image(image,  width=250)