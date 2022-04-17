from turtle import width
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np


def app():
    st.title('🔥 Gainers and Lossers')

    def gainers_and_losers():

        df = pd.read_json('https://api.binance.com/api/v3/ticker/24hr')
        df = df[df.symbol.str.contains('USDT')]

        def round_value(input_value):
            if input_value.values > 1:
                a = float(round(input_value, 2))
            else:
                a = float(round(input_value, 8))
            return a

        sorted_df = df.sort_values('priceChangePercent',ascending=True)
        top = sorted_df.head(5)
        bottom = sorted_df.tail(5)
        losers_and_gainers = pd.concat([top, bottom], axis=0)
        coins = losers_and_gainers['symbol'].to_list()
        col1, col2 = st.columns(2)

        pct_change = []

        for count, coin in enumerate(coins):
            # DataFrame of selected Cryptocurrency
            col_df = losers_and_gainers[losers_and_gainers.symbol == coin]
            # Apply a custom function to conditionally round values
            col_price = round_value(col_df.weightedAvgPrice)
            # Select the priceChangePercent column
            col_percent = f'{float(col_df.priceChangePercent)}%'

            pct_change.append(float(col_df.priceChangePercent))

            if count < 5:
                col1.metric(coin, col_price, col_percent)
            else: 
                col2.metric(coin, col_price, col_percent)

        plot_data = pd.DataFrame(pct_change, coins).reset_index().rename(columns={'index':'symbol', 0:'pct_change'})
    #plot_data.transpose()

        plot_data['colour'] = np.where(plot_data['pct_change'] < 0, 'red', 'green')

        fig = go.Figure()

        fig.update_layout(title="Gainers and Losers Cryptocurrencies",
                        template='simple_white',
                        width = 1000,
                        xaxis_tickfont_size=14,
                        yaxis=dict(
                title='Percentage Change %',
                titlefont_size=16,
                tickfont_size=14,
            ))

        fig.add_trace(go.Bar(x=plot_data['symbol'], 
                            y=plot_data['pct_change'],
                            marker_color=plot_data['colour'],
                            name='expenses'))

        st.plotly_chart(fig)


    if st.button('Get updated crypto prices'):
        gainers_and_losers()
    else:
        gainers_and_losers()
