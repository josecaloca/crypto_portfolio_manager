import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid
import plotly.graph_objects as go
import datetime as dt
from binance.client import Client
import numpy as np
from scipy.stats import norm
import plotly.express as px
from io import BytesIO
#from pyxlsb import open_workbook as open_xlsb


def app():

    st.title("📈 Portfolio Manager")

    st.header("**Selected Price**")
    st.markdown(
        """
    #### 24 hour rolling window price change statistics
    """
    )
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    # Load market data from Binance API
    df = pd.read_json("https://api.binance.com/api/v3/ticker/24hr")
    df = df[df.symbol.str.contains("USDT")]

    # Custom function for rounding values
    def round_value(input_value):
        if input_value.values > 1:
            a = float(round(input_value, 2))
        else:
            a = float(round(input_value, 8))
        return a

    col1, col2, col3 = st.columns(3)

    # Widget (Cryptocurrency selection box)
    col1_selection = st.sidebar.selectbox(
        "Crypto 1", df.symbol, list(df.symbol).index("BTCUSDT")
    )
    amount_col1 = st.sidebar.number_input("Insert amount of Crypto 1", min_value=0)

    col2_selection = st.sidebar.selectbox(
        "Crypto 2", df.symbol, list(df.symbol).index("ETHUSDT")
    )
    amount_col2 = st.sidebar.number_input("Insert amount of Crypto 2", min_value=0)

    col3_selection = st.sidebar.selectbox(
        "Crypto 3", df.symbol, list(df.symbol).index("BNBUSDT")
    )
    amount_col3 = st.sidebar.number_input("Insert amount of Crypto 3", min_value=0)

    col4_selection = st.sidebar.selectbox(
        "Crypto 4", df.symbol, list(df.symbol).index("XRPUSDT")
    )
    amount_col4 = st.sidebar.number_input("Insert amount of Crypto 4", min_value=0)

    col5_selection = st.sidebar.selectbox(
        "Crypto 5", df.symbol, list(df.symbol).index("SOLUSDT")
    )
    amount_col5 = st.sidebar.number_input("Insert amount of Crypto 5", min_value=0)

    col6_selection = st.sidebar.selectbox(
        "Crypto 6", df.symbol, list(df.symbol).index("HBARUSDT")
    )
    amount_col6 = st.sidebar.number_input("Insert amount of Crypto 6", min_value=0)

    col7_selection = st.sidebar.selectbox(
        "Crypto 7", df.symbol, list(df.symbol).index("AAVEUSDT")
    )
    amount_col7 = st.sidebar.number_input("Insert amount of Crypto 7", min_value=0)

    col8_selection = st.sidebar.selectbox(
        "Crypto 8", df.symbol, list(df.symbol).index("ADAUSDT")
    )
    amount_col8 = st.sidebar.number_input("Insert amount of Crypto 8", min_value=0)

    col9_selection = st.sidebar.selectbox(
        "Crypto 9", df.symbol, list(df.symbol).index("LUNAUSDT")
    )
    amount_col9 = st.sidebar.number_input("Insert amount of Crypto 9", min_value=0)

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
    col1_percent = f"{float(col1_df.priceChangePercent)}%"
    col2_percent = f"{float(col2_df.priceChangePercent)}%"
    col3_percent = f"{float(col3_df.priceChangePercent)}%"
    col4_percent = f"{float(col4_df.priceChangePercent)}%"
    col5_percent = f"{float(col5_df.priceChangePercent)}%"
    col6_percent = f"{float(col6_df.priceChangePercent)}%"
    col7_percent = f"{float(col7_df.priceChangePercent)}%"
    col8_percent = f"{float(col8_df.priceChangePercent)}%"
    col9_percent = f"{float(col9_df.priceChangePercent)}%"

    # Create a metrics price box

    # update every 30 sec: this code works nicely when the app is
    # from streamlit_autorefresh import st_autorefresh
    # st_autorefresh(interval= 1 * 30 * 1000, key="crypto_prices_refresh")

    # set function to show crypto prices when the app refreshes or the counter above trigers
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
    if st.button("Get updated crypto prices"):
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
    st.header("**Portfolio Analytics**")
    st.write(
        "If you have inserted the amount of cryptocurrencies you are holding, you will be able to assess the value and composition and value of your portfolio"
    )
    with st.expander("Click to Expand"):
        # Set API conection
        api_key = "nndIDRzmcgSGMrLvcs0VI6mmXBF4uVURog4YcfZuPBLEbvNQHbw66FgxGaLwL6Ca"
        api_secret = "AePEYUZgxvC3gbEKO9mYF9XqP6lCdm6S0VsKoe3pDqIMEXpc9eGdkBExOLqim9Fl"
        client = Client(api_key, api_secret)

        # label of cryptos of the portfolio
        cryptos = [
            col1_selection,
            col2_selection,
            col3_selection,
            col4_selection,
            col5_selection,
            col6_selection,
            col7_selection,
            col8_selection,
            col9_selection,
        ]

        # value of the cryptos of the portfolio
        actual_values = [
            amount_col1 * col1_price,
            amount_col2 * col2_price,
            amount_col3 * col3_price,
            amount_col4 * col4_price,
            amount_col5 * col5_price,
            amount_col6 * col6_price,
            amount_col7 * col7_price,
            amount_col8 * col8_price,
            amount_col9 * col9_price,
        ]

        # start investment date
        start = st.date_input("Input start date", dt.date(2021, 1, 1)).strftime(
            "%d %B, %Y"
        )
        # until today
        end = dt.datetime.now().strftime("%d %B, %Y")

        @st.cache
        def pull_live_data():
            # Download initial values of the cryptos
            # set empty list for storing data from the 'for loop'
            close_prices = []

            for crypto in cryptos:

                # retrieve historical data from API
                klines = client.get_historical_klines(
                    crypto, Client.KLINE_INTERVAL_1DAY, start, end
                )
                # create dataframe
                data = pd.DataFrame(klines)
                # Add column names
                metric_plot = [
                    "open_time",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "close_time",
                    "qav",
                    "num_trades",
                    "taker_base_vol",
                    "taker_quote_vol",
                    "ignore",
                ]
                data.columns = metric_plot
                # get close price
                close = data["close"]
                close_prices.append(close)

            # get historical data for all cryptos
            historical_data = pd.DataFrame(close_prices).T
            historical_data.columns = cryptos
            # change the type of variables from object to float
            for col in historical_data.columns:
                historical_data[col] = historical_data[col].astype(float)

            return historical_data

        # call function defined above
        historical_data = pull_live_data()
        # list of amount investment from the sidebar
        invested_amount = [
            amount_col1,
            amount_col2,
            amount_col3,
            amount_col4,
            amount_col5,
            amount_col6,
            amount_col7,
            amount_col8,
            amount_col9,
        ]

        # create a function for calculating daily value at risk
        def calculate_var():

            # get initial prices
            initial_values = historical_data.loc[0, :].to_list()
            # calculate the value of the cryptos at the itial time (t0)
            initial_portfolio_value = [
                a * b for a, b in zip(initial_values, invested_amount)
            ]
            # calculate the amount of the initial investment
            initial_investment = sum(initial_portfolio_value)

            # Calculate weights of assets in the portfolio
            weights = [i / initial_investment for i in initial_portfolio_value]
            weights = np.array(weights)
            # From the closing prices, calculate periodic returns
            returns = historical_data.pct_change()

            # calculate covariance matrix
            cov_matrix = returns.cov()

            # Calculate mean returns for each crypto
            avg_rets = returns.mean()

            # Calculate mean returns for portfolio overall, using dot product to normalize individual means against investment weights
            port_mean = avg_rets.dot(weights)

            # Calculate portfolio standard deviation
            port_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))

            # Calculate mean of investment
            mean_investment = (1 + port_mean) * initial_investment

            # Calculate standard deviation of investmnet
            stdev_investment = initial_investment * port_stdev

            # Select our confidence interval (I'll choose 95% here)
            conf_level1 = 0.05

            # Using SciPy ppf method to generate values for the
            # inverse cumulative distribution function to a normal distribution
            # Plugging in the mean, standard deviation of our portfolio
            # as calculated above
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html

            cutoff1 = norm.ppf(conf_level1, mean_investment, stdev_investment)

            # Finally, we can calculate the VaR at our confidence interval
            var_1d1 = initial_investment - cutoff1

            return var_1d1, initial_investment, returns

        if sum(invested_amount) > 0:
            var_1d1, initial_investment, returns = calculate_var()

            VaR = "${:,.2f}".format(round(var_1d1, 2))
            current_portfolio_value = round(sum(actual_values), 2)
            current_portfolio_value_format = "${:,.2f}".format(current_portfolio_value)
            initial_investment_format = "${:,.2f}".format(initial_investment)

            pct_change_portfolio_value = round(
                ((current_portfolio_value - initial_investment) / initial_investment)
                * 100,
                2,
            )
            pct_change_portfolio_value = f"{pct_change_portfolio_value}%"
            profit = current_portfolio_value - initial_investment
            profit = "${:,.2f}".format(profit)

            column1, column2 = st.columns(2)

            column1.metric("Initial investment", initial_investment_format)
            column1.metric("Current Portfolio Value", current_portfolio_value_format)
            column2.metric("Profit", profit, pct_change_portfolio_value)
            column2.metric("Value at Risk", VaR)

            st.write(
                "Here we are saying with 95 percent confidence that our portfolio of",
                current_portfolio_value_format,
            )
            st.write(
                "will not exceed losses greater than", VaR, "over a one day period"
            )
            st.write("")
            st.write("")
            st.write("")
            st.write("")

            st.markdown(
                """
                
                There are two main ways to calculate VaR:
                - Using Monte Carlo simulation
                - Using the variance-covariance method
                \\
                \\
                We focus on the **variance-covariance method**.
                \\
                In short, the **variance-covariance method** looks at historical price movements (standard deviation, mean price) 
                of a given equity or portfolio of equities over a specified lookback period, 
                and then uses probability theory to calculate the maximum loss within the specified confidence interval, 
                which in this case is 95%.
                \\
                \\
                For calculating the Value at Risk we assume the returns of the portfolio to be normally distributed. 
                This is of course not realistic for most assets, but allows us to develop a baseline using a much more simplistic calculation.
                \\
                """
            )

            ########################################

            st.header("Share of Cryptocurrencies in the portfolio")
            # Pie chart
            fig = go.Figure(
                go.Pie(
                    labels=cryptos,
                    values=actual_values,
                    hoverinfo="label+percent",
                    textinfo="value",
                    hole=0.15,
                )
            )

            fig.update_traces(
                hoverinfo="label+percent",
                textinfo="value",
                marker=dict(line=dict(color="#000000", width=2)),
            )

            st.plotly_chart(fig)

            ########################################

            st.header("Estimation of VaR in time")
            # Estimate the VaR in time

            num_days = st.number_input(
                "Inser number of days", min_value=0, step=1, value=15
            )

            # create a list of days upfront
            base = dt.datetime.today()
            date_list = [base + dt.timedelta(days=x) for x in range(num_days)]

            var_array = []
            for day in range(1, num_days + 1):
                var_array.append(np.round(var_1d1 * np.sqrt(day), 2))

            # create dataframe
            var_future = pd.DataFrame(dict(days=date_list, var=var_array))

            fig = px.line(
                var_future,  # Data Frame
                x="days",  # Columns from the data frame
                y="var",
                title=f"Max portfolio loss (VaR) over {num_days}-day period",
                width=1000,
                template="simple_white",
            )

            fig.update_traces(line_color="maroon")
            st.plotly_chart(fig)

            ########################################
            st.header("Analysis of distribution of the assets in the portfolio")

            for col in returns.columns:
                fig = px.histogram(
                    returns,
                    x=col,
                    width=1000,
                    template="simple_white",
                    color_discrete_sequence=["maroon"],
                )
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

    st.header(f"**All Crypto Prices on {now}**")
    # add a button so user can download the data
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine="xlsxwriter")
        df.to_excel(writer, index=False, sheet_name="Sheet1")
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]
        format1 = workbook.add_format({"num_format": "0.00"})
        worksheet.set_column("A:A", None, format1)
        writer.save()
        processed_data = output.getvalue()
        return processed_data

    df_xlsx = to_excel(df)
    st.download_button(
        label="📥 Download Data (.xlsx)",
        data=df_xlsx,
        file_name=f"All Crypto Prices on {now}.xlsx",
    )
    # add a button so user can update prices at any time without waiting for the auto refresher
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
    gb.configure_side_bar()  # Add a sidebar
    gb.configure_selection(
        "multiple",
        use_checkbox=True,
        groupSelectsChildren="Group checkbox select children",
    )  # Enable multi-row selection
    gridOptions = gb.build()
    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode="AS_INPUT",
        update_mode="MODEL_CHANGED",
        fit_columns_on_grid_load=False,
        theme="dark",  # Add theme color to the table
        enable_enterprise_modules=True,
        height=500,
        width="100%",
        reload_data=True,
    )

    selected = grid_response["selected_rows"]
    df = pd.DataFrame(selected)  # Pass the selected rows to a new dataframe df

    st.markdown(
        """
    ### **TODO**:

    - Add Fear and Greed Index

    Ideally:
    - Add cryptobot to operate on binance based on an algorithmic trading strategy
    """
    )
