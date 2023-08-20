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
                    page_icon=":moneybag:",
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

# DEFINING SQL QUERY AND DATAFRAME
mycursor.execute("SELECT * FROM Customer") # SQL query command
result = mycursor.fetchall()       # Assigning sql query result to a variable
df = pd.DataFrame(result)          # Converting sql result to Pandas dataframe
df_fmt = df.set_axis(['Cust ID','Title','Firstname','Surname','Address 1','Address 2',\
                    'Town','Postcode','Phone','Mtype','Email'], axis=1)

# Defining a filter function 
def search_opt(x,y):
    # Adding filtering feature on sidebar
    st.sidebar.subheader("Basic Search:")
    filtercol = st.sidebar.selectbox(x, df_fmt.columns)
    filterow = st.sidebar.selectbox(y, df_fmt[filtercol].unique())
    # Display filtering result
    st.subheader('Search :green[**_Result_**] ⏳')
    st.checkbox("Use container width", value=False, key="use_container_width")
    st.dataframe(df_fmt[df_fmt[filtercol]==filterow].set_index('Cust ID'),
                 use_container_width=st.session_state.use_container_width)

# ADD A MENU WIDGET ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
selected1 = option_menu(None, ["Create", "Read", "Update", "Delete"], 
    icons=['bricks', 'book', 'folder-symlink', 'trash-fill'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
selected1
st.markdown('---')

# DEFINING SQL QUERY AND DATAFRAME 1
mycursor.execute("SELECT * FROM Orders") # SQL query command
result = mycursor.fetchall()             # Assigning sql query result to a variable
df = pd.DataFrame(result)                # Converting sql result to Pandas dataframe
df_fmt1 = df.set_axis(['Order ID','Customer ID','Order date'], axis=1) #Formating df axis 1

 # DEFINING SQL QUERY AND DATAFRAME 2
mycursor.execute("SELECT * FROM Orderitem") # SQL query command
result = mycursor.fetchall()       # Assigning sql query result to a variable
df = pd.DataFrame(result)          # Converting sql result to Pandas dataframe
df_fmt2 = df.set_axis(['Order ID','Product ID','Item QTY', 'Item saleprice'], axis=1)

# DEFINING SQL QUERY AND DATAFRAME
mycursor.execute("SELECT * FROM Product") # SQL query command
result = mycursor.fetchall()       # Assigning sql query result to a variable
df = pd.DataFrame(result)          # Converting sql result to Pandas dataframe
df_fmt3 = df.set_axis(['Product ID','Product name', 'Product type', 'Product price','Product desc'], axis=1)

# # ---------------SIDEBAR------------------
st.sidebar.success("Select a page above 👒")
st.sidebar.divider()
# --------------------------------------------

if selected1 == "Create":
    st.markdown("Click on :orange[**Orders**] tab to enter information about the Order\
            and click on :orange[**Items**] tab to enter information about the Item.")
    # Creating tabs
    tab1, tab2 = st.tabs(["Orders", "Items"])
    with tab1:
        # Add sub header
        st.subheader(":green[**_Create_**] Orders Records ☘️")
        order_custid = st.text_input("Enter Customer ID")
        order_date = st.date_input("Enter Order date")
        # Add button
        if st.button("Save"):
            # Assigning sql command to variablea
            sqlcmd = "INSERT INTO Orders (order_custid, order_date) values(%s,%s)"
            val = (order_custid, order_date)
            mycursor.execute(sqlcmd, val)                 # Executing sql command
            dbconnect.commit()                            # Saves the changes in the db
            st.success("Record created successfully !!!") # Display a success message
            time.sleep(1)
            st.balloons()                                 # Celebration balloon
        
        with st.expander(":red[**Important note**]"):
            st.markdown("You can :orange[**USE**] the search feature \
                        in the sidebar to help you find the customer record you \
                        you are looking for to enable you fill the form above accurately.")
        # Adding Customers record search option feature
        x, y = 'Columns','Rows'
        search_opt(x, y)

    with tab2:
        # Add sub header
        st.subheader(":green[**_Create_**] Items Records 🧩")
        order_id = st.selectbox("Choose Order Id", df_fmt1['Order ID'].tolist())
        product_id = st.selectbox("Choose product Id", df_fmt3['Product ID'].tolist())
        Item_quantity = st.text_input("Enter Item quantity")
        Item_saleprice = st.text_input("Enter sales price")
        # Add button
        if st.button("Create"):
            # Assigning sql command to variablea
            sqlcmd = "INSERT INTO Orderitem (order_id, product_id, Item_quantity, Item_saleprice) values(%s,%s,%s,%s)"
            val = (order_id, product_id, Item_quantity, Item_saleprice)
            mycursor.execute(sqlcmd, val)                 # Executing sql command
            dbconnect.commit()                            # Saves the changes in the db
            st.success("Record created successfully !!!") # Display a success message
            time.sleep(1)
            st.balloons()  
        
        # Displaying records
        st.subheader(":red[**_Items_**] Records View🦓")
        with st.expander(":red[**Important note**]"):
            st.markdown("You can :violet[**view**] information on the item ordered such as\
                        product ID and order ID to help you fill the form accurately.")
        with st.expander(":orange[**View ordered item records**]"):
            st.checkbox("Use container width", value=False, key="use_container_width6")
            st.dataframe(df_fmt2.set_index('Order ID'), use_container_width=st.session_state.use_container_width6)      
        with st.expander(":violet[**View products records**]"):
            st.checkbox("Use container width", value=False, key="use_container_width13")
            st.dataframe(df_fmt3.set_index('Product ID'), use_container_width=st.session_state.use_container_width13)

elif selected1 == "Read":
    st.markdown("Click on :orange[**Orders**] tab to read information about Orders\
            and click on :violet[**Items**] tab to read information about Items.")
    # Creating tabs
    tab1, tab2 = st.tabs(["Orders", "Items"])
    with tab1:
        # Displaying the result and reseting the index
        st.subheader(":red[**_Read_**] Orders Records 🦘")
        st.checkbox("Use container width", value=False, key="use_container_width5")
        st.dataframe(df_fmt1.set_index('Order ID'), use_container_width=st.session_state.use_container_width5)     
    with tab2:
        # Displaying the result and reseting the index
        st.subheader(":red[**_Read_**] Items Records 🦓")
        st.checkbox("Use container width", value=False, key="use_container_width6")
        st.dataframe(df_fmt2.set_index('Order ID'), use_container_width=st.session_state.use_container_width6)     

# ADDING FUNCTIIONALITY TO UPDATE
elif selected1 == "Update":
    st.markdown("Click on :orange[**Orders**] tab to Update information about Orders\
                and click on :violet[**Items**] tab to Update information about Items.")
    # Creating tabs
    tab1, tab2 = st.tabs(["Orders", "Items"])
    with tab1:
        # Displaying the result and reseting the index
        st.subheader(":violet[**_Update_**] Orders Records 🦄")
        #order_id = st.selectbox("Select Order Id", df_fmt1['Order ID'].tolist())
        order_id = st.number_input("Type order_id", min_value=1)
        order_custid = st.selectbox("Enter Customer ID", df_fmt1['Customer ID'].unique())
        order_date = st.date_input("Enter Order date")
        # Adding button
        if st.button("Update"):
            # SQL query command
            sqlcmd = "UPDATE Orders SET order_custid=%d, order_date=%s \
                     where order_id=%d"
            val = (order_custid, order_date, order_id)
            mycursor.execute(sqlcmd, val)                 # Executing sql command
            dbconnect.commit()                            # Saves the changes in the db
            st.success("Hooray, Record Updated successfully !!!") # Display a success message
            time.sleep(1)
            st.balloons()  
        st.divider()
        # Displaying the result and reseting the index
        st.subheader(":red[**_Customers_**] Records view 🕊️")
        with st.expander("Note importante!"):
            st.write(":orange[**Refresh**] the page after you have clicked on the Update \
                        button to view the up to date records. You can also \
                        use the search feature in the sidebar to find the customer record.") 
        # Adding Customers record search option feature
        x, y = 'Columns','Rows'
        search_opt(x, y)
        # st.checkbox("Use container width", value=False, key="use_container_width7")
        # st.dataframe(df_fmt1.set_index('Order ID'), use_container_width=st.session_state.use_container_width7)
        st.divider()
        
    with tab2:
        # Displaying the result and reseting the index
        st.subheader(":green[**_Update_**] Items Records 🦆")
        order_id = st.selectbox("Choose Order Id", df_fmt2['Order ID'].tolist())
        product_id = st.selectbox("Enter Product ID", df_fmt2['Product ID'].unique())
        item_quantity = st.text_input("Enter Item quantity")
        #item_saleprice = st.selectbox("Select sale price", df_fmt3['Product price'].tolist())
        item_saleprice = st.text_input("Enter Item sales price")
        # Adding button
        if st.button("Save"):
            # SQL query command
            sqlcmd = "UPDATE Orderitem SET product_id=%s, item_quantity=%s, item_saleprice=%f \
                      WHERE order_id=%s"
            val = (product_id, item_quantity, item_saleprice, order_id)
            mycursor.execute(sqlcmd, val)                 # Executing sql command
            dbconnect.commit()                            # Saves the changes in the db
            st.success("Hooray, Record Updated successfully !!!") # Display a success message
            time.sleep(1)
            st.balloons()   
        st.divider()
        choice = st.radio(":orange[*Select the record you would like to view*]",\
                          ("Item ordered","Product"), horizontal=True)
        with st.expander(":red[**Note importante!**]"):
            st.write(":violet[**Refresh**] the page after you have clicked on the Save \
                    button to view the up to date records. You can also select a radio\
                    button to view any ordered item or product records.") 
        if choice == "Item ordered":
            # Displaying the result and reseting the index
            st.subheader(":red[**_Items_**] Records view 🦃")
            st.checkbox("Use container width", value=False, key="use_container_width8")
            st.dataframe(df_fmt2.set_index('Order ID'), use_container_width=st.session_state.use_container_width8)
        if choice == "Product":
            # Displaying the result and reseting the index
            st.subheader(":orange[**_Products_**] Records View 🦅")
            st.checkbox("Use container width", value=False, key="use_container_width12")
            st.dataframe(df_fmt3.set_index('Product ID'), use_container_width=st.session_state.use_container_width12)

# ADDING FUNCTIIONALITY TO DELETE
elif selected1 == "Delete":
    st.markdown("Click on :orange[**Orders**] tab to Delete Order record\
                and click on :violet[**Items**] tab to Delete Items record.")
    # Creating tabs
    tab1, tab2 = st.tabs(["Orders", "Items"])
    with tab1:
        st.subheader(":orange[**Delete**] Order Records 🗑️")
        order_id = st.selectbox("Select Order Id", df_fmt1['Order ID'].tolist())
        if st.button("Delete"):
            sqlcmd = "DELETE FROM Orders WHERE order_id = %s"
            val = (order_id, )                         
            mycursor.execute(sqlcmd, val)                     # Executing the query
            dbconnect.commit()                                # Saves the changes in the db
            st.success("Hooray, Record Deleted successfully !!!") # Display a success message
            time.sleep(1)
            st.balloons()                                     # Celebration balloon
        # Displaying the result and reseting the index
        st.divider()
        st.subheader(":red[**_Orders_**] Records view 🚷")
        st.markdown(":red[**Refresh**] the page after clicking on the Delete \
                    button to see the change appears in the Orders records.") 
        st.checkbox("Use container width", value=False, key="use_container_width9")
        st.dataframe(df_fmt1.set_index('Order ID'), use_container_width=st.session_state.use_container_width9)
    with tab2:
        st.subheader(":orange[**Delete**] Item Records 🗑️")
        order_id = st.selectbox("Choose Order ID", df_fmt2['Order ID'].tolist())
        if st.button("Erase"):
            sqlcmd = "DELETE FROM Orderitem WHERE order_id = %s"
            val = (order_id, )                         
            mycursor.execute(sqlcmd, val)                     # Executing the query
            dbconnect.commit()                                # Saves the changes in the db
            st.success("Hooray, Record Deleted successfully !!!") # Display a success message
            time.sleep(1)
            st.balloons()                                     # Celebration balloon
        # Displaying the result and reseting the index
        st.divider()
        st.subheader(":green[**_Item_**] Records view 🚯")
        st.markdown(":red[**Refresh**] the page after clicking on the Delete \
                    button to see the change appears in the Orders records.") 
        st.checkbox("Use container width", value=False, key="use_container_width10")
        st.dataframe(df_fmt1.set_index('Order ID'), use_container_width=st.session_state.use_container_width10)
        #st.markdown("""---""")

# Define Brand Logo image
image = Image.open('E:/VS_Code/Webapps/Datarec/ressources/images/techno.png')
# Add logo to the bottom right position of the page
st.sidebar.markdown('###')
st.sidebar.markdown('###')
st.sidebar.image(image,  width=250)

