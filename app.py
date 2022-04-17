from apps import home, CryptoNews_app
from multiapp import MultiApp
import streamlit as st

app = MultiApp()

st.set_page_config(layout="wide")

st.image(
    "https://c.tenor.com/7VzBpq5zYR8AAAAd/eth.gif",
    width=500,)

st.markdown('''# **Ongoing crypto project**
## **Portfolio Manager Using Binance API**
A simple cryptocurrency price app pulling live price data from **Binance API**.
Prices are refreshed every 30 seconds. 
''')

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Crypto News Finder", CryptoNews_app.app)
# The main app
app.run()
