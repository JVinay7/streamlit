import streamlit as st
import pandas as pd
import matplotlib.pyplot  as plt
import plotly.express as px
import requests
import snowflake.connector
import yfinance as yahooFinance
from yahoo_fin import stock_info as si
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
#st.dataframe(data)
st.write("Column Names:", data.columns)


data1=data.groupby(["CATEGORY"]).agg({"INVESTEDAMOUNT":"sum"}).reset_index()
data1.columns=["CATEGORY","INVESTEDAMOUNT"]
data2=data.groupby(["CATEGORY"]).agg({"SHARECOUNT":"sum"}).reset_index()
data2.columns=["CATEGORY","Invested Quantity"]

data1=data1.set_index("CATEGORY")
data2=data2.set_index("CATEGORY")

original_title1 = '<p style="font-family:Courier;text-align:left; color:Blue; font-size: 30px;">Amount and Quantity Visualization</p>'
st.write(original_title1  ,unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1: 
    scatter_fig = plt.figure(figsize=(6,4))
    scatter_ax = scatter_fig.add_subplot(111)
    plt.xlabel("CATEGORY")
    plt.ylabel("Amount Invested")
    data1.plot.bar(alpha=0.9, ax=scatter_ax, rot=45)
    st.pyplot(scatter_fig)
with col2:
    bar_fig = plt.figure(figsize=(6,4))
    bar_ax = bar_fig.add_subplot(111)
    plt.xlabel("CATEGORY")
    plt.ylabel("Quantity of Shares in category")
    data2.plot.bar(alpha=0.8, ax=bar_ax, rot=45)
    st.pyplot(bar_fig)

st.sidebar.markdown("## CATEGORY :")
n1=list(data["CATEGORY"].unique())
a1 = st.sidebar.selectbox("CATEGORY", n1)

original_title1 = '<p style="font-family:Courier;text-align:left; color:Blue; font-size: 30px;">Shares in Selected Category</p>'
st.write(original_title1  ,unsafe_allow_html=True)
data3=data[data["CATEGORY"]==a1]
data4=data3[["SHARES","BUYPRICE"]]
data4=data4.set_index("SHARES")
data5=data3[["SHARES","SHARECOUNT"]]
data5=data5.set_index("SHARES")
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

# if(a1=="ETF"):
#     pass
# else:
#     st.sidebar.markdown("## SHARES :")
#     n2=list(data3["SHARES"].unique())
#     a2 = st.sidebar.selectbox("SHARES", n2)
#     data6=data3[data3["SHARES"]==a2]
# st.write(data6)

# agree=st.sidebar.checkbox("Want to compare with live update")
# p=0
# if agree:
    #data=pd.read_excel("my_share_profile.xlsx")
    my_cur.execute("select * from my_share_profiletb")
    my_data_row = my_cur.fetchall()
    data = pd.DataFrame(my_data_row, columns=[desc[0] for desc in my_cur.description])
    data=data[data["CATEGORY"]!="ETF"]
    data["Live Price"]=data["TICKERFORYAHOO"].apply(lambda i:round(si.get_live_price(i), 3))
    data["Total Amount"]=data["Live Price"]*data["ShareCount"]
    data["Total Profit"]=data["Total Amount"]-data["INVESTEDAMOUNT"]
    data["Per Share perofit"]=data["Live Price"]-data["buyprice"]
    df = data.to_csv("new_data.csv",index=False)
    st.write(df.columns)
    
# data=pd.read_csv("new_data.csv")
# Total_Invested_Amount=data["INVESTEDAMOUNT"].sum()
# Total_current_value=data["Total Amount"].sum()
# total_profit=Total_current_value-Total_Invested_Amount
# original_title1 = '<p style="font-family:Courier;text-align:left; color:Blue; font-size: 30px;">Comparing With Return</p>'
# st.write(original_title1  ,unsafe_allow_html=True)

# col1, col2 ,col3= st.columns(3)
# with col1:
#     st.write("INVESTEDAMOUNT",Total_Invested_Amount)
# with col2:
#     st.write("Current Value",Total_current_value)
# with col3:
#     st.write("Profit",total_profit)
# data1=data.groupby(["Category"]).agg({"INVESTEDAMOUNT":"sum","Total Amount":"sum","Total Profit":"sum"}).reset_index()
# data1.columns=["Category","INVESTEDAMOUNT","Current Value","Total Profit"]
# data1=data1.sort_values(by="Total Profit", axis=0, ascending=False)
# st.table(data1)


# if(a1=="ETF"):
#     pass
# else:
#     data2=data[data["Category"]==a1]


# original_title1 = '<p style="font-family:Courier;text-align:left; color:Blue; font-size: 30px;">Comparing with in Category</p>'
# st.write(original_title1  ,unsafe_allow_html=True)
# data3=data2[["shares","buy price","INVESTEDAMOUNT","Total Amount","Total Profit","Per Share perofit"]]
# data3=data3.sort_values(by="Total Profit", axis=0, ascending=False)
# st.table(data3)


# original_title1 = '<p style="font-family:Courier;text-align:left; color:Blue; font-size: 30px;">Share wise Analysis</p>'
# st.write(original_title1  ,unsafe_allow_html=True)

# st.sidebar.markdown("## Shares :")
# n2=list(data2["shares"].unique())
# a2 = st.sidebar.selectbox("shares", n2)
# data6=data2[data2["shares"]==a2]
# data7=data6.drop(["index","Category","ticker for yahoo"],axis=1)
# st.write(data7)
# m=list(data6["ticker for yahoo"])
# m1=m[0]

# data_fin = yahooFinance.Ticker(m1)
# data_fin1=data_fin.history(period="12mo")
# data_fin2=data_fin1[["Close"]]
# max1=list(data_fin2.max())
# min1=list(data_fin2.min())
# col1, col2 = st.columns(2)
# with col1:
#     st.write("Last 1 year Max Close Value",max1[0])
# with col2:
#     st.write("Last 1 year Min Close Value",min1[0])

# original_title1 = '<p style="font-family:Courier;text-align:left; color:Blue; font-size: 30px;">Last 1 year closing plot</p>'
# st.write(original_title1  ,unsafe_allow_html=True)

# st.line_chart(data_fin2)

