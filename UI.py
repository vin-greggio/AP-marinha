import pandas as pd
import streamlit as st

xls = pd.ExcelFile('big planilha.xlsx')

st.set_page_config(page_title="Planilhas Marinha", page_icon="🌍")

st.sidebar.header("Planilhas")

with st.form("Formulário de empréstimo"):
   st.write("Insira as informações do novo empréstimo")
   nome_emprestimo = st.text_input('Nome')
   valor_emprestimo = st.text_input('Valor')
   tempo_meses = st.text_input('Meses')
   st.form_submit_button('Criar empréstimo')