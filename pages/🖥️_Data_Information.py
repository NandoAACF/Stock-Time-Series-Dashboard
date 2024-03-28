import streamlit as st
import pandas as pd

st.set_page_config(page_title='Data Information', page_icon='🖥️')

st.title('🖥️ Data Information')

col1, col2 = st.columns([0.8, 0.2])
col1.image('images/yahoo_finance.png')
st.write('Data di-scraping dari Yahoo Finance mulai tanggal 1 Januari 2019 sampai sekarang.')
st.write('Feature-nya berupa Date, Open, High, Low, Close, Volume, dan Dividen.')
st.write('User dapat memasukkan kode ticker saham yang ingin dianalisis. Program akan memvisualisasikan analisis dari data saham sesuai keinginan user.')

st.image('images/yfinance.png')
st.write('Scraping Yahoo Finance menggunakan Python dengan library yfinance.')
st.write('Ketika user mengakses dashboard ini, maka sistem akan langsung scraping data terbaru dari Yahoo Finance sehingga data selalu up to date.')

st.markdown('## **Thank You 😀**')