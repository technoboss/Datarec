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
                    page_icon=":curly_haired_man:",
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
    
# ADD A MENU WIDGET ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
selected1 = option_menu(None, ["Create", "Read", "Update", "Delete"], 
    icons=['bricks', 'book', 'folder-symlink', 'trash-fill'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
selected1
st.markdown('---')

# DEFINING SQL QUERY AND DATAFRAME
mycursor.execute("SELECT * FROM Membertype") # SQL query command
result = mycursor.fetchall()       # Assigning sql query result to a variable
df = pd.DataFrame(result)          # Converting sql result to Pandas dataframe
df_fmt = df.set_axis(['Mtype ID','Mtype name','Mtype fee','Mtype discount'], axis=1) #Formating df axis 1

# ADDING FUNCTIIONALITY TO CREATE
if selected1 == "Create":
    # Add sub header
    st.subheader(":red[**_Create_**] Membership Record 🎫")
    mtype_name = st.text_input("Enter Membership Name")
    mtype_fee = st.text_input("Enter Membership Fee")
    mtype_discount = st.text_input("Enter Discount value")
    # Add button
    if st.button("Create"):
        # Assigning sql command to variablea
        sqlcmd = "INSERT INTO Membertype (mtype_name, mtype_fee, mtype_discount) values(%s,%s,%s)"
        val = (mtype_name, mtype_fee, mtype_discount)
        mycursor.execute(sqlcmd, val)                 # Executing sql command
        dbconnect.commit()                            # Saves the changes in the db
        st.success("Record created successfully !!!") # Display a success message
        time.sleep(1)
        st.balloons()                                 # Celebration balloon

# ADDING FUNCTIIONALITY TO READ
elif selected1 == "Read":
    # Displaying the result and reseting the index
    st.subheader(":red[**_Read_**] Membership Records 🦢")
    st.checkbox("Use container width", value=False, key="use_container_width2")
    st.dataframe(df_fmt.set_index('Mtype ID'), use_container_width=st.session_state.use_container_width2)

# ADDING FUNCTIIONALITY TO UPDATE
elif selected1 == "Update":
    # Displaying the result and reseting the index
    st.subheader(":red[**_Membership_**] Records view 🕊️")
    st.checkbox("Use container width", value=False, key="use_container_width3")
    st.dataframe(df_fmt.set_index('Mtype ID'), use_container_width=st.session_state.use_container_width3)
    st.markdown(":violet[**Refresh**] the page after clicking on the Update \
                button to see the change appears in the Membership records.")
    st.divider()
    st.subheader(":orange[**_Update_**] Membership Records 🏌️‍♂️")
    # Adding new customer record
    left, middle, right = st.columns([0.4,0.03,0.4])
    with left:
        mtype_id = st.selectbox("Select a Membership ID", df_fmt['Mtype ID'].tolist())
        mtype_name = st.text_input("Enter Membership Name")
        #mtype_name = st.selectbox("Select a Membership", df_fmt['Mtype name'].tolist())
    with middle:
        st.write("")
    with right:
        mtype_fee = st.text_input("Enter new fee")
        mtype_discount = st.text_input("Enter new discount")
        # Adding button
        if st.button("Update"):
            # SQL query command
            sqlcmd = "UPDATE Membertype SET mtype_name=%s, mtype_fee=%s, \
                    mtype_discount=%s where mtype_id=%s"
            val = (mtype_name, mtype_fee, mtype_discount, mtype_id)
            mycursor.execute(sqlcmd, val)                 # Executing sql command
            dbconnect.commit()                            # Saves the changes in the db
            st.success("Hooray, Record Updated successfully !!!") # Display a success message
            time.sleep(1)
            st.balloons()                                 # Celebration balloon
    
# ADDING FUNCTIIONALITY TO DELETE
elif selected1 == "Delete":
    st.subheader(":orange[**Delete**] Membership Records 🗑️")
    #customer_id = st.number_input("Enter Customer ID", min_value=1)
    mtype_id = st.selectbox("Select a Membership ID", df_fmt['Mtype ID'].tolist())
    if st.button("Delete"):
        sqlcmd = "DELETE FROM Membertype WHERE mtype_id=%s"
        val = (mtype_id, )                         
        mycursor.execute(sqlcmd, val)                         # Executing the query
        dbconnect.commit()                                    # Saves the changes in the db
        st.success("Hooray, Record Deleted successfully !!!") # Display a success message
        time.sleep(1)
        st.balloons()                                     # Celebration balloon
    st.divider()
    # Displaying the result and reseting the index
    st.subheader(":red[**_Membership_**] Records view 🕊️")
    st.markdown(":violet[**Refresh**] the page after clicking on the Delete \
                button to see the change appears in the Membership records.")
    st.checkbox("Use container width", value=False, key="use_container_width4")
    st.dataframe(df_fmt.set_index('Mtype ID'), use_container_width=st.session_state.use_container_width4)

# # -----SIDEBAR-----
# ADDING SUCCESS MESSAGE ON SIDEBAR
st.sidebar.success("Select a page above 👒")
st.sidebar.markdown("""---""")
# Define Brand Logo image
image = Image.open('ressources/images/techno.png')
# Add logo to the bottom right position of the page 
st.sidebar.markdown('###')
st.sidebar.markdown('###')
st.sidebar.image(image,  width=250)
