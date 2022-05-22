import streamlit as st
import plotly.express as px
from binance.client import Client

# from crypto_portfolio_manager.  # import  #import to_excel
import pandas as pd
import datetime as dt
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb


def app():
    st.title("📉 Historical Crypto Prices")
    # set columns
    column1, column2 = st.columns(2)
    # crrate list of crypto symbols
    df = pd.read_json("https://api.binance.com/api/v3/ticker/24hr")
    df = df[df.symbol.str.contains("USDT")]
    crypto_symbols = df["symbol"].to_list()

    # Set conection to Binance API
    api_key = "nndIDRzmcgSGMrLvcs0VI6mmXBF4uVURog4YcfZuPBLEbvNQHbw66FgxGaLwL6Ca"
    api_secret = "AePEYUZgxvC3gbEKO9mYF9XqP6lCdm6S0VsKoe3pDqIMEXpc9eGdkBExOLqim9Fl"
    client = Client(api_key, api_secret)

    # set intervals for downloading historical data from Binance API
    intervals = (
        Client.KLINE_INTERVAL_1MINUTE,
        Client.KLINE_INTERVAL_30MINUTE,
        Client.KLINE_INTERVAL_1WEEK,
    )

    intervals_option = {
        Client.KLINE_INTERVAL_1MINUTE: "1 minute",
        Client.KLINE_INTERVAL_30MINUTE: "30 minutes",
        Client.KLINE_INTERVAL_1WEEK: "1 week",
    }

    # Different metrics to display
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

    now = dt.datetime.now().strftime("%d %B, %Y at %H:%M:%S sec")

    # Add widgets to the webapp
    option = column1.selectbox(
        "Select Cryptocurrency to visualise",
        crypto_symbols,
        crypto_symbols.index("ETHUSDT"),
    )

    metric = column1.selectbox("Select metric", metric_plot, metric_plot.index("close"))

    start = column2.date_input("Input start date", dt.date(2021, 1, 1)).strftime(
        "%d %B, %Y"
    )

    end = column2.date_input("Input end date", dt.date(2021, 12, 31)).strftime(
        "%d %B, %Y"
    )

    interval = st.radio(
        "Select interval", intervals, format_func=lambda x: intervals_option.get(x)
    )

    # pull historical data from binance API
    def pull_data(
        option="ETHUSDT",
        interval=Client.KLINE_INTERVAL_1WEEK,
        start="1 Jan, 2021",
        end="31 Dec, 2021",
        metric="close",
    ):

        klines = client.get_historical_klines(option, interval, start, end)
        data = pd.DataFrame(klines)
        # create colums name
        data.columns = metric_plot
        # change the type of variables from object to float
        for col in data.columns:
            data[col] = data[col].astype(float)
        # change to datetime type
        data.close_time = pd.to_datetime(data.close_time, unit="ms")
        data.open_time = pd.to_datetime(data.open_time, unit="ms")

        # Plot historical data
        fig = px.line(
            data,  # Data Frame
            x="close_time",  # Columns from the data frame
            y=metric,
            title=f"{option.rstrip('USDT')} {metric} over time",
            width=1000,
            template="simple_white",
        )
        fig.update_traces(line_color="maroon")
        st.plotly_chart(fig)
        return data

    if st.button("Get Graph"):
        data = pull_data(option, interval, start, end, metric)
    else:
        data = pull_data()
    df_xlsx = to_excel(data)

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv()

    csv = convert_df(data)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.download_button(
            label="📥 Download Data (.xlsx)",
            data=df_xlsx,
            file_name=f"All Crypto Prices on {now}.xlsx",
            key=1,
        )
    with col2:
        st.download_button(
            label="📥 Download Data (.csv)",
            data=csv,
            file_name="crypto_data.csv",
            mime="text/csv",
            key=2,
        )
