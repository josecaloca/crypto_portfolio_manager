# Cryptocurrency Portfolio Manager with Real Time Data

![flowchart](https://user-images.githubusercontent.com/59198442/170316366-c2023332-fbd0-4c18-83bc-e94177778637.jpg)

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

Make sure you have a private Binance API Key. This can be obtained by subscribing to binance [using my referral code here](https://accounts.binance.com/en/register?ref=186625161)

Also, instructions on how to get the API Key are described in the following article by Binance: [click here](https://www.binance.com/en/support/faq/360002502072)

We recommend to add the corresponding ```api_key``` and ```api_secret``` manually in line 23 and 24 of the file ```home.py```


###  Launch the app

```
streamlit run app.py
```

# Docker

The ```dockerfile``` contains all instructions on how the image was built

###  Pull the app in a Docker container

Pull a docker image from the [Docker Hub Repository](https://hub.docker.com/r/josecaloca/crypto_manager)

```
docker pull josecaloca/crypto_manager
```

## Run

### Run docker image

```
docker run -p 8501:8501 crypto_manager
```

### The app will be available locally on

http://localhost:8501


## Stop

### Lists containers
```
docker ps
```

Get **CONTAINER ID** from the **IMAGE** josecaloca/crypto_manager


### Stop running container
```
docker stop <CONTAINER ID>
```

### Delete the container
```
docker rm -f josecaloca/crypto_manager
```