import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid
import plotly.graph_objects as go
import datetime as dt


def app():
    
    st.title('📈 Portfolio Manager')

    st.header('**Selected Price**')
    st.markdown('''
    #### 24 hour rolling window price change statistics
    ''')
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
    # Load market data from Binance API
    df = pd.read_json('https://api.binance.com/api/v3/ticker/24hr')
    df = df[df.symbol.str.contains('USDT')]


    # Custom function for rounding values
    def round_value(input_value):
        if input_value.values > 1:
            a = float(round(input_value, 2))
        else:
            a = float(round(input_value, 8))
        return a

    col1, col2, col3 = st.columns(3)

    # Widget (Cryptocurrency selection box)
    col1_selection = st.sidebar.selectbox('Crypto 1', df.symbol, list(df.symbol).index('BTCUSDT') )
    amount_col1 = st.sidebar.number_input('Insert amount of Crypto 1')

    col2_selection = st.sidebar.selectbox('Crypto 2', df.symbol, list(df.symbol).index('ETHUSDT') )
    amount_col2 = st.sidebar.number_input('Insert amount of Crypto 2')

    col3_selection = st.sidebar.selectbox('Crypto 3', df.symbol, list(df.symbol).index('BNBUSDT') )
    amount_col3 = st.sidebar.number_input('Insert amount of Crypto 3')

    col4_selection = st.sidebar.selectbox('Crypto 4', df.symbol, list(df.symbol).index('XRPUSDT') )
    amount_col4 = st.sidebar.number_input('Insert amount of Crypto 4')

    col5_selection = st.sidebar.selectbox('Crypto 5', df.symbol, list(df.symbol).index('SOLUSDT') )
    amount_col5 = st.sidebar.number_input('Insert amount of Crypto 5')

    col6_selection = st.sidebar.selectbox('Crypto 6', df.symbol, list(df.symbol).index('HBARUSDT') )
    amount_col6 = st.sidebar.number_input('Insert amount of Crypto 6')

    col7_selection = st.sidebar.selectbox('Crypto 7', df.symbol, list(df.symbol).index('AAVEUSDT') )
    amount_col7 = st.sidebar.number_input('Insert amount of Crypto 7')

    col8_selection = st.sidebar.selectbox('Crypto 8', df.symbol, list(df.symbol).index('ADAUSDT') )
    amount_col8 = st.sidebar.number_input('Insert amount of Crypto 8')

    col9_selection = st.sidebar.selectbox('Crypto 9', df.symbol, list(df.symbol).index('LUNAUSDT') )
    amount_col9 = st.sidebar.number_input('Insert amount of Crypto 9')


    # DataFrame of selected Cryptocurrency
    col1_df = df[df.symbol == col1_selection]
    col2_df = df[df.symbol == col2_selection]
    col3_df = df[df.symbol == col3_selection]
    col4_df = df[df.symbol == col4_selection]
    col5_df = df[df.symbol == col5_selection]
    col6_df = df[df.symbol == col6_selection]
    col7_df = df[df.symbol == col7_selection]
    col8_df = df[df.symbol == col8_selection]
    col9_df = df[df.symbol == col9_selection]

    # Apply a custom function to conditionally round values
    col1_price = round_value(col1_df.weightedAvgPrice)
    col2_price = round_value(col2_df.weightedAvgPrice)
    col3_price = round_value(col3_df.weightedAvgPrice)
    col4_price = round_value(col4_df.weightedAvgPrice)
    col5_price = round_value(col5_df.weightedAvgPrice)
    col6_price = round_value(col6_df.weightedAvgPrice)
    col7_price = round_value(col7_df.weightedAvgPrice)
    col8_price = round_value(col8_df.weightedAvgPrice)
    col9_price = round_value(col9_df.weightedAvgPrice)

    # Select the priceChangePercent column
    col1_percent = f'{float(col1_df.priceChangePercent)}%'
    col2_percent = f'{float(col2_df.priceChangePercent)}%'
    col3_percent = f'{float(col3_df.priceChangePercent)}%'
    col4_percent = f'{float(col4_df.priceChangePercent)}%'
    col5_percent = f'{float(col5_df.priceChangePercent)}%'
    col6_percent = f'{float(col6_df.priceChangePercent)}%'
    col7_percent = f'{float(col7_df.priceChangePercent)}%'
    col8_percent = f'{float(col8_df.priceChangePercent)}%'
    col9_percent = f'{float(col9_df.priceChangePercent)}%'

    # Create a metrics price box

    # update every 30 sec: this code works nicely when the app is 
    #from streamlit_autorefresh import st_autorefresh
    #st_autorefresh(interval= 1 * 30 * 1000, key="crypto_prices_refresh")

    #set function to show crypto prices when the app refreshes or the counter above trigers  
    def crypto_prices():
        col1.metric(col1_selection, col1_price, col1_percent) 
        col2.metric(col2_selection, col2_price, col2_percent)
        col3.metric(col3_selection, col3_price, col3_percent)
        col1.metric(col4_selection, col4_price, col4_percent)
        col2.metric(col5_selection, col5_price, col5_percent)
        col3.metric(col6_selection, col6_price, col6_percent)
        col1.metric(col7_selection, col7_price, col7_percent)
        col2.metric(col8_selection, col8_price, col8_percent)
        col3.metric(col9_selection, col9_price, col9_percent)
        
    # add a button so user can update prices at any time without waiting for the auto refresher
    if st.button('Get updated crypto prices'):
        crypto_prices()
    else:
        crypto_prices()

    ##########################
    # Add another section
    ##########################
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.header('**Portfolio Composition**')
    st.write("If you have inserted the amount of cryptocurrencies you are holding, you will be able to assess the value and composition and value of your portfolio")
    with st.expander("Click to Expand"):
        # label of cryptos of the portfolio
        cryptos =  [col1_selection, 
                    col2_selection, 
                    col3_selection,
                    col4_selection,
                    col5_selection,
                    col6_selection,
                    col7_selection,
                    col8_selection,
                    col9_selection]

        # value of the cryptos of the portfolio
        values= [amount_col1*col1_price,
                amount_col2*col2_price,
                amount_col3*col3_price,
                amount_col4*col4_price,
                amount_col5*col5_price,
                amount_col6*col6_price,
                amount_col7*col7_price,
                amount_col8*col8_price,
                amount_col9*col9_price]

        fig = go.Figure(
            go.Pie(
            labels = cryptos,
            values = values,
            hoverinfo = "label+percent",
            textinfo = "value"
        ))

        st.header("Share of Cryptocurrencies in the portfolio")
        st.metric("Portfolio value", "${:,.2f}".format(round(sum(values), 2)))
        st.plotly_chart(fig)


    ##########################
    # Add another section
    ##########################
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    now = dt.datetime.now().strftime("%d %B, %Y at %H:%M:%S sec")

    st.header(f'**All Crypto Prices on {now}**')

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=False,
        theme='dark', #Add theme color to the table
        enable_enterprise_modules=True,
        height=500, 
        width='100%',
        reload_data=True
    )

    data = grid_response['data']
    selected = grid_response['selected_rows'] 
    df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

    st.markdown('''
    ### **TODO**:

    - Add VaR of the portfolio
    - Add Fear and Greed Index

    Ideally:
    - Add cryptobot to operate on binance based on an algorithmic trading strategy
    ''')