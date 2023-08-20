import mysql.connector
#import streamlit as st
import streamlit_authenticator as stauth
from settings import secrets

# Db connection param
conn = mysql.connector.connect(
        host = "192.168.2.70",
        port = "3306",
        user = "djehuty",
        password = secrets["DB_PASSWORD"],
        database = "afsavdb"
    )

c = conn.cursor()
 
# querying functions
def customer_count():
    c.execute('SELECT COUNT(cust_id) FROM Customer;')
    data = c.fetchall()
    return data

def total_sales():
    c.execute('SELECT ROUND(SUM(item_quantity * item_saleprice), 2)\
               AS "Total Sales" FROM Orderitem;')
    data = c.fetchall()
    return data

def agv_sales():
    c.execute('SELECT ROUND(AVG(item_quantity * item_saleprice), 2)\
               AS "Avg Sales" FROM Orderitem;')
    data = c.fetchall()
    return data

def sales_count():
    c.execute('SELECT COUNT(order_id) AS "Sales Count" FROM Orderitem;')
    data = c.fetchall()
    return data

def product_sales():
    c.execute('SELECT S.order_date AS "Date", P.product_name AS "Product", \
              O.item_quantity AS "Quantity", O.item_quantity * O.item_saleprice AS "Sales"\
              FROM Orderitem O \
              JOIN Orders S ON O.order_id = S.order_id\
              JOIN Product P ON P.product_id = O.product_id\
              WHERE MONTH(S.order_date) BETWEEN MONTH(now()) - 2 AND MONTH(now())\
              ORDER BY S.order_date;')
    data = c.fetchall()
    return data
# ---------------------------------------------------------------------------
# Reports query 
def sales_report():
    c.execute('SELECT REPLACE(YEAR(O.order_date),",","") AS Year,\
               MONTHNAME(O.order_date) AS Month, DAY(O.order_date) AS Day,\
               SUM(P.item_quantity * P.item_saleprice) AS Sales\
               FROM Orders O\
               JOIN Orderitem P ON P.order_id = O.order_id\
               WHERE MONTH(O.order_date) BETWEEN MONTH(now()) - 3 AND MONTH(now())\
               GROUP BY REPLACE(YEAR(O.order_date),",",""), MONTHNAME(O.order_date), DAY(O.order_date);')
    data = c.fetchall()
    return data

def monthly_sales_by_product():
    c.execute('SELECT P.product_name AS "Product Name",\
              COUNT(O.product_id) AS "Unit Sold",\
              SUM(O.item_quantity * O.item_saleprice) AS Sales \
              FROM Orderitem O\
              JOIN Product P on P.product_id = O.product_id\
              JOIN Orders S ON S.order_id = O.order_id\
              WHERE MONTH(S.order_date) = MONTH(now())\
              GROUP BY O.product_id')
    data = c.fetchall()
    return data