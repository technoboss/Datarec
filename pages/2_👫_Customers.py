# Required libraries
import streamlit as st
from streamlit_option_menu import option_menu
from  PIL import Image
import pandas as pd
import mysql.connector
from settings import secrets
import time

# SETTING UP THE APP BASIC INFORMATION
st.set_page_config (page_title="Ouad|Jet",
                    page_icon=":runner:",
                    layout="wide"
                    ) 

# ESTABLISH CONNECTION TO MYSQL SERVER
dbconnect = mysql.connector.connect(
    host = "192.168.2.70",
    port = "3306",
    user = "djehuty",
    password =  secrets["DB_PASSWORD"], 
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
    st.dataframe(df_fmt[df_fmt[filtercol]==filterow].set_index('Cust ID'),
                 use_container_width=st.session_state.use_container_width)
    
# CREATION OF THE MENU OPTION BAR
selected1 = option_menu(None, ["Create", "Read", "Update", "Delete"], 
    icons=['bricks', 'book', 'folder-symlink', 'trash-fill'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
selected1
st.markdown("""---""")

# ADDING SUCCESS MESSAGE ON SIDEBAR
st.sidebar.success("Select a page above 👒")
st.sidebar.markdown("""---""")

# DEFINING SQL QUERY AND DATAFRAME
mycursor.execute("SELECT * FROM Customer") # SQL query command
result = mycursor.fetchall()       # Assigning sql query result to a variable
df = pd.DataFrame(result)          # Converting sql result to Pandas dataframe
df_fmt = df.set_axis(['Cust ID','Title','Firstname','Surname','Address 1','Address 2',\
                      'Town','Postcode','Phone','Mtype','Email','Join date'], axis=1) #Formating df axis 1

# DEFINING SQL QUERY AND DATAFRAME
mycursor.execute("SELECT * FROM Membertype") # SQL query command
result = mycursor.fetchall()       # Assigning sql query result to a variable
df = pd.DataFrame(result)          # Converting sql result to Pandas dataframe
df_fmt2 = df.set_axis(['Mtype ID','Mtype name','Mtype fee','Mtype discount'], axis=1) #Formating df axis 1

# ADDING FUNCTIIONALITY TO CREATE
if selected1 == "Create":
    # Add sub header
    st.subheader(":red[**_Create_**] Customer Record 😎")
    #st.divider()

    # Add 3 columns with different width
    left, middle, right = st.columns([0.4,0.03,0.4])
    # Add text input
    with left:
        cust_title = st.selectbox("Choose Title", ('Mr', 'Mlle','Mme'))
        cust_fname = st.text_input("First Name")
        cust_sname = st.text_input("Surname")
        cust_address1 = st.text_input("Addresse 1")
        cust_address2 = st.text_input("Address 2")
    with middle:
        st.write("")
    with right:
        cust_town = st.text_input("Town")
        cust_pcode = st.text_input("Postcode")
        cust_phone = st.text_input("Phone number")
        cust_mtype = st.selectbox("Select Menbership ID", df_fmt2['Mtype ID'].tolist())
        cust_email = st.text_input("Email")
        join_date = st.date_input("Enter Join date")
        # Add button
        if st.button("Create"):
            # Assigning sql command to variablea
            sqlcmd = "INSERT INTO Customer (cust_title, cust_fname, cust_sname, cust_address1, \
                      cust_address2, cust_town, cust_pcode, cust_phone, cust_mtype, cust_email,\
                      join_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (cust_title, cust_fname, cust_sname, cust_address1, cust_address2,\
                   cust_town, cust_pcode, cust_phone, cust_mtype, cust_email, join_date)
            mycursor.execute(sqlcmd, val)                 # Executing sql command
            dbconnect.commit()                            # Saves the changes in the db
            st.success("Record created successfully !!!") # Display a success message
            time.sleep(1)
            st.balloons()                                 # Celebration balloon

# ADDING FUNCTIIONALITY TO READ
elif selected1 == "Read":
    # Adding search option feature
    x, y = 'Columns','Rows'
    search_opt(x, y)
    st.markdown("""---""")
    # Displaying the result and reseting the index
    st.subheader(":red[**_Read_**] Customers Records 🧑‍💻")
    st.dataframe(df_fmt.set_index('Cust ID'))

# ADDING FUNCTIIONALITY TO UPDATE
elif selected1 == "Update":
    # Adding record search feature on sidebar
    x, y = 'Columns','Rows'
    search_opt(x, y)
    st.markdown(":violet[**Relaunch**] your search options on the sidebar again\
                 after clicking on the Update button to refresh the query result.")
    st.markdown("""---""")

    # Add 3 columns with different width
    left, middle, right = st.columns([0.4,0.03,0.4])
    # Adding new customer record
    with left:
        st.subheader(":red[**_Update_**] Customers Records 🤵‍♂️")
        with st.expander("Important note"):
            st.markdown("The :orange[**customer ID, Title, First name and Surname**] cannot be changed\
                        by the system users. Only select the appropriate matching information with the\
                        original record. A search option is available in the sidebar to help you.\
                        If need be to update these records, please contact our :violet[**DevOps**] at\
                        :blue[**_m.curtisdon@yahoo.co.uk_**].")
       
        #customer_id = st.number_input("Enter Customer ID", min_value=1) 
        cust_id = st.selectbox("Select a customer ID", df_fmt['Cust ID'].tolist())
        cust_title = st.selectbox("Choose Title", ('Mr', 'Mlle','Mme'))
        cust_fname = st.selectbox("Select First Name", df_fmt['Firstname'].tolist())
        cust_sname = st.selectbox("Select Surname", df_fmt['Surname'].tolist())
        cust_address1 = st.text_input("Enter new Address 1")
        cust_address2 = st.text_input("Enter new Address 2")
    #st.markdown("""---""")
    with middle:
        st.write("")
    with right:
        with st.expander("Important note"):
            st.markdown("Here, :orange[**ONLY**] provide the new record where it is \
                        appropriate, otherwise enter the original matching record.")
        
        cust_town = st.text_input("Enter new Town")
        cust_pcode = st.text_input("Enter new Postcode")
        cust_phone = st.text_input("Enter new Phone number")
        cust_mtype = st.selectbox("Select Menbership ID", df_fmt2['Mtype ID'].tolist())
        cust_email = st.text_input("Enter new Email")
        join_date = st.date_input("Enter Join date")
        if st.button("Update"):
            # SQL query command
            sqlcmd = "UPDATE Customer SET cust_title=%s, cust_fname=%s, cust_sname=%s,\
                    cust_address1=%s, cust_address2=%s, cust_town=%s, cust_pcode=%s,\
                    cust_phone=%s, cust_mtype=%s, cust_email=%s, join_date=%s where cust_id=%s"
            val = (cust_title, cust_fname, cust_sname, cust_address1, cust_address2, \
                   cust_town, cust_pcode, cust_phone, cust_mtype, cust_email, join_date, cust_id)
            mycursor.execute(sqlcmd, val)                 # Executing sql command
            dbconnect.commit()                            # Saves the changes in the db
            st.success("Hooray, Record Updated successfully !!!") # Display a success message
            time.sleep(1)
            st.balloons()                                 # Celebration balloon
    
# ADDING FUNCTIIONALITY TO DELETE
elif selected1 == "Delete":
    # Adding record search feature on sidebar
    x, y = 'Columns','Rows'
    search_opt(x, y)
    st.markdown(":violet[**Relaunch**] your search option on the sidebar again\
                 after clicking on the Delete button to refresh the query result.")
    
    st.markdown("""---""")
    st.subheader(":orange[**Delete**] Customers Records 🗑️")
    #customer_id = st.number_input("Enter Customer ID", min_value=1)
    cust_id = st.selectbox("Select a customer ID", df_fmt['Cust ID'].tolist())
    if st.button("Delete"):
        sqlcmd = "DELETE FROM Customer WHERE cust_id = %s"
        val = (cust_id, )                         
        mycursor.execute(sqlcmd, val)                     # Executing the query
        dbconnect.commit()                                # Saves the changes in the db
        st.success("Hooray, Record Deleted successfully !!!") # Display a success message
        time.sleep(1)
        st.balloons()                                     # Celebration balloon

# Define Brand Logo image
image = Image.open('ressources/images/techno.png')
# Add logo to the bottom right position of the page
st.sidebar.markdown('###')
st.sidebar.markdown('###')
st.sidebar.image(image,  width=250)
    
