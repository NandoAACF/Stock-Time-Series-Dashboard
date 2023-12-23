import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

@st.cache_data(ttl=60 * 60 * 24)
def load_data():
    ticker_symbol = 'BBRI.JK'

    ticker_data = yf.Ticker(ticker_symbol)

    # Dari 2019 - now
    ticker_df = ticker_data.history(period='1d', start='2019-1-1')

    ticker_df.head()

    stock_data = ticker_df.copy()

    stock_data.columns = map(str.lower, stock_data.columns)
    stock_data.index.name = stock_data.index.name.lower()

    return stock_data

stock_data = load_data()


def show_insight():
    st.title("BBRI Stock Time Series Analysis")

    st.write('Info: This data is automatically updated everyday.')

    st.markdown("### **Bagaimana tren saham BBRI sejak tahun 2019?**")

    plt.figure(figsize=(15, 12))

    # Time Series Plot of Closing Prices
    plt.subplot(3, 1, 1)
    plt.plot(stock_data.index, stock_data['close'], color='blue')
    plt.title('Closing Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.grid(True)

    # Plot of Trading Volume
    plt.subplot(3, 1, 2)
    plt.bar(stock_data.index, stock_data['volume'], color='orange')
    plt.title('Trading Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.grid(True)

    plt.subplot(3, 1, 3)
    stock_data['daily change'] = stock_data['close'].pct_change() * 100
    plt.plot(stock_data['daily change'], label='Daily % Change', color='green')
    plt.title('Daily Percentage Change in BBRI Stock Closing Price')
    plt.xlabel('Date')
    plt.ylabel('Percentage Change (%)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    st.pyplot(plt)


    st.markdown("### **Bagaimana moving average saham BBRI?**")

    stock_data['MA50'] = stock_data['close'].rolling(window=50).mean()
    stock_data['MA200'] = stock_data['close'].rolling(window=200).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['close'], label='Closing Price', color='blue', alpha=0.6)
    plt.plot(stock_data['MA50'], label='50-Day MA', color='red')
    plt.plot(stock_data['MA200'], label='200-Day MA', color='green')
    plt.title('BBRI Stock Closing Price with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)


    st.markdown("### **Bagaimana distribusi daily return saham BBRI?**")

    daily_returns = stock_data['close'].pct_change()

    plt.figure(figsize=(10, 6))
    sns.histplot(daily_returns, bins=50, kde=True, color='blue')
    plt.title('Distribution of BBRI Stock Daily Returns')
    plt.xlabel('Daily Return')
    plt.ylabel('Frequency')
    st.pyplot(plt)


    st.markdown("### **Bagaimana monthly return saham BBRI?**")
    monthly_returns = stock_data['close'].resample('M').ffill().pct_change()

    bar_colors = ['red' if x < 0 else 'green' for x in monthly_returns]

    monthly_returns.index = monthly_returns.index.strftime('%Y-%m')

    label_indices = range(0, len(monthly_returns), 3)

    plt.figure(figsize=(12, 6))
    monthly_returns.plot(kind='bar', color=bar_colors)
    plt.title('BBRI Stock Monthly Returns')
    plt.xlabel('Month')
    plt.ylabel('Monthly Return')
    plt.xticks(ticks=label_indices, labels=[monthly_returns.index[i] for i in label_indices], rotation=45)
    plt.axhline(y=0, color='gray', linestyle='--')
    plt.tight_layout()
    plt.grid(True)
    st.pyplot(plt)


    st.markdown("### **Bagaimana yearly return saham BBRI?**")

    yearly_returns = stock_data['close'].resample('Y').ffill().pct_change()
    yearly_returns = yearly_returns.dropna()

    bar_colors = ['red' if x < 0 else 'green' for x in yearly_returns]

    yearly_returns.index = yearly_returns.index.strftime('%Y')

    plt.figure(figsize=(9, 5))
    yearly_returns.plot(kind='bar', color=bar_colors)
    plt.title('BBRI Stock Yearly Returns')
    plt.xlabel('Year', fontsize=13)
    plt.ylabel('Yearly Return')
    plt.axhline(y=0, color='gray', linestyle='--')
    plt.grid(True)
    st.pyplot(plt)


    st.markdown("### **Bagaimana kestabilan saham BBRI?**")

    rolling_volatility = daily_returns.rolling(window=30).std()

    plt.figure(figsize=(12, 6))
    rolling_volatility.plot(color='darkred')
    plt.title('BBRI Stock 30-Day Rolling Volatility')
    plt.xlabel('Date')
    plt.ylabel('Rolling Standard Deviation')
    st.pyplot(plt)


    st.markdown("### **Bagaimana bollinger bands saham BBRI?**")

    stock_data['SMA20'] = stock_data['close'].rolling(window=20).mean()  # 20-day Simple Moving Average
    stock_data['Upper Band'] = stock_data['SMA20'] + (stock_data['close'].rolling(window=20).std() * 2)
    stock_data['Lower Band'] = stock_data['SMA20'] - (stock_data['close'].rolling(window=20).std() * 2)

    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['close'], label='Closing Price', color='blue', alpha=0.5)
    plt.plot(stock_data['SMA20'], label='20-Day SMA', color='orange')
    plt.plot(stock_data['Upper Band'], label='Upper Band', color='green')
    plt.plot(stock_data['Lower Band'], label='Lower Band', color='red')
    plt.fill_between(stock_data.index, stock_data['Upper Band'], stock_data['Lower Band'], color='gray', alpha=0.1)
    plt.title('BBRI Stock Price and Bollinger Bands')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)


    # st.markdown("## **Kesimpulan**")