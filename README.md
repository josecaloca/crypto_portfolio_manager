# Cryptocurrency Portfolio Manager with Real Life Data

# Demo

Launch the web app:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/josecaloca/crypto_portfolio_manager/app.py)

# Reproducing this web app
To recreate this web app on your own computer, do the following.

### Create conda environment (Optional)
Firstly, we will create a conda environment called *binance*
```
conda create -n binance python=3.7.9
```
Secondly, we will login to the *binance* environment
```
conda activate binance
```

###  Download GitHub repo

```
git clone https://github.com/dataprofessor/binance
```

###  Pip install libraries
```
pip install -r requirements.txt
```

### Get Binance Api Key

Make sure you have a private Binance API Key. This can be obtained by subscribing to binance by [cliking here](https://accounts.binance.com/en/register?ref=186625161)

Also, instructions on how to get the API Key are described in the following article by Binance: [click here](https://www.binance.com/en/support/faq/360002502072)

We recommend to add a CSV file to the root of this repository named ```api_key.csv``` containing both your ```api_key``` and ```api_secret``` in the corresponding order

**Example**
File name: ```api_key.csv```.

| api_key                                                          | api_secret                                                       |
|------------------------------------------------------------------|------------------------------------------------------------------|
| nndIDRzmc.... | AePEYUZgx.... |


###  Launch the app

```
streamlit run app.py
```
