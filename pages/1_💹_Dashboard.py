# Required libraries
import streamlit as st
from streamlit_option_menu import option_menu
from  PIL import Image
import pandas as pd
import plotly.express as px
#from numerize.numerize import numerize
from sqlquery import *
import time

# Setting the web app basic information
st.set_page_config (page_title="Ouad|Jet",
                    page_icon=":chart_with_upwards_trend:",
                    layout="wide"
)
# Adjusting page Top and bottom padding
st.markdown("""
            <style>
                    .block-container {
                        padding-top:2rem;
                        padding-bottom: 0rem
                    }
            </style>
            """, unsafe_allow_html=True)

image = Image.open('E:/VS_Code/Webapps/Datarec/ressources/images/project.png')

col1, col2 = st.columns([8, 2])
with col1:
    st.title("Analytics Dashboard")
with col2:
    st.image(image, width=150)

with st.spinner('Wait for it...'):
    time.sleep(3)

st.divider()
st.subheader(":red[**Key**] Metrics 🔑")

# Defining data frames
client_count =  customer_count()
df1 = pd.DataFrame(client_count, columns = ["Count"])

delta_cnt1 =  customer_count_delta1()
df_1d = pd.DataFrame(delta_cnt1, columns = ["Join Date"])

delta_cnt2 =  customer_count_delta2()
df_2d = pd.DataFrame(delta_cnt2, columns = ["Join Date"])

val1 = df_1d["Join Date"].iloc[0] - df_2d["Join Date"].iloc[0]
#----------------------
turnover = total_sales()
df2 = pd.DataFrame(turnover, columns = ['Total Sales'])
val2 = df2['Total Sales'].astype(float)

current_mth = total_sales_curr()
df2_1d = pd.DataFrame(current_mth, columns = ['Current Sales'])

prev_mth = total_sales_prev()
df2_2d = pd.DataFrame(prev_mth, columns = ['Previous Sales'])

val2_1d = df2_1d['Current Sales'].iloc[0] - df2_2d['Previous Sales'].iloc[0]
#----------------------------
avg_sales = agv_sales()
df3 = pd.DataFrame(avg_sales, columns = ['Avg Sales'])
val3 = df3['Avg Sales'].astype(float)

curr_avgsales = avg_sales_curr()
df3_1d = pd.DataFrame(curr_avgsales, columns = ['Current Avg'])

prev_avgsales = avg_sales_prev()
df3_2d = pd.DataFrame(prev_avgsales, columns = ['Previous Avg'])

val3_1d = df3_1d['Current Avg'].iloc[0] - df3_2d['Previous Avg'].iloc[0]
#-----------------------------------------------
count_sales = sales_count()
df4 = pd.DataFrame(count_sales, columns = ['Sales Count'])

count_sales_curr = curr_sales_count()
df4_1d = pd.DataFrame(count_sales_curr, columns = ['Current Count'])

count_sales_prev = prev_sales_count()
df4_2d = pd.DataFrame(count_sales_prev, columns = ['Previous Count'])

val4 = df4_1d['Current Count'].iloc[0] - df4_2d['Previous Count'].iloc[0]
#------------------------------------------------
prod_sales = product_sales()
df5 = pd.DataFrame(prod_sales, columns = ['Date','Product','Quantity','Sales'])

# Defining metrics 
col1, col2, col3, col4 = st.columns(4, gap='large')
with col1:
    st.info(" Customer Stats", icon = "💁‍♀️")
    st.metric(":orange[Total Customers]", value = df1["Count"], delta = f'{val1}') 
with col2:
    st.info("Sales Turnover", icon = "💲")
    st.metric(":orange[Total Turnover (€)] ", value = val2, delta = f'{val2_1d}')
with col3:
    st.info("Sales Statistics", icon = "💱")
    st.metric(":orange[Average Sales (€)]", value = val3, delta = f'{val3_1d}')
with col4:
    st.info("Number of Sales", icon = "🪁")
    st.metric(":orange[Sales Counting]", value = df4['Sales Count'], delta = f'{val4}')
#----------------------------GRAPHS---------------------------------------------
st.divider()
st.subheader(":red[**Data**] Vizualisation 📊")
left, right = st.columns(2)
with left:
    # Line plot
    fig_line=px.line(
       df5,
       x=df5['Date'],
       y=df5['Sales'],
       orientation="v",
       text="Sales",
       markers=True,
       title="<b> Bimonthly Sales trend </b>",
       color_discrete_sequence=["#0083b8"]*len(df5),
       template="plotly_white",
    )
    fig_line.update_layout(
    yaxis_title='Sales in €uro',
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=True))
    ) 
    fig_line.update_traces(line=dict(width=3, color='crimson')) 
    left.plotly_chart(fig_line,use_container_width=True)
with right:
    # Bar plot
    fig_bar=px.bar(
       df5,
       x=df5['Product'],
       y=df5['Quantity'],
       orientation="v",
       color = 'Quantity', 
       range_color=(0,35),
       title="<b> Product sold Bimonthly </b>",
       color_continuous_scale = 'portland',
       #color_discrete_sequence=["#0083B8"]*len(df5), # Bleu #0083B8
       template="plotly_white",
    )
    fig_bar.update_coloraxes(colorbar_len=1.2)
    fig_bar.update_layout(
    yaxis_title='Count',
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
    )
    right.plotly_chart(fig_bar,use_container_width=True)

# # -----SIDEBAR-----
st.sidebar.success("Select a page above 👒")
st.sidebar.divider()
# Define Brand Logo image
image = Image.open('E:/VS_Code/Webapps/Datarec/ressources/images/techno.png')
# Add logo to the bottom right position of the page
st.sidebar.markdown('###')
st.sidebar.markdown('###')
st.sidebar.image(image,  width=250)
