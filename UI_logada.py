
import streamlit as st
import hashlib
import json
import os
import pandas as pd
from PyPDF2 import PdfFileReader
from streamlit_option_menu import option_menu


emprestimo = 0
planilhas = 0

with st.sidebar:
    selected = option_menu(
            "Menu",
            ["Planilhas", 'Empréstimo'],
            icons=['info', 'calculator'],)

if selected=='Empréstimo':
    with st.form("Formulário de empréstimo"):
        st.write("Insira as informações do novo empréstimo")
        nome_emprestimo = st.text_input('Nome')
        valor_emprestimo = st.text_input('Valor')
        tempo_meses = st.text_input('Meses')
        st.form_submit_button('Criar empréstimo')

elif selected=='Planilhas':
    st.title('Planilhas')
    xls = pd.ExcelFile('big planilha.xlsx')
    planilha_selecionada = st.selectbox('Selecione a planilha desejada', ['BP_Pagamento','Condomínio Papem', 'Taxa_de_Condomínio', 'Despesas', 'ReceitasxDespesas', 'Previsão orçamentaria', 'Taxa complementar', 'Empréstimo'])
    df = pd.read_excel(xls, sheet_name=planilha_selecionada)
    df = st.data_editor(df, num_rows='dynamic')

