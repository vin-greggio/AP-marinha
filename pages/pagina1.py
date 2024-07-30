import pandas as pd
import streamlit as st

xls = pd.ExcelFile('big planilha.xlsx')
planilha = pd.read_excel(xls, sheet_name='Demonstrativo Fevereiro')

st.dataframe(planilha)
