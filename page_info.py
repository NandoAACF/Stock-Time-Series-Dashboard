import streamlit as st
import pandas as pd

def show_info():
    st.title('Data Information')

    st.image('images/yahoo_finance.png')
    st.write('Data yang digunakan adalah data yang diambil dari Yahoo Finance mulai tanggal 1 September 2019 sampai sekarang.')
    st.write('Data ini berisi tentang saham BBRI. Ke depannya, akan ditambahkan data saham dari perusahaan lainnya dan user bisa memilih perusahaan yang diinginkan.')

    st.image('images/yfinance.png')
    st.write('Scraping Yahoo Finance menggunakan Python dengan library yfinance.')
    st.write('Ketika web ini dibuka, maka sistem akan langsung scraping data terbaru dari Yahoo Finance sehingga data selalu up to date.')

    st.markdown('## **Thank You 😀**')