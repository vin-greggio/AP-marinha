
import streamlit as st
import hashlib
import json
import os
import pandas as pd
from PyPDF2 import PdfFileReader

emprestimo = 0
planilhas = 0

with st.sidebar:
    if st.button('Empréstimo'):
        emprestimo = 1
        planilhas = 0
    if st.button('Planilhas'):
        emprestimo = 0
        planilhas = 1

if emprestimo:
    with st.form("Formulário de empréstimo"):
        st.write("Insira as informações do novo empréstimo")
        nome_emprestimo = st.text_input('Nome')
        valor_emprestimo = st.text_input('Valor')
        tempo_meses = st.text_input('Meses')
        st.form_submit_button('Criar empréstimo')

xls = pd.ExcelFile('big planilha.xlsx')

if planilhas:
    planilha_selecionada = st.selectbox('Selecione a planilha desejada', ['BP_Pagamento','Condomínio Papem', 'Taxa_de_Condomínio', 'Despesas', 'ReceitasxDespesas', 'Previsão orçamentaria', 'Taxa complementar',
                                                            'Empréstimo'])
    df = pd.read_excel('big planilha.xlsx', sheet_name=planilha_selecionada)
    df = st.data_editor(df, num_rows='dynamic')

