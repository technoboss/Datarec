# Required libraries
import streamlit as st
from streamlit_option_menu import option_menu
from  PIL import Image
import pandas as pd
import mysql.connector
from settings import secrets
import time

# Setting the web app basic information
st.set_page_config (page_title="Ouad|Jet",
                    page_icon=":package:",
                    layout="wide"
) 

# ESTABLISH CONNECTION TO MYSQL SERVER
dbconnect = mysql.connector.connect(
    host = "192.168.2.70",
    user = "djehuty",
    password = secrets["DB_PASSWORD"],
    database = "afsavdb"
    )
mycursor = dbconnect.cursor() # Creating a cursor

# Defining a function to display search option feature
def search_opt(x,y):
    # Adding filtering feature on sidebar
    st.sidebar.subheader("Basic Search:")
    filtercol = st.sidebar.selectbox(x, df_fmt.columns)
    filterow = st.sidebar.selectbox(y, df_fmt[filtercol].unique())
    st.sidebar.markdown('---')

    # Display filtering result
    st.subheader('Search :green[**_Result_**] ⏳')
    st.checkbox("Use container width", value=False, key="use_container_width")
    st.dataframe(df_fmt[df_fmt[filtercol]==filterow].set_index('Product ID'),
                 use_container_width=st.session_state.use_container_width)
def cook_breakfast():
    msg = st.toast('Gathering ingredients...')
    time.sleep(2)
    msg.toast('Cooking...')
    time.sleep(2)
    msg.toast('Ready!', icon = "🥞")

# ADD A MENU WIDGET ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
selected1 = option_menu(None, ["Create", "Read", "Update", "Delete"], 
    icons=['bricks', 'book', 'folder-symlink', 'trash-fill'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
selected1
st.divider()

# DEFINING SQL QUERY AND DATAFRAME
mycursor.execute("SELECT * FROM Product") # SQL query command
result = mycursor.fetchall()       # Assigning sql query result to a variable
df = pd.DataFrame(result)          # Converting sql result to Pandas dataframe
df_fmt = df.set_axis(['Product ID','Product name', 'Product type', 'Product price','Product desc'], axis=1) #Formating df axis 1

# # -----------------SIDEBAR-------------
st.sidebar.success("Select a page above 👒")
st.sidebar.markdown("""---""")

# ADDING FUNCTIIONALITY TO THE MENU OPTION
if selected1 == "Create":
    cook_breakfast()
    # Add sub header
    st.subheader(":red[**Create**] Products Record 🍓🍉🍏🍌")
    product_name = st.text_input("Enter Product name")
    product_type = st.selectbox("Select Product type", ('Grocery','Meat','Cereal','Dry Nuts',\
                                'Fruit','Vegetable','Spices', 'Fish'))
    product_price = st.text_input("Product price")
    product_description = st.text_input("Brief description")
    # Add button
    if st.button("Create"):
        # Assigning sql command to variablea
        sqlcmd = "INSERT INTO Product (product_name, product_type, product_price,\
                  product_description) values(%s,%s,%s,%s)"
        val = (product_name, product_type, product_price,product_description )
        mycursor.execute(sqlcmd, val)                 # Executing sql command
        dbconnect.commit()                            # Saves the changes in the db
        time.sleep(2)
        st.success("Record created successfully !!!") # Display a success message
        time.sleep(2)
        st.balloons()                                 # Celebration balloon

# ADDING FUNCTIIONALITY TO READ
elif selected1 == "Read":
    # Displaying the result and reseting the index
    st.subheader(":violet[**_Read_**] Products Records 🦅")
    st.checkbox("Use container width", value=False, key="use_container_width11")
    st.dataframe(df_fmt.set_index('Product ID'), use_container_width=st.session_state.use_container_width11)

# ADDING FUNCTIIONALITY TO UPDATE
elif selected1 == "Update":
    # Adding record search feature on sidebar
    x, y = 'Columns','Rows'
    search_opt(x, y)
    st.markdown(":orange[**Rerun**] your search option on the sidebar again\
                 after clicking on the Update button to refresh the query result.")
    st.divider()
    # Displaying the result and reseting the index
    st.subheader(":violet[**_Update_**] Products Records 🦉")
    # Adding new customer record
    left, middle, right = st.columns([0.4,0.03,0.4])
    with left:
        product_id = st.selectbox("Select Product Id", df_fmt['Product ID'].tolist())
        #product_name = st.text_input ("Enter product name")
        product_name = st.selectbox("Select Product name", df_fmt['Product name'].tolist())
        product_type = st.selectbox("Select Product type", ('Grocery', 'Meat','Cereal','Dry Nuts','Fruit',\
                                    'Vegetable','Spices', 'Fish'))
    with middle:
        st.write("")
    with right:
        product_price = st.text_input("Enter new price")
        product_description = st.text_input("Enter new description")
        # Adding button
        st.markdown('###')
        if st.button("Update"):
            cook_breakfast()
            # SQL query command
            sqlcmd = "UPDATE Product SET product_name=%s, product_type=%s, \
                    product_price=%s, product_description=%s where product_id=%s"
            val = (product_name, product_type, product_price, product_description, product_id)
            mycursor.execute(sqlcmd, val)                 # Executing sql command
            dbconnect.commit()                            # Saves the changes in the db
            time.sleep(2)
            st.success("Hooray, Record Updated successfully !!!") # Display a success message
            time.sleep(2)
            st.balloons()   

# ADDING FUNCTIIONALITY TO DELETE
elif selected1 == "Delete":
    
    st.subheader(":orange[**Delete**] Products Records 🗑️")
    #customer_id = st.number_input("Enter Customer ID", min_value=1)
    product_id = st.selectbox("Select Product Id", df_fmt['Product ID'].tolist())
    if st.button("Delete"):
        sqlcmd = "DELETE FROM Product WHERE product_id = %s"
        val = (product_id, )                         
        mycursor.execute(sqlcmd, val)                     # Executing the query
        dbconnect.commit()                                # Saves the changes in the db
        st.success("Hooray, Record Deleted successfully !!!") # Display a success message
        time.sleep(1)
        st.balloons()                                     # Celebration balloon
    # Adding record search feature on sidebar
    st.divider()
    x, y = 'Columns','Rows'
    search_opt(x, y)
    st.markdown(":red[**Rerun**] your search options on the sidebar again\
                 after clicking on the Delete button to refresh the query result.")

# Define Brand Logo image
image = Image.open('E:/VS_Code/Webapps/Datarec/ressources/images/techno.png')
# Add logo to the bottom right position of the page
st.sidebar.markdown('###')
st.sidebar.markdown('###')
st.sidebar.image(image,  width=250)