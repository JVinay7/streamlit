import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import warnings
from urllib.error import URLError
warnings.filterwarnings("ignore")
st.set_page_config(layout="wide")

original_title1 = '<p style="font-family:Courier;text-align:center; color:Blue; font-size: 40px;">Investment Portfolio Dashboard</p>'
st.write(original_title1 ,unsafe_allow_html=True)

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from my_share_profiletb")
my_data_row = my_cur.fetchall()
data = pd.DataFrame(my_data_row, columns=[desc[0] for desc in my_cur.description])
st.title("Data from Snowflake")
st.dataframe(data)

print(data.columns)

data1=data.groupby(["category"]).agg({"InvestedAmount":"sum"}).reset_index()
data1.columns=["category","Invested Amount"]
data2=data.groupby(["category"]).agg({"ShareCount":"sum"}).reset_index()
data2.columns=["category","Invested Quantity"]

data1=data1.set_index("category")
data2=data2.set_index("category")

original_title1 = '<p style="font-family:Courier;text-align:left; color:Blue; font-size: 30px;">Amount and Quantity Visualization</p>'
st.write(original_title1  ,unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1: 
    scatter_fig = plt.figure(figsize=(6,4))
    scatter_ax = scatter_fig.add_subplot(111)
    plt.xlabel("category")
    plt.ylabel("Amount Invested")
    data1.plot.bar(alpha=0.9, ax=scatter_ax, rot=45)
    st.pyplot(scatter_fig)
with col2:
    bar_fig = plt.figure(figsize=(6,4))
    bar_ax = bar_fig.add_subplot(111)
    plt.xlabel("category")
    plt.ylabel("Quantity of Shares in category")
    data2.plot.bar(alpha=0.8, ax=bar_ax, rot=45)
    st.pyplot(bar_fig)

st.sidebar.markdown("## category :")
n1=list(data["category"].unique())
a1 = st.sidebar.selectbox("category", n1)

original_title1 = '<p style="font-family:Courier;text-align:left; color:Blue; font-size: 30px;">Shares in Selected Category</p>'
st.write(original_title1  ,unsafe_allow_html=True)
data3=data[data["category"]==a1]
data4=data3[["shares","buyprice"]]
data4=data4.set_index("shares")
data5=data3[["shares","ShareCount"]]
data5=data5.set_index("shares")
col1, col2 = st.columns(2)
with col1: 
    scatter_fig = plt.figure(figsize=(6,4))
    scatter_ax = scatter_fig.add_subplot(111)
    plt.ylabel("Buying Price per Share")
    data4.plot.bar(alpha=0.9, ax=scatter_ax, rot=45)
    st.pyplot(scatter_fig)
with col2:
    bar_fig = plt.figure(figsize=(6,4))
    bar_ax = bar_fig.add_subplot(111)
    plt.ylabel("Quantity of Shares")
    data5.plot.bar(alpha=0.8, ax=bar_ax, rot=45)
    st.pyplot(bar_fig)

if(a1=="ETF"):
    pass
else:
    st.sidebar.markdown("## Shares :")
    n2=list(data3["shares"].unique())
    a2 = st.sidebar.selectbox("shares", n2)
    data6=data3[data3["shares"]==a2]
st.write(data6)

