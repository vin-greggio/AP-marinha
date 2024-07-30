import pandas as pd
import streamlit as st

xls = pd.ExcelFile('big planilha.xlsx')

st.set_page_config(page_title="Planilhas Marinha", page_icon="🌍")

st.sidebar.header("Planilhas")
