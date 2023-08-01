import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import yfinance as yahooFinance
from yahoo_fin import stock_info as si
import snowflake.connector
import warnings
warnings.filterwarnings("ignore")
st.set_page_config(layout="wide")

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)
