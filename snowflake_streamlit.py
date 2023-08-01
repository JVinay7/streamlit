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
data = pd.read_csv(my_data_row)
st.text("Hello from Snowflake:")
st.dataframe(my_data_row)

