import streamlit as st
from page_insight import show_insight
from page_info import show_info

page = st.sidebar.radio("Choose Option", ("Insight", "Data Information"))

if page == 'Insight':
    show_insight()
elif page == 'Data Information':
    show_info()