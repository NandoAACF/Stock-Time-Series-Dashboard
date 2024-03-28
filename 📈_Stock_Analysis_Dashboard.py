import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import mplfinance as mpf
from pandas.plotting import autocorrelation_plot
import datetime

st.set_page_config(page_title='Stock Analysis Dashboard', page_icon='📈')

def show_insight():

    st.title('📈 Stock Time Series Dashboard')

    st.info("📜 Kode ticker saham dapat dilihat di link spreadsheet ini: https://docs.google.com/spreadsheets/d/1w6mSKJw38ZMTJ3Jwc1Mlvdr8WVtcuH0f/edit?usp=sharing&ouid=103372145316556844007&rtpof=true&sd=true")

    ticker_symbol = st.text_input('Masukkan kode ticker saham yang ingin dianalisis: (contoh: BBCA.JK)')

    # Filter date range
    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.date.today()

    selected_dates = st.slider("Pilih rentang tanggal yang diinginkan:", start_date, end_date, (start_date, end_date), format="MM/DD/YYYY")
    # analyze = st.button('Analyze')

    if ticker_symbol == '':
        st.warning('📢 Silakan masukkan kode ticker saham terlebih dahulu.')
        return
    else:
        try:
            ticker_data = yf.Ticker(ticker_symbol)
            ticker_df = ticker_data.history(period='1d', start=selected_dates[0], end=selected_dates[1])
            ticker_df.head()
            last_update = ticker_df.index[-1].strftime('%d %B %Y')
            nama_saham = ticker_data.info['longName']
        except:
            st.write('Kode ticker saham tidak ditemukan.')
            return

        stock_data = ticker_df.copy()

        stock_data.columns = map(str.lower, stock_data.columns)
        stock_data.index.name = stock_data.index.name.lower()

        st.markdown(f"# **Saham {nama_saham}**")

        st.write('Info: Data saham otomatis diperbarui setiap hari.')
        st.write('Last updated:', last_update)

        st.markdown(f"### **Bagaimana tren saham {nama_saham}?**")

        plt.figure(figsize=(15, 12))

        plt.subplot(3, 1, 1)
        plt.plot(stock_data.index, stock_data['close'], color='blue')
        plt.title('Closing Price Over Time')
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.grid(True)

        plt.subplot(3, 1, 2)
        plt.bar(stock_data.index, stock_data['volume'], color='orange')
        plt.title('Trading Volume Over Time')
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.grid(True)

        plt.subplot(3, 1, 3)
        stock_data['daily change'] = stock_data['close'].pct_change() * 100
        plt.plot(stock_data['daily change'], label='Daily % Change', color='green')
        plt.title('Daily Percentage Change of Stock Closing Price')
        plt.xlabel('Date')
        plt.ylabel('Percentage Change (%)')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        st.pyplot(plt)

        with st.expander("📋 Penjelasan Chart"):
            st.info("Chart di atas menunjukkan tren harga penutupan saham, volume perdagangan, dan persentase perubahan harian harga penutupan saham.")


        st.markdown(f"### **Bagaimana candlestick saham {nama_saham}?**")

        plt.figure(figsize=(12, 6))

        len_data = len(stock_data)
        selected_period = st.slider('Ingin menampilkan data dari berapa hari terakhir?', 1, len_data, 60)

        negative_len_data = selected_period * -1
        subset_data = stock_data[negative_len_data:]

        mpf.plot(subset_data, type='candle', style='charles', title=f'Candlestick Chart (Last {selected_period} Days)', volume=True, mav=(20), figsize=(12, 6), show_nontrading=False)
        st.pyplot(plt)

        with st.expander("📋 Penjelasan Chart"):
            st.info("Candlestick chart adalah grafik yang digunakan untuk menunjukkan harga pembukaan, penutupan, tertinggi, dan terendah saham dalam satu periode tertentu.")


        st.markdown(f"### **Bagaimana moving average saham {nama_saham}?**")

        stock_data['MA50'] = stock_data['close'].rolling(window=50).mean()
        stock_data['MA200'] = stock_data['close'].rolling(window=200).mean()

        plt.figure(figsize=(12, 6))
        plt.plot(stock_data['close'], label='Closing Price', color='blue', alpha=0.6)
        plt.plot(stock_data['MA50'], label='50-Day MA', color='red')
        plt.plot(stock_data['MA200'], label='200-Day MA', color='green')
        plt.title('Stock Closing Price with Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        with st.expander("📋 Penjelasan Chart"):
            st.info("Moving average adalah indikator yang digunakan untuk mengidentifikasi tren harga saham berdasarkan rata-rata dari sejumlah nilai periodis (50 hari atau 200 hari). Tujuannya untuk meratakan fluktuasi jangka pendek dalam data dan menyoroti tren jangka panjang dengan menghilangkan komponen acak atau noise dari data. Dengan begitu, MA dapat digunakan untuk mengidentifikasi apakah trennya akan bergerak naik atau turun.")


        st.markdown(f"### **Bagaimana distribusi daily return saham {nama_saham}?**")

        daily_returns = stock_data['close'].pct_change()

        plt.figure(figsize=(10, 6))
        sns.histplot(daily_returns, bins=50, kde=True, color='blue')
        plt.title('Distribution of Stock Daily Returns')
        plt.xlabel('Daily Return')
        plt.ylabel('Frequency')
        st.pyplot(plt)

        with st.expander("📋 Penjelasan Chart"):
            st.info("Distribusi daily return saham di atas menunjukkan seberapa sering dan seberapa besar perubahan harga saham setiap hari. Investor menjadi tahu apakah saham tersebut lebih sering turun atau naik dibandingkan hari sebelumnya.")


        st.markdown(f"### **Bagaimana monthly return saham {nama_saham}?**")
        monthly_returns = stock_data['close'].resample('M').ffill().pct_change()

        bar_colors = ['red' if x < 0 else 'green' for x in monthly_returns]

        monthly_returns.index = monthly_returns.index.strftime('%Y-%m')

        label_indices = range(0, len(monthly_returns), 3)

        plt.figure(figsize=(12, 6))
        monthly_returns.plot(kind='bar', color=bar_colors)
        plt.title('Stock Monthly Returns')
        plt.xlabel('Month')
        plt.ylabel('Monthly Return')
        plt.xticks(ticks=label_indices, labels=[monthly_returns.index[i] for i in label_indices], rotation=45)
        plt.axhline(y=0, color='gray', linestyle='--')
        plt.tight_layout()
        plt.grid(True)
        st.pyplot(plt)

        with st.expander("📋 Penjelasan Chart"):
            st.info("Monthly return adalah ukuran yang digunakan untuk mengukur seberapa besar nilai sebuah saham berubah dari satu bulan ke bulan berikutnya. Di pasar saham, investor dan analis menggunakan monthly return untuk memahami seberapa volatil atau stabil performa sebuah saham dalam jangka waktu bulanan.")


        st.markdown(f"### **Bagaimana yearly return saham {nama_saham}?**")

        yearly_returns = stock_data['close'].resample('Y').ffill().pct_change()
        yearly_returns = yearly_returns.dropna()

        bar_colors = ['red' if x < 0 else 'green' for x in yearly_returns]

        yearly_returns.index = yearly_returns.index.strftime('%Y')

        plt.figure(figsize=(9, 5))
        yearly_returns.plot(kind='bar', color=bar_colors)
        plt.title('Stock Yearly Returns')
        plt.xlabel('Year', fontsize=13)
        plt.ylabel('Yearly Return')
        plt.axhline(y=0, color='gray', linestyle='--')
        plt.grid(True)
        st.pyplot(plt)

        with st.expander("📋 Penjelasan Chart"):
            st.info("Yearly return adalah ukuran yang digunakan untuk mengukur seberapa besar nilai sebuah saham berubah dari satu tahun ke tahun berikutnya. Dengan begitu, investor dapat mengevaluasi kinerja investasi mereka dalam jangka waktu yang lebih panjang.")


        st.markdown(f"### **Bagaimana distribusi persentase monthly change saham {nama_saham}?**")

        monthly_change_data = stock_data['close'].resample('M').last().pct_change() * 100

        plt.figure(figsize=(10, 6))
        sns.boxplot(x=monthly_change_data.dropna(), color='orange')
        plt.title('Box Plot of Monthly Price Changes')
        plt.xlabel('Percentage Change (%)')
        plt.grid(True)
        st.pyplot(plt)

        with st.expander("📋 Penjelasan Chart"):
            st.info("Box plot digunakan untuk menunjukkan distribusi persentase perubahan harga saham setiap bulan. Box plot menunjukkan median, kuartil, dan rentang data. Dengan begitu, investor dapat mengetahui seberapa besar fluktuasi harga saham setiap bulan.")


        st.markdown(f"### **Bagaimana distribusi persentase yearly change saham {nama_saham}?**")

        plt.figure(figsize=(12, 6))
        autocorrelation_plot(stock_data['close'], color='blue')
        plt.title('Autocorrelation of Daily Closing Prices')
        plt.xlabel('Lags')
        plt.ylabel('Autocorrelation')
        plt.grid(True)
        st.pyplot(plt)

        with st.expander("📋 Penjelasan Chart"):
            st.info("Autocorrelation plot digunakan untuk menunjukkan seberapa berkaitan nilai harga saham pada suatu rentang waktu. Lags pada sumbu x menunjukkan jumlah perbedaan harinya. Jika nilainya 1, artinya harga saham pada suatu rentang waktu (lags) sangat berkaitan. Sebaliknya, jika nilainya mendekati 0, artinya harga saham dalam rentang waktu tersebut tidak saling berkaitan.")


        st.markdown(f"### **Bagaimana kestabilan saham {nama_saham}?**")

        rolling_volatility = daily_returns.rolling(window=30).std()

        plt.figure(figsize=(12, 6))
        rolling_volatility.plot(color='darkred')
        plt.title('Stock 30-Day Rolling Volatility')
        plt.xlabel('Date')
        plt.ylabel('Rolling Standard Deviation')
        st.pyplot(plt)

        with st.expander("📋 Penjelasan Chart"):
            st.info("30-day rolling volatility menunjukkan seberapa besar fluktuasi harga saham dalam jangka waktu setiap 30 hari. Dengan begitu, investor dapat mengetahui seberapa volatil saham tersebut dalam jangka waktu tertentu. Jika angkanya cukup besar, artinya ada lonjakan volatilitas harga saham dalam jangka waktu tersebut. Jika mendekati 0, artinya harga saham cukup stabil.")


        st.markdown(f"### **Bagaimana bollinger bands saham {nama_saham}?**")

        len_data = len(stock_data)
        selected_period_bollinger = st.slider('Ingin menampilkan bollinger bands sejak berapa hari terakhir?', 1, len_data, 150)

        negative_len_data_bollinger = selected_period_bollinger * -1
        subset_data_bollinger = stock_data[negative_len_data_bollinger:]

        subset_data_bollinger['SMA20'] = subset_data_bollinger['close'].rolling(window=20).mean()  # 20-day Simple Moving Average
        subset_data_bollinger['Upper Band'] = subset_data_bollinger['SMA20'] + (subset_data_bollinger['close'].rolling(window=20).std() * 2)
        subset_data_bollinger['Lower Band'] = subset_data_bollinger['SMA20'] - (subset_data_bollinger['close'].rolling(window=20).std() * 2)

        plt.figure(figsize=(12, 6))
        plt.plot(subset_data_bollinger['close'], label='Closing Price', color='blue', alpha=0.5)
        plt.plot(subset_data_bollinger['SMA20'], label='20-Day SMA', color='orange')
        plt.plot(subset_data_bollinger['Upper Band'], label='Upper Band', color='green')
        plt.plot(subset_data_bollinger['Lower Band'], label='Lower Band', color='red')
        plt.fill_between(subset_data_bollinger.index, subset_data_bollinger['Upper Band'], subset_data_bollinger['Lower Band'], color='gray', alpha=0.1)
        plt.title('Stock Price and Bollinger Bands')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        with st.expander("📋 Penjelasan Chart"):
            st.info("Bollinger Bands adalah alat analisis teknikal yang digunakan dalam analisis saham untuk mengukur potensi titik balik harga. Bollinger Bands membantu investor untuk mengidentifikasi apakah harga saham sedang overbought (terlalu tinggi) atau oversold (terlalu rendah) pada suatu periode waktu. Ketika harga saham mendekati upper band, itu bisa menjadi sinyal bahwa harga saham mungkin terlalu tinggi dan akan turun, sementara ketika harga saham mendekati lower band, artinya harga saham mungkin terlalu rendah dan akan segera naik.")


        st.markdown(f"### **Bagaimana pembagian dividen saham {nama_saham}?**")
        plt.figure(figsize=(12, 6))
        plt.plot(stock_data['dividends'], label='Dividends', color='purple', marker='o')
        plt.title('Stock Dividends Over Time')
        plt.xlabel('Date')
        plt.ylabel('Dividend Amount (in Rupiah)')
        plt.legend()
        st.pyplot(plt)

        with st.expander("📋 Penjelasan Chart"):
            st.info("Chart di atas menunjukkan besar pembagian dividen saham dari waktu ke waktu. Dividen adalah pembagian laba perusahaan kepada pemegang saham.")

show_insight()